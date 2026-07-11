from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint4.governed_restoration_approval_packet import (
    ApprovalDecisionOption,
    build_restoration_approval_packet,
)
from eaios.sprint4.governed_restoration_decision import (
    OperatorDecisionInput,
    OperatorDecisionValidationState,
    SafeRestorationState,
    build_default_operator_decision_validation,
    summarize_operator_decision_validation,
    to_view_model,
    validate_operator_decision,
)


def _packet():
    return build_restoration_approval_packet()


def test_default_operator_decision_validation_requests_more_evidence():
    validation = build_default_operator_decision_validation()

    assert validation.validation_id == "operator-decision-validation-001"
    assert validation.packet_id == "sprint4d-restoration-approval-packet-001"
    assert validation.operator_id == "operator-demo-001"
    assert validation.decision == "REQUEST_MORE_EVIDENCE"
    assert validation.validation_state == OperatorDecisionValidationState.ACCEPTED_OPERATOR_DECISION
    assert validation.safe_restoration_state == SafeRestorationState.MORE_EVIDENCE_REQUESTED
    assert validation.accepted is True


def test_operator_decision_accepts_approve_for_manual_execution_only():
    packet = _packet()

    validation = validate_operator_decision(
        packet,
        OperatorDecisionInput(
            operator_id="operator-approve-001",
            decision=ApprovalDecisionOption.APPROVE_PACKAGE_FOR_MANUAL_EXECUTION,
            decision_rationale="Approve for manual execution after review.",
            approved_action_ids=(
                "restore-candidate-payment-validate-evidence",
                "restore-candidate-inventory-validate-topology",
            ),
            service_owner_acknowledgement=True,
            rollback_criteria_acknowledgement=True,
            communications_review_acknowledgement=True,
            timestamp="2026-07-10T01:00:00-07:00",
        ),
    )

    assert validation.accepted is True
    assert validation.safe_restoration_state == (
        SafeRestorationState.APPROVED_FOR_MANUAL_EXECUTION_ONLY
    )
    assert validation.manual_execution_only is True
    assert validation.autonomous_remediation_allowed is False
    assert validation.real_tool_execution_performed is False
    assert validation.benchmark_scoring_allowed_from_decision is False
    assert validation.human_approval_recorded is True


def test_operator_decision_accepts_reject_package():
    packet = _packet()

    validation = validate_operator_decision(
        packet,
        OperatorDecisionInput(
            operator_id="operator-reject-001",
            decision=ApprovalDecisionOption.REJECT_PACKAGE,
            decision_rationale="Reject package due to insufficient evidence.",
            approved_action_ids=(),
            service_owner_acknowledgement=True,
            rollback_criteria_acknowledgement=True,
            communications_review_acknowledgement=True,
            timestamp="2026-07-10T01:05:00-07:00",
        ),
    )

    assert validation.accepted is True
    assert validation.safe_restoration_state == SafeRestorationState.REJECTED_BY_OPERATOR
    assert validation.manual_execution_only is False
    assert validation.human_approval_recorded is True


def test_operator_decision_accepts_defer_to_service_owner():
    packet = _packet()

    validation = validate_operator_decision(
        packet,
        OperatorDecisionInput(
            operator_id="operator-defer-001",
            decision=ApprovalDecisionOption.DEFER_TO_SERVICE_OWNER,
            decision_rationale="Service owner should review risky inventory path.",
            approved_action_ids=(),
            service_owner_acknowledgement=True,
            rollback_criteria_acknowledgement=True,
            communications_review_acknowledgement=True,
            timestamp="2026-07-10T01:10:00-07:00",
        ),
    )

    assert validation.accepted is True
    assert validation.safe_restoration_state == SafeRestorationState.DEFERRED_TO_SERVICE_OWNER
    assert validation.human_approval_recorded is True


def test_operator_decision_blocks_invalid_decision():
    packet = _packet()

    validation = validate_operator_decision(
        packet,
        OperatorDecisionInput(
            operator_id="operator-invalid-001",
            decision="EXECUTE_NOW",
            decision_rationale="Invalid decision should be blocked.",
            approved_action_ids=(),
            service_owner_acknowledgement=True,
            rollback_criteria_acknowledgement=True,
            communications_review_acknowledgement=True,
            timestamp="2026-07-10T01:15:00-07:00",
        ),
    )

    assert validation.accepted is False
    assert validation.validation_state == OperatorDecisionValidationState.BLOCKED_INVALID_DECISION
    assert validation.safe_restoration_state == SafeRestorationState.BLOCKED_INVALID_DECISION
    assert validation.human_approval_recorded is False
    assert "Decision is not allowed: EXECUTE_NOW" in validation.reasons


