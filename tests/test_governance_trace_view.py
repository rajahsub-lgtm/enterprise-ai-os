import pytest

from src.views.governance_trace_view import GovernanceTraceView


def trace() -> dict:
    return {
        "trace_id": "TRACE-S3-001",
        "case_id": "CASE-S3-001",
        "governance_required": True,
        "human_approval_required": True,
        "autonomous_action_allowed": False,
        "agent_steps": [
            {
                "step_id": "STEP-PLAN-001",
                "agent_id": "memory_pattern_agent",
                "step_name": "Planned governed source access",
                "status": "PLANNED",
                "source_id": "enterprise_memory",
                "source_access_purpose": "evaluate prior governed experience",
                "governance_decision": "PENDING",
                "audit_id": None,
                "evidence_id": None,
                "content_safety_status": None,
                "allowed_for_reasoning": False,
                "required_controls": [],
                "reason": None,
            },
            {
                "step_id": "STEP-RESULT-001",
                "agent_id": "memory_pattern_agent",
                "step_name": "Governed evidence collected",
                "status": "COMPLETED",
                "source_id": "enterprise_memory",
                "source_access_purpose": "evaluate prior governed experience",
                "governance_decision": "ALLOW",
                "audit_id": "audit-001",
                "evidence_id": "ev-001",
                "content_safety_status": "SAFE_BY_APPROVED_PROVENANCE",
                "allowed_for_reasoning": True,
                "required_controls": ["governed_access_required"],
                "reason": None,
            },
            {
                "step_id": "STEP-RESULT-002",
                "agent_id": "knowledge_retrieval_agent",
                "step_name": "Governed evidence collected",
                "status": "COMPLETED",
                "source_id": "support_knowledge",
                "source_access_purpose": "retrieve governed knowledge",
                "governance_decision": "ALLOW",
                "audit_id": "audit-002",
                "evidence_id": "ev-002",
                "content_safety_status": "NEEDS_HUMAN_REVIEW",
                "allowed_for_reasoning": False,
                "required_controls": ["human_review_required"],
                "reason": "Evidence was collected but excluded from reasoning.",
            },
            {
                "step_id": "STEP-RESULT-003",
                "agent_id": "memory_pattern_agent",
                "step_name": "Governed evidence gap recorded",
                "status": "BLOCKED",
                "source_id": "restricted_source",
                "source_access_purpose": "request restricted source",
                "governance_decision": "DENY",
                "audit_id": "audit-003",
                "evidence_id": None,
                "content_safety_status": None,
                "allowed_for_reasoning": False,
                "required_controls": ["least_privilege_enforced"],
                "reason": "Agent is not entitled to this source.",
            },
        ],
    }


def test_governance_trace_view_projects_required_row_fields():
    view = GovernanceTraceView.from_orchestration_trace(trace())
    value = view.to_dict()

    first_row = value["rows"][0]

    required_fields = {
        "agent_id",
        "source_id",
        "source_access_purpose",
        "governance_decision",
        "audit_id",
        "evidence_id",
        "content_safety_status",
        "allowed_for_reasoning",
        "required_controls",
        "approval_state",
        "autonomous_action_allowed",
        "reason",
    }

    assert required_fields.issubset(first_row)


def test_governance_trace_view_omits_pending_planned_steps():
    view = GovernanceTraceView.from_orchestration_trace(trace())
    value = view.to_dict()

    assert len(value["rows"]) == 3
    assert all(row["governance_decision"] != "PENDING" for row in value["rows"])


def test_allowed_reasoning_eligible_row_is_pending_human_review():
    view = GovernanceTraceView.from_orchestration_trace(trace())
    row = view.reasoning_eligible_rows()[0]

    assert row["agent_id"] == "memory_pattern_agent"
    assert row["source_id"] == "enterprise_memory"
    assert row["governance_decision"] == "ALLOW"
    assert row["audit_id"] == "audit-001"
    assert row["evidence_id"] == "ev-001"
    assert row["content_safety_status"] == "SAFE_BY_APPROVED_PROVENANCE"
    assert row["allowed_for_reasoning"] is True
    assert row["approval_state"] == "PENDING_HUMAN_REVIEW"
    assert row["autonomous_action_allowed"] is False


def test_review_required_row_is_not_reasoning_eligible():
    view = GovernanceTraceView.from_orchestration_trace(trace())
    blocked_rows = view.blocked_rows()

    review_row = [
        row for row in blocked_rows if row["source_id"] == "support_knowledge"
    ][0]

    assert review_row["governance_decision"] == "ALLOW"
    assert review_row["content_safety_status"] == "NEEDS_HUMAN_REVIEW"
    assert review_row["allowed_for_reasoning"] is False
    assert review_row["approval_state"] == "NOT_ELIGIBLE_FOR_REASONING"
    assert "human_review_required" in review_row["required_controls"]


def test_denied_row_is_blocked_by_governance():
    view = GovernanceTraceView.from_orchestration_trace(trace())
    denied_row = view.rows_for_decision("DENY")[0]

    assert denied_row["agent_id"] == "memory_pattern_agent"
    assert denied_row["source_id"] == "restricted_source"
    assert denied_row["governance_decision"] == "DENY"
    assert denied_row["audit_id"] == "audit-003"
    assert denied_row["evidence_id"] is None
    assert denied_row["approval_state"] == "BLOCKED_BY_GOVERNANCE"
    assert denied_row["reason"] == "Agent is not entitled to this source."


def test_summary_counts_allowed_denied_reasoning_and_blocked_rows():
    value = GovernanceTraceView.from_orchestration_trace(trace()).to_dict()

    assert value["summary"] == {
        "total_rows": 3,
        "allowed_rows": 2,
        "denied_rows": 1,
        "reasoning_eligible_rows": 1,
        "blocked_rows": 2,
    }


def test_view_requires_governance_required_true():
    bad_trace = trace()
    bad_trace["governance_required"] = False

    with pytest.raises(ValueError):
        GovernanceTraceView.from_orchestration_trace(bad_trace)


def test_view_requires_human_approval_required_true():
    bad_trace = trace()
    bad_trace["human_approval_required"] = False

    with pytest.raises(ValueError):
        GovernanceTraceView.from_orchestration_trace(bad_trace)


def test_view_rejects_autonomous_action_allowed_true():
    bad_trace = trace()
    bad_trace["autonomous_action_allowed"] = True

    with pytest.raises(ValueError):
        GovernanceTraceView.from_orchestration_trace(bad_trace)


def test_view_does_not_invent_missing_audit_or_evidence_ids():
    bad_trace = trace()
    bad_trace["agent_steps"][1]["audit_id"] = None
    bad_trace["agent_steps"][1]["evidence_id"] = None

    row = GovernanceTraceView.from_orchestration_trace(bad_trace).to_dict()["rows"][0]

    assert row["audit_id"] is None
    assert row["evidence_id"] is None
    assert row["governance_decision"] == "ALLOW"
