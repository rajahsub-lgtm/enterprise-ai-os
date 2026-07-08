import pytest

from src.domain_adapters.it_application_health.itil_repository_loader import (
    ItApplicationHealthRepository,
)


def test_repository_loader_reads_business_outcome():
    repository = ItApplicationHealthRepository()

    assert repository.business_outcome() == "Maintain Application Health"


def test_repository_loader_returns_all_scenarios():
    repository = ItApplicationHealthRepository()

    scenarios = repository.scenarios()

    assert len(scenarios) == 6
    assert [scenario["scenario_id"] for scenario in scenarios] == [
        "GS-001",
        "GS-002",
        "GS-003",
        "GS-004",
        "GS-005",
        "GS-006",
    ]


def test_repository_loader_finds_scenario_by_id():
    repository = ItApplicationHealthRepository()

    scenario = repository.scenario_by_id("GS-001")

    assert scenario["name"] == "Tier-0 Checkout Degradation"
    assert scenario["business_outcome"] == "Maintain Application Health"


def test_repository_loader_fails_closed_for_unknown_scenario():
    repository = ItApplicationHealthRepository()

    with pytest.raises(KeyError):
        repository.scenario_by_id("GS-999")


def test_repository_loader_returns_records_for_scenario():
    repository = ItApplicationHealthRepository()

    records = repository.records_for_scenario("GS-001")

    assert len(records["monitoring_events"]) == 3
    assert len(records["incidents"]) == 2
    assert len(records["problems"]) == 1
    assert len(records["knowledge_articles"]) == 1
    assert len(records["change_requests"]) == 1
    assert len(records["memory_patterns"]) == 1


def test_repository_loader_maps_ci_to_business_services():
    repository = ItApplicationHealthRepository()

    services = repository.business_services_for_ci("CI-COMPUTE-HOST-007")

    service_ids = {service["business_service_id"] for service in services}

    assert "BS-DIGITAL-CHECKOUT" in service_ids
    assert "BS-PAYMENT-AUTH" in service_ids


def test_repository_loader_detects_unmapped_ci():
    repository = ItApplicationHealthRepository()

    assert repository.is_unmapped_ci("CI-UNMAPPED-API-001") is True
    assert repository.is_unmapped_ci("CI-CHECKOUT-API-001") is False


def test_repository_loader_exposes_unknown_impact_policy():
    repository = ItApplicationHealthRepository()

    policy = repository.unknown_impact_policy()

    assert policy["impact_tier"] == "UNKNOWN"
    assert policy["required_action"] == "ESCALATE_FOR_IMPACT_ASSESSMENT"
    assert policy["autonomous_action_allowed"] is False
