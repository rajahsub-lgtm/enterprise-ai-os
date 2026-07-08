import json
from pathlib import Path


IMPACT_MAP_PATH = Path("data/domain/it_application_health/business_impact_map.json")


def load_impact_map() -> dict:
    return json.loads(IMPACT_MAP_PATH.read_text(encoding="utf-8"))


def test_business_impact_map_exists_and_is_business_outcome_aligned():
    data = load_impact_map()

    assert data["business_outcome"] == "Maintain Application Health"
    assert data["version"] == "0.1.0"
    assert len(data["business_services"]) == 6


def test_high_impact_services_require_human_approval_and_no_autonomous_action():
    data = load_impact_map()

    high_impact_services = [
        service
        for service in data["business_services"]
        if service["impact_tier"] == "HIGH"
    ]

    assert high_impact_services

    for service in high_impact_services:
        assert service["criticality"] == "TIER_0"
        assert service["requires_human_approval"] is True
        assert service["autonomous_action_allowed"] is False


def test_checkout_service_maps_to_expected_critical_cis():
    data = load_impact_map()

    checkout = next(
        service
        for service in data["business_services"]
        if service["business_service_id"] == "BS-DIGITAL-CHECKOUT"
    )

    assert checkout["impact_tier"] == "HIGH"
    assert checkout["impact_confidence"] == "HIGH"

    assert "CI-CHECKOUT-API-001" in checkout["mapped_cis"]
    assert "CI-PAYMENT-SVC-001" in checkout["mapped_cis"]
    assert "CI-AUTH-SVC-001" in checkout["mapped_cis"]
    assert "CI-COMPUTE-HOST-007" in checkout["mapped_cis"]


def test_low_business_impact_is_explicit_not_inferred():
    data = load_impact_map()

    internal_reporting = next(
        service
        for service in data["business_services"]
        if service["business_service_id"] == "BS-INTERNAL-REPORTING"
    )

    assert internal_reporting["impact_tier"] == "LOW"
    assert internal_reporting["impact_confidence"] == "HIGH"
    assert internal_reporting["criticality"] == "TIER_3"


def test_unknown_impact_policy_escalates_and_creates_governance_debt():
    data = load_impact_map()

    policy = data["unknown_impact_policy"]

    assert policy["impact_tier"] == "UNKNOWN"
    assert policy["impact_confidence"] == "LOW"
    assert policy["required_action"] == "ESCALATE_FOR_IMPACT_ASSESSMENT"
    assert policy["autonomous_action_allowed"] is False
    assert policy["governance_debt"] == "missing_business_impact_mapping"


def test_unmapped_ci_is_not_treated_as_low_impact():
    data = load_impact_map()

    unmapped = next(
        item
        for item in data["unmapped_cis"]
        if item["ci_id"] == "CI-UNMAPPED-API-001"
    )

    assert unmapped["required_action"] == "ESCALATE_FOR_IMPACT_ASSESSMENT"
    assert unmapped["governance_debt"] == "missing_business_impact_mapping"