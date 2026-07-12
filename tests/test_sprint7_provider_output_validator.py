from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint7.provider_output_validator import (
    ProviderOutputDecision,
    ProviderOutputIssueSeverity,
    ProviderOutputIssueType,
    ProviderOutputValidatorMode,
    summarize_provider_output_validation,
    to_view_model,
    validate_provider_output,
)


def _clean_output():
    return {
        "response_id": "provider-response-001",
        "request_schema_id": "sprint7-provider-request-schema-001",
        "summary": "Synthetic evidence suggests a possible application-health risk.",
        "evidence_refs": ["docs/EAIOS_2_SPRINT_6_CLOSEOUT.md"],
        "risk_flags": ["requires_operator_review"],
        "confidence_statement": "Moderate confidence based on synthetic evidence.",
        "human_review_required": True,
        "blocked_actions": ["execute_remediation", "send_notification"],
    }


def test_provider_output_validator_accepts_clean_shape_but_blocks_pending_human_review():
    result = validate_provider_output(_clean_output())

    assert result.validation_id == "sprint7-provider-output-validation-001"
    assert result.mode == ProviderOutputValidatorMode.REVIEW_ONLY_VALIDATOR
    assert result.source_provider_schema_id == "sprint7-provider-exchange-schema-001"
    assert result.decision == ProviderOutputDecision.BLOCKED_PENDING_HUMAN_REVIEW
    assert result.issues == ()
    assert result.validation_performed is True
    assert result.provider_output_accepted is False
    assert result.human_review_required is True
    assert result.provenance == "provider_output_validator:result"


def test_provider_output_validator_detects_missing_required_fields():
    result = validate_provider_output({"summary": "Only a summary."})

    issue_types = tuple(issue.issue_type for issue in result.issues)

    assert result.decision == ProviderOutputDecision.BLOCKED_VALIDATION_ISSUES
    assert ProviderOutputIssueType.MISSING_REQUIRED_FIELD in issue_types
    assert ProviderOutputIssueType.EVIDENCE_REFERENCE_MISSING in issue_types
    assert ProviderOutputIssueType.HUMAN_REVIEW_MISSING in issue_types


def test_provider_output_validator_detects_unsafe_provider_output_patterns():
    output = {
        "response_id": "provider-response-unsafe",
        "request_schema_id": "sprint7-provider-request-schema-001",
        "summary": (
            "This can define benchmark truth and score benchmark results. "
            "Restart service and send notification. It is 100% certain."
        ),
        "evidence_refs": ["docs/EAIOS_2_SPRINT_6_CLOSEOUT.md"],
        "risk_flags": ["unsafe"],
        "confidence_statement": "Definitely the root cause.",
        "human_review_required": False,
        "blocked_actions": [],
    }

    result = validate_provider_output(output)
    issue_types = {issue.issue_type for issue in result.issues}

    assert result.decision == ProviderOutputDecision.BLOCKED_VALIDATION_ISSUES
    assert ProviderOutputIssueType.HUMAN_REVIEW_MISSING in issue_types
    assert ProviderOutputIssueType.BENCHMARK_TRUTH_CLAIM in issue_types
    assert ProviderOutputIssueType.BENCHMARK_SCORING_ATTEMPT in issue_types
    assert ProviderOutputIssueType.REMEDIATION_INSTRUCTION in issue_types
    assert ProviderOutputIssueType.NOTIFICATION_INSTRUCTION in issue_types
    assert ProviderOutputIssueType.UNSAFE_CERTAINTY in issue_types


def test_provider_output_validator_issues_are_blocking_and_provenanced():
    result = validate_provider_output({})

    assert len(result.issues) >= 3

    for issue in result.issues:
        assert issue.issue_id.startswith("provider-output-issue-")
        assert issue.severity == ProviderOutputIssueSeverity.BLOCKING
        assert issue.message
        assert issue.field
        assert issue.provenance == "provider_output_validator:issue"


