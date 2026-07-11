"""Sprint 5 single end-to-end scenario command contract.

This module defines one read-only command path for the benchmark-grounded
application-health demo.

It does not execute shell commands, call tools, call providers, apply dashboard
changes, score benchmarks, or enable autonomous remediation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint5.demo_runner import (
    DemoRunResult,
    run_sprint5_operator_demo,
    summarize_demo_run,
    to_view_model as demo_run_to_view_model,
)


class ScenarioCommandName(str, Enum):
    RUN_APPLICATION_HEALTH_DEMO = "RUN_APPLICATION_HEALTH_DEMO"
    EXPORT_OPERATOR_DASHBOARD = "EXPORT_OPERATOR_DASHBOARD"
    VERIFY_GOVERNANCE_BOUNDARIES = "VERIFY_GOVERNANCE_BOUNDARIES"


class ScenarioOutputFormat(str, Enum):
    CLI_TEXT = "CLI_TEXT"
    MARKDOWN = "MARKDOWN"
    JSON_VIEW_MODEL = "JSON_VIEW_MODEL"


class ScenarioCommandState(str, Enum):
    COMPLETED_READ_ONLY = "COMPLETED_READ_ONLY"
    BLOCKED_UNSUPPORTED_COMMAND = "BLOCKED_UNSUPPORTED_COMMAND"
    BLOCKED_NON_READ_ONLY_INVOCATION = "BLOCKED_NON_READ_ONLY_INVOCATION"


@dataclass(frozen=True)
class ScenarioCommandInvocation:
    invocation_id: str
    command_name: ScenarioCommandName | str
    output_format: ScenarioOutputFormat | str
    scenario_name: str
    read_only: bool
    requested_by: str
    command_path: str


@dataclass(frozen=True)
class ScenarioCommandResult:
    result_id: str
    invocation_id: str
    command_name: str
    output_format: str
    scenario_name: str
    state: ScenarioCommandState
    source_demo_run_id: str
    command_path: str
    rendered_output: str | dict[str, Any]
    demo_summary: dict[str, object]
    stage_names: tuple[str, ...]
    governance_checks: dict[str, bool]
    blocked_actions: tuple[str, ...]
    real_shell_command_executed: bool
    real_tool_execution_performed: bool
    provider_call_performed: bool
    dashboard_changes_applied: bool
    benchmark_scoring_allowed_from_command: bool
    autonomous_remediation_allowed: bool
    human_review_required: bool
    provenance: str


def build_default_scenario_command_invocation() -> ScenarioCommandInvocation:
    return ScenarioCommandInvocation(
        invocation_id="sprint5-scenario-command-invocation-001",
        command_name=ScenarioCommandName.RUN_APPLICATION_HEALTH_DEMO,
        output_format=ScenarioOutputFormat.CLI_TEXT,
        scenario_name="application-health",
        read_only=True,
        requested_by="operator-demo",
        command_path="eaios sprint5 run --scenario application-health --read-only",
    )


def run_sprint5_scenario_command(
    invocation: ScenarioCommandInvocation | None = None,
) -> ScenarioCommandResult:
    if invocation is None:
        invocation = build_default_scenario_command_invocation()

    if invocation.read_only is not True:
        return _blocked_command_result(
            invocation=invocation,
            reason="Scenario command must be read-only.",
            state=ScenarioCommandState.BLOCKED_NON_READ_ONLY_INVOCATION,
        )

    try:
        command_name = ScenarioCommandName(invocation.command_name)
    except ValueError:
        return _blocked_command_result(
            invocation=invocation,
            reason=f"Unsupported command: {invocation.command_name}",
            state=ScenarioCommandState.BLOCKED_UNSUPPORTED_COMMAND,
        )

    try:
        output_format = ScenarioOutputFormat(invocation.output_format)
    except ValueError:
        return _blocked_command_result(
            invocation=invocation,
            reason=f"Unsupported output format: {invocation.output_format}",
            state=ScenarioCommandState.BLOCKED_UNSUPPORTED_COMMAND,
        )

    demo = run_sprint5_operator_demo()
    rendered_output = _render_output(demo, output_format)
    demo_summary = summarize_demo_run(demo)

    governance_checks = {
        **demo.governance_checks,
        "real_shell_command_not_executed": True,
        "command_invocation_read_only": invocation.read_only is True,
        "supported_command": command_name in ScenarioCommandName,
        "supported_output_format": output_format in ScenarioOutputFormat,
        "application_health_scenario": invocation.scenario_name == "application-health",
    }

    return ScenarioCommandResult(
        result_id="sprint5-scenario-command-result-001",
        invocation_id=invocation.invocation_id,
        command_name=command_name.value,
        output_format=output_format.value,
        scenario_name=invocation.scenario_name,
        state=ScenarioCommandState.COMPLETED_READ_ONLY,
        source_demo_run_id=demo.run_id,
        command_path=invocation.command_path,
        rendered_output=rendered_output,
        demo_summary=demo_summary,
        stage_names=tuple(step.stage.value for step in demo.steps),
        governance_checks=governance_checks,
        blocked_actions=demo.blocked_actions,
        real_shell_command_executed=False,
        real_tool_execution_performed=False,
        provider_call_performed=False,
        dashboard_changes_applied=False,
        benchmark_scoring_allowed_from_command=False,
        autonomous_remediation_allowed=False,
        human_review_required=True,
        provenance="scenario_command:read_only_application_health_command",
    )


def summarize_scenario_command_result(
    result: ScenarioCommandResult,
) -> dict[str, object]:
    return {
        "result_id": result.result_id,
        "invocation_id": result.invocation_id,
        "command_name": result.command_name,
        "output_format": result.output_format,
        "scenario_name": result.scenario_name,
        "state": result.state.value,
        "source_demo_run_id": result.source_demo_run_id,
        "stage_count": len(result.stage_names),
        "blocked_action_count": len(result.blocked_actions),
        "governance_check_count": len(result.governance_checks),
        "all_governance_checks_passed": all(result.governance_checks.values()),
        "real_shell_command_executed": result.real_shell_command_executed,
        "real_tool_execution_performed": result.real_tool_execution_performed,
        "provider_call_performed": result.provider_call_performed,
        "dashboard_changes_applied": result.dashboard_changes_applied,
        "benchmark_scoring_allowed_from_command": (
            result.benchmark_scoring_allowed_from_command
        ),
        "autonomous_remediation_allowed": result.autonomous_remediation_allowed,
        "human_review_required": result.human_review_required,
    }


def to_view_model(result: ScenarioCommandResult) -> dict[str, Any]:
    return {
        "summary": summarize_scenario_command_result(result),
        "command_path": result.command_path,
        "rendered_output": result.rendered_output,
        "demo_summary": result.demo_summary,
        "stage_names": list(result.stage_names),
        "governance_checks": result.governance_checks,
        "blocked_actions": list(result.blocked_actions),
        "real_shell_command_executed": result.real_shell_command_executed,
        "real_tool_execution_performed": result.real_tool_execution_performed,
        "provider_call_performed": result.provider_call_performed,
        "dashboard_changes_applied": result.dashboard_changes_applied,
        "benchmark_scoring_allowed_from_command": (
            result.benchmark_scoring_allowed_from_command
        ),
        "autonomous_remediation_allowed": result.autonomous_remediation_allowed,
        "human_review_required": result.human_review_required,
        "provenance": result.provenance,
    }


def _render_output(
    demo: DemoRunResult,
    output_format: ScenarioOutputFormat,
) -> str | dict[str, Any]:
    if output_format == ScenarioOutputFormat.CLI_TEXT:
        return demo.rendered_cli_text
    if output_format == ScenarioOutputFormat.MARKDOWN:
        return demo.rendered_markdown
    return demo_run_to_view_model(demo)


def _blocked_command_result(
    invocation: ScenarioCommandInvocation,
    reason: str,
    state: ScenarioCommandState,
) -> ScenarioCommandResult:
    governance_checks = {
        "real_shell_command_not_executed": True,
        "real_tool_execution_not_performed": True,
        "provider_call_not_performed": True,
        "dashboard_changes_not_applied": True,
        "benchmark_scoring_not_allowed_from_command": True,
        "autonomous_remediation_not_allowed": True,
        "human_review_required": True,
        "blocked_reason_recorded": True,
    }

    return ScenarioCommandResult(
        result_id="sprint5-scenario-command-result-blocked-001",
        invocation_id=invocation.invocation_id,
        command_name=str(invocation.command_name),
        output_format=str(invocation.output_format),
        scenario_name=invocation.scenario_name,
        state=state,
        source_demo_run_id="",
        command_path=invocation.command_path,
        rendered_output=reason,
        demo_summary={},
        stage_names=(),
        governance_checks=governance_checks,
        blocked_actions=(
            "real_shell_command_execution",
            "real_tool_execution",
            "provider_call",
            "dashboard_change_application",
            "benchmark_scoring_from_command",
            "autonomous_remediation",
        ),
        real_shell_command_executed=False,
        real_tool_execution_performed=False,
        provider_call_performed=False,
        dashboard_changes_applied=False,
        benchmark_scoring_allowed_from_command=False,
        autonomous_remediation_allowed=False,
        human_review_required=True,
        provenance="scenario_command:blocked_invocation",
    )
