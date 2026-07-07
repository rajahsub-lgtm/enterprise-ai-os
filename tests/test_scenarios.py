import json
from pathlib import Path

import pytest

from src.governance.access_governance_system import AccessGovernanceSystem
from src.governance.action_request import ActionRequest
from src.governance.audit_logger import AuditLogger
from src.governance.governance_broker import GovernanceBroker
from src.governance.governance_debt_logger import GovernanceDebtLogger
from src.governance.governed_knowledge_client import GovernedKnowledgeClient
from src.governance.registry_loader import RegistryLoader


def write_json(path: Path, data: list[dict] | dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


@pytest.fixture()
def governance_test_environment(tmp_path):
    governance_dir = tmp_path / "governance"
    audit_path = tmp_path / "audit_log.json"
    debt_path = tmp_path / "governance_debt.json"

    write_json(
        governance_dir / "agents.json",
        [
            {
                "agent_id": "application_health_agent",
                "name": "Application Health Agent",
                "owner": "application_operations",
                "risk_tier": "medium",
                "allowed_target_agents": ["knowledge_agent"],
                "allowed_goal_categories": ["operational_troubleshooting"],
                "capabilities": ["request_operational_support"],
            },
            {
                "agent_id": "self_help_agent",
                "name": "Self Help Agent",
                "owner": "employee_experience",
                "risk_tier": "low",
                "allowed_target_agents": ["knowledge_agent"],
                "allowed_goal_categories": ["self_help"],
                "capabilities": ["request_self_help_support"],
            },
            {
                "agent_id": "hr_support_agent",
                "name": "HR Support Agent",
                "owner": "human_resources",
                "risk_tier": "high",
                "allowed_target_agents": ["knowledge_agent"],
                "allowed_goal_categories": ["hr_support"],
                "capabilities": ["request_hr_support"],
            },
            {
                "agent_id": "knowledge_agent",
                "name": "Knowledge Agent",
                "owner": "enterprise_knowledge",
                "risk_tier": "medium",
                "capabilities": [
                    "retrieve_best_knowledge",
                    "retrieve_identity_context",
                    "write_validated_learning",
                ],
            },
        ],
    )

    write_json(
        governance_dir / "data_sources.json",
        [
            {
                "source_id": "support_knowledge",
                "name": "Support Knowledge",
                "owner": "it_support",
                "classification": "internal",
                "trust_level": "approved",
                "allowed_capabilities": ["retrieve_best_knowledge"],
                "allowed_goal_categories": ["operational_troubleshooting"],
                "source_role": "primary",
                "required_controls": [
                    "log_source_access",
                    "return_knowledge_quality_score",
                    "check_last_validated_date",
                ],
                "high_impact_signals": [],
                "metadata_complete": True,
            },
            {
                "source_id": "self_help_knowledge",
                "name": "Self Help Knowledge",
                "owner": "employee_experience",
                "classification": "internal",
                "trust_level": "approved",
                "allowed_capabilities": ["retrieve_best_knowledge"],
                "allowed_goal_categories": ["operational_troubleshooting", "self_help"],
                "source_role": "supporting",
                "required_controls": [
                    "log_source_access",
                    "return_knowledge_quality_score",
                ],
                "high_impact_signals": [],
                "metadata_complete": True,
            },
            {
                "source_id": "wiki_knowledge",
                "name": "Wiki Knowledge",
                "owner": "enterprise_knowledge",
                "classification": "internal",
                "trust_level": "conditional",
                "allowed_capabilities": ["retrieve_best_knowledge"],
                "allowed_goal_categories": ["operational_troubleshooting", "self_help"],
                "source_role": "supporting",
                "required_controls": [
                    "log_source_access",
                    "check_last_validated_date",
                    "distinguish_authoritative_vs_supporting_knowledge",
                ],
                "high_impact_signals": [],
                "metadata_complete": True,
            },
            {
                "source_id": "human_resources_knowledge",
                "name": "Human Resources Knowledge",
                "owner": "human_resources",
                "classification": "confidential",
                "trust_level": "approved",
                "allowed_capabilities": ["retrieve_best_knowledge"],
                "allowed_goal_categories": ["hr_support"],
                "source_role": "restricted",
                "required_controls": [
                    "log_source_access",
                    "record_policy_reference",
                ],
                "high_impact_signals": ["confidential_data", "hr_data"],
                "metadata_complete": True,
            },
            {
                "source_id": "employee_identification_knowledge",
                "name": "Employee Identification Knowledge",
                "owner": "identity_and_access_management",
                "classification": "restricted",
                "trust_level": "approved",
                "allowed_capabilities": ["retrieve_identity_context"],
                "allowed_goal_categories": ["hr_support"],
                "source_role": "restricted",
                "contains_pii": True,
                "required_controls": [
                    "privacy_control",
                    "business_justification",
                    "human_review",
                ],
                "high_impact_signals": ["pii", "identity_data", "regulated_data"],
                "metadata_complete": True,
            },
            {
                "source_id": "validated_learning_store",
                "name": "Validated Learning Store",
                "owner": "enterprise_knowledge",
                "classification": "internal",
                "trust_level": "approved",
                "allowed_capabilities": ["write_validated_learning"],
                "allowed_goal_categories": ["operational_troubleshooting"],
                "source_role": "write_target",
                "required_controls": [
                    "human_approval",
                    "append_audit_record",
                ],
                "high_impact_signals": ["write_action", "enterprise_memory_update"],
                "metadata_complete": True,
            },
        ],
    )

    write_json(
        governance_dir / "policies.json",
        [
            {
                "policy_id": "POL-GOAL-CONTEXT-001",
                "name": "Goal Context Required",
                "owner": "enterprise_governance",
                "risk_tier": "high",
                "effect": {"missing_goal_context": "DENY"},
            },
            {
                "policy_id": "POL-KNOWLEDGE-OPERATIONAL-001",
                "name": "Operational Troubleshooting Knowledge Access",
                "owner": "enterprise_governance",
                "risk_tier": "medium",
                "subject": {
                    "target_agent_id": "knowledge_agent",
                    "capability": "retrieve_best_knowledge",
                },
                "condition": {
                    "goal_category": "operational_troubleshooting",
                    "allowed_sources": [
                        "support_knowledge",
                        "wiki_knowledge",
                        "self_help_knowledge",
                    ],
                },
                "effect": {"allowed": "APPROVED_WITH_CONTROLS"},
            },
            {
                "policy_id": "POL-KNOWLEDGE-SELFHELP-001",
                "name": "Self Help Knowledge Access",
                "owner": "enterprise_governance",
                "risk_tier": "low",
                "subject": {
                    "target_agent_id": "knowledge_agent",
                    "capability": "retrieve_best_knowledge",
                },
                "condition": {
                    "goal_category": "self_help",
                    "allowed_sources": [
                        "self_help_knowledge",
                        "wiki_knowledge",
                    ],
                },
                "effect": {"allowed": "APPROVED_WITH_CONTROLS"},
            },
            {
                "policy_id": "POL-KNOWLEDGE-HR-001",
                "name": "Restrict Human Resources Knowledge to HR Goal Contexts",
                "owner": "enterprise_governance",
                "risk_tier": "high",
                "subject": {
                    "target_agent_id": "knowledge_agent",
                    "capability": "retrieve_best_knowledge",
                },
                "condition": {
                    "requested_source": "human_resources_knowledge",
                    "allowed_goal_categories": ["hr_support"],
                },
                "effect": {"when_goal_category_not_in_allowed_list": "DENY"},
                "controls": [
                    "log_denied_access",
                    "record_policy_reference",
                    "notify_source_owner_if_repeated",
                ],
            },
            {
                "policy_id": "POL-KNOWLEDGE-IDENTITY-001",
                "name": "Restrict Employee Identity Knowledge",
                "owner": "enterprise_governance",
                "risk_tier": "high",
                "subject": {
                    "target_agent_id": "knowledge_agent",
                },
                "condition": {
                    "requested_source": "employee_identification_knowledge",
                    "required_capability": "retrieve_identity_context",
                    "required_goal_category": "hr_support",
                    "requires_business_justification": True,
                },
                "effect": {
                    "generic_retrieval": "DENY",
                    "missing_business_justification": "DENY",
                    "valid_identity_context": "ESCALATE",
                },
            },
            {
                "policy_id": "POL-KNOWLEDGE-WRITE-001",
                "name": "Validated Learning Writes Require Human Approval",
                "owner": "enterprise_governance",
                "risk_tier": "high",
                "subject": {
                    "target_agent_id": "knowledge_agent",
                    "capability": "write_validated_learning",
                },
                "condition": {
                    "requested_source": "validated_learning_store",
                },
                "effect": {"write_request": "ESCALATE"},
            },
            {
                "policy_id": "POL-GOVERNANCE-DEBT-001",
                "name": "Unknown Source Is Governance Debt",
                "owner": "enterprise_governance",
                "risk_tier": "medium",
                "effect": {"unknown_source": "ESCALATE"},
            },
            {
                "policy_id": "POL-RISK-HIGH-UNCERTAINTY-001",
                "name": "High-Risk Uncertainty Default Denial",
                "owner": "enterprise_governance",
                "risk_tier": "high",
                "effect": {
                    "missing_required_control_with_high_impact_signal": "DENY"
                },
            },
        ],
    )

    loader = RegistryLoader(governance_path=str(governance_dir))
    ags = AccessGovernanceSystem(
        agents=loader.load_agents(),
        data_sources=loader.load_data_sources(),
        policies=loader.load_policies(),
    )
    audit_logger = AuditLogger(audit_path=str(audit_path))
    governance_debt_logger = GovernanceDebtLogger(debt_path=str(debt_path))
    broker = GovernanceBroker(
        ags=ags,
        audit_logger=audit_logger,
        governance_debt_logger=governance_debt_logger,
    )
    client = GovernedKnowledgeClient(broker=broker)

    return {
        "client": client,
        "audit_path": audit_path,
        "debt_path": debt_path,
    }


def make_request(
    request_id: str,
    caller_agent_id: str = "application_health_agent",
    target_agent_id: str = "knowledge_agent",
    requested_capability: str = "retrieve_best_knowledge",
    goal_category: str | None = "operational_troubleshooting",
    requested_sources: list[str] | None = None,
    business_justification: str | None = None,
    risk_context: dict | None = None,
):
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
        risk_context=risk_context or {},
    )


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def assert_governed_response(
    response: dict,
    expected_decision: str,
    request_id: str,
    audit_path: Path,
    expect_audit: bool = True,
):
    assert response["decision"]["decision"] == expected_decision

    if expected_decision == "APPROVED_WITH_CONTROLS":
        assert response["allowed"] is True
        assert response["accessible_sources"]
        assert response["decision"]["required_controls"]
    else:
        assert response["allowed"] is False
        assert response["accessible_sources"] == []

    if expect_audit:
        assert audit_path.exists()
        audit_records = read_json(audit_path)
        assert any(
            record["decision"]["request_id"] == request_id
            and record["decision"]["decision"] == expected_decision
            for record in audit_records
        )


