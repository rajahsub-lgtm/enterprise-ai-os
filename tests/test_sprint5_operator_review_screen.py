from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint5.operator_review_screen import (
    OperatorDecisionControlState,
    OperatorReviewScreenMode,
    OperatorReviewScreenSection,
    build_operator_review_screen_model,
    summarize_operator_review_screen,
    to_view_model,
)


def _screen():
    return build_operator_review_screen_model()


def test_operator_review_screen_builds_from_scenario_command():
    screen = _screen()

    assert screen.screen_id == "sprint5-operator-review-screen-001"
    assert screen.source_command_result_id == "sprint5-scenario-command-result-001"
    assert screen.mode == OperatorReviewScreenMode.READ_ONLY_REVIEW
    assert screen.title == "EAIOS Operator Review Screen"
    assert screen.provenance == "operator_review_screen:screen_model"


def test_operator_review_screen_has_read_only_banner():
    screen = _screen()

    assert "READ ONLY SCREEN" in screen.banner
    assert "decision controls are disabled" in screen.banner
    assert "no shell command" in screen.banner
    assert "tool call" in screen.banner
    assert "provider call" in screen.banner
    assert "remediation" in screen.banner
    assert "benchmark scoring" in screen.banner


def test_operator_review_screen_has_expected_section_cards():
    screen = _screen()

    assert len(screen.section_cards) == 5

    sections = tuple(card.section for card in screen.section_cards)

    assert sections == (
        OperatorReviewScreenSection.SCENARIO_CONTEXT,
        OperatorReviewScreenSection.COMMAND_OUTPUT,
        OperatorReviewScreenSection.GOVERNANCE_CHECKS,
        OperatorReviewScreenSection.BLOCKED_ACTIONS,
        OperatorReviewScreenSection.HUMAN_REVIEW_CONTROLS,
    )

    for card in screen.section_cards:
        assert card.review_required is True
        assert card.provenance.startswith("operator_review_screen:")


def test_operator_review_screen_decision_controls_are_disabled():
    screen = _screen()

    assert len(screen.decision_controls) == 4

    for control in screen.decision_controls:
        assert control.disabled is True
        assert control.external_process_required is True
        assert control.can_execute_action is False
        assert control.provenance == "operator_review_screen:decision_control"


def test_operator_review_screen_decision_control_options_are_stable():
    screen = _screen()

    decisions = tuple(control.intended_decision for control in screen.decision_controls)

    assert decisions == (
        "APPROVE_PACKAGE_FOR_MANUAL_EXECUTION",
        "REQUEST_MORE_EVIDENCE",
        "REJECT_PACKAGE",
        "DEFER_TO_SERVICE_OWNER",
    )


def test_operator_review_screen_approve_control_requires_external_process():
    screen = _screen()

    control = next(
        item for item in screen.decision_controls
        if item.intended_decision == "APPROVE_PACKAGE_FOR_MANUAL_EXECUTION"
    )

    assert control.state == OperatorDecisionControlState.EXTERNAL_HUMAN_PROCESS_REQUIRED
    assert "cannot record approval or execute remediation" in control.reason_disabled


def test_operator_review_screen_embeds_command_summary_and_output():
    screen = _screen()

    assert screen.command_summary["result_id"] == "sprint5-scenario-command-result-001"
    assert screen.command_summary["state"] == "COMPLETED_READ_ONLY"
    assert screen.command_summary["all_governance_checks_passed"] is True

    assert isinstance(screen.rendered_command_output, str)
    assert "EAIOS Sprint 5 Operator Demo" in screen.rendered_command_output


def test_operator_review_screen_embeds_command_view_model():
    screen = _screen()

    assert screen.command_view["summary"]["result_id"] == "sprint5-scenario-command-result-001"
    assert screen.command_view["summary"]["real_shell_command_executed"] is False
    assert screen.command_view["summary"]["benchmark_scoring_allowed_from_command"] is False


def test_operator_review_screen_preserves_governance_checks():
    screen = _screen()

    assert screen.governance_checks["real_shell_command_not_executed"] is True
    assert screen.governance_checks["command_invocation_read_only"] is True
    assert screen.governance_checks["supported_command"] is True
    assert screen.governance_checks["supported_output_format"] is True
    assert screen.governance_checks["application_health_scenario"] is True
    assert all(screen.governance_checks.values()) is True


def test_operator_review_screen_preserves_blocked_actions():
    screen = _screen()

    assert len(screen.blocked_actions) == 16
    assert "execute_remediation" in screen.blocked_actions
    assert "restart_service" in screen.blocked_actions
    assert "benchmark_truth_update" in screen.blocked_actions
    assert "benchmark_score_update" in screen.blocked_actions
    assert "score_benchmark_from_operator_export" in screen.blocked_actions
    assert "apply_dashboard_changes_automatically" in screen.blocked_actions


def test_operator_review_screen_preserves_no_execution_boundaries():
    screen = _screen()

    assert screen.real_shell_command_executed is False
    assert screen.real_tool_execution_performed is False
    assert screen.provider_call_performed is False
    assert screen.dashboard_changes_applied is False
    assert screen.benchmark_scoring_allowed_from_screen is False
    assert screen.autonomous_remediation_allowed is False
    assert screen.human_review_required is True


def test_operator_review_screen_summary_is_view_ready():
    screen = _screen()

    assert summarize_operator_review_screen(screen) == {
        "screen_id": "sprint5-operator-review-screen-001",
        "source_command_result_id": "sprint5-scenario-command-result-001",
        "mode": "READ_ONLY_REVIEW",
        "section_card_count": 5,
        "decision_control_count": 4,
        "disabled_control_count": 4,
        "blocked_action_count": 16,
        "governance_check_count": 13,
        "all_governance_checks_passed": True,
        "real_shell_command_executed": False,
        "real_tool_execution_performed": False,
        "provider_call_performed": False,
        "dashboard_changes_applied": False,
        "benchmark_scoring_allowed_from_screen": False,
        "autonomous_remediation_allowed": False,
        "human_review_required": True,
    }


def test_operator_review_screen_view_model_is_json_serializable():
    screen = _screen()

    serialized = json.dumps(to_view_model(screen), indent=2)

    assert "sprint5-operator-review-screen-001" in serialized
    assert "READ_ONLY_REVIEW" in serialized
    assert "decision_controls" in serialized
    assert "APPROVE_PACKAGE_FOR_MANUAL_EXECUTION" in serialized
    assert "benchmark_scoring_allowed_from_screen" in serialized


def test_operator_review_screen_module_does_not_execute_real_tools_or_score_benchmark():
    source = Path("src/eaios/sprint5/operator_review_screen.py").read_text(
        encoding="utf-8"
    )

    assert "subprocess" not in source
    assert "import requests" not in source.lower()
    assert "import httpx" not in source.lower()
    assert "execute_tool(" not in source
    assert "restart_service(" not in source
    assert "score_benchmark_result(" not in source
