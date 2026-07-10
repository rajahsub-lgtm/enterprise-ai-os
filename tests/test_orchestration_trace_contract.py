from src.governance.source_access_request import SourceAccessRequest
from src.governance.source_access_result import SourceAccessResult
from src.orchestration.agent_step import AgentStep
from src.orchestration.orchestration_trace import OrchestrationTrace


def source_request() -> SourceAccessRequest:
    return SourceAccessRequest(
        case_id="CASE-S3-TRACE-001",
        agent_id="memory_pattern_agent",
        source_id="enterprise_memory",
        capability="retrieve_memory_patterns",
        goal_category="capability_health_management",
        purpose="evaluate prior governed experience",
        evidence_class="memory_state_evidence",
    )


def allowed_result() -> SourceAccessResult:
    request = source_request()

    return SourceAccessResult(
        case_id=request.case_id,
        agent_id=request.agent_id,
        source_id=request.source_id,
        capability=request.capability,
        goal_category=request.goal_category,
        purpose=request.purpose,
        evidence_class=request.evidence_class,
        access_decision="ALLOW",
        audit_id="audit-trace-001",
        evidence_id="ev-trace-001",
        content_safety_status="SAFE_BY_APPROVED_PROVENANCE",
        allowed_for_reasoning=True,
        payload={"summary": "Governed evidence is eligible for reasoning."},
        required_controls=["governed_access_required"],
    )


def denied_result() -> SourceAccessResult:
    request = source_request()

    return SourceAccessResult.denied(
        request,
        reason="Agent is not entitled to this source.",
        audit_id="audit-denied-001",
        required_controls=["least_privilege_enforced"],
    )


def trace() -> OrchestrationTrace:
    return OrchestrationTrace(
        trace_id="TRACE-CASE-S3-001",
        case_id="CASE-S3-TRACE-001",
        joint_goal="Maintain the target outcome while preserving controls.",
        current_phase="PARTIAL_CONTEXT",
        selected_due_diligence_level="EXPANDED_VALIDATION",
        why_path_selected="Operational confidence requires broader validation.",
    )


def test_planned_source_access_step_records_request_shape():
    step = AgentStep.planned_source_access(
        step_id="STEP-001",
        step_name="Evaluate prior experience",
        request=source_request(),
    )

    assert step.status == "PLANNED"
    assert step.governance_decision == "PENDING"
    assert step.source_id == "enterprise_memory"
    assert step.allowed_for_reasoning is False
    assert step.details["evidence_class"] == "memory_state_evidence"


def test_allowed_source_access_result_becomes_completed_step():
    step = AgentStep.from_source_access_result(
        step_id="STEP-002",
        step_name="Evaluate prior experience",
        result=allowed_result(),
    )

    assert step.status == "COMPLETED"
    assert step.governance_decision == "ALLOW"
    assert step.audit_id == "audit-trace-001"
    assert step.evidence_id == "ev-trace-001"
    assert step.has_reasoning_eligible_evidence() is True


def test_denied_source_access_result_becomes_blocked_step():
    step = AgentStep.from_source_access_result(
        step_id="STEP-003",
        step_name="Evaluate prior experience",
        result=denied_result(),
    )

    assert step.status == "BLOCKED"
    assert step.governance_decision == "DENY"
    assert step.evidence_id is None
    assert step.allowed_for_reasoning is False
    assert step.reason == "Agent is not entitled to this source."


def test_trace_records_joint_goal_phase_depth_and_reason():
    value = trace().to_dict()

    assert value["joint_goal"] == "Maintain the target outcome while preserving controls."
    assert value["current_phase"] == "PARTIAL_CONTEXT"
    assert value["selected_due_diligence_level"] == "EXPANDED_VALIDATION"
    assert value["why_path_selected"] == "Operational confidence requires broader validation."
    assert value["governance_required"] is True
    assert value["human_approval_required"] is True
    assert value["autonomous_action_allowed"] is False


def test_trace_records_governed_source_requests():
    orchestration_trace = trace()
    orchestration_trace.add_source_request(source_request())

    value = orchestration_trace.to_dict()

    assert value["governed_source_requests"] == [
        {
            "case_id": "CASE-S3-TRACE-001",
            "agent_id": "memory_pattern_agent",
            "source_id": "enterprise_memory",
            "capability": "retrieve_memory_patterns",
            "goal_category": "capability_health_management",
            "purpose": "evaluate prior governed experience",
            "evidence_class": "memory_state_evidence",
        }
    ]


def test_trace_collects_access_decisions():
    orchestration_trace = trace()
    orchestration_trace.add_step(
        AgentStep.from_source_access_result(
            step_id="STEP-002",
            step_name="Evaluate prior experience",
            result=allowed_result(),
        )
    )

    value = orchestration_trace.to_dict()

    assert value["access_decisions"] == [
        {
            "step_id": "STEP-002",
            "agent_id": "memory_pattern_agent",
            "source_id": "enterprise_memory",
            "governance_decision": "ALLOW",
            "audit_id": "audit-trace-001",
            "reason": None,
        }
    ]


def test_trace_collects_audit_ids_and_evidence_ids():
    orchestration_trace = trace()
    orchestration_trace.add_step(
        AgentStep.from_source_access_result(
            step_id="STEP-002",
            step_name="Evaluate prior experience",
            result=allowed_result(),
        )
    )

    value = orchestration_trace.to_dict()

    assert value["audit_ids"] == ["audit-trace-001"]
    assert value["evidence_ids"] == ["ev-trace-001"]


def test_trace_records_reasoning_eligibility():
    orchestration_trace = trace()
    orchestration_trace.add_step(
        AgentStep.from_source_access_result(
            step_id="STEP-002",
            step_name="Evaluate prior experience",
            result=allowed_result(),
        )
    )

    value = orchestration_trace.to_dict()

    assert value["reasoning_eligibility"] == [
        {
            "step_id": "STEP-002",
            "agent_id": "memory_pattern_agent",
            "source_id": "enterprise_memory",
            "evidence_id": "ev-trace-001",
            "content_safety_status": "SAFE_BY_APPROVED_PROVENANCE",
            "allowed_for_reasoning": True,
        }
    ]


def test_trace_records_denied_access_without_evidence_id():
    orchestration_trace = trace()
    orchestration_trace.add_step(
        AgentStep.from_source_access_result(
            step_id="STEP-003",
            step_name="Evaluate prior experience",
            result=denied_result(),
        )
    )

    value = orchestration_trace.to_dict()

    assert value["access_decisions"][0]["governance_decision"] == "DENY"
    assert value["evidence_ids"] == []
    assert value["reasoning_eligibility"][0]["allowed_for_reasoning"] is False


def test_trace_validation_requires_governance_and_human_boundary():
    orchestration_trace = trace()

    assert orchestration_trace.is_valid() is True

    orchestration_trace.governance_required = False
    orchestration_trace.human_approval_required = False
    orchestration_trace.autonomous_action_allowed = True

    errors = orchestration_trace.validation_errors()

    assert "governance_required must be True" in errors
    assert "human_approval_required must be True" in errors
    assert "autonomous_action_allowed must be False" in errors
