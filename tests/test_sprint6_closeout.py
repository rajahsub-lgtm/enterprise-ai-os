from pathlib import Path


DOC = Path("docs/EAIOS_2_SPRINT_6_CLOSEOUT.md")

REQUIRED_FILES = [
    Path("src/eaios/sprint6/demo_package.py"),
    Path("src/eaios/sprint6/local_cli.py"),
    Path("src/eaios/sprint6/artifact_export_plan.py"),
    Path("src/eaios/sprint6/static_review_page.py"),
    Path("src/eaios/sprint6/portfolio_walkthrough.py"),
    Path("docs/EAIOS_2_SPRINT_6_QUICKSTART.md"),
    Path("docs/EAIOS_2_SPRINT_6_GCP_DEPLOYMENT_DESIGN.md"),
    Path("docs/EAIOS_2_SPRINT_6_PROVIDER_INTEGRATION_DESIGN.md"),
    Path("docs/EAIOS_2_SPRINT_6_MCP_CONNECTOR_PERMISSION_MODEL.md"),
]


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_sprint6_closeout_file_exists():
    assert DOC.exists()


def test_sprint6_closeout_required_files_exist():
    assert [str(path) for path in REQUIRED_FILES if not path.exists()] == []


def test_sprint6_closeout_declares_sprint_closed():
    text = _text()

    assert "Sprint 6 ? Demo Packaging and Portfolio Readiness" in text
    assert "CLOSED" in text
    assert "portfolio-ready, test-backed, read-only review package" in text


def test_sprint6_closeout_lists_completed_slices():
    text = _text()

    for expected in [
        "6-1 local demo package manifest",
        "6-2 local CLI entrypoint contract",
        "6-3 dry-run artifact export plan",
        "6-4 portfolio quickstart guide",
        "6-5 static HTML review page model",
        "6-6 portfolio walkthrough contract",
        "6-7 GCP deployment design",
        "6-8 provider integration design",
        "6-9 MCP connector permission model",
        "6-10 Sprint 6 closeout",
    ]:
        assert expected in text


def test_sprint6_closeout_lists_primary_and_test_artifacts():
    text = _text()

    for expected in [
        "src/eaios/sprint6/demo_package.py",
        "src/eaios/sprint6/local_cli.py",
        "src/eaios/sprint6/artifact_export_plan.py",
        "src/eaios/sprint6/static_review_page.py",
        "src/eaios/sprint6/portfolio_walkthrough.py",
        "docs/EAIOS_2_SPRINT_6_QUICKSTART.md",
        "docs/EAIOS_2_SPRINT_6_GCP_DEPLOYMENT_DESIGN.md",
        "docs/EAIOS_2_SPRINT_6_PROVIDER_INTEGRATION_DESIGN.md",
        "docs/EAIOS_2_SPRINT_6_MCP_CONNECTOR_PERMISSION_MODEL.md",
        "tests/test_sprint6_closeout.py",
    ]:
        assert expected in text


def test_sprint6_closeout_preserves_review_modes():
    text = _text()

    for expected in [
        "LOCAL_MANIFEST_ONLY",
        "DRY_RUN_ONLY",
        "RENDER_ONLY",
        "READ_ONLY_SCRIPT",
        "REVIEW_ONLY_DESIGN",
        "REVIEW_ONLY_PERMISSION_MODEL",
        "GCP_READINESS_REVIEW_ONLY",
        "REVIEW_READY_NOT_DEPLOYED",
        "REAL_PROVIDER_DISABLED_BY_DEFAULT",
        "REAL_MCP_CONNECTORS_DISABLED_BY_DEFAULT",
        "DETERMINISTIC_FIXTURE_ONLY",
        "DETERMINISTIC_CONNECTOR_FIXTURE_ONLY",
    ]:
        assert expected in text


def test_sprint6_closeout_preserves_governance_boundaries():
    text = _text()

    for expected in [
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
        "benchmark_scoring_from_provider_output_blocked",
        "benchmark_scoring_from_connector_output_blocked",
        "benchmark_truth_update_from_provider_output_blocked",
        "benchmark_truth_update_from_connector_output_blocked",
        "autonomous_remediation_disabled",
    ]:
        assert expected in text


def test_sprint6_closeout_documents_cloud_provider_connector_and_benchmark_boundaries():
    text = _text()

    for expected in [
        "No gcloud command is run.",
        "No Terraform apply is run.",
        "No Kubernetes apply is run.",
        "Provider output is evidence, not truth.",
        "Provider output is advisory, not executable.",
        "Real MCP connectors remain disabled by default.",
        "Connector permissions must be explicit.",
        "Benchmark truth remains external.",
        "Runtime output must not define benchmark truth.",
        "Provider output must not score benchmarks.",
        "Connector output must not score benchmarks.",
    ]:
        assert expected in text


def test_sprint6_closeout_documents_human_review_boundary():
    text = _text()

    for expected in [
        "provider-generated recommendations",
        "connector-generated observations",
        "write-capable connector requests",
        "production record changes",
        "notification operations",
        "remediation operations",
        "identity or access operations",
        "cloud deployment approval",
        "secret enablement",
        "benchmark scoring requests",
        "benchmark truth update requests",
    ]:
        assert expected in text


def test_sprint6_closeout_documents_portfolio_narrative_and_claims():
    text = _text()

    for expected in [
        "Start with EAIOS as an enterprise AI operating model.",
        "Show the benchmark-grounded governed AIOps demo.",
        "Show the operator review surface.",
        "Show that unsafe controls are disabled.",
        "Explain GCP readiness as review-only.",
        "Explain provider integration as disabled by default.",
        "Explain MCP connector enablement as permission-gated.",
        "EAIOS is portfolio-ready as a read-only, test-backed demonstration",
        "production deployment",
        "real provider integration",
        "real MCP connector integration",
        "autonomous production action",
    ]:
        assert expected in text


def test_sprint6_closeout_documents_commands_and_sprint7_direction():
    text = _text()

    for expected in [
        "python -m pytest tests\\\\test_sprint6_demo_package.py --basetemp .pytest_tmp",
        "python -m pytest tests\\\\test_sprint6_closeout.py --basetemp .pytest_tmp",
        "python -m pytest --basetemp .pytest_tmp",
        "Sprint 7 can move from portfolio readiness into controlled runtime hardening.",
        "container packaging contract",
        "provider request and response schema",
        "MCP connector inventory schema",
        "human approval workflow model",
        "demo release checklist",
    ]:
        assert expected in text


def test_sprint6_closeout_has_no_execution_commands_or_secrets():
    text = _text().lower()

    assert "gcloud run deploy" not in text
    assert "kubectl apply" not in text
    assert "api_key" not in text
    assert "password" not in text
    assert "bearer " not in text
    assert "curl " not in text
    assert "requests.post" not in text
    assert "httpx.post" not in text
