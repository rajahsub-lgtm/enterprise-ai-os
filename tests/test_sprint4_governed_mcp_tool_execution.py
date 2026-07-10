from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint4.governed_mcp_tool_execution import (
    MCPExecutionState,
    MCPToolRequestEnvelope,
    build_governed_mcp_tool_execution_plan,
    summarize_tool_execution_plan,
    to_view_model,
    validate_tool_request_envelope,
)
from eaios.sprint4.governed_mcp_tool_manifest import (
    MCPToolRequest,
    ToolPermissionDecision,
)


def _plan():
    return build_governed_mcp_tool_execution_plan()


def test_plan_builds_validation_only_mcp_execution_boundary():
    plan = _plan()

    assert plan.plan_id == "sprint4c-governed-mcp-tool-execution-plan-001"
    assert plan.source_snapshot_id == "governed-reasoning::composition-structural-001"
    assert len(plan.envelopes) == 4
    assert len(plan.validations) == 4
    assert plan.real_tool_execution_performed is False


def test_plan_has_allowed_and_denied_paths():
    plan = _plan()

    assert plan.allowed_count == 3
    assert plan.denied_count == 1

    decisions = tuple(v.permission.decision for v in plan.validations)

    assert ToolPermissionDecision.ALLOWED_WITH_GOVERNANCE in decisions
    assert ToolPermissionDecision.DENIED_GLOBAL_OPERATION in decisions


def test_allowed_requests_are_simulated_not_executed():
    plan = _plan()
    allowed = [v for v in plan.validations if v.permission.allowed]

    assert len(allowed) == 3

    for validation in allowed:
        assert validation.execution_state == MCPExecutionState.VALIDATED_ALLOWED_SIMULATED
        assert validation.simulated_result_summary is not None
        assert "no real tool execution performed" in validation.simulated_result_summary
        assert validation.denied_reason_summary is None


def test_denied_request_records_reason_and_audit_trail():
    plan = _plan()
    denied = next(v for v in plan.validations if not v.permission.allowed)

    assert denied.request_id == "mcp-request-denied-remediation-payment"
    assert denied.tool_id == "remediation.plan.propose"
    assert denied.operation == "restart_service"
    assert denied.execution_state == MCPExecutionState.VALIDATED_DENIED
    assert denied.permission.decision == ToolPermissionDecision.DENIED_GLOBAL_OPERATION
    assert denied.simulated_result_summary is None
    assert denied.denied_reason_summary == "Operation is globally denied."
    assert "denied_request_recorded:true" in denied.audit_events


def test_envelopes_preserve_governance_fields():
    plan = _plan()

    for envelope in plan.envelopes:
        assert envelope.provenance_required is True
        assert envelope.audit_required is True
        assert envelope.kill_switch_checked is True
        assert envelope.budget_checked is True
        assert envelope.degraded_mode_supported is True
        assert envelope.human_approval_required is True
        assert envelope.autonomous_execution_allowed is False
        assert envelope.benchmark_scoring_allowed is False
        assert envelope.source_cluster_id.startswith("cluster::")
        assert envelope.source_failure_case_id.startswith("structural-failure-")


def test_validations_preserve_no_truth_no_scoring_boundary():
    plan = _plan()

    assert plan.human_approval_required is True
    assert plan.autonomous_execution_allowed is False
    assert plan.benchmark_scoring_allowed_from_tool_output is False

    for validation in plan.validations:
        assert validation.output_can_define_benchmark_truth is False
        assert validation.output_can_score_benchmark is False
        assert validation.human_approval_required is True
        assert validation.autonomous_execution_allowed is False
        assert "benchmark_scoring_allowed:false" in validation.audit_events


