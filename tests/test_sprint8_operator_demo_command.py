from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint8.operator_demo_command import (
    OperatorDemoCommandMode,
    OperatorDemoCommandName,
    OperatorDemoCommandRequest,
    OperatorDemoCommandStatus,
    OperatorDemoRenderFormat,
    default_operator_demo_command_request,
    run_operator_demo_command,
    summarize_operator_demo_command_result,
    to_view_model,
)


def test_operator_demo_command_default_request_is_read_only_release_checklist():
    request = default_operator_demo_command_request()

    assert request.command_name == OperatorDemoCommandName.SHOW_RELEASE_CHECKLIST.value
    assert request.read_only is True
    assert request.render_format == OperatorDemoRenderFormat.TEXT


def test_operator_demo_command_runs_default_read_only_command():
    result = run_operator_demo_command()

    assert result.command_id == "sprint8-operator-demo-command-001"
    assert result.mode == OperatorDemoCommandMode.REVIEW_ONLY_OPERATOR_COMMAND
    assert result.command_name == OperatorDemoCommandName.SHOW_RELEASE_CHECKLIST.value
    assert result.status == OperatorDemoCommandStatus.COMPLETED_READ_ONLY
    assert result.title == "EAIOS Sprint 8 Operator Demo Command"
    assert result.provenance == "operator_demo_command:result"


def test_operator_demo_command_embeds_release_checklist_summary():
    result = run_operator_demo_command()

    assert result.release_checklist_summary["checklist_id"] == (
        "sprint7-demo-release-checklist-001"
    )
    assert result.release_checklist_summary["readiness_status"] == (
        "BLOCKED_PENDING_RELEASE_APPROVAL"
    )
    assert result.release_checklist_summary["release_created"] is False
    assert result.release_checklist_summary["human_review_required"] is True


def test_operator_demo_command_supports_runtime_hardening_chain_view():
    result = run_operator_demo_command(
        OperatorDemoCommandRequest(
            command_name=OperatorDemoCommandName.SHOW_RUNTIME_HARDENING_CHAIN.value,
            read_only=True,
            render_format=OperatorDemoRenderFormat.TEXT,
        )
    )

    assert result.status == OperatorDemoCommandStatus.COMPLETED_READ_ONLY
    assert result.sections == ("runtime_hardening_chain", "governance_boundary")
    assert "package, web review, cloud preflight" in result.output_lines[0]


def test_operator_demo_command_supports_human_approval_status_view():
    result = run_operator_demo_command(
        OperatorDemoCommandRequest(
            command_name=OperatorDemoCommandName.SHOW_HUMAN_APPROVAL_STATUS.value,
            read_only=True,
            render_format=OperatorDemoRenderFormat.TEXT,
        )
    )

    assert result.status == OperatorDemoCommandStatus.COMPLETED_READ_ONLY
    assert result.sections == ("human_approval_status", "approval_boundary")
    assert "Human approval is required" in result.output_lines[0]



def test_operator_demo_command_supports_safety_boundaries_view():
    result = run_operator_demo_command(
        OperatorDemoCommandRequest(
            command_name=OperatorDemoCommandName.SHOW_SAFETY_BOUNDARIES.value,
            read_only=True,
            render_format=OperatorDemoRenderFormat.TEXT,
        )
    )

    assert result.status == OperatorDemoCommandStatus.COMPLETED_READ_ONLY
    assert result.sections == ("safety_boundaries", "blocked_actions")
    assert "Benchmark truth remains isolated" in result.output_lines[1]


def test_operator_demo_command_blocks_non_read_only_requests():
    result = run_operator_demo_command(
        OperatorDemoCommandRequest(
            command_name=OperatorDemoCommandName.SHOW_RELEASE_CHECKLIST.value,
            read_only=False,
            render_format=OperatorDemoRenderFormat.TEXT,
        )
    )

    assert result.status == OperatorDemoCommandStatus.BLOCKED_NON_READ_ONLY
    assert result.command_executed is False
    assert result.runtime_actions_executed is False


def test_operator_demo_command_blocks_unsupported_commands():
    result = run_operator_demo_command(
        OperatorDemoCommandRequest(
            command_name="DEPLOY_TO_CLOUD",
            read_only=True,
            render_format=OperatorDemoRenderFormat.TEXT,
        )
    )

    assert result.status == OperatorDemoCommandStatus.BLOCKED_UNSUPPORTED_COMMAND
    assert result.command_executed is False
    assert "Unsupported operator demo command" in result.output_lines[0]


def test_operator_demo_command_preserves_no_execution_boundaries():
    result = run_operator_demo_command()

    assert result.command_executed is True
    assert result.runtime_actions_executed is False
    assert result.release_created is False
    assert result.archive_created is False
    assert result.static_site_published is False
    assert result.container_built is False
    assert result.cloud_deployed is False
    assert result.provider_enabled is False
    assert result.connector_enabled is False
    assert result.approval_records_persisted is False
    assert result.remediation_performed is False
    assert result.notifications_sent is False
    assert result.benchmark_scoring_performed is False
    assert result.benchmark_truth_updated is False
    assert result.autonomous_remediation_allowed is False
    assert result.human_review_required is True


def test_operator_demo_command_summary_is_view_ready():
    result = run_operator_demo_command()

    assert summarize_operator_demo_command_result(result) == {
        "command_id": "sprint8-operator-demo-command-001",
        "mode": "REVIEW_ONLY_OPERATOR_COMMAND",
        "command_name": "SHOW_RELEASE_CHECKLIST",
        "status": "COMPLETED_READ_ONLY",
        "title": "EAIOS Sprint 8 Operator Demo Command",
        "section_count": 2,
        "output_line_count": 4,
        "blocked_action_count": 15,
        "command_executed": True,
        "runtime_actions_executed": False,
        "release_created": False,
        "archive_created": False,
        "static_site_published": False,
        "container_built": False,
        "cloud_deployed": False,
        "provider_enabled": False,
        "connector_enabled": False,
        "approval_records_persisted": False,
        "remediation_performed": False,
        "notifications_sent": False,
        "benchmark_scoring_performed": False,
        "benchmark_truth_updated": False,
        "autonomous_remediation_allowed": False,
        "human_review_required": True,
    }


def test_operator_demo_command_view_model_is_json_serializable():
    result = run_operator_demo_command()

    serialized = json.dumps(to_view_model(result), indent=2)

    assert "sprint8-operator-demo-command-001" in serialized
    assert "SHOW_RELEASE_CHECKLIST" in serialized
    assert "BLOCKED_PENDING_RELEASE_APPROVAL" in serialized
    assert "score_benchmark_from_demo_command" in serialized


def test_operator_demo_command_module_does_not_call_external_systems():
    source = Path("src/eaios/sprint8/operator_demo_command.py").read_text(
        encoding="utf-8"
    ).lower()

    assert "subprocess" not in source
    assert "os.system" not in source
    assert "requests.post" not in source
    assert "httpx.post" not in source
    assert "api_key" not in source
    assert "password" not in source
    assert "bearer " not in source
    assert "curl " not in source
    assert "write_text(" not in source
    assert "mkdir(" not in source
    assert "execute_tool(" not in source
    assert "restart_service(" not in source
