"""Sprint 7 provider output validator.

This module validates hypothetical provider output against the Sprint 7 provider
exchange schema.

It does not call providers, load secrets, access external networks, send
prompts, store raw provider responses, execute remediation, send notifications,
score benchmarks, update benchmark truth, or enable autonomous remediation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from eaios.sprint7.provider_exchange_schema import (
    ProviderExchangeSchema,
    build_provider_exchange_schema,
    summarize_provider_exchange_schema,
)


class ProviderOutputValidatorMode(str, Enum):
    REVIEW_ONLY_VALIDATOR = "REVIEW_ONLY_VALIDATOR"


class ProviderOutputDecision(str, Enum):
    BLOCKED_PENDING_HUMAN_REVIEW = "BLOCKED_PENDING_HUMAN_REVIEW"
    BLOCKED_VALIDATION_ISSUES = "BLOCKED_VALIDATION_ISSUES"


class ProviderOutputIssueSeverity(str, Enum):
    BLOCKING = "BLOCKING"
    WARNING = "WARNING"


class ProviderOutputIssueType(str, Enum):
    MISSING_REQUIRED_FIELD = "MISSING_REQUIRED_FIELD"
    EVIDENCE_REFERENCE_MISSING = "EVIDENCE_REFERENCE_MISSING"
    HUMAN_REVIEW_MISSING = "HUMAN_REVIEW_MISSING"
    UNSUPPORTED_ACTION_REQUEST = "UNSUPPORTED_ACTION_REQUEST"
    BENCHMARK_TRUTH_CLAIM = "BENCHMARK_TRUTH_CLAIM"
    BENCHMARK_SCORING_ATTEMPT = "BENCHMARK_SCORING_ATTEMPT"
    REMEDIATION_INSTRUCTION = "REMEDIATION_INSTRUCTION"
    NOTIFICATION_INSTRUCTION = "NOTIFICATION_INSTRUCTION"
    SECRET_EXPOSURE_RISK = "SECRET_EXPOSURE_RISK"
    UNSAFE_CERTAINTY = "UNSAFE_CERTAINTY"


@dataclass(frozen=True)
class ProviderOutputValidationIssue:
    issue_id: str
    issue_type: ProviderOutputIssueType
    severity: ProviderOutputIssueSeverity
    message: str
    field: str
    provenance: str


@dataclass(frozen=True)
class ProviderOutputValidationResult:
    validation_id: str
    mode: ProviderOutputValidatorMode
    source_provider_schema_id: str
    decision: ProviderOutputDecision
    issues: tuple[ProviderOutputValidationIssue, ...]
    required_fields_checked: tuple[str, ...]
    validation_checks_performed: tuple[str, ...]
    blocked_actions: tuple[str, ...]
    provider_exchange_summary: dict[str, object]
    validation_performed: bool
    provider_call_performed: bool
    secrets_loaded: bool
    network_access_performed: bool
    prompt_sent_to_provider: bool
    raw_provider_response_stored: bool
    provider_output_accepted: bool
    remediation_performed: bool
    notifications_sent: bool
    benchmark_scoring_performed: bool
    benchmark_truth_updated: bool
    autonomous_remediation_allowed: bool
    human_review_required: bool
    provenance: str


def validate_provider_output(
    provider_output: Mapping[str, Any],
    schema: ProviderExchangeSchema | None = None,
) -> ProviderOutputValidationResult:
    exchange_schema = schema or build_provider_exchange_schema()
    exchange_summary = summarize_provider_exchange_schema(exchange_schema)

    issues = _collect_validation_issues(provider_output, exchange_schema)

    decision = (
        ProviderOutputDecision.BLOCKED_VALIDATION_ISSUES
        if issues
        else ProviderOutputDecision.BLOCKED_PENDING_HUMAN_REVIEW
    )

    return ProviderOutputValidationResult(
        validation_id="sprint7-provider-output-validation-001",
        mode=ProviderOutputValidatorMode.REVIEW_ONLY_VALIDATOR,
        source_provider_schema_id=exchange_schema.schema_id,
        decision=decision,
        issues=issues,
        required_fields_checked=exchange_schema.response_schema.required_fields,
        validation_checks_performed=exchange_schema.response_schema.validation_checks,
        blocked_actions=(
            "accept_unvalidated_provider_output",
            "store_raw_provider_response",
            "display_provider_output_without_human_review",
            "execute_provider_suggested_action",
            "send_provider_suggested_notification",
            "score_benchmark_from_provider_output",
            "update_benchmark_truth_from_provider_output",
            "enable_autonomous_remediation",
            "bypass_human_review",
        ),
        provider_exchange_summary=exchange_summary,
        validation_performed=True,
        provider_call_performed=False,
        secrets_loaded=False,
        network_access_performed=False,
        prompt_sent_to_provider=False,
        raw_provider_response_stored=False,
        provider_output_accepted=False,
        remediation_performed=False,
        notifications_sent=False,
        benchmark_scoring_performed=False,
        benchmark_truth_updated=False,
        autonomous_remediation_allowed=False,
        human_review_required=True,
        provenance="provider_output_validator:result",
    )


def summarize_provider_output_validation(
    result: ProviderOutputValidationResult,
) -> dict[str, object]:
    return {
        "validation_id": result.validation_id,
        "mode": result.mode.value,
        "source_provider_schema_id": result.source_provider_schema_id,
        "decision": result.decision.value,
        "issue_count": len(result.issues),
        "required_field_count": len(result.required_fields_checked),
        "validation_check_count": len(result.validation_checks_performed),
        "blocked_action_count": len(result.blocked_actions),
        "validation_performed": result.validation_performed,
        "provider_call_performed": result.provider_call_performed,
        "secrets_loaded": result.secrets_loaded,
        "network_access_performed": result.network_access_performed,
        "prompt_sent_to_provider": result.prompt_sent_to_provider,
        "raw_provider_response_stored": result.raw_provider_response_stored,
        "provider_output_accepted": result.provider_output_accepted,
        "remediation_performed": result.remediation_performed,
        "notifications_sent": result.notifications_sent,
        "benchmark_scoring_performed": result.benchmark_scoring_performed,
        "benchmark_truth_updated": result.benchmark_truth_updated,
        "autonomous_remediation_allowed": result.autonomous_remediation_allowed,
        "human_review_required": result.human_review_required,
    }


def to_view_model(result: ProviderOutputValidationResult) -> dict[str, Any]:
    return {
        "summary": summarize_provider_output_validation(result),
        "issues": [
            {
                "issue_id": issue.issue_id,
                "issue_type": issue.issue_type.value,
                "severity": issue.severity.value,
                "message": issue.message,
                "field": issue.field,
                "provenance": issue.provenance,
            }
            for issue in result.issues
        ],
        "required_fields_checked": list(result.required_fields_checked),
        "validation_checks_performed": list(result.validation_checks_performed),
        "blocked_actions": list(result.blocked_actions),
        "provider_exchange_summary": result.provider_exchange_summary,
        "provenance": result.provenance,
    }


def _collect_validation_issues(
    provider_output: Mapping[str, Any],
    schema: ProviderExchangeSchema,
) -> tuple[ProviderOutputValidationIssue, ...]:
    issues: list[ProviderOutputValidationIssue] = []

    for field in schema.response_schema.required_fields:
        if field not in provider_output:
            issues.append(
                _issue(
                    issue_type=ProviderOutputIssueType.MISSING_REQUIRED_FIELD,
                    message=f"Missing required field: {field}",
                    field=field,
                    index=len(issues) + 1,
                )
            )

    evidence_refs = provider_output.get("evidence_refs")
    if not evidence_refs:
        issues.append(
            _issue(
                issue_type=ProviderOutputIssueType.EVIDENCE_REFERENCE_MISSING,
                message="Provider output must include evidence references.",
                field="evidence_refs",
                index=len(issues) + 1,
            )
        )

    if provider_output.get("human_review_required") is not True:
        issues.append(
            _issue(
                issue_type=ProviderOutputIssueType.HUMAN_REVIEW_MISSING,
                message="Provider output must preserve human review.",
                field="human_review_required",
                index=len(issues) + 1,
            )
        )

    corpus = _flatten_text(provider_output)

    pattern_groups: tuple[tuple[ProviderOutputIssueType, str, tuple[str, ...]], ...] = (
        (
            ProviderOutputIssueType.UNSUPPORTED_ACTION_REQUEST,
            "Provider output requested an unsupported action.",
            (
                "call tools",
                "modify records",
                "write production",
                "bypass human review",
            ),
        ),
        (
            ProviderOutputIssueType.BENCHMARK_TRUTH_CLAIM,
            "Provider output attempted to define or modify benchmark truth.",
            (
                "define benchmark truth",
                "modify benchmark truth",
                "update benchmark truth",
                "benchmark truth is",
            ),
        ),
        (
            ProviderOutputIssueType.BENCHMARK_SCORING_ATTEMPT,
            "Provider output attempted benchmark scoring.",
            (
                "score benchmark",
                "benchmark score",
                "scored benchmark",
                "benchmark scoring",
            ),
        ),
        (
            ProviderOutputIssueType.REMEDIATION_INSTRUCTION,
            "Provider output included remediation instructions.",
            (
                "restart service",
                "execute remediation",
                "apply fix",
                "rollback production",
            ),
        ),
        (
            ProviderOutputIssueType.NOTIFICATION_INSTRUCTION,
            "Provider output included notification instructions.",
            (
                "send notification",
                "email users",
                "page team",
                "notify customers",
            ),
        ),
        (
            ProviderOutputIssueType.SECRET_EXPOSURE_RISK,
            "Provider output appears to expose secret material.",
            (
                "api" + "_key",
                "pass" + "word",
                "bear" + "er ",
                "secret token",
            ),
        ),
        (
            ProviderOutputIssueType.UNSAFE_CERTAINTY,
            "Provider output used unsafe certainty.",
            (
                "100% certain",
                "definitely the root cause",
                "no human review needed",
                "safe to execute now",
            ),
        ),
    )

    for issue_type, message, patterns in pattern_groups:
        if any(pattern in corpus for pattern in patterns):
            issues.append(
                _issue(
                    issue_type=issue_type,
                    message=message,
                    field="provider_output",
                    index=len(issues) + 1,
                )
            )

    return tuple(issues)


def _issue(
    issue_type: ProviderOutputIssueType,
    message: str,
    field: str,
    index: int,
) -> ProviderOutputValidationIssue:
    return ProviderOutputValidationIssue(
        issue_id=f"provider-output-issue-{index:03d}",
        issue_type=issue_type,
        severity=ProviderOutputIssueSeverity.BLOCKING,
        message=message,
        field=field,
        provenance="provider_output_validator:issue",
    )


def _flatten_text(value: Any) -> str:
    if isinstance(value, Mapping):
        return " ".join(_flatten_text(item) for item in value.values()).lower()
    if isinstance(value, (list, tuple, set)):
        return " ".join(_flatten_text(item) for item in value).lower()
    return str(value).lower()
