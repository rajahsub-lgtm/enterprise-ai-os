from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint5.scenario_command import (
    ScenarioCommandInvocation,
    ScenarioCommandName,
    ScenarioCommandState,
    ScenarioOutputFormat,
    build_default_scenario_command_invocation,
    run_sprint5_scenario_command,
    summarize_scenario_command_result,
    to_view_model,
)


def _result():
    return run_sprint5_scenario_command()


def test_default_scenario_command_invocation_is_read_only_application_health():
    invocation = build_default_scenario_command_invocation()

    assert invocation.invocation_id == "sprint5-scenario-command-invocation-001"
    assert invocation.command_name == ScenarioCommandName.RUN_APPLICATION_HEALTH_DEMO
    assert invocation.output_format == ScenarioOutputFormat.CLI_TEXT
    assert invocation.scenario_name == "application-health"
    assert invocation.read_only is True
    assert invocation.requested_by == "operator-demo"
    assert invocation.command_path == (
        "eaios sprint5 run --scenario application-health --read-only"
    )


def test_scenario_command_runs_default_read_only_path():
    result = _result()

    assert result.result_id == "sprint5-scenario-command-result-001"
    assert result.invocation_id == "sprint5-scenario-command-invocation-001"
    assert result.command_name == "RUN_APPLICATION_HEALTH_DEMO"
    assert result.output_format == "CLI_TEXT"
    assert result.scenario_name == "application-health"
    assert result.state == ScenarioCommandState.COMPLETED_READ_ONLY
    assert result.source_demo_run_id == "sprint5-operator-demo-run-001"
    assert result.provenance == "scenario_command:read_only_application_health_command"


def test_scenario_command_renders_cli_text_by_default():
    result = _result()

    assert isinstance(result.rendered_output, str)
    assert "EAIOS Sprint 5 Operator Demo" in result.rendered_output
    assert "Mode: READ_ONLY_LOCAL" in result.rendered_output
    assert "Safety: no tools, no providers, no remediation, no benchmark scoring" in (
        result.rendered_output
    )


def test_scenario_command_supports_markdown_output():
    invocation = ScenarioCommandInvocation(
        invocation_id="sprint5-scenario-command-invocation-markdown-001",
        command_name=ScenarioCommandName.EXPORT_OPERATOR_DASHBOARD,
        output_format=ScenarioOutputFormat.MARKDOWN,
        scenario_name="application-health",
        read_only=True,
        requested_by="operator-demo",
        command_path="eaios sprint5 export --scenario application-health --format markdown --read-only",
    )

    result = run_sprint5_scenario_command(invocation)

    assert result.state == ScenarioCommandState.COMPLETED_READ_ONLY
    assert result.command_name == "EXPORT_OPERATOR_DASHBOARD"
    assert result.output_format == "MARKDOWN"
    assert isinstance(result.rendered_output, str)
    assert "# EAIOS Operator Dashboard Export" in result.rendered_output
    assert "Safety: READ ONLY" in result.rendered_output


def test_scenario_command_supports_json_view_model_output():
    invocation = ScenarioCommandInvocation(
        invocation_id="sprint5-scenario-command-invocation-json-001",
        command_name=ScenarioCommandName.VERIFY_GOVERNANCE_BOUNDARIES,
        output_format=ScenarioOutputFormat.JSON_VIEW_MODEL,
        scenario_name="application-health",
        read_only=True,
        requested_by="operator-demo",
        command_path="eaios sprint5 verify --scenario application-health --format json --read-only",
    )

    result = run_sprint5_scenario_command(invocation)

    assert result.state == ScenarioCommandState.COMPLETED_READ_ONLY
    assert result.command_name == "VERIFY_GOVERNANCE_BOUNDARIES"
    assert result.output_format == "JSON_VIEW_MODEL"
    assert isinstance(result.rendered_output, dict)
    assert result.rendered_output["summary"]["run_id"] == "sprint5-operator-demo-run-001"
    assert result.rendered_output["summary"]["all_governance_checks_passed"] is True


def test_scenario_command_embeds_demo_summary_and_stages():
    result = _result()

    assert result.demo_summary["run_id"] == "sprint5-operator-demo-run-001"
    assert result.demo_summary["step_count"] == 5
    assert result.demo_summary["all_governance_checks_passed"] is True

    assert result.stage_names == (
        "LOAD_OPERATOR_EXPORT",
        "RENDER_MARKDOWN",
        "RENDER_JSON_VIEW_MODEL",
        "RENDER_CLI_TEXT",
        "VERIFY_GOVERNANCE_BOUNDARIES",
    )


def test_scenario_command_preserves_blocked_actions():
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


