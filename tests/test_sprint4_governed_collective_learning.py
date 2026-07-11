from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint4.governed_collective_learning import (
    FeedbackSignal,
    LearningEventType,
    LearningSafetyState,
    build_governed_collective_learning_snapshot,
    summarize_collective_learning_snapshot,
    to_view_model,
)


def _snapshot():
    return build_governed_collective_learning_snapshot()


def test_collective_learning_snapshot_builds_from_restoration_observation():
    snapshot = _snapshot()

    assert snapshot.snapshot_id == "governed-collective-learning::composition-structural-001"
    assert snapshot.source_restoration_snapshot_id == (
        "governed-restoration-observation::composition-structural-001"
    )
    assert snapshot.provenance == "governed_collective_learning:snapshot"


def test_collective_learning_captures_operator_feedback_records():
    snapshot = _snapshot()

    assert len(snapshot.feedback_records) == 2

    signals = tuple(record.feedback_signal for record in snapshot.feedback_records)

    assert FeedbackSignal.REQUESTED_MORE_EVIDENCE in signals
    assert FeedbackSignal.RESTORATION_DEFERRED in signals

    for record in snapshot.feedback_records:
        assert record.learning_allowed is True
        assert record.can_update_benchmark_truth is False
        assert record.can_score_benchmark is False
        assert record.can_enable_autonomous_remediation is False
        assert record.human_review_required is True


def test_collective_learning_preserves_feedback_references():
    snapshot = _snapshot()

    first = snapshot.feedback_records[0]
    second = snapshot.feedback_records[1]

    assert first.related_action_ids == (
        "restore-candidate-payment-validate-evidence",
        "restore-candidate-inventory-validate-topology",
    )
    assert "mcp-tool-evidence::mcp-request-read-telemetry-payment" in first.related_evidence_ids
    assert "mcp-tool-evidence::mcp-request-read-topology-inventory" in first.related_evidence_ids

    assert second.related_action_ids == (
        "restore-candidate-cross-cluster-approval-hold",
    )
    assert second.related_evidence_ids == (
        "mcp-tool-evidence::mcp-request-denied-remediation-payment",
    )


def test_collective_learning_records_decision_outcome_history():
    snapshot = _snapshot()

    outcome = snapshot.outcome_history

    assert outcome.outcome_history_id == "decision-outcome-history-001"
    assert outcome.source_decision_validation_id == "operator-decision-validation-001"
    assert outcome.decision == "REQUEST_MORE_EVIDENCE"
    assert outcome.safe_restoration_state == "MORE_EVIDENCE_REQUESTED"
    assert outcome.operator_decision_accepted is True
    assert outcome.outcome_label == "MORE_EVIDENCE_REQUESTED_BY_OPERATOR"
    assert outcome.benchmark_truth_updated is False
    assert outcome.benchmark_score_updated is False
    assert outcome.autonomous_policy_changed is False
    assert outcome.human_review_required is True


def test_collective_learning_records_governed_learning_events():
    snapshot = _snapshot()

    assert len(snapshot.learning_events) == 2

    event_types = tuple(event.event_type for event in snapshot.learning_events)

    assert LearningEventType.OPERATOR_FEEDBACK_CAPTURED in event_types
    assert LearningEventType.DECISION_OUTCOME_RECORDED in event_types

    for event in snapshot.learning_events:
        assert event.safety_state == LearningSafetyState.GOVERNED_LEARNING_ALLOWED
        assert event.requires_human_review is True
        assert event.can_update_benchmark_truth is False
        assert event.can_score_benchmark is False
        assert event.can_enable_autonomous_remediation is False
        assert "benchmark_truth_update" in event.blocked_updates
        assert "autonomous_remediation_policy_change" in event.blocked_updates


def test_collective_learning_policy_blocks_unsafe_updates():
    snapshot = _snapshot()

    assert snapshot.learning_policy == {
        "learning_allowed": True,
        "human_review_required": True,
        "benchmark_truth_update_allowed": False,
        "benchmark_scoring_allowed_from_learning": False,
        "autonomous_policy_change_allowed": False,
        "real_tool_execution_allowed": False,
        "production_knowledge_auto_approval_allowed": False,
    }


def test_collective_learning_improvement_candidates_are_dashboard_ready():
    snapshot = _snapshot()

    assert snapshot.improvement_candidates == (
        "Increase prominence of conflict/staleness warnings in restoration dashboard.",
        "Add service-owner review prompt for risky inventory dependency evidence.",
        "Add degraded-mode explanation when remediation tool requests are denied.",
    )


def test_collective_learning_blocks_benchmark_and_autonomous_updates():
    snapshot = _snapshot()

    assert snapshot.blocked_updates == (
        "benchmark_truth_update",
        "benchmark_score_update",
        "autonomous_remediation_policy_change",
        "real_tool_execution",
        "production_knowledge_auto_approval",
    )
    assert snapshot.human_review_required is True
    assert snapshot.benchmark_truth_update_allowed is False
    assert snapshot.benchmark_scoring_allowed_from_learning is False
    assert snapshot.autonomous_policy_change_allowed is False
    assert snapshot.real_tool_execution_performed is False


def test_collective_learning_summary_is_view_ready():
    snapshot = _snapshot()

    assert summarize_collective_learning_snapshot(snapshot) == {
        "snapshot_id": "governed-collective-learning::composition-structural-001",
        "source_restoration_snapshot_id": (
            "governed-restoration-observation::composition-structural-001"
        ),
        "feedback_record_count": 2,
        "learning_event_count": 2,
        "improvement_candidate_count": 3,
        "blocked_update_count": 5,
        "outcome_label": "MORE_EVIDENCE_REQUESTED_BY_OPERATOR",
        "safe_restoration_state": "MORE_EVIDENCE_REQUESTED",
        "human_review_required": True,
        "benchmark_truth_update_allowed": False,
        "benchmark_scoring_allowed_from_learning": False,
        "autonomous_policy_change_allowed": False,
        "real_tool_execution_performed": False,
    }


def test_collective_learning_view_model_is_json_serializable():
    snapshot = _snapshot()

    serialized = json.dumps(to_view_model(snapshot), indent=2)

    assert "governed-collective-learning::composition-structural-001" in serialized
    assert "operator-feedback-more-evidence-001" in serialized
    assert "decision-outcome-history-001" in serialized
    assert "learning-event-operator-feedback-001" in serialized
    assert "benchmark_truth_update_allowed" in serialized


def test_collective_learning_module_does_not_execute_real_tools_or_score_benchmark():
    source = Path("src/eaios/sprint4/governed_collective_learning.py").read_text(
        encoding="utf-8"
    )

    assert "subprocess" not in source
    assert "import requests" not in source.lower()
    assert "import httpx" not in source.lower()
    assert "execute_tool(" not in source
    assert "restart_service(" not in source
    assert "score_benchmark_result(" not in source
