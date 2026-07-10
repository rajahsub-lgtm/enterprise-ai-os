"""Sprint 4C governed MCP tool evidence integration.

This module converts validated MCP tool envelopes into governed evidence records.

It does not execute real tools. It only packages validation outcomes as
provenance-preserving evidence for downstream reasoning and dashboards.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint4.governed_mcp_tool_execution import (
    MCPExecutionState,
    MCPToolExecutionValidation,
    MCPToolExecutionValidationPlan,
    build_governed_mcp_tool_execution_plan,
)


class MCPToolEvidenceState(str, Enum):
    AVAILABLE_SIMULATED = "AVAILABLE_SIMULATED"
    DENIED_RECORDED = "DENIED_RECORDED"
    DEGRADED_MODE = "DEGRADED_MODE"


@dataclass(frozen=True)
class MCPToolEvidenceRecord:
    evidence_id: str
    envelope_id: str
    request_id: str
    tool_id: str
    operation: str
    cluster_id: str
    source_failure_case_id: str
    evidence_state: MCPToolEvidenceState
    evidence_summary: str
    denied_reason_summary: str | None
    degraded_mode_reason: str | None
    provenance_chain: tuple[str, ...]
    audit_events: tuple[str, ...]
    usable_for_reasoning: bool
    output_can_define_benchmark_truth: bool
    output_can_score_benchmark: bool
    human_approval_required: bool
    autonomous_execution_allowed: bool
    real_tool_execution_performed: bool


@dataclass(frozen=True)
class MCPToolEvidenceIntegration:
    integration_id: str
    source_plan_id: str
    source_snapshot_id: str
    evidence_records: tuple[MCPToolEvidenceRecord, ...]
    available_count: int
    denied_count: int
    degraded_count: int
    real_tool_execution_performed: bool
    human_approval_required: bool
    autonomous_execution_allowed: bool
    benchmark_scoring_allowed_from_tool_output: bool
    provenance: str


def build_governed_mcp_tool_evidence_integration() -> MCPToolEvidenceIntegration:
    plan = build_governed_mcp_tool_execution_plan()
    records = tuple(_record_from_validation(plan, validation) for validation in plan.validations)

    return MCPToolEvidenceIntegration(
        integration_id="sprint4c-governed-mcp-tool-evidence-integration-001",
        source_plan_id=plan.plan_id,
        source_snapshot_id=plan.source_snapshot_id,
        evidence_records=records,
        available_count=sum(
            1 for record in records
            if record.evidence_state == MCPToolEvidenceState.AVAILABLE_SIMULATED
        ),
        denied_count=sum(
            1 for record in records
            if record.evidence_state == MCPToolEvidenceState.DENIED_RECORDED
        ),
        degraded_count=sum(
            1 for record in records
            if record.evidence_state == MCPToolEvidenceState.DEGRADED_MODE
        ),
        real_tool_execution_performed=False,
        human_approval_required=True,
        autonomous_execution_allowed=False,
        benchmark_scoring_allowed_from_tool_output=False,
        provenance="governed_mcp_tool_evidence:integration",
    )


def summarize_tool_evidence_integration(
    integration: MCPToolEvidenceIntegration,
) -> dict[str, object]:
    return {
        "integration_id": integration.integration_id,
        "source_plan_id": integration.source_plan_id,
        "source_snapshot_id": integration.source_snapshot_id,
        "evidence_record_count": len(integration.evidence_records),
        "available_count": integration.available_count,
        "denied_count": integration.denied_count,
        "degraded_count": integration.degraded_count,
        "real_tool_execution_performed": integration.real_tool_execution_performed,
        "human_approval_required": integration.human_approval_required,
        "autonomous_execution_allowed": integration.autonomous_execution_allowed,
        "benchmark_scoring_allowed_from_tool_output": (
            integration.benchmark_scoring_allowed_from_tool_output
        ),
        "evidence_states": tuple(
            record.evidence_state.value for record in integration.evidence_records
        ),
    }


def to_view_model(integration: MCPToolEvidenceIntegration) -> dict[str, Any]:
    return {
        "summary": summarize_tool_evidence_integration(integration),
        "evidence_records": [
            {
                "evidence_id": record.evidence_id,
                "envelope_id": record.envelope_id,
                "request_id": record.request_id,
                "tool_id": record.tool_id,
                "operation": record.operation,
                "cluster_id": record.cluster_id,
                "source_failure_case_id": record.source_failure_case_id,
                "evidence_state": record.evidence_state.value,
                "evidence_summary": record.evidence_summary,
                "denied_reason_summary": record.denied_reason_summary,
                "degraded_mode_reason": record.degraded_mode_reason,
                "provenance_chain": list(record.provenance_chain),
                "audit_events": list(record.audit_events),
                "usable_for_reasoning": record.usable_for_reasoning,
                "output_can_define_benchmark_truth": (
                    record.output_can_define_benchmark_truth
                ),
                "output_can_score_benchmark": record.output_can_score_benchmark,
                "human_approval_required": record.human_approval_required,
                "autonomous_execution_allowed": record.autonomous_execution_allowed,
                "real_tool_execution_performed": record.real_tool_execution_performed,
            }
            for record in integration.evidence_records
        ],
        "real_tool_execution_performed": integration.real_tool_execution_performed,
        "human_approval_required": integration.human_approval_required,
        "autonomous_execution_allowed": integration.autonomous_execution_allowed,
        "benchmark_scoring_allowed_from_tool_output": (
            integration.benchmark_scoring_allowed_from_tool_output
        ),
        "provenance": integration.provenance,
    }


def _record_from_validation(
    plan: MCPToolExecutionValidationPlan,
    validation: MCPToolExecutionValidation,
) -> MCPToolEvidenceRecord:
    envelope = next(
        envelope
        for envelope in plan.envelopes
        if envelope.envelope_id == validation.envelope_id
    )

    evidence_state = _evidence_state(validation)
    denied_reason = validation.denied_reason_summary
    degraded_reason = _degraded_reason(validation)

    return MCPToolEvidenceRecord(
        evidence_id=f"mcp-tool-evidence::{validation.request_id}",
        envelope_id=validation.envelope_id,
        request_id=validation.request_id,
        tool_id=validation.tool_id,
        operation=validation.operation,
        cluster_id=envelope.source_cluster_id,
        source_failure_case_id=envelope.source_failure_case_id,
        evidence_state=evidence_state,
        evidence_summary=_evidence_summary(validation, evidence_state),
        denied_reason_summary=denied_reason,
        degraded_mode_reason=degraded_reason,
        provenance_chain=(
            plan.source_snapshot_id,
            plan.plan_id,
            validation.envelope_id,
            validation.request_id,
            validation.provenance,
        ),
        audit_events=validation.audit_events,
        usable_for_reasoning=True,
        output_can_define_benchmark_truth=False,
        output_can_score_benchmark=False,
        human_approval_required=True,
        autonomous_execution_allowed=False,
        real_tool_execution_performed=False,
    )


def _evidence_state(
    validation: MCPToolExecutionValidation,
) -> MCPToolEvidenceState:
    if validation.permission.allowed:
        return MCPToolEvidenceState.AVAILABLE_SIMULATED

    if validation.execution_state == MCPExecutionState.VALIDATED_DENIED:
        return MCPToolEvidenceState.DENIED_RECORDED

    return MCPToolEvidenceState.DEGRADED_MODE


def _degraded_reason(validation: MCPToolExecutionValidation) -> str | None:
    if validation.permission.allowed:
        return None

    return "Tool denied; downstream reasoning must use degraded-mode evidence."


def _evidence_summary(
    validation: MCPToolExecutionValidation,
    evidence_state: MCPToolEvidenceState,
) -> str:
    if evidence_state == MCPToolEvidenceState.AVAILABLE_SIMULATED:
        return (
            f"Simulated governed MCP evidence for {validation.tool_id} "
            f"operation {validation.operation}; no real execution performed."
        )

    if evidence_state == MCPToolEvidenceState.DENIED_RECORDED:
        return (
            f"Denied MCP tool evidence for {validation.tool_id} "
            f"operation {validation.operation}; denial recorded for governance."
        )

    return (
        f"Degraded-mode MCP evidence for {validation.tool_id} "
        f"operation {validation.operation}."
    )
