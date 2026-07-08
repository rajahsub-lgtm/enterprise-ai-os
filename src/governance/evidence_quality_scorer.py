from __future__ import annotations

from typing import Any

from src.governance.content_safety_gateway import ContentSafetyGateway


class EvidenceQualityScorer:
    """
    Sprint 2 deterministic quality scorer.

    Quality is metadata confidence, not safety.
    Unsafe content can still have metadata quality, but safety gates decide use.
    """

    def __init__(self) -> None:
        self.safety_gateway = ContentSafetyGateway()

    def score(
        self,
        *,
        source_metadata: dict[str, Any],
        knowledge_item: dict[str, Any],
        trust_level: str | None,
        collected_at: str,
        content_hash: str,
    ) -> dict[str, Any]:
        signals: list[str] = []
        score = 0.0

        normalized_trust = self._normalize(trust_level)

        if normalized_trust == "approved":
            score += 0.35
            signals.append("approved_source")
        elif normalized_trust == "conditional":
            score += 0.25
            signals.append("conditional_source")
        else:
            score += 0.10
            signals.append("low_trust_source")

        if source_metadata.get("owner"):
            score += 0.15
            signals.append("source_owner_present")
        else:
            signals.append("source_owner_missing")

        if knowledge_item.get("item_owner"):
            score += 0.15
            signals.append("item_owner_present")
        else:
            signals.append("item_owner_missing")

        if knowledge_item.get("item_last_validated"):
            score += 0.15
            signals.append("item_last_validated_present")

            if self.safety_gateway.is_stale(
                item_last_validated=knowledge_item.get("item_last_validated"),
                collected_at=collected_at,
            ):
                signals.append("stale_content")
            else:
                score += 0.15
                signals.append("fresh_content")
        else:
            signals.append("item_last_validated_missing")

        if content_hash:
            score += 0.05
            signals.append("content_hash_present")

        score = min(round(score, 2), 1.0)

        return {
            "score": score,
            "level": self._level(score),
            "signals": signals,
        }

    def _level(self, score: float) -> str:
        if score >= 0.80:
            return "HIGH"
        if score >= 0.50:
            return "MEDIUM"
        return "LOW"

    def _normalize(self, value: str | None) -> str:
        if value is None:
            return ""
        return str(value).strip().lower()