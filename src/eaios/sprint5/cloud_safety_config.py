"""Sprint 5 cloud-safe configuration boundary.

This module creates a GCP-readiness review profile for the read-only operator
experience.

It does not deploy cloud resources, load secrets, call providers, connect real
tools, write external data, score benchmarks, or enable autonomous remediation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint5.operator_review_screen import (
    OperatorReviewScreenModel,
    build_operator_review_screen_model,
    summarize_operator_review_screen,
    to_view_model as operator_review_screen_to_view_model,
)


class CloudEnvironmentTarget(str, Enum):
    LOCAL_DEMO = "LOCAL_DEMO"
    GCP_READINESS_REVIEW = "GCP_READINESS_REVIEW"


class CloudReadinessState(str, Enum):
    REVIEW_READY = "REVIEW_READY"
    BLOCKED_UNSAFE_CAPABILITY = "BLOCKED_UNSAFE_CAPABILITY"


class CloudCapabilityDecision(str, Enum):
    ALLOWED_READ_ONLY = "ALLOWED_READ_ONLY"
    BLOCKED_REQUIRES_REVIEW = "BLOCKED_REQUIRES_REVIEW"


class CloudSafetyControl(str, Enum):
    READ_ONLY_RUNTIME = "READ_ONLY_RUNTIME"
    NO_EXTERNAL_WRITES = "NO_EXTERNAL_WRITES"
    NO_SECRET_MATERIAL = "NO_SECRET_MATERIAL"
    PROVIDER_DISABLED_BY_DEFAULT = "PROVIDER_DISABLED_BY_DEFAULT"
    TOOL_CONNECTORS_DISABLED_BY_DEFAULT = "TOOL_CONNECTORS_DISABLED_BY_DEFAULT"
    HUMAN_APPROVAL_REQUIRED = "HUMAN_APPROVAL_REQUIRED"
    BENCHMARK_TRUTH_EXTERNAL = "BENCHMARK_TRUTH_EXTERNAL"
    AUDIT_EXPORT_REQUIRED = "AUDIT_EXPORT_REQUIRED"


@dataclass(frozen=True)
class CloudCapabilityToggle:
    capability_id: str
    name: str
    requested: bool
    decision: CloudCapabilityDecision
    reason: str
    default_enabled: bool
    can_enable_without_review: bool
    requires_secret: bool
    performs_external_action: bool
    provenance: str


@dataclass(frozen=True)
class CloudSafetyChecklistItem:
    check_id: str
    control: CloudSafetyControl
    description: str
    passed: bool
    blocking: bool
    evidence_refs: tuple[str, ...]
    provenance: str


@dataclass(frozen=True)
class CloudSafeConfigProfile:
    profile_id: str
    source_screen_id: str
    target_environment: CloudEnvironmentTarget
    readiness_state: CloudReadinessState
    capability_toggles: tuple[CloudCapabilityToggle, ...]
    safety_checklist: tuple[CloudSafetyChecklistItem, ...]
    allowed_capabilities: tuple[str, ...]
    blocked_capabilities: tuple[str, ...]
    screen_summary: dict[str, object]
    screen_view: dict[str, Any]
    deployment_actions_performed: bool
    secrets_required: bool
    external_network_required: bool
    cloud_resources_created: bool
    provider_calls_allowed: bool
    real_tool_connectors_allowed: bool
    external_writes_allowed: bool
    benchmark_scoring_allowed_from_config: bool
    autonomous_remediation_allowed: bool
    human_review_required: bool
    provenance: str


def build_cloud_safe_config_profile(
    screen: OperatorReviewScreenModel | None = None,
) -> CloudSafeConfigProfile:
    if screen is None:
        screen = build_operator_review_screen_model()

    capability_toggles = (
        CloudCapabilityToggle(
            capability_id="runtime.read_only_demo",
            name="Read-only local runtime",
            requested=True,
            decision=CloudCapabilityDecision.ALLOWED_READ_ONLY,
            reason="Required for local demo rendering and does not perform external action.",
            default_enabled=True,
            can_enable_without_review=True,
            requires_secret=False,
            performs_external_action=False,
            provenance="cloud_safety_config:capability_toggle",
        ),
        CloudCapabilityToggle(
            capability_id="provider.llm",
            name="Real LLM provider calls",
            requested=False,
            decision=CloudCapabilityDecision.BLOCKED_REQUIRES_REVIEW,
            reason="Provider integration requires explicit secret handling and validation gate.",
            default_enabled=False,
            can_enable_without_review=False,
            requires_secret=True,
            performs_external_action=True,
            provenance="cloud_safety_config:capability_toggle",
        ),
        CloudCapabilityToggle(
            capability_id="mcp.connectors",
            name="Real MCP/tool connectors",
            requested=False,
            decision=CloudCapabilityDecision.BLOCKED_REQUIRES_REVIEW,
            reason="Real connectors require permission review, audit logging, and sandboxing.",
            default_enabled=False,
            can_enable_without_review=False,
            requires_secret=True,
            performs_external_action=True,
            provenance="cloud_safety_config:capability_toggle",
        ),
        CloudCapabilityToggle(
            capability_id="cloud.gcp_deploy",
            name="GCP deployment action",
            requested=False,
            decision=CloudCapabilityDecision.BLOCKED_REQUIRES_REVIEW,
            reason="Cloud resource creation is outside this read-only readiness profile.",
            default_enabled=False,
            can_enable_without_review=False,
            requires_secret=True,
            performs_external_action=True,
            provenance="cloud_safety_config:capability_toggle",
        ),
        CloudCapabilityToggle(
            capability_id="storage.external_write",
            name="External storage write",
            requested=False,
            decision=CloudCapabilityDecision.BLOCKED_REQUIRES_REVIEW,
            reason="External writes are blocked until an approved storage boundary exists.",
            default_enabled=False,
            can_enable_without_review=False,
            requires_secret=True,
            performs_external_action=True,
            provenance="cloud_safety_config:capability_toggle",
        ),
        CloudCapabilityToggle(
            capability_id="dashboard.apply_changes",
            name="Apply dashboard improvements",
            requested=False,
            decision=CloudCapabilityDecision.BLOCKED_REQUIRES_REVIEW,
            reason="Dashboard improvements remain review-only candidates.",
            default_enabled=False,
            can_enable_without_review=False,
            requires_secret=False,
            performs_external_action=False,
            provenance="cloud_safety_config:capability_toggle",
        ),
    )

    checklist = (
        CloudSafetyChecklistItem(
            check_id="cloud-check-read-only-runtime-001",
            control=CloudSafetyControl.READ_ONLY_RUNTIME,
            description="Runtime profile is read-only and demo-safe.",
            passed=True,
            blocking=True,
            evidence_refs=(screen.screen_id,),
            provenance="cloud_safety_config:safety_check",
        ),
        CloudSafetyChecklistItem(
            check_id="cloud-check-no-external-writes-001",
            control=CloudSafetyControl.NO_EXTERNAL_WRITES,
            description="No external writes are allowed by this profile.",
            passed=True,
            blocking=True,
            evidence_refs=("storage.external_write",),
            provenance="cloud_safety_config:safety_check",
        ),
        CloudSafetyChecklistItem(
            check_id="cloud-check-no-secret-material-001",
            control=CloudSafetyControl.NO_SECRET_MATERIAL,
            description="No secrets are required or loaded by this profile.",
            passed=True,
            blocking=True,
            evidence_refs=("provider.llm", "mcp.connectors", "cloud.gcp_deploy"),
            provenance="cloud_safety_config:safety_check",
        ),
        CloudSafetyChecklistItem(
            check_id="cloud-check-provider-disabled-001",
            control=CloudSafetyControl.PROVIDER_DISABLED_BY_DEFAULT,
            description="Provider calls are disabled by default.",
            passed=True,
            blocking=True,
            evidence_refs=("provider.llm",),
            provenance="cloud_safety_config:safety_check",
        ),
        CloudSafetyChecklistItem(
            check_id="cloud-check-tool-connectors-disabled-001",
            control=CloudSafetyControl.TOOL_CONNECTORS_DISABLED_BY_DEFAULT,
            description="Real MCP/tool connectors are disabled by default.",
            passed=True,
            blocking=True,
            evidence_refs=("mcp.connectors",),
            provenance="cloud_safety_config:safety_check",
        ),
        CloudSafetyChecklistItem(
            check_id="cloud-check-human-approval-required-001",
            control=CloudSafetyControl.HUMAN_APPROVAL_REQUIRED,
            description="Human review remains required.",
            passed=screen.human_review_required is True,
            blocking=True,
            evidence_refs=("human_review_required",),
            provenance="cloud_safety_config:safety_check",
        ),
        CloudSafetyChecklistItem(
            check_id="cloud-check-benchmark-truth-external-001",
            control=CloudSafetyControl.BENCHMARK_TRUTH_EXTERNAL,
            description="Benchmark truth remains external to cloud configuration.",
            passed=True,
            blocking=True,
            evidence_refs=("RCAEval / Train Ticket",),
            provenance="cloud_safety_config:safety_check",
        ),
        CloudSafetyChecklistItem(
            check_id="cloud-check-audit-export-required-001",
            control=CloudSafetyControl.AUDIT_EXPORT_REQUIRED,
            description="Operator export and review screen are available for audit.",
            passed=True,
            blocking=True,
            evidence_refs=(screen.source_command_result_id, screen.screen_id),
            provenance="cloud_safety_config:safety_check",
        ),
    )

    return CloudSafeConfigProfile(
        profile_id="sprint5-cloud-safe-config-profile-001",
        source_screen_id=screen.screen_id,
        target_environment=CloudEnvironmentTarget.GCP_READINESS_REVIEW,
        readiness_state=CloudReadinessState.REVIEW_READY,
        capability_toggles=capability_toggles,
        safety_checklist=checklist,
        allowed_capabilities=(
            "runtime.read_only_demo",
            "operator_review_screen_rendering",
            "local_json_export",
            "local_markdown_export",
            "governance_check_summary",
        ),
        blocked_capabilities=(
            "provider.llm",
            "mcp.connectors",
            "cloud.gcp_deploy",
            "storage.external_write",
            "dashboard.apply_changes",
            "autonomous_remediation",
            "benchmark_scoring_from_cloud_profile",
        ),
        screen_summary=summarize_operator_review_screen(screen),
        screen_view=operator_review_screen_to_view_model(screen),
        deployment_actions_performed=False,
        secrets_required=False,
        external_network_required=False,
        cloud_resources_created=False,
        provider_calls_allowed=False,
        real_tool_connectors_allowed=False,
        external_writes_allowed=False,
        benchmark_scoring_allowed_from_config=False,
        autonomous_remediation_allowed=False,
        human_review_required=True,
        provenance="cloud_safety_config:gcp_readiness_profile",
    )


def summarize_cloud_safe_config_profile(
    profile: CloudSafeConfigProfile,
) -> dict[str, object]:
    return {
        "profile_id": profile.profile_id,
        "source_screen_id": profile.source_screen_id,
        "target_environment": profile.target_environment.value,
        "readiness_state": profile.readiness_state.value,
        "capability_toggle_count": len(profile.capability_toggles),
        "safety_check_count": len(profile.safety_checklist),
        "passed_safety_check_count": len(
            [item for item in profile.safety_checklist if item.passed]
        ),
        "allowed_capability_count": len(profile.allowed_capabilities),
        "blocked_capability_count": len(profile.blocked_capabilities),
        "deployment_actions_performed": profile.deployment_actions_performed,
        "secrets_required": profile.secrets_required,
        "external_network_required": profile.external_network_required,
        "cloud_resources_created": profile.cloud_resources_created,
        "provider_calls_allowed": profile.provider_calls_allowed,
        "real_tool_connectors_allowed": profile.real_tool_connectors_allowed,
        "external_writes_allowed": profile.external_writes_allowed,
        "benchmark_scoring_allowed_from_config": (
            profile.benchmark_scoring_allowed_from_config
        ),
        "autonomous_remediation_allowed": profile.autonomous_remediation_allowed,
        "human_review_required": profile.human_review_required,
    }


def to_view_model(profile: CloudSafeConfigProfile) -> dict[str, Any]:
    return {
        "summary": summarize_cloud_safe_config_profile(profile),
        "capability_toggles": [
            {
                "capability_id": toggle.capability_id,
                "name": toggle.name,
                "requested": toggle.requested,
                "decision": toggle.decision.value,
                "reason": toggle.reason,
                "default_enabled": toggle.default_enabled,
                "can_enable_without_review": toggle.can_enable_without_review,
                "requires_secret": toggle.requires_secret,
                "performs_external_action": toggle.performs_external_action,
                "provenance": toggle.provenance,
            }
            for toggle in profile.capability_toggles
        ],
        "safety_checklist": [
            {
                "check_id": item.check_id,
                "control": item.control.value,
                "description": item.description,
                "passed": item.passed,
                "blocking": item.blocking,
                "evidence_refs": list(item.evidence_refs),
                "provenance": item.provenance,
            }
            for item in profile.safety_checklist
        ],
        "allowed_capabilities": list(profile.allowed_capabilities),
        "blocked_capabilities": list(profile.blocked_capabilities),
        "screen_summary": profile.screen_summary,
        "screen_view": profile.screen_view,
        "deployment_actions_performed": profile.deployment_actions_performed,
        "secrets_required": profile.secrets_required,
        "external_network_required": profile.external_network_required,
        "cloud_resources_created": profile.cloud_resources_created,
        "provider_calls_allowed": profile.provider_calls_allowed,
        "real_tool_connectors_allowed": profile.real_tool_connectors_allowed,
        "external_writes_allowed": profile.external_writes_allowed,
        "benchmark_scoring_allowed_from_config": (
            profile.benchmark_scoring_allowed_from_config
        ),
        "autonomous_remediation_allowed": profile.autonomous_remediation_allowed,
        "human_review_required": profile.human_review_required,
        "provenance": profile.provenance,
    }
