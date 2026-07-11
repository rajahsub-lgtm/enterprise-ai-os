from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint4.governed_restoration_orchestration import (
    RestorationActionType,
    RestorationPlanState,
    RestorationRiskLevel,
    build_cross_cluster_restoration_plan,
    summarize_restoration_plan,
    to_view_model,
)


def _plan():
    return build_cross_cluster_restoration_plan()


def test_cross_cluster_restoration_plan_builds_from_reasoning_and_mcp_snapshots():
    plan = _plan()

    assert plan.plan_id == "sprint4d-cross-cluster-restoration-plan-001"
    assert plan.source_reasoning_snapshot_id == "governed-reasoning::composition-structural-001"
    assert plan.source_mcp_snapshot_id == "governed-mcp-observation::composition-structural-001"
    assert plan.plan_state == RestorationPlanState.BLOCKED_PENDING_APPROVAL
    assert plan.cluster_count == 2
    assert plan.provenance == "governed_restoration_orchestration:cross_cluster_plan"


def test_cross_cluster_restoration_plan_contains_three_candidate_actions():
    plan = _plan()

    assert len(plan.action_candidates) == 3

    action_ids = {action.action_id for action in plan.action_candidates}

    assert action_ids == {
        "restore-candidate-payment-validate-evidence",
        "restore-candidate-inventory-validate-topology",
        "restore-candidate-cross-cluster-approval-hold",
    }


def test_payment_restoration_candidate_preserves_conflict_review_boundary():
    plan = _plan()

    payment = next(
        action
        for action in plan.action_candidates
        if action.source_failure_case_id == "structural-failure-payment-latency-001"
    )

    assert payment.action_type == RestorationActionType.VALIDATE_EVIDENCE
    assert payment.risk_level == RestorationRiskLevel.MEDIUM
    assert payment.required_evidence_ids == (
        "mcp-tool-evidence::mcp-request-read-telemetry-payment",
        "mcp-tool-evidence::mcp-request-search-knowledge-payment",
    )
    assert "conflicting evidence" in payment.rationale
    assert payment.can_execute_autonomously is False
    assert payment.human_approval_required is True
    assert payment.benchmark_scoring_allowed is False


def test_inventory_restoration_candidate_preserves_risky_incomplete_boundary():
    plan = _plan()

    inventory = next(
        action
        for action in plan.action_candidates
        if action.source_failure_case_id == "structural-failure-inventory-errors-001"
    )

    assert inventory.action_type == RestorationActionType.INVESTIGATE
    assert inventory.risk_level == RestorationRiskLevel.HIGH
    assert inventory.required_evidence_ids == (
        "mcp-tool-evidence::mcp-request-read-topology-inventory",
    )
    assert "risky and incomplete knowledge" in inventory.rationale
    assert inventory.can_execute_autonomously is False
    assert inventory.human_approval_required is True
    assert inventory.benchmark_scoring_allowed is False


def test_cross_cluster_hold_candidate_uses_denied_tool_evidence():
    plan = _plan()

    hold = next(
        action
        for action in plan.action_candidates
        if action.cluster_id == "cross-cluster"
    )

    assert hold.action_type == RestorationActionType.HOLD_FOR_APPROVAL
    assert hold.risk_level == RestorationRiskLevel.HIGH
    assert hold.required_evidence_ids == (
        "mcp-tool-evidence::mcp-request-denied-remediation-payment",
    )
    assert "blocked until an operator approves" in hold.rationale
    assert hold.rollback_note == "No rollback required because no action has been executed."
    assert hold.can_execute_autonomously is False
    assert hold.human_approval_required is True


def test_restoration_plan_preserves_shared_risks_and_rollback_notes():
    plan = _plan()

    assert plan.shared_risks == (
        "Payment evidence contains stale and conflicting knowledge.",
        "Inventory evidence contains risky and incomplete knowledge.",
        "A remediation request was denied and must be represented as degraded-mode evidence.",
        "Cross-cluster restoration may create unintended downstream impact.",
    )
    assert plan.rollback_notes == (
        "No production action has been executed by this plan.",
        "Any future restoration package must include explicit backout criteria.",
        "Operator must verify service owner approval before action.",
    )


def test_restoration_plan_records_operator_decision_questions():
    plan = _plan()

    assert len(plan.operator_decision_questions) == 3
    assert any(
        "payment latency is still active" in question
        for question in plan.operator_decision_questions
    )
    assert any(
        "route-planning impact" in question
        for question in plan.operator_decision_questions
    )
    assert any(
        "approve a restoration package" in question
        for question in plan.operator_decision_questions
    )


def test_restoration_plan_preserves_denied_tool_constraints():
    plan = _plan()

    assert plan.denied_tool_constraints == (
        "remediation.plan.propose::restart_service::Operation is globally denied.",
    )


def test_restoration_plan_never_executes_or_scores_benchmark():
    plan = _plan()

    assert plan.approval_packet_required is True
    assert plan.autonomous_remediation_allowed is False
    assert plan.real_tool_execution_performed is False
    assert plan.benchmark_scoring_allowed_from_restoration is False
    assert plan.human_approval_required is True

    for action in plan.action_candidates:
        assert action.can_execute_autonomously is False
        assert action.human_approval_required is True
        assert action.benchmark_scoring_allowed is False


def test_restoration_plan_summary_is_view_ready():
    plan = _plan()

    assert summarize_restoration_plan(plan) == {
        "plan_id": "sprint4d-cross-cluster-restoration-plan-001",
        "source_reasoning_snapshot_id": "governed-reasoning::composition-structural-001",
        "source_mcp_snapshot_id": "governed-mcp-observation::composition-structural-001",
        "plan_state": "BLOCKED_PENDING_APPROVAL",
        "cluster_count": 2,
        "action_candidate_count": 3,
        "shared_risk_count": 4,
        "rollback_note_count": 3,
        "operator_question_count": 3,
        "denied_tool_constraint_count": 1,
        "approval_packet_required": True,
        "autonomous_remediation_allowed": False,
        "real_tool_execution_performed": False,
        "benchmark_scoring_allowed_from_restoration": False,
        "human_approval_required": True,
    }


def test_restoration_plan_view_model_is_json_serializable():
    plan = _plan()

    serialized = json.dumps(to_view_model(plan), indent=2)

    assert "sprint4d-cross-cluster-restoration-plan-001" in serialized
    assert "restore-candidate-payment-validate-evidence" in serialized
    assert "restore-candidate-inventory-validate-topology" in serialized
    assert "restore-candidate-cross-cluster-approval-hold" in serialized
    assert "denied_tool_constraints" in serialized
    assert "approval_packet_required" in serialized


def test_restoration_orchestration_module_does_not_execute_real_tools_or_score_benchmark():
    source = Path("src/eaios/sprint4/governed_restoration_orchestration.py").read_text(
        encoding="utf-8"
    )

    assert "subprocess" not in source
    assert "import requests" not in source.lower()
    assert "import httpx" not in source.lower()
    assert "execute_tool(" not in source
    assert "restart_service(" not in source
    assert "score_benchmark_result(" not in source
