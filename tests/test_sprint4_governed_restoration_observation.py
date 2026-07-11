from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint4.governed_restoration_observation import (
    build_governed_restoration_observation_snapshot,
    summarize_restoration_observation,
    to_view_model,
)


def _snapshot():
    return build_governed_restoration_observation_snapshot()


def test_restoration_observation_snapshot_builds_from_4d_contracts():
    snapshot = _snapshot()

    assert snapshot.snapshot_id == "governed-restoration-observation::composition-structural-001"
    assert snapshot.source_plan_id == "sprint4d-cross-cluster-restoration-plan-001"
    assert snapshot.source_packet_id == "sprint4d-restoration-approval-packet-001"
    assert snapshot.decision_validation_id == "operator-decision-validation-001"
    assert snapshot.provenance == "governed_restoration_observation:dashboard_snapshot"


def test_restoration_observation_includes_restoration_summary():
    snapshot = _snapshot()

    assert snapshot.restoration_summary["plan_id"] == "sprint4d-cross-cluster-restoration-plan-001"
    assert snapshot.restoration_summary["plan_state"] == "BLOCKED_PENDING_APPROVAL"
    assert snapshot.restoration_summary["cluster_count"] == 2
    assert snapshot.restoration_summary["action_candidate_count"] == 3
    assert snapshot.restoration_summary["approval_packet_required"] is True
    assert snapshot.restoration_summary["autonomous_remediation_allowed"] is False


def test_restoration_observation_includes_approval_summary():
    snapshot = _snapshot()

    assert snapshot.approval_summary["packet_id"] == "sprint4d-restoration-approval-packet-001"
    assert snapshot.approval_summary["packet_state"] == "BLOCKED_PENDING_HUMAN_DECISION"
    assert snapshot.approval_summary["allowed_decision_count"] == 4
    assert snapshot.approval_summary["evidence_reference_count"] == 4
    assert snapshot.approval_summary["blocked_action_count"] == 10
    assert snapshot.approval_summary["approval_required_before_action"] is True


def test_restoration_observation_includes_operator_decision_summary():
    snapshot = _snapshot()

    assert snapshot.decision_summary["validation_id"] == "operator-decision-validation-001"
    assert snapshot.decision_summary["decision"] == "REQUEST_MORE_EVIDENCE"
    assert snapshot.decision_summary["validation_state"] == "ACCEPTED_OPERATOR_DECISION"
    assert snapshot.decision_summary["safe_restoration_state"] == "MORE_EVIDENCE_REQUESTED"
    assert snapshot.decision_summary["accepted"] is True
    assert snapshot.decision_summary["real_tool_execution_performed"] is False


def test_restoration_observation_exposes_dashboard_sections():
    snapshot = _snapshot()

    assert snapshot.dashboard_sections == (
        "cross_cluster_restoration_plan",
        "human_approval_packet",
        "operator_decision_record",
        "safe_restoration_state",
        "blocked_actions",
        "governance_boundaries",
    )


def test_restoration_observation_preserves_action_cards():
    snapshot = _snapshot()

    assert len(snapshot.action_cards) == 3

    action_ids = {card["action_id"] for card in snapshot.action_cards}

    assert action_ids == {
        "restore-candidate-payment-validate-evidence",
        "restore-candidate-inventory-validate-topology",
        "restore-candidate-cross-cluster-approval-hold",
    }

    for card in snapshot.action_cards:
        assert card["human_approval_required"] is True
        assert card["can_execute_autonomously"] is False
        assert card["benchmark_scoring_allowed"] is False


def test_restoration_observation_preserves_blocked_actions():
    snapshot = _snapshot()

    assert snapshot.blocked_actions == (
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


def test_restoration_observation_preserves_governance_boundaries():
    snapshot = _snapshot()

    assert "cross_cluster_restoration_plan_required" in snapshot.governance_boundaries
    assert "human_approval_packet_required" in snapshot.governance_boundaries
    assert "operator_decision_record_required" in snapshot.governance_boundaries
    assert "safe_state_machine_required" in snapshot.governance_boundaries
    assert "manual_execution_only" in snapshot.governance_boundaries
    assert "autonomous_remediation_disabled" in snapshot.governance_boundaries
    assert "real_tool_execution_blocked" in snapshot.governance_boundaries
    assert "benchmark_scoring_from_restoration_blocked" in snapshot.governance_boundaries
    assert "denied_tool_constraints_preserved" in snapshot.governance_boundaries
    assert "service_owner_review_required" in snapshot.governance_boundaries
    assert "rollback_review_required" in snapshot.governance_boundaries
    assert "communications_review_required" in snapshot.governance_boundaries
    assert "human_approval_required" in snapshot.governance_boundaries


def test_restoration_observation_never_executes_or_scores_benchmark():
    snapshot = _snapshot()

    assert snapshot.real_tool_execution_performed is False
    assert snapshot.autonomous_remediation_allowed is False
    assert snapshot.benchmark_scoring_allowed_from_restoration is False
    assert snapshot.human_approval_required is True

    assert snapshot.restoration_plan_view["summary"]["real_tool_execution_performed"] is False
    assert snapshot.approval_packet_view["summary"]["real_tool_execution_performed"] is False
    assert snapshot.decision_view["summary"]["real_tool_execution_performed"] is False


def test_restoration_observation_summary_is_view_ready():
    snapshot = _snapshot()

    assert summarize_restoration_observation(snapshot) == {
        "snapshot_id": "governed-restoration-observation::composition-structural-001",
        "source_plan_id": "sprint4d-cross-cluster-restoration-plan-001",
        "source_packet_id": "sprint4d-restoration-approval-packet-001",
        "decision_validation_id": "operator-decision-validation-001",
        "restoration_plan_state": "BLOCKED_PENDING_APPROVAL",
        "approval_packet_state": "BLOCKED_PENDING_HUMAN_DECISION",
        "safe_restoration_state": "MORE_EVIDENCE_REQUESTED",
        "action_candidate_count": 3,
        "evidence_reference_count": 4,
        "operator_decision_accepted": True,
        "blocked_action_count": 10,
        "real_tool_execution_performed": False,
        "autonomous_remediation_allowed": False,
        "benchmark_scoring_allowed_from_restoration": False,
        "human_approval_required": True,
    }


def test_restoration_observation_view_model_is_json_serializable():
    snapshot = _snapshot()

    serialized = json.dumps(to_view_model(snapshot), indent=2)

    assert "governed-restoration-observation::composition-structural-001" in serialized
    assert "cross_cluster_restoration_plan" in serialized
    assert "human_approval_packet" in serialized
    assert "operator_decision_record" in serialized
    assert "MORE_EVIDENCE_REQUESTED" in serialized
    assert "blocked_actions" in serialized


def test_restoration_observation_module_does_not_execute_real_tools_or_score_benchmark():
    source = Path("src/eaios/sprint4/governed_restoration_observation.py").read_text(
        encoding="utf-8"
    )

    assert "subprocess" not in source
    assert "import requests" not in source.lower()
    assert "import httpx" not in source.lower()
    assert "execute_tool(" not in source
    assert "restart_service(" not in source
    assert "score_benchmark_result(" not in source
