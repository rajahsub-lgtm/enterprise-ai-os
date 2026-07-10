import json
from pathlib import Path


SCENARIOS_PATH = Path(
    "data/domain/it_application_health/sprint3_demo_scenarios.json"
)
MEMORY_STATES_PATH = Path(
    "data/domain/it_application_health/sprint3_demo_memory_states.json"
)


def scenarios() -> list[dict]:
    return json.loads(SCENARIOS_PATH.read_text(encoding="utf-8"))


def memory_states() -> list[dict]:
    return json.loads(MEMORY_STATES_PATH.read_text(encoding="utf-8"))


def scenario_by_type() -> dict[str, dict]:
    return {
        scenario["scenario_type"]: scenario
        for scenario in scenarios()
    }


def memory_state_ids() -> set[str]:
    return {
        state["memory_state_id"]
        for state in memory_states()
    }


def test_sprint3_scenario_file_contains_required_same_alert_cases():
    required_types = {
        "same_alert_no_memory",
        "same_alert_emerging_memory",
        "same_alert_trusted_memory",
        "same_alert_trusted_but_drifting_memory",
        "same_alert_conflicting_evidence",
        "same_alert_unknown_impact",
        "same_alert_simulated_outcome_feedback",
    }

    assert required_types == set(scenario_by_type())


def test_all_scenarios_share_same_alert_signature():
    signatures = {
        scenario["initial_signal"]["alert_signature"]
        for scenario in scenarios()
    }

    assert signatures == {"digital_checkout_latency_and_error_spike"}


def test_each_scenario_references_existing_memory_state():
    available_memory_states = memory_state_ids()

    for scenario in scenarios():
        assert scenario["memory_state_id"] in available_memory_states


def test_scenarios_include_required_expected_behavior_fields():
    required_fields = {
        "scenario_id",
        "scenario_type",
        "case_id",
        "model_label",
        "initial_signal",
        "memory_state_id",
        "impact",
        "fusion_state",
        "expected_operational_confidence",
        "expected_confidence_direction",
        "expected_due_diligence_level",
        "expected_knowledge_retrieval_required",
        "expected_governance_required",
        "expected_human_approval_required",
        "expected_autonomous_action_allowed",
    }

    for scenario in scenarios():
        assert required_fields.issubset(scenario)
        assert scenario["expected_governance_required"] is True
        assert scenario["expected_human_approval_required"] is True
        assert scenario["expected_autonomous_action_allowed"] is False


def test_scenarios_include_kt_lite_contrast_data():
    required_contrast_fields = {
        "affected_entities",
        "unaffected_entities",
        "present_symptoms",
        "absent_symptoms",
        "changed_conditions",
        "unchanged_conditions",
        "candidate_hypotheses",
        "expected_is_statements",
        "expected_is_not_statements",
    }

    for scenario in scenarios():
        assert required_contrast_fields.issubset(scenario)

        for field in required_contrast_fields:
            assert scenario[field], f"{scenario['scenario_id']} missing {field}"


def test_kt_lite_expected_is_and_is_not_are_deterministic_not_invented():
    for scenario in scenarios():
        assert all("Digital Checkout" in statement or "payment" in statement or "latency" in statement or "error" in statement for statement in scenario["expected_is_statements"])
        assert all("not" in statement.lower() for statement in scenario["expected_is_not_statements"])


def test_unknown_impact_scenario_requires_escalation():
    scenario = scenario_by_type()["same_alert_unknown_impact"]

    assert scenario["impact"]["impact_tier"] == "UNKNOWN"
    assert scenario["impact"]["impact_confidence"] == "LOW"
    assert scenario["fusion_state"] == "UNKNOWN_IMPACT"
    assert scenario["expected_due_diligence_level"] == "ESCALATE_FOR_IMPACT_ASSESSMENT"
    assert scenario["expected_operational_confidence"] == "LOW"


def test_conflicting_evidence_scenario_requires_expanded_validation():
    scenario = scenario_by_type()["same_alert_conflicting_evidence"]

    assert scenario["fusion_state"] == "CONFLICTING"
    assert scenario["expected_due_diligence_level"] == "EXPANDED_VALIDATION"
    assert scenario["expected_operational_confidence"] == "LOW"
    assert scenario["expected_knowledge_retrieval_required"] is True


def test_memory_states_are_labeled_as_simulated_not_production_persistence():
    for state in memory_states():
        assert state["model_label"] == "simulated_demo_memory_state"
        assert state["production_persistence"] is False
        assert state["memory_update_persistence"] == "deferred_to_sprint_3_1_or_v1_2"
        assert state["memory_as_evidence_not_truth"] is True


def test_simulated_outcome_feedback_does_not_write_production_memory():
    scenario = scenario_by_type()["same_alert_simulated_outcome_feedback"]

    feedback = scenario["simulated_outcome_feedback"]

    assert feedback["feedback_type"] == "simulated_demo_feedback"
    assert feedback["result"] == "human_review_confirmed_pattern"
    assert feedback["memory_update_persistence"] == "deferred"
    assert feedback["production_memory_written"] is False
