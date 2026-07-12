"""Sprint 7 local web review surface model.

This module defines an in-memory review surface for a future local browser demo.
It does not start a server, open a browser, write files, create cloud resources,
load secrets, call providers, call connectors, execute remediation, send
notifications, score benchmarks, or enable autonomous remediation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from html import escape
from typing import Any

from eaios.sprint7.container_packaging_contract import (
    build_container_packaging_contract,
    summarize_container_packaging_contract,
)


class LocalWebReviewMode(str, Enum):
    SURFACE_MODEL_ONLY = "SURFACE_MODEL_ONLY"


class LocalWebPageKind(str, Enum):
    OVERVIEW = "OVERVIEW"
    GOVERNANCE = "GOVERNANCE"
    PACKAGE = "PACKAGE"
    CLOUD = "CLOUD"
    PROVIDER = "PROVIDER"
    CONNECTOR = "CONNECTOR"


@dataclass(frozen=True)
class LocalWebReviewPage:
    page_id: str
    page_kind: LocalWebPageKind
    route: str
    title: str
    summary: str
    evidence_refs: tuple[str, ...]
    disabled_controls: tuple[str, ...]
    provenance: str


@dataclass(frozen=True)
class LocalWebReviewSurface:
    surface_id: str
    mode: LocalWebReviewMode
    title: str
    source_container_contract_id: str
    pages: tuple[LocalWebReviewPage, ...]
    navigation_labels: tuple[str, ...]
    blocked_actions: tuple[str, ...]
    container_contract_summary: dict[str, object]
    rendered_html: str
    server_started: bool
    browser_opened: bool
    files_written: bool
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


def build_local_web_review_surface() -> LocalWebReviewSurface:
    container_contract = build_container_packaging_contract()
    container_summary = summarize_container_packaging_contract(container_contract)

    pages = (
        LocalWebReviewPage(
            page_id="local-web-page-overview-001",
            page_kind=LocalWebPageKind.OVERVIEW,
            route="/review/overview",
            title="Overview",
            summary="EAIOS portfolio review surface for read-only enterprise AI governance.",
            evidence_refs=("docs/EAIOS_2_SPRINT_6_CLOSEOUT.md",),
            disabled_controls=("start_server", "open_browser", "write_html_file"),
            provenance="local_web_review_surface:page",
        ),
        LocalWebReviewPage(
            page_id="local-web-page-governance-001",
            page_kind=LocalWebPageKind.GOVERNANCE,
            route="/review/governance",
            title="Governance Boundaries",
            summary="Shows human review, benchmark isolation, and blocked unsafe actions.",
            evidence_refs=("docs/EAIOS_2_SPRINT_6_CLOSEOUT.md",),
            disabled_controls=("execute_remediation", "send_notification", "score_benchmark"),
            provenance="local_web_review_surface:page",
        ),
        LocalWebReviewPage(
            page_id="local-web-page-package-001",
            page_kind=LocalWebPageKind.PACKAGE,
            route="/review/package",
            title="Container Package Contract",
            summary="Shows the review-only container packaging contract and image boundaries.",
            evidence_refs=("src/eaios/sprint7/container_packaging_contract.py",),
            disabled_controls=("build_container_image", "run_container", "push_container_image"),
            provenance="local_web_review_surface:page",
        ),
        LocalWebReviewPage(
            page_id="local-web-page-cloud-001",
            page_kind=LocalWebPageKind.CLOUD,
            route="/review/cloud",
            title="Cloud Readiness",
            summary="Shows GCP readiness as review-only and not deployed.",
            evidence_refs=("docs/EAIOS_2_SPRINT_6_GCP_DEPLOYMENT_DESIGN.md",),
            disabled_controls=("create_cloud_resources", "run_cloud_deploy", "load_secret_material"),
            provenance="local_web_review_surface:page",
        ),
        LocalWebReviewPage(
            page_id="local-web-page-provider-001",
            page_kind=LocalWebPageKind.PROVIDER,
            route="/review/provider",
            title="Provider Integration",
            summary="Shows real provider integration as disabled by default.",
            evidence_refs=("docs/EAIOS_2_SPRINT_6_PROVIDER_INTEGRATION_DESIGN.md",),
            disabled_controls=("call_real_provider", "send_prompt_to_provider", "load_secret_material"),
            provenance="local_web_review_surface:page",
        ),
        LocalWebReviewPage(
            page_id="local-web-page-connector-001",
            page_kind=LocalWebPageKind.CONNECTOR,
            route="/review/connector",
            title="MCP Connector Permissions",
            summary="Shows real MCP connector enablement as permission-gated and disabled by default.",
            evidence_refs=("docs/EAIOS_2_SPRINT_6_MCP_CONNECTOR_PERMISSION_MODEL.md",),
            disabled_controls=("call_real_connector", "execute_tool_action", "perform_external_write"),
            provenance="local_web_review_surface:page",
        ),
    )

    blocked_actions = (
        "start_local_server",
        "open_browser",
        "write_static_html_file",
        "build_container_image",
        "run_container",
        "push_container_image",
        "create_cloud_resources",
        "load_secret_material",
        "call_real_provider",
        "call_real_connector",
        "execute_remediation",
        "send_notification",
        "score_benchmark_from_web_output",
        "update_benchmark_truth_from_web_output",
        "enable_autonomous_remediation",
    )

    navigation_labels = tuple(page.title for page in pages)

    return LocalWebReviewSurface(
        surface_id="sprint7-local-web-review-surface-001",
        mode=LocalWebReviewMode.SURFACE_MODEL_ONLY,
        title="EAIOS Local Web Review Surface",
        source_container_contract_id=str(container_summary["contract_id"]),
        pages=pages,
        navigation_labels=navigation_labels,
        blocked_actions=blocked_actions,
        container_contract_summary=container_summary,
        rendered_html=render_local_web_review_surface_html(
            title="EAIOS Local Web Review Surface",
            pages=pages,
            blocked_actions=blocked_actions,
        ),
        server_started=False,
        browser_opened=False,
        files_written=False,
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
        provenance="local_web_review_surface:model",
    )


def summarize_local_web_review_surface(
    surface: LocalWebReviewSurface,
) -> dict[str, object]:
    return {
        "surface_id": surface.surface_id,
        "mode": surface.mode.value,
        "title": surface.title,
        "source_container_contract_id": surface.source_container_contract_id,
        "page_count": len(surface.pages),
        "navigation_count": len(surface.navigation_labels),
        "blocked_action_count": len(surface.blocked_actions),
        "server_started": surface.server_started,
        "browser_opened": surface.browser_opened,
        "files_written": surface.files_written,
        "shell_commands_executed": surface.shell_commands_executed,
        "cloud_resources_created": surface.cloud_resources_created,
        "secrets_loaded": surface.secrets_loaded,
        "provider_calls_performed": surface.provider_calls_performed,
        "real_connectors_called": surface.real_connectors_called,
        "remediation_performed": surface.remediation_performed,
        "notifications_sent": surface.notifications_sent,
        "benchmark_scoring_performed": surface.benchmark_scoring_performed,
        "autonomous_remediation_allowed": surface.autonomous_remediation_allowed,
        "human_review_required": surface.human_review_required,
    }


def to_view_model(surface: LocalWebReviewSurface) -> dict[str, Any]:
    return {
        "summary": summarize_local_web_review_surface(surface),
        "navigation_labels": list(surface.navigation_labels),
        "pages": [
            {
                "page_id": page.page_id,
                "page_kind": page.page_kind.value,
                "route": page.route,
                "title": page.title,
                "summary": page.summary,
                "evidence_refs": list(page.evidence_refs),
                "disabled_controls": list(page.disabled_controls),
                "provenance": page.provenance,
            }
            for page in surface.pages
        ],
        "blocked_actions": list(surface.blocked_actions),
        "container_contract_summary": surface.container_contract_summary,
        "rendered_html": surface.rendered_html,
        "provenance": surface.provenance,
    }


def render_local_web_review_surface_html(
    title: str,
    pages: tuple[LocalWebReviewPage, ...],
    blocked_actions: tuple[str, ...],
) -> str:
    nav_html = "\n".join(
        f"<li>{escape(page.route)} ? {escape(page.title)}</li>" for page in pages
    )
    page_html = "\n".join(
        (
            "<section>"
            f"<h2>{escape(page.title)}</h2>"
            f"<p>{escape(page.summary)}</p>"
            f"<p>Disabled controls: {escape(', '.join(page.disabled_controls))}</p>"
            f"<p>Evidence: {escape(', '.join(page.evidence_refs))}</p>"
            "</section>"
        )
        for page in pages
    )
    blocked_html = "\n".join(f"<li>{escape(action)}</li>" for action in blocked_actions)

    return (
        "<!doctype html>\n"
        "<html lang=\"en\">\n"
        "<head><meta charset=\"utf-8\">"
        f"<title>{escape(title)}</title></head>\n"
        "<body>\n"
        f"<h1>{escape(title)}</h1>\n"
        "<p>Mode: SURFACE_MODEL_ONLY</p>\n"
        "<nav><ul>\n"
        f"{nav_html}\n"
        "</ul></nav>\n"
        f"{page_html}\n"
        "<section><h2>Blocked Actions</h2><ul>\n"
        f"{blocked_html}\n"
        "</ul></section>\n"
        "<p>Human review required: true</p>\n"
        "</body>\n</html>\n"
    )
