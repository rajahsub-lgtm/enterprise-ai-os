"""Sprint 6 static HTML review page model.

This module renders a static portfolio review page as an in-memory string.
No HTML file is written and no external system is called.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from html import escape
from typing import Any

from eaios.sprint6.artifact_export_plan import (
    build_artifact_export_plan,
    summarize_artifact_export_plan,
)


class StaticReviewPageMode(str, Enum):
    RENDER_ONLY = "RENDER_ONLY"


@dataclass(frozen=True)
class StaticReviewPageSection:
    section_id: str
    title: str
    body: str
    evidence_refs: tuple[str, ...]
    provenance: str


@dataclass(frozen=True)
class StaticReviewPageModel:
    page_id: str
    mode: StaticReviewPageMode
    title: str
    source_export_plan_id: str
    sections: tuple[StaticReviewPageSection, ...]
    blocked_actions: tuple[str, ...]
    export_plan_summary: dict[str, object]
    rendered_html: str
    html_file_written: bool
    export_folder_created: bool
    files_copied: bool
    archive_created: bool
    shell_commands_executed: bool
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


def build_static_review_page_model() -> StaticReviewPageModel:
    export_plan = build_artifact_export_plan()
    export_summary = summarize_artifact_export_plan(export_plan)

    sections = (
        StaticReviewPageSection(
            section_id="review-section-demo-story-001",
            title="Demo Story",
            body=(
                "EAIOS presents benchmark-grounded governed AIOps as a "
                "read-only operator experience."
            ),
            evidence_refs=("docs/EAIOS_2_SPRINT_5_DEMO_NARRATIVE.md",),
            provenance="static_review_page:section",
        ),
        StaticReviewPageSection(
            section_id="review-section-operator-experience-001",
            title="Operator Experience",
            body=(
                "The operator can review scenario context, dashboard export, "
                "CLI output, disabled controls, and blocked actions."
            ),
            evidence_refs=("src/eaios/sprint5/operator_review_screen.py",),
            provenance="static_review_page:section",
        ),
        StaticReviewPageSection(
            section_id="review-section-cloud-readiness-001",
            title="Cloud Readiness",
            body=(
                "GCP readiness is review-only: REVIEW_READY_NOT_DEPLOYED and "
                "GCP_READINESS_REVIEW_ONLY."
            ),
            evidence_refs=("src/eaios/sprint5/gcp_readiness_checklist.py",),
            provenance="static_review_page:section",
        ),
        StaticReviewPageSection(
            section_id="review-section-package-plan-001",
            title="Package Plan",
            body=(
                "Sprint 6 defines a local manifest, CLI contract, and dry-run "
                "artifact export plan without writing files."
            ),
            evidence_refs=("src/eaios/sprint6/artifact_export_plan.py",),
            provenance="static_review_page:section",
        ),
        StaticReviewPageSection(
            section_id="review-section-governance-boundaries-001",
            title="Governance Boundaries",
            body=(
                "Real execution, providers, connectors, secrets, cloud creation, "
                "remediation, notifications, and benchmark scoring remain blocked."
            ),
            evidence_refs=("tests/test_sprint6_artifact_export_plan.py",),
            provenance="static_review_page:section",
        ),
    )

    blocked_actions = (
        "write_static_html_file",
        "create_export_folder",
        "copy_artifact_files",
        "create_archive",
        "run_shell_command",
        "create_cloud_resources",
        "load_secret_material",
        "call_real_provider",
        "call_real_connector",
        "execute_remediation",
        "send_notification",
        "score_benchmark_from_review_page",
        "enable_autonomous_remediation",
    )

    return StaticReviewPageModel(
        page_id="sprint6-static-review-page-001",
        mode=StaticReviewPageMode.RENDER_ONLY,
        title="EAIOS Portfolio Review Page",
        source_export_plan_id=str(export_summary["export_plan_id"]),
        sections=sections,
        blocked_actions=blocked_actions,
        export_plan_summary=export_summary,
        rendered_html=_render_html(
            title="EAIOS Portfolio Review Page",
            sections=sections,
            blocked_actions=blocked_actions,
            export_summary=export_summary,
        ),
        html_file_written=False,
        export_folder_created=False,
        files_copied=False,
        archive_created=False,
        shell_commands_executed=False,
        cloud_resources_created=False,
        secrets_loaded=False,
        provider_calls_performed=False,
        real_connectors_called=False,
        remediation_performed=False,
        notifications_sent=False,
        benchmark_scoring_performed=False,
        autonomous_remediation_allowed=False,
        human_review_required=True,
        provenance="static_review_page:model",
    )


def summarize_static_review_page_model(page: StaticReviewPageModel) -> dict[str, object]:
    return {
        "page_id": page.page_id,
        "mode": page.mode.value,
        "title": page.title,
        "source_export_plan_id": page.source_export_plan_id,
        "section_count": len(page.sections),
        "blocked_action_count": len(page.blocked_actions),
        "html_file_written": page.html_file_written,
        "export_folder_created": page.export_folder_created,
        "files_copied": page.files_copied,
        "archive_created": page.archive_created,
        "shell_commands_executed": page.shell_commands_executed,
        "cloud_resources_created": page.cloud_resources_created,
        "secrets_loaded": page.secrets_loaded,
        "provider_calls_performed": page.provider_calls_performed,
        "real_connectors_called": page.real_connectors_called,
        "remediation_performed": page.remediation_performed,
        "notifications_sent": page.notifications_sent,
        "benchmark_scoring_performed": page.benchmark_scoring_performed,
        "autonomous_remediation_allowed": page.autonomous_remediation_allowed,
        "human_review_required": page.human_review_required,
    }


def to_view_model(page: StaticReviewPageModel) -> dict[str, Any]:
    return {
        "summary": summarize_static_review_page_model(page),
        "sections": [
            {
                "section_id": section.section_id,
                "title": section.title,
                "body": section.body,
                "evidence_refs": list(section.evidence_refs),
                "provenance": section.provenance,
            }
            for section in page.sections
        ],
        "blocked_actions": list(page.blocked_actions),
        "export_plan_summary": page.export_plan_summary,
        "rendered_html": page.rendered_html,
        "provenance": page.provenance,
    }


def _render_html(
    title: str,
    sections: tuple[StaticReviewPageSection, ...],
    blocked_actions: tuple[str, ...],
    export_summary: dict[str, object],
) -> str:
    section_html = "\n".join(
        "<section>"
        f"<h2>{escape(section.title)}</h2>"
        f"<p>{escape(section.body)}</p>"
        f"<p><strong>Evidence:</strong> {escape(', '.join(section.evidence_refs))}</p>"
        "</section>"
        for section in sections
    )

    blocked_html = "\n".join(
        f"<li>{escape(action)}</li>" for action in blocked_actions
    )

    return (
        "<!doctype html>\n"
        "<html lang=\"en\">\n"
        "<head><meta charset=\"utf-8\">"
        f"<title>{escape(title)}</title></head>\n"
        "<body>\n"
        f"<h1>{escape(title)}</h1>\n"
        "<p>Mode: RENDER_ONLY</p>\n"
        f"<p>Source export plan: {escape(str(export_summary['export_plan_id']))}</p>\n"
        f"{section_html}\n"
        "<section><h2>Blocked Actions</h2><ul>\n"
        f"{blocked_html}\n"
        "</ul></section>\n"
        "<p>Human review required: true</p>\n"
        "</body>\n</html>\n"
    )
