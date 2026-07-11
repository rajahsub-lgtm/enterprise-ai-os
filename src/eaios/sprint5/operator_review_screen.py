"""Sprint 5 operator review screen model.

This module converts the single read-only scenario command result into a
UI-ready operator review screen.

It does not execute shell commands, call tools, call providers, apply dashboard
changes, score benchmarks, or enable autonomous remediation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint5.scenario_command import (
    ScenarioCommandResult,
    run_sprint5_scenario_command,
    summarize_scenario_command_result,
    to_view_model as scenario_command_to_view_model,
)


class OperatorReviewScreenMode(str, Enum):
    READ_ONLY_REVIEW = "READ_ONLY_REVIEW"


class OperatorReviewScreenSection(str, Enum):
    SCENARIO_CONTEXT = "SCENARIO_CONTEXT"
    COMMAND_OUTPUT = "COMMAND_OUTPUT"
    GOVERNANCE_CHECKS = "GOVERNANCE_CHECKS"
    BLOCKED_ACTIONS = "BLOCKED_ACTIONS"
    HUMAN_REVIEW_CONTROLS = "HUMAN_REVIEW_CONTROLS"


class OperatorDecisionControlState(str, Enum):
    DISABLED_READ_ONLY_DEMO = "DISABLED_READ_ONLY_DEMO"
    EXTERNAL_HUMAN_PROCESS_REQUIRED = "EXTERNAL_HUMAN_PROCESS_REQUIRED"


@dataclass(frozen=True)
class OperatorReviewSectionCard:
    card_id: str
    section: OperatorReviewScreenSection
    title: str
    body: str
    status: str
    severity: str
    evidence_refs: tuple[str, ...]
    review_required: bool
    provenance: str


@dataclass(frozen=True)
class OperatorDecisionControl:
    control_id: str
    label: str
    intended_decision: str
    state: OperatorDecisionControlState
    disabled: bool
    reason_disabled: str
    external_process_required: bool
    can_execute_action: bool
    provenance: str


@dataclass(frozen=True)
class OperatorReviewScreenModel:
    screen_id: str
    source_command_result_id: str
    mode: OperatorReviewScreenMode
    title: str
    banner: str
    command_summary: dict[str, object]
    section_cards: tuple[OperatorReviewSectionCard, ...]
    decision_controls: tuple[OperatorDecisionControl, ...]
    governance_checks: dict[str, bool]
    blocked_actions: tuple[str, ...]
    rendered_command_output: str | dict[str, Any]
    command_view: dict[str, Any]
    real_shell_command_executed: bool
    real_tool_execution_performed: bool
    provider_call_performed: bool
    dashboard_changes_applied: bool
    benchmark_scoring_allowed_from_screen: bool
    autonomous_remediation_allowed: bool
    human_review_required: bool
    provenance: str


def build_operator_review_screen_model(
    command_result: ScenarioCommandResult | None = None,
) -> OperatorReviewScreenModel:
    if command_result is None:
        command_result = run_sprint5_scenario_command()

    command_summary = summarize_scenario_command_result(command_result)

    cards = (
        OperatorReviewSectionCard(
            card_id="review-screen-card-scenario-context-001",
            section=OperatorReviewScreenSection.SCENARIO_CONTEXT,
            title="Application-health scenario is loaded",
            body=(
                "The operator screen is connected to the read-only Sprint 5 "
                "application-health scenario command."
            ),
            status=str(command_summary["state"]),
            severity="INFO",
            evidence_refs=(command_result.source_demo_run_id,),
            review_required=True,
            provenance="operator_review_screen:scenario_context",
        ),
        OperatorReviewSectionCard(
            card_id="review-screen-card-command-output-001",
            section=OperatorReviewScreenSection.COMMAND_OUTPUT,
            title="Command output is rendered for review",
            body=(
                "The command output is visible to the operator, but the screen "
                "does not execute the command path."
            ),
            status=str(command_summary["output_format"]),
            severity="INFO",
            evidence_refs=(command_result.result_id,),
            review_required=True,
            provenance="operator_review_screen:command_output",
        ),
        OperatorReviewSectionCard(
            card_id="review-screen-card-governance-checks-001",
            section=OperatorReviewScreenSection.GOVERNANCE_CHECKS,
            title="Governance checks passed",
            body=(
                "All governance checks are true and confirm read-only behavior, "
                "no external action, and human review required."
            ),
            status="ALL_GOVERNANCE_CHECKS_PASSED",
            severity="CONTROL",
            evidence_refs=tuple(command_result.governance_checks.keys()),
            review_required=True,
            provenance="operator_review_screen:governance_checks",
        ),
        OperatorReviewSectionCard(
            card_id="review-screen-card-blocked-actions-001",
            section=OperatorReviewScreenSection.BLOCKED_ACTIONS,
            title="Unsafe actions remain blocked",
            body=(
                "Remediation, real tool execution, benchmark scoring, autonomous "
                "policy changes, and automatic dashboard changes remain blocked."
            ),
            status="BLOCKED_ACTIONS_VISIBLE",
            severity="CONTROL",
            evidence_refs=command_result.blocked_actions,
            review_required=True,
            provenance="operator_review_screen:blocked_actions",
        ),
        OperatorReviewSectionCard(
            card_id="review-screen-card-human-controls-001",
            section=OperatorReviewScreenSection.HUMAN_REVIEW_CONTROLS,
            title="Decision controls are disabled in the read-only demo",
            body=(
                "Human decisions are displayed as intended controls only. Any real "
                "approval must occur through an external governed process."
            ),
            status="CONTROLS_DISABLED",
            severity="CONTROL",
            evidence_refs=("human_review_required",),
            review_required=True,
            provenance="operator_review_screen:human_controls",
        ),
    )

    controls = (
        OperatorDecisionControl(
            control_id="review-control-approve-manual-execution-001",
            label="Approve for manual execution",
            intended_decision="APPROVE_PACKAGE_FOR_MANUAL_EXECUTION",
            state=OperatorDecisionControlState.EXTERNAL_HUMAN_PROCESS_REQUIRED,
            disabled=True,
            reason_disabled=(
                "Read-only demo cannot record approval or execute remediation."
            ),
            external_process_required=True,
            can_execute_action=False,
            provenance="operator_review_screen:decision_control",
        ),
        OperatorDecisionControl(
            control_id="review-control-request-more-evidence-001",
            label="Request more evidence",
            intended_decision="REQUEST_MORE_EVIDENCE",
            state=OperatorDecisionControlState.DISABLED_READ_ONLY_DEMO,
            disabled=True,
            reason_disabled=(
                "Read-only demo displays the decision option but does not write records."
            ),
            external_process_required=True,
            can_execute_action=False,
            provenance="operator_review_screen:decision_control",
        ),
        OperatorDecisionControl(
            control_id="review-control-reject-package-001",
            label="Reject package",
            intended_decision="REJECT_PACKAGE",
            state=OperatorDecisionControlState.DISABLED_READ_ONLY_DEMO,
            disabled=True,
            reason_disabled=(
                "Read-only demo displays the decision option but does not write records."
            ),
            external_process_required=True,
            can_execute_action=False,
            provenance="operator_review_screen:decision_control",
        ),
        OperatorDecisionControl(
            control_id="review-control-defer-service-owner-001",
            label="Defer to service owner",
            intended_decision="DEFER_TO_SERVICE_OWNER",
            state=OperatorDecisionControlState.DISABLED_READ_ONLY_DEMO,
            disabled=True,
            reason_disabled=(
                "Read-only demo displays the decision option but does not route work."
            ),
            external_process_required=True,
            can_execute_action=False,
            provenance="operator_review_screen:decision_control",
        ),
    )

    return OperatorReviewScreenModel(
        screen_id="sprint5-operator-review-screen-001",
        source_command_result_id=command_result.result_id,
        mode=OperatorReviewScreenMode.READ_ONLY_REVIEW,
        title="EAIOS Operator Review Screen",
        banner=(
            "READ ONLY SCREEN: decision controls are disabled; no shell command, "
            "tool call, provider call, remediation, benchmark scoring, or dashboard "
            "change is performed."
        ),
        command_summary=command_summary,
        section_cards=cards,
        decision_controls=controls,
        governance_checks=command_result.governance_checks,
        blocked_actions=command_result.blocked_actions,
        rendered_command_output=command_result.rendered_output,
        command_view=scenario_command_to_view_model(command_result),
        real_shell_command_executed=False,
        real_tool_execution_performed=False,
        provider_call_performed=False,
        dashboard_changes_applied=False,
        benchmark_scoring_allowed_from_screen=False,
        autonomous_remediation_allowed=False,
        human_review_required=True,
        provenance="operator_review_screen:screen_model",
    )


def summarize_operator_review_screen(
    screen: OperatorReviewScreenModel,
) -> dict[str, object]:
    return {
        "screen_id": screen.screen_id,
        "source_command_result_id": screen.source_command_result_id,
        "mode": screen.mode.value,
        "section_card_count": len(screen.section_cards),
        "decision_control_count": len(screen.decision_controls),
        "disabled_control_count": len(
            [control for control in screen.decision_controls if control.disabled]
        ),
        "blocked_action_count": len(screen.blocked_actions),
        "governance_check_count": len(screen.governance_checks),
        "all_governance_checks_passed": all(screen.governance_checks.values()),
        "real_shell_command_executed": screen.real_shell_command_executed,
        "real_tool_execution_performed": screen.real_tool_execution_performed,
        "provider_call_performed": screen.provider_call_performed,
        "dashboard_changes_applied": screen.dashboard_changes_applied,
        "benchmark_scoring_allowed_from_screen": (
            screen.benchmark_scoring_allowed_from_screen
        ),
        "autonomous_remediation_allowed": screen.autonomous_remediation_allowed,
        "human_review_required": screen.human_review_required,
    }


def to_view_model(screen: OperatorReviewScreenModel) -> dict[str, Any]:
    return {
        "summary": summarize_operator_review_screen(screen),
        "title": screen.title,
        "banner": screen.banner,
        "command_summary": screen.command_summary,
        "section_cards": [
            {
                "card_id": card.card_id,
                "section": card.section.value,
                "title": card.title,
                "body": card.body,
                "status": card.status,
                "severity": card.severity,
                "evidence_refs": list(card.evidence_refs),
                "review_required": card.review_required,
                "provenance": card.provenance,
            }
            for card in screen.section_cards
        ],
        "decision_controls": [
            {
                "control_id": control.control_id,
                "label": control.label,
                "intended_decision": control.intended_decision,
                "state": control.state.value,
                "disabled": control.disabled,
                "reason_disabled": control.reason_disabled,
                "external_process_required": control.external_process_required,
                "can_execute_action": control.can_execute_action,
                "provenance": control.provenance,
            }
            for control in screen.decision_controls
        ],
        "governance_checks": screen.governance_checks,
        "blocked_actions": list(screen.blocked_actions),
        "rendered_command_output": screen.rendered_command_output,
        "command_view": screen.command_view,
        "real_shell_command_executed": screen.real_shell_command_executed,
        "real_tool_execution_performed": screen.real_tool_execution_performed,
        "provider_call_performed": screen.provider_call_performed,
        "dashboard_changes_applied": screen.dashboard_changes_applied,
        "benchmark_scoring_allowed_from_screen": (
            screen.benchmark_scoring_allowed_from_screen
        ),
        "autonomous_remediation_allowed": screen.autonomous_remediation_allowed,
        "human_review_required": screen.human_review_required,
        "provenance": screen.provenance,
    }
