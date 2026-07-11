from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint5.cloud_safety_config import build_cloud_safe_config_profile, summarize_cloud_safe_config_profile
from eaios.sprint5.gcp_readiness_checklist import build_gcp_readiness_checklist, summarize_gcp_readiness_checklist
from eaios.sprint5.mcp_connector_harness import build_mcp_connector_harness_profile, summarize_mcp_connector_harness_profile
from eaios.sprint5.operator_review_screen import build_operator_review_screen_model, summarize_operator_review_screen
from eaios.sprint5.provider_plugin_seam import build_provider_plugin_seam_profile, summarize_provider_plugin_seam_profile
from eaios.sprint5.scenario_command import run_sprint5_scenario_command, summarize_scenario_command_result


CLOSEOUT = Path("docs/EAIOS_2_SPRINT_5_CLOSEOUT.md")

REQUIRED_FILES = [
    Path("src/eaios/sprint5/operator_experience.py"),
    Path("src/eaios/sprint5/demo_runner.py"),
    Path("src/eaios/sprint5/scenario_command.py"),
    Path("src/eaios/sprint5/operator_review_screen.py"),
    Path("src/eaios/sprint5/cloud_safety_config.py"),
    Path("src/eaios/sprint5/provider_plugin_seam.py"),
    Path("src/eaios/sprint5/mcp_connector_harness.py"),
    Path("src/eaios/sprint5/gcp_readiness_checklist.py"),
    Path("docs/EAIOS_2_SPRINT_5_DEMO_NARRATIVE.md"),
    CLOSEOUT,
]


def _text() -> str:
    return CLOSEOUT.read_text(encoding="utf-8")


def test_sprint5_closeout_file_exists_and_declares_closed():
    assert CLOSEOUT.exists()
    text = _text()
    assert "Sprint 5 ? Operator Experience and Cloud Readiness" in text
    assert "CLOSED" in text
    assert "Sprint 5 is complete." in text


def test_sprint5_closeout_required_files_exist():
    assert [str(path) for path in REQUIRED_FILES if not path.exists()] == []


def test_sprint5_closeout_lists_completed_slices_and_flow():
    text = _text()
    for expected in [
        "5-1 read-only operator dashboard export",
        "5-2 read-only CLI demo runner",
        "5-3 single scenario command contract",
        "5-4 operator review screen model",
        "5-5 cloud-safe configuration boundary",
        "5-6 provider plug-in seam safety boundary",
        "5-7 MCP connector simulation harness",
        "5-8 GCP deployment readiness checklist",
        "5-9 README demo narrative",
        "-> Sprint 5 closeout",
    ]:
        assert expected in text


def test_sprint5_closeout_preserves_core_safety_boundaries():
    text = _text()
    for expected in [
        "read_only_demo",
        "human_review_required",
        "real_shell_command_execution_blocked",
        "real_tool_execution_blocked",
        "provider_call_blocked",
        "secret_loading_blocked",
        "network_access_blocked",
        "external_write_blocked",
        "cloud_resource_creation_blocked",
        "real_connector_call_blocked",
        "remediation_blocked",
        "notification_blocked",
        "dashboard_changes_not_applied",
        "benchmark_truth_external",
        "benchmark_scoring_from_demo_blocked",
        "benchmark_scoring_from_provider_blocked",
        "benchmark_scoring_from_connector_blocked",
        "benchmark_scoring_from_deployment_blocked",
        "autonomous_remediation_disabled",
        "production_knowledge_auto_approval_blocked",
    ]:
        assert expected in text


def test_sprint5_closeout_documents_command_cloud_target_and_sprint6():
    text = _text()
    assert "eaios sprint5 run --scenario application-health --read-only" in text
    assert "GCP_READINESS_REVIEW_ONLY" in text
    assert "REVIEW_READY_NOT_DEPLOYED" in text
    assert "demo packaging" in text
    assert "local CLI entrypoint" in text
    assert "portfolio-ready demo walkthrough" in text


def test_sprint5_contract_summaries_remain_safe():
    command = summarize_scenario_command_result(run_sprint5_scenario_command())
    screen = summarize_operator_review_screen(build_operator_review_screen_model())
    cloud = summarize_cloud_safe_config_profile(build_cloud_safe_config_profile())
    provider = summarize_provider_plugin_seam_profile(build_provider_plugin_seam_profile())
    harness = summarize_mcp_connector_harness_profile(build_mcp_connector_harness_profile())
    gcp = summarize_gcp_readiness_checklist(build_gcp_readiness_checklist())

    assert command["real_shell_command_executed"] is False
    assert screen["benchmark_scoring_allowed_from_screen"] is False
    assert cloud["cloud_resources_created"] is False
    assert provider["real_provider_call_performed"] is False
    assert harness["real_connector_called"] is False
    assert gcp["deployment_actions_performed"] is False

    for summary in [command, screen, cloud, provider, harness, gcp]:
        assert summary["human_review_required"] is True
