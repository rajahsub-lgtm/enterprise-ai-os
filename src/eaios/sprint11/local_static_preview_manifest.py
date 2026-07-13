"""Sprint 11 local static preview manifest builder.

This module builds an in-memory manifest for a local static preview.

It does not write files, publish a site, start a server, open a browser, create
cloud resources, call providers, call MCP connectors, load credentials, read
production data, send notifications, execute remediation, mutate benchmark
truth, approve actions, or enable autonomous action.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any

from eaios.sprint11.local_static_preview_generator import (
    LocalStaticPreviewGeneratorContract,
    LocalStaticPreviewMode,
    LocalStaticPreviewType,
    build_local_static_preview_generator_contract,
)


class LocalStaticPreviewManifestStatus(str, Enum):
    READY_IN_MEMORY = "READY_IN_MEMORY"
    BLOCKED_INVALID_CONTEXT = "BLOCKED_INVALID_CONTEXT"


class LocalStaticPreviewDecision(str, Enum):
    DO_NOT_DEPLOY_YET = "DO_NOT_DEPLOY_YET"


@dataclass(frozen=True)
class LocalStaticPreviewGenerationContext:
    branch: str
    commit: str
    git_status_clean: bool
    full_test_suite_passed: bool


@dataclass(frozen=True)
class LocalStaticPreviewManifestArtifact:
    artifact_id: str
    output_path: str
    source_paths: tuple[str, ...]
    materialized: bool
    included: bool


@dataclass(frozen=True)
class LocalStaticPreviewManifest:
    manifest_id: str
    preview_id: str
    preview_type: LocalStaticPreviewType
    mode: LocalStaticPreviewMode
    status: LocalStaticPreviewManifestStatus
    decision: LocalStaticPreviewDecision
    branch: str
    commit: str
    git_status_clean: bool
    full_test_suite_passed: bool
    source_artifacts: tuple[str, ...]
    planned_artifacts: tuple[LocalStaticPreviewManifestArtifact, ...]
    allowed_actions: tuple[str, ...]
    blocked_actions: tuple[str, ...]
    cloud_deployment_approved: bool
    static_preview_approved: bool
    implementation_approved: bool
    files_materialized: bool
    cloud_resources_created: bool
    runtime_enabled: bool
    server_started: bool
    browser_opened: bool
    providers_enabled: bool
    provider_runtime_enabled: bool
    provider_credentials_present: bool
    provider_invocation_allowed: bool
    provider_cost_enabled: bool
    mcp_connectors_enabled: bool
    connector_runtime_enabled: bool
    connector_credentials_present: bool
    connector_invocation_allowed: bool
    connector_write_allowed: bool
    connector_notification_allowed: bool
    connector_remediation_allowed: bool
    connector_benchmark_mutation_allowed: bool
    connector_cost_enabled: bool
    production_data_used: bool
    credentials_required: bool
    writes_enabled: bool
    notifications_enabled: bool
    remediation_enabled: bool
    benchmark_truth_mutation_enabled: bool
    autonomous_action_enabled: bool
    human_approval_required: bool
    rollback_required: bool
    approval_record_created: bool
    release_created: bool
    provenance: str


def build_generation_context(
    *,
    branch: str,
    commit: str,
    git_status_clean: bool,
    full_test_suite_passed: bool,
) -> LocalStaticPreviewGenerationContext:
    return LocalStaticPreviewGenerationContext(
        branch=branch,
        commit=commit,
        git_status_clean=git_status_clean,
        full_test_suite_passed=full_test_suite_passed,
    )


def _status_for_context(
    context: LocalStaticPreviewGenerationContext,
) -> LocalStaticPreviewManifestStatus:
    if (
        context.branch == "sprint-11-local-static-preview"
        and bool(context.commit.strip())
        and context.git_status_clean
        and context.full_test_suite_passed
    ):
        return LocalStaticPreviewManifestStatus.READY_IN_MEMORY

    return LocalStaticPreviewManifestStatus.BLOCKED_INVALID_CONTEXT



def build_local_static_preview_manifest(
    context: LocalStaticPreviewGenerationContext,
    contract: LocalStaticPreviewGeneratorContract | None = None,
) -> LocalStaticPreviewManifest:
    contract = contract or build_local_static_preview_generator_contract()
    manifest_contract = contract.manifest_contract
    status = _status_for_context(context)

    planned_artifacts = tuple(
        LocalStaticPreviewManifestArtifact(
            artifact_id=artifact.artifact_id,
            output_path=artifact.output_path,
            source_paths=artifact.source_paths,
            materialized=False,
            included=True,
        )
        for artifact in contract.planned_artifacts
    )

    return LocalStaticPreviewManifest(
        manifest_id="sprint11-local-static-preview-manifest-001",
        preview_id=manifest_contract.preview_id,
        preview_type=manifest_contract.preview_type,
        mode=manifest_contract.mode,
        status=status,
        decision=LocalStaticPreviewDecision.DO_NOT_DEPLOY_YET,
        branch=context.branch,
        commit=context.commit,
        git_status_clean=context.git_status_clean,
        full_test_suite_passed=context.full_test_suite_passed,
        source_artifacts=tuple(source.path for source in contract.source_artifacts),
        planned_artifacts=planned_artifacts,
        allowed_actions=contract.allowed_actions,
        blocked_actions=contract.blocked_actions,
        cloud_deployment_approved=False,
        static_preview_approved=False,
        implementation_approved=False,
        files_materialized=False,
        cloud_resources_created=False,
        runtime_enabled=False,
        server_started=False,
        browser_opened=False,
        providers_enabled=manifest_contract.providers_enabled,
        provider_runtime_enabled=manifest_contract.provider_runtime_enabled,
        provider_credentials_present=manifest_contract.provider_credentials_present,
        provider_invocation_allowed=manifest_contract.provider_invocation_allowed,
        provider_cost_enabled=manifest_contract.provider_cost_enabled,
        mcp_connectors_enabled=manifest_contract.mcp_connectors_enabled,
        connector_runtime_enabled=manifest_contract.connector_runtime_enabled,
        connector_credentials_present=manifest_contract.connector_credentials_present,
        connector_invocation_allowed=manifest_contract.connector_invocation_allowed,
        connector_write_allowed=manifest_contract.connector_write_allowed,
        connector_notification_allowed=manifest_contract.connector_notification_allowed,
        connector_remediation_allowed=manifest_contract.connector_remediation_allowed,
        connector_benchmark_mutation_allowed=(
            manifest_contract.connector_benchmark_mutation_allowed
        ),
        connector_cost_enabled=manifest_contract.connector_cost_enabled,
        production_data_used=manifest_contract.production_data_used,
        credentials_required=False,
        writes_enabled=manifest_contract.writes_enabled,
        notifications_enabled=manifest_contract.notifications_enabled,
        remediation_enabled=manifest_contract.remediation_enabled,
        benchmark_truth_mutation_enabled=(
            manifest_contract.benchmark_truth_mutation_enabled
        ),
        autonomous_action_enabled=manifest_contract.autonomous_action_enabled,
        human_approval_required=manifest_contract.human_approval_required,
        rollback_required=manifest_contract.rollback_required,
        approval_record_created=False,
        release_created=False,
        provenance="local_static_preview_manifest:in_memory",
    )


def manifest_to_dict(manifest: LocalStaticPreviewManifest) -> dict[str, Any]:
    raw = asdict(manifest)

    raw["preview_type"] = manifest.preview_type.value
    raw["mode"] = manifest.mode.value
    raw["status"] = manifest.status.value
    raw["decision"] = manifest.decision.value

    return raw


def summarize_manifest(manifest: LocalStaticPreviewManifest) -> dict[str, object]:
    return {
        "manifest_id": manifest.manifest_id,
        "preview_id": manifest.preview_id,
        "preview_type": manifest.preview_type.value,
        "mode": manifest.mode.value,
        "status": manifest.status.value,
        "decision": manifest.decision.value,
        "branch": manifest.branch,
        "commit": manifest.commit,
        "git_status_clean": manifest.git_status_clean,
        "full_test_suite_passed": manifest.full_test_suite_passed,
        "source_artifact_count": len(manifest.source_artifacts),
        "planned_artifact_count": len(manifest.planned_artifacts),
        "cloud_deployment_approved": manifest.cloud_deployment_approved,
        "static_preview_approved": manifest.static_preview_approved,
        "implementation_approved": manifest.implementation_approved,
        "files_materialized": manifest.files_materialized,
        "providers_enabled": manifest.providers_enabled,
        "mcp_connectors_enabled": manifest.mcp_connectors_enabled,
        "production_data_used": manifest.production_data_used,
        "credentials_required": manifest.credentials_required,
        "runtime_enabled": manifest.runtime_enabled,
        "writes_enabled": manifest.writes_enabled,
        "notifications_enabled": manifest.notifications_enabled,
        "remediation_enabled": manifest.remediation_enabled,
        "benchmark_truth_mutation_enabled": manifest.benchmark_truth_mutation_enabled,
        "autonomous_action_enabled": manifest.autonomous_action_enabled,
        "human_approval_required": manifest.human_approval_required,
        "rollback_required": manifest.rollback_required,
    }


def validate_manifest_is_static_review_only(
    manifest: LocalStaticPreviewManifest,
) -> tuple[bool, tuple[str, ...]]:
    violations: list[str] = []

    if manifest.cloud_deployment_approved:
        violations.append("cloud deployment must not be approved")
    if manifest.static_preview_approved:
        violations.append("static preview must not be approved by manifest")
    if manifest.implementation_approved:
        violations.append("implementation must not be approved by manifest")
    if manifest.files_materialized:
        violations.append("files must not be materialized")
    if manifest.cloud_resources_created:
        violations.append("cloud resources must not be created")
    if manifest.runtime_enabled:
        violations.append("runtime must not be enabled")
    if manifest.providers_enabled:
        violations.append("providers must remain disabled")
    if manifest.mcp_connectors_enabled:
        violations.append("MCP connectors must remain disabled")
    if manifest.production_data_used:
        violations.append("production data must not be used")
    if manifest.credentials_required:
        violations.append("credentials must not be required")
    if manifest.writes_enabled:
        violations.append("writes must remain disabled")
    if manifest.notifications_enabled:
        violations.append("notifications must remain disabled")
    if manifest.remediation_enabled:
        violations.append("remediation must remain disabled")
    if manifest.benchmark_truth_mutation_enabled:
        violations.append("benchmark truth mutation must remain disabled")
    if manifest.autonomous_action_enabled:
        violations.append("autonomous action must remain disabled")
    if not manifest.human_approval_required:
        violations.append("human approval must remain required")
    if not manifest.rollback_required:
        violations.append("rollback must remain required")

    return len(violations) == 0, tuple(violations)
