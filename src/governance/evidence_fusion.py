"""
Evidence fusion contract.

Classification: EAIOS Core

This module accepts a core-facing case context and produces a structured
fusion package. It does not decide final truth and does not authorize action.

The fusion package separates:
- supporting evidence
- weakening evidence
- conflicting evidence
- missing evidence
- evidence gaps

Sprint 3 adds a governed-evidence-package path while preserving the existing
domain-adapter context path.
"""

from __future__ import annotations

from typing import Any


SAFE_REASONING_STATUSES = {
    "SAFE",
    "SAFE_WITH_CONTROLS",
    "SAFE_BY_APPROVED_PROVENANCE",
}

REVIEW_REQUIRED_STATUSES = {
    "NEEDS_HUMAN_REVIEW",
    "REVIEW_REQUIRED",
    "REQUIRES_HUMAN_REVIEW",
}

LOW_TRUST_LEVELS = {
    "CONDITIONAL",
    "conditional",
    "UNKNOWN",
    "unknown",
    "UNVERIFIED",
    "unverified",
}


class FusionInputError(ValueError):
    pass


class EvidenceFusionEngine:
    def fuse(self, case_context: dict[str, Any]) -> dict[str, Any]:
        if (
            "raw_source_records" in case_context
            and "governed_evidence_package" not in case_context
        ):
            raise FusionInputError(
                "Raw ungoverned records cannot be fused. "
                "Provide governed_evidence_package."
            )

        if "governed_evidence_package" in case_context:
            return self._fuse_governed_evidence_package(case_context)

        return self._fuse_domain_context(case_context)

    def _fuse_governed_evidence_package(
        self,
        case_context: dict[str, Any],
    ) -> dict[str, Any]:
        package = self._validated_governed_evidence_package(case_context)

        supporting_evidence: list[dict[str, Any]] = []
        weakening_evidence: list[dict[str, Any]] = []
        conflicting_evidence: list[dict[str, Any]] = []
        missing_evidence: list[dict[str, Any]] = []
        evidence_gaps: list[dict[str, Any]] = list(package["evidence_gaps"])

        for evidence in package["evidence_items"]:
            if self._is_reasoning_eligible(evidence):
                supporting_evidence.append(
                    self._governed_evidence_as_supporting(evidence)
                )

                if self._has_low_trust(evidence):
                    weakening_evidence.append(
                        self._governed_evidence_as_weakening(evidence)
                    )

                if self._has_conflict_signal(evidence):
                    conflicting_evidence.append(
                        self._governed_evidence_as_conflicting(evidence)
                    )

                continue

            missing_evidence.append(
                self._governed_evidence_as_missing(evidence)
            )

            evidence_gaps.append(
                self._governed_evidence_gap_for_excluded_item(evidence)
            )

        fusion_confidence = self._governed_fusion_confidence(
            case_context=case_context,
            conflicting_evidence=conflicting_evidence,
            missing_evidence=missing_evidence,
            weakening_evidence=weakening_evidence,
            evidence_gaps=evidence_gaps,
        )

        requires_human_review = (
            case_context.get("human_approval_required", True)
            or bool(conflicting_evidence)
            or bool(missing_evidence)
            or bool(evidence_gaps)
            or case_context.get("impact", {}).get("impact_tier") == "UNKNOWN"
        )

        return {
            "fusion_id": f"FUSION-{case_context['case_id']}",
            "case_id": case_context["case_id"],
            "scenario_id": case_context.get("scenario_id"),
            "business_outcome": case_context["business_outcome"],
            "goal_category": case_context["goal_category"],
            "governed_package_id": package["package_id"],
            "supporting_evidence": supporting_evidence,
            "weakening_evidence": weakening_evidence,
            "conflicting_evidence": conflicting_evidence,
            "missing_evidence": missing_evidence,
            "evidence_gaps": evidence_gaps,
            "audit_ids": self._audit_ids(package),
            "reasoning_eligible_evidence_ids": [
                evidence["evidence_id"] for evidence in supporting_evidence
            ],
            "excluded_evidence_ids": [
                evidence["evidence_id"] for evidence in missing_evidence
            ],
            "fusion_confidence": fusion_confidence,
            "requires_human_review": requires_human_review,
            "autonomous_action_allowed": False,
        }

    def _validated_governed_evidence_package(
        self,
        case_context: dict[str, Any],
    ) -> dict[str, Any]:
        package = case_context.get("governed_evidence_package")

        if not isinstance(package, dict):
            raise FusionInputError("governed_evidence_package must be a dictionary.")

        if not package.get("package_id"):
            raise FusionInputError("governed_evidence_package.package_id is required.")

        evidence_items = package.get("evidence_items")
        evidence_gaps = package.get("evidence_gaps")

        if not isinstance(evidence_items, list):
            raise FusionInputError(
                "governed_evidence_package.evidence_items must be a list."
            )

        if not isinstance(evidence_gaps, list):
            raise FusionInputError(
                "governed_evidence_package.evidence_gaps must be a list."
            )

        if not evidence_items and not evidence_gaps:
            raise FusionInputError(
                "governed_evidence_package must contain evidence_items or evidence_gaps."
            )

        for index, evidence in enumerate(evidence_items):
            self._validate_governed_evidence_item(evidence, index)

        for index, gap in enumerate(evidence_gaps):
            self._validate_governed_evidence_gap(gap, index)

        return package

    def _validate_governed_evidence_item(
        self,
        evidence: dict[str, Any],
        index: int,
    ) -> None:
        required_fields = {
            "evidence_id",
            "source_id",
            "agent_id",
            "access_decision",
            "audit_id",
            "content_safety_status",
            "allowed_for_reasoning",
            "evidence_class",
        }

        missing = sorted(field for field in required_fields if field not in evidence)

        if missing:
            raise FusionInputError(
                f"governed_evidence_package.evidence_items[{index}] "
                f"missing required fields: {', '.join(missing)}"
            )

        if evidence["access_decision"] != "ALLOW":
            raise FusionInputError(
                "Denied source access must be represented as an evidence gap, "
                "not as an evidence item."
            )

    def _validate_governed_evidence_gap(
        self,
        gap: dict[str, Any],
        index: int,
    ) -> None:
        required_fields = {
            "gap_id",
            "source_id",
            "agent_id",
            "reason",
        }

        missing = sorted(field for field in required_fields if field not in gap)

        if missing:
            raise FusionInputError(
                f"governed_evidence_package.evidence_gaps[{index}] "
                f"missing required fields: {', '.join(missing)}"
            )

    def _is_reasoning_eligible(self, evidence: dict[str, Any]) -> bool:
        return (
            evidence.get("allowed_for_reasoning") is True
            and evidence.get("content_safety_status") in SAFE_REASONING_STATUSES
        )

    def _has_low_trust(self, evidence: dict[str, Any]) -> bool:
        payload = evidence.get("payload", {})

        return (
            evidence.get("trust_level") in LOW_TRUST_LEVELS
            or evidence.get("source_trust_level") in LOW_TRUST_LEVELS
            or payload.get("trust_level") in LOW_TRUST_LEVELS
            or payload.get("source_trust_level") in LOW_TRUST_LEVELS
        )

    def _has_conflict_signal(self, evidence: dict[str, Any]) -> bool:
        payload = evidence.get("payload", {})

        return bool(
            evidence.get("conflicts_with")
            or evidence.get("conflict")
            or payload.get("conflicts_with")
            or payload.get("conflict")
        )

    def _governed_evidence_as_supporting(
        self,
        evidence: dict[str, Any],
    ) -> dict[str, Any]:
        payload = evidence.get("payload", {})

        return {
            "evidence_id": evidence["evidence_id"],
            "evidence_type": evidence["evidence_class"],
            "source_id": evidence["source_id"],
            "agent_id": evidence["agent_id"],
            "audit_id": evidence["audit_id"],
            "content_safety_status": evidence["content_safety_status"],
            "summary": payload.get("summary") or evidence.get("summary", ""),
            "supports": evidence.get("purpose", "case_context"),
            "governed": True,
        }

    def _governed_evidence_as_weakening(
        self,
        evidence: dict[str, Any],
    ) -> dict[str, Any]:
        payload = evidence.get("payload", {})

        return {
            "evidence_id": f"WEAK-{evidence['evidence_id']}",
            "evidence_type": "source_trust_limitation",
            "source_id": evidence["source_id"],
            "agent_id": evidence["agent_id"],
            "audit_id": evidence["audit_id"],
            "summary": payload.get("summary") or evidence.get("summary", ""),
            "weakens": "confidence_without_corroboration",
            "governed": True,
        }

    def _governed_evidence_as_conflicting(
        self,
        evidence: dict[str, Any],
    ) -> dict[str, Any]:
        payload = evidence.get("payload", {})

        return {
            "evidence_id": f"CONFLICT-{evidence['evidence_id']}",
            "evidence_type": "governed_evidence_conflict",
            "source_id": evidence["source_id"],
            "agent_id": evidence["agent_id"],
            "audit_id": evidence["audit_id"],
            "summary": payload.get("summary") or evidence.get("summary", ""),
            "conflicts_with": (
                evidence.get("conflicts_with")
                or evidence.get("conflict")
                or payload.get("conflicts_with")
                or payload.get("conflict")
            ),
            "governed": True,
        }

    def _governed_evidence_as_missing(
        self,
        evidence: dict[str, Any],
    ) -> dict[str, Any]:
        safety_status = evidence["content_safety_status"]

        if safety_status in REVIEW_REQUIRED_STATUSES:
            evidence_type = "missing_human_validation"
            summary = "Human validation is required before reasoning use."
        elif safety_status == "UNSAFE":
            evidence_type = "excluded_unsafe_content"
            summary = "Evidence was excluded from reasoning by safety controls."
        else:
            evidence_type = "excluded_non_reasoning_evidence"
            summary = "Evidence was not eligible for reasoning."

        return {
            "evidence_id": evidence["evidence_id"],
            "evidence_type": evidence_type,
            "source_id": evidence["source_id"],
            "agent_id": evidence["agent_id"],
            "audit_id": evidence["audit_id"],
            "content_safety_status": safety_status,
            "summary": summary,
            "governed": True,
        }

    def _governed_evidence_gap_for_excluded_item(
        self,
        evidence: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "gap_id": f"GAP-{evidence['evidence_id']}",
            "gap_type": "reasoning_eligible_evidence_unavailable",
            "source_id": evidence["source_id"],
            "agent_id": evidence["agent_id"],
            "audit_id": evidence["audit_id"],
            "reason": "Evidence was collected but excluded from reasoning.",
        }

    def _audit_ids(self, package: dict[str, Any]) -> list[str]:
        audit_ids = {
            evidence["audit_id"]
            for evidence in package["evidence_items"]
            if evidence.get("audit_id")
        }

        audit_ids.update(
            gap["audit_id"]
            for gap in package["evidence_gaps"]
            if gap.get("audit_id")
        )

        return sorted(audit_ids)

    def _governed_fusion_confidence(
        self,
        *,
        case_context: dict[str, Any],
        conflicting_evidence: list[dict[str, Any]],
        missing_evidence: list[dict[str, Any]],
        weakening_evidence: list[dict[str, Any]],
        evidence_gaps: list[dict[str, Any]],
    ) -> str:
        if case_context.get("impact", {}).get("impact_tier") == "UNKNOWN":
            return "LOW"

        if conflicting_evidence or missing_evidence or evidence_gaps:
            return "LOW"

        if weakening_evidence:
            return "MEDIUM"

        return case_context.get("impact", {}).get("impact_confidence", "HIGH")

    def _fuse_domain_context(self, case_context: dict[str, Any]) -> dict[str, Any]:
        supporting_evidence: list[dict[str, Any]] = []
        weakening_evidence: list[dict[str, Any]] = []
        conflicting_evidence: list[dict[str, Any]] = []
        missing_evidence: list[dict[str, Any]] = []
        evidence_gaps: list[dict[str, Any]] = []

        supporting_evidence.extend(
            self._observations_as_supporting(case_context)
        )
        supporting_evidence.extend(
            self._context_as_supporting(case_context)
        )

        weakening_evidence.extend(
            self._low_trust_context_as_weakening(case_context)
        )

        conflicting_evidence.extend(
            self._conflict_candidates(case_context)
        )

        missing_evidence.extend(
            self._missing_impact_evidence(case_context)
        )
        missing_evidence.extend(
            self._missing_validation_evidence(case_context)
        )

        evidence_gaps.extend(
            self._evidence_gaps(
                case_context=case_context,
                conflicting_evidence=conflicting_evidence,
                missing_evidence=missing_evidence,
            )
        )

        fusion_confidence = self._fusion_confidence(
            case_context=case_context,
            conflicting_evidence=conflicting_evidence,
            missing_evidence=missing_evidence,
            weakening_evidence=weakening_evidence,
        )

        requires_human_review = (
            case_context["human_approval_required"]
            or bool(conflicting_evidence)
            or bool(missing_evidence)
            or case_context["impact"]["impact_tier"] == "UNKNOWN"
        )

        return {
            "fusion_id": f"FUSION-{case_context['case_id']}",
            "case_id": case_context["case_id"],
            "scenario_id": case_context["scenario_id"],
            "business_outcome": case_context["business_outcome"],
            "goal_category": case_context["goal_category"],
            "supporting_evidence": supporting_evidence,
            "weakening_evidence": weakening_evidence,
            "conflicting_evidence": conflicting_evidence,
            "missing_evidence": missing_evidence,
            "evidence_gaps": evidence_gaps,
            "fusion_confidence": fusion_confidence,
            "requires_human_review": requires_human_review,
            "autonomous_action_allowed": False,
        }

    def _observations_as_supporting(
        self,
        case_context: dict[str, Any],
    ) -> list[dict[str, Any]]:
        return [
            {
                "evidence_id": observation["observation_id"],
                "evidence_type": observation["observation_type"],
                "source_record_id": observation["source_record_id"],
                "entity_id": observation["entity_id"],
                "summary": observation["summary"],
                "supports": "case_under_investigation",
            }
            for observation in case_context["observations"]
        ]

    def _context_as_supporting(
        self,
        case_context: dict[str, Any],
    ) -> list[dict[str, Any]]:
        supporting: list[dict[str, Any]] = []
        context_records = case_context["context_records"]

        for group_name, evidence_type in [
            ("problem_context", "pattern_context"),
            ("knowledge_context", "knowledge_context"),
            ("change_context", "lifecycle_context"),
            ("memory_context", "memory_context"),
        ]:
            for record in context_records[group_name]:
                supporting.append(
                    {
                        "evidence_id": f"EVIDENCE-{record['record_id']}",
                        "evidence_type": evidence_type,
                        "source_record_id": record["record_id"],
                        "entity_id": record["entity_id"],
                        "summary": record["summary"],
                        "supports": "case_context",
                    }
                )

        return supporting

    def _low_trust_context_as_weakening(
        self,
        case_context: dict[str, Any],
    ) -> list[dict[str, Any]]:
        weakening: list[dict[str, Any]] = []

        for record in case_context["context_records"]["knowledge_context"]:
            if record["trust_level"] in {"conditional", "unknown"}:
                weakening.append(
                    {
                        "evidence_id": f"WEAK-{record['record_id']}",
                        "evidence_type": "source_trust_limitation",
                        "source_record_id": record["record_id"],
                        "entity_id": record["entity_id"],
                        "summary": record["summary"],
                        "weakens": "confidence_without_corroboration",
                    }
                )

        for record in case_context["context_records"]["memory_context"]:
            if record["validation_state"] != "HUMAN_VALIDATED":
                weakening.append(
                    {
                        "evidence_id": f"WEAK-{record['record_id']}",
                        "evidence_type": "memory_validation_limitation",
                        "source_record_id": record["record_id"],
                        "entity_id": record["entity_id"],
                        "summary": record["summary"],
                        "weakens": "memory_reuse_without_validation",
                    }
                )

        return weakening

    def _conflict_candidates(
        self,
        case_context: dict[str, Any],
    ) -> list[dict[str, Any]]:
        observed_entities = {
            observation["entity_id"]
            for observation in case_context["observations"]
        }

        if (
            case_context["impact"]["impact_confidence"] == "LOW"
            and len(observed_entities) > 1
        ):
            return [
                {
                    "evidence_id": f"CONFLICT-{case_context['case_id']}",
                    "evidence_type": "multi_entity_low_confidence_conflict",
                    "source_record_id": case_context["case_id"],
                    "entity_ids": sorted(observed_entities),
                    "summary": (
                        "Multiple observed entities are present while impact "
                        "confidence is low; additional evidence is required."
                    ),
                    "conflicts_with": "single_cause_assumption",
                }
            ]

        return []

    def _missing_impact_evidence(
        self,
        case_context: dict[str, Any],
    ) -> list[dict[str, Any]]:
        if case_context["impact"]["impact_tier"] != "UNKNOWN":
            return []

        return [
            {
                "evidence_id": f"MISSING-IMPACT-{case_context['case_id']}",
                "evidence_type": "missing_impact_mapping",
                "source_record_id": case_context["case_id"],
                "summary": "Business impact mapping is missing.",
                "required_action": case_context["impact"]["required_action"],
                "governance_debt": case_context["impact"]["governance_debt"],
            }
        ]

    def _missing_validation_evidence(
        self,
        case_context: dict[str, Any],
    ) -> list[dict[str, Any]]:
        missing: list[dict[str, Any]] = []

        for record in case_context["context_records"]["knowledge_context"]:
            if record["expected_content_safety"] == "NEEDS_HUMAN_REVIEW":
                missing.append(
                    {
                        "evidence_id": f"MISSING-VALIDATION-{record['record_id']}",
                        "evidence_type": "missing_human_validation",
                        "source_record_id": record["record_id"],
                        "entity_id": record["entity_id"],
                        "summary": "Human validation is required before reasoning use.",
                    }
                )

        return missing

    def _evidence_gaps(
        self,
        *,
        case_context: dict[str, Any],
        conflicting_evidence: list[dict[str, Any]],
        missing_evidence: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        gaps: list[dict[str, Any]] = []

        if conflicting_evidence:
            gaps.append(
                {
                    "gap_id": f"GAP-CONFLICT-{case_context['case_id']}",
                    "gap_type": "conflict_resolution_required",
                    "summary": "Conflicting signals require additional investigation.",
                }
            )

        if missing_evidence:
            gaps.append(
                {
                    "gap_id": f"GAP-MISSING-{case_context['case_id']}",
                    "gap_type": "missing_required_evidence",
                    "summary": "Required evidence is missing or requires validation.",
                }
            )

        return gaps

    def _fusion_confidence(
        self,
        *,
        case_context: dict[str, Any],
        conflicting_evidence: list[dict[str, Any]],
        missing_evidence: list[dict[str, Any]],
        weakening_evidence: list[dict[str, Any]],
    ) -> str:
        if case_context["impact"]["impact_tier"] == "UNKNOWN":
            return "LOW"

        if conflicting_evidence or missing_evidence:
            return "LOW"

        if weakening_evidence:
            return "MEDIUM"

        return case_context["impact"]["impact_confidence"]
