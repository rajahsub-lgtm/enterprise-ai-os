"""Sprint 11 local static preview page renderer.

This module renders local static preview pages in memory.

It does not persist files, publish a site, start a server, open a browser, create
cloud resources, call providers, call MCP connectors, load credentials, read
production data, send notifications, execute remediation, mutate benchmark
truth, approve actions, or enable autonomous action.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from html import escape
from typing import Any

from eaios.sprint11.local_static_preview_manifest import (
    LocalStaticPreviewManifest,
    build_generation_context,
    build_local_static_preview_manifest,
    validate_manifest_is_static_review_only,
)


class LocalStaticPreviewRenderStatus(str, Enum):
    RENDERED_IN_MEMORY = "RENDERED_IN_MEMORY"
    BLOCKED_MANIFEST_VIOLATIONS = "BLOCKED_MANIFEST_VIOLATIONS"


class LocalStaticPreviewPageKind(str, Enum):
    LANDING = "LANDING"
    ARCHITECTURE = "ARCHITECTURE"
    DEMO_STORYBOARD = "DEMO_STORYBOARD"
    ENTERPRISE_MAPPING = "ENTERPRISE_MAPPING"
    INTERVIEW_QA = "INTERVIEW_QA"
    MANIFEST = "MANIFEST"


@dataclass(frozen=True)
class LocalStaticPreviewPage:
    page_id: str
    kind: LocalStaticPreviewPageKind
    output_path: str
    title: str
    source_paths: tuple[str, ...]
    html: str
    rendered_in_memory: bool
    persisted: bool


@dataclass(frozen=True)
class LocalStaticPreviewRenderResult:
    render_id: str
    status: LocalStaticPreviewRenderStatus
    manifest_id: str
    decision: str
    page_count: int
    pages: tuple[LocalStaticPreviewPage, ...]
    violations: tuple[str, ...]
    files_persisted: bool
    site_published: bool
    server_started: bool
    browser_opened: bool
    cloud_resources_created: bool
    providers_enabled: bool
    mcp_connectors_enabled: bool
    production_data_used: bool
    credentials_required: bool
    runtime_enabled: bool
    writes_enabled: bool
    notifications_enabled: bool
    remediation_enabled: bool
    benchmark_truth_mutation_enabled: bool
    autonomous_action_enabled: bool
    human_approval_required: bool
    rollback_required: bool
    provenance: str


_PAGE_KIND_BY_OUTPUT = {
    "preview/index.html": LocalStaticPreviewPageKind.LANDING,
    "preview/architecture.html": LocalStaticPreviewPageKind.ARCHITECTURE,
    "preview/demo-storyboard.html": LocalStaticPreviewPageKind.DEMO_STORYBOARD,
    "preview/real-enterprise-mapping.html": LocalStaticPreviewPageKind.ENTERPRISE_MAPPING,
    "preview/interview-qa.html": LocalStaticPreviewPageKind.INTERVIEW_QA,
    "preview/manifest.json": LocalStaticPreviewPageKind.MANIFEST,
}


_TITLE_BY_KIND = {
    LocalStaticPreviewPageKind.LANDING: "EAIOS Local Static Preview",
    LocalStaticPreviewPageKind.ARCHITECTURE: "Architecture Narrative",
    LocalStaticPreviewPageKind.DEMO_STORYBOARD: "Demo Storyboard",
    LocalStaticPreviewPageKind.ENTERPRISE_MAPPING: "Real Enterprise Mapping",
    LocalStaticPreviewPageKind.INTERVIEW_QA: "Interview Q&A",
    LocalStaticPreviewPageKind.MANIFEST: "Disabled-State Manifest",
}


def _safe_li(value: str) -> str:
    return f"<li>{escape(value)}</li>"


def _render_safety_banner(manifest: LocalStaticPreviewManifest) -> str:
    safety_items = (
        f"Decision: {manifest.decision.value}",
        f"Preview type: {manifest.preview_type.value}",
        f"Status: {manifest.status.value}",
        f"Providers enabled: {manifest.providers_enabled}",
        f"MCP connectors enabled: {manifest.mcp_connectors_enabled}",
        f"Production data used: {manifest.production_data_used}",
        f"Credentials required: {manifest.credentials_required}",
        f"Runtime enabled: {manifest.runtime_enabled}",
        f"Writes enabled: {manifest.writes_enabled}",
        f"Notifications enabled: {manifest.notifications_enabled}",
        f"Remediation enabled: {manifest.remediation_enabled}",
        f"Benchmark truth mutation enabled: {manifest.benchmark_truth_mutation_enabled}",
        f"Autonomous action enabled: {manifest.autonomous_action_enabled}",
        f"Human approval required: {manifest.human_approval_required}",
        f"Rollback required: {manifest.rollback_required}",
    )

    return (
        "<section id=\"safety-banner\">"
        "<h2>Safety Posture</h2>"
        "<ul>"
        + "".join(_safe_li(item) for item in safety_items)
        + "</ul>"
        "</section>"
    )


def _render_page_html(
    *,
    title: str,
    manifest: LocalStaticPreviewManifest,
    source_paths: tuple[str, ...],
    body_points: tuple[str, ...],
) -> str:
    return (
        "<!doctype html>"
        "<html>"
        "<head>"
        f"<title>{escape(title)}</title>"
        "</head>"
        "<body>"
        f"<h1>{escape(title)}</h1>"
        + _render_safety_banner(manifest)
        + "<section id=\"source-paths\"><h2>Source Artifacts</h2><ul>"
        + "".join(_safe_li(path) for path in source_paths)
        + "</ul></section>"
        + "<section id=\"page-summary\"><h2>Page Summary</h2><ul>"
        + "".join(_safe_li(point) for point in body_points)
        + "</ul></section>"
        + "</body></html>"
    )



def _body_points_for_kind(kind: LocalStaticPreviewPageKind) -> tuple[str, ...]:
    if kind == LocalStaticPreviewPageKind.LANDING:
        return (
            "Portfolio front door for EAIOS.",
            "Synthetic execution, real enterprise architecture.",
            "Cloud deployment remains not approved.",
            "Static preview remains local and in memory.",
        )

    if kind == LocalStaticPreviewPageKind.ARCHITECTURE:
        return (
            "Business Outcome -> Capability -> Skill -> Agent / Human / Tool / Workflow.",
            "Governance, observability, feedback, and learning remain first-class.",
            "EAIOS is positioned as an enterprise AI operating model.",
        )

    if kind == LocalStaticPreviewPageKind.DEMO_STORYBOARD:
        return (
            "Maintain Application Health.",
            "HIGH evidence with LOW operational confidence leads to expanded validation.",
            "Human approval remains required.",
            "Autonomous action remains disabled.",
        )

    if kind == LocalStaticPreviewPageKind.ENTERPRISE_MAPPING:
        return (
            "Synthetic records map to ServiceNow, BigPanda, Dynatrace, SAP SolMan, CMDB, and Solution 360.",
            "The preview explains integration seams without executing integrations.",
            "Providers and MCP connectors remain disabled.",
        )

    if kind == LocalStaticPreviewPageKind.INTERVIEW_QA:
        return (
            "Explains what EAIOS is.",
            "Explains synthetic versus real enterprise mapping.",
            "Explains why deployment remains gated.",
            "Explains provider, connector, benchmark, and human approval boundaries.",
        )

    return (
        "Manifest view of disabled-state controls.",
        "Decision remains DO_NOT_DEPLOY_YET.",
        "No implementation approval is created by this render.",
    )


def build_local_static_preview_pages(
    manifest: LocalStaticPreviewManifest,
) -> tuple[LocalStaticPreviewPage, ...]:
    pages: list[LocalStaticPreviewPage] = []

    for artifact in manifest.planned_artifacts:
        kind = _PAGE_KIND_BY_OUTPUT[artifact.output_path]
        title = _TITLE_BY_KIND[kind]
        source_paths = tuple(artifact.source_paths)
        html = _render_page_html(
            title=title,
            manifest=manifest,
            source_paths=source_paths,
            body_points=_body_points_for_kind(kind),
        )

        pages.append(
            LocalStaticPreviewPage(
                page_id=artifact.artifact_id.replace("artifact-", "page-"),
                kind=kind,
                output_path=artifact.output_path,
                title=title,
                source_paths=source_paths,
                html=html,
                rendered_in_memory=True,
                persisted=False,
            )
        )

    return tuple(pages)


def render_local_static_preview(
    manifest: LocalStaticPreviewManifest | None = None,
) -> LocalStaticPreviewRenderResult:
    manifest = manifest or build_local_static_preview_manifest(
        build_generation_context(
            branch="sprint-11-local-static-preview",
            commit="local-preview-render",
            git_status_clean=True,
            full_test_suite_passed=True,
        )
    )

    valid, violations = validate_manifest_is_static_review_only(manifest)

    if not valid:
        return LocalStaticPreviewRenderResult(
            render_id="sprint11-local-static-preview-render-001",
            status=LocalStaticPreviewRenderStatus.BLOCKED_MANIFEST_VIOLATIONS,
            manifest_id=manifest.manifest_id,
            decision=manifest.decision.value,
            page_count=0,
            pages=(),
            violations=violations,
            files_persisted=False,
            site_published=False,
            server_started=False,
            browser_opened=False,
            cloud_resources_created=False,
            providers_enabled=manifest.providers_enabled,
            mcp_connectors_enabled=manifest.mcp_connectors_enabled,
            production_data_used=manifest.production_data_used,
            credentials_required=manifest.credentials_required,
            runtime_enabled=manifest.runtime_enabled,
            writes_enabled=manifest.writes_enabled,
            notifications_enabled=manifest.notifications_enabled,
            remediation_enabled=manifest.remediation_enabled,
            benchmark_truth_mutation_enabled=manifest.benchmark_truth_mutation_enabled,
            autonomous_action_enabled=manifest.autonomous_action_enabled,
            human_approval_required=manifest.human_approval_required,
            rollback_required=manifest.rollback_required,
            provenance="local_static_preview_renderer:blocked",
        )

    pages = build_local_static_preview_pages(manifest)

    return LocalStaticPreviewRenderResult(
        render_id="sprint11-local-static-preview-render-001",
        status=LocalStaticPreviewRenderStatus.RENDERED_IN_MEMORY,
        manifest_id=manifest.manifest_id,
        decision=manifest.decision.value,
        page_count=len(pages),
        pages=pages,
        violations=(),
        files_persisted=False,
        site_published=False,
        server_started=False,
        browser_opened=False,
        cloud_resources_created=False,
        providers_enabled=manifest.providers_enabled,
        mcp_connectors_enabled=manifest.mcp_connectors_enabled,
        production_data_used=manifest.production_data_used,
        credentials_required=manifest.credentials_required,
        runtime_enabled=manifest.runtime_enabled,
        writes_enabled=manifest.writes_enabled,
        notifications_enabled=manifest.notifications_enabled,
        remediation_enabled=manifest.remediation_enabled,
        benchmark_truth_mutation_enabled=manifest.benchmark_truth_mutation_enabled,
        autonomous_action_enabled=manifest.autonomous_action_enabled,
        human_approval_required=manifest.human_approval_required,
        rollback_required=manifest.rollback_required,
        provenance="local_static_preview_renderer:in_memory",
    )


def render_result_to_view_model(
    result: LocalStaticPreviewRenderResult,
) -> dict[str, Any]:
    return {
        "render_id": result.render_id,
        "status": result.status.value,
        "manifest_id": result.manifest_id,
        "decision": result.decision,
        "page_count": result.page_count,
        "pages": [
            {
                "page_id": page.page_id,
                "kind": page.kind.value,
                "output_path": page.output_path,
                "title": page.title,
                "source_paths": list(page.source_paths),
                "html": page.html,
                "rendered_in_memory": page.rendered_in_memory,
                "persisted": page.persisted,
            }
            for page in result.pages
        ],
        "violations": list(result.violations),
        "files_persisted": result.files_persisted,
        "site_published": result.site_published,
        "server_started": result.server_started,
        "browser_opened": result.browser_opened,
        "cloud_resources_created": result.cloud_resources_created,
        "providers_enabled": result.providers_enabled,
        "mcp_connectors_enabled": result.mcp_connectors_enabled,
        "production_data_used": result.production_data_used,
        "credentials_required": result.credentials_required,
        "runtime_enabled": result.runtime_enabled,
        "writes_enabled": result.writes_enabled,
        "notifications_enabled": result.notifications_enabled,
        "remediation_enabled": result.remediation_enabled,
        "benchmark_truth_mutation_enabled": result.benchmark_truth_mutation_enabled,
        "autonomous_action_enabled": result.autonomous_action_enabled,
        "human_approval_required": result.human_approval_required,
        "rollback_required": result.rollback_required,
        "provenance": result.provenance,
    }