def test_scenario_command_governance_checks_pass():
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
        "real_shell_command_not_executed": True,
        "command_invocation_read_only": True,
        "supported_command": True,
        "supported_output_format": True,
        "application_health_scenario": True,
    }


def test_scenario_command_preserves_no_execution_boundaries():
    result = _result()

    assert result.real_shell_command_executed is False
    assert result.real_tool_execution_performed is False
    assert result.provider_call_performed is False
    assert result.dashboard_changes_applied is False
    assert result.benchmark_scoring_allowed_from_command is False
    assert result.autonomous_remediation_allowed is False
    assert result.human_review_required is True


def test_scenario_command_blocks_non_read_only_invocation():
    invocation = ScenarioCommandInvocation(
        invocation_id="sprint5-scenario-command-invocation-write-001",
        command_name=ScenarioCommandName.RUN_APPLICATION_HEALTH_DEMO,
        output_format=ScenarioOutputFormat.CLI_TEXT,
        scenario_name="application-health",
        read_only=False,
        requested_by="operator-demo",
        command_path="eaios sprint5 run --scenario application-health",
    )

    result = run_sprint5_scenario_command(invocation)

    assert result.state == ScenarioCommandState.BLOCKED_NON_READ_ONLY_INVOCATION
    assert result.rendered_output == "Scenario command must be read-only."
    assert result.real_shell_command_executed is False
    assert result.real_tool_execution_performed is False
    assert result.provider_call_performed is False
    assert result.human_review_required is True


def test_scenario_command_blocks_unsupported_command():
    invocation = ScenarioCommandInvocation(
        invocation_id="sprint5-scenario-command-invocation-unsupported-001",
        command_name="EXECUTE_REMEDIATION",
        output_format=ScenarioOutputFormat.CLI_TEXT,
        scenario_name="application-health",
        read_only=True,
        requested_by="operator-demo",
        command_path="eaios sprint5 execute-remediation --scenario application-health --read-only",
    )

    result = run_sprint5_scenario_command(invocation)

    assert result.state == ScenarioCommandState.BLOCKED_UNSUPPORTED_COMMAND
    assert result.rendered_output == "Unsupported command: EXECUTE_REMEDIATION"
    assert "autonomous_remediation" in result.blocked_actions
    assert result.real_shell_command_executed is False


def test_scenario_command_blocks_unsupported_output_format():
    invocation = ScenarioCommandInvocation(
        invocation_id="sprint5-scenario-command-invocation-bad-format-001",
        command_name=ScenarioCommandName.RUN_APPLICATION_HEALTH_DEMO,
        output_format="HTML",
        scenario_name="application-health",
        read_only=True,
        requested_by="operator-demo",
        command_path="eaios sprint5 run --scenario application-health --format html --read-only",
    )

    result = run_sprint5_scenario_command(invocation)

    assert result.state == ScenarioCommandState.BLOCKED_UNSUPPORTED_COMMAND
    assert result.rendered_output == "Unsupported output format: HTML"
    assert result.real_shell_command_executed is False


def test_scenario_command_summary_is_view_ready():
    result = _result()

    assert summarize_scenario_command_result(result) == {
        "result_id": "sprint5-scenario-command-result-001",
        "invocation_id": "sprint5-scenario-command-invocation-001",
        "command_name": "RUN_APPLICATION_HEALTH_DEMO",
        "output_format": "CLI_TEXT",
        "scenario_name": "application-health",
        "state": "COMPLETED_READ_ONLY",
        "source_demo_run_id": "sprint5-operator-demo-run-001",
        "stage_count": 5,
        "blocked_action_count": 16,
        "governance_check_count": 13,
        "all_governance_checks_passed": True,
        "real_shell_command_executed": False,
        "real_tool_execution_performed": False,
        "provider_call_performed": False,
        "dashboard_changes_applied": False,
        "benchmark_scoring_allowed_from_command": False,
        "autonomous_remediation_allowed": False,
        "human_review_required": True,
    }


def test_scenario_command_view_model_is_json_serializable():
    result = _result()

    serialized = json.dumps(to_view_model(result), indent=2)

    assert "sprint5-scenario-command-result-001" in serialized
    assert "RUN_APPLICATION_HEALTH_DEMO" in serialized
    assert "COMPLETED_READ_ONLY" in serialized
    assert "rendered_output" in serialized
    assert "benchmark_scoring_allowed_from_command" in serialized


def test_scenario_command_module_does_not_execute_real_tools_or_score_benchmark():
    source = Path("src/eaios/sprint5/scenario_command.py").read_text(
        encoding="utf-8"
    )

    assert "subprocess" not in source
    assert "import requests" not in source.lower()
    assert "import httpx" not in source.lower()
    assert "execute_tool(" not in source
    assert "restart_service(" not in source
    assert "score_benchmark_result(" not in source