def test_approved_operational_troubleshooting_source_access(governance_test_environment):
    request = make_request(
        request_id="req-001",
        requested_sources=[
            "support_knowledge",
            "wiki_knowledge",
            "self_help_knowledge",
        ],
    )

    response = governance_test_environment["client"].request_knowledge_access(request)

    assert_governed_response(
        response,
        "APPROVED_WITH_CONTROLS",
        "req-001",
        governance_test_environment["audit_path"],
    )


def test_approved_self_help_source_access(governance_test_environment):
    request = make_request(
        request_id="req-002",
        caller_agent_id="self_help_agent",
        goal_category="self_help",
        requested_sources=[
            "self_help_knowledge",
            "wiki_knowledge",
        ],
    )

    response = governance_test_environment["client"].request_knowledge_access(request)

    assert_governed_response(
        response,
        "APPROVED_WITH_CONTROLS",
        "req-002",
        governance_test_environment["audit_path"],
    )


def test_denied_hr_source_from_non_hr_context(governance_test_environment):
    request = make_request(
        request_id="req-003",
        goal_category="operational_troubleshooting",
        requested_sources=["human_resources_knowledge"],
    )

    response = governance_test_environment["client"].request_knowledge_access(request)

    assert_governed_response(
        response,
        "DENIED",
        "req-003",
        governance_test_environment["audit_path"],
    )
    assert response["decision"]["policy_id"] == "POL-KNOWLEDGE-HR-001"


