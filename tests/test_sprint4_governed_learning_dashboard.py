from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint4.governed_learning_dashboard import (
    DashboardDeltaType,
    build_governed_learning_dashboard_snapshot,
    summarize_learning_dashboard_snapshot,
    to_view_model,
)


def _snapshot():
    return build_governed_learning_dashboard_snapshot()


def test_learning_dashboard_snapshot_builds_from_4e_learning_and_improvements():
    snapshot = _snapshot()

    assert snapshot.snapshot_id == "governed-learning-dashboard::composition-structural-001"
    assert snapshot.source_restoration_snapshot_id == (
        "governed-restoration-observation::composition-structural-001"
    )
    assert snapshot.source_learning_snapshot_id == (
        "governed-collective-learning::composition-structural-001"
    )
    assert snapshot.source_improvement_snapshot_id == (
        "governed-learning-improvement::composition-structural-001"
    )
    assert snapshot.provenance == "governed_learning_dashboard:snapshot"


def test_learning_dashboard_contains_before_and_after_states():
    snapshot = _snapshot()

    assert len(snapshot.before_dashboard_state) == 4
    assert len(snapshot.after_dashboard_candidates) == 3

    assert "Restoration dashboard shows action cards and blocked actions." in (
        snapshot.before_dashboard_state
    )
    assert any(
        "payment conflict and stale-knowledge warnings" in candidate
        for candidate in snapshot.after_dashboard_candidates
    )
    assert any(
        "service-owner review prompt" in candidate
        for candidate in snapshot.after_dashboard_candidates
    )
    assert any(
        "degraded-mode explanation" in candidate
        for candidate in snapshot.after_dashboard_candidates
    )


def test_learning_dashboard_creates_three_review_only_deltas():
    snapshot = _snapshot()

    assert len(snapshot.dashboard_deltas) == 3

    for delta in snapshot.dashboard_deltas:
        assert delta.review_only is True
        assert delta.applied_automatically is False
        assert delta.human_review_required is True
        assert delta.can_update_benchmark_truth is False
        assert delta.can_score_benchmark is False
        assert delta.can_enable_autonomous_remediation is False
        assert delta.can_execute_real_tools is False


def test_learning_dashboard_delta_types_are_stable():
    snapshot = _snapshot()

    delta_types = tuple(delta.delta_type for delta in snapshot.dashboard_deltas)

    assert delta_types == (
        DashboardDeltaType.VISIBILITY_IMPROVEMENT,
        DashboardDeltaType.REVIEW_PROMPT_IMPROVEMENT,
        DashboardDeltaType.DEGRADED_MODE_IMPROVEMENT,
    )


def test_learning_dashboard_preserves_improvement_review_queue():
    snapshot = _snapshot()

    assert snapshot.review_queue == (
        "improvement-dashboard-conflict-staleness-001",
        "improvement-service-owner-risk-prompt-001",
        "improvement-denied-tool-degraded-mode-001",
    )


def test_learning_dashboard_blocks_unsafe_updates():
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
    assert snapshot.benchmark_scoring_allowed_from_dashboard is False
    assert snapshot.autonomous_policy_change_allowed is False
    assert snapshot.real_tool_execution_performed is False
    assert snapshot.dashboard_changes_applied is False


def test_learning_dashboard_embeds_restoration_learning_and_improvement_views():
    snapshot = _snapshot()

    assert snapshot.restoration_view["summary"]["snapshot_id"] == (
        "governed-restoration-observation::composition-structural-001"
    )
    assert snapshot.learning_view["summary"]["snapshot_id"] == (
        "governed-collective-learning::composition-structural-001"
    )
    assert snapshot.improvement_view["summary"]["snapshot_id"] == (
        "governed-learning-improvement::composition-structural-001"
    )


def test_learning_dashboard_summary_is_view_ready():
    snapshot = _snapshot()

    assert summarize_learning_dashboard_snapshot(snapshot) == {
        "snapshot_id": "governed-learning-dashboard::composition-structural-001",
        "source_restoration_snapshot_id": (
            "governed-restoration-observation::composition-structural-001"
        ),
        "source_learning_snapshot_id": (
            "governed-collective-learning::composition-structural-001"
        ),
        "source_improvement_snapshot_id": (
            "governed-learning-improvement::composition-structural-001"
        ),
        "before_state_count": 4,
        "after_candidate_count": 3,
        "dashboard_delta_count": 3,
        "review_queue_count": 3,
        "blocked_update_count": 5,
        "dashboard_changes_applied": False,
        "human_review_required": True,
        "benchmark_truth_update_allowed": False,
        "benchmark_scoring_allowed_from_dashboard": False,
        "autonomous_policy_change_allowed": False,
        "real_tool_execution_performed": False,
    }


def test_learning_dashboard_view_model_is_json_serializable():
    snapshot = _snapshot()

    serialized = json.dumps(to_view_model(snapshot), indent=2)

    assert "governed-learning-dashboard::composition-structural-001" in serialized
    assert "before_dashboard_state" in serialized
    assert "after_dashboard_candidates" in serialized
    assert "dashboard_deltas" in serialized
    assert "benchmark_scoring_allowed_from_dashboard" in serialized
    assert "dashboard_changes_applied" in serialized


def test_learning_dashboard_module_does_not_execute_real_tools_or_score_benchmark():
    source = Path("src/eaios/sprint4/governed_learning_dashboard.py").read_text(
        encoding="utf-8"
    )

    assert "subprocess" not in source
    assert "import requests" not in source.lower()
    assert "import httpx" not in source.lower()
    assert "execute_tool(" not in source
    assert "restart_service(" not in source
    assert "score_benchmark_result(" not in source
