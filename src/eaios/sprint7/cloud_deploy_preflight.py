"""Sprint 7 cloud deploy preflight model.

This module defines a review-only preflight gate for a future cloud deployment.
It does not execute deployment commands, build images, push images, create cloud
resources, load secrets, call providers, call connectors, execute remediation,
send notifications, score benchmarks, or enable autonomous remediation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint7.local_web_review_surface import (
    build_local_web_review_surface,
    summarize_local_web_review_surface,
)


class CloudDeployPreflightMode(str, Enum):
    REVIEW_ONLY_PREFLIGHT = "REVIEW_ONLY_PREFLIGHT"


class CloudDeployPreflightStatus(str, Enum):
    BLOCKED_PENDING_REVIEWS = "BLOCKED_PENDING_REVIEWS"
    REVIEW_READY_NOT_DEPLOYED = "REVIEW_READY_NOT_DEPLOYED"


class CloudDeployCheckStatus(str, Enum):
    REQUIRED = "REQUIRED"
    BLOCKING = "BLOCKING"
    SATISFIED_BY_DESIGN = "SATISFIED_BY_DESIGN"


@dataclass(frozen=True)
class CloudDeployPreflightCheck:
    check_id: str
    name: str
    status: CloudDeployCheckStatus
    evidence_refs: tuple[str, ...]
    blocking_reason: str
    required_review: str
    provenance: str


@dataclass(frozen=True)
class CloudDeployPreflight:
    preflight_id: str
    mode: CloudDeployPreflightMode
    status: CloudDeployPreflightStatus
    title: str
    target_platform: str
    source_web_surface_id: str
    checks: tuple[CloudDeployPreflightCheck, ...]
    required_reviews: tuple[str, ...]
    blocked_actions: tuple[str, ...]
    web_surface_summary: dict[str, object]
    deployment_commands_generated: bool
    deployment_commands_executed: bool
    container_image_built: bool
    container_image_pushed: bool
    cloud_resources_created: bool
    service_account_created: bool
    secrets_loaded: bool
    network_egress_enabled: bool
    provider_calls_performed: bool
    real_connectors_called: bool
    remediation_performed: bool
    notifications_sent: bool
    benchmark_scoring_performed: bool
    benchmark_truth_updated: bool
    autonomous_remediation_allowed: bool
    human_review_required: bool
    provenance: str


def build_cloud_deploy_preflight() -> CloudDeployPreflight:
    web_surface = build_local_web_review_surface()
    web_summary = summarize_local_web_review_surface(web_surface)

    checks = (
        CloudDeployPreflightCheck(
            check_id="cloud-preflight-check-001-architecture",
            name="Cloud architecture review",
            status=CloudDeployCheckStatus.REQUIRED,
            evidence_refs=("docs/EAIOS_2_SPRINT_6_GCP_DEPLOYMENT_DESIGN.md",),
            blocking_reason="Architecture review must approve the target topology.",
            required_review="cloud_architecture_review",
            provenance="cloud_deploy_preflight:check",
        ),
        CloudDeployPreflightCheck(
            check_id="cloud-preflight-check-002-container",
            name="Container packaging review",
            status=CloudDeployCheckStatus.REQUIRED,
            evidence_refs=("src/eaios/sprint7/container_packaging_contract.py",),
            blocking_reason="Container contract is review-only and no image is built.",
            required_review="container_packaging_review",
            provenance="cloud_deploy_preflight:check",
        ),
        CloudDeployPreflightCheck(
            check_id="cloud-preflight-check-003-secret",
            name="Secret handling review",
            status=CloudDeployCheckStatus.BLOCKING,
            evidence_refs=("docs/EAIOS_2_SPRINT_6_PROVIDER_INTEGRATION_DESIGN.md",),
            blocking_reason="No secret inventory or approved secret store is enabled.",
            required_review="security_and_secret_handling_review",
            provenance="cloud_deploy_preflight:check",
        ),
        CloudDeployPreflightCheck(
            check_id="cloud-preflight-check-004-provider",
            name="Provider integration review",
            status=CloudDeployCheckStatus.BLOCKING,
            evidence_refs=("docs/EAIOS_2_SPRINT_6_PROVIDER_INTEGRATION_DESIGN.md",),
            blocking_reason="Real provider calls remain disabled by default.",
            required_review="provider_integration_review",
            provenance="cloud_deploy_preflight:check",
        ),
        CloudDeployPreflightCheck(
            check_id="cloud-preflight-check-005-connector",
            name="MCP connector permission review",
            status=CloudDeployCheckStatus.BLOCKING,
            evidence_refs=("docs/EAIOS_2_SPRINT_6_MCP_CONNECTOR_PERMISSION_MODEL.md",),
            blocking_reason="Real MCP connectors remain disabled by default.",
            required_review="mcp_connector_permission_review",
            provenance="cloud_deploy_preflight:check",
        ),
        CloudDeployPreflightCheck(
            check_id="cloud-preflight-check-006-benchmark",
            name="Benchmark truth isolation review",
            status=CloudDeployCheckStatus.REQUIRED,
            evidence_refs=("docs/EAIOS_2_SPRINT_6_CLOSEOUT.md",),
            blocking_reason="Runtime output must not define or score benchmark truth.",
            required_review="benchmark_truth_isolation_review",
            provenance="cloud_deploy_preflight:check",
        ),
        CloudDeployPreflightCheck(
            check_id="cloud-preflight-check-007-human-review",
            name="Human approval workflow review",
            status=CloudDeployCheckStatus.REQUIRED,
            evidence_refs=("docs/EAIOS_2_SPRINT_6_CLOSEOUT.md",),
            blocking_reason="Human review must remain required for high-risk actions.",
            required_review="human_approval_workflow_review",
            provenance="cloud_deploy_preflight:check",
        ),
        CloudDeployPreflightCheck(
            check_id="cloud-preflight-check-008-local-surface",
            name="Local web review surface",
            status=CloudDeployCheckStatus.SATISFIED_BY_DESIGN,
            evidence_refs=("src/eaios/sprint7/local_web_review_surface.py",),
            blocking_reason="Surface is model-only and does not start a server.",
            required_review="local_web_review_surface_review",
            provenance="cloud_deploy_preflight:check",
        ),
    )

    required_reviews = tuple(check.required_review for check in checks)

    blocked_actions = (
        "generate_deployment_command",
        "execute_deployment_command",
        "build_container_image",
        "push_container_image",
        "create_cloud_resources",
        "create_service_account",
        "load_secret_material",
        "enable_network_egress",
        "call_real_provider",
        "call_real_connector",
        "execute_remediation",
        "send_notification",
        "score_benchmark_from_cloud_runtime",
        "update_benchmark_truth_from_cloud_runtime",
        "enable_autonomous_remediation",
    )

    return CloudDeployPreflight(
        preflight_id="sprint7-cloud-deploy-preflight-001",
        mode=CloudDeployPreflightMode.REVIEW_ONLY_PREFLIGHT,
        status=CloudDeployPreflightStatus.BLOCKED_PENDING_REVIEWS,
        title="EAIOS Cloud Deploy Preflight",
        target_platform="GCP Cloud Run read-only preview",
        source_web_surface_id=str(web_summary["surface_id"]),
        checks=checks,
        required_reviews=required_reviews,
        blocked_actions=blocked_actions,
        web_surface_summary=web_summary,
        deployment_commands_generated=False,
        deployment_commands_executed=False,
        container_image_built=False,
        container_image_pushed=False,
        cloud_resources_created=False,
        service_account_created=False,
        secrets_loaded=False,
        network_egress_enabled=False,
        provider_calls_performed=False,
        real_connectors_called=False,
        remediation_performed=False,
        notifications_sent=False,
        benchmark_scoring_performed=False,
        benchmark_truth_updated=False,
        autonomous_remediation_allowed=False,
        human_review_required=True,
        provenance="cloud_deploy_preflight:model",
    )


def summarize_cloud_deploy_preflight(
    preflight: CloudDeployPreflight,
) -> dict[str, object]:
    return {
        "preflight_id": preflight.preflight_id,
        "mode": preflight.mode.value,
        "status": preflight.status.value,
        "title": preflight.title,
        "target_platform": preflight.target_platform,
        "source_web_surface_id": preflight.source_web_surface_id,
        "check_count": len(preflight.checks),
        "required_review_count": len(preflight.required_reviews),
        "blocked_action_count": len(preflight.blocked_actions),
        "deployment_commands_generated": preflight.deployment_commands_generated,
        "deployment_commands_executed": preflight.deployment_commands_executed,
        "container_image_built": preflight.container_image_built,
        "container_image_pushed": preflight.container_image_pushed,
        "cloud_resources_created": preflight.cloud_resources_created,
        "service_account_created": preflight.service_account_created,
        "secrets_loaded": preflight.secrets_loaded,
        "network_egress_enabled": preflight.network_egress_enabled,
        "provider_calls_performed": preflight.provider_calls_performed,
        "real_connectors_called": preflight.real_connectors_called,
        "remediation_performed": preflight.remediation_performed,
        "notifications_sent": preflight.notifications_sent,
        "benchmark_scoring_performed": preflight.benchmark_scoring_performed,
        "benchmark_truth_updated": preflight.benchmark_truth_updated,
        "autonomous_remediation_allowed": preflight.autonomous_remediation_allowed,
        "human_review_required": preflight.human_review_required,
    }


def to_view_model(preflight: CloudDeployPreflight) -> dict[str, Any]:
    return {
        "summary": summarize_cloud_deploy_preflight(preflight),
        "checks": [
            {
                "check_id": check.check_id,
                "name": check.name,
                "status": check.status.value,
                "evidence_refs": list(check.evidence_refs),
                "blocking_reason": check.blocking_reason,
                "required_review": check.required_review,
                "provenance": check.provenance,
            }
            for check in preflight.checks
        ],
        "required_reviews": list(preflight.required_reviews),
        "blocked_actions": list(preflight.blocked_actions),
        "web_surface_summary": preflight.web_surface_summary,
        "provenance": preflight.provenance,
    }
