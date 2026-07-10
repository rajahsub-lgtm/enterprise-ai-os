import json
from pathlib import Path


AGENTS_PATH = Path("data/governance/agents.json")
SOURCES_PATH = Path("data/governance/data_sources.json")
POLICIES_PATH = Path("data/governance/policies.json")


SPRINT3_GOAL_CATEGORY = "application_health_management"

SPRINT3_AGENTS = {
    "adaptive_orchestrator_agent",
    "memory_pattern_agent",
    "incident_correlation_agent",
    "cmdb_impact_agent",
    "business_impact_agent",
    "change_analysis_agent",
    "knowledge_retrieval_agent",
}

SPRINT3_SOURCES = {
    "enterprise_memory",
    "itil_incidents",
    "itil_changes",
    "itil_cmdb_topology",
    "itil_business_impact_map",
    "itil_operational_records",
}

PLANNED_ACCESS = {
    ("memory_pattern_agent", "enterprise_memory"),
    ("incident_correlation_agent", "itil_incidents"),
    ("cmdb_impact_agent", "itil_cmdb_topology"),
    ("business_impact_agent", "itil_business_impact_map"),
    ("change_analysis_agent", "itil_changes"),
    ("knowledge_retrieval_agent", "support_knowledge"),
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def records(document, preferred_key: str) -> list[dict]:
    if isinstance(document, list):
        return document

    for key in [preferred_key, "items", "records", "policies"]:
        if key in document and isinstance(document[key], list):
            return document[key]

    raise AssertionError(f"Could not find list collection for {preferred_key}")


def agents() -> list[dict]:
    return records(load(AGENTS_PATH), "agents")


def sources() -> list[dict]:
    return records(load(SOURCES_PATH), "data_sources")


def policies() -> list[dict]:
    return records(load(POLICIES_PATH), "policies")


def source_id(policy: dict) -> str | None:
    return (
        policy.get("source_id")
        or policy.get("resource_id")
        or policy.get("resource", {}).get("source_id")
    )


def agent_id(policy: dict) -> str | None:
    return (
        policy.get("agent_id")
        or policy.get("subject_agent_id")
        or policy.get("target_agent_id")
        or policy.get("subject", {}).get("agent_id")
    )


def effect(policy: dict) -> str | None:
    return policy.get("effect") or policy.get("decision")


def allows(agent: str, source: str) -> bool:
    return any(
        effect(policy) == "ALLOW"
        and agent_id(policy) == agent
        and source_id(policy) == source
        and SPRINT3_GOAL_CATEGORY in policy.get("allowed_goal_categories", [])
        for policy in policies()
    )


def test_sprint3_agents_are_registered_with_full_minimum_schema():
    by_id = {agent["agent_id"]: agent for agent in agents()}

    assert SPRINT3_AGENTS.issubset(by_id)

    for agent_id in SPRINT3_AGENTS:
        agent = by_id[agent_id]

        assert agent["metadata_complete"] is True
        assert agent["capabilities"]
        assert SPRINT3_GOAL_CATEGORY in agent["allowed_goal_categories"]
        assert "allowed_target_agents" in agent


def test_sprint3_sources_are_registered_with_full_ags_schema():
    by_id = {source["source_id"]: source for source in sources()}

    assert SPRINT3_SOURCES.issubset(by_id)

    required_fields = {
        "source_id",
        "allowed_capabilities",
        "allowed_goal_categories",
        "metadata_complete",
        "high_impact_signals",
        "required_controls",
        "trust_level",
        "classification",
        "owner",
    }

    for source_id_value in SPRINT3_SOURCES:
        source = by_id[source_id_value]

        assert required_fields.issubset(source)
        assert source["metadata_complete"] is True
        assert source["allowed_capabilities"]
        assert SPRINT3_GOAL_CATEGORY in source["allowed_goal_categories"]
        assert source["required_controls"]
        assert source["trust_level"]
        assert source["classification"]
        assert source["owner"]


def test_support_knowledge_is_reused_not_duplicated():
    support_knowledge_sources = [
        source for source in sources() if source["source_id"] == "support_knowledge"
    ]

    assert len(support_knowledge_sources) == 1


def test_planned_sprint3_agent_source_access_is_allowed_by_policy():
    for agent, source in PLANNED_ACCESS:
        assert allows(agent, source), f"Missing ALLOW policy for {agent} -> {source}"


def test_wrong_source_access_has_no_allow_policy():
    disallowed_access = {
        ("memory_pattern_agent", "itil_business_impact_map"),
        ("incident_correlation_agent", "enterprise_memory"),
        ("change_analysis_agent", "itil_cmdb_topology"),
        ("knowledge_retrieval_agent", "itil_changes"),
    }

    for agent, source in disallowed_access:
        assert not allows(agent, source), f"Unexpected ALLOW policy for {agent} -> {source}"


def test_unregistered_agent_has_no_allow_policy():
    assert not allows("unregistered_sprint3_agent", "enterprise_memory")


def test_sprint3_source_trust_levels_are_deliberate():
    by_id = {source["source_id"]: source for source in sources()}

    assert by_id["itil_cmdb_topology"]["trust_level"] == "APPROVED_HIGH"
    assert by_id["itil_business_impact_map"]["trust_level"] == "APPROVED_HIGH"
    assert by_id["enterprise_memory"]["trust_level"] == "CONDITIONAL"
