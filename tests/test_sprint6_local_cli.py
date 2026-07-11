from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint6.local_cli import (
    LocalCLICommand,
    LocalCLIInvocation,
    LocalCLIOutputFormat,
    LocalCLIState,
    build_default_local_cli_invocation,
    run_local_cli_entrypoint,
    summarize_local_cli_result,
    to_view_model,
)


def test_local_cli_default_invocation_is_read_only():
    invocation = build_default_local_cli_invocation()

    assert invocation.invocation_id == "sprint6-local-cli-invocation-001"
    assert invocation.command == LocalCLICommand.SHOW_PACKAGE_MANIFEST
    assert invocation.output_format == LocalCLIOutputFormat.TEXT
    assert invocation.read_only is True
    assert invocation.argv == (
        "eaios",
        "sprint6",
        "package",
        "show-manifest",
        "--read-only",
        "--format",
        "text",
    )


def test_local_cli_default_run_renders_manifest_text():
    result = run_local_cli_entrypoint()

    assert result.result_id == "sprint6-local-cli-result-001"
    assert result.state == LocalCLIState.COMPLETED_READ_ONLY
    assert result.command == "SHOW_PACKAGE_MANIFEST"
    assert result.output_format == "TEXT"
    assert isinstance(result.rendered_output, str)
    assert "# EAIOS Portfolio Demo Package Manifest" in result.rendered_output
    assert "Human review required: true" in result.rendered_output


def test_local_cli_can_render_governance_boundaries():
    result = run_local_cli_entrypoint(
        LocalCLIInvocation(
            invocation_id="test-governance",
            argv=("eaios", "sprint6", "package", "governance", "--read-only"),
            command=LocalCLICommand.SHOW_GOVERNANCE_BOUNDARIES,
            output_format=LocalCLIOutputFormat.TEXT,
            read_only=True,
            provenance="test",
        )
    )

    assert result.state == LocalCLIState.COMPLETED_READ_ONLY
    assert "# EAIOS Governance Boundaries" in result.rendered_output
    assert "score_benchmark_from_package" in result.rendered_output


def test_local_cli_can_render_readiness_summary():
    result = run_local_cli_entrypoint(
        LocalCLIInvocation(
            invocation_id="test-readiness",
            argv=("eaios", "sprint6", "package", "readiness", "--read-only"),
            command=LocalCLICommand.SHOW_READINESS_SUMMARY,
            output_format=LocalCLIOutputFormat.TEXT,
            read_only=True,
            provenance="test",
        )
    )

    assert result.state == LocalCLIState.COMPLETED_READ_ONLY
    assert "# EAIOS Readiness Summary" in result.rendered_output
    assert "Manifest: sprint6-demo-package-manifest-001" in result.rendered_output


def test_local_cli_can_render_json_view_model():
    result = run_local_cli_entrypoint(
        LocalCLIInvocation(
            invocation_id="test-json",
            argv=("eaios", "sprint6", "package", "show-manifest", "--read-only"),
            command=LocalCLICommand.SHOW_PACKAGE_MANIFEST,
            output_format=LocalCLIOutputFormat.JSON_VIEW_MODEL,
            read_only=True,
            provenance="test",
        )
    )

    assert result.state == LocalCLIState.COMPLETED_READ_ONLY
    assert isinstance(result.rendered_output, dict)
    assert result.rendered_output["summary"]["manifest_id"] == (
        "sprint6-demo-package-manifest-001"
    )


def test_local_cli_blocks_non_read_only_invocation():
    result = run_local_cli_entrypoint(
        LocalCLIInvocation(
            invocation_id="test-not-read-only",
            argv=("eaios", "sprint6", "package", "show-manifest"),
            command=LocalCLICommand.SHOW_PACKAGE_MANIFEST,
            output_format=LocalCLIOutputFormat.TEXT,
            read_only=False,
            provenance="test",
        )
    )

    assert result.state == LocalCLIState.BLOCKED_NON_READ_ONLY
    assert result.rendered_output == "Blocked: BLOCKED_NON_READ_ONLY"
    assert result.shell_commands_executed is False
    assert result.package_files_written is False


def test_local_cli_blocks_unsupported_command():
    result = run_local_cli_entrypoint(
        LocalCLIInvocation(
            invocation_id="test-unsupported",
            argv=("eaios", "sprint6", "package", "bad", "--read-only"),
            command="BAD_COMMAND",
            output_format=LocalCLIOutputFormat.TEXT,
            read_only=True,
            provenance="test",
        )
    )

    assert result.state == LocalCLIState.BLOCKED_UNSUPPORTED_COMMAND
    assert result.shell_commands_executed is False


def test_local_cli_preserves_no_execution_boundaries():
    result = run_local_cli_entrypoint()

    assert result.shell_commands_executed is False
    assert result.package_files_written is False
    assert result.external_files_written is False
    assert result.cloud_resources_created is False
    assert result.secrets_loaded is False
    assert result.provider_calls_performed is False
    assert result.real_connectors_called is False
    assert result.remediation_performed is False
    assert result.notifications_sent is False
    assert result.benchmark_scoring_performed is False
    assert result.autonomous_remediation_allowed is False
    assert result.human_review_required is True


def test_local_cli_summary_is_view_ready():
    result = run_local_cli_entrypoint()

    assert summarize_local_cli_result(result) == {
        "result_id": "sprint6-local-cli-result-001",
        "invocation_id": "sprint6-local-cli-invocation-001",
        "state": "COMPLETED_READ_ONLY",
        "command": "SHOW_PACKAGE_MANIFEST",
        "output_format": "TEXT",
        "blocked_action_count": 11,
        "shell_commands_executed": False,
        "package_files_written": False,
        "external_files_written": False,
        "cloud_resources_created": False,
        "secrets_loaded": False,
        "provider_calls_performed": False,
        "real_connectors_called": False,
        "remediation_performed": False,
        "notifications_sent": False,
        "benchmark_scoring_performed": False,
        "autonomous_remediation_allowed": False,
        "human_review_required": True,
    }


def test_local_cli_view_model_is_json_serializable():
    result = run_local_cli_entrypoint()

    serialized = json.dumps(to_view_model(result), indent=2)

    assert "sprint6-local-cli-result-001" in serialized
    assert "SHOW_PACKAGE_MANIFEST" in serialized
    assert "score_benchmark_from_package" in serialized


def test_local_cli_module_does_not_execute_shell_or_call_external_systems():
    source = Path("src/eaios/sprint6/local_cli.py").read_text(encoding="utf-8")

    assert "subprocess" not in source
    assert "os.system" not in source
    assert "import requests" not in source.lower()
    assert "import httpx" not in source.lower()
    assert "google.cloud" not in source.lower()
    assert "openai" not in source.lower()
    assert "anthropic" not in source.lower()
    assert "execute_tool(" not in source
    assert "restart_service(" not in source
    assert "score_benchmark_result(" not in source
