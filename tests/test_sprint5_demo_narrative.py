from pathlib import Path


NARRATIVE = Path("docs/EAIOS_2_SPRINT_5_DEMO_NARRATIVE.md")

REQUIRED_SOURCE_FILES = [
    Path("src/eaios/sprint5/operator_experience.py"),
    Path("src/eaios/sprint5/demo_runner.py"),
    Path("src/eaios/sprint5/scenario_command.py"),
    Path("src/eaios/sprint5/operator_review_screen.py"),
    Path("src/eaios/sprint5/cloud_safety_config.py"),
    Path("src/eaios/sprint5/provider_plugin_seam.py"),
    Path("src/eaios/sprint5/mcp_connector_harness.py"),
    Path("src/eaios/sprint5/gcp_readiness_checklist.py"),
]


def _text() -> str:
    return NARRATIVE.read_text(encoding="utf-8")


def test_sprint5_demo_narrative_file_exists():
    assert NARRATIVE.exists()


def test_sprint5_demo_narrative_required_source_files_exist():
    missing = [str(path) for path in REQUIRED_SOURCE_FILES if not path.exists()]
    assert missing == []


def test_sprint5_demo_narrative_has_title_and_one_line_demo():
    text = _text()

    assert "EAIOS Operator Experience: Benchmark-Grounded Governed AIOps" in text
    assert "EAIOS shows an operator how application-health evidence" in text
    assert "without executing remediation or weakening governance" in text


def test_sprint5_demo_narrative_lists_demo_scope():
    text = _text()

    assert "read-only operator dashboard export" in text
    assert "read-only CLI demo runner" in text
    assert "single end-to-end scenario command" in text
    assert "operator review screen model" in text
    assert "cloud-safe configuration profile" in text
    assert "provider plug-in safety seam" in text
    assert "MCP connector simulation harness" in text
    assert "GCP deployment readiness checklist" in text


def test_sprint5_demo_narrative_lists_non_goals():
    text = _text()

    assert "execute remediation" in text
    assert "call real tools" in text
    assert "call real LLM providers" in text
    assert "load secrets" in text
    assert "access external networks" in text
    assert "create cloud resources" in text
    assert "write external data" in text
    assert "score benchmarks from demo output" in text
    assert "apply dashboard changes automatically" in text
    assert "enable autonomous remediation" in text


def test_sprint5_demo_narrative_documents_command_path():
    text = _text()

    assert "eaios sprint5 run --scenario application-health --read-only" in text
    assert "src/eaios/sprint5/scenario_command.py" in text
    assert "COMPLETED_READ_ONLY" in text


def test_sprint5_demo_narrative_documents_operator_dashboard_export():
    text = _text()

    assert "src/eaios/sprint5/operator_experience.py" in text
    assert "OperatorDashboardExport" in text
    assert "OperatorDashboardCard" in text
    assert "READ_ONLY_DEMO" in text
    assert "benchmark_scoring_allowed_from_export = false" in text


def test_sprint5_demo_narrative_documents_cli_demo_runner():
    text = _text()

    assert "src/eaios/sprint5/demo_runner.py" in text
    assert "DemoRunResult" in text
    assert "DemoRunStep" in text
    assert "rendered_cli_text" in text
    assert "READ_ONLY_LOCAL" in text


def test_sprint5_demo_narrative_documents_scenario_command_contract():
    text = _text()

    assert "RUN_APPLICATION_HEALTH_DEMO" in text
    assert "EXPORT_OPERATOR_DASHBOARD" in text
    assert "VERIFY_GOVERNANCE_BOUNDARIES" in text
    assert "CLI_TEXT" in text
    assert "MARKDOWN" in text
    assert "JSON_VIEW_MODEL" in text
    assert "Unsupported commands are blocked." in text
    assert "Non-read-only invocations are blocked." in text


def test_sprint5_demo_narrative_documents_operator_review_screen():
    text = _text()

    assert "src/eaios/sprint5/operator_review_screen.py" in text
    assert "OperatorReviewScreenModel" in text
    assert "OperatorReviewSectionCard" in text
    assert "OperatorDecisionControl" in text
    assert "APPROVE_PACKAGE_FOR_MANUAL_EXECUTION" in text
    assert "Approval requires an external governed human process." in text


