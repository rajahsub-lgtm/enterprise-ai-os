from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint7.provider_exchange_schema import (
    ProviderDataClassification,
    ProviderExchangeMode,
    ProviderRequestPurpose,
    ProviderValidationStatus,
    build_provider_exchange_schema,
    summarize_provider_exchange_schema,
    to_view_model,
)


def _schema():
    return build_provider_exchange_schema()


def test_provider_exchange_schema_builds_review_only_schema():
    schema = _schema()

    assert schema.schema_id == "sprint7-provider-exchange-schema-001"
    assert schema.mode == ProviderExchangeMode.REVIEW_ONLY_SCHEMA
    assert schema.title == "EAIOS Provider Request and Response Schema"
    assert schema.source_cloud_preflight_id == "sprint7-cloud-deploy-preflight-001"
    assert schema.provenance == "provider_exchange_schema:model"


def test_provider_request_schema_declares_scope_and_boundaries():
    request = _schema().request_schema

    assert request.request_schema_id == "sprint7-provider-request-schema-001"
    assert request.request_purpose == ProviderRequestPurpose.ROOT_CAUSE_REVIEW
    assert request.business_outcome == "Maintain Application Health"
    assert request.scenario_id == "application-health-read-only-review"
    assert request.data_classification == ProviderDataClassification.SYNTHETIC_OPERATIONAL_EVIDENCE
    assert request.audit_correlation_id_required is True
    assert request.human_review_required is True
    assert request.benchmark_truth_isolated is True
    assert request.provider_call_performed is False
    assert request.secrets_loaded is False
    assert request.network_access_performed is False
    assert request.prompt_sent_to_provider is False
    assert request.provenance == "provider_exchange_schema:request"


def test_provider_request_schema_capabilities_are_explicit():
    request = _schema().request_schema

    assert request.allowed_capabilities == (
        "summarize_evidence",
        "identify_risks",
        "draft_operator_explanation",
        "draft_human_review_questions",
    )

    assert request.disallowed_capabilities == (
        "define_benchmark_truth",
        "score_benchmark_results",
        "execute_remediation",
        "send_notification",
        "modify_records",
        "call_tools",
        "bypass_human_review",
    )


def test_provider_response_schema_declares_validation_requirements():
    response = _schema().response_schema

    assert response.response_schema_id == "sprint7-provider-response-schema-001"
    assert response.request_schema_id == "sprint7-provider-request-schema-001"
    assert response.validation_status == ProviderValidationStatus.BLOCKED_PENDING_VALIDATION
    assert response.citations_required is True
    assert response.raw_response_storage_allowed is False
    assert response.provider_output_accepted is False
    assert response.benchmark_truth_claimed is False
    assert response.benchmark_scoring_attempted is False
    assert response.remediation_instruction_present is False
    assert response.notification_instruction_present is False
    assert response.secret_leakage_detected is False
    assert response.unsupported_action_requested is False
    assert response.human_review_required is True
    assert response.provenance == "provider_exchange_schema:response"


def test_provider_response_schema_required_fields_checks_and_blocks_are_explicit():
    response = _schema().response_schema

    assert response.required_fields == (
        "response_id",
        "request_schema_id",
        "summary",
        "evidence_refs",
        "risk_flags",
        "confidence_statement",
        "human_review_required",
        "blocked_actions",
    )

    assert response.validation_checks == (
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

    assert response.blocked_response_patterns == (
        "benchmark_truth_claim",
        "benchmark_scoring_attempt",
        "autonomous_action_request",
        "production_write_instruction",
        "notification_send_instruction",
        "secret_exposure",
        "tool_execution_instruction",
        "human_review_bypass",
    )


def test_provider_exchange_schema_required_reviews_are_explicit():
    schema = _schema()

    assert schema.required_reviews == (
        "provider_request_schema_review",
        "provider_response_schema_review",
        "provider_output_validation_review",
        "secret_handling_review",
        "network_access_review",
        "benchmark_truth_isolation_review",
        "human_approval_workflow_review",
    )


def test_provider_exchange_schema_blocked_actions_are_explicit():
    schema = _schema()

    assert schema.blocked_actions == (
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


def test_provider_exchange_schema_preserves_no_execution_boundaries():
    schema = _schema()

    assert schema.provider_call_performed is False
    assert schema.secrets_loaded is False
    assert schema.network_access_performed is False
    assert schema.prompt_sent_to_provider is False
    assert schema.raw_provider_response_stored is False
    assert schema.remediation_performed is False
    assert schema.notifications_sent is False
    assert schema.benchmark_scoring_performed is False
    assert schema.benchmark_truth_updated is False
    assert schema.autonomous_remediation_allowed is False
    assert schema.human_review_required is True


def test_provider_exchange_schema_embeds_cloud_preflight_summary():
    schema = _schema()

    assert schema.cloud_preflight_summary["preflight_id"] == (
        "sprint7-cloud-deploy-preflight-001"
    )
    assert schema.cloud_preflight_summary["mode"] == "REVIEW_ONLY_PREFLIGHT"
    assert schema.cloud_preflight_summary["deployment_commands_executed"] is False
    assert schema.cloud_preflight_summary["human_review_required"] is True


def test_provider_exchange_schema_summary_is_view_ready():
    schema = _schema()

    assert summarize_provider_exchange_schema(schema) == {
        "schema_id": "sprint7-provider-exchange-schema-001",
        "mode": "REVIEW_ONLY_SCHEMA",
        "title": "EAIOS Provider Request and Response Schema",
        "source_cloud_preflight_id": "sprint7-cloud-deploy-preflight-001",
        "request_schema_id": "sprint7-provider-request-schema-001",
        "response_schema_id": "sprint7-provider-response-schema-001",
        "required_review_count": 7,
        "blocked_action_count": 12,
        "allowed_capability_count": 4,
        "disallowed_capability_count": 7,
        "validation_check_count": 10,
        "provider_call_performed": False,
        "secrets_loaded": False,
        "network_access_performed": False,
        "prompt_sent_to_provider": False,
        "raw_provider_response_stored": False,
        "remediation_performed": False,
        "notifications_sent": False,
        "benchmark_scoring_performed": False,
        "benchmark_truth_updated": False,
        "autonomous_remediation_allowed": False,
        "human_review_required": True,
    }


def test_provider_exchange_schema_view_model_is_json_serializable():
    schema = _schema()

    serialized = json.dumps(to_view_model(schema), indent=2)

    assert "sprint7-provider-exchange-schema-001" in serialized
    assert "sprint7-provider-request-schema-001" in serialized
    assert "sprint7-provider-response-schema-001" in serialized
    assert "score_benchmark_from_provider_output" in serialized


def test_provider_exchange_schema_module_does_not_call_provider_or_network():
    source = Path("src/eaios/sprint7/provider_exchange_schema.py").read_text(
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
