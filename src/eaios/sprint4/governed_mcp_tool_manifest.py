"""Sprint 4C governed MCP tool manifest.

Classification: governed MCP/tool boundary.

This module defines the tool manifest and permission policy for Sprint 4C.
It does not execute tools.

Boundary:
- no real tool execution
- no autonomous remediation
- no silent external action
- no benchmark scoring from tool output
- provenance and audit required
- human approval required
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import json
from pathlib import Path
from typing import Any


DEFAULT_MCP_TOOL_MANIFEST_PATH = Path(
    "data/domain/it_application_health/governed_mcp_tool_manifest.json"
)


class ToolAccessMode(str, Enum):
    READ_ONLY = "read_only"
    PROPOSAL_ONLY = "proposal_only"
    DRAFT_ONLY = "draft_only"


class ToolPermissionDecision(str, Enum):
    ALLOWED_WITH_GOVERNANCE = "ALLOWED_WITH_GOVERNANCE"
    DENIED_UNKNOWN_TOOL = "DENIED_UNKNOWN_TOOL"
    DENIED_OPERATION_NOT_ALLOWED = "DENIED_OPERATION_NOT_ALLOWED"
    DENIED_GLOBAL_OPERATION = "DENIED_GLOBAL_OPERATION"
    DENIED_AUTONOMOUS_EXECUTION = "DENIED_AUTONOMOUS_EXECUTION"
    DENIED_BENCHMARK_SCORING = "DENIED_BENCHMARK_SCORING"
    DENIED_MISSING_HUMAN_APPROVAL = "DENIED_MISSING_HUMAN_APPROVAL"


@dataclass(frozen=True)
class GovernedMCPTool:
    tool_id: str
    display_name: str
    capability_type: str
    access_mode: ToolAccessMode
    allowed_operations: tuple[str, ...]
    prohibited_operations: tuple[str, ...]
    data_classes: tuple[str, ...]
    max_result_items: int
    requires_human_approval: bool
    autonomous_execution_allowed: bool
    benchmark_scoring_allowed: bool
    provenance_required: bool


@dataclass(frozen=True)
class GovernedMCPToolManifest:
    manifest_id: str
    domain: str
    policy: dict[str, Any]
    tools: tuple[GovernedMCPTool, ...]
    globally_denied_operations: tuple[str, ...]
    required_request_fields: tuple[str, ...]


@dataclass(frozen=True)
class MCPToolRequest:
    request_id: str
    tool_id: str
    operation: str
    purpose: str
    cluster_id: str
    source_failure_case_id: str
    requested_by_agent: str
    human_approval_required: bool
    autonomous_execution_requested: bool
    benchmark_scoring_requested: bool


@dataclass(frozen=True)
class MCPToolPermissionResult:
    request_id: str
    tool_id: str
    operation: str
    decision: ToolPermissionDecision
    allowed: bool
    reasons: tuple[str, ...]
    human_approval_required: bool
    autonomous_execution_allowed: bool
    benchmark_scoring_allowed: bool
    provenance_required: bool
    audit_required: bool


def load_governed_mcp_tool_manifest(
    path: str | Path = DEFAULT_MCP_TOOL_MANIFEST_PATH,
) -> GovernedMCPToolManifest:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    policy = payload["policy"]

    if policy["real_tool_execution_allowed"] is not False:
        raise ValueError("Sprint 4C manifest must not allow real tool execution.")
    if policy["autonomous_action_allowed"] is not False:
        raise ValueError("Sprint 4C manifest must not allow autonomous action.")
    if policy["human_approval_required"] is not True:
        raise ValueError("Sprint 4C manifest must require human approval.")
    if policy["benchmark_scoring_allowed_from_tool_output"] is not False:
        raise ValueError("Tool output must not score benchmarks.")
    if policy["tool_output_can_define_benchmark_truth"] is not False:
        raise ValueError("Tool output must not define benchmark truth.")
    if policy["provenance_required"] is not True:
        raise ValueError("Tool output provenance is required.")
    if policy["audit_required"] is not True:
        raise ValueError("Tool audit is required.")
    if policy["kill_switch_required"] is not True:
        raise ValueError("Tool kill switch is required.")

    tools = tuple(_parse_tool(raw_tool) for raw_tool in payload["allowed_tools"])

    if any(tool.autonomous_execution_allowed for tool in tools):
        raise ValueError("No governed MCP tool may allow autonomous execution.")
    if any(tool.benchmark_scoring_allowed for tool in tools):
        raise ValueError("No governed MCP tool may score benchmarks.")
    if any(tool.provenance_required is not True for tool in tools):
        raise ValueError("Every governed MCP tool must require provenance.")

    return GovernedMCPToolManifest(
        manifest_id=payload["manifest_id"],
        domain=payload["domain"],
        policy=policy,
        tools=tools,
        globally_denied_operations=tuple(payload["globally_denied_operations"]),
        required_request_fields=tuple(payload["required_request_fields"]),
    )


def evaluate_tool_permission(
    manifest: GovernedMCPToolManifest,
    request: MCPToolRequest,
) -> MCPToolPermissionResult:
    tool = _find_tool(manifest, request.tool_id)
    reasons: list[str] = []

    if tool is None:
        return MCPToolPermissionResult(
            request_id=request.request_id,
            tool_id=request.tool_id,
            operation=request.operation,
            decision=ToolPermissionDecision.DENIED_UNKNOWN_TOOL,
            allowed=False,
            reasons=("Unknown tool id.",),
            human_approval_required=True,
            autonomous_execution_allowed=False,
            benchmark_scoring_allowed=False,
            provenance_required=True,
            audit_required=True,
        )

    if request.operation in manifest.globally_denied_operations:
        reasons.append("Operation is globally denied.")
        return _denied_result(
            request=request,
            decision=ToolPermissionDecision.DENIED_GLOBAL_OPERATION,
            reasons=tuple(reasons),
            tool=tool,
        )

    if request.operation in tool.prohibited_operations:
        reasons.append("Operation is prohibited for this tool.")
        return _denied_result(
            request=request,
            decision=ToolPermissionDecision.DENIED_OPERATION_NOT_ALLOWED,
            reasons=tuple(reasons),
            tool=tool,
        )

    if request.operation not in tool.allowed_operations:
        reasons.append("Operation is not explicitly allowed for this tool.")
        return _denied_result(
            request=request,
            decision=ToolPermissionDecision.DENIED_OPERATION_NOT_ALLOWED,
            reasons=tuple(reasons),
            tool=tool,
        )

    if request.autonomous_execution_requested:
        reasons.append("Autonomous execution was requested and is blocked.")
        return _denied_result(
            request=request,
            decision=ToolPermissionDecision.DENIED_AUTONOMOUS_EXECUTION,
            reasons=tuple(reasons),
            tool=tool,
        )

    if request.benchmark_scoring_requested:
        reasons.append("Benchmark scoring from tool output was requested and is blocked.")
        return _denied_result(
            request=request,
            decision=ToolPermissionDecision.DENIED_BENCHMARK_SCORING,
            reasons=tuple(reasons),
            tool=tool,
        )

    if request.human_approval_required is not True:
        reasons.append("Human approval boundary was not preserved.")
        return _denied_result(
            request=request,
            decision=ToolPermissionDecision.DENIED_MISSING_HUMAN_APPROVAL,
            reasons=tuple(reasons),
            tool=tool,
        )

    return MCPToolPermissionResult(
        request_id=request.request_id,
        tool_id=request.tool_id,
        operation=request.operation,
        decision=ToolPermissionDecision.ALLOWED_WITH_GOVERNANCE,
        allowed=True,
        reasons=("Tool request allowed by manifest but execution remains simulated/governed.",),
        human_approval_required=True,
        autonomous_execution_allowed=False,
        benchmark_scoring_allowed=False,
        provenance_required=tool.provenance_required,
        audit_required=True,
    )


def summarize_tool_manifest(
    manifest: GovernedMCPToolManifest,
) -> dict[str, object]:
    return {
        "manifest_id": manifest.manifest_id,
        "domain": manifest.domain,
        "tool_count": len(manifest.tools),
        "tool_ids": tuple(tool.tool_id for tool in manifest.tools),
        "globally_denied_operation_count": len(manifest.globally_denied_operations),
        "human_approval_required": manifest.policy["human_approval_required"],
        "autonomous_action_allowed": manifest.policy["autonomous_action_allowed"],
        "benchmark_scoring_allowed_from_tool_output": (
            manifest.policy["benchmark_scoring_allowed_from_tool_output"]
        ),
        "provenance_required": manifest.policy["provenance_required"],
        "audit_required": manifest.policy["audit_required"],
        "kill_switch_required": manifest.policy["kill_switch_required"],
    }


def _parse_tool(raw_tool: dict[str, Any]) -> GovernedMCPTool:
    return GovernedMCPTool(
        tool_id=raw_tool["tool_id"],
        display_name=raw_tool["display_name"],
        capability_type=raw_tool["capability_type"],
        access_mode=ToolAccessMode(raw_tool["access_mode"]),
        allowed_operations=tuple(raw_tool["allowed_operations"]),
        prohibited_operations=tuple(raw_tool["prohibited_operations"]),
        data_classes=tuple(raw_tool["data_classes"]),
        max_result_items=int(raw_tool["max_result_items"]),
        requires_human_approval=bool(raw_tool["requires_human_approval"]),
        autonomous_execution_allowed=bool(raw_tool["autonomous_execution_allowed"]),
        benchmark_scoring_allowed=bool(raw_tool["benchmark_scoring_allowed"]),
        provenance_required=bool(raw_tool["provenance_required"]),
    )


def _find_tool(
    manifest: GovernedMCPToolManifest,
    tool_id: str,
) -> GovernedMCPTool | None:
    return next((tool for tool in manifest.tools if tool.tool_id == tool_id), None)


def _denied_result(
    request: MCPToolRequest,
    decision: ToolPermissionDecision,
    reasons: tuple[str, ...],
    tool: GovernedMCPTool,
) -> MCPToolPermissionResult:
    return MCPToolPermissionResult(
        request_id=request.request_id,
        tool_id=request.tool_id,
        operation=request.operation,
        decision=decision,
        allowed=False,
        reasons=reasons,
        human_approval_required=True,
        autonomous_execution_allowed=False,
        benchmark_scoring_allowed=False,
        provenance_required=tool.provenance_required,
        audit_required=True,
    )
