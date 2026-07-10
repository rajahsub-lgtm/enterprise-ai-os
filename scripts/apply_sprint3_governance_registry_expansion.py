import json
from pathlib import Path
from typing import Any


AGENTS_PATH = Path("data/governance/agents.json")
SOURCES_PATH = Path("data/governance/data_sources.json")
POLICIES_PATH = Path("data/governance/policies.json")


SPRINT3_GOAL_CATEGORY = "application_health_management"

SPRINT3_AGENTS = [
    {
        "agent_id": "adaptive_orchestrator_agent",
        "capabilities": [
            "coordinate_adaptive_orchestration",
            "select_due_diligence_depth",
            "maintain_orchestration_trace",
        ],
        "allowed_target_agents": [
            "memory_pattern_agent",
            "incident_correlation_agent",
            "cmdb_impact_agent",
            "business_impact_agent",
            "change_analysis_agent",
            "knowledge_retrieval_agent",
        ],
    },
    {
        "agent_id": "memory_pattern_agent",
        "capabilities": ["retrieve_memory_patterns", "evaluate_memory_maturity"],
        "allowed_target_agents": [],
    },
    {
        "agent_id": "incident_correlation_agent",
        "capabilities": ["retrieve_incident_context", "correlate_operational_signals"],
        "allowed_target_agents": [],
    },
    {
        "agent_id": "cmdb_impact_agent",
        "capabilities": ["retrieve_topology_context", "assess_dependency_context"],
        "allowed_target_agents": [],
    },
    {
        "agent_id": "business_impact_agent",
        "capabilities": ["retrieve_business_impact_context", "assess_impact_context"],
        "allowed_target_agents": [],
    },
    {
        "agent_id": "change_analysis_agent",
        "capabilities": ["retrieve_change_context", "assess_lifecycle_context"],
        "allowed_target_agents": [],
    },
    {
        "agent_id": "knowledge_retrieval_agent",
        "capabilities": ["retrieve_support_knowledge", "create_governed_knowledge_evidence"],
        "allowed_target_agents": ["knowledge_agent"],
    },
]


SPRINT3_SOURCES = [
    {
        "source_id": "enterprise_memory",
        "allowed_capabilities": ["retrieve_memory_patterns", "evaluate_memory_maturity"],
        "trust_level": "CONDITIONAL",
        "classification": "INTERNAL",
        "owner": "enterprise_ai_governance",
        "high_impact_signals": True,
        "required_controls": [
            "governed_access_required",
            "memory_as_evidence_not_truth",
            "human_review_required",
        ],
    },
    {
        "source_id": "itil_incidents",
        "allowed_capabilities": ["retrieve_incident_context", "correlate_operational_signals"],
        "trust_level": "APPROVED_MEDIUM_HIGH",
        "classification": "INTERNAL",
        "owner": "it_service_management",
        "high_impact_signals": True,
        "required_controls": ["governed_access_required", "audit_required"],
    },
    {
        "source_id": "itil_changes",
        "allowed_capabilities": ["retrieve_change_context", "assess_lifecycle_context"],
        "trust_level": "APPROVED_MEDIUM_HIGH",
        "classification": "INTERNAL",
        "owner": "it_service_management",
        "high_impact_signals": True,
        "required_controls": ["governed_access_required", "audit_required"],
    },
    {
        "source_id": "itil_cmdb_topology",
        "allowed_capabilities": ["retrieve_topology_context", "assess_dependency_context"],
        "trust_level": "APPROVED_HIGH",
        "classification": "INTERNAL",
        "owner": "configuration_management",
        "high_impact_signals": True,
        "required_controls": ["governed_access_required", "audit_required"],
    },
    {
        "source_id": "itil_business_impact_map",
        "allowed_capabilities": ["retrieve_business_impact_context", "assess_impact_context"],
        "trust_level": "APPROVED_HIGH",
        "classification": "INTERNAL",
        "owner": "business_service_management",
        "high_impact_signals": True,
        "required_controls": [
            "governed_access_required",
            "audit_required",
            "human_review_required",
        ],
    },
    {
        "source_id": "itil_operational_records",
        "allowed_capabilities": [
            "retrieve_incident_context",
            "retrieve_change_context",
            "retrieve_topology_context",
            "retrieve_business_impact_context",
        ],
        "trust_level": "APPROVED_MEDIUM_HIGH",
        "classification": "INTERNAL",
        "owner": "it_service_management",
        "high_impact_signals": True,
        "required_controls": ["governed_access_required", "audit_required"],
    },
]


