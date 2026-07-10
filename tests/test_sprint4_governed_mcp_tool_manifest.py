from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint4.governed_mcp_tool_manifest import (
    MCPToolRequest,
    ToolAccessMode,
    ToolPermissionDecision,
    evaluate_tool_permission,
    load_governed_mcp_tool_manifest,
    summarize_tool_manifest,
)


def _manifest():
    return load_governed_mcp_tool_manifest()


def test_governed_mcp_tool_manifest_loads_policy_boundary():
    manifest = _manifest()

    assert manifest.manifest_id == "it-application-health-governed-mcp-tools-v1"
    assert manifest.domain == "it_application_health"
    assert manifest.policy["source_layer"] == "governed_mcp_tool_boundary"
    assert manifest.policy["real_tool_execution_allowed"] is False
    assert manifest.policy["autonomous_action_allowed"] is False
    assert manifest.policy["human_approval_required"] is True
    assert manifest.policy["benchmark_scoring_allowed_from_tool_output"] is False
    assert manifest.policy["tool_output_can_define_benchmark_truth"] is False


def test_governed_mcp_tool_manifest_contains_expected_tool_ids():
    manifest = _manifest()

    tool_ids = {tool.tool_id for tool in manifest.tools}

    assert tool_ids == {
        "observability.telemetry.read",
        "cmdb.topology.read",
        "incident.records.read",
        "knowledge.search.read",
        "change.context.read",
        "remediation.plan.propose",
        "notification.draft.prepare",
    }


def test_all_governed_mcp_tools_preserve_no_autonomous_action_and_no_benchmark_scoring():
    manifest = _manifest()

    assert all(tool.requires_human_approval is True for tool in manifest.tools)
    assert all(tool.autonomous_execution_allowed is False for tool in manifest.tools)
    assert all(tool.benchmark_scoring_allowed is False for tool in manifest.tools)
    assert all(tool.provenance_required is True for tool in manifest.tools)


def test_mcp_manifest_distinguishes_read_proposal_and_draft_modes():
    manifest = _manifest()

    modes_by_tool = {tool.tool_id: tool.access_mode for tool in manifest.tools}

    assert modes_by_tool["observability.telemetry.read"] == ToolAccessMode.READ_ONLY
    assert modes_by_tool["remediation.plan.propose"] == ToolAccessMode.PROPOSAL_ONLY
    assert modes_by_tool["notification.draft.prepare"] == ToolAccessMode.DRAFT_ONLY


def test_tool_permission_allows_read_operation_with_governance():
    manifest = _manifest()

    result = evaluate_tool_permission(
        manifest,
        MCPToolRequest(
            request_id="tool-request-001",
            tool_id="observability.telemetry.read",
            operation="read_metrics",
            purpose="Read synthetic telemetry for governed reasoning.",
            cluster_id="cluster::structural-failure-payment-latency-001",
            source_failure_case_id="structural-failure-payment-latency-001",
            requested_by_agent="mcp-boundary-agent",
            human_approval_required=True,
            autonomous_execution_requested=False,
            benchmark_scoring_requested=False,
        ),
    )

    assert result.allowed is True
    assert result.decision == ToolPermissionDecision.ALLOWED_WITH_GOVERNANCE
    assert result.human_approval_required is True
    assert result.autonomous_execution_allowed is False
    assert result.benchmark_scoring_allowed is False
    assert result.provenance_required is True
    assert result.audit_required is True


def test_tool_permission_denies_unknown_tool():
    manifest = _manifest()

    result = evaluate_tool_permission(
        manifest,
        MCPToolRequest(
            request_id="tool-request-unknown",
            tool_id="unknown.tool",
            operation="read_metrics",
            purpose="Unknown tool should be denied.",
            cluster_id="cluster::structural-failure-payment-latency-001",
            source_failure_case_id="structural-failure-payment-latency-001",
            requested_by_agent="mcp-boundary-agent",
            human_approval_required=True,
            autonomous_execution_requested=False,
            benchmark_scoring_requested=False,
        ),
    )

    assert result.allowed is False
    assert result.decision == ToolPermissionDecision.DENIED_UNKNOWN_TOOL


