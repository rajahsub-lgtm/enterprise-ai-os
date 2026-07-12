from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint7.audit_event_envelope import (
    AuditEventEnvelopeMode,
    AuditEventSeverity,
    AuditEventType,
    build_audit_event_envelope,
    summarize_audit_event_envelope,
    to_view_model,
)


def _envelope():
    return build_audit_event_envelope()


def test_audit_event_envelope_builds_review_only_model():
    envelope = _envelope()

    assert envelope.envelope_id == "sprint7-audit-event-envelope-001"
    assert envelope.mode == AuditEventEnvelopeMode.REVIEW_ONLY_AUDIT_ENVELOPE
    assert envelope.title == "EAIOS Sprint 7 Audit Event Envelope"
    assert envelope.source_classifier_id == (
        "sprint7-mcp-connector-permission-classifier-001"
    )
    assert envelope.provenance == "audit_event_envelope:model"


def test_audit_event_envelope_events_are_declared():
    envelope = _envelope()

    assert len(envelope.events) == 5

    event_ids = tuple(event.event_id for event in envelope.events)
    assert event_ids[0] == "audit-event-001-governance-boundary"
    assert event_ids[-1] == "audit-event-999-human-review-required"

    assert all(event.provenance == "audit_event_envelope:event" for event in envelope.events)
    assert all(event.human_review_required is True for event in envelope.events)


def test_audit_event_envelope_event_types_and_severities_are_explicit():
    envelope = _envelope()

    event_types = tuple(event.event_type for event in envelope.events)
    severities = tuple(event.severity for event in envelope.events)

    assert event_types == (
        AuditEventType.GOVERNANCE_BOUNDARY_RECORDED,
        AuditEventType.READ_ONLY_REVIEW_ALLOWED,
        AuditEventType.READ_ONLY_REVIEW_ALLOWED,
        AuditEventType.WRITE_OPERATION_BLOCKED,
        AuditEventType.HUMAN_REVIEW_REQUIRED,
    )

    assert severities == (
        AuditEventSeverity.REVIEW_REQUIRED,
        AuditEventSeverity.INFO,
        AuditEventSeverity.INFO,
        AuditEventSeverity.BLOCKING,
        AuditEventSeverity.REVIEW_REQUIRED,
    )


def test_audit_event_envelope_records_connector_decisions():
    envelope = _envelope()

    connector_events = [
        event for event in envelope.events if event.subject_type == "mcp_connector"
    ]

    assert len(connector_events) == 3

    decisions = tuple(event.decision for event in connector_events)
    assert decisions == (
        "ALLOW_READ_ONLY_REVIEW",
        "ALLOW_READ_ONLY_REVIEW",
        "BLOCK_PRODUCTION_WRITE",
    )

    assert connector_events[0].subject_id == "mcp-connector-servicenow-incident-read-001"
    assert connector_events[1].subject_id == "mcp-connector-observability-alert-read-001"
    assert connector_events[2].subject_id == "mcp-connector-change-write-001"


def test_audit_event_envelope_required_reviews_and_blocks_are_explicit():
    envelope = _envelope()

    assert envelope.required_reviews == (
        "audit_event_schema_review",
        "audit_trace_review",
        "connector_permission_review",
        "human_approval_workflow_review",
        "benchmark_truth_isolation_review",
    )

    assert envelope.blocked_actions == (
        "persist_audit_events_to_external_store",
        "call_real_connector",
        "execute_tool_action",
        "perform_external_write",
        "modify_production_record",
        "change_infrastructure",
        "send_notification",
        "load_secret_material",
        "access_external_network",
        "score_benchmark_from_audit_event",
        "update_benchmark_truth_from_audit_event",
        "enable_autonomous_remediation",
        "bypass_human_review",
    )


def test_audit_event_envelope_preserves_no_execution_boundaries():
    envelope = _envelope()

    assert envelope.envelope_built is True
    assert envelope.audit_events_persisted is False
    assert envelope.real_connector_calls_performed is False
    assert envelope.external_writes_performed is False
    assert envelope.production_records_modified is False
    assert envelope.infrastructure_changed is False
    assert envelope.secrets_loaded is False
    assert envelope.network_access_performed is False
    assert envelope.remediation_performed is False
    assert envelope.notifications_sent is False
    assert envelope.benchmark_scoring_performed is False
    assert envelope.benchmark_truth_updated is False
    assert envelope.autonomous_remediation_allowed is False
    assert envelope.human_review_required is True


def test_audit_event_envelope_embeds_classifier_summary():
    envelope = _envelope()

    assert envelope.classifier_summary["classifier_id"] == (
        "sprint7-mcp-connector-permission-classifier-001"
    )
    assert envelope.classifier_summary["mode"] == "REVIEW_ONLY_CLASSIFIER"
    assert envelope.classifier_summary["real_connector_calls_performed"] is False
    assert envelope.classifier_summary["human_review_required"] is True


def test_audit_event_envelope_summary_is_view_ready():
    envelope = _envelope()

    assert summarize_audit_event_envelope(envelope) == {
        "envelope_id": "sprint7-audit-event-envelope-001",
        "mode": "REVIEW_ONLY_AUDIT_ENVELOPE",
        "title": "EAIOS Sprint 7 Audit Event Envelope",
        "source_classifier_id": "sprint7-mcp-connector-permission-classifier-001",
        "event_count": 5,
        "blocking_event_count": 1,
        "review_required_event_count": 2,
        "required_review_count": 5,
        "blocked_action_count": 13,
        "envelope_built": True,
        "audit_events_persisted": False,
        "real_connector_calls_performed": False,
        "external_writes_performed": False,
        "production_records_modified": False,
        "infrastructure_changed": False,
        "secrets_loaded": False,
        "network_access_performed": False,
        "remediation_performed": False,
        "notifications_sent": False,
        "benchmark_scoring_performed": False,
        "benchmark_truth_updated": False,
        "autonomous_remediation_allowed": False,
        "human_review_required": True,
    }


def test_audit_event_envelope_view_model_is_json_serializable():
    envelope = _envelope()

    serialized = json.dumps(to_view_model(envelope), indent=2)

    assert "sprint7-audit-event-envelope-001" in serialized
    assert "READ_ONLY_REVIEW_ALLOWED" in serialized
    assert "WRITE_OPERATION_BLOCKED" in serialized
    assert "score_benchmark_from_audit_event" in serialized


def test_audit_event_envelope_events_include_evidence_and_blocked_actions():
    envelope = _envelope()

    for event in envelope.events:
        assert event.message
        assert event.evidence_refs
        assert event.blocked_actions
        assert event.human_review_required is True


def test_audit_event_envelope_module_does_not_persist_or_call_external_systems():
    source = Path("src/eaios/sprint7/audit_event_envelope.py").read_text(
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