def test_operator_decision_blocks_missing_required_field():
    packet = _packet()

    validation = validate_operator_decision(
        packet,
        OperatorDecisionInput(
            operator_id="",
            decision=ApprovalDecisionOption.REQUEST_MORE_EVIDENCE,
            decision_rationale="Missing operator id should be blocked.",
            approved_action_ids=(),
            service_owner_acknowledgement=True,
            rollback_criteria_acknowledgement=True,
            communications_review_acknowledgement=True,
            timestamp="2026-07-10T01:20:00-07:00",
        ),
    )

    assert validation.accepted is False
    assert validation.validation_state == (
        OperatorDecisionValidationState.BLOCKED_MISSING_REQUIRED_FIELD
    )
    assert validation.safe_restoration_state == SafeRestorationState.BLOCKED_INVALID_DECISION
    assert "Missing required field: operator_id" in validation.reasons


def test_operator_decision_blocks_missing_acknowledgement():
    packet = _packet()

    validation = validate_operator_decision(
        packet,
        OperatorDecisionInput(
            operator_id="operator-no-ack-001",
            decision=ApprovalDecisionOption.REQUEST_MORE_EVIDENCE,
            decision_rationale="Missing acknowledgement should be blocked.",
            approved_action_ids=(),
            service_owner_acknowledgement=False,
            rollback_criteria_acknowledgement=True,
            communications_review_acknowledgement=True,
            timestamp="2026-07-10T01:25:00-07:00",
        ),
    )

    assert validation.accepted is False
    assert validation.validation_state == (
        OperatorDecisionValidationState.BLOCKED_MISSING_ACKNOWLEDGEMENT
    )
    assert validation.safe_restoration_state == SafeRestorationState.BLOCKED_INVALID_DECISION
    assert "Missing required acknowledgement: service_owner_acknowledgement" in validation.reasons


def test_operator_decision_preserves_blocked_actions():
    validation = build_default_operator_decision_validation()

    assert "execute_remediation" in validation.blocked_actions
    assert "restart_service" in validation.blocked_actions
    assert "scale_service" in validation.blocked_actions
    assert "score_benchmark_from_restoration" in validation.blocked_actions


def test_operator_decision_never_executes_or_scores_benchmark():
    validation = build_default_operator_decision_validation()

    assert validation.autonomous_remediation_allowed is False
    assert validation.real_tool_execution_performed is False
    assert validation.benchmark_scoring_allowed_from_decision is False


def test_operator_decision_summary_is_view_ready():
    validation = build_default_operator_decision_validation()

    assert summarize_operator_decision_validation(validation) == {
        "validation_id": "operator-decision-validation-001",
        "packet_id": "sprint4d-restoration-approval-packet-001",
        "operator_id": "operator-demo-001",
        "decision": "REQUEST_MORE_EVIDENCE",
        "validation_state": "ACCEPTED_OPERATOR_DECISION",
        "safe_restoration_state": "MORE_EVIDENCE_REQUESTED",
        "accepted": True,
        "reason_count": 1,
        "approved_action_count": 0,
        "blocked_action_count": 10,
        "manual_execution_only": False,
        "autonomous_remediation_allowed": False,
        "real_tool_execution_performed": False,
        "benchmark_scoring_allowed_from_decision": False,
        "human_approval_recorded": True,
    }


def test_operator_decision_view_model_is_json_serializable():
    validation = build_default_operator_decision_validation()

    serialized = json.dumps(to_view_model(validation), indent=2)

    assert "operator-decision-validation-001" in serialized
    assert "REQUEST_MORE_EVIDENCE" in serialized
    assert "MORE_EVIDENCE_REQUESTED" in serialized
    assert "blocked_actions" in serialized
    assert "benchmark_scoring_allowed_from_decision" in serialized


def test_restoration_decision_module_does_not_execute_real_tools_or_score_benchmark():
    source = Path("src/eaios/sprint4/governed_restoration_decision.py").read_text(
        encoding="utf-8"
    )

    assert "subprocess" not in source
    assert "import requests" not in source.lower()
    assert "import httpx" not in source.lower()
    assert "execute_tool(" not in source
    assert "restart_service(" not in source
    assert "score_benchmark_result(" not in source
