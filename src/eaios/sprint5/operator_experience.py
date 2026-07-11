"""Sprint 5 read-only operator experience export.

This module converts the Sprint 4 governed learning dashboard into an
operator-facing export bundle.

It does not execute tools, call providers, apply dashboard changes, update
benchmark truth, score benchmarks, or enable autonomous remediation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint4.governed_learning_dashboard import (
    build_governed_learning_dashboard_snapshot,
    summarize_learning_dashboard_snapshot,
    to_view_model as learning_dashboard_to_view_model,
)


class OperatorExperienceMode(str, Enum):
    READ_ONLY_DEMO = "READ_ONLY_DEMO"
    EXPORT_READY = "EXPORT_READY"


class OperatorReviewSection(str, Enum):
    INCIDENT_CONTEXT = "INCIDENT_CONTEXT"
    RESTORATION_STATUS = "RESTORATION_STATUS"
    APPROVAL_DECISION = "APPROVAL_DECISION"
    LEARNING_FEEDBACK = "LEARNING_FEEDBACK"
    IMPROVEMENT_QUEUE = "IMPROVEMENT_QUEUE"


@dataclass(frozen=True)
class OperatorDashboardCard:
    card_id: str
    section: OperatorReviewSection
    title: str
    status: str
    summary: str
    evidence_refs: tuple[str, ...]
    operator_actions: tuple[str, ...]
    blocked: bool
    review_required: bool
    provenance: str


@dataclass(frozen=True)
class OperatorDashboardExport:
    export_id: str
    source_dashboard_snapshot_id: str
    mode: OperatorExperienceMode
    title: str
    safety_banner: str
    summary: dict[str, object]
    cards: tuple[OperatorDashboardCard, ...]
    blocked_actions: tuple[str, ...]
    review_queue: tuple[str, ...]
    export_formats: tuple[str, ...]
    dashboard_view: dict[str, Any]
    real_tool_execution_performed: bool
    autonomous_remediation_allowed: bool
    dashboard_changes_applied: bool
    benchmark_scoring_allowed_from_export: bool
    human_review_required: bool
    provenance: str


def build_operator_dashboard_export() -> OperatorDashboardExport:
    dashboard = build_governed_learning_dashboard_snapshot()
    dashboard_summary = summarize_learning_dashboard_snapshot(dashboard)

    cards = (
        OperatorDashboardCard(
            card_id="operator-card-incident-context-001",
            section=OperatorReviewSection.INCIDENT_CONTEXT,
            title="Application health scenario is ready for operator review",
            status="BENCHMARK_GROUNDED_CONTEXT_AVAILABLE",
            summary=(
                "The dashboard is grounded in the Sprint 4 benchmark-backed "
                "application-health scenario and preserves external benchmark truth."
            ),
            evidence_refs=(
                dashboard.source_restoration_snapshot_id,
                dashboard.source_learning_snapshot_id,
            ),
            operator_actions=(
                "Review benchmark-grounded context.",
                "Confirm this export is read-only.",
            ),
            blocked=False,
            review_required=True,
            provenance="operator_experience:incident_context_card",
        ),
        OperatorDashboardCard(
            card_id="operator-card-restoration-status-001",
            section=OperatorReviewSection.RESTORATION_STATUS,
            title="Restoration remains blocked from autonomous execution",
            status=str(dashboard.restoration_summary["safe_restoration_state"]),
            summary=(
                "Restoration candidates exist, but the safe state requires more "
                "evidence and does not permit autonomous remediation."
            ),
            evidence_refs=(
                dashboard.source_restoration_snapshot_id,
            ),
            operator_actions=(
                "Review restoration action cards.",
                "Confirm blocked actions are still blocked.",
            ),
            blocked=True,
            review_required=True,
            provenance="operator_experience:restoration_status_card",
        ),
        OperatorDashboardCard(
            card_id="operator-card-approval-decision-001",
            section=OperatorReviewSection.APPROVAL_DECISION,
            title="Operator decision is captured as request for more evidence",
            status="MORE_EVIDENCE_REQUESTED",
            summary=(
                "The default operator decision record is accepted, but it requests "
                "more evidence rather than approving execution."
            ),
            evidence_refs=(
                "operator-decision-validation-001",
            ),
            operator_actions=(
                "Review decision rationale.",
                "Collect missing or conflicting evidence before manual action.",
            ),
            blocked=True,
            review_required=True,
            provenance="operator_experience:approval_decision_card",
        ),
        OperatorDashboardCard(
            card_id="operator-card-learning-feedback-001",
            section=OperatorReviewSection.LEARNING_FEEDBACK,
            title="Learning captured feedback without changing truth or policy",
            status="GOVERNED_LEARNING_REVIEW_REQUIRED",
            summary=(
                "Operator feedback and decision outcome history are captured as "
                "governed learning inputs, not as benchmark truth updates."
            ),
            evidence_refs=(
                dashboard.source_learning_snapshot_id,
                "decision-outcome-history-001",
            ),
            operator_actions=(
                "Review captured feedback.",
                "Approve or reject learning interpretation outside this export.",
            ),
            blocked=False,
            review_required=True,
            provenance="operator_experience:learning_feedback_card",
        ),
        OperatorDashboardCard(
            card_id="operator-card-improvement-queue-001",
            section=OperatorReviewSection.IMPROVEMENT_QUEUE,
            title="Dashboard improvements are review-only candidates",
            status="REVIEW_ONLY_QUEUE",
            summary=(
                "Dashboard deltas are visible for review but are not applied "
                "automatically."
            ),
            evidence_refs=dashboard.review_queue,
            operator_actions=(
                "Review improvement candidates.",
                "Keep benchmark scoring and autonomous policy unchanged.",
            ),
            blocked=True,
            review_required=True,
            provenance="operator_experience:improvement_queue_card",
        ),
    )

    return OperatorDashboardExport(
        export_id="sprint5-operator-dashboard-export-001",
        source_dashboard_snapshot_id=dashboard.snapshot_id,
        mode=OperatorExperienceMode.READ_ONLY_DEMO,
        title="EAIOS Operator Dashboard Export",
        safety_banner=(
            "READ ONLY: no remediation, no real tools, no provider calls, no "
            "benchmark scoring, no dashboard changes applied."
        ),
        summary=dashboard_summary,
        cards=cards,
        blocked_actions=_blocked_actions_for_export(dashboard.blocked_updates),
        review_queue=dashboard.review_queue,
        export_formats=(
            "json_view_model",
            "markdown_summary",
            "cli_text",
        ),
        dashboard_view=learning_dashboard_to_view_model(dashboard),
        real_tool_execution_performed=False,
        autonomous_remediation_allowed=False,
        dashboard_changes_applied=False,
        benchmark_scoring_allowed_from_export=False,
        human_review_required=True,
        provenance="operator_experience:dashboard_export",
    )


def summarize_operator_dashboard_export(
    export: OperatorDashboardExport,
) -> dict[str, object]:
    return {
        "export_id": export.export_id,
        "source_dashboard_snapshot_id": export.source_dashboard_snapshot_id,
        "mode": export.mode.value,
        "card_count": len(export.cards),
        "blocked_card_count": len([card for card in export.cards if card.blocked]),
        "review_required_card_count": len(
            [card for card in export.cards if card.review_required]
        ),
        "blocked_action_count": len(export.blocked_actions),
        "review_queue_count": len(export.review_queue),
        "export_format_count": len(export.export_formats),
        "real_tool_execution_performed": export.real_tool_execution_performed,
        "autonomous_remediation_allowed": export.autonomous_remediation_allowed,
        "dashboard_changes_applied": export.dashboard_changes_applied,
        "benchmark_scoring_allowed_from_export": (
            export.benchmark_scoring_allowed_from_export
        ),
        "human_review_required": export.human_review_required,
    }


def render_operator_dashboard_markdown(export: OperatorDashboardExport) -> str:
    lines = [
        f"# {export.title}",
        "",
        f"Export ID: {export.export_id}",
        f"Mode: {export.mode.value}",
        "",
        f"Safety: {export.safety_banner}",
        "",
        "## Operator Cards",
    ]

    for card in export.cards:
        lines.extend(
            [
                "",
                f"### {card.title}",
                f"- Section: {card.section.value}",
                f"- Status: {card.status}",
                f"- Review required: {str(card.review_required).lower()}",
                f"- Blocked: {str(card.blocked).lower()}",
                f"- Summary: {card.summary}",
            ]
        )

    lines.extend(
        [
            "",
            "## Blocked Actions",
            *[f"- {action}" for action in export.blocked_actions],
            "",
            "## Review Queue",
            *[f"- {item}" for item in export.review_queue],
        ]
    )

    return "\n".join(lines)


def to_view_model(export: OperatorDashboardExport) -> dict[str, Any]:
    return {
        "summary": summarize_operator_dashboard_export(export),
        "title": export.title,
        "safety_banner": export.safety_banner,
        "cards": [
            {
                "card_id": card.card_id,
                "section": card.section.value,
                "title": card.title,
                "status": card.status,
                "summary": card.summary,
                "evidence_refs": list(card.evidence_refs),
                "operator_actions": list(card.operator_actions),
                "blocked": card.blocked,
                "review_required": card.review_required,
                "provenance": card.provenance,
            }
            for card in export.cards
        ],
        "blocked_actions": list(export.blocked_actions),
        "review_queue": list(export.review_queue),
        "export_formats": list(export.export_formats),
        "dashboard": export.dashboard_view,
        "markdown_summary": render_operator_dashboard_markdown(export),
        "real_tool_execution_performed": export.real_tool_execution_performed,
        "autonomous_remediation_allowed": export.autonomous_remediation_allowed,
        "dashboard_changes_applied": export.dashboard_changes_applied,
        "benchmark_scoring_allowed_from_export": (
            export.benchmark_scoring_allowed_from_export
        ),
        "human_review_required": export.human_review_required,
        "provenance": export.provenance,
    }


def _blocked_actions_for_export(blocked_updates: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(
        dict.fromkeys(
            (
                *blocked_updates,
                "execute_remediation",
                "restart_service",
                "scale_service",
                "modify_database",
                "deploy_code",
                "rollback_change",
                "send_notification",
                "page_on_call",
                "publish_status",
                "score_benchmark_from_operator_export",
                "apply_dashboard_changes_automatically",
            )
        )
    )
