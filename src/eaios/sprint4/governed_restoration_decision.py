"""Sprint 4D governed restoration operator decision record.

This module validates an operator decision against the human approval packet and
moves the restoration package through a safe state machine.

It does not execute remediation. Approval means manual operator execution may
be considered outside this module; EAIOS still performs no autonomous action.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint4.governed_restoration_approval_packet import (
    ApprovalDecisionOption,
    RestorationApprovalPacket,
    build_restoration_approval_packet,
)


class OperatorDecisionValidationState(str, Enum):
    ACCEPTED_OPERATOR_DECISION = "ACCEPTED_OPERATOR_DECISION"
    BLOCKED_INVALID_DECISION = "BLOCKED_INVALID_DECISION"
    BLOCKED_MISSING_REQUIRED_FIELD = "BLOCKED_MISSING_REQUIRED_FIELD"
    BLOCKED_MISSING_ACKNOWLEDGEMENT = "BLOCKED_MISSING_ACKNOWLEDGEMENT"


class SafeRestorationState(str, Enum):
    PENDING_OPERATOR_DECISION = "PENDING_OPERATOR_DECISION"
    APPROVED_FOR_MANUAL_EXECUTION_ONLY = "APPROVED_FOR_MANUAL_EXECUTION_ONLY"
    MORE_EVIDENCE_REQUESTED = "MORE_EVIDENCE_REQUESTED"
    REJECTED_BY_OPERATOR = "REJECTED_BY_OPERATOR"
    DEFERRED_TO_SERVICE_OWNER = "DEFERRED_TO_SERVICE_OWNER"
    BLOCKED_INVALID_DECISION = "BLOCKED_INVALID_DECISION"


@dataclass(frozen=True)
class OperatorDecisionInput:
    operator_id: str
    decision: ApprovalDecisionOption | str
    decision_rationale: str
    approved_action_ids: tuple[str, ...]
    service_owner_acknowledgement: bool
    rollback_criteria_acknowledgement: bool
    communications_review_acknowledgement: bool
    timestamp: str


@dataclass(frozen=True)
class OperatorDecisionValidation:
    validation_id: str
    packet_id: str
    operator_id: str
    decision: str
    validation_state: OperatorDecisionValidationState
    safe_restoration_state: SafeRestorationState
    accepted: bool
    reasons: tuple[str, ...]
    approved_action_ids: tuple[str, ...]
    blocked_actions: tuple[str, ...]
    manual_execution_only: bool
    autonomous_remediation_allowed: bool
    real_tool_execution_performed: bool
    benchmark_scoring_allowed_from_decision: bool
    human_approval_recorded: bool
    provenance: str


def build_default_operator_decision_validation() -> OperatorDecisionValidation:
    packet = build_restoration_approval_packet()

    decision = OperatorDecisionInput(
        operator_id="operator-demo-001",
        decision=ApprovalDecisionOption.REQUEST_MORE_EVIDENCE,
        decision_rationale=(
            "Request more evidence because payment evidence has conflicts and "
            "inventory evidence has risky incomplete knowledge."
        ),
        approved_action_ids=(),
        service_owner_acknowledgement=True,
        rollback_criteria_acknowledgement=True,
        communications_review_acknowledgement=True,
        timestamp="2026-07-10T00:00:00-07:00",
    )

    return validate_operator_decision(packet, decision)


def validate_operator_decision(
    packet: RestorationApprovalPacket,
    decision_input: OperatorDecisionInput,
) -> OperatorDecisionValidation:
    missing_fields = _missing_required_fields(packet, decision_input)
    if missing_fields:
        return _blocked_validation(
            packet=packet,
            decision_input=decision_input,
            validation_state=OperatorDecisionValidationState.BLOCKED_MISSING_REQUIRED_FIELD,
            reasons=tuple(f"Missing required field: {field}" for field in missing_fields),
        )

    missing_acknowledgements = _missing_acknowledgements(decision_input)
    if missing_acknowledgements:
        return _blocked_validation(
            packet=packet,
            decision_input=decision_input,
            validation_state=OperatorDecisionValidationState.BLOCKED_MISSING_ACKNOWLEDGEMENT,
            reasons=tuple(
                f"Missing required acknowledgement: {field}"
                for field in missing_acknowledgements
            ),
        )

    try:
        decision = ApprovalDecisionOption(decision_input.decision)
    except ValueError:
        return _blocked_validation(
            packet=packet,
            decision_input=decision_input,
            validation_state=OperatorDecisionValidationState.BLOCKED_INVALID_DECISION,
            reasons=(f"Decision is not allowed: {decision_input.decision}",),
        )

    if decision not in packet.decision_template.allowed_decisions:
        return _blocked_validation(
            packet=packet,
            decision_input=decision_input,
            validation_state=OperatorDecisionValidationState.BLOCKED_INVALID_DECISION,
            reasons=(f"Decision is not allowed: {decision.value}",),
        )

    state = _safe_state_for_decision(decision)

    return OperatorDecisionValidation(
        validation_id="operator-decision-validation-001",
        packet_id=packet.packet_id,
        operator_id=decision_input.operator_id,
        decision=decision.value,
        validation_state=OperatorDecisionValidationState.ACCEPTED_OPERATOR_DECISION,
        safe_restoration_state=state,
        accepted=True,
        reasons=("Operator decision accepted by approval packet policy.",),
        approved_action_ids=decision_input.approved_action_ids,
        blocked_actions=packet.blocked_actions,
        manual_execution_only=(
            decision == ApprovalDecisionOption.APPROVE_PACKAGE_FOR_MANUAL_EXECUTION
        ),
        autonomous_remediation_allowed=False,
        real_tool_execution_performed=False,
        benchmark_scoring_allowed_from_decision=False,
        human_approval_recorded=True,
        provenance="governed_restoration_decision:operator_decision_validation",
    )


def summarize_operator_decision_validation(
    validation: OperatorDecisionValidation,
) -> dict[str, object]:
    return {
        "validation_id": validation.validation_id,
        "packet_id": validation.packet_id,
        "operator_id": validation.operator_id,
        "decision": validation.decision,
        "validation_state": validation.validation_state.value,
        "safe_restoration_state": validation.safe_restoration_state.value,
        "accepted": validation.accepted,
        "reason_count": len(validation.reasons),
        "approved_action_count": len(validation.approved_action_ids),
        "blocked_action_count": len(validation.blocked_actions),
        "manual_execution_only": validation.manual_execution_only,
        "autonomous_remediation_allowed": validation.autonomous_remediation_allowed,
        "real_tool_execution_performed": validation.real_tool_execution_performed,
        "benchmark_scoring_allowed_from_decision": (
            validation.benchmark_scoring_allowed_from_decision
        ),
        "human_approval_recorded": validation.human_approval_recorded,
    }


def to_view_model(validation: OperatorDecisionValidation) -> dict[str, Any]:
    return {
        "summary": summarize_operator_decision_validation(validation),
        "reasons": list(validation.reasons),
        "approved_action_ids": list(validation.approved_action_ids),
        "blocked_actions": list(validation.blocked_actions),
        "manual_execution_only": validation.manual_execution_only,
        "autonomous_remediation_allowed": validation.autonomous_remediation_allowed,
        "real_tool_execution_performed": validation.real_tool_execution_performed,
        "benchmark_scoring_allowed_from_decision": (
            validation.benchmark_scoring_allowed_from_decision
        ),
        "human_approval_recorded": validation.human_approval_recorded,
        "provenance": validation.provenance,
    }


def _missing_required_fields(
    packet: RestorationApprovalPacket,
    decision_input: OperatorDecisionInput,
) -> tuple[str, ...]:
    values = {
        "operator_id": decision_input.operator_id,
        "decision": decision_input.decision,
        "decision_rationale": decision_input.decision_rationale,
        "approved_action_ids": decision_input.approved_action_ids,
        "service_owner_acknowledgement": decision_input.service_owner_acknowledgement,
        "rollback_criteria_acknowledgement": (
            decision_input.rollback_criteria_acknowledgement
        ),
        "communications_review_acknowledgement": (
            decision_input.communications_review_acknowledgement
        ),
        "timestamp": decision_input.timestamp,
    }

    missing: list[str] = []
    for field in packet.decision_template.required_fields:
        value = values[field]
        if value is None or value == "":
            missing.append(field)

    return tuple(missing)


def _missing_acknowledgements(
    decision_input: OperatorDecisionInput,
) -> tuple[str, ...]:
    missing: list[str] = []

    if decision_input.service_owner_acknowledgement is not True:
        missing.append("service_owner_acknowledgement")
    if decision_input.rollback_criteria_acknowledgement is not True:
        missing.append("rollback_criteria_acknowledgement")
    if decision_input.communications_review_acknowledgement is not True:
        missing.append("communications_review_acknowledgement")

    return tuple(missing)


def _safe_state_for_decision(
    decision: ApprovalDecisionOption,
) -> SafeRestorationState:
    if decision == ApprovalDecisionOption.APPROVE_PACKAGE_FOR_MANUAL_EXECUTION:
        return SafeRestorationState.APPROVED_FOR_MANUAL_EXECUTION_ONLY
    if decision == ApprovalDecisionOption.REQUEST_MORE_EVIDENCE:
        return SafeRestorationState.MORE_EVIDENCE_REQUESTED
    if decision == ApprovalDecisionOption.REJECT_PACKAGE:
        return SafeRestorationState.REJECTED_BY_OPERATOR
    if decision == ApprovalDecisionOption.DEFER_TO_SERVICE_OWNER:
        return SafeRestorationState.DEFERRED_TO_SERVICE_OWNER

    return SafeRestorationState.BLOCKED_INVALID_DECISION


def _blocked_validation(
    packet: RestorationApprovalPacket,
    decision_input: OperatorDecisionInput,
    validation_state: OperatorDecisionValidationState,
    reasons: tuple[str, ...],
) -> OperatorDecisionValidation:
    return OperatorDecisionValidation(
        validation_id="operator-decision-validation-001",
        packet_id=packet.packet_id,
        operator_id=decision_input.operator_id,
        decision=str(decision_input.decision),
        validation_state=validation_state,
        safe_restoration_state=SafeRestorationState.BLOCKED_INVALID_DECISION,
        accepted=False,
        reasons=reasons,
        approved_action_ids=(),
        blocked_actions=packet.blocked_actions,
        manual_execution_only=False,
        autonomous_remediation_allowed=False,
        real_tool_execution_performed=False,
        benchmark_scoring_allowed_from_decision=False,
        human_approval_recorded=False,
        provenance="governed_restoration_decision:blocked_operator_decision",
    )
