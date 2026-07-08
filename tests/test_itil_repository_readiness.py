import json
from pathlib import Path


DOMAIN_PATH = Path("data/domain/it_application_health")

SCENARIOS_PATH = DOMAIN_PATH / "golden_scenarios.json"
IMPACT_MAP_PATH = DOMAIN_PATH / "business_impact_map.json"
TOPOLOGY_PATH = DOMAIN_PATH / "cmdb_topology.json"
RECORDS_PATH = DOMAIN_PATH / "operational_records.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_repository() -> dict:
    return {
        "scenarios": load_json(SCENARIOS_PATH),
        "impact_map": load_json(IMPACT_MAP_PATH),
        "topology": load_json(TOPOLOGY_PATH),
        "records": load_json(RECORDS_PATH),
    }


def test_synthetic_itil_repository_files_exist():
    assert SCENARIOS_PATH.exists()
    assert IMPACT_MAP_PATH.exists()
    assert TOPOLOGY_PATH.exists()
    assert RECORDS_PATH.exists()


def test_synthetic_itil_repository_is_business_outcome_aligned():
    repo = load_repository()

    assert repo["scenarios"]["business_outcome"] == "Maintain Application Health"
    assert repo["impact_map"]["business_outcome"] == "Maintain Application Health"
    assert repo["topology"]["business_outcome"] == "Maintain Application Health"
    assert repo["records"]["business_outcome"] == "Maintain Application Health"


def test_synthetic_itil_repository_has_expected_core_counts():
    repo = load_repository()

    assert len(repo["scenarios"]["scenarios"]) == 6
    assert len(repo["impact_map"]["business_services"]) == 6
    assert len(repo["topology"]["cis"]) == 24
    assert len(repo["topology"]["relationships"]) == 28

    assert len(repo["records"]["monitoring_events"]) == 9
    assert len(repo["records"]["incidents"]) == 7
    assert len(repo["records"]["problems"]) == 4
    assert len(repo["records"]["knowledge_articles"]) == 6
    assert len(repo["records"]["change_requests"]) == 3
    assert len(repo["records"]["memory_patterns"]) == 3


def test_all_scenario_primary_entities_reference_valid_cmdb_cis():
    repo = load_repository()

    ci_ids = {ci["ci_id"] for ci in repo["topology"]["cis"]}

    for scenario in repo["scenarios"]["scenarios"]:
        for ci_id in scenario["primary_entities"]["affected_cis"]:
            assert ci_id in ci_ids


def test_all_scenario_business_services_are_known_or_explicitly_unknown():
    repo = load_repository()

    known_services = {
        service["business_service_id"]
        for service in repo["impact_map"]["business_services"]
    }

    for scenario in repo["scenarios"]["scenarios"]:
        service_id = scenario["primary_entities"]["business_service"]

        if scenario["scenario_id"] == "GS-005":
            assert service_id is None
            assert scenario["impact_tier"] == "UNKNOWN"
        else:
            assert service_id in known_services


def test_all_operational_records_reference_known_scenarios():
    repo = load_repository()

    known_scenarios = {
        scenario["scenario_id"]
        for scenario in repo["scenarios"]["scenarios"]
    }

    record_groups = [
        "monitoring_events",
        "incidents",
        "problems",
        "knowledge_articles",
        "change_requests",
        "memory_patterns",
    ]

    for group in record_groups:
        for record in repo["records"][group]:
            assert record["scenario_id"] in known_scenarios


def test_all_operational_record_cis_exist_in_cmdb_topology():
    repo = load_repository()

    ci_ids = {ci["ci_id"] for ci in repo["topology"]["cis"]}

    record_groups = [
        "monitoring_events",
        "incidents",
        "problems",
        "knowledge_articles",
        "change_requests",
        "memory_patterns",
    ]

    for group in record_groups:
        for record in repo["records"][group]:
            if "related_ci" in record and record["related_ci"] is not None:
                assert record["related_ci"] in ci_ids


def test_business_impact_map_and_cmdb_service_mappings_are_consistent():
    repo = load_repository()

    service_to_cis = {
        service["business_service_id"]: set(service["mapped_cis"])
        for service in repo["impact_map"]["business_services"]
    }

    ci_to_services = {
        ci["ci_id"]: set(ci["mapped_business_services"])
        for ci in repo["topology"]["cis"]
    }

    for service_id, mapped_cis in service_to_cis.items():
        for ci_id in mapped_cis:
            assert ci_id in ci_to_services
            assert service_id in ci_to_services[ci_id]


def test_memory_patterns_referenced_by_scenarios_exist_in_operational_records():
    repo = load_repository()

    known_memory_ids = {
        memory["memory_id"]
        for memory in repo["records"]["memory_patterns"]
    }

    for scenario in repo["scenarios"]["scenarios"]:
        referenced_memory = scenario["primary_entities"].get("memory_patterns", [])

        for memory_id in referenced_memory:
            assert memory_id in known_memory_ids


def test_change_requests_referenced_by_scenarios_exist_in_operational_records():
    repo = load_repository()

    known_change_ids = {
        change["change_id"]
        for change in repo["records"]["change_requests"]
    }

    for scenario in repo["scenarios"]["scenarios"]:
        referenced_changes = scenario["primary_entities"].get("change_requests", [])

        for change_id in referenced_changes:
            assert change_id in known_change_ids


def test_unknown_impact_policy_matches_unknown_scenario_and_records():
    repo = load_repository()

    policy = repo["impact_map"]["unknown_impact_policy"]

    unknown_scenario = next(
        scenario
        for scenario in repo["scenarios"]["scenarios"]
        if scenario["scenario_id"] == "GS-005"
    )

    unknown_incident = next(
        incident
        for incident in repo["records"]["incidents"]
        if incident["scenario_id"] == "GS-005"
    )

    assert policy["impact_tier"] == "UNKNOWN"
    assert policy["required_action"] == "ESCALATE_FOR_IMPACT_ASSESSMENT"

    assert unknown_scenario["impact_tier"] == "UNKNOWN"
    assert unknown_scenario["expected_result"]["required_action"] == policy["required_action"]

    assert unknown_incident["priority"] == "IMPACT_UNKNOWN"
    assert unknown_incident["business_service_id"] is None


def test_repository_never_allows_autonomous_action():
    repo = load_repository()

    for scenario in repo["scenarios"]["scenarios"]:
        assert scenario["autonomous_action_allowed"] is False
        assert scenario["requires_human_approval"] is True

    for service in repo["impact_map"]["business_services"]:
        assert service["autonomous_action_allowed"] is False
        assert service["requires_human_approval"] is True

    assert repo["impact_map"]["unknown_impact_policy"]["autonomous_action_allowed"] is False
