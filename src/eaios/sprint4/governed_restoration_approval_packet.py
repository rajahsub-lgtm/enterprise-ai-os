"""Sprint 4D governed restoration approval packet.

This module converts the cross-cluster restoration plan into a human approval
packet.

It does not approve, execute, remediate, notify, or score benchmarks. It only
creates an operator-review package with decision options, evidence references,
risks, rollback notes, and explicit execution blocks.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint4.governed_restoration_orchestration import (
    CrossClusterRestorationPlan,
    build_cross_cluster_restoration_plan,
)


class ApprovalDecisionOption(str, Enum):
    APPROVE_PACKAGE_FOR_MANUAL_EXECUTION = "APPROVE_PACKAGE_FOR_MANUAL_EXECUTION"
    REQUEST_MORE_EVIDENCE = "REQUEST_MORE_EVIDENCE"
    REJECT_PACKAGE = "REJECT_PACKAGE"
    DEFER_TO_SERVICE_OWNER = "DEFER_TO_SERVICE_OWNER"


class ApprovalPacketState(str, Enum):
    READY_FOR_OPERATOR_REVIEW = "READY_FOR_OPERATOR_REVIEW"
    BLOCKED_PENDING_HUMAN_DECISION = "BLOCKED_PENDING_HUMAN_DECISION"


@dataclass(frozen=True)
class ApprovalEvidenceReference:
    evidence_id: str
    source_action_id: str
    cluster_id: str
    source_failure_case_id: str
    reason_required: str
    evidence_available: bool
    degraded_or_denied: bool
    human_review_required: bool


@dataclass(frozen=True)
class OperatorDecisionRecordTemplate:
    decision_record_id: str
    allowed_decisions: tuple[ApprovalDecisionOption, ...]
    required_fields: tuple[str, ...]
    blocked_actions: tuple[str, ...]
    approval_statement: str
    autonomous_execution_allowed: bool
    real_tool_execution_allowed: bool
    benchmark_scoring_allowed: bool


@dataclass(frozen=True)
class RestorationApprovalPacket:
    packet_id: str
    source_plan_id: str
    packet_state: ApprovalPacketState
    decision_template: OperatorDecisionRecordTemplate
    evidence_references: tuple[ApprovalEvidenceReference, ...]
    risk_summary: tuple[str, ...]
    rollback_summary: tuple[str, ...]
    operator_questions: tuple[str, ...]
    proposed_manual_actions: tuple[str, ...]
    blocked_actions: tuple[str, ...]
    service_owner_review_required: bool
    change_review_required: bool
    communications_review_required: bool
    approval_required_before_action: bool
    autonomous_remediation_allowed: bool
    real_tool_execution_performed: bool
    benchmark_scoring_allowed_from_packet: bool
    human_approval_required: bool
    provenance: str


def build_restoration_approval_packet(
    plan: CrossClusterRestorationPlan | None = None,
) -> RestorationApprovalPacket:
    if plan is None:
        plan = build_cross_cluster_restoration_plan()

    evidence_references = tuple(
        ApprovalEvidenceReference(
            evidence_id=evidence_id,
            source_action_id=action.action_id,
            cluster_id=action.cluster_id,
            source_failure_case_id=action.source_failure_case_id,
            reason_required=(
                "Required to support operator review of the restoration candidate."
            ),
            evidence_available=not evidence_id.endswith("denied-remediation-payment"),
            degraded_or_denied=evidence_id.endswith("denied-remediation-payment"),
            human_review_required=True,
        )
        for action in plan.action_candidates
        for evidence_id in action.required_evidence_ids
    )

    blocked_actions = (
        "execute_remediation",
        "restart_service",
        "scale_service",
        "modify_database",
        "deploy_code",
        "rollback_change",
        "send_notification",
        "page_on_call",
        "publish_status",
        "score_benchmark_from_restoration",
    )

    return RestorationApprovalPacket(
        packet_id="sprint4d-restoration-approval-packet-001",
        source_plan_id=plan.plan_id,
        packet_state=ApprovalPacketState.BLOCKED_PENDING_HUMAN_DECISION,
        decision_template=OperatorDecisionRecordTemplate(
            decision_record_id="operator-decision-template-restoration-001",
            allowed_decisions=(
                ApprovalDecisionOption.APPROVE_PACKAGE_FOR_MANUAL_EXECUTION,
                ApprovalDecisionOption.REQUEST_MORE_EVIDENCE,
                ApprovalDecisionOption.REJECT_PACKAGE,
                ApprovalDecisionOption.DEFER_TO_SERVICE_OWNER,
            ),
            required_fields=(
                "operator_id",
                "decision",
                "decision_rationale",
                "approved_action_ids",
                "service_owner_acknowledgement",
                "rollback_criteria_acknowledgement",
                "communications_review_acknowledgement",
                "timestamp",
            ),
            blocked_actions=blocked_actions,
            approval_statement=(
                "Approval permits manual operator execution only; EAIOS still "
                "does not execute remediation autonomously."
            ),
            autonomous_execution_allowed=False,
            real_tool_execution_allowed=False,
            benchmark_scoring_allowed=False,
        ),
        evidence_references=evidence_references,
        risk_summary=plan.shared_risks,
        rollback_summary=plan.rollback_notes,
        operator_questions=plan.operator_decision_questions,
        proposed_manual_actions=tuple(
            f"{action.action_id}: {action.title}"
            for action in plan.action_candidates
        ),
        blocked_actions=blocked_actions,
        service_owner_review_required=True,
        change_review_required=True,
        communications_review_required=True,
        approval_required_before_action=True,
        autonomous_remediation_allowed=False,
        real_tool_execution_performed=False,
        benchmark_scoring_allowed_from_packet=False,
        human_approval_required=True,
        provenance="governed_restoration_approval_packet:human_review_packet",
    )


def summarize_approval_packet(packet: RestorationApprovalPacket) -> dict[str, object]:
    return {
        "packet_id": packet.packet_id,
        "source_plan_id": packet.source_plan_id,
        "packet_state": packet.packet_state.value,
        "allowed_decision_count": len(packet.decision_template.allowed_decisions),
        "evidence_reference_count": len(packet.evidence_references),
        "risk_count": len(packet.risk_summary),
        "rollback_note_count": len(packet.rollback_summary),
        "operator_question_count": len(packet.operator_questions),
        "proposed_manual_action_count": len(packet.proposed_manual_actions),
        "blocked_action_count": len(packet.blocked_actions),
        "service_owner_review_required": packet.service_owner_review_required,
        "change_review_required": packet.change_review_required,
        "communications_review_required": packet.communications_review_required,
        "approval_required_before_action": packet.approval_required_before_action,
        "autonomous_remediation_allowed": packet.autonomous_remediation_allowed,
        "real_tool_execution_performed": packet.real_tool_execution_performed,
        "benchmark_scoring_allowed_from_packet": (
            packet.benchmark_scoring_allowed_from_packet
        ),
        "human_approval_required": packet.human_approval_required,
    }


def to_view_model(packet: RestorationApprovalPacket) -> dict[str, Any]:
    return {
        "summary": summarize_approval_packet(packet),
        "decision_template": {
            "decision_record_id": packet.decision_template.decision_record_id,
            "allowed_decisions": [
                decision.value for decision in packet.decision_template.allowed_decisions
            ],
            "required_fields": list(packet.decision_template.required_fields),
            "blocked_actions": list(packet.decision_template.blocked_actions),
            "approval_statement": packet.decision_template.approval_statement,
            "autonomous_execution_allowed": (
                packet.decision_template.autonomous_execution_allowed
            ),
            "real_tool_execution_allowed": (
                packet.decision_template.real_tool_execution_allowed
            ),
            "benchmark_scoring_allowed": (
                packet.decision_template.benchmark_scoring_allowed
            ),
        },
        "evidence_references": [
            {
                "evidence_id": reference.evidence_id,
                "source_action_id": reference.source_action_id,
                "cluster_id": reference.cluster_id,
                "source_failure_case_id": reference.source_failure_case_id,
                "reason_required": reference.reason_required,
                "evidence_available": reference.evidence_available,
                "degraded_or_denied": reference.degraded_or_denied,
                "human_review_required": reference.human_review_required,
            }
            for reference in packet.evidence_references
        ],
        "risk_summary": list(packet.risk_summary),
        "rollback_summary": list(packet.rollback_summary),
        "operator_questions": list(packet.operator_questions),
        "proposed_manual_actions": list(packet.proposed_manual_actions),
        "blocked_actions": list(packet.blocked_actions),
        "service_owner_review_required": packet.service_owner_review_required,
        "change_review_required": packet.change_review_required,
        "communications_review_required": packet.communications_review_required,
        "approval_required_before_action": packet.approval_required_before_action,
        "autonomous_remediation_allowed": packet.autonomous_remediation_allowed,
        "real_tool_execution_performed": packet.real_tool_execution_performed,
        "benchmark_scoring_allowed_from_packet": (
            packet.benchmark_scoring_allowed_from_packet
        ),
        "human_approval_required": packet.human_approval_required,
        "provenance": packet.provenance,
    }
