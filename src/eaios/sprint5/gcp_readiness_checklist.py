"""Sprint 5 GCP deployment readiness checklist.

This module creates a deployment-readiness review checklist for the Sprint 5
read-only demo.

It does not deploy cloud resources, run shell commands, load secrets, call
providers, connect real MCP tools, write external data, execute remediation,
send notifications, score benchmarks, or enable autonomous remediation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint5.mcp_connector_harness import (
    MCPConnectorHarnessProfile,
    build_mcp_connector_harness_profile,
    summarize_mcp_connector_harness_profile,
    to_view_model as mcp_connector_harness_to_view_model,
)


class GCPReadinessCategory(str, Enum):
    RUNTIME_PACKAGING = "RUNTIME_PACKAGING"
    CONFIGURATION_BOUNDARY = "CONFIGURATION_BOUNDARY"
    SECRET_HANDLING = "SECRET_HANDLING"
    PROVIDER_INTEGRATION = "PROVIDER_INTEGRATION"
    CONNECTOR_INTEGRATION = "CONNECTOR_INTEGRATION"
    EXTERNAL_WRITES = "EXTERNAL_WRITES"
    AUDIT_EXPORT = "AUDIT_EXPORT"
    HUMAN_APPROVAL = "HUMAN_APPROVAL"
    DEPLOYMENT_ACTION = "DEPLOYMENT_ACTION"


class GCPReadinessDecision(str, Enum):
    READY_READ_ONLY = "READY_READ_ONLY"
    BLOCKED_REQUIRES_REVIEW = "BLOCKED_REQUIRES_REVIEW"
    NOT_APPLICABLE_READ_ONLY = "NOT_APPLICABLE_READ_ONLY"


class GCPDeploymentReadinessState(str, Enum):
    REVIEW_READY_NOT_DEPLOYED = "REVIEW_READY_NOT_DEPLOYED"
    DEPLOYMENT_BLOCKED_PENDING_APPROVAL = "DEPLOYMENT_BLOCKED_PENDING_APPROVAL"


@dataclass(frozen=True)
class GCPReadinessCheck:
    check_id: str
    category: GCPReadinessCategory
    title: str
    decision: GCPReadinessDecision
    passed: bool
    blocking: bool
    evidence_refs: tuple[str, ...]
    blockers: tuple[str, ...]
    provenance: str


@dataclass(frozen=True)
class GCPDeploymentGate:
    gate_id: str
    name: str
    decision: GCPReadinessDecision
    allowed: bool
    reason: str
    required_review: str
    can_create_cloud_resources: bool
    can_load_secrets: bool
    can_access_network: bool
    can_enable_real_connectors: bool
    can_execute_remediation: bool
    can_score_benchmark: bool
    provenance: str


@dataclass(frozen=True)
class GCPReadinessChecklist:
    checklist_id: str
    source_connector_harness_profile_id: str
    target_environment: str
    readiness_state: GCPDeploymentReadinessState
    checks: tuple[GCPReadinessCheck, ...]
    deployment_gates: tuple[GCPDeploymentGate, ...]
    allowed_next_steps: tuple[str, ...]
    blocked_deployment_actions: tuple[str, ...]
    required_human_reviews: tuple[str, ...]
    connector_harness_summary: dict[str, object]
    connector_harness_view: dict[str, Any]
    deployment_plan_generated: bool
    deployment_actions_performed: bool
    cloud_resources_created: bool
    shell_commands_executed: bool
    secrets_loaded: bool
    network_access_performed: bool
    provider_calls_allowed: bool
    real_connectors_allowed: bool
    external_writes_allowed: bool
    remediation_allowed: bool
    notification_allowed: bool
    benchmark_scoring_allowed_from_readiness: bool
    autonomous_remediation_allowed: bool
    human_review_required: bool
    provenance: str


def build_gcp_readiness_checklist(
    harness_profile: MCPConnectorHarnessProfile | None = None,
) -> GCPReadinessChecklist:
    if harness_profile is None:
        harness_profile = build_mcp_connector_harness_profile()

    checks = _build_checks(harness_profile)
    deployment_gates = _build_deployment_gates()

    return GCPReadinessChecklist(
        checklist_id="sprint5-gcp-readiness-checklist-001",
        source_connector_harness_profile_id=harness_profile.profile_id,
        target_environment="GCP_READINESS_REVIEW_ONLY",
        readiness_state=GCPDeploymentReadinessState.REVIEW_READY_NOT_DEPLOYED,
        checks=checks,
        deployment_gates=deployment_gates,
        allowed_next_steps=(
            "review_local_demo_export",
            "review_operator_screen_model",
            "review_cloud_safety_profile",
            "review_provider_plugin_seam",
            "review_mcp_connector_harness",
        ),
        blocked_deployment_actions=(
            "create_cloud_resources",
            "run_shell_deployment_command",
            "load_secret_material",
            "enable_real_provider",
            "enable_real_mcp_connectors",
            "perform_external_write",
            "execute_remediation",
            "send_notification",
            "score_benchmark_from_deployment",
        ),
        required_human_reviews=(
            "cloud_architecture_review",
            "security_and_secret_handling_review",
            "provider_integration_review",
            "mcp_connector_permission_review",
            "production_deployment_approval",
        ),
        connector_harness_summary=summarize_mcp_connector_harness_profile(
            harness_profile
        ),
        connector_harness_view=mcp_connector_harness_to_view_model(harness_profile),
        deployment_plan_generated=True,
        deployment_actions_performed=False,
        cloud_resources_created=False,
        shell_commands_executed=False,
        secrets_loaded=False,
        network_access_performed=False,
        provider_calls_allowed=False,
        real_connectors_allowed=False,
        external_writes_allowed=False,
        remediation_allowed=False,
        notification_allowed=False,
        benchmark_scoring_allowed_from_readiness=False,
        autonomous_remediation_allowed=False,
        human_review_required=True,
        provenance="gcp_readiness_checklist:review_only_checklist",
    )


def summarize_gcp_readiness_checklist(
    checklist: GCPReadinessChecklist,
) -> dict[str, object]:
    return {
        "checklist_id": checklist.checklist_id,
        "source_connector_harness_profile_id": (
            checklist.source_connector_harness_profile_id
        ),
        "target_environment": checklist.target_environment,
        "readiness_state": checklist.readiness_state.value,
        "check_count": len(checklist.checks),
        "passed_check_count": len([check for check in checklist.checks if check.passed]),
        "deployment_gate_count": len(checklist.deployment_gates),
        "allowed_gate_count": len(
            [gate for gate in checklist.deployment_gates if gate.allowed]
        ),
        "blocked_gate_count": len(
            [gate for gate in checklist.deployment_gates if not gate.allowed]
        ),
        "allowed_next_step_count": len(checklist.allowed_next_steps),
        "blocked_deployment_action_count": len(checklist.blocked_deployment_actions),
        "required_human_review_count": len(checklist.required_human_reviews),
        "deployment_plan_generated": checklist.deployment_plan_generated,
        "deployment_actions_performed": checklist.deployment_actions_performed,
        "cloud_resources_created": checklist.cloud_resources_created,
        "shell_commands_executed": checklist.shell_commands_executed,
        "secrets_loaded": checklist.secrets_loaded,
        "network_access_performed": checklist.network_access_performed,
        "provider_calls_allowed": checklist.provider_calls_allowed,
        "real_connectors_allowed": checklist.real_connectors_allowed,
        "external_writes_allowed": checklist.external_writes_allowed,
        "remediation_allowed": checklist.remediation_allowed,
        "notification_allowed": checklist.notification_allowed,
        "benchmark_scoring_allowed_from_readiness": (
            checklist.benchmark_scoring_allowed_from_readiness
        ),
        "autonomous_remediation_allowed": checklist.autonomous_remediation_allowed,
        "human_review_required": checklist.human_review_required,
    }


def to_view_model(checklist: GCPReadinessChecklist) -> dict[str, Any]:
    return {
        "summary": summarize_gcp_readiness_checklist(checklist),
        "checks": [
            {
                "check_id": check.check_id,
                "category": check.category.value,
                "title": check.title,
                "decision": check.decision.value,
                "passed": check.passed,
                "blocking": check.blocking,
                "evidence_refs": list(check.evidence_refs),
                "blockers": list(check.blockers),
                "provenance": check.provenance,
            }
            for check in checklist.checks
        ],
        "deployment_gates": [
            {
                "gate_id": gate.gate_id,
                "name": gate.name,
                "decision": gate.decision.value,
                "allowed": gate.allowed,
                "reason": gate.reason,
                "required_review": gate.required_review,
                "can_create_cloud_resources": gate.can_create_cloud_resources,
                "can_load_secrets": gate.can_load_secrets,
                "can_access_network": gate.can_access_network,
                "can_enable_real_connectors": gate.can_enable_real_connectors,
                "can_execute_remediation": gate.can_execute_remediation,
                "can_score_benchmark": gate.can_score_benchmark,
                "provenance": gate.provenance,
            }
            for gate in checklist.deployment_gates
        ],
        "allowed_next_steps": list(checklist.allowed_next_steps),
        "blocked_deployment_actions": list(checklist.blocked_deployment_actions),
        "required_human_reviews": list(checklist.required_human_reviews),
        "connector_harness_summary": checklist.connector_harness_summary,
        "connector_harness_view": checklist.connector_harness_view,
        "deployment_plan_generated": checklist.deployment_plan_generated,
        "deployment_actions_performed": checklist.deployment_actions_performed,
        "cloud_resources_created": checklist.cloud_resources_created,
        "shell_commands_executed": checklist.shell_commands_executed,
        "secrets_loaded": checklist.secrets_loaded,
        "network_access_performed": checklist.network_access_performed,
        "provider_calls_allowed": checklist.provider_calls_allowed,
        "real_connectors_allowed": checklist.real_connectors_allowed,
        "external_writes_allowed": checklist.external_writes_allowed,
        "remediation_allowed": checklist.remediation_allowed,
        "notification_allowed": checklist.notification_allowed,
        "benchmark_scoring_allowed_from_readiness": (
            checklist.benchmark_scoring_allowed_from_readiness
        ),
        "autonomous_remediation_allowed": checklist.autonomous_remediation_allowed,
        "human_review_required": checklist.human_review_required,
        "provenance": checklist.provenance,
    }


def _build_checks(
    harness_profile: MCPConnectorHarnessProfile,
) -> tuple[GCPReadinessCheck, ...]:
    return (
        GCPReadinessCheck(
            check_id="gcp-check-runtime-packaging-001",
            category=GCPReadinessCategory.RUNTIME_PACKAGING,
            title="Runtime package can be reviewed as read-only demo",
            decision=GCPReadinessDecision.READY_READ_ONLY,
            passed=True,
            blocking=True,
            evidence_refs=(harness_profile.profile_id,),
            blockers=(),
            provenance="gcp_readiness_checklist:check",
        ),
        GCPReadinessCheck(
            check_id="gcp-check-config-boundary-001",
            category=GCPReadinessCategory.CONFIGURATION_BOUNDARY,
            title="Configuration boundary preserves read-only execution",
            decision=GCPReadinessDecision.READY_READ_ONLY,
            passed=True,
            blocking=True,
            evidence_refs=("sprint5-cloud-safe-config-profile-001",),
            blockers=(),
            provenance="gcp_readiness_checklist:check",
        ),
        GCPReadinessCheck(
            check_id="gcp-check-secret-handling-001",
            category=GCPReadinessCategory.SECRET_HANDLING,
            title="Secret handling requires separate security review",
            decision=GCPReadinessDecision.BLOCKED_REQUIRES_REVIEW,
            passed=True,
            blocking=True,
            evidence_refs=("provider.llm", "mcp.connectors", "cloud.gcp_deploy"),
            blockers=("load_secret_material",),
            provenance="gcp_readiness_checklist:check",
        ),
        GCPReadinessCheck(
            check_id="gcp-check-provider-integration-001",
            category=GCPReadinessCategory.PROVIDER_INTEGRATION,
            title="Provider integration remains disabled",
            decision=GCPReadinessDecision.BLOCKED_REQUIRES_REVIEW,
            passed=True,
            blocking=True,
            evidence_refs=("sprint5-provider-plugin-seam-profile-001",),
            blockers=("enable_real_provider",),
            provenance="gcp_readiness_checklist:check",
        ),
        GCPReadinessCheck(
            check_id="gcp-check-connector-integration-001",
            category=GCPReadinessCategory.CONNECTOR_INTEGRATION,
            title="Real MCP connectors remain disabled",
            decision=GCPReadinessDecision.BLOCKED_REQUIRES_REVIEW,
            passed=True,
            blocking=True,
            evidence_refs=(harness_profile.profile_id,),
            blockers=("enable_real_mcp_connectors",),
            provenance="gcp_readiness_checklist:check",
        ),
        GCPReadinessCheck(
            check_id="gcp-check-external-writes-001",
            category=GCPReadinessCategory.EXTERNAL_WRITES,
            title="External writes are blocked",
            decision=GCPReadinessDecision.BLOCKED_REQUIRES_REVIEW,
            passed=True,
            blocking=True,
            evidence_refs=("storage.external_write",),
            blockers=("perform_external_write",),
            provenance="gcp_readiness_checklist:check",
        ),
        GCPReadinessCheck(
            check_id="gcp-check-audit-export-001",
            category=GCPReadinessCategory.AUDIT_EXPORT,
            title="Audit export artifacts are available",
            decision=GCPReadinessDecision.READY_READ_ONLY,
            passed=True,
            blocking=True,
            evidence_refs=(
                "sprint5-operator-dashboard-export-001",
                "sprint5-operator-review-screen-001",
            ),
            blockers=(),
            provenance="gcp_readiness_checklist:check",
        ),
        GCPReadinessCheck(
            check_id="gcp-check-human-approval-001",
            category=GCPReadinessCategory.HUMAN_APPROVAL,
            title="Human approval remains required",
            decision=GCPReadinessDecision.READY_READ_ONLY,
            passed=True,
            blocking=True,
            evidence_refs=("human_review_required",),
            blockers=(),
            provenance="gcp_readiness_checklist:check",
        ),
        GCPReadinessCheck(
            check_id="gcp-check-deployment-action-001",
            category=GCPReadinessCategory.DEPLOYMENT_ACTION,
            title="Deployment actions are not performed by readiness checklist",
            decision=GCPReadinessDecision.BLOCKED_REQUIRES_REVIEW,
            passed=True,
            blocking=True,
            evidence_refs=("GCP_READINESS_REVIEW_ONLY",),
            blockers=("create_cloud_resources", "run_shell_deployment_command"),
            provenance="gcp_readiness_checklist:check",
        ),
    )


def _build_deployment_gates() -> tuple[GCPDeploymentGate, ...]:
    return (
        GCPDeploymentGate(
            gate_id="gcp-gate-local-review-export-001",
            name="Local read-only review export",
            decision=GCPReadinessDecision.READY_READ_ONLY,
            allowed=True,
            reason="Local review artifacts can be generated without cloud deployment.",
            required_review="operator_review",
            can_create_cloud_resources=False,
            can_load_secrets=False,
            can_access_network=False,
            can_enable_real_connectors=False,
            can_execute_remediation=False,
            can_score_benchmark=False,
            provenance="gcp_readiness_checklist:deployment_gate",
        ),
        GCPDeploymentGate(
            gate_id="gcp-gate-cloud-resource-creation-001",
            name="Cloud resource creation",
            decision=GCPReadinessDecision.BLOCKED_REQUIRES_REVIEW,
            allowed=False,
            reason="Cloud resource creation requires deployment approval.",
            required_review="cloud_architecture_review",
            can_create_cloud_resources=False,
            can_load_secrets=False,
            can_access_network=False,
            can_enable_real_connectors=False,
            can_execute_remediation=False,
            can_score_benchmark=False,
            provenance="gcp_readiness_checklist:deployment_gate",
        ),
        GCPDeploymentGate(
            gate_id="gcp-gate-secret-loading-001",
            name="Secret loading",
            decision=GCPReadinessDecision.BLOCKED_REQUIRES_REVIEW,
            allowed=False,
            reason="Secret material requires security review and approved storage boundary.",
            required_review="security_and_secret_handling_review",
            can_create_cloud_resources=False,
            can_load_secrets=False,
            can_access_network=False,
            can_enable_real_connectors=False,
            can_execute_remediation=False,
            can_score_benchmark=False,
            provenance="gcp_readiness_checklist:deployment_gate",
        ),
        GCPDeploymentGate(
            gate_id="gcp-gate-provider-network-001",
            name="Provider and network access",
            decision=GCPReadinessDecision.BLOCKED_REQUIRES_REVIEW,
            allowed=False,
            reason="Provider and network access remain disabled until reviewed.",
            required_review="provider_integration_review",
            can_create_cloud_resources=False,
            can_load_secrets=False,
            can_access_network=False,
            can_enable_real_connectors=False,
            can_execute_remediation=False,
            can_score_benchmark=False,
            provenance="gcp_readiness_checklist:deployment_gate",
        ),
        GCPDeploymentGate(
            gate_id="gcp-gate-real-connectors-001",
            name="Real MCP connectors",
            decision=GCPReadinessDecision.BLOCKED_REQUIRES_REVIEW,
            allowed=False,
            reason="Real connectors require permission, audit, and sandbox review.",
            required_review="mcp_connector_permission_review",
            can_create_cloud_resources=False,
            can_load_secrets=False,
            can_access_network=False,
            can_enable_real_connectors=False,
            can_execute_remediation=False,
            can_score_benchmark=False,
            provenance="gcp_readiness_checklist:deployment_gate",
        ),
        GCPDeploymentGate(
            gate_id="gcp-gate-remediation-benchmark-001",
            name="Remediation and benchmark scoring",
            decision=GCPReadinessDecision.BLOCKED_REQUIRES_REVIEW,
            allowed=False,
            reason="Remediation, notifications, and benchmark scoring are blocked.",
            required_review="production_deployment_approval",
            can_create_cloud_resources=False,
            can_load_secrets=False,
            can_access_network=False,
            can_enable_real_connectors=False,
            can_execute_remediation=False,
            can_score_benchmark=False,
            provenance="gcp_readiness_checklist:deployment_gate",
        ),
    )
