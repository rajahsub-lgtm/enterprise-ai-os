"""Sprint 6 local CLI entrypoint contract.

This module defines a safe local CLI contract for the portfolio demo.

It does not execute shell commands, write package files, deploy cloud resources,
load secrets, call providers, connect real tools, execute remediation, send
notifications, score benchmarks, or enable autonomous remediation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint6.demo_package import (
    build_demo_package_manifest,
    render_demo_package_manifest_text,
    summarize_demo_package_manifest,
    to_view_model as demo_package_to_view_model,
)


class LocalCLICommand(str, Enum):
    SHOW_PACKAGE_MANIFEST = "SHOW_PACKAGE_MANIFEST"
    SHOW_GOVERNANCE_BOUNDARIES = "SHOW_GOVERNANCE_BOUNDARIES"
    SHOW_READINESS_SUMMARY = "SHOW_READINESS_SUMMARY"


class LocalCLIOutputFormat(str, Enum):
    TEXT = "TEXT"
    JSON_VIEW_MODEL = "JSON_VIEW_MODEL"


class LocalCLIState(str, Enum):
    COMPLETED_READ_ONLY = "COMPLETED_READ_ONLY"
    BLOCKED_UNSUPPORTED_COMMAND = "BLOCKED_UNSUPPORTED_COMMAND"
    BLOCKED_NON_READ_ONLY = "BLOCKED_NON_READ_ONLY"


@dataclass(frozen=True)
class LocalCLIInvocation:
    invocation_id: str
    argv: tuple[str, ...]
    command: LocalCLICommand | str
    output_format: LocalCLIOutputFormat | str
    read_only: bool
    provenance: str


@dataclass(frozen=True)
class LocalCLIResult:
    result_id: str
    invocation_id: str
    state: LocalCLIState
    command: str
    output_format: str
    rendered_output: str | dict[str, Any]
    manifest_summary: dict[str, object]
    blocked_actions: tuple[str, ...]
    shell_commands_executed: bool
    package_files_written: bool
    external_files_written: bool
    cloud_resources_created: bool
    secrets_loaded: bool
    provider_calls_performed: bool
    real_connectors_called: bool
    remediation_performed: bool
    notifications_sent: bool
    benchmark_scoring_performed: bool
    autonomous_remediation_allowed: bool
    human_review_required: bool
    provenance: str


def build_default_local_cli_invocation() -> LocalCLIInvocation:
    return LocalCLIInvocation(
        invocation_id="sprint6-local-cli-invocation-001",
        argv=(
            "eaios",
            "sprint6",
            "package",
            "show-manifest",
            "--read-only",
            "--format",
            "text",
        ),
        command=LocalCLICommand.SHOW_PACKAGE_MANIFEST,
        output_format=LocalCLIOutputFormat.TEXT,
        read_only=True,
        provenance="local_cli:default_invocation",
    )


def run_local_cli_entrypoint(
    invocation: LocalCLIInvocation | None = None,
) -> LocalCLIResult:
    if invocation is None:
        invocation = build_default_local_cli_invocation()

    if invocation.read_only is not True:
        return _blocked_result(invocation, LocalCLIState.BLOCKED_NON_READ_ONLY)

    try:
        command = LocalCLICommand(invocation.command)
    except ValueError:
        return _blocked_result(invocation, LocalCLIState.BLOCKED_UNSUPPORTED_COMMAND)

    try:
        output_format = LocalCLIOutputFormat(invocation.output_format)
    except ValueError:
        return _blocked_result(invocation, LocalCLIState.BLOCKED_UNSUPPORTED_COMMAND)

    manifest = build_demo_package_manifest()
    manifest_summary = summarize_demo_package_manifest(manifest)

    if output_format == LocalCLIOutputFormat.JSON_VIEW_MODEL:
        rendered_output: str | dict[str, Any] = demo_package_to_view_model(manifest)
    elif command == LocalCLICommand.SHOW_GOVERNANCE_BOUNDARIES:
        rendered_output = _render_governance_boundaries(manifest.blocked_actions)
    elif command == LocalCLICommand.SHOW_READINESS_SUMMARY:
        rendered_output = _render_readiness_summary(manifest_summary)
    else:
        rendered_output = render_demo_package_manifest_text(manifest)

    return LocalCLIResult(
        result_id="sprint6-local-cli-result-001",
        invocation_id=invocation.invocation_id,
        state=LocalCLIState.COMPLETED_READ_ONLY,
        command=command.value,
        output_format=output_format.value,
        rendered_output=rendered_output,
        manifest_summary=manifest_summary,
        blocked_actions=manifest.blocked_actions,
        shell_commands_executed=False,
        package_files_written=False,
        external_files_written=False,
        cloud_resources_created=False,
        secrets_loaded=False,
        provider_calls_performed=False,
        real_connectors_called=False,
        remediation_performed=False,
        notifications_sent=False,
        benchmark_scoring_performed=False,
        autonomous_remediation_allowed=False,
        human_review_required=True,
        provenance="local_cli:result",
    )


def summarize_local_cli_result(result: LocalCLIResult) -> dict[str, object]:
    return {
        "result_id": result.result_id,
        "invocation_id": result.invocation_id,
        "state": result.state.value,
        "command": result.command,
        "output_format": result.output_format,
        "blocked_action_count": len(result.blocked_actions),
        "shell_commands_executed": result.shell_commands_executed,
        "package_files_written": result.package_files_written,
        "external_files_written": result.external_files_written,
        "cloud_resources_created": result.cloud_resources_created,
        "secrets_loaded": result.secrets_loaded,
        "provider_calls_performed": result.provider_calls_performed,
        "real_connectors_called": result.real_connectors_called,
        "remediation_performed": result.remediation_performed,
        "notifications_sent": result.notifications_sent,
        "benchmark_scoring_performed": result.benchmark_scoring_performed,
        "autonomous_remediation_allowed": result.autonomous_remediation_allowed,
        "human_review_required": result.human_review_required,
    }


def to_view_model(result: LocalCLIResult) -> dict[str, Any]:
    return {
        "summary": summarize_local_cli_result(result),
        "rendered_output": result.rendered_output,
        "manifest_summary": result.manifest_summary,
        "blocked_actions": list(result.blocked_actions),
        "provenance": result.provenance,
    }


def _render_governance_boundaries(blocked_actions: tuple[str, ...]) -> str:
    lines = "\n".join(f"- {item}" for item in blocked_actions)
    return "# EAIOS Governance Boundaries\n\nBlocked actions:\n" + lines + "\n"


def _render_readiness_summary(summary: dict[str, object]) -> str:
    return (
        "# EAIOS Readiness Summary\n\n"
        f"Manifest: {summary['manifest_id']}\n"
        f"Mode: {summary['mode']}\n"
        f"Artifacts: {summary['artifact_count']}\n"
        f"Blocked actions: {summary['blocked_action_count']}\n"
        "Human review required: true\n"
    )


def _blocked_result(
    invocation: LocalCLIInvocation,
    state: LocalCLIState,
) -> LocalCLIResult:
    return LocalCLIResult(
        result_id="sprint6-local-cli-result-blocked-001",
        invocation_id=invocation.invocation_id,
        state=state,
        command=str(invocation.command),
        output_format=str(invocation.output_format),
        rendered_output=f"Blocked: {state.value}",
        manifest_summary={},
        blocked_actions=(
            "shell_command_execution",
            "package_file_write",
            "cloud_resource_creation",
            "secret_loading",
            "provider_call",
            "real_connector_call",
            "remediation_execution",
            "notification_send",
            "benchmark_scoring",
            "autonomous_remediation",
        ),
        shell_commands_executed=False,
        package_files_written=False,
        external_files_written=False,
        cloud_resources_created=False,
        secrets_loaded=False,
        provider_calls_performed=False,
        real_connectors_called=False,
        remediation_performed=False,
        notifications_sent=False,
        benchmark_scoring_performed=False,
        autonomous_remediation_allowed=False,
        human_review_required=True,
        provenance="local_cli:blocked_result",
    )
