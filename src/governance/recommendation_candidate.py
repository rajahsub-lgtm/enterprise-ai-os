"""
Recommendation candidate contract.

Classification: EAIOS Core

This module creates a recommendation candidate from a case context, evidence
fusion package, and optional reasoning explanation. It does not execute
anything. It does not authorize automated production operation. It prepares a
human-review package.

Core rule:
Every production-impacting recommendation candidate requires human approval.
"""

from __future__ import annotations

from typing import Any


class RecommendationCandidateBuilder:
    def build(
        self,
        *,
        case_context: dict[str, Any],
        fusion: dict[str, Any],
        reasoning: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        risk_level = self._risk_level(case_context=case_context, fusion=fusion)
        required_controls = self._required_controls(
            case_context=case_context,
            fusion=fusion,
            risk_level=risk_level,
            reasoning=reasoning,
        )

        return {
            "recommendation_id": f"REC-{case_context['case_id']}",
            "case_id": case_context["case_id"],
            "scenario_id": case_context["scenario_id"],
            "business_outcome": case_context["business_outcome"],
            "goal_category": case_context["goal_category"],
            "summary": self._summary(
                case_context=case_context,
                fusion=fusion,
                reasoning=reasoning,
            ),
            "risk_level": risk_level,
            "fusion_confidence": fusion["fusion_confidence"],
            "reasoning_id": reasoning["reasoning_id"] if reasoning else None,
            "selected_hypothesis_id": (
                reasoning["selected_hypothesis_id"] if reasoning else None
            ),
            "reasoning_confidence": (
                reasoning["reasoning_confidence"] if reasoning else None
            ),
            "reasoning_summary": (
                reasoning["reasoning_summary"] if reasoning else None
            ),
            "supporting_evidence_ids": [
                evidence["evidence_id"]
                for evidence in fusion["supporting_evidence"]
            ],
            "weakening_evidence_ids": [
                evidence["evidence_id"]
                for evidence in fusion["weakening_evidence"]
            ],
            "conflicting_evidence_ids": [
                evidence["evidence_id"]
                for evidence in fusion["conflicting_evidence"]
            ],
            "missing_evidence_ids": [
                evidence["evidence_id"]
                for evidence in fusion["missing_evidence"]
            ],
            "evidence_gap_ids": [
                gap["gap_id"]
                for gap in fusion["evidence_gaps"]
            ],
            "required_controls": required_controls,
            "requires_human_approval": True,
            "approval_state": "PENDING",
            "autonomous_action_allowed": False,
            "prohibited_autonomous_actions": [
                "execute_production_change",
                "modify_live_service",
                "restart_live_component",
                "disable_control",
                "bypass_review",
            ],
            "candidate_status": "READY_FOR_HUMAN_REVIEW",
        }

    def _summary(
        self,
        *,
        case_context: dict[str, Any],
        fusion: dict[str, Any],
        reasoning: dict[str, Any] | None,
    ) -> str:
        if case_context["impact"]["impact_tier"] == "UNKNOWN":
            return (
                "Impact is unknown. Escalate for impact assessment before "
                "any production-impacting decision."
            )

        if fusion["conflicting_evidence"]:
            return (
                "Evidence is conflicting. Gather additional evidence and route "
                "the candidate for human review."
            )

        if fusion["missing_evidence"]:
            return (
                "Required evidence is missing. Complete validation before "
                "making a production-impacting decision."
            )

        if reasoning:
            return (
                "Reasoning explanation is prepared for human review: "
                f"{reasoning['reasoning_summary']}"
            )

        return (
            "Evidence package is prepared for human review. Proceed only after "
            "required controls and approval are satisfied."
        )

    def _risk_level(
        self,
        *,
        case_context: dict[str, Any],
        fusion: dict[str, Any],
    ) -> str:
        impact_tier = case_context["impact"]["impact_tier"]

        if impact_tier == "UNKNOWN":
            return "HIGH"

        if fusion["conflicting_evidence"] or fusion["missing_evidence"]:
            return "HIGH"

        if impact_tier == "HIGH":
            return "HIGH"

        if fusion["weakening_evidence"]:
            return "MEDIUM"

        return "MEDIUM"

    def _required_controls(
        self,
        *,
        case_context: dict[str, Any],
        fusion: dict[str, Any],
        risk_level: str,
        reasoning: dict[str, Any] | None,
    ) -> list[str]:
        controls = {
            "human_approval_required",
            "audit_required",
            "evidence_review_required",
        }

        if reasoning:
            controls.add("reasoning_review_required")

        if risk_level == "HIGH":
            controls.add("senior_owner_review_required")

        if case_context["impact"]["impact_tier"] == "UNKNOWN":
            controls.add("impact_assessment_required")
            controls.add("governance_debt_review_required")

        if fusion["conflicting_evidence"]:
            controls.add("conflict_resolution_required")

        if fusion["missing_evidence"]:
            controls.add("missing_evidence_review_required")

        if fusion["weakening_evidence"]:
            controls.add("corroboration_required")

        return sorted(controls)
