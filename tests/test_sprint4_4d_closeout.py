from pathlib import Path


CLOSEOUT = Path("docs/EAIOS_2_SPRINT_4D_CLOSEOUT.md")

REQUIRED_FILES = [
    Path("src/eaios/sprint4/governed_restoration_orchestration.py"),
    Path("src/eaios/sprint4/governed_restoration_approval_packet.py"),
    Path("src/eaios/sprint4/governed_restoration_decision.py"),
    Path("src/eaios/sprint4/governed_restoration_observation.py"),
    Path("tests/test_sprint4_governed_restoration_orchestration.py"),
    Path("tests/test_sprint4_governed_restoration_approval_packet.py"),
    Path("tests/test_sprint4_governed_restoration_decision.py"),
    Path("tests/test_sprint4_governed_restoration_observation.py"),
]


def _text() -> str:
    return CLOSEOUT.read_text(encoding="utf-8")


def test_sprint4_4d_closeout_file_exists():
    assert CLOSEOUT.exists()


def test_sprint4_4d_required_files_exist():
    missing = [str(path) for path in REQUIRED_FILES if not path.exists()]
    assert missing == []


def test_sprint4_4d_closeout_lists_completed_slices():
    text = _text()

    assert "4D-1 Cross-cluster restoration orchestration plan" in text
    assert "4D-2 Human approval packet for restoration" in text
    assert "4D-3 Operator decision record and safe restoration state machine" in text
    assert "4D-4 Governed restoration observation snapshot" in text
    assert "4D-5 Closeout contract and architecture checkpoint" in text


def test_sprint4_4d_closeout_locks_layer_boundary():
    text = _text()

    assert "Layer 14: Cross-cluster restoration orchestration plan" in text
    assert "Layer 15: Human approval packet" in text
    assert "Layer 16: Operator decision record and safe state machine" in text
    assert "Layer 17: Governed restoration observation snapshot" in text


def test_sprint4_4d_closeout_states_core_thesis():
    text = _text()

    assert "Restoration can be orchestrated." in text
    assert "Restoration cannot be executed autonomously." in text
    assert "Approval can be packaged." in text
    assert "Approval cannot bypass governance." in text
    assert "Operator decisions can be validated." in text
    assert "Operator decisions cannot score benchmarks." in text
    assert "Denied tool constraints remain visible." in text
    assert "Human approval remains required." in text


def test_sprint4_4d_closeout_documents_restoration_plan_contract():
    text = _text()

    assert "CrossClusterRestorationPlan" in text
    assert "RestorationActionCandidate" in text
    assert "RestorationActionType" in text
    assert "RestorationRiskLevel" in text
    assert "RestorationPlanState" in text
    assert "BLOCKED_PENDING_APPROVAL" in text


def test_sprint4_4d_closeout_documents_restoration_actions_and_blocks():
    text = _text()

    assert "can_execute_autonomously = false" in text
    assert "human_approval_required = true" in text
    assert "benchmark_scoring_allowed = false" in text
    assert "VALIDATE_EVIDENCE" in text
    assert "HOLD_FOR_APPROVAL" in text
    assert "restart_service" in text
    assert "score_benchmark_from_restoration" in text


def test_sprint4_4d_closeout_documents_approval_packet():
    text = _text()

    assert "RestorationApprovalPacket" in text
    assert "ApprovalEvidenceReference" in text
    assert "OperatorDecisionRecordTemplate" in text
    assert "ApprovalDecisionOption" in text
    assert "ApprovalPacketState" in text
    assert "BLOCKED_PENDING_HUMAN_DECISION" in text


def test_sprint4_4d_closeout_documents_allowed_operator_decisions():
    text = _text()

    assert "APPROVE_PACKAGE_FOR_MANUAL_EXECUTION" in text
    assert "REQUEST_MORE_EVIDENCE" in text
    assert "REJECT_PACKAGE" in text
    assert "DEFER_TO_SERVICE_OWNER" in text
    assert "Approval means manual operator execution only." in text


def test_sprint4_4d_closeout_documents_operator_decision_record():
    text = _text()

    assert "OperatorDecisionInput" in text
    assert "OperatorDecisionValidation" in text
    assert "OperatorDecisionValidationState" in text
    assert "SafeRestorationState" in text
    assert "REQUEST_MORE_EVIDENCE" in text
    assert "MORE_EVIDENCE_REQUESTED" in text


def test_sprint4_4d_closeout_documents_safe_state_machine():
    text = _text()

    assert "PENDING_OPERATOR_DECISION" in text
    assert "APPROVED_FOR_MANUAL_EXECUTION_ONLY" in text
    assert "MORE_EVIDENCE_REQUESTED" in text
    assert "REJECTED_BY_OPERATOR" in text
    assert "DEFERRED_TO_SERVICE_OWNER" in text
    assert "BLOCKED_INVALID_DECISION" in text
    assert "The state machine never enters an autonomous execution state." in text


def test_sprint4_4d_closeout_documents_observation_snapshot():
    text = _text()

    assert "GovernedRestorationObservationSnapshot" in text
    assert "restoration_summary" in text
    assert "approval_summary" in text
    assert "decision_summary" in text
    assert "action_cards" in text
    assert "blocked_actions" in text


def test_sprint4_4d_closeout_preserves_governance_boundaries():
    text = _text()

    assert "cross_cluster_restoration_plan_required" in text
    assert "human_approval_packet_required" in text
    assert "operator_decision_record_required" in text
    assert "safe_state_machine_required" in text
    assert "manual_execution_only" in text
    assert "autonomous_remediation_disabled" in text
    assert "real_tool_execution_blocked" in text
    assert "benchmark_scoring_from_restoration_blocked" in text
    assert "denied_tool_constraints_preserved" in text
    assert "service_owner_review_required" in text
    assert "rollback_review_required" in text
    assert "communications_review_required" in text


def test_sprint4_4d_closeout_preserves_benchmark_separation():
    text = _text()

    assert "Restoration output cannot define benchmark truth." in text
    assert "Restoration output cannot score benchmark results." in text
    assert "Approval output cannot define benchmark truth." in text
    assert "Approval output cannot score benchmark results." in text
    assert "Operator decision output cannot define benchmark truth." in text
    assert "Operator decision output cannot score benchmark results." in text
    assert "Manual execution approval cannot change benchmark scoring." in text


def test_sprint4_4d_closeout_documents_human_approval_boundary():
    text = _text()

    assert "compose restoration candidates" in text
    assert "prepare human approval packets" in text
    assert "validate operator decisions" in text
    assert "record safe restoration state" in text
    assert "execute remediation" in text
    assert "write to production" in text


def test_sprint4_4d_closeout_sets_4e_entry_criteria():
    text = _text()

    assert "cross-cluster restoration plan" in text
    assert "human approval packet" in text
    assert "operator decision record" in text
    assert "safe restoration state machine" in text
    assert "governed restoration observation snapshot" in text
    assert "manual-execution-only boundary" in text
    assert "no-autonomous-remediation boundary" in text
    assert "benchmark separation" in text


def test_sprint4_4d_closeout_defines_4e_direction():
    text = _text()

    assert "operator feedback capture" in text
    assert "decision outcome history" in text
    assert "learning event contract" in text
    assert "recommendation improvement record" in text
    assert "governed learning policy" in text
    assert "before-after dashboard summary" in text
    assert "learning-safe evidence update" in text
    assert "future restoration improvement suggestions" in text
