from __future__ import annotations

from datetime import date, datetime
from typing import Any


class ContentSafetyGateway:
    """
    Sprint 2 deterministic content-safety gateway.

    Rule precedence is first-match-wins:
    1. Prompt injection -> UNSAFE
    2. Unsafe operational command without validation language -> NEEDS_HUMAN_REVIEW
    3. Missing item owner -> NEEDS_HUMAN_REVIEW
    4. Low trust -> SUPPORTING_ONLY
    5. Stale content with owner -> SUPPORTING_ONLY
    6. Conditional fresh content -> SUPPORTING_ONLY
    7. Approved operational content -> SAFE_WITH_CONTROLS
    8. Approved non-operational content -> SAFE
    """

    STALE_THRESHOLD_DAYS = 180

    PROMPT_INJECTION_PATTERNS = [
        "ignore previous instructions",
        "bypass policy",
        "override governance",
        "disable guardrails",
        "ignore governance",
        "act outside policy",
    ]

    UNSAFE_OPERATIONAL_PATTERNS = [
        "restart production",
        "delete records",
        "disable monitoring",
        "shutdown service",
        "drop table",
        "force deploy",
        "bypass approval",
    ]

    VALIDATION_LANGUAGE_PATTERNS = [
        "validate",
        "validation",
        "confirm",
        "approved change",
        "change ticket",
        "human approval",
        "rollback plan",
        "maintenance window",
    ]

    LOW_TRUST_LEVELS = {None, "", "unverified", "unknown"}

    def evaluate(
        self,
        *,
        content: str,
        trust_level: str | None,
        item_owner: str | None,
        item_last_validated: str | None,
        collected_at: str,
    ) -> dict[str, Any]:
        normalized_content = self._normalize(content)
        normalized_trust = self._normalize(trust_level)

        if self._contains_any(normalized_content, self.PROMPT_INJECTION_PATTERNS):
            return self._result(
                status="UNSAFE",
                allowed_for_reasoning=False,
                usage_level="blocked",
                authoritative=False,
                reason="Prompt-injection-like content matched a blocked pattern.",
                required_controls=[],
            )

        if (
            self._contains_any(normalized_content, self.UNSAFE_OPERATIONAL_PATTERNS)
            and not self._contains_any(normalized_content, self.VALIDATION_LANGUAGE_PATTERNS)
        ):
            return self._result(
                status="NEEDS_HUMAN_REVIEW",
                allowed_for_reasoning=False,
                usage_level="blocked_pending_review",
                authoritative=False,
                reason="Production-impacting command lacks validation language.",
                required_controls=["human_review", "approved_change_required"],
            )

        if not item_owner or not str(item_owner).strip():
            return self._result(
                status="NEEDS_HUMAN_REVIEW",
                allowed_for_reasoning=False,
                usage_level="not_authoritative",
                authoritative=False,
                reason="Knowledge item is missing item-level ownership.",
                required_controls=["assign_item_owner", "human_review"],
            )

        if normalized_trust in self.LOW_TRUST_LEVELS:
            return self._result(
                status="SUPPORTING_ONLY",
                allowed_for_reasoning=True,
                usage_level="supporting",
                authoritative=False,
                reason="Low-trust content may support reasoning but cannot drive a recommendation.",
                required_controls=["corroborating_evidence_required"],
            )

        if self.is_stale(item_last_validated=item_last_validated, collected_at=collected_at):
            return self._result(
                status="SUPPORTING_ONLY",
                allowed_for_reasoning=True,
                usage_level="supporting",
                authoritative=False,
                reason="Stale content with item owner may support investigation but is not authoritative.",
                required_controls=["fresh_validation_required"],
            )

        if normalized_trust == "conditional":
            return self._result(
                status="SUPPORTING_ONLY",
                allowed_for_reasoning=True,
                usage_level="supporting",
                authoritative=False,
                reason="Conditional source content may support reasoning but is not authoritative.",
                required_controls=["authoritative_source_required"],
            )

        if normalized_trust == "approved" and self._contains_any(
            normalized_content, self.UNSAFE_OPERATIONAL_PATTERNS
        ):
            return self._result(
                status="SAFE_WITH_CONTROLS",
                allowed_for_reasoning=True,
                usage_level="authoritative",
                authoritative=True,
                reason="Approved operational content may be used with required validation controls.",
                required_controls=["human_validation", "check_recent_changes"],
            )

        if normalized_trust == "approved":
            return self._result(
                status="SAFE",
                allowed_for_reasoning=True,
                usage_level="authoritative",
                authoritative=True,
                reason="Approved non-operational content may be used normally.",
                required_controls=[],
            )

        return self._result(
            status="SUPPORTING_ONLY",
            allowed_for_reasoning=True,
            usage_level="supporting",
            authoritative=False,
            reason="Content did not qualify as authoritative and is limited to supporting use.",
            required_controls=["corroborating_evidence_required"],
        )

    def is_stale(self, *, item_last_validated: str | None, collected_at: str) -> bool:
        if not item_last_validated:
            return True

        item_date = self._parse_date(item_last_validated)
        collected_date = self._parse_date(collected_at)

        if item_date is None or collected_date is None:
            return True

        return (collected_date - item_date).days > self.STALE_THRESHOLD_DAYS

    def _result(
        self,
        *,
        status: str,
        allowed_for_reasoning: bool,
        usage_level: str,
        authoritative: bool,
        reason: str,
        required_controls: list[str],
    ) -> dict[str, Any]:
        return {
            "content_safety": {
                "status": status,
                "allowed_for_reasoning": allowed_for_reasoning,
                "reason": reason,
                "required_controls": required_controls,
            },
            "usage": {
                "level": usage_level,
                "authoritative": authoritative,
                "reason": reason,
            },
        }

    def _contains_any(self, content: str, patterns: list[str]) -> bool:
        return any(pattern in content for pattern in patterns)

    def _normalize(self, value: str | None) -> str:
        if value is None:
            return ""
        return str(value).strip().lower()

    def _parse_date(self, value: str | None) -> date | None:
        if not value:
            return None

        try:
            return datetime.fromisoformat(str(value).replace("Z", "+00:00")).date()
        except ValueError:
            try:
                return date.fromisoformat(str(value)[:10])
            except ValueError:
                return None