"""Sprint 11 local static preview bundle assembler.

This module assembles rendered static preview pages into an in-memory bundle.

It does not persist files, publish a site, start a server, launch a browser,
create cloud resources, call providers, call MCP connectors, load credentials,
read production data, send notifications, execute remediation, mutate benchmark
truth, approve actions, or enable autonomous action.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Any

from eaios.sprint11.local_static_preview_manifest import (
    LocalStaticPreviewManifest,
    manifest_to_dict,
)
from eaios.sprint11.local_static_preview_renderer import (
    LocalStaticPreviewRenderResult,
    LocalStaticPreviewRenderStatus,
    render_local_static_preview,
)


class LocalStaticPreviewBundleStatus(str, Enum):
    ASSEMBLED_IN_MEMORY = "ASSEMBLED_IN_MEMORY"
    BLOCKED_RENDER_NOT_SAFE = "BLOCKED_RENDER_NOT_SAFE"


class LocalStaticPreviewBundleFileType(str, Enum):
    HTML = "HTML"
    JSON = "JSON"


@dataclass(frozen=True)
class LocalStaticPreviewBundleFile:
    file_id: str
    output_path: str
    file_type: LocalStaticPreviewBundleFileType
    content: str
    sha256_digest: str
    byte_count: int
    persisted: bool


@dataclass(frozen=True)
class LocalStaticPreviewBundle:
    bundle_id: str
    status: LocalStaticPreviewBundleStatus
    render_id: str
    manifest_id: str
    decision: str
    files: tuple[LocalStaticPreviewBundleFile, ...]
    file_count: int
    total_byte_count: int
    bundle_digest: str
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


def _digest(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def _byte_count(value: str) -> int:
    return len(value.encode("utf-8"))


def _manifest_json(manifest: LocalStaticPreviewManifest) -> str:
    return json.dumps(manifest_to_dict(manifest), indent=2, sort_keys=True, default=str)


def _build_bundle_files(
    *,
    manifest: LocalStaticPreviewManifest,
    render_result: LocalStaticPreviewRenderResult,
) -> tuple[LocalStaticPreviewBundleFile, ...]:
    html_files = tuple(
        LocalStaticPreviewBundleFile(
            file_id=f"bundle-{page.page_id}",
            output_path=page.output_path,
            file_type=LocalStaticPreviewBundleFileType.HTML,
            content=page.html,
            sha256_digest=_digest(page.html),
            byte_count=_byte_count(page.html),
            persisted=False,
        )
        for page in render_result.pages
    )

    manifest_content = _manifest_json(manifest)
    manifest_file = LocalStaticPreviewBundleFile(
        file_id="bundle-manifest-json",
        output_path="preview/manifest.json",
        file_type=LocalStaticPreviewBundleFileType.JSON,
        content=manifest_content,
        sha256_digest=_digest(manifest_content),
        byte_count=_byte_count(manifest_content),
        persisted=False,
    )

    return html_files + (manifest_file,)


def _bundle_digest(files: tuple[LocalStaticPreviewBundleFile, ...]) -> str:
    material = "\n".join(
        f"{item.output_path}:{item.sha256_digest}" for item in sorted(files, key=lambda f: f.output_path)
    )
    return _digest(material)



def assemble_local_static_preview_bundle(
    *,
    manifest: LocalStaticPreviewManifest,
    render_result: LocalStaticPreviewRenderResult | None = None,
) -> LocalStaticPreviewBundle:
    render_result = render_result or render_local_static_preview(manifest)

    if render_result.status != LocalStaticPreviewRenderStatus.RENDERED_IN_MEMORY:
        return LocalStaticPreviewBundle(
            bundle_id="sprint11-local-static-preview-bundle-001",
            status=LocalStaticPreviewBundleStatus.BLOCKED_RENDER_NOT_SAFE,
            render_id=render_result.render_id,
            manifest_id=render_result.manifest_id,
            decision=render_result.decision,
            files=(),
            file_count=0,
            total_byte_count=0,
            bundle_digest="",
            violations=render_result.violations,
            files_persisted=False,
            site_published=False,
            server_started=False,
            browser_opened=False,
            cloud_resources_created=False,
            providers_enabled=render_result.providers_enabled,
            mcp_connectors_enabled=render_result.mcp_connectors_enabled,
            production_data_used=render_result.production_data_used,
            credentials_required=render_result.credentials_required,
            runtime_enabled=render_result.runtime_enabled,
            writes_enabled=render_result.writes_enabled,
            notifications_enabled=render_result.notifications_enabled,
            remediation_enabled=render_result.remediation_enabled,
            benchmark_truth_mutation_enabled=render_result.benchmark_truth_mutation_enabled,
            autonomous_action_enabled=render_result.autonomous_action_enabled,
            human_approval_required=render_result.human_approval_required,
            rollback_required=render_result.rollback_required,
            provenance="local_static_preview_bundle:blocked",
        )

    files = _build_bundle_files(manifest=manifest, render_result=render_result)

    return LocalStaticPreviewBundle(
        bundle_id="sprint11-local-static-preview-bundle-001",
        status=LocalStaticPreviewBundleStatus.ASSEMBLED_IN_MEMORY,
        render_id=render_result.render_id,
        manifest_id=render_result.manifest_id,
        decision=render_result.decision,
        files=files,
        file_count=len(files),
        total_byte_count=sum(item.byte_count for item in files),
        bundle_digest=_bundle_digest(files),
        violations=(),
        files_persisted=False,
        site_published=False,
        server_started=False,
        browser_opened=False,
        cloud_resources_created=False,
        providers_enabled=render_result.providers_enabled,
        mcp_connectors_enabled=render_result.mcp_connectors_enabled,
        production_data_used=render_result.production_data_used,
        credentials_required=render_result.credentials_required,
        runtime_enabled=render_result.runtime_enabled,
        writes_enabled=render_result.writes_enabled,
        notifications_enabled=render_result.notifications_enabled,
        remediation_enabled=render_result.remediation_enabled,
        benchmark_truth_mutation_enabled=render_result.benchmark_truth_mutation_enabled,
        autonomous_action_enabled=render_result.autonomous_action_enabled,
        human_approval_required=render_result.human_approval_required,
        rollback_required=render_result.rollback_required,
        provenance="local_static_preview_bundle:in_memory",
    )


def bundle_to_manifest_view(bundle: LocalStaticPreviewBundle) -> dict[str, Any]:
    return {
        "bundle_id": bundle.bundle_id,
        "status": bundle.status.value,
        "render_id": bundle.render_id,
        "manifest_id": bundle.manifest_id,
        "decision": bundle.decision,
        "file_count": bundle.file_count,
        "total_byte_count": bundle.total_byte_count,
        "bundle_digest": bundle.bundle_digest,
        "files": [
            {
                "file_id": item.file_id,
                "output_path": item.output_path,
                "file_type": item.file_type.value,
                "sha256_digest": item.sha256_digest,
                "byte_count": item.byte_count,
                "persisted": item.persisted,
            }
            for item in bundle.files
        ],
        "violations": list(bundle.violations),
        "files_persisted": bundle.files_persisted,
        "site_published": bundle.site_published,
        "server_started": bundle.server_started,
        "browser_opened": bundle.browser_opened,
        "cloud_resources_created": bundle.cloud_resources_created,
        "providers_enabled": bundle.providers_enabled,
        "mcp_connectors_enabled": bundle.mcp_connectors_enabled,
        "production_data_used": bundle.production_data_used,
        "credentials_required": bundle.credentials_required,
        "runtime_enabled": bundle.runtime_enabled,
        "writes_enabled": bundle.writes_enabled,
        "notifications_enabled": bundle.notifications_enabled,
        "remediation_enabled": bundle.remediation_enabled,
        "benchmark_truth_mutation_enabled": bundle.benchmark_truth_mutation_enabled,
        "autonomous_action_enabled": bundle.autonomous_action_enabled,
        "human_approval_required": bundle.human_approval_required,
        "rollback_required": bundle.rollback_required,
        "provenance": bundle.provenance,
    }


def validate_bundle_is_in_memory_static_only(
    bundle: LocalStaticPreviewBundle,
) -> tuple[bool, tuple[str, ...]]:
    violations: list[str] = []

    if bundle.status != LocalStaticPreviewBundleStatus.ASSEMBLED_IN_MEMORY:
        violations.append("bundle must be assembled in memory")
    if bundle.files_persisted:
        violations.append("files must not be persisted")
    if any(item.persisted for item in bundle.files):
        violations.append("bundle files must not be persisted")
    if bundle.site_published:
        violations.append("site must not be published")
    if bundle.server_started:
        violations.append("server must not be started")
    if bundle.browser_opened:
        violations.append("browser must not be opened")
    if bundle.cloud_resources_created:
        violations.append("cloud resources must not be created")
    if bundle.providers_enabled:
        violations.append("providers must remain disabled")
    if bundle.mcp_connectors_enabled:
        violations.append("MCP connectors must remain disabled")
    if bundle.production_data_used:
        violations.append("production data must not be used")
    if bundle.credentials_required:
        violations.append("credentials must not be required")
    if bundle.runtime_enabled:
        violations.append("runtime must not be enabled")
    if bundle.writes_enabled:
        violations.append("writes must remain disabled")
    if bundle.notifications_enabled:
        violations.append("notifications must remain disabled")
    if bundle.remediation_enabled:
        violations.append("remediation must remain disabled")
    if bundle.benchmark_truth_mutation_enabled:
        violations.append("benchmark truth mutation must remain disabled")
    if bundle.autonomous_action_enabled:
        violations.append("autonomous action must remain disabled")
    if not bundle.human_approval_required:
        violations.append("human approval must remain required")
    if not bundle.rollback_required:
        violations.append("rollback must remain required")

    return len(violations) == 0, tuple(violations)
