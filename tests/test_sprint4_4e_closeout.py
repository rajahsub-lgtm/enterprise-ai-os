from pathlib import Path


CLOSEOUT = Path("docs/EAIOS_2_SPRINT_4E_CLOSEOUT.md")

REQUIRED_FILES = [
    Path("src/eaios/sprint4/governed_collective_learning.py"),
    Path("src/eaios/sprint4/governed_learning_improvement.py"),
    Path("src/eaios/sprint4/governed_learning_dashboard.py"),
    Path("tests/test_sprint4_governed_collective_learning.py"),
    Path("tests/test_sprint4_governed_learning_improvement.py"),
    Path("tests/test_sprint4_governed_learning_dashboard.py"),
]


def _text() -> str:
    return CLOSEOUT.read_text(encoding="utf-8")


def test_sprint4_4e_closeout_file_exists():
    assert CLOSEOUT.exists()


def test_sprint4_4e_required_files_exist():
    missing = [str(path) for path in REQUIRED_FILES if not path.exists()]
    assert missing == []


def test_sprint4_4e_closeout_lists_completed_slices():
    text = _text()

    assert "4E-1 Governed collective learning event contract" in text
    assert "4E-2 Governed recommendation improvement records" in text
    assert "4E-3 Governed learning dashboard snapshot" in text
    assert "4E-4 Closeout contract and architecture checkpoint" in text


def test_sprint4_4e_closeout_locks_layer_boundary():
    text = _text()

    assert "Layer 18: Governed collective learning snapshot" in text
    assert "Layer 19: Governed recommendation improvement records" in text
    assert "Layer 20: Governed learning dashboard snapshot" in text


def test_sprint4_4e_closeout_states_core_thesis():
    text = _text()

    assert "Learning can capture feedback." in text
    assert "Learning can record operator outcomes." in text
    assert "Learning can propose improvements." in text
    assert "Learning cannot update benchmark truth." in text
    assert "Learning cannot score benchmarks." in text
    assert "Learning cannot enable autonomous remediation." in text
    assert "Learning remains human-reviewed and governed." in text


def test_sprint4_4e_closeout_documents_collective_learning_contract():
    text = _text()

    assert "OperatorFeedbackRecord" in text
    assert "DecisionOutcomeHistory" in text
    assert "GovernedLearningEvent" in text
    assert "GovernedCollectiveLearningSnapshot" in text
    assert "FeedbackSignal" in text
    assert "LearningEventType" in text
    assert "LearningSafetyState" in text


def test_sprint4_4e_closeout_documents_learning_policy():
    text = _text()

    assert "learning_allowed = true" in text
    assert "human_review_required = true" in text
    assert "benchmark_truth_update_allowed = false" in text
    assert "benchmark_scoring_allowed_from_learning = false" in text
    assert "autonomous_policy_change_allowed = false" in text
    assert "real_tool_execution_allowed = false" in text
    assert "production_knowledge_auto_approval_allowed = false" in text


def test_sprint4_4e_closeout_documents_improvement_records():
    text = _text()

    assert "RecommendationImprovementRecord" in text
    assert "GovernedLearningImprovementSnapshot" in text
    assert "ImprovementTarget" in text
    assert "ImprovementDisposition" in text
    assert "RESTORATION_DASHBOARD" in text
    assert "SERVICE_OWNER_REVIEW_PROMPT" in text
    assert "DEGRADED_MODE_EXPLANATION" in text
    assert "REVIEW_ONLY_CANDIDATE" in text


def test_sprint4_4e_closeout_documents_dashboard_contract():
    text = _text()

    assert "GovernedDashboardDelta" in text
    assert "GovernedLearningDashboardSnapshot" in text
    assert "DashboardDeltaType" in text
    assert "VISIBILITY_IMPROVEMENT" in text
    assert "REVIEW_PROMPT_IMPROVEMENT" in text
    assert "DEGRADED_MODE_IMPROVEMENT" in text
    assert "before_dashboard_state" in text
    assert "after_dashboard_candidates" in text
    assert "dashboard_deltas" in text


def test_sprint4_4e_closeout_documents_blocked_updates():
    text = _text()

    assert "benchmark_truth_update" in text
    assert "benchmark_score_update" in text
    assert "autonomous_remediation_policy_change" in text
    assert "real_tool_execution" in text
    assert "production_knowledge_auto_approval" in text


def test_sprint4_4e_closeout_preserves_governance_boundaries():
    text = _text()

    assert "operator_feedback_capture_allowed" in text
    assert "decision_outcome_history_allowed" in text
    assert "recommendation_improvement_candidates_allowed" in text
    assert "dashboard_delta_candidates_allowed" in text
    assert "human_review_required" in text
    assert "review_only_candidates" in text
    assert "benchmark_truth_update_blocked" in text
    assert "benchmark_scoring_from_learning_blocked" in text
    assert "autonomous_policy_change_blocked" in text
    assert "real_tool_execution_blocked" in text
    assert "dashboard_changes_not_applied_automatically" in text


def test_sprint4_4e_closeout_preserves_benchmark_separation():
    text = _text()

    assert "Learning output cannot define benchmark truth." in text
    assert "Learning output cannot score benchmark results." in text
    assert "Improvement output cannot define benchmark truth." in text
    assert "Improvement output cannot score benchmark results." in text
    assert "Dashboard output cannot define benchmark truth." in text
    assert "Dashboard output cannot score benchmark results." in text
    assert "Operator feedback cannot change benchmark scoring." in text


def test_sprint4_4e_closeout_documents_human_review_boundary():
    text = _text()

    assert "capture operator feedback" in text
    assert "record decision outcome history" in text
    assert "propose improvement candidates" in text
    assert "prepare review queue" in text
    assert "show before and after dashboard candidates" in text
    assert "apply improvements automatically" in text
    assert "approve production knowledge automatically" in text


def test_sprint4_4e_closeout_sets_final_closeout_entry_criteria():
    text = _text()

    assert "governed collective learning snapshot" in text
    assert "operator feedback capture" in text
    assert "decision outcome history" in text
    assert "recommendation improvement records" in text
    assert "review-only improvement queue" in text
    assert "governed learning dashboard snapshot" in text
    assert "no-benchmark-truth-update boundary" in text
    assert "human review boundary" in text


def test_sprint4_4e_closeout_defines_final_sprint4_direction():
    text = _text()

    assert "4A benchmark-grounded environment and observation" in text
    assert "4B governed KB and LLM reasoning boundary" in text
    assert "4C governed MCP/tool boundary" in text
    assert "4D governed restoration orchestration boundary" in text
    assert "4E governed collective learning and dashboard improvement" in text
    assert "EAIOS reasons over and governs knowledge and records" in text
