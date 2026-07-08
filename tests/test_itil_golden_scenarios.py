import json
from pathlib import Path


SCENARIO_PATH = Path("data/domain/it_application_health/golden_scenarios.json")


def load_scenarios() -> dict:
    return json.loads(SCENARIO_PATH.read_text(encoding="utf-8"))


def test_golden_scenarios_file_exists_and_has_six_scenarios():
    data = load_scenarios()

    assert data["business_outcome"] == "Maintain Application Health"
    assert data["scenario_count"] == 6
    assert len(data["scenarios"]) == 6


def test_golden_scenario_ids_are_deterministic_and_complete():
    data = load_scenarios()

    scenario_ids = [scenario["scenario_id"] for scenario in data["scenarios"]]

    assert scenario_ids == [
        "GS-001",
        "GS-002",
        "GS-003",
        "GS-004",
        "GS-005",
        "GS-006",
    ]


def test_every_golden_scenario_starts_with_business_outcome_and_goal_context():
    data = load_scenarios()

    for scenario in data["scenarios"]:
        assert scenario["business_outcome"] == "Maintain Application Health"
        assert scenario["goal_category"] == "operational_troubleshooting"
        assert scenario["story"]
        assert scenario["expected_concepts"]


def test_every_golden_scenario_preserves_human_approval_boundary():
    data = load_scenarios()

    for scenario in data["scenarios"]:
        assert scenario["autonomous_action_allowed"] is False
        assert scenario["requires_human_approval"] is True
        assert scenario["expected_result"]["recommendation_type"] == "recommendation_candidate"


def test_unknown_business_impact_is_not_treated_as_low():
    data = load_scenarios()

    unknown = next(
        scenario
        for scenario in data["scenarios"]
        if scenario["scenario_id"] == "GS-005"
    )

    assert unknown["impact_tier"] == "UNKNOWN"
    assert unknown["impact_confidence"] == "LOW"
    assert unknown["governance_debt"] == "missing_business_impact_mapping"
    assert unknown["expected_result"]["required_action"] == "ESCALATE_FOR_IMPACT_ASSESSMENT"
    assert "unknown_is_not_low" in unknown["expected_concepts"]


def test_conflicting_evidence_scenario_requires_more_evidence():
    data = load_scenarios()

    conflicting = next(
        scenario
        for scenario in data["scenarios"]
        if scenario["scenario_id"] == "GS-006"
    )

    assert conflicting["impact_confidence"] == "LOW"
    assert "conflicting_evidence" in conflicting["expected_concepts"]
    assert conflicting["expected_result"]["required_action"] == "GATHER_ADDITIONAL_EVIDENCE"