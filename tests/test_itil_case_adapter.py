from src.domain_adapters.it_application_health.itil_case_adapter import (
    ItApplicationHealthCaseAdapter,
)
from src.domain_adapters.it_application_health.itil_repository_loader import (
    ItApplicationHealthRepository,
)


def build_adapter() -> ItApplicationHealthCaseAdapter:
    return ItApplicationHealthCaseAdapter(ItApplicationHealthRepository())


def test_case_adapter_builds_business_outcome_first_case():
    adapter = build_adapter()

    case = adapter.build_case("GS-001")

    assert case["case_id"] == "CASE-GS-001"
    assert case["scenario_id"] == "GS-001"
    assert case["business_outcome"] == "Maintain Application Health"
    assert case["goal_category"] == "operational_troubleshooting"
    assert case["case_summary"]


def test_case_adapter_creates_entities_for_business_service_and_affected_cis():
    adapter = build_adapter()

    case = adapter.build_case("GS-001")

    entity_ids = {entity["entity_id"] for entity in case["entities"]}

    assert "BS-DIGITAL-CHECKOUT" in entity_ids
    assert "CI-CHECKOUT-API-001" in entity_ids
    assert "CI-PAYMENT-SVC-001" in entity_ids
    assert "CI-AUTH-SVC-001" in entity_ids
    assert "CI-COMPUTE-HOST-007" in entity_ids


def test_case_adapter_creates_observations_from_events_and_incidents():
    adapter = build_adapter()

    case = adapter.build_case("GS-001")

    observation_types = {
        observation["observation_type"]
        for observation in case["observations"]
    }

    assert "telemetry_signal" in observation_types
    assert "reported_symptom" in observation_types
    assert len(case["observations"]) == 5


def test_case_adapter_preserves_context_records_without_fusing_them():
    adapter = build_adapter()

    case = adapter.build_case("GS-001")

    context = case["context_records"]

    assert len(context["problem_context"]) == 1
    assert len(context["knowledge_context"]) == 1
    assert len(context["change_context"]) == 1
    assert len(context["memory_context"]) == 1

    assert "supporting_evidence" not in case
    assert "recommendation" not in case


def test_case_adapter_maps_high_impact_case():
    adapter = build_adapter()

    case = adapter.build_case("GS-001")

    impact = case["impact"]

    assert impact["business_service_id"] == "BS-DIGITAL-CHECKOUT"
    assert impact["impact_tier"] == "HIGH"
    assert impact["impact_confidence"] == "HIGH"
    assert impact["criticality"] == "TIER_0"
    assert impact["autonomous_action_allowed"] is False


def test_case_adapter_preserves_unknown_impact_as_governance_debt():
    adapter = build_adapter()

    case = adapter.build_case("GS-005")

    impact = case["impact"]
    flags = case["governance_flags"]

    assert impact["business_service_id"] is None
    assert impact["impact_tier"] == "UNKNOWN"
    assert impact["impact_confidence"] == "LOW"
    assert impact["required_action"] == "ESCALATE_FOR_IMPACT_ASSESSMENT"
    assert impact["governance_debt"] == "missing_business_impact_mapping"

    assert flags["requires_impact_assessment"] is True
    assert flags["governance_debt"] == "missing_business_impact_mapping"


def test_case_adapter_preserves_human_approval_boundary_for_all_scenarios():
    adapter = build_adapter()

    for scenario_id in ["GS-001", "GS-002", "GS-003", "GS-004", "GS-005", "GS-006"]:
        case = adapter.build_case(scenario_id)

        assert case["human_approval_required"] is True
        assert case["autonomous_action_allowed"] is False
        assert case["governance_flags"]["recommendation_type"] == "recommendation_candidate"


def test_case_adapter_maps_memory_as_context_not_truth():
    adapter = build_adapter()

    case = adapter.build_case("GS-002")

    memory_context = case["context_records"]["memory_context"]

    assert len(memory_context) == 1
    assert memory_context[0]["record_id"] == "MEM-DB-CONNECTION-EXHAUSTION-001"
    assert memory_context[0]["validation_state"] == "HUMAN_VALIDATED"
    assert memory_context[0]["confidence"] == "MEDIUM"

    assert "truth" not in memory_context[0]
    assert "authorize_action" not in memory_context[0]


def test_case_adapter_keeps_conflicting_records_as_context_for_later_fusion():
    adapter = build_adapter()

    case = adapter.build_case("GS-006")

    observed_entities = {
        observation["entity_id"]
        for observation in case["observations"]
    }

    assert "CI-NETWORK-EDGE-003" in observed_entities
    assert "CI-CHECKOUT-API-001" in observed_entities

    assert case["impact"]["impact_confidence"] == "LOW"
    assert "supporting_evidence" not in case
    assert "conflicting_evidence" not in case
