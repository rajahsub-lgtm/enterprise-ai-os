"""Sprint 8 static demo export.

Read-only static export model for interview demo review.

It renders markdown and HTML strings from the canonical operator demo command.
It does not write files, start a server, publish a site, build containers,
deploy cloud resources, call providers, call connectors, persist approvals,
send notifications, execute remediation, score benchmarks, update benchmark
truth, or enable autonomous remediation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from html import escape
from typing import Any

from eaios.sprint8.operator_demo_command import (
    OperatorDemoCommandName,
    OperatorDemoCommandRequest,
    OperatorDemoRenderFormat,
    run_operator_demo_command,
    summarize_operator_demo_command_result,
)


class StaticDemoExportMode(str, Enum):
    REVIEW_ONLY_STATIC_EXPORT = "REVIEW_ONLY_STATIC_EXPORT"


class StaticDemoExportFormat(str, Enum):
    MARKDOWN = "MARKDOWN"
    HTML = "HTML"
    JSON_VIEW_MODEL = "JSON_VIEW_MODEL"


class StaticDemoExportStatus(str, Enum):
    RENDERED_IN_MEMORY = "RENDERED_IN_MEMORY"
    BLOCKED_NON_READ_ONLY = "BLOCKED_NON_READ_ONLY"


@dataclass(frozen=True)
class StaticDemoExportSection:
    section_id: str
    title: str
    markdown: str
    html: str
    provenance: str


@dataclass(frozen=True)
class StaticDemoExport:
    export_id: str
    mode: StaticDemoExportMode
    status: StaticDemoExportStatus
    title: str
    source_operator_command_id: str
    sections: tuple[StaticDemoExportSection, ...]
    markdown_document: str
    html_document: str
    blocked_actions: tuple[str, ...]
    operator_command_summary: dict[str, object]
    export_rendered: bool
    files_written: bool
    server_started: bool
    static_site_published: bool
    archive_created: bool
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


def build_static_demo_export() -> StaticDemoExport:
    command_result = run_operator_demo_command(
        OperatorDemoCommandRequest(
            command_name=OperatorDemoCommandName.SHOW_RELEASE_CHECKLIST.value,
            read_only=True,
            render_format=OperatorDemoRenderFormat.JSON_VIEW_MODEL,
        )
    )
    command_summary = summarize_operator_demo_command_result(command_result)

    sections = (
        StaticDemoExportSection(
            section_id="static-export-section-001-overview",
            title="Interview Demo Overview",
            markdown=(
                "EAIOS is presented as a governed enterprise AI operating-system demo "
                "using synthetic ITIL/AIOps data with real-enterprise integration seams."
            ),
            html=(
                "<p>EAIOS is presented as a governed enterprise AI operating-system demo "
                "using synthetic ITIL/AIOps data with real-enterprise integration seams.</p>"
            ),
            provenance="static_demo_export:section",
        ),
        StaticDemoExportSection(
            section_id="static-export-section-002-command",
            title="Canonical Operator Command",
            markdown="\n".join(command_result.output_lines),
            html="".join(f"<p>{escape(line)}</p>" for line in command_result.output_lines),
            provenance="static_demo_export:section",
        ),
        StaticDemoExportSection(
            section_id="static-export-section-003-safety",
            title="Safety Boundaries",
            markdown=(
                "The export is review-only. Providers, MCP connectors, cloud deployment, "
                "release creation, notifications, remediation, benchmark scoring, and "
                "benchmark truth updates remain blocked."
            ),
            html=(
                "<p>The export is review-only. Providers, MCP connectors, cloud deployment, "
                "release creation, notifications, remediation, benchmark scoring, and "
                "benchmark truth updates remain blocked.</p>"
            ),
            provenance="static_demo_export:section",
        ),
    )

    markdown_document = _render_markdown_document(sections)
    html_document = _render_html_document(sections)

    return StaticDemoExport(
        export_id="sprint8-static-demo-export-001",
        mode=StaticDemoExportMode.REVIEW_ONLY_STATIC_EXPORT,
        status=StaticDemoExportStatus.RENDERED_IN_MEMORY,
        title="EAIOS Sprint 8 Static Demo Export",
        source_operator_command_id=str(command_summary["command_id"]),
        sections=sections,
        markdown_document=markdown_document,
        html_document=html_document,
        blocked_actions=(
            "write_static_export_file",
            "start_local_server",
            "publish_static_site",
            "create_release_archive",
            "build_container_image",
            "push_container_image",
            "deploy_to_cloud",
            "enable_real_provider",
            "enable_real_connector",
            "persist_approval_record_to_external_store",
            "send_notification",
            "execute_remediation",
            "score_benchmark_from_static_export",
            "update_benchmark_truth_from_static_export",
            "enable_autonomous_remediation",
            "bypass_human_review",
        ),
        operator_command_summary=command_summary,
        export_rendered=True,
        files_written=False,
        server_started=False,
        static_site_published=False,
        archive_created=False,
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
        provenance="static_demo_export:model",
    )


def summarize_static_demo_export(export: StaticDemoExport) -> dict[str, object]:
    return {
        "export_id": export.export_id,
        "mode": export.mode.value,
        "status": export.status.value,
        "title": export.title,
        "source_operator_command_id": export.source_operator_command_id,
        "section_count": len(export.sections),
        "markdown_length": len(export.markdown_document),
        "html_length": len(export.html_document),
        "blocked_action_count": len(export.blocked_actions),
        "export_rendered": export.export_rendered,
        "files_written": export.files_written,
        "server_started": export.server_started,
        "static_site_published": export.static_site_published,
        "archive_created": export.archive_created,
        "container_built": export.container_built,
        "cloud_deployed": export.cloud_deployed,
        "provider_enabled": export.provider_enabled,
        "connector_enabled": export.connector_enabled,
        "approval_records_persisted": export.approval_records_persisted,
        "remediation_performed": export.remediation_performed,
        "notifications_sent": export.notifications_sent,
        "benchmark_scoring_performed": export.benchmark_scoring_performed,
        "benchmark_truth_updated": export.benchmark_truth_updated,
        "autonomous_remediation_allowed": export.autonomous_remediation_allowed,
        "human_review_required": export.human_review_required,
    }


def to_view_model(export: StaticDemoExport) -> dict[str, Any]:
    return {
        "summary": summarize_static_demo_export(export),
        "sections": [
            {
                "section_id": section.section_id,
                "title": section.title,
                "markdown": section.markdown,
                "html": section.html,
                "provenance": section.provenance,
            }
            for section in export.sections
        ],
        "markdown_document": export.markdown_document,
        "html_document": export.html_document,
        "blocked_actions": list(export.blocked_actions),
        "operator_command_summary": export.operator_command_summary,
        "provenance": export.provenance,
    }


def _render_markdown_document(sections: tuple[StaticDemoExportSection, ...]) -> str:
    body = ["# EAIOS Sprint 8 Interview Demo Export", ""]
    for section in sections:
        body.extend([f"## {section.title}", "", section.markdown, ""])
    return "\n".join(body).strip() + "\n"


def _render_html_document(sections: tuple[StaticDemoExportSection, ...]) -> str:
    section_html = "\n".join(
        f"<section><h2>{escape(section.title)}</h2>{section.html}</section>"
        for section in sections
    )
    return (
        "<!doctype html>\n"
        "<html><head><meta charset=\"utf-8\">"
        "<title>EAIOS Sprint 8 Interview Demo Export</title>"
        "</head><body>"
        "<h1>EAIOS Sprint 8 Interview Demo Export</h1>"
        f"{section_html}"
        "</body></html>"
    )
