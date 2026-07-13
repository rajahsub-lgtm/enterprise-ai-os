"""Sprint 8 operator demo command.

Canonical read-only command contract for portfolio and interview demos.

It does not execute runtime actions, create releases, publish sites, build
containers, deploy cloud resources, enable providers, enable connectors, persist
approvals, send notifications, execute remediation, score benchmarks, update
benchmark truth, or enable autonomous remediation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint7.demo_release_checklist import (
    build_demo_release_checklist,
    summarize_demo_release_checklist,
)


class OperatorDemoCommandMode(str, Enum):
    REVIEW_ONLY_OPERATOR_COMMAND = "REVIEW_ONLY_OPERATOR_COMMAND"


class OperatorDemoCommandName(str, Enum):
    SHOW_RELEASE_CHECKLIST = "SHOW_RELEASE_CHECKLIST"
    SHOW_RUNTIME_HARDENING_CHAIN = "SHOW_RUNTIME_HARDENING_CHAIN"
    SHOW_HUMAN_APPROVAL_STATUS = "SHOW_HUMAN_APPROVAL_STATUS"
    SHOW_SAFETY_BOUNDARIES = "SHOW_SAFETY_BOUNDARIES"


class OperatorDemoRenderFormat(str, Enum):
    TEXT = "TEXT"
    JSON_VIEW_MODEL = "JSON_VIEW_MODEL"


class OperatorDemoCommandStatus(str, Enum):
    COMPLETED_READ_ONLY = "COMPLETED_READ_ONLY"
    BLOCKED_UNSUPPORTED_COMMAND = "BLOCKED_UNSUPPORTED_COMMAND"
    BLOCKED_NON_READ_ONLY = "BLOCKED_NON_READ_ONLY"


@dataclass(frozen=True)
class OperatorDemoCommandRequest:
    command_name: str
    read_only: bool
    render_format: OperatorDemoRenderFormat


@dataclass(frozen=True)
class OperatorDemoCommandResult:
    command_id: str
    mode: OperatorDemoCommandMode
    command_name: str
    status: OperatorDemoCommandStatus
    title: str
    sections: tuple[str, ...]
    output_lines: tuple[str, ...]
    blocked_actions: tuple[str, ...]
    release_checklist_summary: dict[str, object]
    command_executed: bool
    runtime_actions_executed: bool
    release_created: bool
    archive_created: bool
    static_site_published: bool
    container_built: bool
    cloud_deployed: bool
    provider_enabled: bool
    connector_enabled: bool
    approval_records_persisted: bool
    remediation_performed: bool
    notifications_sent: bool
    benchmark_scoring_performed: bool
    benchmark_truth_updated: bool
    autonomous_remediation_allowed: bool
    human_review_required: bool
    provenance: str


def default_operator_demo_command_request() -> OperatorDemoCommandRequest:
    return OperatorDemoCommandRequest(
        command_name=OperatorDemoCommandName.SHOW_RELEASE_CHECKLIST.value,
        read_only=True,
        render_format=OperatorDemoRenderFormat.TEXT,
    )


def run_operator_demo_command(
    request: OperatorDemoCommandRequest | None = None,
) -> OperatorDemoCommandResult:
    command_request = request or default_operator_demo_command_request()
    checklist = build_demo_release_checklist()
    checklist_summary = summarize_demo_release_checklist(checklist)

    blocked_actions = (
        "execute_runtime_action",
        "create_release_archive",
        "publish_static_site",
        "build_container_image",
        "push_container_image",
        "deploy_to_cloud",
        "enable_real_provider",
        "enable_real_connector",
        "persist_approval_record_to_external_store",
        "send_notification",
        "execute_remediation",
        "score_benchmark_from_demo_command",
        "update_benchmark_truth_from_demo_command",
        "enable_autonomous_remediation",
        "bypass_human_review",
    )

    supported_commands = tuple(item.value for item in OperatorDemoCommandName)

    if command_request.read_only is False:
        return _blocked_result(
            command_name=command_request.command_name,
            status=OperatorDemoCommandStatus.BLOCKED_NON_READ_ONLY,
            title="Operator Demo Command Blocked",
            sections=("non_read_only_request_blocked",),
            output_lines=("Non-read-only operator demo command was blocked.",),
            blocked_actions=blocked_actions,
            checklist_summary=checklist_summary,
        )

    if command_request.command_name not in supported_commands:
        return _blocked_result(
            command_name=command_request.command_name,
            status=OperatorDemoCommandStatus.BLOCKED_UNSUPPORTED_COMMAND,
            title="Operator Demo Command Unsupported",
            sections=("unsupported_command_blocked",),
            output_lines=(f"Unsupported operator demo command: {command_request.command_name}",),
            blocked_actions=blocked_actions,
            checklist_summary=checklist_summary,
        )

    sections, output_lines = _render_supported_command(
        command_name=command_request.command_name,
        checklist_summary=checklist_summary,
    )

    return OperatorDemoCommandResult(
        command_id="sprint8-operator-demo-command-001",
        mode=OperatorDemoCommandMode.REVIEW_ONLY_OPERATOR_COMMAND,
        command_name=command_request.command_name,
        status=OperatorDemoCommandStatus.COMPLETED_READ_ONLY,
        title="EAIOS Sprint 8 Operator Demo Command",
        sections=sections,
        output_lines=output_lines,
        blocked_actions=blocked_actions,
        release_checklist_summary=checklist_summary,
        command_executed=True,
        runtime_actions_executed=False,
        release_created=False,
        archive_created=False,
        static_site_published=False,
        container_built=False,
        cloud_deployed=False,
        provider_enabled=False,
        connector_enabled=False,
        approval_records_persisted=False,
        remediation_performed=False,
        notifications_sent=False,
        benchmark_scoring_performed=False,
        benchmark_truth_updated=False,
        autonomous_remediation_allowed=False,
        human_review_required=True,
        provenance="operator_demo_command:result",
    )


def summarize_operator_demo_command_result(
    result: OperatorDemoCommandResult,
) -> dict[str, object]:
    return {
        "command_id": result.command_id,
        "mode": result.mode.value,
        "command_name": result.command_name,
        "status": result.status.value,
        "title": result.title,
        "section_count": len(result.sections),
        "output_line_count": len(result.output_lines),
        "blocked_action_count": len(result.blocked_actions),
        "command_executed": result.command_executed,
        "runtime_actions_executed": result.runtime_actions_executed,
        "release_created": result.release_created,
        "archive_created": result.archive_created,
        "static_site_published": result.static_site_published,
        "container_built": result.container_built,
        "cloud_deployed": result.cloud_deployed,
        "provider_enabled": result.provider_enabled,
        "connector_enabled": result.connector_enabled,
        "approval_records_persisted": result.approval_records_persisted,
        "remediation_performed": result.remediation_performed,
        "notifications_sent": result.notifications_sent,
        "benchmark_scoring_performed": result.benchmark_scoring_performed,
        "benchmark_truth_updated": result.benchmark_truth_updated,
        "autonomous_remediation_allowed": result.autonomous_remediation_allowed,
        "human_review_required": result.human_review_required,
    }


def to_view_model(result: OperatorDemoCommandResult) -> dict[str, Any]:
    return {
        "summary": summarize_operator_demo_command_result(result),
        "sections": list(result.sections),
        "output_lines": list(result.output_lines),
        "blocked_actions": list(result.blocked_actions),
        "release_checklist_summary": result.release_checklist_summary,
        "provenance": result.provenance,
    }


def _render_supported_command(
    command_name: str,
    checklist_summary: dict[str, object],
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    if command_name == OperatorDemoCommandName.SHOW_RUNTIME_HARDENING_CHAIN.value:
        return (
            ("runtime_hardening_chain", "governance_boundary"),
            (
                "Runtime hardening chain: package, web review, cloud preflight, provider validation, connector classification, audit, approval, release gate.",
                "All runtime hardening surfaces remain review-only.",
            ),
        )

    if command_name == OperatorDemoCommandName.SHOW_HUMAN_APPROVAL_STATUS.value:
        return (
            ("human_approval_status", "approval_boundary"),
            (
                "Human approval is required before release, connector enablement, remediation, notification, or benchmark operations.",
                "No approval records are persisted and no approved actions are executed.",
            ),
        )

    if command_name == OperatorDemoCommandName.SHOW_SAFETY_BOUNDARIES.value:
        return (
            ("safety_boundaries", "blocked_actions"),
            (
                "Providers and MCP connectors remain disabled by default.",
                "Benchmark truth remains isolated from runtime, provider, connector, audit, approval, and release outputs.",
            ),
        )

    return (
        ("release_checklist", "release_readiness"),
        (
            f"Release readiness: {checklist_summary['readiness_status']}",
            f"Checklist items: {checklist_summary['item_count']}",
            f"Blocking items: {checklist_summary['blocking_item_count']}",
            "Release is review-ready but not executable as production.",
        ),
    )


def _blocked_result(
    command_name: str,
    status: OperatorDemoCommandStatus,
    title: str,
    sections: tuple[str, ...],
    output_lines: tuple[str, ...],
    blocked_actions: tuple[str, ...],
    checklist_summary: dict[str, object],
) -> OperatorDemoCommandResult:
    return OperatorDemoCommandResult(
        command_id="sprint8-operator-demo-command-001",
        mode=OperatorDemoCommandMode.REVIEW_ONLY_OPERATOR_COMMAND,
        command_name=command_name,
        status=status,
        title=title,
        sections=sections,
        output_lines=output_lines,
        blocked_actions=blocked_actions,
        release_checklist_summary=checklist_summary,
        command_executed=False,
        runtime_actions_executed=False,
        release_created=False,
        archive_created=False,
        static_site_published=False,
        container_built=False,
        cloud_deployed=False,
        provider_enabled=False,
        connector_enabled=False,
        approval_records_persisted=False,
        remediation_performed=False,
        notifications_sent=False,
        benchmark_scoring_performed=False,
        benchmark_truth_updated=False,
        autonomous_remediation_allowed=False,
        human_review_required=True,
        provenance="operator_demo_command:result",
    )