def test_denied_identity_source_through_generic_retrieval(governance_test_environment):
    request = make_request(
        request_id="req-004",
        caller_agent_id="self_help_agent",
        goal_category="self_help",
        requested_capability="retrieve_best_knowledge",
        requested_sources=["employee_identification_knowledge"],
    )

    response = governance_test_environment["client"].request_knowledge_access(request)

    assert_governed_response(
        response,
        "DENIED",
        "req-004",
        governance_test_environment["audit_path"],
    )


def test_escalated_identity_access_with_justification(governance_test_environment):
    request = make_request(
        request_id="req-005",
        caller_agent_id="hr_support_agent",
        goal_category="hr_support",
        requested_capability="retrieve_identity_context",
        requested_sources=["employee_identification_knowledge"],
        business_justification="Validate employee identity for HR support case.",
    )

    response = governance_test_environment["client"].request_knowledge_access(request)

    assert_governed_response(
        response,
        "ESCALATE",
        "req-005",
        governance_test_environment["audit_path"],
    )


def test_escalated_knowledge_write(governance_test_environment):
    request = make_request(
        request_id="req-006",
        requested_capability="write_validated_learning",
        requested_sources=["validated_learning_store"],
    )

    response = governance_test_environment["client"].request_knowledge_access(request)

    assert_governed_response(
        response,
        "ESCALATE",
        "req-006",
        governance_test_environment["audit_path"],
    )


