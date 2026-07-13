"""Sprint 11 local static preview dry-run command.

This module runs the local static preview flow in memory.

It does not persist files, publish a site, start a server, launch a browser,
create cloud resources, call providers, call MCP connectors, load credentials,
read production data, send notifications, execute remediation, mutate benchmark
truth, approve actions, or enable autonomous action.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import Any

from eaios.sprint11.local_static_preview_bundle import (
    LocalStaticPreviewBundle,
    assemble_local_static_preview_bundle,
    bundle_to_manifest_view,
)
from eaios.sprint11.local_static_preview_manifest import (
    LocalStaticPreviewManifest,
    LocalStaticPreviewManifestStatus,
    build_generation_context,
    build_local_static_preview_manifest,
    summarize_manifest,
)
from eaios.sprint11.local_static_preview_renderer import (
    LocalStaticPreviewRenderResult,
    render_local_static_preview,
    render_result_to_view_model,
)
from eaios.sprint11.local_static_preview_verifier import (
    LocalStaticPreviewVerificationResult,
    LocalStaticPreviewVerificationStatus,
    verification_to_view_model,
    verify_local_static_preview_bundle_safety,
)


class LocalStaticPreviewDryRunStatus(str, Enum):
    COMPLETED_SAFE_LOCAL_REVIEW = "COMPLETED_SAFE_LOCAL_REVIEW"
    BLOCKED_SAFETY_VERIFICATION = "BLOCKED_SAFETY_VERIFICATION"


@dataclass(frozen=True)
class LocalStaticPreviewDryRunRequest:
    branch: str
    commit: str
    git_status_clean: bool
    full_test_suite_passed: bool


@dataclass(frozen=True)
class LocalStaticPreviewDryRunResult:
    dry_run_id: str
    status: LocalStaticPreviewDryRunStatus
    decision: str
    manifest: LocalStaticPreviewManifest
    render_result: LocalStaticPreviewRenderResult
    bundle: LocalStaticPreviewBundle
    verification: LocalStaticPreviewVerificationResult
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
    materialization_allowed: bool
    cloud_deployment_allowed: bool
    provenance: str


def build_local_static_preview_dry_run_request(
    *,
    branch: str,
    commit: str,
    git_status_clean: bool,
    full_test_suite_passed: bool,
) -> LocalStaticPreviewDryRunRequest:
    return LocalStaticPreviewDryRunRequest(
        branch=branch,
        commit=commit,
        git_status_clean=git_status_clean,
        full_test_suite_passed=full_test_suite_passed,
    )


def _verification_with_context_violation(
    verification: LocalStaticPreviewVerificationResult,
    manifest: LocalStaticPreviewManifest,
) -> LocalStaticPreviewVerificationResult:
    if manifest.status == LocalStaticPreviewManifestStatus.READY_IN_MEMORY:
        return verification

    context_violation = (
        f"manifest context must be READY_IN_MEMORY, got {manifest.status.value}",
    )

    return replace(
        verification,
        status=LocalStaticPreviewVerificationStatus.BLOCKED_SAFETY_VIOLATIONS,
        violations=verification.violations + context_violation,
        check_count=verification.check_count,
        passed_count=verification.passed_count,
        failed_count=verification.failed_count + 1,
        materialization_allowed=False,
        cloud_deployment_allowed=False,
    )


def run_local_static_preview_dry_run(
    request: LocalStaticPreviewDryRunRequest,
) -> LocalStaticPreviewDryRunResult:
    context = build_generation_context(
        branch=request.branch,
        commit=request.commit,
        git_status_clean=request.git_status_clean,
        full_test_suite_passed=request.full_test_suite_passed,
    )
    manifest = build_local_static_preview_manifest(context)
    render_result = render_local_static_preview(manifest)
    bundle = assemble_local_static_preview_bundle(
        manifest=manifest,
        render_result=render_result,
    )
    verification = _verification_with_context_violation(
        verify_local_static_preview_bundle_safety(bundle),
        manifest,
    )

    status = (
        LocalStaticPreviewDryRunStatus.COMPLETED_SAFE_LOCAL_REVIEW
        if verification.failed_count == 0
        else LocalStaticPreviewDryRunStatus.BLOCKED_SAFETY_VERIFICATION
    )

    return LocalStaticPreviewDryRunResult(
        dry_run_id="sprint11-local-static-preview-dry-run-001",
        status=status,
        decision=verification.decision,
        manifest=manifest,
        render_result=render_result,
        bundle=bundle,
        verification=verification,
        files_persisted=False,
        site_published=False,
        server_started=False,
        browser_opened=False,
        cloud_resources_created=False,
        providers_enabled=bundle.providers_enabled,
        mcp_connectors_enabled=bundle.mcp_connectors_enabled,
        production_data_used=bundle.production_data_used,
        credentials_required=bundle.credentials_required,
        runtime_enabled=bundle.runtime_enabled,
        writes_enabled=bundle.writes_enabled,
        notifications_enabled=bundle.notifications_enabled,
        remediation_enabled=bundle.remediation_enabled,
        benchmark_truth_mutation_enabled=bundle.benchmark_truth_mutation_enabled,
        autonomous_action_enabled=bundle.autonomous_action_enabled,
        human_approval_required=bundle.human_approval_required,
        rollback_required=bundle.rollback_required,
        materialization_allowed=False,
        cloud_deployment_allowed=False,
        provenance="local_static_preview_dry_run:in_memory",
    )


def dry_run_to_view_model(result: LocalStaticPreviewDryRunResult) -> dict[str, Any]:
    return {
        "dry_run_id": result.dry_run_id,
        "status": result.status.value,
        "decision": result.decision,
        "manifest_summary": summarize_manifest(result.manifest),
        "render": render_result_to_view_model(result.render_result),
        "bundle": bundle_to_manifest_view(result.bundle),
        "verification": verification_to_view_model(result.verification),
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
        "materialization_allowed": result.materialization_allowed,
        "cloud_deployment_allowed": result.cloud_deployment_allowed,
        "provenance": result.provenance,
    }
