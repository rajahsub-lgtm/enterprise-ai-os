from pathlib import Path

from src.governance.access_governance_system import AccessGovernanceSystem
from src.governance.action_request import ActionRequest
from src.governance.registry_loader import RegistryLoader


GOVERNANCE_PATH = Path("data/governance")


def make_request(
    *,
    request_id: str,
    caller_agent_id: str = "application_health_agent",
    target_agent_id: str = "knowledge_agent",
    requested_capability: str = "retrieve_best_knowledge",
    goal_category: str | None = "operational_troubleshooting",
    requested_sources: list[str] | None = None,
    business_justification: str | None = None,
) -> ActionRequest:
    goal_context = None

    if goal_category is not None:
        goal_context = {
            "business_outcome": "Maintain Application Health",
            "goal_category": goal_category,
            "caller_goal": "Investigate current request",
            "target_agent_goal": "Retrieve governed knowledge for this context",
        }

    return ActionRequest(
        request_id=request_id,
        caller_agent_id=caller_agent_id,
        target_agent_id=target_agent_id,
        requested_capability=requested_capability,
        goal_context=goal_context,
        requested_sources=requested_sources or ["support_knowledge"],
        business_justification=business_justification,
        risk_context={},
    )


def build_ags_from_checked_in_registry() -> AccessGovernanceSystem:
    loader = RegistryLoader(governance_path=str(GOVERNANCE_PATH))

    agents = loader.load_agents()
    data_sources = loader.load_data_sources()
    policies = loader.load_policies()

    return AccessGovernanceSystem(
        agents=agents,
        data_sources=data_sources,
        policies=policies,
    )


def test_checked_in_governance_registry_files_load():
    loader = RegistryLoader(governance_path=str(GOVERNANCE_PATH))

    agents = loader.load_agents()
    data_sources = loader.load_data_sources()
    policies = loader.load_policies()

    assert agents
    assert data_sources
    assert policies

    assert any(agent["agent_id"] == "application_health_agent" for agent in agents)
    assert any(agent["agent_id"] == "knowledge_agent" for agent in agents)
    assert any(source["source_id"] == "support_knowledge" for source in data_sources)
    assert any(
        policy["policy_id"] == "POL-KNOWLEDGE-OPERATIONAL-001"
        for policy in policies
    )


def test_checked_in_registry_supports_approved_operational_request():
    ags = build_ags_from_checked_in_registry()

    decision = ags.evaluate(
        make_request(
            request_id="real-registry-001",
            requested_sources=["support_knowledge", "wiki_knowledge"],
        )
    )

    assert decision["decision"] == "APPROVED_WITH_CONTROLS"
    assert decision["approved_sources"] == ["support_knowledge", "wiki_knowledge"]
    assert decision["policy_id"] == "POL-KNOWLEDGE-OPERATIONAL-001"
    assert "audit_required" in decision["required_controls"]
    assert "content_safety_required" in decision["required_controls"]


def test_checked_in_registry_denies_goal_category_spoofing():
    ags = build_ags_from_checked_in_registry()

    decision = ags.evaluate(
        make_request(
            request_id="real-registry-002",
            caller_agent_id="application_health_agent",
            goal_category="hr_support",
            requested_sources=["human_resources_knowledge"],
        )
    )

    assert decision["decision"] == "DENIED"
    assert decision["policy_id"] == "POL-GOAL-CATEGORY-ENTITLEMENT-001"


def test_checked_in_registry_escalates_unknown_source_as_governance_debt():
    ags = build_ags_from_checked_in_registry()

    decision = ags.evaluate(
        make_request(
            request_id="real-registry-003",
            requested_sources=["unknown_operational_source"],
        )
    )

    assert decision["decision"] == "ESCALATE"
    assert decision["policy_id"] == "POL-GOVERNANCE-DEBT-001"
    assert decision["governance_debt"]
    assert decision["governance_debt"][0]["missing_item"] == "unknown_operational_source"


def test_checked_in_registry_denies_high_risk_uncertainty():
    ags = build_ags_from_checked_in_registry()

    decision = ags.evaluate(
        make_request(
            request_id="real-registry-004",
            requested_sources=["high_impact_incomplete_source"],
        )
    )

    assert decision["decision"] == "DENIED"
    assert decision["policy_id"] == "POL-RISK-HIGH-UNCERTAINTY-001"


def test_checked_in_registry_escalates_validated_learning_write():
    ags = build_ags_from_checked_in_registry()

    decision = ags.evaluate(
        make_request(
            request_id="real-registry-005",
            requested_capability="write_validated_learning",
            requested_sources=["validated_learning_store"],
        )
    )

    assert decision["decision"] == "ESCALATE"
    assert decision["policy_id"] == "POL-KNOWLEDGE-WRITE-001"