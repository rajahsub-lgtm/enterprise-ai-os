from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint4.governed_restoration_approval_packet import (
    ApprovalDecisionOption,
    ApprovalPacketState,
    build_restoration_approval_packet,
    summarize_approval_packet,
    to_view_model,
)


def _packet():
    return build_restoration_approval_packet()


def test_restoration_approval_packet_builds_from_cross_cluster_plan():
    packet = _packet()

    assert packet.packet_id == "sprint4d-restoration-approval-packet-001"
    assert packet.source_plan_id == "sprint4d-cross-cluster-restoration-plan-001"
    assert packet.packet_state == ApprovalPacketState.BLOCKED_PENDING_HUMAN_DECISION
    assert packet.provenance == "governed_restoration_approval_packet:human_review_packet"


def test_restoration_approval_packet_defines_allowed_operator_decisions():
    packet = _packet()

    assert packet.decision_template.decision_record_id == (
        "operator-decision-template-restoration-001"
    )
    assert packet.decision_template.allowed_decisions == (
        ApprovalDecisionOption.APPROVE_PACKAGE_FOR_MANUAL_EXECUTION,
        ApprovalDecisionOption.REQUEST_MORE_EVIDENCE,
        ApprovalDecisionOption.REJECT_PACKAGE,
        ApprovalDecisionOption.DEFER_TO_SERVICE_OWNER,
    )
    assert "operator_id" in packet.decision_template.required_fields
    assert "decision_rationale" in packet.decision_template.required_fields
    assert "rollback_criteria_acknowledgement" in packet.decision_template.required_fields


def test_restoration_approval_packet_blocks_execution_actions():
    packet = _packet()

    assert packet.blocked_actions == (
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
    assert packet.decision_template.blocked_actions == packet.blocked_actions


def test_restoration_approval_packet_preserves_manual_only_approval_statement():
    packet = _packet()

    assert "manual operator execution only" in packet.decision_template.approval_statement
    assert packet.decision_template.autonomous_execution_allowed is False
    assert packet.decision_template.real_tool_execution_allowed is False
    assert packet.decision_template.benchmark_scoring_allowed is False


def test_restoration_approval_packet_references_required_evidence():
    packet = _packet()

    evidence_ids = {reference.evidence_id for reference in packet.evidence_references}

    assert evidence_ids == {
        "mcp-tool-evidence::mcp-request-read-telemetry-payment",
        "mcp-tool-evidence::mcp-request-search-knowledge-payment",
        "mcp-tool-evidence::mcp-request-read-topology-inventory",
        "mcp-tool-evidence::mcp-request-denied-remediation-payment",
    }

    assert len(packet.evidence_references) == 4


def test_restoration_approval_packet_marks_denied_evidence_as_degraded():
    packet = _packet()

    denied = next(
        reference for reference in packet.evidence_references
        if reference.evidence_id == "mcp-tool-evidence::mcp-request-denied-remediation-payment"
    )

    assert denied.evidence_available is False
    assert denied.degraded_or_denied is True
    assert denied.human_review_required is True
    assert denied.source_action_id == "restore-candidate-cross-cluster-approval-hold"


def test_restoration_approval_packet_marks_available_evidence_as_review_required():
    packet = _packet()

    available = [
        reference for reference in packet.evidence_references
        if reference.evidence_available
    ]

    assert len(available) == 3

    for reference in available:
        assert reference.degraded_or_denied is False
        assert reference.human_review_required is True
        assert reference.cluster_id.startswith("cluster::")


def test_restoration_approval_packet_carries_risks_rollbacks_and_questions():
    packet = _packet()

    assert len(packet.risk_summary) == 4
    assert len(packet.rollback_summary) == 3
    assert len(packet.operator_questions) == 3

    assert "Payment evidence contains stale and conflicting knowledge." in packet.risk_summary
    assert "No production action has been executed by this plan." in packet.rollback_summary
    assert any(
        "approve a restoration package" in question
        for question in packet.operator_questions
    )


def test_restoration_approval_packet_lists_proposed_manual_actions():
    packet = _packet()

    assert packet.proposed_manual_actions == (
        "restore-candidate-payment-validate-evidence: Validate payment latency evidence before remediation planning",
        "restore-candidate-inventory-validate-topology: Validate inventory dependency impact before restoration package",
        "restore-candidate-cross-cluster-approval-hold: Hold restoration for human approval packet",
    )


def test_restoration_approval_packet_requires_reviews_before_action():
    packet = _packet()

    assert packet.service_owner_review_required is True
    assert packet.change_review_required is True
    assert packet.communications_review_required is True
    assert packet.approval_required_before_action is True
    assert packet.human_approval_required is True


def test_restoration_approval_packet_never_executes_or_scores_benchmark():
    packet = _packet()

    assert packet.autonomous_remediation_allowed is False
    assert packet.real_tool_execution_performed is False
    assert packet.benchmark_scoring_allowed_from_packet is False
    assert packet.human_approval_required is True


def test_restoration_approval_packet_summary_is_view_ready():
    packet = _packet()

    assert summarize_approval_packet(packet) == {
        "packet_id": "sprint4d-restoration-approval-packet-001",
        "source_plan_id": "sprint4d-cross-cluster-restoration-plan-001",
        "packet_state": "BLOCKED_PENDING_HUMAN_DECISION",
        "allowed_decision_count": 4,
        "evidence_reference_count": 4,
        "risk_count": 4,
        "rollback_note_count": 3,
        "operator_question_count": 3,
        "proposed_manual_action_count": 3,
        "blocked_action_count": 10,
        "service_owner_review_required": True,
        "change_review_required": True,
        "communications_review_required": True,
        "approval_required_before_action": True,
        "autonomous_remediation_allowed": False,
        "real_tool_execution_performed": False,
        "benchmark_scoring_allowed_from_packet": False,
        "human_approval_required": True,
    }


def test_restoration_approval_packet_view_model_is_json_serializable():
    packet = _packet()

    serialized = json.dumps(to_view_model(packet), indent=2)

    assert "sprint4d-restoration-approval-packet-001" in serialized
    assert "APPROVE_PACKAGE_FOR_MANUAL_EXECUTION" in serialized
    assert "REQUEST_MORE_EVIDENCE" in serialized
    assert "mcp-tool-evidence::mcp-request-denied-remediation-payment" in serialized
    assert "approval_required_before_action" in serialized


def test_restoration_approval_packet_module_does_not_execute_real_tools_or_score_benchmark():
    source = Path("src/eaios/sprint4/governed_restoration_approval_packet.py").read_text(
        encoding="utf-8"
    )

    assert "subprocess" not in source
    assert "import requests" not in source.lower()
    assert "import httpx" not in source.lower()
    assert "execute_tool(" not in source
    assert "restart_service(" not in source
    assert "score_benchmark_result(" not in source
