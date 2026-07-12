"""Sprint 7 provider request and response schema.

This module defines structured, review-only provider exchange schemas.

It does not call providers, load secrets, access external networks, send prompts,
store raw provider responses, execute remediation, send notifications, score
benchmarks, update benchmark truth, or enable autonomous remediation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint7.cloud_deploy_preflight import (
    build_cloud_deploy_preflight,
    summarize_cloud_deploy_preflight,
)


class ProviderExchangeMode(str, Enum):
    REVIEW_ONLY_SCHEMA = "REVIEW_ONLY_SCHEMA"


class ProviderRequestPurpose(str, Enum):
    OPERATOR_SUMMARY = "OPERATOR_SUMMARY"
    RISK_SUMMARY = "RISK_SUMMARY"
    ROOT_CAUSE_REVIEW = "ROOT_CAUSE_REVIEW"
    APPROVAL_PACKET_DRAFT = "APPROVAL_PACKET_DRAFT"


class ProviderDataClassification(str, Enum):
    INTERNAL_DEMO_METADATA = "INTERNAL_DEMO_METADATA"
    SYNTHETIC_OPERATIONAL_EVIDENCE = "SYNTHETIC_OPERATIONAL_EVIDENCE"


class ProviderValidationStatus(str, Enum):
    NOT_EVALUATED = "NOT_EVALUATED"
    BLOCKED_PENDING_VALIDATION = "BLOCKED_PENDING_VALIDATION"


@dataclass(frozen=True)
class ProviderRequestSchema:
    request_schema_id: str
    request_purpose: ProviderRequestPurpose
    business_outcome: str
    scenario_id: str
    evidence_refs: tuple[str, ...]
    allowed_capabilities: tuple[str, ...]
    disallowed_capabilities: tuple[str, ...]
    data_classification: ProviderDataClassification
    audit_correlation_id_required: bool
    human_review_required: bool
    benchmark_truth_isolated: bool
    provider_call_performed: bool
    secrets_loaded: bool
    network_access_performed: bool
    prompt_sent_to_provider: bool
    provenance: str


@dataclass(frozen=True)
class ProviderResponseSchema:
    response_schema_id: str
    request_schema_id: str
    validation_status: ProviderValidationStatus
    required_fields: tuple[str, ...]
    validation_checks: tuple[str, ...]
    blocked_response_patterns: tuple[str, ...]
    citations_required: bool
    raw_response_storage_allowed: bool
    provider_output_accepted: bool
    benchmark_truth_claimed: bool
    benchmark_scoring_attempted: bool
    remediation_instruction_present: bool
    notification_instruction_present: bool
    secret_leakage_detected: bool
    unsupported_action_requested: bool
    human_review_required: bool
    provenance: str


@dataclass(frozen=True)
class ProviderExchangeSchema:
    schema_id: str
    mode: ProviderExchangeMode
    title: str
    source_cloud_preflight_id: str
    request_schema: ProviderRequestSchema
    response_schema: ProviderResponseSchema
    required_reviews: tuple[str, ...]
    blocked_actions: tuple[str, ...]
    cloud_preflight_summary: dict[str, object]
    provider_call_performed: bool
    secrets_loaded: bool
    network_access_performed: bool
    prompt_sent_to_provider: bool
    raw_provider_response_stored: bool
    remediation_performed: bool
    notifications_sent: bool
    benchmark_scoring_performed: bool
    benchmark_truth_updated: bool
    autonomous_remediation_allowed: bool
    human_review_required: bool
    provenance: str


def build_provider_exchange_schema() -> ProviderExchangeSchema:
    preflight = build_cloud_deploy_preflight()
    preflight_summary = summarize_cloud_deploy_preflight(preflight)

    request_schema = ProviderRequestSchema(
        request_schema_id="sprint7-provider-request-schema-001",
        request_purpose=ProviderRequestPurpose.ROOT_CAUSE_REVIEW,
        business_outcome="Maintain Application Health",
        scenario_id="application-health-read-only-review",
        evidence_refs=(
            "docs/EAIOS_2_SPRINT_6_PROVIDER_INTEGRATION_DESIGN.md",
            "docs/EAIOS_2_SPRINT_6_CLOSEOUT.md",
            "src/eaios/sprint7/cloud_deploy_preflight.py",
        ),
        allowed_capabilities=(
            "summarize_evidence",
            "identify_risks",
            "draft_operator_explanation",
            "draft_human_review_questions",
        ),
        disallowed_capabilities=(
            "define_benchmark_truth",
            "score_benchmark_results",
            "execute_remediation",
            "send_notification",
            "modify_records",
            "call_tools",
            "bypass_human_review",
        ),
        data_classification=ProviderDataClassification.SYNTHETIC_OPERATIONAL_EVIDENCE,
        audit_correlation_id_required=True,
        human_review_required=True,
        benchmark_truth_isolated=True,
        provider_call_performed=False,
        secrets_loaded=False,
        network_access_performed=False,
        prompt_sent_to_provider=False,
        provenance="provider_exchange_schema:request",
    )

    response_schema = ProviderResponseSchema(
        response_schema_id="sprint7-provider-response-schema-001",
        request_schema_id=request_schema.request_schema_id,
        validation_status=ProviderValidationStatus.BLOCKED_PENDING_VALIDATION,
        required_fields=(
            "response_id",
            "request_schema_id",
            "summary",
            "evidence_refs",
            "risk_flags",
            "confidence_statement",
            "human_review_required",
            "blocked_actions",
        ),
        validation_checks=(
            "schema_validity_check",
            "evidence_reference_check",
            "unsupported_action_check",
            "benchmark_truth_claim_check",
            "benchmark_scoring_attempt_check",
            "remediation_instruction_check",
            "notification_instruction_check",
            "secret_leakage_check",
            "unsafe_certainty_check",
            "human_review_requirement_check",
        ),
        blocked_response_patterns=(
            "benchmark_truth_claim",
            "benchmark_scoring_attempt",
            "autonomous_action_request",
            "production_write_instruction",
            "notification_send_instruction",
            "secret_exposure",
            "tool_execution_instruction",
            "human_review_bypass",
        ),
        citations_required=True,
        raw_response_storage_allowed=False,
        provider_output_accepted=False,
        benchmark_truth_claimed=False,
        benchmark_scoring_attempted=False,
        remediation_instruction_present=False,
        notification_instruction_present=False,
        secret_leakage_detected=False,
        unsupported_action_requested=False,
        human_review_required=True,
        provenance="provider_exchange_schema:response",
    )

    blocked_actions = (
        "call_real_provider",
        "load_secret_material",
        "access_external_network",
        "send_prompt_to_provider",
        "store_raw_provider_response",
        "accept_unvalidated_provider_output",
        "execute_provider_suggested_action",
        "send_provider_suggested_notification",
        "score_benchmark_from_provider_output",
        "update_benchmark_truth_from_provider_output",
        "enable_autonomous_remediation",
        "bypass_human_review",
    )

    return ProviderExchangeSchema(
        schema_id="sprint7-provider-exchange-schema-001",
        mode=ProviderExchangeMode.REVIEW_ONLY_SCHEMA,
        title="EAIOS Provider Request and Response Schema",
        source_cloud_preflight_id=str(preflight_summary["preflight_id"]),
        request_schema=request_schema,
        response_schema=response_schema,
        required_reviews=(
            "provider_request_schema_review",
            "provider_response_schema_review",
            "provider_output_validation_review",
            "secret_handling_review",
            "network_access_review",
            "benchmark_truth_isolation_review",
            "human_approval_workflow_review",
        ),
        blocked_actions=blocked_actions,
        cloud_preflight_summary=preflight_summary,
        provider_call_performed=False,
        secrets_loaded=False,
        network_access_performed=False,
        prompt_sent_to_provider=False,
        raw_provider_response_stored=False,
        remediation_performed=False,
        notifications_sent=False,
        benchmark_scoring_performed=False,
        benchmark_truth_updated=False,
        autonomous_remediation_allowed=False,
        human_review_required=True,
        provenance="provider_exchange_schema:model",
    )


def summarize_provider_exchange_schema(
    schema: ProviderExchangeSchema,
) -> dict[str, object]:
    return {
        "schema_id": schema.schema_id,
        "mode": schema.mode.value,
        "title": schema.title,
        "source_cloud_preflight_id": schema.source_cloud_preflight_id,
        "request_schema_id": schema.request_schema.request_schema_id,
        "response_schema_id": schema.response_schema.response_schema_id,
        "required_review_count": len(schema.required_reviews),
        "blocked_action_count": len(schema.blocked_actions),
        "allowed_capability_count": len(schema.request_schema.allowed_capabilities),
        "disallowed_capability_count": len(schema.request_schema.disallowed_capabilities),
        "validation_check_count": len(schema.response_schema.validation_checks),
        "provider_call_performed": schema.provider_call_performed,
        "secrets_loaded": schema.secrets_loaded,
        "network_access_performed": schema.network_access_performed,
        "prompt_sent_to_provider": schema.prompt_sent_to_provider,
        "raw_provider_response_stored": schema.raw_provider_response_stored,
        "remediation_performed": schema.remediation_performed,
        "notifications_sent": schema.notifications_sent,
        "benchmark_scoring_performed": schema.benchmark_scoring_performed,
        "benchmark_truth_updated": schema.benchmark_truth_updated,
        "autonomous_remediation_allowed": schema.autonomous_remediation_allowed,
        "human_review_required": schema.human_review_required,
    }


def to_view_model(schema: ProviderExchangeSchema) -> dict[str, Any]:
    return {
        "summary": summarize_provider_exchange_schema(schema),
        "request_schema": {
            "request_schema_id": schema.request_schema.request_schema_id,
            "request_purpose": schema.request_schema.request_purpose.value,
            "business_outcome": schema.request_schema.business_outcome,
            "scenario_id": schema.request_schema.scenario_id,
            "evidence_refs": list(schema.request_schema.evidence_refs),
            "allowed_capabilities": list(schema.request_schema.allowed_capabilities),
            "disallowed_capabilities": list(schema.request_schema.disallowed_capabilities),
            "data_classification": schema.request_schema.data_classification.value,
            "audit_correlation_id_required": schema.request_schema.audit_correlation_id_required,
            "human_review_required": schema.request_schema.human_review_required,
            "benchmark_truth_isolated": schema.request_schema.benchmark_truth_isolated,
            "provenance": schema.request_schema.provenance,
        },
        "response_schema": {
            "response_schema_id": schema.response_schema.response_schema_id,
            "request_schema_id": schema.response_schema.request_schema_id,
            "validation_status": schema.response_schema.validation_status.value,
            "required_fields": list(schema.response_schema.required_fields),
            "validation_checks": list(schema.response_schema.validation_checks),
            "blocked_response_patterns": list(schema.response_schema.blocked_response_patterns),
            "citations_required": schema.response_schema.citations_required,
            "raw_response_storage_allowed": schema.response_schema.raw_response_storage_allowed,
            "provider_output_accepted": schema.response_schema.provider_output_accepted,
            "human_review_required": schema.response_schema.human_review_required,
            "provenance": schema.response_schema.provenance,
        },
        "required_reviews": list(schema.required_reviews),
        "blocked_actions": list(schema.blocked_actions),
        "cloud_preflight_summary": schema.cloud_preflight_summary,
        "provenance": schema.provenance,
    }