def test_sprint5_demo_narrative_documents_cloud_safe_configuration():
    text = _text()

    assert "src/eaios/sprint5/cloud_safety_config.py" in text
    assert "CloudSafeConfigProfile" in text
    assert "CloudCapabilityToggle" in text
    assert "CloudSafetyChecklistItem" in text
    assert "GCP_READINESS_REVIEW" in text
    assert "runtime.read_only_demo" in text
    assert "benchmark_scoring_from_cloud_profile" in text


def test_sprint5_demo_narrative_documents_provider_plugin_seam():
    text = _text()

    assert "src/eaios/sprint5/provider_plugin_seam.py" in text
    assert "ProviderPluginSeamProfile" in text
    assert "ProviderRequestEnvelope" in text
    assert "ProviderValidationResult" in text
    assert "DETERMINISTIC_FIXTURE_ONLY" in text
    assert "Real provider calls are disabled by default." in text
    assert "Benchmark scoring from provider output is blocked." in text


def test_sprint5_demo_narrative_documents_mcp_connector_harness():
    text = _text()

    assert "src/eaios/sprint5/mcp_connector_harness.py" in text
    assert "MCPConnectorHarnessProfile" in text
    assert "MCPConnectorDefinition" in text
    assert "MCPConnectorSimulationRequest" in text
    assert "MCPConnectorSimulationResult" in text
    assert "READ_ONLY_SIMULATION" in text
    assert "benchmark_scoring_from_connector" in text


def test_sprint5_demo_narrative_documents_gcp_readiness_checklist():
    text = _text()

    assert "src/eaios/sprint5/gcp_readiness_checklist.py" in text
    assert "GCPReadinessChecklist" in text
    assert "GCPReadinessCheck" in text
    assert "GCPDeploymentGate" in text
    assert "REVIEW_READY_NOT_DEPLOYED" in text
    assert "GCP_READINESS_REVIEW_ONLY" in text
    assert "production_deployment_approval" in text


def test_sprint5_demo_narrative_documents_storyboard_and_talk_tracks():
    text = _text()

    assert "EAIOS starts from a benchmark-grounded application-health scenario." in text
    assert "This is a read-only governed AIOps demo." in text
    assert "The benchmark truth remains external." in text
    assert "Every external or unsafe capability is blocked by default" in text
    assert "The GCP readiness checklist is not a deployment." in text


def test_sprint5_demo_narrative_documents_end_to_end_flow():
    text = _text()

    assert "Sprint 4 governed learning dashboard" in text
    assert "-> operator dashboard export" in text
    assert "-> single scenario command" in text
    assert "-> provider plug-in safety seam" in text
    assert "-> GCP deployment readiness checklist" in text
    assert "-> demo narrative" in text


def test_sprint5_demo_narrative_preserves_safety_boundaries():
    text = _text()

    assert "read_only_demo" in text
    assert "human_review_required" in text
    assert "real_shell_command_execution_blocked" in text
    assert "real_tool_execution_blocked" in text
    assert "provider_call_blocked" in text
    assert "secret_loading_blocked" in text
    assert "network_access_blocked" in text
    assert "cloud_resource_creation_blocked" in text
    assert "benchmark_truth_external" in text
    assert "benchmark_scoring_from_demo_blocked" in text
    assert "autonomous_remediation_disabled" in text


def test_sprint5_demo_narrative_documents_success_criteria():
    text = _text()

    assert "operator-facing dashboard export" in text
    assert "CLI text output" in text
    assert "Markdown output" in text
    assert "JSON view model output" in text
    assert "disabled operator decision controls" in text
    assert "cloud-safe configuration boundary" in text
    assert "MCP connector harness read-only simulation" in text
    assert "governance boundaries visible in every layer" in text


def test_sprint5_demo_narrative_documents_live_demo_sequence():
    text = _text()

    assert "1. Show the one-line demo." in text
    assert "2. Show the read-only command path." in text
    assert "3. Show the operator dashboard export." in text
    assert "4. Show the operator review screen." in text
    assert "7. Show the provider seam." in text
    assert "9. Show the GCP readiness checklist." in text
    assert "10. Close with the governance thesis." in text


def test_sprint5_demo_narrative_closeout_statement():
    text = _text()

    assert "Sprint 5 creates the operator-facing and cloud-readiness demo narrative" in text
    assert "read-only experience" in text
    assert "ready for Sprint 5 closeout" in text
