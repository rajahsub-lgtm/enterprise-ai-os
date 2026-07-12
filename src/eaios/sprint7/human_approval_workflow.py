"""Sprint 7 human approval workflow model.

Review-only approval workflow for EAIOS Sprint 7 audit events.

It does not approve requests, reject requests, execute actions, persist approval
records, call connectors, perform writes, load secrets, access networks, execute
remediation, send notifications, score benchmarks, update benchmark truth, or
enable autonomous remediation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint7.audit_event_envelope import (
    AuditEvent,
    AuditEventSeverity,
    build_audit_event_envelope,
    summarize_audit_event_envelope,
)


class HumanApprovalWorkflowMode(str, Enum):
    REVIEW_ONLY_WORKFLOW = "REVIEW_ONLY_WORKFLOW"


class ApprovalRequestStatus(str, Enum):
    PENDING_HUMAN_REVIEW = "PENDING_HUMAN_REVIEW"
    BLOCKED_UNTIL_APPROVED = "BLOCKED_UNTIL_APPROVED"


class ApprovalRiskLevel(str, Enum):
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    BLOCKING = "BLOCKING"


class ApprovalActionCategory(str, Enum):
    GOVERNANCE_REVIEW = "GOVERNANCE_REVIEW"
    CONNECTOR_WRITE_REVIEW = "CONNECTOR_WRITE_REVIEW"
    HUMAN_REVIEW_BOUNDARY = "HUMAN_REVIEW_BOUNDARY"


@dataclass(frozen=True)
class HumanApprovalRequest:
    request_id: str
    source_event_id: str
    subject_id: str
    subject_type: str
    action_category: ApprovalActionCategory
    status: ApprovalRequestStatus
    risk_level: ApprovalRiskLevel
    requested_decision: str
    reason: str
    required_approvers: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    blocked_actions: tuple[str, ...]
    approved: bool
    rejected: bool
    expired: bool
    action_executed: bool
    human_review_required: bool
    provenance: str


@dataclass(frozen=True)
class HumanApprovalWorkflow:
    workflow_id: str
    mode: HumanApprovalWorkflowMode
    title: str
    source_audit_envelope_id: str
    requests: tuple[HumanApprovalRequest, ...]
    decision_policy: tuple[str, ...]
    required_reviews: tuple[str, ...]
    blocked_actions: tuple[str, ...]
    audit_envelope_summary: dict[str, object]
    workflow_built: bool
    approval_records_persisted: bool
    approvals_granted: bool
    rejections_recorded: bool
    actions_executed: bool
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


def build_human_approval_workflow() -> HumanApprovalWorkflow:
    envelope = build_audit_event_envelope()
    envelope_summary = summarize_audit_event_envelope(envelope)

    review_events = tuple(
        event for event in envelope.events if event.severity != AuditEventSeverity.INFO
    )

    requests = tuple(
        _request_from_event(event=event, index=index)
        for index, event in enumerate(review_events, start=1)
    )

    return HumanApprovalWorkflow(
        workflow_id="sprint7-human-approval-workflow-001",
        mode=HumanApprovalWorkflowMode.REVIEW_ONLY_WORKFLOW,
        title="EAIOS Sprint 7 Human Approval Workflow",
        source_audit_envelope_id=str(envelope_summary["envelope_id"]),
        requests=requests,
        decision_policy=(
            "human_approval_required_for_write_operations",
            "human_approval_required_for_remediation",
            "human_approval_required_for_notifications",
            "human_approval_required_for_benchmark_scoring",
            "human_approval_required_for_benchmark_truth_updates",
            "human_approval_required_for_connector_enablement",
            "human_approval_required_for_provider_output_acceptance",
            "human_approval_required_for_cloud_deployment",
        ),
        required_reviews=(
            "approval_workflow_schema_review",
            "segregation_of_duties_review",
            "risk_acceptance_review",
            "audit_trace_review",
            "rollback_disable_switch_review",
            "benchmark_truth_isolation_review",
        ),
        blocked_actions=(
            "approve_without_human",
            "reject_without_human",
            "persist_approval_record_to_external_store",
            "execute_approved_action",
            "call_real_connector",
            "execute_tool_action",
            "perform_external_write",
            "modify_production_record",
            "change_infrastructure",
            "send_notification",
            "load_secret_material",
            "access_external_network",
            "score_benchmark_from_approval",
            "update_benchmark_truth_from_approval",
            "enable_autonomous_remediation",
            "bypass_human_review",
        ),
        audit_envelope_summary=envelope_summary,
        workflow_built=True,
        approval_records_persisted=False,
        approvals_granted=False,
        rejections_recorded=False,
        actions_executed=False,
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
        provenance="human_approval_workflow:model",
    )



def summarize_human_approval_workflow(
    workflow: HumanApprovalWorkflow,
) -> dict[str, object]:
    blocking_count = sum(
        1 for request in workflow.requests if request.risk_level == ApprovalRiskLevel.BLOCKING
    )

    return {
        "workflow_id": workflow.workflow_id,
        "mode": workflow.mode.value,
        "title": workflow.title,
        "source_audit_envelope_id": workflow.source_audit_envelope_id,
        "request_count": len(workflow.requests),
        "blocking_request_count": blocking_count,
        "decision_policy_count": len(workflow.decision_policy),
        "required_review_count": len(workflow.required_reviews),
        "blocked_action_count": len(workflow.blocked_actions),
        "workflow_built": workflow.workflow_built,
        "approval_records_persisted": workflow.approval_records_persisted,
        "approvals_granted": workflow.approvals_granted,
        "rejections_recorded": workflow.rejections_recorded,
        "actions_executed": workflow.actions_executed,
        "real_connector_calls_performed": workflow.real_connector_calls_performed,
        "external_writes_performed": workflow.external_writes_performed,
        "production_records_modified": workflow.production_records_modified,
        "infrastructure_changed": workflow.infrastructure_changed,
        "secrets_loaded": workflow.secrets_loaded,
        "network_access_performed": workflow.network_access_performed,
        "remediation_performed": workflow.remediation_performed,
        "notifications_sent": workflow.notifications_sent,
        "benchmark_scoring_performed": workflow.benchmark_scoring_performed,
        "benchmark_truth_updated": workflow.benchmark_truth_updated,
        "autonomous_remediation_allowed": workflow.autonomous_remediation_allowed,
        "human_review_required": workflow.human_review_required,
    }


def to_view_model(workflow: HumanApprovalWorkflow) -> dict[str, Any]:
    return {
        "summary": summarize_human_approval_workflow(workflow),
        "requests": [
            {
                "request_id": request.request_id,
                "source_event_id": request.source_event_id,
                "subject_id": request.subject_id,
                "subject_type": request.subject_type,
                "action_category": request.action_category.value,
                "status": request.status.value,
                "risk_level": request.risk_level.value,
                "requested_decision": request.requested_decision,
                "reason": request.reason,
                "required_approvers": list(request.required_approvers),
                "evidence_refs": list(request.evidence_refs),
                "blocked_actions": list(request.blocked_actions),
                "approved": request.approved,
                "rejected": request.rejected,
                "expired": request.expired,
                "action_executed": request.action_executed,
                "human_review_required": request.human_review_required,
                "provenance": request.provenance,
            }
            for request in workflow.requests
        ],
        "decision_policy": list(workflow.decision_policy),
        "required_reviews": list(workflow.required_reviews),
        "blocked_actions": list(workflow.blocked_actions),
        "audit_envelope_summary": workflow.audit_envelope_summary,
        "provenance": workflow.provenance,
    }


def _request_from_event(event: AuditEvent, index: int) -> HumanApprovalRequest:
    if event.severity == AuditEventSeverity.BLOCKING:
        status = ApprovalRequestStatus.BLOCKED_UNTIL_APPROVED
        risk_level = ApprovalRiskLevel.BLOCKING
    else:
        status = ApprovalRequestStatus.PENDING_HUMAN_REVIEW
        risk_level = ApprovalRiskLevel.HIGH

    action_category = _category_for_event(event)

    return HumanApprovalRequest(
        request_id=f"human-approval-request-{index:03d}",
        source_event_id=event.event_id,
        subject_id=event.subject_id,
        subject_type=event.subject_type,
        action_category=action_category,
        status=status,
        risk_level=risk_level,
        requested_decision=event.decision,
        reason=event.message,
        required_approvers=_required_approvers_for_category(action_category),
        evidence_refs=event.evidence_refs,
        blocked_actions=event.blocked_actions,
        approved=False,
        rejected=False,
        expired=False,
        action_executed=False,
        human_review_required=True,
        provenance="human_approval_workflow:request",
    )


def _category_for_event(event: AuditEvent) -> ApprovalActionCategory:
    if event.subject_type == "mcp_connector":
        return ApprovalActionCategory.CONNECTOR_WRITE_REVIEW
    if event.subject_type == "approval_boundary":
        return ApprovalActionCategory.HUMAN_REVIEW_BOUNDARY
    return ApprovalActionCategory.GOVERNANCE_REVIEW


def _required_approvers_for_category(
    category: ApprovalActionCategory,
) -> tuple[str, ...]:
    if category == ApprovalActionCategory.CONNECTOR_WRITE_REVIEW:
        return (
            "service_owner",
            "technical_owner",
            "governance_reviewer",
        )
    if category == ApprovalActionCategory.HUMAN_REVIEW_BOUNDARY:
        return (
            "governance_reviewer",
            "risk_owner",
        )
    return (
        "governance_reviewer",
        "architecture_owner",
    )
