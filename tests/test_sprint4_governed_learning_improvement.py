from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint4.governed_learning_improvement import (
    ImprovementDisposition,
    ImprovementTarget,
    build_governed_learning_improvement_snapshot,
    summarize_learning_improvement_snapshot,
    to_view_model,
)


def _snapshot():
    return build_governed_learning_improvement_snapshot()


def test_learning_improvement_snapshot_builds_from_collective_learning():
    snapshot = _snapshot()

    assert snapshot.snapshot_id == "governed-learning-improvement::composition-structural-001"
    assert snapshot.source_learning_snapshot_id == (
        "governed-collective-learning::composition-structural-001"
    )
    assert snapshot.provenance == "governed_learning_improvement:snapshot"


def test_learning_improvement_snapshot_contains_three_review_only_records():
    snapshot = _snapshot()

    assert len(snapshot.improvement_records) == 3

    assert tuple(record.disposition for record in snapshot.improvement_records) == (
        ImprovementDisposition.REVIEW_ONLY_CANDIDATE,
        ImprovementDisposition.REVIEW_ONLY_CANDIDATE,
        ImprovementDisposition.REVIEW_ONLY_CANDIDATE,
    )


def test_learning_improvement_targets_are_expected_dashboard_improvements():
    snapshot = _snapshot()

    targets = tuple(record.target for record in snapshot.improvement_records)

    assert targets == (
        ImprovementTarget.RESTORATION_DASHBOARD,
        ImprovementTarget.SERVICE_OWNER_REVIEW_PROMPT,
        ImprovementTarget.DEGRADED_MODE_EXPLANATION,
    )


def test_dashboard_conflict_staleness_improvement_is_review_only():
    snapshot = _snapshot()

    record = next(
        item for item in snapshot.improvement_records
        if item.improvement_id == "improvement-dashboard-conflict-staleness-001"
    )

    assert record.target == ImprovementTarget.RESTORATION_DASHBOARD
    assert "conflict and staleness" in record.title
    assert "payment conflict and stale-knowledge warnings" in record.proposed_change
    assert record.requires_human_review is True
    assert record.can_update_benchmark_truth is False
    assert record.can_score_benchmark is False
    assert record.can_enable_autonomous_remediation is False
    assert record.can_execute_real_tools is False


def test_service_owner_prompt_improvement_is_review_only():
    snapshot = _snapshot()

    record = next(
        item for item in snapshot.improvement_records
        if item.improvement_id == "improvement-service-owner-risk-prompt-001"
    )

    assert record.target == ImprovementTarget.SERVICE_OWNER_REVIEW_PROMPT
    assert "service-owner prompt" in record.title
    assert "risky, incomplete, or dependency-impacting" in record.proposed_change
    assert record.requires_human_review is True
    assert record.can_update_benchmark_truth is False
    assert record.can_score_benchmark is False
    assert record.can_enable_autonomous_remediation is False
    assert record.can_execute_real_tools is False


def test_degraded_mode_improvement_is_review_only():
    snapshot = _snapshot()

    record = next(
        item for item in snapshot.improvement_records
        if item.improvement_id == "improvement-denied-tool-degraded-mode-001"
    )

    assert record.target == ImprovementTarget.DEGRADED_MODE_EXPLANATION
    assert "denied remediation requests" in record.title
    assert "degraded-mode explanation" in record.proposed_change
    assert record.requires_human_review is True
    assert record.can_update_benchmark_truth is False
    assert record.can_score_benchmark is False
    assert record.can_enable_autonomous_remediation is False
    assert record.can_execute_real_tools is False


def test_learning_improvement_records_preserve_learning_event_and_feedback_provenance():
    snapshot = _snapshot()

    for record in snapshot.improvement_records:
        assert record.source_learning_event_ids == (
            "learning-event-operator-feedback-001",
            "learning-event-decision-outcome-001",
        )
        assert record.source_feedback_ids == (
            "operator-feedback-more-evidence-001",
            "operator-feedback-denied-tool-001",
        )
        assert record.provenance.startswith("governed_learning_improvement:")


def test_learning_improvement_records_preserve_safety_constraints():
    snapshot = _snapshot()

    for record in snapshot.improvement_records:
        assert record.safety_constraints == (
            "review_only_candidate",
            "human_review_required",
            "must_not_update_benchmark_truth",
            "must_not_score_benchmark",
            "must_not_enable_autonomous_remediation",
            "must_not_execute_real_tools",
        )
        assert record.blocked_updates == (
            "benchmark_truth_update",
            "benchmark_score_update",
            "autonomous_remediation_policy_change",
            "real_tool_execution",
            "production_knowledge_auto_approval",
        )


def test_learning_improvement_snapshot_review_queue_is_stable():
    snapshot = _snapshot()

    assert snapshot.review_queue == (
        "improvement-dashboard-conflict-staleness-001",
        "improvement-service-owner-risk-prompt-001",
        "improvement-denied-tool-degraded-mode-001",
    )


def test_learning_improvement_policy_blocks_unsafe_updates():
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

    assert snapshot.human_review_required is True
    assert snapshot.benchmark_truth_update_allowed is False
    assert snapshot.benchmark_scoring_allowed_from_improvements is False
    assert snapshot.autonomous_policy_change_allowed is False
    assert snapshot.real_tool_execution_performed is False


def test_learning_improvement_summary_is_view_ready():
    snapshot = _snapshot()

    assert summarize_learning_improvement_snapshot(snapshot) == {
        "snapshot_id": "governed-learning-improvement::composition-structural-001",
        "source_learning_snapshot_id": (
            "governed-collective-learning::composition-structural-001"
        ),
        "improvement_record_count": 3,
        "review_queue_count": 3,
        "blocked_update_count": 5,
        "targets": (
            "RESTORATION_DASHBOARD",
            "SERVICE_OWNER_REVIEW_PROMPT",
            "DEGRADED_MODE_EXPLANATION",
        ),
        "dispositions": (
            "REVIEW_ONLY_CANDIDATE",
            "REVIEW_ONLY_CANDIDATE",
            "REVIEW_ONLY_CANDIDATE",
        ),
        "human_review_required": True,
        "benchmark_truth_update_allowed": False,
        "benchmark_scoring_allowed_from_improvements": False,
        "autonomous_policy_change_allowed": False,
        "real_tool_execution_performed": False,
    }


def test_learning_improvement_view_model_is_json_serializable():
    snapshot = _snapshot()

    serialized = json.dumps(to_view_model(snapshot), indent=2)

    assert "governed-learning-improvement::composition-structural-001" in serialized
    assert "improvement-dashboard-conflict-staleness-001" in serialized
    assert "improvement-service-owner-risk-prompt-001" in serialized
    assert "improvement-denied-tool-degraded-mode-001" in serialized
    assert "benchmark_scoring_allowed_from_improvements" in serialized


def test_learning_improvement_module_does_not_execute_real_tools_or_score_benchmark():
    source = Path("src/eaios/sprint4/governed_learning_improvement.py").read_text(
        encoding="utf-8"
    )

    assert "subprocess" not in source
    assert "import requests" not in source.lower()
    assert "import httpx" not in source.lower()
    assert "execute_tool(" not in source
    assert "restart_service(" not in source
    assert "score_benchmark_result(" not in source
