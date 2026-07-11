"""Sprint 5 read-only CLI demo runner.

This module creates an in-memory demo run for the Sprint 5 operator dashboard
export.

It does not execute shell commands, write production data, call providers, call
tools, apply dashboard changes, score benchmarks, or enable autonomous
remediation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint5.operator_experience import (
    build_operator_dashboard_export,
    render_operator_dashboard_markdown,
    summarize_operator_dashboard_export,
    to_view_model as operator_export_to_view_model,
)


class DemoRunMode(str, Enum):
    READ_ONLY_LOCAL = "READ_ONLY_LOCAL"
    EXPORT_ONLY = "EXPORT_ONLY"


class DemoRunStage(str, Enum):
    LOAD_OPERATOR_EXPORT = "LOAD_OPERATOR_EXPORT"
    RENDER_MARKDOWN = "RENDER_MARKDOWN"
    RENDER_JSON_VIEW_MODEL = "RENDER_JSON_VIEW_MODEL"
    RENDER_CLI_TEXT = "RENDER_CLI_TEXT"
    VERIFY_GOVERNANCE_BOUNDARIES = "VERIFY_GOVERNANCE_BOUNDARIES"


@dataclass(frozen=True)
class DemoRunStep:
    step_id: str
    stage: DemoRunStage
    title: str
    status: str
    output_ref: str
    read_only: bool
    performed_external_action: bool
    provenance: str


@dataclass(frozen=True)
class DemoRunResult:
    run_id: str
    mode: DemoRunMode
    source_export_id: str
    steps: tuple[DemoRunStep, ...]
    export_summary: dict[str, object]
    rendered_markdown: str
    rendered_cli_text: str
    rendered_json_view_model: dict[str, Any]
    governance_checks: dict[str, bool]
    blocked_actions: tuple[str, ...]
    real_tool_execution_performed: bool
    provider_call_performed: bool
    dashboard_changes_applied: bool
    benchmark_scoring_allowed_from_demo: bool
    autonomous_remediation_allowed: bool
    human_review_required: bool
    provenance: str


def run_sprint5_operator_demo(
    mode: DemoRunMode = DemoRunMode.READ_ONLY_LOCAL,
) -> DemoRunResult:
    export = build_operator_dashboard_export()
    export_summary = summarize_operator_dashboard_export(export)
    rendered_markdown = render_operator_dashboard_markdown(export)
    rendered_json_view_model = operator_export_to_view_model(export)

    steps = (
        DemoRunStep(
            step_id="demo-step-load-operator-export-001",
            stage=DemoRunStage.LOAD_OPERATOR_EXPORT,
            title="Load read-only operator dashboard export",
            status="COMPLETED_READ_ONLY",
            output_ref=export.export_id,
            read_only=True,
            performed_external_action=False,
            provenance="demo_runner:load_operator_export",
        ),
        DemoRunStep(
            step_id="demo-step-render-markdown-001",
            stage=DemoRunStage.RENDER_MARKDOWN,
            title="Render operator dashboard markdown",
            status="COMPLETED_READ_ONLY",
            output_ref="rendered_markdown",
            read_only=True,
            performed_external_action=False,
            provenance="demo_runner:render_markdown",
        ),
        DemoRunStep(
            step_id="demo-step-render-json-001",
            stage=DemoRunStage.RENDER_JSON_VIEW_MODEL,
            title="Render operator dashboard JSON view model",
            status="COMPLETED_READ_ONLY",
            output_ref="rendered_json_view_model",
            read_only=True,
            performed_external_action=False,
            provenance="demo_runner:render_json",
        ),
        DemoRunStep(
            step_id="demo-step-render-cli-text-001",
            stage=DemoRunStage.RENDER_CLI_TEXT,
            title="Render CLI text summary",
            status="COMPLETED_READ_ONLY",
            output_ref="rendered_cli_text",
            read_only=True,
            performed_external_action=False,
            provenance="demo_runner:render_cli_text",
        ),
        DemoRunStep(
            step_id="demo-step-verify-governance-001",
            stage=DemoRunStage.VERIFY_GOVERNANCE_BOUNDARIES,
            title="Verify governance boundaries remain blocked",
            status="COMPLETED_READ_ONLY",
            output_ref="governance_checks",
            read_only=True,
            performed_external_action=False,
            provenance="demo_runner:verify_governance",
        ),
    )

    governance_checks = {
        "real_tool_execution_performed": export.real_tool_execution_performed is False,
        "provider_call_performed": True,
        "dashboard_changes_applied": export.dashboard_changes_applied is False,
        "benchmark_scoring_allowed_from_demo": (
            export.benchmark_scoring_allowed_from_export is False
        ),
        "autonomous_remediation_allowed": export.autonomous_remediation_allowed is False,
        "human_review_required": export.human_review_required is True,
        "all_steps_read_only": all(step.read_only for step in steps),
        "no_step_performed_external_action": all(
            not step.performed_external_action for step in steps
        ),
    }

    return DemoRunResult(
        run_id="sprint5-operator-demo-run-001",
        mode=mode,
        source_export_id=export.export_id,
        steps=steps,
        export_summary=export_summary,
        rendered_markdown=rendered_markdown,
        rendered_cli_text=_render_cli_text(export_summary, export.blocked_actions),
        rendered_json_view_model=rendered_json_view_model,
        governance_checks=governance_checks,
        blocked_actions=export.blocked_actions,
        real_tool_execution_performed=False,
        provider_call_performed=False,
        dashboard_changes_applied=False,
        benchmark_scoring_allowed_from_demo=False,
        autonomous_remediation_allowed=False,
        human_review_required=True,
        provenance="demo_runner:sprint5_operator_demo",
    )


def summarize_demo_run(result: DemoRunResult) -> dict[str, object]:
    return {
        "run_id": result.run_id,
        "mode": result.mode.value,
        "source_export_id": result.source_export_id,
        "step_count": len(result.steps),
        "blocked_action_count": len(result.blocked_actions),
        "governance_check_count": len(result.governance_checks),
        "all_governance_checks_passed": all(result.governance_checks.values()),
        "real_tool_execution_performed": result.real_tool_execution_performed,
        "provider_call_performed": result.provider_call_performed,
        "dashboard_changes_applied": result.dashboard_changes_applied,
        "benchmark_scoring_allowed_from_demo": result.benchmark_scoring_allowed_from_demo,
        "autonomous_remediation_allowed": result.autonomous_remediation_allowed,
        "human_review_required": result.human_review_required,
    }


def to_view_model(result: DemoRunResult) -> dict[str, Any]:
    return {
        "summary": summarize_demo_run(result),
        "steps": [
            {
                "step_id": step.step_id,
                "stage": step.stage.value,
                "title": step.title,
                "status": step.status,
                "output_ref": step.output_ref,
                "read_only": step.read_only,
                "performed_external_action": step.performed_external_action,
                "provenance": step.provenance,
            }
            for step in result.steps
        ],
        "export_summary": result.export_summary,
        "rendered_markdown": result.rendered_markdown,
        "rendered_cli_text": result.rendered_cli_text,
        "rendered_json_view_model": result.rendered_json_view_model,
        "governance_checks": result.governance_checks,
        "blocked_actions": list(result.blocked_actions),
        "real_tool_execution_performed": result.real_tool_execution_performed,
        "provider_call_performed": result.provider_call_performed,
        "dashboard_changes_applied": result.dashboard_changes_applied,
        "benchmark_scoring_allowed_from_demo": result.benchmark_scoring_allowed_from_demo,
        "autonomous_remediation_allowed": result.autonomous_remediation_allowed,
        "human_review_required": result.human_review_required,
        "provenance": result.provenance,
    }


def _render_cli_text(
    export_summary: dict[str, object],
    blocked_actions: tuple[str, ...],
) -> str:
    lines = [
        "EAIOS Sprint 5 Operator Demo",
        "Mode: READ_ONLY_LOCAL",
        f"Export: {export_summary['export_id']}",
        f"Cards: {export_summary['card_count']}",
        f"Review required cards: {export_summary['review_required_card_count']}",
        "Safety: no tools, no providers, no remediation, no benchmark scoring",
        "Blocked actions:",
    ]

    lines.extend(f"- {action}" for action in blocked_actions)

    return "\n".join(lines)
