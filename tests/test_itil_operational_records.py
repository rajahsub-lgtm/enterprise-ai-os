import json
from pathlib import Path


RECORDS_PATH = Path("data/domain/it_application_health/operational_records.json")
SCENARIOS_PATH = Path("data/domain/it_application_health/golden_scenarios.json")
TOPOLOGY_PATH = Path("data/domain/it_application_health/cmdb_topology.json")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_records() -> dict:
    return load_json(RECORDS_PATH)


def scenario_ids() -> set[str]:
    scenarios = load_json(SCENARIOS_PATH)
    return {scenario["scenario_id"] for scenario in scenarios["scenarios"]}


def ci_ids() -> set[str]:
    topology = load_json(TOPOLOGY_PATH)
    return {ci["ci_id"] for ci in topology["cis"]}


def all_records(records: dict) -> list[dict]:
    combined = []
    for key in [
        "monitoring_events",
        "incidents",
        "problems",
        "knowledge_articles",
        "change_requests",
        "memory_patterns",
    ]:
        combined.extend(records[key])
    return combined


def test_operational_records_file_exists_and_is_business_outcome_aligned():
    records = load_records()

    assert records["business_outcome"] == "Maintain Application Health"
    assert records["version"] == "0.1.0"

    assert len(records["monitoring_events"]) == 9
    assert len(records["incidents"]) == 7
    assert len(records["problems"]) == 4
    assert len(records["knowledge_articles"]) == 6
    assert len(records["change_requests"]) == 3
    assert len(records["memory_patterns"]) == 3


def test_every_operational_record_maps_to_a_known_golden_scenario():
    records = load_records()
    known_scenarios = scenario_ids()

    for record in all_records(records):
        assert record["scenario_id"] in known_scenarios


def test_every_golden_scenario_has_at_least_one_operational_record():
    records = load_records()
    known_scenarios = scenario_ids()

    scenarios_with_records = {
        record["scenario_id"]
        for record in all_records(records)
    }

    assert known_scenarios.issubset(scenarios_with_records)


def test_operational_records_reference_existing_cmdb_cis():
    records = load_records()
    known_cis = ci_ids()

    for record in all_records(records):
        if "related_ci" in record and record["related_ci"] is not None:
            assert record["related_ci"] in known_cis


def test_unknown_impact_records_preserve_impact_uncertainty():
    records = load_records()

    unknown_incident = next(
        incident
        for incident in records["incidents"]
        if incident["incident_id"] == "INC-GS005-001"
    )

    unknown_knowledge = next(
        article
        for article in records["knowledge_articles"]
        if article["knowledge_id"] == "KB-GS005-001"
    )

    assert unknown_incident["priority"] == "IMPACT_UNKNOWN"
    assert unknown_incident["business_service_id"] is None
    assert unknown_knowledge["content_safety_expected"] == "NEEDS_HUMAN_REVIEW"


def test_memory_patterns_are_evidence_not_truth():
    records = load_records()

    memory_by_id = {
        memory["memory_id"]: memory
        for memory in records["memory_patterns"]
    }

    validated = memory_by_id["MEM-DB-CONNECTION-EXHAUSTION-001"]
    unvalidated = memory_by_id["MEM-NETWORK-EDGE-CONFLICT-001"]

    assert validated["validation_state"] == "HUMAN_VALIDATED"
    assert validated["confidence"] == "MEDIUM"

    assert unvalidated["validation_state"] == "UNVALIDATED"
    assert unvalidated["confidence"] == "LOW"


def test_recent_change_correlation_is_present_for_gs003():
    records = load_records()

    change = next(
        change
        for change in records["change_requests"]
        if change["change_id"] == "CHG-2026-0007"
    )

    incident = next(
        incident
        for incident in records["incidents"]
        if incident["incident_id"] == "INC-GS003-001"
    )

    assert change["scenario_id"] == "GS-003"
    assert change["related_ci"] == incident["related_ci"]
    assert change["status"] == "implemented"


def test_conflicting_evidence_has_network_and_application_records():
    records = load_records()

    gs006_events = [
        event
        for event in records["monitoring_events"]
        if event["scenario_id"] == "GS-006"
    ]

    related_cis = {event["related_ci"] for event in gs006_events}

    assert "CI-NETWORK-EDGE-003" in related_cis
    assert "CI-CHECKOUT-API-001" in related_cis