PLANNED_ACCESS = [
    ("memory_pattern_agent", "enterprise_memory", "retrieve_memory_patterns"),
    ("incident_correlation_agent", "itil_incidents", "retrieve_incident_context"),
    ("cmdb_impact_agent", "itil_cmdb_topology", "retrieve_topology_context"),
    ("business_impact_agent", "itil_business_impact_map", "retrieve_business_impact_context"),
    ("change_analysis_agent", "itil_changes", "retrieve_change_context"),
    ("knowledge_retrieval_agent", "support_knowledge", "retrieve_support_knowledge"),
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def collection(document: Any, preferred_key: str) -> list[dict[str, Any]]:
    if isinstance(document, list):
        return document

    if isinstance(document, dict):
        for key in [preferred_key, "items", "records", "policies"]:
            if key in document and isinstance(document[key], list):
                return document[key]

        document[preferred_key] = []
        return document[preferred_key]

    raise TypeError(f"Unsupported JSON shape for {preferred_key}")


def upsert_by_id(
    records: list[dict[str, Any]],
    id_field: str,
    new_record: dict[str, Any],
) -> None:
    for index, existing in enumerate(records):
        if existing.get(id_field) == new_record[id_field]:
            merged = {**existing, **new_record}
            records[index] = merged
            return

    records.append(new_record)


def ensure_agents() -> None:
    document = load_json(AGENTS_PATH)
    agents = collection(document, "agents")

    for agent in SPRINT3_AGENTS:
        record = {
            **agent,
            "allowed_goal_categories": [SPRINT3_GOAL_CATEGORY],
            "metadata_complete": True,
        }
        upsert_by_id(agents, "agent_id", record)

    write_json(AGENTS_PATH, document)


def ensure_sources() -> None:
    document = load_json(SOURCES_PATH)
    sources = collection(document, "data_sources")

    for source in SPRINT3_SOURCES:
        record = {
            **source,
            "allowed_goal_categories": [SPRINT3_GOAL_CATEGORY],
            "metadata_complete": True,
        }
        upsert_by_id(sources, "source_id", record)

    support_knowledge_count = sum(
        1 for source in sources if source.get("source_id") == "support_knowledge"
    )
    if support_knowledge_count != 1:
        raise RuntimeError(
            "support_knowledge must exist exactly once. Reuse the existing source; do not duplicate it."
        )

    write_json(SOURCES_PATH, document)


def policy_id(agent_id: str, source_id: str) -> str:
    return f"sprint3_allow_{agent_id}_to_{source_id}"


def ensure_policies() -> None:
    document = load_json(POLICIES_PATH)
    policies = collection(document, "policies")

    for agent_id, source_id, capability in PLANNED_ACCESS:
        record = {
            "policy_id": policy_id(agent_id, source_id),
            "effect": "ALLOW",
            "decision": "ALLOW",
            "agent_id": agent_id,
            "subject_agent_id": agent_id,
            "target_agent_id": agent_id,
            "source_id": source_id,
            "resource_id": source_id,
            "capability": capability,
            "allowed_capabilities": [capability],
            "allowed_goal_categories": [SPRINT3_GOAL_CATEGORY],
            "required_controls": ["governed_access_required", "audit_required"],
            "condition": {
                "goal_category": SPRINT3_GOAL_CATEGORY,
                "capability": capability,
            },
            "subject": {
                "agent_id": agent_id,
            },
            "resource": {
                "source_id": source_id,
            },
        }
        upsert_by_id(policies, "policy_id", record)

    write_json(POLICIES_PATH, document)


def main() -> None:
    ensure_agents()
    ensure_sources()
    ensure_policies()


if __name__ == "__main__":
    main()
