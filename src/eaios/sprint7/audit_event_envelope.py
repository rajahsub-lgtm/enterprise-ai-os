"""Sprint 7 audit event envelope.

Review-only audit event envelope for EAIOS Sprint 7 decisions.

It does not call connectors, execute tools, perform writes, load secrets, access
external networks, execute remediation, send notifications, score benchmarks,
update benchmark truth, or enable autonomous remediation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint7.mcp_connector_permission_classifier import (
    ConnectorPermissionDecision,
    classify_mcp_connector_permissions,
    summarize_mcp_connector_permission_classifier_report,
)


class AuditEventEnvelopeMode(str, Enum):
    REVIEW_ONLY_AUDIT_ENVELOPE = "REVIEW_ONLY_AUDIT_ENVELOPE"


class AuditEventType(str, Enum):
    GOVERNANCE_BOUNDARY_RECORDED = "GOVERNANCE_BOUNDARY_RECORDED"
    CONNECTOR_PERMISSION_CLASSIFIED = "CONNECTOR_PERMISSION_CLASSIFIED"
    READ_ONLY_REVIEW_ALLOWED = "READ_ONLY_REVIEW_ALLOWED"
    WRITE_OPERATION_BLOCKED = "WRITE_OPERATION_BLOCKED"
    BENCHMARK_OPERATION_BLOCKED = "BENCHMARK_OPERATION_BLOCKED"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"


class AuditEventSeverity(str, Enum):
    INFO = "INFO"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    BLOCKING = "BLOCKING"


@dataclass(frozen=True)
class AuditEvent:
    event_id: str
    event_type: AuditEventType
    severity: AuditEventSeverity
    subject_id: str
    subject_type: str
    decision: str
    message: str
    evidence_refs: tuple[str, ...]
    blocked_actions: tuple[str, ...]
    human_review_required: bool
    provenance: str


@dataclass(frozen=True)
class AuditEventEnvelope:
    envelope_id: str
    mode: AuditEventEnvelopeMode
    title: str
    source_classifier_id: str
    events: tuple[AuditEvent, ...]
    required_reviews: tuple[str, ...]
    blocked_actions: tuple[str, ...]
    classifier_summary: dict[str, object]
    envelope_built: bool
    audit_events_persisted: bool
    real_connector_calls_performed: bool
    external_writes_performed: bool
    production_records_modified: bool
    infrastructure_changed: bool
    secrets_loaded: bool
    network_access_performed: bool
    remediation_performed: bool
    notifications_sent: bool
    benchmark_scoring_performed: bool
    benchmark_truth_updated: bool
    autonomous_remediation_allowed: bool
    human_review_required: bool
    provenance: str


def build_audit_event_envelope() -> AuditEventEnvelope:
    classifier_report = classify_mcp_connector_permissions()
    classifier_summary = summarize_mcp_connector_permission_classifier_report(
        classifier_report
    )

    events: list[AuditEvent] = [
        AuditEvent(
            event_id="audit-event-001-governance-boundary",
            event_type=AuditEventType.GOVERNANCE_BOUNDARY_RECORDED,
            severity=AuditEventSeverity.REVIEW_REQUIRED,
            subject_id="sprint7-runtime-hardening",
            subject_type="governance_boundary",
            decision="REVIEW_ONLY",
            message="Sprint 7 audit envelope records decisions without executing actions.",
            evidence_refs=("docs/EAIOS_2_SPRINT_6_CLOSEOUT.md",),
            blocked_actions=classifier_report.blocked_actions,
            human_review_required=True,
            provenance="audit_event_envelope:event",
        )
    ]

    for index, classification in enumerate(classifier_report.classifications, start=2):
        if classification.decision == ConnectorPermissionDecision.ALLOW_READ_ONLY_REVIEW:
            event_type = AuditEventType.READ_ONLY_REVIEW_ALLOWED
            severity = AuditEventSeverity.INFO
            blocked_actions = ("call_real_connector", "perform_external_write")
        elif classification.benchmark_operation_blocked:
            event_type = AuditEventType.BENCHMARK_OPERATION_BLOCKED
            severity = AuditEventSeverity.BLOCKING
            blocked_actions = (
                "score_benchmark_from_connector_output",
                "update_benchmark_truth_from_connector_output",
            )
        elif classification.write_blocked:
            event_type = AuditEventType.WRITE_OPERATION_BLOCKED
            severity = AuditEventSeverity.BLOCKING
            blocked_actions = (
                "perform_external_write",
                "modify_production_record",
                "execute_tool_action",
            )
        else:
            event_type = AuditEventType.CONNECTOR_PERMISSION_CLASSIFIED
            severity = AuditEventSeverity.REVIEW_REQUIRED
            blocked_actions = ("call_real_connector", "execute_tool_action")

        events.append(
            AuditEvent(
                event_id=f"audit-event-{index:03d}-{classification.connector_id}",
                event_type=event_type,
                severity=severity,
                subject_id=classification.connector_id,
                subject_type="mcp_connector",
                decision=classification.decision.value,
                message=(
                    f"Connector {classification.connector_name} classified as "
                    f"{classification.decision.value}."
                ),
                evidence_refs=(
                    "src/eaios/sprint7/mcp_connector_inventory_schema.py",
                    "src/eaios/sprint7/mcp_connector_permission_classifier.py",
                ),
                blocked_actions=blocked_actions,
                human_review_required=True,
                provenance="audit_event_envelope:event",
            )
        )

    events.append(
        AuditEvent(
            event_id="audit-event-999-human-review-required",
            event_type=AuditEventType.HUMAN_REVIEW_REQUIRED,
            severity=AuditEventSeverity.REVIEW_REQUIRED,
            subject_id="sprint7-human-review-boundary",
            subject_type="approval_boundary",
            decision="HUMAN_REVIEW_REQUIRED",
            message="All high-risk provider, connector, benchmark, and remediation actions require human review.",
            evidence_refs=("docs/EAIOS_2_SPRINT_6_CLOSEOUT.md",),
            blocked_actions=(
                "bypass_human_review",
                "enable_autonomous_remediation",
                "execute_remediation",
                "send_notification",
            ),
            human_review_required=True,
            provenance="audit_event_envelope:event",
        )
    )

    return AuditEventEnvelope(
        envelope_id="sprint7-audit-event-envelope-001",
        mode=AuditEventEnvelopeMode.REVIEW_ONLY_AUDIT_ENVELOPE,
        title="EAIOS Sprint 7 Audit Event Envelope",
        source_classifier_id=str(classifier_summary["classifier_id"]),
        events=tuple(events),
        required_reviews=(
            "audit_event_schema_review",
            "audit_trace_review",
            "connector_permission_review",
            "human_approval_workflow_review",
            "benchmark_truth_isolation_review",
        ),
        blocked_actions=(
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
        ),
        classifier_summary=classifier_summary,
        envelope_built=True,
        audit_events_persisted=False,
        real_connector_calls_performed=False,
        external_writes_performed=False,
        production_records_modified=False,
        infrastructure_changed=False,
        secrets_loaded=False,
        network_access_performed=False,
        remediation_performed=False,
        notifications_sent=False,
        benchmark_scoring_performed=False,
        benchmark_truth_updated=False,
        autonomous_remediation_allowed=False,
        human_review_required=True,
        provenance="audit_event_envelope:model",
    )


def summarize_audit_event_envelope(envelope: AuditEventEnvelope) -> dict[str, object]:
    blocking_count = sum(
        1 for event in envelope.events if event.severity == AuditEventSeverity.BLOCKING
    )
    review_required_count = sum(
        1
        for event in envelope.events
        if event.severity == AuditEventSeverity.REVIEW_REQUIRED
    )

    return {
        "envelope_id": envelope.envelope_id,
        "mode": envelope.mode.value,
        "title": envelope.title,
        "source_classifier_id": envelope.source_classifier_id,
        "event_count": len(envelope.events),
        "blocking_event_count": blocking_count,
        "review_required_event_count": review_required_count,
        "required_review_count": len(envelope.required_reviews),
        "blocked_action_count": len(envelope.blocked_actions),
        "envelope_built": envelope.envelope_built,
        "audit_events_persisted": envelope.audit_events_persisted,
        "real_connector_calls_performed": envelope.real_connector_calls_performed,
        "external_writes_performed": envelope.external_writes_performed,
        "production_records_modified": envelope.production_records_modified,
        "infrastructure_changed": envelope.infrastructure_changed,
        "secrets_loaded": envelope.secrets_loaded,
        "network_access_performed": envelope.network_access_performed,
        "remediation_performed": envelope.remediation_performed,
        "notifications_sent": envelope.notifications_sent,
        "benchmark_scoring_performed": envelope.benchmark_scoring_performed,
        "benchmark_truth_updated": envelope.benchmark_truth_updated,
        "autonomous_remediation_allowed": envelope.autonomous_remediation_allowed,
        "human_review_required": envelope.human_review_required,
    }


def to_view_model(envelope: AuditEventEnvelope) -> dict[str, Any]:
    return {
        "summary": summarize_audit_event_envelope(envelope),
        "events": [
            {
                "event_id": event.event_id,
                "event_type": event.event_type.value,
                "severity": event.severity.value,
                "subject_id": event.subject_id,
                "subject_type": event.subject_type,
                "decision": event.decision,
                "message": event.message,
                "evidence_refs": list(event.evidence_refs),
                "blocked_actions": list(event.blocked_actions),
                "human_review_required": event.human_review_required,
                "provenance": event.provenance,
            }
            for event in envelope.events
        ],
        "required_reviews": list(envelope.required_reviews),
        "blocked_actions": list(envelope.blocked_actions),
        "classifier_summary": envelope.classifier_summary,
        "provenance": envelope.provenance,
    }