def test_tool_permission_denies_global_remediation_operations():
    manifest = _manifest()

    result = evaluate_tool_permission(
        manifest,
        MCPToolRequest(
            request_id="tool-request-denied-global",
            tool_id="remediation.plan.propose",
            operation="restart_service",
            purpose="Attempt actual remediation.",
            cluster_id="cluster::structural-failure-payment-latency-001",
            source_failure_case_id="structural-failure-payment-latency-001",
            requested_by_agent="mcp-boundary-agent",
            human_approval_required=True,
            autonomous_execution_requested=False,
            benchmark_scoring_requested=False,
        ),
    )

    assert result.allowed is False
    assert result.decision == ToolPermissionDecision.DENIED_GLOBAL_OPERATION
    assert "Operation is globally denied." in result.reasons


def test_tool_permission_denies_operations_not_explicitly_allowed():
    manifest = _manifest()

    result = evaluate_tool_permission(
        manifest,
        MCPToolRequest(
            request_id="tool-request-denied-operation",
            tool_id="incident.records.read",
            operation="close_incident",
            purpose="Attempt incident update.",
            cluster_id="cluster::structural-failure-payment-latency-001",
            source_failure_case_id="structural-failure-payment-latency-001",
            requested_by_agent="mcp-boundary-agent",
            human_approval_required=True,
            autonomous_execution_requested=False,
            benchmark_scoring_requested=False,
        ),
    )

    assert result.allowed is False
    assert result.decision == ToolPermissionDecision.DENIED_OPERATION_NOT_ALLOWED


def test_tool_permission_denies_autonomous_execution_request():
    manifest = _manifest()

    result = evaluate_tool_permission(
        manifest,
        MCPToolRequest(
            request_id="tool-request-denied-auto",
            tool_id="knowledge.search.read",
            operation="search_articles",
            purpose="Attempt autonomous request.",
            cluster_id="cluster::structural-failure-payment-latency-001",
            source_failure_case_id="structural-failure-payment-latency-001",
            requested_by_agent="mcp-boundary-agent",
            human_approval_required=True,
            autonomous_execution_requested=True,
            benchmark_scoring_requested=False,
        ),
    )

    assert result.allowed is False
    assert result.decision == ToolPermissionDecision.DENIED_AUTONOMOUS_EXECUTION


def test_tool_permission_denies_benchmark_scoring_request():
    manifest = _manifest()

    result = evaluate_tool_permission(
        manifest,
        MCPToolRequest(
            request_id="tool-request-denied-scoring",
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
    )

    assert result.allowed is False
    assert result.decision == ToolPermissionDecision.DENIED_BENCHMARK_SCORING


def test_tool_permission_denies_missing_human_approval_boundary():
    manifest = _manifest()

    result = evaluate_tool_permission(
        manifest,
        MCPToolRequest(
            request_id="tool-request-denied-human",
            tool_id="change.context.read",
            operation="read_change_context",
            purpose="Missing human approval flag.",
            cluster_id="cluster::structural-failure-inventory-errors-001",
            source_failure_case_id="structural-failure-inventory-errors-001",
            requested_by_agent="mcp-boundary-agent",
            human_approval_required=False,
            autonomous_execution_requested=False,
            benchmark_scoring_requested=False,
        ),
    )

    assert result.allowed is False
    assert result.decision == ToolPermissionDecision.DENIED_MISSING_HUMAN_APPROVAL


def test_tool_manifest_summary_is_view_ready():
    manifest = _manifest()

    summary = summarize_tool_manifest(manifest)

    assert summary["manifest_id"] == "it-application-health-governed-mcp-tools-v1"
    assert summary["domain"] == "it_application_health"
    assert summary["tool_count"] == 7
    assert summary["globally_denied_operation_count"] >= 10
    assert summary["human_approval_required"] is True
    assert summary["autonomous_action_allowed"] is False
    assert summary["benchmark_scoring_allowed_from_tool_output"] is False
    assert summary["provenance_required"] is True
    assert summary["audit_required"] is True
    assert summary["kill_switch_required"] is True


def test_governed_mcp_tool_manifest_module_does_not_execute_tools():
    source = Path("src/eaios/sprint4/governed_mcp_tool_manifest.py").read_text(
        encoding="utf-8"
    )

    assert "subprocess" not in source
    assert "requests" not in source.lower()
    assert "httpx" not in source.lower()
    assert "execute_tool(" not in source
    assert "restart_service(" not in source
    assert "score_benchmark_result(" not in source
