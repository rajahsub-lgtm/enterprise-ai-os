from pathlib import Path


QUICKSTART = Path("docs/EAIOS_2_SPRINT_6_QUICKSTART.md")

REQUIRED_FILES = [
    Path("src/eaios/sprint6/demo_package.py"),
    Path("src/eaios/sprint6/local_cli.py"),
    Path("src/eaios/sprint6/artifact_export_plan.py"),
    Path("docs/EAIOS_2_SPRINT_5_DEMO_NARRATIVE.md"),
    Path("docs/EAIOS_2_SPRINT_5_CLOSEOUT.md"),
]


def _text() -> str:
    return QUICKSTART.read_text(encoding="utf-8")


def test_sprint6_quickstart_file_exists():
    assert QUICKSTART.exists()


def test_sprint6_quickstart_required_files_exist():
    assert [str(path) for path in REQUIRED_FILES if not path.exists()] == []


def test_sprint6_quickstart_core_content():
    text = _text()

    for expected in [
        "EAIOS Portfolio Demo Quickstart",
        "read-only portfolio demo guide",
        "benchmark-grounded governed AIOps",
        "portfolio packaging plan",
        "local demo package manifest",
        "local CLI entrypoint contract",
        "dry-run artifact export plan",
        "Sprint 5 operator demo narrative",
        "Sprint 5 closeout checkpoint",
        "cloud-readiness review state",
        "provider and connector seams",
    ]:
        assert expected in text


def test_sprint6_quickstart_non_claims():
    text = _text()

    for expected in [
        "deploys cloud resources",
        "writes export folders",
        "copies files into a package",
        "creates archives",
        "loads secrets",
        "calls real LLM providers",
        "connects real MCP tools",
        "executes remediation",
        "scores benchmarks from demo output",
    ]:
        assert expected in text


def test_sprint6_quickstart_contracts_and_modes():
    text = _text()

    for expected in [
        "eaios sprint5 run --scenario application-health --read-only",
        "src/eaios/sprint5/scenario_command.py",
        "not a real shell executor",
        "src/eaios/sprint6/local_cli.py",
        "eaios sprint6 package show-manifest --read-only --format text",
        "SHOW_PACKAGE_MANIFEST",
        "SHOW_GOVERNANCE_BOUNDARIES",
        "SHOW_READINESS_SUMMARY",
        "JSON_VIEW_MODEL",
        "src/eaios/sprint6/demo_package.py",
        "sprint6-demo-package-manifest-001",
        "LOCAL_MANIFEST_ONLY",
        "src/eaios/sprint6/artifact_export_plan.py",
        "sprint6-artifact-export-plan-001",
        "DRY_RUN_ONLY",
        "artifacts/eaios-demo",
    ]:
        assert expected in text


def test_sprint6_quickstart_test_commands_walkthrough_and_boundaries():
    text = _text()

    for expected in [
        "python -m pytest tests\\\\test_sprint6_demo_package.py --basetemp .pytest_tmp",
        "python -m pytest tests\\\\test_sprint6_local_cli.py --basetemp .pytest_tmp",
        "python -m pytest tests\\\\test_sprint6_artifact_export_plan.py --basetemp .pytest_tmp",
        "python -m pytest tests\\\\test_sprint6_quickstart.py --basetemp .pytest_tmp",
        "python -m pytest --basetemp .pytest_tmp",
        "1. Open the Sprint 5 demo narrative.",
        "4. Show the Sprint 6 local demo package manifest.",
        "5. Show the Sprint 6 local CLI contract.",
        "6. Show the Sprint 6 dry-run artifact export plan.",
        "8. Close with the cloud-readiness and human-review story.",
        "read_only_demo",
        "local_manifest_only",
        "dry_run_only",
        "human_review_required",
        "package_file_write_blocked",
        "export_folder_creation_blocked",
        "file_copy_blocked",
        "archive_creation_blocked",
        "shell_command_execution_blocked",
        "cloud_resource_creation_blocked",
        "secret_loading_blocked",
        "provider_call_blocked",
        "real_connector_call_blocked",
        "external_write_blocked",
        "remediation_blocked",
        "notification_blocked",
        "benchmark_scoring_from_package_blocked",
        "benchmark_scoring_from_export_blocked",
        "autonomous_remediation_disabled",
    ]:
        assert expected in text


def test_sprint6_quickstart_cloud_readiness_close_and_next_step():
    text = _text()

    for expected in [
        "REVIEW_READY_NOT_DEPLOYED",
        "GCP_READINESS_REVIEW_ONLY",
        "cloud_architecture_review",
        "security_and_secret_handling_review",
        "provider_integration_review",
        "mcp_connector_permission_review",
        "production_deployment_approval",
        "portfolio-ready, read-only demo of EAIOS governance",
        "without executing unsafe actions",
        "optional static HTML review page model",
        "portfolio walkthrough contract",
    ]:
        assert expected in text
