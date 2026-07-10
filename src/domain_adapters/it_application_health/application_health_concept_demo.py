"""
Application Health concept demo.

Classification: Domain Adapter

This module demonstrates the Sprint 2.5c concept path:

Business Outcome
→ Domain Repository
→ Case Context
→ Evidence Fusion
→ Reasoning Explanation
→ Recommendation Candidate
→ Human Review Package

It does not execute actions or modify production systems.
"""

from __future__ import annotations

from typing import Any

from src.domain_adapters.it_application_health.itil_case_adapter import (
    ItApplicationHealthCaseAdapter,
)
from src.domain_adapters.it_application_health.itil_repository_loader import (
    ItApplicationHealthRepository,
)
from src.governance.evidence_fusion import EvidenceFusionEngine
from src.governance.reasoning_explanation import ReasoningExplanationEngine
from src.governance.recommendation_candidate import RecommendationCandidateBuilder


class ApplicationHealthConceptDemo:
    def __init__(self) -> None:
        self.repository = ItApplicationHealthRepository()
        self.case_adapter = ItApplicationHealthCaseAdapter(self.repository)
        self.fusion_engine = EvidenceFusionEngine()
        self.reasoning_engine = ReasoningExplanationEngine()
        self.recommendation_builder = RecommendationCandidateBuilder()

    def run(self, scenario_id: str) -> dict[str, Any]:
        case_context = self.case_adapter.build_case(scenario_id)
        fusion = self.fusion_engine.fuse(case_context)
        reasoning = self.reasoning_engine.explain(
            case_context=case_context,
            fusion=fusion,
        )
        recommendation_candidate = self.recommendation_builder.build(
            case_context=case_context,
            fusion=fusion,
            reasoning=reasoning,
        )

        return {
            "demo_id": f"APP-HEALTH-DEMO-{scenario_id}",
            "scenario_id": scenario_id,
            "business_outcome": case_context["business_outcome"],
            "goal_category": case_context["goal_category"],
            "case_context": case_context,
            "evidence_fusion": fusion,
            "reasoning_explanation": reasoning,
            "recommendation_candidate": recommendation_candidate,
            "human_review_package": self._human_review_package(
                case_context=case_context,
                fusion=fusion,
                reasoning=reasoning,
                recommendation_candidate=recommendation_candidate,
            ),
            "safety_summary": {
                "requires_human_approval": recommendation_candidate[
                    "requires_human_approval"
                ],
                "approval_state": recommendation_candidate["approval_state"],
                "autonomous_action_allowed": False,
                "candidate_status": recommendation_candidate["candidate_status"],
            },
        }

    def _human_review_package(
        self,
        *,
        case_context: dict[str, Any],
        fusion: dict[str, Any],
        reasoning: dict[str, Any],
        recommendation_candidate: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "review_id": f"REVIEW-{case_context['case_id']}",
            "case_id": case_context["case_id"],
            "business_outcome": case_context["business_outcome"],
            "case_summary": case_context["case_summary"],
            "impact": case_context["impact"],
            "fusion_confidence": fusion["fusion_confidence"],
            "reasoning_id": reasoning["reasoning_id"],
            "selected_hypothesis_id": reasoning["selected_hypothesis_id"],
            "reasoning_confidence": reasoning["reasoning_confidence"],
            "reasoning_summary": reasoning["reasoning_summary"],
            "recommendation_id": recommendation_candidate["recommendation_id"],
            "recommendation_summary": recommendation_candidate["summary"],
            "approval_state": recommendation_candidate["approval_state"],
            "candidate_status": recommendation_candidate["candidate_status"],
            "supporting_evidence_count": len(fusion["supporting_evidence"]),
            "weakening_evidence_count": len(fusion["weakening_evidence"]),
            "conflicting_evidence_count": len(fusion["conflicting_evidence"]),
            "missing_evidence_count": len(fusion["missing_evidence"]),
            "evidence_gap_count": len(fusion["evidence_gaps"]),
            "risk_level": recommendation_candidate["risk_level"],
            "required_controls": recommendation_candidate["required_controls"],
            "requires_human_approval": True,
            "autonomous_action_allowed": False,
        }