def test_provider_output_validator_checks_schema_fields_and_validation_checks():
    result = validate_provider_output(_clean_output())

    assert result.required_fields_checked == (
        "response_id",
        "request_schema_id",
        "summary",
        "evidence_refs",
        "risk_flags",
        "confidence_statement",
        "human_review_required",
        "blocked_actions",
    )

    assert result.validation_checks_performed == (
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
    )


def test_provider_output_validator_blocked_actions_are_explicit():
    result = validate_provider_output(_clean_output())

    assert result.blocked_actions == (
        "accept_unvalidated_provider_output",
        "store_raw_provider_response",
        "display_provider_output_without_human_review",
        "execute_provider_suggested_action",
        "send_provider_suggested_notification",
        "score_benchmark_from_provider_output",
        "update_benchmark_truth_from_provider_output",
        "enable_autonomous_remediation",
        "bypass_human_review",
    )


def test_provider_output_validator_preserves_no_execution_boundaries():
    result = validate_provider_output(_clean_output())

    assert result.provider_call_performed is False
    assert result.secrets_loaded is False
    assert result.network_access_performed is False
    assert result.prompt_sent_to_provider is False
    assert result.raw_provider_response_stored is False
    assert result.provider_output_accepted is False
    assert result.remediation_performed is False
    assert result.notifications_sent is False
    assert result.benchmark_scoring_performed is False
    assert result.benchmark_truth_updated is False
    assert result.autonomous_remediation_allowed is False
    assert result.human_review_required is True


def test_provider_output_validator_embeds_provider_exchange_summary():
    result = validate_provider_output(_clean_output())

    assert result.provider_exchange_summary["schema_id"] == (
        "sprint7-provider-exchange-schema-001"
    )
    assert result.provider_exchange_summary["mode"] == "REVIEW_ONLY_SCHEMA"
    assert result.provider_exchange_summary["provider_call_performed"] is False
    assert result.provider_exchange_summary["human_review_required"] is True


def test_provider_output_validator_summary_is_view_ready():
    result = validate_provider_output(_clean_output())

    assert summarize_provider_output_validation(result) == {
        "validation_id": "sprint7-provider-output-validation-001",
        "mode": "REVIEW_ONLY_VALIDATOR",
        "source_provider_schema_id": "sprint7-provider-exchange-schema-001",
        "decision": "BLOCKED_PENDING_HUMAN_REVIEW",
        "issue_count": 0,
        "required_field_count": 8,
        "validation_check_count": 10,
        "blocked_action_count": 9,
        "validation_performed": True,
        "provider_call_performed": False,
        "secrets_loaded": False,
        "network_access_performed": False,
        "prompt_sent_to_provider": False,
        "raw_provider_response_stored": False,
        "provider_output_accepted": False,
        "remediation_performed": False,
        "notifications_sent": False,
        "benchmark_scoring_performed": False,
        "benchmark_truth_updated": False,
        "autonomous_remediation_allowed": False,
        "human_review_required": True,
    }


def test_provider_output_validator_view_model_is_json_serializable():
    result = validate_provider_output(_clean_output())

    serialized = json.dumps(to_view_model(result), indent=2)

    assert "sprint7-provider-output-validation-001" in serialized
    assert "BLOCKED_PENDING_HUMAN_REVIEW" in serialized
    assert "score_benchmark_from_provider_output" in serialized
    assert "sprint7-provider-exchange-schema-001" in serialized


def test_provider_output_validator_module_does_not_call_provider_or_network():
    source = Path("src/eaios/sprint7/provider_output_validator.py").read_text(
        encoding="utf-8"
    ).lower()

    assert "subprocess" not in source
    assert "os.system" not in source
    assert "requests.post" not in source
    assert "httpx.post" not in source
    assert "api_key" not in source
    assert "password" not in source
    assert "bearer " not in source
    assert "curl " not in source
    assert "write_text(" not in source
    assert "mkdir(" not in source
    assert "execute_tool(" not in source
    assert "restart_service(" not in source
