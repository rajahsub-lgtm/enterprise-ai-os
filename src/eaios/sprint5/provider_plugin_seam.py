"""Sprint 5 provider plug-in seam safety boundary.

This module defines a safe seam for future LLM/provider integration.

It does not call providers, load secrets, access networks, execute tools,
execute remediation, update benchmark truth, score benchmarks, or enable
autonomous remediation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint5.cloud_safety_config import (
    CloudSafeConfigProfile,
    build_cloud_safe_config_profile,
    summarize_cloud_safe_config_profile,
    to_view_model as cloud_config_to_view_model,
)


class ProviderPluginMode(str, Enum):
    DETERMINISTIC_FIXTURE_ONLY = "DETERMINISTIC_FIXTURE_ONLY"
    REAL_PROVIDER_DISABLED = "REAL_PROVIDER_DISABLED"


class ProviderCapability(str, Enum):
    SUMMARIZE_EVIDENCE = "SUMMARIZE_EVIDENCE"
    DRAFT_OPERATOR_TEXT = "DRAFT_OPERATOR_TEXT"
    VALIDATE_OUTPUT_SCHEMA = "VALIDATE_OUTPUT_SCHEMA"


class ProviderSafetyDecision(str, Enum):
    ALLOWED_DETERMINISTIC_LOCAL = "ALLOWED_DETERMINISTIC_LOCAL"
    BLOCKED_REAL_PROVIDER_DISABLED = "BLOCKED_REAL_PROVIDER_DISABLED"
    BLOCKED_SECRET_REQUIRED = "BLOCKED_SECRET_REQUIRED"
    BLOCKED_NETWORK_REQUIRED = "BLOCKED_NETWORK_REQUIRED"
    BLOCKED_BENCHMARK_SCORING = "BLOCKED_BENCHMARK_SCORING"
    BLOCKED_ACTION_REQUEST = "BLOCKED_ACTION_REQUEST"


@dataclass(frozen=True)
class ProviderRequestEnvelope:
    request_id: str
    capability: ProviderCapability
    prompt_summary: str
    source_profile_id: str
    allow_real_provider: bool
    requires_secret: bool
    requires_network: bool
    contains_benchmark_truth_claim: bool
    asks_to_score_benchmark: bool
    asks_to_execute_action: bool
    provenance: str


@dataclass(frozen=True)
class ProviderValidationResult:
    validation_id: str
    request_id: str
    capability: ProviderCapability
    decision: ProviderSafetyDecision
    allowed: bool
    reason: str
    deterministic_fixture_used: bool
    real_provider_call_performed: bool
    secret_loaded: bool
    network_access_performed: bool
    benchmark_truth_updated: bool
    benchmark_scoring_allowed: bool
    autonomous_action_allowed: bool
    human_review_required: bool
    provenance: str


@dataclass(frozen=True)
class ProviderPluginSeamProfile:
    profile_id: str
    source_cloud_profile_id: str
    mode: ProviderPluginMode
    request_envelopes: tuple[ProviderRequestEnvelope, ...]
    validation_results: tuple[ProviderValidationResult, ...]
    deterministic_response_fixtures: dict[str, str]
    safety_controls: tuple[str, ...]
    blocked_capabilities: tuple[str, ...]
    cloud_config_summary: dict[str, object]
    cloud_config_view: dict[str, Any]
    real_provider_calls_allowed: bool
    real_provider_call_performed: bool
    secrets_loaded: bool
    network_access_performed: bool
    benchmark_truth_update_allowed: bool
    benchmark_scoring_allowed_from_provider: bool
    autonomous_remediation_allowed: bool
    human_review_required: bool
    provenance: str


def build_provider_plugin_seam_profile(
    cloud_profile: CloudSafeConfigProfile | None = None,
) -> ProviderPluginSeamProfile:
    if cloud_profile is None:
        cloud_profile = build_cloud_safe_config_profile()

    request_envelopes = (
        ProviderRequestEnvelope(
            request_id="provider-request-local-summary-001",
            capability=ProviderCapability.SUMMARIZE_EVIDENCE,
            prompt_summary="Summarize governed dashboard evidence using deterministic fixture.",
            source_profile_id=cloud_profile.profile_id,
            allow_real_provider=False,
            requires_secret=False,
            requires_network=False,
            contains_benchmark_truth_claim=False,
            asks_to_score_benchmark=False,
            asks_to_execute_action=False,
            provenance="provider_plugin_seam:request_envelope",
        ),
        ProviderRequestEnvelope(
            request_id="provider-request-real-llm-draft-001",
            capability=ProviderCapability.DRAFT_OPERATOR_TEXT,
            prompt_summary="Draft operator-facing text using a real provider.",
            source_profile_id=cloud_profile.profile_id,
            allow_real_provider=True,
            requires_secret=True,
            requires_network=True,
            contains_benchmark_truth_claim=False,
            asks_to_score_benchmark=False,
            asks_to_execute_action=False,
            provenance="provider_plugin_seam:request_envelope",
        ),
        ProviderRequestEnvelope(
            request_id="provider-request-benchmark-score-001",
            capability=ProviderCapability.VALIDATE_OUTPUT_SCHEMA,
            prompt_summary="Attempt to score benchmark from provider output.",
            source_profile_id=cloud_profile.profile_id,
            allow_real_provider=False,
            requires_secret=False,
            requires_network=False,
            contains_benchmark_truth_claim=True,
            asks_to_score_benchmark=True,
            asks_to_execute_action=False,
            provenance="provider_plugin_seam:request_envelope",
        ),
        ProviderRequestEnvelope(
            request_id="provider-request-action-001",
            capability=ProviderCapability.DRAFT_OPERATOR_TEXT,
            prompt_summary="Attempt to draft an autonomous remediation instruction.",
            source_profile_id=cloud_profile.profile_id,
            allow_real_provider=False,
            requires_secret=False,
            requires_network=False,
            contains_benchmark_truth_claim=False,
            asks_to_score_benchmark=False,
            asks_to_execute_action=True,
            provenance="provider_plugin_seam:request_envelope",
        ),
    )

    validation_results = tuple(_validate_provider_request(envelope) for envelope in request_envelopes)

    return ProviderPluginSeamProfile(
        profile_id="sprint5-provider-plugin-seam-profile-001",
        source_cloud_profile_id=cloud_profile.profile_id,
        mode=ProviderPluginMode.DETERMINISTIC_FIXTURE_ONLY,
        request_envelopes=request_envelopes,
        validation_results=validation_results,
        deterministic_response_fixtures={
            "provider-request-local-summary-001": (
                "Deterministic fixture: operator dashboard remains read-only; "
                "human review is required; unsafe actions remain blocked."
            )
        },
        safety_controls=(
            "real_provider_disabled_by_default",
            "secret_loading_blocked",
            "network_access_blocked",
            "deterministic_fixture_only",
            "benchmark_truth_update_blocked",
            "benchmark_scoring_from_provider_blocked",
            "autonomous_action_blocked",
            "human_review_required",
        ),
        blocked_capabilities=(
            "real_llm_provider_call",
            "secret_loading",
            "network_access",
            "benchmark_truth_update",
            "benchmark_scoring_from_provider",
            "autonomous_remediation_instruction",
        ),
        cloud_config_summary=summarize_cloud_safe_config_profile(cloud_profile),
        cloud_config_view=cloud_config_to_view_model(cloud_profile),
        real_provider_calls_allowed=False,
        real_provider_call_performed=False,
        secrets_loaded=False,
        network_access_performed=False,
        benchmark_truth_update_allowed=False,
        benchmark_scoring_allowed_from_provider=False,
        autonomous_remediation_allowed=False,
        human_review_required=True,
        provenance="provider_plugin_seam:safety_profile",
    )


def summarize_provider_plugin_seam_profile(
    profile: ProviderPluginSeamProfile,
) -> dict[str, object]:
    return {
        "profile_id": profile.profile_id,
        "source_cloud_profile_id": profile.source_cloud_profile_id,
        "mode": profile.mode.value,
        "request_count": len(profile.request_envelopes),
        "validation_count": len(profile.validation_results),
        "allowed_validation_count": len(
            [result for result in profile.validation_results if result.allowed]
        ),
        "blocked_validation_count": len(
            [result for result in profile.validation_results if not result.allowed]
        ),
        "fixture_count": len(profile.deterministic_response_fixtures),
        "safety_control_count": len(profile.safety_controls),
        "blocked_capability_count": len(profile.blocked_capabilities),
        "real_provider_calls_allowed": profile.real_provider_calls_allowed,
        "real_provider_call_performed": profile.real_provider_call_performed,
        "secrets_loaded": profile.secrets_loaded,
        "network_access_performed": profile.network_access_performed,
        "benchmark_truth_update_allowed": profile.benchmark_truth_update_allowed,
        "benchmark_scoring_allowed_from_provider": (
            profile.benchmark_scoring_allowed_from_provider
        ),
        "autonomous_remediation_allowed": profile.autonomous_remediation_allowed,
        "human_review_required": profile.human_review_required,
    }


def to_view_model(profile: ProviderPluginSeamProfile) -> dict[str, Any]:
    return {
        "summary": summarize_provider_plugin_seam_profile(profile),
        "request_envelopes": [
            {
                "request_id": envelope.request_id,
                "capability": envelope.capability.value,
                "prompt_summary": envelope.prompt_summary,
                "source_profile_id": envelope.source_profile_id,
                "allow_real_provider": envelope.allow_real_provider,
                "requires_secret": envelope.requires_secret,
                "requires_network": envelope.requires_network,
                "contains_benchmark_truth_claim": envelope.contains_benchmark_truth_claim,
                "asks_to_score_benchmark": envelope.asks_to_score_benchmark,
                "asks_to_execute_action": envelope.asks_to_execute_action,
                "provenance": envelope.provenance,
            }
            for envelope in profile.request_envelopes
        ],
        "validation_results": [
            {
                "validation_id": result.validation_id,
                "request_id": result.request_id,
                "capability": result.capability.value,
                "decision": result.decision.value,
                "allowed": result.allowed,
                "reason": result.reason,
                "deterministic_fixture_used": result.deterministic_fixture_used,
                "real_provider_call_performed": result.real_provider_call_performed,
                "secret_loaded": result.secret_loaded,
                "network_access_performed": result.network_access_performed,
                "benchmark_truth_updated": result.benchmark_truth_updated,
                "benchmark_scoring_allowed": result.benchmark_scoring_allowed,
                "autonomous_action_allowed": result.autonomous_action_allowed,
                "human_review_required": result.human_review_required,
                "provenance": result.provenance,
            }
            for result in profile.validation_results
        ],
        "deterministic_response_fixtures": profile.deterministic_response_fixtures,
        "safety_controls": list(profile.safety_controls),
        "blocked_capabilities": list(profile.blocked_capabilities),
        "cloud_config_summary": profile.cloud_config_summary,
        "cloud_config_view": profile.cloud_config_view,
        "real_provider_calls_allowed": profile.real_provider_calls_allowed,
        "real_provider_call_performed": profile.real_provider_call_performed,
        "secrets_loaded": profile.secrets_loaded,
        "network_access_performed": profile.network_access_performed,
        "benchmark_truth_update_allowed": profile.benchmark_truth_update_allowed,
        "benchmark_scoring_allowed_from_provider": (
            profile.benchmark_scoring_allowed_from_provider
        ),
        "autonomous_remediation_allowed": profile.autonomous_remediation_allowed,
        "human_review_required": profile.human_review_required,
        "provenance": profile.provenance,
    }


def _validate_provider_request(
    envelope: ProviderRequestEnvelope,
) -> ProviderValidationResult:
    if envelope.asks_to_score_benchmark or envelope.contains_benchmark_truth_claim:
        return _blocked_result(
            envelope,
            ProviderSafetyDecision.BLOCKED_BENCHMARK_SCORING,
            "Provider output cannot define benchmark truth or score benchmarks.",
        )

    if envelope.asks_to_execute_action:
        return _blocked_result(
            envelope,
            ProviderSafetyDecision.BLOCKED_ACTION_REQUEST,
            "Provider seam cannot request autonomous action or remediation.",
        )

    if envelope.requires_secret:
        return _blocked_result(
            envelope,
            ProviderSafetyDecision.BLOCKED_SECRET_REQUIRED,
            "Provider request requires secret material and is blocked.",
        )

    if envelope.requires_network:
        return _blocked_result(
            envelope,
            ProviderSafetyDecision.BLOCKED_NETWORK_REQUIRED,
            "Provider request requires network access and is blocked.",
        )

    if envelope.allow_real_provider:
        return _blocked_result(
            envelope,
            ProviderSafetyDecision.BLOCKED_REAL_PROVIDER_DISABLED,
            "Real provider calls are disabled by default.",
        )

    return ProviderValidationResult(
        validation_id=f"provider-validation::{envelope.request_id}",
        request_id=envelope.request_id,
        capability=envelope.capability,
        decision=ProviderSafetyDecision.ALLOWED_DETERMINISTIC_LOCAL,
        allowed=True,
        reason="Deterministic local fixture is allowed for read-only demo output.",
        deterministic_fixture_used=True,
        real_provider_call_performed=False,
        secret_loaded=False,
        network_access_performed=False,
        benchmark_truth_updated=False,
        benchmark_scoring_allowed=False,
        autonomous_action_allowed=False,
        human_review_required=True,
        provenance="provider_plugin_seam:validation",
    )


def _blocked_result(
    envelope: ProviderRequestEnvelope,
    decision: ProviderSafetyDecision,
    reason: str,
) -> ProviderValidationResult:
    return ProviderValidationResult(
        validation_id=f"provider-validation::{envelope.request_id}",
        request_id=envelope.request_id,
        capability=envelope.capability,
        decision=decision,
        allowed=False,
        reason=reason,
        deterministic_fixture_used=False,
        real_provider_call_performed=False,
        secret_loaded=False,
        network_access_performed=False,
        benchmark_truth_updated=False,
        benchmark_scoring_allowed=False,
        autonomous_action_allowed=False,
        human_review_required=True,
        provenance="provider_plugin_seam:validation",
    )
