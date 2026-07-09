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
"""

from __future__ import annotations

from typing import Any


class EvidenceFusionEngine:
    def fuse(self, case_context: dict[str, Any]) -> dict[str, Any]:
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
