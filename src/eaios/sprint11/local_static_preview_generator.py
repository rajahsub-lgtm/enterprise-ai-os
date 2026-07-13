"""Sprint 11 local static preview generator contract.

This module defines a local-only static preview generator contract.

It does not write files, publish a site, start a server, open a browser, create
cloud resources, call providers, call MCP connectors, load secrets, read
production data, send notifications, execute remediation, mutate benchmark
truth, approve actions, or enable autonomous action.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class LocalStaticPreviewMode(str, Enum):
    LOCAL_CONTRACT_ONLY = "LOCAL_CONTRACT_ONLY"


class LocalStaticPreviewStatus(str, Enum):
    CONTRACT_READY_NOT_MATERIALIZED = "CONTRACT_READY_NOT_MATERIALIZED"
    BLOCKED_UNSAFE_SCOPE = "BLOCKED_UNSAFE_SCOPE"


class LocalStaticPreviewType(str, Enum):
    STATIC_REVIEW_PREVIEW = "STATIC_REVIEW_PREVIEW"


@dataclass(frozen=True)
class LocalStaticPreviewSource:
    source_id: str
    path: str
    purpose: str
    required: bool


@dataclass(frozen=True)
class LocalStaticPreviewArtifact:
    artifact_id: str
    output_path: str
    source_paths: tuple[str, ...]
    purpose: str
    materialized: bool


@dataclass(frozen=True)
class LocalStaticPreviewManifestContract:
    preview_id: str
    preview_type: LocalStaticPreviewType
    mode: LocalStaticPreviewMode
    generated_from_branch_required: bool
    generated_from_commit_required: bool
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
    secrets_required: bool
    runtime_enabled: bool
    writes_enabled: bool
    notifications_enabled: bool
    remediation_enabled: bool
    benchmark_truth_mutation_enabled: bool
    autonomous_action_enabled: bool
    human_approval_required: bool
    rollback_required: bool


@dataclass(frozen=True)
class LocalStaticPreviewGeneratorContract:
    contract_id: str
    mode: LocalStaticPreviewMode
    status: LocalStaticPreviewStatus
    preview_type: LocalStaticPreviewType
    title: str
    source_artifacts: tuple[LocalStaticPreviewSource, ...]
    planned_artifacts: tuple[LocalStaticPreviewArtifact, ...]
    manifest_contract: LocalStaticPreviewManifestContract
    allowed_actions: tuple[str, ...]
    blocked_actions: tuple[str, ...]
    cloud_deployment_approved: bool
    static_preview_approved: bool
    implementation_approved: bool
    files_materialized: bool
    cloud_resources_created: bool
    runtime_started: bool
    server_started: bool
    browser_opened: bool
    providers_enabled: bool
    mcp_connectors_enabled: bool
    production_data_used: bool
    secrets_required: bool
    writes_enabled: bool
    notifications_enabled: bool
    remediation_enabled: bool
    benchmark_truth_mutation_enabled: bool
    autonomous_action_enabled: bool
    human_approval_required: bool
    rollback_required: bool
    decision: str
    provenance: str


def build_local_static_preview_generator_contract() -> LocalStaticPreviewGeneratorContract:
    source_artifacts = (
        LocalStaticPreviewSource(
            source_id="source-readme",
            path="README.md",
            purpose="portfolio front door",
            required=True,
        ),
        LocalStaticPreviewSource(
            source_id="source-sprint8-storyboard",
            path="docs/EAIOS_2_SPRINT_8_DEMO_STORYBOARD.md",
            purpose="demo narrative",
            required=True,
        ),
        LocalStaticPreviewSource(
            source_id="source-sprint9-architecture",
            path="docs/EAIOS_2_SPRINT_9_ARCHITECTURE_NARRATIVE.md",
            purpose="architecture narrative",
            required=True,
        ),
        LocalStaticPreviewSource(
            source_id="source-sprint9-enterprise-map",
            path="docs/EAIOS_2_SPRINT_9_REAL_ENTERPRISE_MAPPING.md",
            purpose="real enterprise mapping",
            required=True,
        ),
        LocalStaticPreviewSource(
            source_id="source-sprint9-qa",
            path="docs/EAIOS_2_SPRINT_9_INTERVIEW_QA_PACK.md",
            purpose="interview Q&A",
            required=True,
        ),
        LocalStaticPreviewSource(
            source_id="source-sprint10-decision",
            path="docs/EAIOS_2_SPRINT_10_STATIC_PREVIEW_DECISION_RECORD.md",
            purpose="deployment decision guardrail",
            required=True,
        ),
    )

    planned_artifacts = (
        LocalStaticPreviewArtifact(
            artifact_id="artifact-index",
            output_path="preview/index.html",
            source_paths=("README.md",),
            purpose="static preview landing page",
            materialized=False,
        ),
        LocalStaticPreviewArtifact(
            artifact_id="artifact-architecture",
            output_path="preview/architecture.html",
            source_paths=("docs/EAIOS_2_SPRINT_9_ARCHITECTURE_NARRATIVE.md",),
            purpose="static architecture narrative",
            materialized=False,
        ),
        LocalStaticPreviewArtifact(
            artifact_id="artifact-demo-storyboard",
            output_path="preview/demo-storyboard.html",
            source_paths=("docs/EAIOS_2_SPRINT_8_DEMO_STORYBOARD.md",),
            purpose="static demo storyboard",
            materialized=False,
        ),
        LocalStaticPreviewArtifact(
            artifact_id="artifact-enterprise-map",
            output_path="preview/real-enterprise-mapping.html",
            source_paths=("docs/EAIOS_2_SPRINT_9_REAL_ENTERPRISE_MAPPING.md",),
            purpose="static enterprise mapping",
            materialized=False,
        ),
        LocalStaticPreviewArtifact(
            artifact_id="artifact-qa",
            output_path="preview/interview-qa.html",
            source_paths=("docs/EAIOS_2_SPRINT_9_INTERVIEW_QA_PACK.md",),
            purpose="static interview Q&A",
            materialized=False,
        ),
        LocalStaticPreviewArtifact(
            artifact_id="artifact-manifest",
            output_path="preview/manifest.json",
            source_paths=("docs/EAIOS_2_SPRINT_10_STATIC_PREVIEW_DECISION_RECORD.md",),
            purpose="static disabled-state manifest",
            materialized=False,
        ),
    )

    manifest_contract = LocalStaticPreviewManifestContract(
        preview_id="eaios-local-static-preview-contract-001",
        preview_type=LocalStaticPreviewType.STATIC_REVIEW_PREVIEW,
        mode=LocalStaticPreviewMode.LOCAL_CONTRACT_ONLY,
        generated_from_branch_required=True,
        generated_from_commit_required=True,
        providers_enabled=False,
        provider_runtime_enabled=False,
        provider_credentials_present=False,
        provider_invocation_allowed=False,
        provider_cost_enabled=False,
        mcp_connectors_enabled=False,
        connector_runtime_enabled=False,
        connector_credentials_present=False,
        connector_invocation_allowed=False,
        connector_write_allowed=False,
        connector_notification_allowed=False,
        connector_remediation_allowed=False,
        connector_benchmark_mutation_allowed=False,
        connector_cost_enabled=False,
        production_data_used=False,
        secrets_required=False,
        runtime_enabled=False,
        writes_enabled=False,
        notifications_enabled=False,
        remediation_enabled=False,
        benchmark_truth_mutation_enabled=False,
        autonomous_action_enabled=False,
        human_approval_required=True,
        rollback_required=True,
    )

    return LocalStaticPreviewGeneratorContract(
        contract_id="sprint11-local-static-preview-generator-contract-001",
        mode=LocalStaticPreviewMode.LOCAL_CONTRACT_ONLY,
        status=LocalStaticPreviewStatus.CONTRACT_READY_NOT_MATERIALIZED,
        preview_type=LocalStaticPreviewType.STATIC_REVIEW_PREVIEW,
        title="EAIOS Local Static Preview Generator Contract",
        source_artifacts=source_artifacts,
        planned_artifacts=planned_artifacts,
        manifest_contract=manifest_contract,
        allowed_actions=(
            "read_approved_repository_docs",
            "plan_local_static_artifacts",
            "build_disabled_state_manifest_contract",
            "validate_no_cloud_scope",
        ),
        blocked_actions=(
            "materialize_preview_files",
            "publish_static_site",
            "deploy_to_cloud",
            "create_cloud_resources",
            "create_iam_roles",
            "create_service_accounts",
            "configure_billing",
            "start_runtime",
            "start_server",
            "open_browser",
            "call_provider",
            "call_mcp_connector",
            "load_secrets",
            "read_production_data",
            "write_production_records",
            "send_notifications",
            "execute_remediation",
            "mutate_benchmark_truth",
            "approve_release",
            "enable_autonomous_action",
        ),
        cloud_deployment_approved=False,
        static_preview_approved=False,
        implementation_approved=False,
        files_materialized=False,
        cloud_resources_created=False,
        runtime_started=False,
        server_started=False,
        browser_opened=False,
        providers_enabled=False,
        mcp_connectors_enabled=False,
        production_data_used=False,
        secrets_required=False,
        writes_enabled=False,
        notifications_enabled=False,
        remediation_enabled=False,
        benchmark_truth_mutation_enabled=False,
        autonomous_action_enabled=False,
        human_approval_required=True,
        rollback_required=True,
        decision="DO_NOT_DEPLOY_YET",
        provenance="local_static_preview_generator:contract",
    )


def summarize_local_static_preview_generator_contract(
    contract: LocalStaticPreviewGeneratorContract,
) -> dict[str, object]:
    return {
        "contract_id": contract.contract_id,
        "mode": contract.mode.value,
        "status": contract.status.value,
        "preview_type": contract.preview_type.value,
        "source_artifact_count": len(contract.source_artifacts),
        "planned_artifact_count": len(contract.planned_artifacts),
        "allowed_action_count": len(contract.allowed_actions),
        "blocked_action_count": len(contract.blocked_actions),
        "cloud_deployment_approved": contract.cloud_deployment_approved,
        "static_preview_approved": contract.static_preview_approved,
        "implementation_approved": contract.implementation_approved,
        "files_materialized": contract.files_materialized,
        "providers_enabled": contract.providers_enabled,
        "mcp_connectors_enabled": contract.mcp_connectors_enabled,
        "production_data_used": contract.production_data_used,
        "secrets_required": contract.secrets_required,
        "runtime_started": contract.runtime_started,
        "writes_enabled": contract.writes_enabled,
        "notifications_enabled": contract.notifications_enabled,
        "remediation_enabled": contract.remediation_enabled,
        "benchmark_truth_mutation_enabled": contract.benchmark_truth_mutation_enabled,
        "autonomous_action_enabled": contract.autonomous_action_enabled,
        "human_approval_required": contract.human_approval_required,
        "rollback_required": contract.rollback_required,
        "decision": contract.decision,
    }


def to_view_model(contract: LocalStaticPreviewGeneratorContract) -> dict[str, Any]:
    return {
        "summary": summarize_local_static_preview_generator_contract(contract),
        "source_artifacts": [
            {
                "source_id": source.source_id,
                "path": source.path,
                "purpose": source.purpose,
                "required": source.required,
            }
            for source in contract.source_artifacts
        ],
        "planned_artifacts": [
            {
                "artifact_id": artifact.artifact_id,
                "output_path": artifact.output_path,
                "source_paths": list(artifact.source_paths),
                "purpose": artifact.purpose,
                "materialized": artifact.materialized,
            }
            for artifact in contract.planned_artifacts
        ],
        "manifest_contract": {
            field: getattr(contract.manifest_contract, field)
            for field in contract.manifest_contract.__dataclass_fields__
        },
        "allowed_actions": list(contract.allowed_actions),
        "blocked_actions": list(contract.blocked_actions),
        "provenance": contract.provenance,
    }
