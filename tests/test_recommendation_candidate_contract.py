from src.domain_adapters.it_application_health.itil_case_adapter import (
    ItApplicationHealthCaseAdapter,
)
from src.domain_adapters.it_application_health.itil_repository_loader import (
    ItApplicationHealthRepository,
)
from src.governance.evidence_fusion import EvidenceFusionEngine
from src.governance.recommendation_candidate import RecommendationCandidateBuilder


def build_case(scenario_id: str) -> dict:
    repository = ItApplicationHealthRepository()
    adapter = ItApplicationHealthCaseAdapter(repository)
    return adapter.build_case(scenario_id)


def build_candidate(scenario_id: str) -> dict:
    case_context = build_case(scenario_id)
    fusion = EvidenceFusionEngine().fuse(case_context)

    return RecommendationCandidateBuilder().build(
        case_context=case_context,
        fusion=fusion,
    )


def test_recommendation_candidate_contract_shape():
    candidate = build_candidate("GS-001")

    assert candidate["recommendation_id"] == "REC-CASE-GS-001"
    assert candidate["case_id"] == "CASE-GS-001"
    assert candidate["scenario_id"] == "GS-001"
    assert candidate["business_outcome"] == "Maintain Application Health"
    assert candidate["goal_category"] == "operational_troubleshooting"

    assert "summary" in candidate
    assert "risk_level" in candidate
    assert "fusion_confidence" in candidate
    assert "supporting_evidence_ids" in candidate
    assert "weakening_evidence_ids" in candidate
    assert "conflicting_evidence_ids" in candidate
    assert "missing_evidence_ids" in candidate
    assert "evidence_gap_ids" in candidate
    assert "required_controls" in candidate


def test_recommendation_candidate_always_requires_human_approval():
    for scenario_id in ["GS-001", "GS-002", "GS-003", "GS-004", "GS-005", "GS-006"]:
        candidate = build_candidate(scenario_id)

        assert candidate["requires_human_approval"] is True
        assert candidate["approval_state"] == "PENDING"
        assert candidate["autonomous_action_allowed"] is False
        assert candidate["candidate_status"] == "READY_FOR_HUMAN_REVIEW"


def test_recommendation_candidate_prohibits_autonomous_production_operations():
    candidate = build_candidate("GS-001")

    prohibited = set(candidate["prohibited_autonomous_actions"])

    assert "execute_production_change" in prohibited
    assert "modify_live_service" in prohibited
    assert "restart_live_component" in prohibited
    assert "disable_control" in prohibited
    assert "bypass_review" in prohibited


def test_high_impact_candidate_is_high_risk_and_requires_senior_review():
    candidate = build_candidate("GS-001")

    assert candidate["risk_level"] == "HIGH"
    assert "senior_owner_review_required" in candidate["required_controls"]
    assert "human_approval_required" in candidate["required_controls"]
    assert "audit_required" in candidate["required_controls"]
    assert candidate["fusion_confidence"] == "HIGH"


def test_unknown_impact_candidate_requires_impact_and_governance_review():
    candidate = build_candidate("GS-005")

    assert candidate["risk_level"] == "HIGH"
    assert candidate["fusion_confidence"] == "LOW"

    assert "impact_assessment_required" in candidate["required_controls"]
    assert "governance_debt_review_required" in candidate["required_controls"]
    assert "missing_evidence_review_required" in candidate["required_controls"]

    assert "Impact is unknown" in candidate["summary"]


def test_conflicting_evidence_candidate_requires_conflict_resolution():
    candidate = build_candidate("GS-006")

    assert candidate["risk_level"] == "HIGH"
    assert candidate["conflicting_evidence_ids"]
    assert "conflict_resolution_required" in candidate["required_controls"]
    assert "Evidence is conflicting" in candidate["summary"]


def test_conditional_knowledge_candidate_requires_corroboration():
    candidate = build_candidate("GS-003")

    assert candidate["risk_level"] == "MEDIUM"
    assert candidate["weakening_evidence_ids"]
    assert "corroboration_required" in candidate["required_controls"]


def test_candidate_contains_evidence_references_not_raw_final_decision():
    candidate = build_candidate("GS-001")

    assert candidate["supporting_evidence_ids"]
    assert "final_decision" not in candidate
    assert "truth" not in candidate
    assert "execute" not in candidate
