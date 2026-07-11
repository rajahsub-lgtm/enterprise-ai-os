"""Sprint 4C governed MCP observation snapshot.

This module packages the governed MCP/tool boundary into one stable
dashboard/export contract.

It does not execute real tools. It combines:
- governed MCP tool manifest
- MCP request validation plan
- governed tool evidence records
- denied/degraded behavior
- benchmark/governance boundaries
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from eaios.sprint4.governed_mcp_tool_evidence import (
    build_governed_mcp_tool_evidence_integration,
    summarize_tool_evidence_integration,
    to_view_model as tool_evidence_to_view_model,
)
from eaios.sprint4.governed_mcp_tool_execution import (
    build_governed_mcp_tool_execution_plan,
    summarize_tool_execution_plan,
    to_view_model as tool_execution_to_view_model,
)
from eaios.sprint4.governed_mcp_tool_manifest import (
    load_governed_mcp_tool_manifest,
    summarize_tool_manifest,
)


@dataclass(frozen=True)
class GovernedMCPObservationSnapshot:
    snapshot_id: str
    source_snapshot_id: str
    manifest_summary: dict[str, object]
    execution_summary: dict[str, object]
    evidence_summary: dict[str, object]
    tool_catalog: tuple[dict[str, object], ...]
    governance_boundaries: tuple[str, ...]
    denied_tool_records: tuple[dict[str, object], ...]
    manifest_view: dict[str, object]
    execution_view: dict[str, Any]
    evidence_view: dict[str, Any]
    real_tool_execution_performed: bool
    human_approval_required: bool
    autonomous_execution_allowed: bool
    benchmark_scoring_allowed_from_tool_output: bool
    tool_output_can_define_benchmark_truth: bool
    provenance: str


def build_governed_mcp_observation_snapshot() -> GovernedMCPObservationSnapshot:
    manifest = load_governed_mcp_tool_manifest()
    execution_plan = build_governed_mcp_tool_execution_plan()
    evidence_integration = build_governed_mcp_tool_evidence_integration()

    denied_records = tuple(
        {
            "request_id": record.request_id,
            "tool_id": record.tool_id,
            "operation": record.operation,
            "evidence_state": record.evidence_state.value,
            "denied_reason_summary": record.denied_reason_summary,
            "degraded_mode_reason": record.degraded_mode_reason,
            "human_approval_required": record.human_approval_required,
            "autonomous_execution_allowed": record.autonomous_execution_allowed,
            "output_can_score_benchmark": record.output_can_score_benchmark,
        }
        for record in evidence_integration.evidence_records
        if record.denied_reason_summary is not None
    )

    return GovernedMCPObservationSnapshot(
        snapshot_id="governed-mcp-observation::composition-structural-001",
        source_snapshot_id=execution_plan.source_snapshot_id,
        manifest_summary=summarize_tool_manifest(manifest),
        execution_summary=summarize_tool_execution_plan(execution_plan),
        evidence_summary=summarize_tool_evidence_integration(evidence_integration),
        tool_catalog=tuple(
            {
                "tool_id": tool.tool_id,
                "display_name": tool.display_name,
                "capability_type": tool.capability_type,
                "access_mode": tool.access_mode.value,
                "allowed_operations": tool.allowed_operations,
                "prohibited_operations": tool.prohibited_operations,
                "requires_human_approval": tool.requires_human_approval,
                "autonomous_execution_allowed": tool.autonomous_execution_allowed,
                "benchmark_scoring_allowed": tool.benchmark_scoring_allowed,
                "provenance_required": tool.provenance_required,
            }
            for tool in manifest.tools
        ),
        governance_boundaries=(
            "governed_mcp_tool_manifest_required",
            "tool_request_envelope_required",
            "permission_validation_required",
            "provenance_required",
            "audit_required",
            "kill_switch_required",
            "budget_check_required",
            "degraded_mode_required",
            "denied_tool_calls_recorded",
            "real_tool_execution_blocked",
            "tool_output_cannot_define_benchmark_truth",
            "tool_output_cannot_score_benchmark",
            "human_approval_required",
            "autonomous_execution_disabled",
        ),
        denied_tool_records=denied_records,
        manifest_view={
            "summary": summarize_tool_manifest(manifest),
            "tools": [
                {
                    "tool_id": tool.tool_id,
                    "display_name": tool.display_name,
                    "capability_type": tool.capability_type,
                    "access_mode": tool.access_mode.value,
                    "allowed_operations": list(tool.allowed_operations),
                    "prohibited_operations": list(tool.prohibited_operations),
                    "data_classes": list(tool.data_classes),
                    "max_result_items": tool.max_result_items,
                    "requires_human_approval": tool.requires_human_approval,
                    "autonomous_execution_allowed": tool.autonomous_execution_allowed,
                    "benchmark_scoring_allowed": tool.benchmark_scoring_allowed,
                    "provenance_required": tool.provenance_required,
                }
                for tool in manifest.tools
            ],
        },
        execution_view=tool_execution_to_view_model(execution_plan),
        evidence_view=tool_evidence_to_view_model(evidence_integration),
        real_tool_execution_performed=False,
        human_approval_required=True,
        autonomous_execution_allowed=False,
        benchmark_scoring_allowed_from_tool_output=False,
        tool_output_can_define_benchmark_truth=False,
        provenance="governed_mcp_observation:snapshot",
    )


def summarize_governed_mcp_observation(
    snapshot: GovernedMCPObservationSnapshot,
) -> dict[str, object]:
    return {
        "snapshot_id": snapshot.snapshot_id,
        "source_snapshot_id": snapshot.source_snapshot_id,
        "tool_count": snapshot.manifest_summary["tool_count"],
        "envelope_count": snapshot.execution_summary["envelope_count"],
        "validation_count": snapshot.execution_summary["validation_count"],
        "allowed_count": snapshot.execution_summary["allowed_count"],
        "denied_count": snapshot.execution_summary["denied_count"],
        "evidence_record_count": snapshot.evidence_summary["evidence_record_count"],
        "available_evidence_count": snapshot.evidence_summary["available_count"],
        "denied_evidence_count": snapshot.evidence_summary["denied_count"],
        "degraded_evidence_count": snapshot.evidence_summary["degraded_count"],
        "real_tool_execution_performed": snapshot.real_tool_execution_performed,
        "human_approval_required": snapshot.human_approval_required,
        "autonomous_execution_allowed": snapshot.autonomous_execution_allowed,
        "benchmark_scoring_allowed_from_tool_output": (
            snapshot.benchmark_scoring_allowed_from_tool_output
        ),
        "tool_output_can_define_benchmark_truth": (
            snapshot.tool_output_can_define_benchmark_truth
        ),
    }


def to_view_model(snapshot: GovernedMCPObservationSnapshot) -> dict[str, Any]:
    return {
        "summary": summarize_governed_mcp_observation(snapshot),
        "governance_boundaries": list(snapshot.governance_boundaries),
        "tool_catalog": list(snapshot.tool_catalog),
        "denied_tool_records": list(snapshot.denied_tool_records),
        "manifest": snapshot.manifest_view,
        "execution": snapshot.execution_view,
        "evidence": snapshot.evidence_view,
        "real_tool_execution_performed": snapshot.real_tool_execution_performed,
        "human_approval_required": snapshot.human_approval_required,
        "autonomous_execution_allowed": snapshot.autonomous_execution_allowed,
        "benchmark_scoring_allowed_from_tool_output": (
            snapshot.benchmark_scoring_allowed_from_tool_output
        ),
        "tool_output_can_define_benchmark_truth": (
            snapshot.tool_output_can_define_benchmark_truth
        ),
        "provenance": snapshot.provenance,
    }
