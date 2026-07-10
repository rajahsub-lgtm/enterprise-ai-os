"""Sprint 4C governed MCP tool request envelope and execution validator.

This module validates tool request envelopes against the governed MCP manifest.
It does not execute real tools.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint4.governed_mcp_tool_manifest import (
    MCPToolPermissionResult,
    MCPToolRequest,
    evaluate_tool_permission,
    load_governed_mcp_tool_manifest,
)
from eaios.sprint4.governed_reasoning_observation import (
    build_governed_reasoning_observation_snapshot,
)


class MCPExecutionState(str, Enum):
    VALIDATED_ALLOWED_SIMULATED = "VALIDATED_ALLOWED_SIMULATED"
    VALIDATED_DENIED = "VALIDATED_DENIED"


@dataclass(frozen=True)
class MCPToolRequestEnvelope:
    envelope_id: str
    request: MCPToolRequest
    source_snapshot_id: str
    source_cluster_id: str
    source_failure_case_id: str
    purpose: str
    expected_result_type: str
    provenance_required: bool
    audit_required: bool
    kill_switch_checked: bool
    budget_checked: bool
    degraded_mode_supported: bool
    human_approval_required: bool
    autonomous_execution_allowed: bool
    benchmark_scoring_allowed: bool
    provenance: str


@dataclass(frozen=True)
class MCPToolExecutionValidation:
    envelope_id: str
    request_id: str
    tool_id: str
    operation: str
    permission: MCPToolPermissionResult
    execution_state: MCPExecutionState
    simulated_result_summary: str | None
    denied_reason_summary: str | None
    output_can_define_benchmark_truth: bool
    output_can_score_benchmark: bool
    human_approval_required: bool
    autonomous_execution_allowed: bool
    provenance: str
    audit_events: tuple[str, ...]


@dataclass(frozen=True)
class MCPToolExecutionValidationPlan:
    plan_id: str
    source_snapshot_id: str
    envelopes: tuple[MCPToolRequestEnvelope, ...]
    validations: tuple[MCPToolExecutionValidation, ...]
    allowed_count: int
    denied_count: int
    real_tool_execution_performed: bool
    human_approval_required: bool
    autonomous_execution_allowed: bool
    benchmark_scoring_allowed_from_tool_output: bool
    provenance: str


def build_governed_mcp_tool_execution_plan() -> MCPToolExecutionValidationPlan:
    snapshot = build_governed_reasoning_observation_snapshot()
    manifest = load_governed_mcp_tool_manifest()
    envelopes = _build_default_envelopes(snapshot)
    validations = tuple(validate_tool_request_envelope(e, manifest) for e in envelopes)

    return MCPToolExecutionValidationPlan(
        plan_id="sprint4c-governed-mcp-tool-execution-plan-001",
        source_snapshot_id=snapshot.snapshot_id,
        envelopes=envelopes,
        validations=validations,
        allowed_count=sum(1 for v in validations if v.permission.allowed),
        denied_count=sum(1 for v in validations if not v.permission.allowed),
        real_tool_execution_performed=False,
        human_approval_required=True,
        autonomous_execution_allowed=False,
        benchmark_scoring_allowed_from_tool_output=False,
        provenance="governed_mcp_tool_execution:validation_plan",
    )


def validate_tool_request_envelope(
    envelope: MCPToolRequestEnvelope,
    manifest: Any | None = None,
) -> MCPToolExecutionValidation:
    if manifest is None:
        manifest = load_governed_mcp_tool_manifest()

    permission = evaluate_tool_permission(manifest, envelope.request)
    state = (
        MCPExecutionState.VALIDATED_ALLOWED_SIMULATED
        if permission.allowed
        else MCPExecutionState.VALIDATED_DENIED
    )

    return MCPToolExecutionValidation(
        envelope_id=envelope.envelope_id,
        request_id=envelope.request.request_id,
        tool_id=envelope.request.tool_id,
        operation=envelope.request.operation,
        permission=permission,
        execution_state=state,
        simulated_result_summary=_simulated_summary(envelope, permission),
        denied_reason_summary=None if permission.allowed else "; ".join(permission.reasons),
        output_can_define_benchmark_truth=False,
        output_can_score_benchmark=False,
        human_approval_required=True,
        autonomous_execution_allowed=False,
        provenance="governed_mcp_tool_execution:validation_only",
        audit_events=_audit_events(envelope, permission, state),
    )


def summarize_tool_execution_plan(plan: MCPToolExecutionValidationPlan) -> dict[str, object]:
    return {
        "plan_id": plan.plan_id,
        "source_snapshot_id": plan.source_snapshot_id,
        "envelope_count": len(plan.envelopes),
        "validation_count": len(plan.validations),
        "allowed_count": plan.allowed_count,
        "denied_count": plan.denied_count,
        "real_tool_execution_performed": plan.real_tool_execution_performed,
        "human_approval_required": plan.human_approval_required,
        "autonomous_execution_allowed": plan.autonomous_execution_allowed,
        "benchmark_scoring_allowed_from_tool_output": (
            plan.benchmark_scoring_allowed_from_tool_output
        ),
        "denied_decisions": tuple(
            v.permission.decision.value for v in plan.validations if not v.permission.allowed
        ),
    }


def to_view_model(plan: MCPToolExecutionValidationPlan) -> dict[str, Any]:
    return {
        "summary": summarize_tool_execution_plan(plan),
        "envelopes": [
            {
                "envelope_id": e.envelope_id,
                "request_id": e.request.request_id,
                "tool_id": e.request.tool_id,
                "operation": e.request.operation,
                "source_cluster_id": e.source_cluster_id,
                "source_failure_case_id": e.source_failure_case_id,
                "purpose": e.purpose,
                "expected_result_type": e.expected_result_type,
                "provenance_required": e.provenance_required,
                "audit_required": e.audit_required,
                "kill_switch_checked": e.kill_switch_checked,
                "budget_checked": e.budget_checked,
                "degraded_mode_supported": e.degraded_mode_supported,
                "human_approval_required": e.human_approval_required,
                "autonomous_execution_allowed": e.autonomous_execution_allowed,
                "benchmark_scoring_allowed": e.benchmark_scoring_allowed,
                "provenance": e.provenance,
            }
            for e in plan.envelopes
        ],
        "validations": [
            {
                "envelope_id": v.envelope_id,
                "request_id": v.request_id,
                "tool_id": v.tool_id,
                "operation": v.operation,
                "decision": v.permission.decision.value,
                "allowed": v.permission.allowed,
                "execution_state": v.execution_state.value,
                "simulated_result_summary": v.simulated_result_summary,
                "denied_reason_summary": v.denied_reason_summary,
                "output_can_define_benchmark_truth": v.output_can_define_benchmark_truth,
                "output_can_score_benchmark": v.output_can_score_benchmark,
                "human_approval_required": v.human_approval_required,
                "autonomous_execution_allowed": v.autonomous_execution_allowed,
                "provenance": v.provenance,
                "audit_events": list(v.audit_events),
                "reasons": list(v.permission.reasons),
            }
            for v in plan.validations
        ],
        "human_approval_required": plan.human_approval_required,
        "autonomous_execution_allowed": plan.autonomous_execution_allowed,
        "benchmark_scoring_allowed_from_tool_output": (
            plan.benchmark_scoring_allowed_from_tool_output
        ),
        "real_tool_execution_performed": plan.real_tool_execution_performed,
        "provenance": plan.provenance,
    }


def _build_default_envelopes(snapshot: Any) -> tuple[MCPToolRequestEnvelope, ...]:
    clusters = snapshot.application_health_view["clusters"]
    payment = next(
        c for c in clusters
        if c["source_failure_case_id"] == "structural-failure-payment-latency-001"
    )
    inventory = next(
        c for c in clusters
        if c["source_failure_case_id"] == "structural-failure-inventory-errors-001"
    )

    return (
        _envelope(
            "mcp-envelope-read-telemetry-payment",
            MCPToolRequest(
                request_id="mcp-request-read-telemetry-payment",
                tool_id="observability.telemetry.read",
                operation="read_metrics",
                purpose="Read synthetic telemetry for payment latency cluster.",
                cluster_id=payment["cluster_id"],
                source_failure_case_id=payment["source_failure_case_id"],
                requested_by_agent="mcp-boundary-agent",
                human_approval_required=True,
                autonomous_execution_requested=False,
                benchmark_scoring_requested=False,
            ),
            snapshot.snapshot_id,
            "synthetic_observability_evidence",
        ),
        _envelope(
            "mcp-envelope-search-knowledge-payment",
            MCPToolRequest(
                request_id="mcp-request-search-knowledge-payment",
                tool_id="knowledge.search.read",
                operation="search_articles",
                purpose="Search governed knowledge for payment latency evidence.",
                cluster_id=payment["cluster_id"],
                source_failure_case_id=payment["source_failure_case_id"],
                requested_by_agent="mcp-boundary-agent",
                human_approval_required=True,
                autonomous_execution_requested=False,
                benchmark_scoring_requested=False,
            ),
            snapshot.snapshot_id,
            "governed_knowledge_evidence",
        ),
        _envelope(
            "mcp-envelope-read-topology-inventory",
            MCPToolRequest(
                request_id="mcp-request-read-topology-inventory",
                tool_id="cmdb.topology.read",
                operation="read_dependencies",
                purpose="Read topology around inventory and route-planning impact.",
                cluster_id=inventory["cluster_id"],
                source_failure_case_id=inventory["source_failure_case_id"],
                requested_by_agent="mcp-boundary-agent",
                human_approval_required=True,
                autonomous_execution_requested=False,
                benchmark_scoring_requested=False,
            ),
            snapshot.snapshot_id,
            "synthetic_topology_evidence",
        ),
        _envelope(
            "mcp-envelope-denied-remediation-payment",
            MCPToolRequest(
                request_id="mcp-request-denied-remediation-payment",
                tool_id="remediation.plan.propose",
                operation="restart_service",
                purpose="Attempt actual remediation to prove denial path.",
                cluster_id=payment["cluster_id"],
                source_failure_case_id=payment["source_failure_case_id"],
                requested_by_agent="mcp-boundary-agent",
                human_approval_required=True,
                autonomous_execution_requested=False,
                benchmark_scoring_requested=False,
            ),
            snapshot.snapshot_id,
            "denied_remediation_attempt",
        ),
    )


def _envelope(
    envelope_id: str,
    request: MCPToolRequest,
    source_snapshot_id: str,
    expected_result_type: str,
) -> MCPToolRequestEnvelope:
    return MCPToolRequestEnvelope(
        envelope_id=envelope_id,
        request=request,
        source_snapshot_id=source_snapshot_id,
        source_cluster_id=request.cluster_id,
        source_failure_case_id=request.source_failure_case_id,
        purpose=request.purpose,
        expected_result_type=expected_result_type,
        provenance_required=True,
        audit_required=True,
        kill_switch_checked=True,
        budget_checked=True,
        degraded_mode_supported=True,
        human_approval_required=True,
        autonomous_execution_allowed=False,
        benchmark_scoring_allowed=False,
        provenance="governed_mcp_tool_execution:request_envelope",
    )


def _simulated_summary(
    envelope: MCPToolRequestEnvelope,
    permission: MCPToolPermissionResult,
) -> str | None:
    if not permission.allowed:
        return None
    return (
        f"Validated request {envelope.request.request_id} for "
        f"{envelope.request.tool_id}.{envelope.request.operation}; "
        "no real tool execution performed."
    )


def _audit_events(
    envelope: MCPToolRequestEnvelope,
    permission: MCPToolPermissionResult,
    state: MCPExecutionState,
) -> tuple[str, ...]:
    events = [
        f"envelope_created:{envelope.envelope_id}",
        f"permission_evaluated:{permission.decision.value}",
        f"execution_state:{state.value}",
        "provenance_preserved:true",
        "human_approval_required:true",
        "autonomous_execution_allowed:false",
        "benchmark_scoring_allowed:false",
    ]
    if not permission.allowed:
        events.append("denied_request_recorded:true")
    return tuple(events)
