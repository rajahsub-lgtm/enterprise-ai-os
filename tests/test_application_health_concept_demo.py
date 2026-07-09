from src.domain_adapters.it_application_health.application_health_concept_demo import (
    ApplicationHealthConceptDemo,
)


def run_demo(scenario_id: str) -> dict:
    return ApplicationHealthConceptDemo().run(scenario_id)


def test_application_health_demo_runs_business_outcome_to_human_review_package():
    result = run_demo("GS-001")

    assert result["demo_id"] == "APP-HEALTH-DEMO-GS-001"
    assert result["business_outcome"] == "Maintain Application Health"
    assert result["goal_category"] == "operational_troubleshooting"

    assert result["case_context"]["case_id"] == "CASE-GS-001"
    assert result["evidence_fusion"]["fusion_id"] == "FUSION-CASE-GS-001"
    assert result["recommendation_candidate"]["recommendation_id"] == "REC-CASE-GS-001"
    assert result["human_review_package"]["review_id"] == "REVIEW-CASE-GS-001"


def test_application_health_demo_preserves_human_approval_boundary():
    for scenario_id in ["GS-001", "GS-002", "GS-003", "GS-004", "GS-005", "GS-006"]:
        result = run_demo(scenario_id)

        assert result["safety_summary"]["requires_human_approval"] is True
        assert result["safety_summary"]["approval_state"] == "PENDING"
        assert result["safety_summary"]["autonomous_action_allowed"] is False

        assert result["human_review_package"]["requires_human_approval"] is True
        assert result["human_review_package"]["autonomous_action_allowed"] is False

        assert result["recommendation_candidate"]["requires_human_approval"] is True
        assert result["recommendation_candidate"]["autonomous_action_allowed"] is False


def test_application_health_demo_unknown_impact_routes_to_review():
    result = run_demo("GS-005")

    impact = result["case_context"]["impact"]
    fusion = result["evidence_fusion"]
    candidate = result["recommendation_candidate"]
    review = result["human_review_package"]

    assert impact["impact_tier"] == "UNKNOWN"
    assert impact["required_action"] == "ESCALATE_FOR_IMPACT_ASSESSMENT"
    assert impact["governance_debt"] == "missing_business_impact_mapping"

    assert fusion["fusion_confidence"] == "LOW"
    assert fusion["missing_evidence"]
    assert candidate["risk_level"] == "HIGH"

    assert "impact_assessment_required" in review["required_controls"]
    assert "governance_debt_review_required" in review["required_controls"]


def test_application_health_demo_conflicting_evidence_routes_to_review():
    result = run_demo("GS-006")

    fusion = result["evidence_fusion"]
    candidate = result["recommendation_candidate"]
    review = result["human_review_package"]

    assert fusion["conflicting_evidence"]
    assert fusion["fusion_confidence"] == "LOW"
    assert candidate["risk_level"] == "HIGH"

    assert review["conflicting_evidence_count"] >= 1
    assert "conflict_resolution_required" in review["required_controls"]


def test_application_health_demo_known_error_memory_remains_reviewable_evidence():
    result = run_demo("GS-002")

    case_context = result["case_context"]
    fusion = result["evidence_fusion"]
    candidate = result["recommendation_candidate"]

    memory_context = case_context["context_records"]["memory_context"]

    assert memory_context
    assert memory_context[0]["validation_state"] == "HUMAN_VALIDATED"
    assert memory_context[0]["confidence"] == "MEDIUM"

    memory_evidence = [
        evidence
        for evidence in fusion["supporting_evidence"]
        if evidence["evidence_type"] == "memory_context"
    ]

    assert memory_evidence
    assert candidate["requires_human_approval"] is True
    assert candidate["autonomous_action_allowed"] is False


def test_application_health_demo_high_impact_case_requires_senior_review():
    result = run_demo("GS-001")

    candidate = result["recommendation_candidate"]
    review = result["human_review_package"]

    assert result["case_context"]["impact"]["impact_tier"] == "HIGH"
    assert candidate["risk_level"] == "HIGH"
    assert "senior_owner_review_required" in candidate["required_controls"]
    assert "senior_owner_review_required" in review["required_controls"]


def test_application_health_demo_output_has_no_final_truth_or_action_execution():
    result = run_demo("GS-001")

    assert "final_decision" not in result
    assert "execution_result" not in result
    assert "production_action" not in result

    assert "final_decision" not in result["recommendation_candidate"]
    assert "execution_result" not in result["recommendation_candidate"]
    assert "production_action" not in result["recommendation_candidate"]

    assert result["safety_summary"]["autonomous_action_allowed"] is False


def test_application_health_demo_all_scenarios_complete_e2e_path():
    for scenario_id in ["GS-001", "GS-002", "GS-003", "GS-004", "GS-005", "GS-006"]:
        result = run_demo(scenario_id)

        assert result["case_context"]
        assert result["evidence_fusion"]
        assert result["recommendation_candidate"]
        assert result["human_review_package"]

        assert result["case_context"]["business_outcome"] == "Maintain Application Health"
        assert result["evidence_fusion"]["business_outcome"] == "Maintain Application Health"
        assert (
            result["recommendation_candidate"]["business_outcome"]
            == "Maintain Application Health"
        )
        assert result["human_review_package"]["business_outcome"] == "Maintain Application Health"