def test_direct_validation_denies_autonomous_execution_request():
    envelope = MCPToolRequestEnvelope(
        envelope_id="mcp-envelope-direct-denied-auto",
        request=MCPToolRequest(
            request_id="mcp-request-direct-denied-auto",
            tool_id="knowledge.search.read",
            operation="search_articles",
            purpose="Attempt autonomous execution through envelope.",
            cluster_id="cluster::structural-failure-payment-latency-001",
            source_failure_case_id="structural-failure-payment-latency-001",
            requested_by_agent="mcp-boundary-agent",
            human_approval_required=True,
            autonomous_execution_requested=True,
            benchmark_scoring_requested=False,
        ),
        source_snapshot_id="governed-reasoning::composition-structural-001",
        source_cluster_id="cluster::structural-failure-payment-latency-001",
        source_failure_case_id="structural-failure-payment-latency-001",
        purpose="Attempt autonomous execution through envelope.",
        expected_result_type="denied_autonomous_request",
        provenance_required=True,
        audit_required=True,
        kill_switch_checked=True,
        budget_checked=True,
        degraded_mode_supported=True,
        human_approval_required=True,
        autonomous_execution_allowed=False,
        benchmark_scoring_allowed=False,
        provenance="governed_mcp_tool_execution:test_envelope",
    )

    validation = validate_tool_request_envelope(envelope)

    assert validation.permission.allowed is False
    assert validation.permission.decision == ToolPermissionDecision.DENIED_AUTONOMOUS_EXECUTION
    assert validation.execution_state == MCPExecutionState.VALIDATED_DENIED
    assert "Autonomous execution was requested and is blocked." in validation.denied_reason_summary


def test_direct_validation_denies_benchmark_scoring_request():
    envelope = MCPToolRequestEnvelope(
        envelope_id="mcp-envelope-direct-denied-scoring",
        request=MCPToolRequest(
            request_id="mcp-request-direct-denied-scoring",
            tool_id="cmdb.topology.read",
            operation="read_services",
            purpose="Attempt benchmark scoring from tool output.",
            cluster_id="cluster::structural-failure-payment-latency-001",
            source_failure_case_id="structural-failure-payment-latency-001",
            requested_by_agent="mcp-boundary-agent",
            human_approval_required=True,
            autonomous_execution_requested=False,
            benchmark_scoring_requested=True,
        ),
        source_snapshot_id="governed-reasoning::composition-structural-001",
        source_cluster_id="cluster::structural-failure-payment-latency-001",
        source_failure_case_id="structural-failure-payment-latency-001",
        purpose="Attempt benchmark scoring from tool output.",
        expected_result_type="denied_benchmark_scoring_request",
        provenance_required=True,
        audit_required=True,
        kill_switch_checked=True,
        budget_checked=True,
        degraded_mode_supported=True,
        human_approval_required=True,
        autonomous_execution_allowed=False,
        benchmark_scoring_allowed=False,
        provenance="governed_mcp_tool_execution:test_envelope",
    )

    validation = validate_tool_request_envelope(envelope)

    assert validation.permission.allowed is False
    assert validation.permission.decision == ToolPermissionDecision.DENIED_BENCHMARK_SCORING
    assert validation.output_can_score_benchmark is False
    assert "Benchmark scoring from tool output was requested and is blocked." in validation.denied_reason_summary


def test_summary_is_view_ready():
    plan = _plan()

    assert summarize_tool_execution_plan(plan) == {
        "plan_id": "sprint4c-governed-mcp-tool-execution-plan-001",
        "source_snapshot_id": "governed-reasoning::composition-structural-001",
        "envelope_count": 4,
        "validation_count": 4,
        "allowed_count": 3,
        "denied_count": 1,
        "real_tool_execution_performed": False,
        "human_approval_required": True,
        "autonomous_execution_allowed": False,
        "benchmark_scoring_allowed_from_tool_output": False,
        "denied_decisions": ("DENIED_GLOBAL_OPERATION",),
    }


def test_view_model_is_json_serializable():
    plan = _plan()
    serialized = json.dumps(to_view_model(plan), indent=2)

    assert "sprint4c-governed-mcp-tool-execution-plan-001" in serialized
    assert "mcp-envelope-read-telemetry-payment" in serialized
    assert "mcp-envelope-denied-remediation-payment" in serialized
    assert "VALIDATED_ALLOWED_SIMULATED" in serialized
    assert "VALIDATED_DENIED" in serialized
    assert "benchmark_scoring_allowed_from_tool_output" in serialized


def test_module_does_not_execute_real_tools():
    source = Path("src/eaios/sprint4/governed_mcp_tool_execution.py").read_text(
        encoding="utf-8"
    )

    assert "subprocess" not in source
    assert "requests" not in source.lower()
    assert "httpx" not in source.lower()
    assert "execute_tool(" not in source
    assert "restart_service(" not in source
    assert "score_benchmark_result(" not in source