def test_unknown_source_creates_governance_debt(governance_test_environment):
    request = make_request(
        request_id="req-007",
        requested_sources=["unknown_knowledge_source"],
    )

    response = governance_test_environment["client"].request_knowledge_access(request)

    assert_governed_response(
        response,
        "ESCALATE",
        "req-007",
        governance_test_environment["audit_path"],
    )

    assert governance_test_environment["debt_path"].exists()
    debt_records = read_json(governance_test_environment["debt_path"])
    assert any(record["request_id"] == "req-007" for record in debt_records)


def test_missing_goal_context_is_denied(governance_test_environment):
    request = make_request(
        request_id="req-008",
        goal_category=None,
        requested_sources=["support_knowledge"],
    )

    response = governance_test_environment["client"].request_knowledge_access(request)

    assert_governed_response(
        response,
        "DENIED",
        "req-008",
        governance_test_environment["audit_path"],
    )


def test_high_risk_uncertainty_is_denied(governance_test_environment):
    request = make_request(
        request_id="req-009",
        caller_agent_id="hr_support_agent",
        goal_category="hr_support",
        requested_capability="retrieve_identity_context",
        requested_sources=["employee_identification_knowledge"],
        business_justification=None,
    )

    response = governance_test_environment["client"].request_knowledge_access(request)

    assert_governed_response(
        response,
        "DENIED",
        "req-009",
        governance_test_environment["audit_path"],
    )


def test_unregistered_caller_agent_is_denied(governance_test_environment):
    request = make_request(
        request_id="req-010",
        caller_agent_id="unregistered_agent",
        requested_sources=["support_knowledge"],
    )

    response = governance_test_environment["client"].request_knowledge_access(request)

    assert_governed_response(
        response,
        "DENIED",
        "req-010",
        governance_test_environment["audit_path"],
    )


class FailingAuditLogger:
    def log_decision(self, decision: dict):
        raise RuntimeError("Simulated audit failure")


def test_audit_failure_fails_closed(governance_test_environment):
    request = make_request(
        request_id="req-011",
        requested_sources=["support_knowledge"],
    )

    client = governance_test_environment["client"]
    client.broker.audit_logger = FailingAuditLogger()

    response = client.request_knowledge_access(request)

    assert response["decision"]["decision"] == "FAIL_CLOSED"
    assert response["allowed"] is False
    assert response["accessible_sources"] == []

def test_goal_category_spoofing_is_denied(governance_test_environment):
    request = make_request(
        request_id="req-012",
        caller_agent_id="application_health_agent",
        goal_category="hr_support",
        requested_capability="retrieve_best_knowledge",
        requested_sources=["human_resources_knowledge"],
    )

    response = governance_test_environment["client"].request_knowledge_access(request)

    assert_governed_response(
        response,
        "DENIED",
        "req-012",
        governance_test_environment["audit_path"],
    )

    assert response["decision"]["policy_id"] == "POL-GOAL-CATEGORY-ENTITLEMENT-001"
    assert "not entitled" in response["decision"]["reason"].lower()



    