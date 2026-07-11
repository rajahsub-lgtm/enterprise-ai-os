from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint5.demo_runner import (
    DemoRunMode,
    DemoRunStage,
    run_sprint5_operator_demo,
    summarize_demo_run,
    to_view_model,
)


def _result():
    return run_sprint5_operator_demo()


def test_sprint5_demo_runner_builds_read_only_demo_result():
    result = _result()

    assert result.run_id == "sprint5-operator-demo-run-001"
    assert result.mode == DemoRunMode.READ_ONLY_LOCAL
    assert result.source_export_id == "sprint5-operator-dashboard-export-001"
    assert result.provenance == "demo_runner:sprint5_operator_demo"


def test_sprint5_demo_runner_has_expected_steps():
    result = _result()

    assert len(result.steps) == 5

    stages = tuple(step.stage for step in result.steps)

    assert stages == (
        DemoRunStage.LOAD_OPERATOR_EXPORT,
        DemoRunStage.RENDER_MARKDOWN,
        DemoRunStage.RENDER_JSON_VIEW_MODEL,
        DemoRunStage.RENDER_CLI_TEXT,
        DemoRunStage.VERIFY_GOVERNANCE_BOUNDARIES,
    )


def test_sprint5_demo_runner_steps_are_read_only():
    result = _result()

    for step in result.steps:
        assert step.status == "COMPLETED_READ_ONLY"
        assert step.read_only is True
        assert step.performed_external_action is False
        assert step.provenance.startswith("demo_runner:")


def test_sprint5_demo_runner_embeds_operator_export_summary():
    result = _result()

    assert result.export_summary["export_id"] == "sprint5-operator-dashboard-export-001"
    assert result.export_summary["card_count"] == 5
    assert result.export_summary["blocked_card_count"] == 3
    assert result.export_summary["review_required_card_count"] == 5
    assert result.export_summary["benchmark_scoring_allowed_from_export"] is False


def test_sprint5_demo_runner_renders_markdown_and_cli_text():
    result = _result()

    assert "# EAIOS Operator Dashboard Export" in result.rendered_markdown
    assert "Safety: READ ONLY" in result.rendered_markdown
    assert "## Operator Cards" in result.rendered_markdown

    assert "EAIOS Sprint 5 Operator Demo" in result.rendered_cli_text
    assert "Mode: READ_ONLY_LOCAL" in result.rendered_cli_text
    assert "Safety: no tools, no providers, no remediation, no benchmark scoring" in (
        result.rendered_cli_text
    )


def test_sprint5_demo_runner_embeds_json_view_model():
    result = _result()

    assert result.rendered_json_view_model["summary"]["export_id"] == (
        "sprint5-operator-dashboard-export-001"
    )
    assert result.rendered_json_view_model["summary"]["mode"] == "READ_ONLY_DEMO"
    assert result.rendered_json_view_model["summary"]["human_review_required"] is True


def test_sprint5_demo_runner_preserves_blocked_actions():
    result = _result()

    assert len(result.blocked_actions) == 16
    assert "benchmark_truth_update" in result.blocked_actions
    assert "benchmark_score_update" in result.blocked_actions
    assert "autonomous_remediation_policy_change" in result.blocked_actions
    assert "real_tool_execution" in result.blocked_actions
    assert "execute_remediation" in result.blocked_actions
    assert "restart_service" in result.blocked_actions
    assert "score_benchmark_from_operator_export" in result.blocked_actions
    assert "apply_dashboard_changes_automatically" in result.blocked_actions


def test_sprint5_demo_runner_governance_checks_pass():
    result = _result()

    assert result.governance_checks == {
        "real_tool_execution_performed": True,
        "provider_call_performed": True,
        "dashboard_changes_applied": True,
        "benchmark_scoring_allowed_from_demo": True,
        "autonomous_remediation_allowed": True,
        "human_review_required": True,
        "all_steps_read_only": True,
        "no_step_performed_external_action": True,
    }


def test_sprint5_demo_runner_preserves_no_execution_boundaries():
    result = _result()

    assert result.real_tool_execution_performed is False
    assert result.provider_call_performed is False
    assert result.dashboard_changes_applied is False
    assert result.benchmark_scoring_allowed_from_demo is False
    assert result.autonomous_remediation_allowed is False
    assert result.human_review_required is True


def test_sprint5_demo_runner_summary_is_view_ready():
    result = _result()

    assert summarize_demo_run(result) == {
        "run_id": "sprint5-operator-demo-run-001",
        "mode": "READ_ONLY_LOCAL",
        "source_export_id": "sprint5-operator-dashboard-export-001",
        "step_count": 5,
        "blocked_action_count": 16,
        "governance_check_count": 8,
        "all_governance_checks_passed": True,
        "real_tool_execution_performed": False,
        "provider_call_performed": False,
        "dashboard_changes_applied": False,
        "benchmark_scoring_allowed_from_demo": False,
        "autonomous_remediation_allowed": False,
        "human_review_required": True,
    }


def test_sprint5_demo_runner_view_model_is_json_serializable():
    result = _result()

    serialized = json.dumps(to_view_model(result), indent=2)

    assert "sprint5-operator-demo-run-001" in serialized
    assert "LOAD_OPERATOR_EXPORT" in serialized
    assert "RENDER_MARKDOWN" in serialized
    assert "rendered_cli_text" in serialized
    assert "benchmark_scoring_allowed_from_demo" in serialized


def test_sprint5_demo_runner_module_does_not_execute_real_tools_or_score_benchmark():
    source = Path("src/eaios/sprint5/demo_runner.py").read_text(encoding="utf-8")

    assert "subprocess" not in source
    assert "import requests" not in source.lower()
    assert "import httpx" not in source.lower()
    assert "execute_tool(" not in source
    assert "restart_service(" not in source
    assert "score_benchmark_result(" not in source
