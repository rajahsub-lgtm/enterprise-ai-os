from pathlib import Path


DOC = Path("docs/EAIOS_2_SPRINT_6_GCP_DEPLOYMENT_DESIGN.md")

REQUIRED_FILES = [
    Path("docs/EAIOS_2_SPRINT_6_QUICKSTART.md"),
    Path("src/eaios/sprint6/demo_package.py"),
    Path("src/eaios/sprint6/local_cli.py"),
    Path("src/eaios/sprint6/artifact_export_plan.py"),
    Path("src/eaios/sprint6/static_review_page.py"),
    Path("src/eaios/sprint6/portfolio_walkthrough.py"),
]


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_gcp_deployment_design_file_exists():
    assert DOC.exists()


def test_gcp_deployment_design_required_inputs_exist():
    assert [str(path) for path in REQUIRED_FILES if not path.exists()] == []


def test_gcp_deployment_design_declares_review_only_state():
    text = _text()

    assert "REVIEW_ONLY_DESIGN" in text
    assert "GCP_READINESS_REVIEW_ONLY" in text
    assert "REVIEW_READY_NOT_DEPLOYED" in text
    assert "not a deployment script" in text


def test_gcp_deployment_design_blocks_deployment_actions():
    text = _text()

    for expected in [
        "create_cloud_resources",
        "run_gcloud_command",
        "run_terraform_apply",
        "run_shell_deployment_command",
        "load_secret_material",
        "enable_real_provider",
        "enable_real_mcp_connectors",
        "perform_external_write",
        "execute_remediation",
        "send_notification",
        "score_benchmark_from_deployment",
        "enable_autonomous_remediation",
    ]:
        assert expected in text


def test_gcp_deployment_design_lists_components_and_reviews():
    text = _text()

    for expected in [
        "Cloud Run",
        "Artifact Registry",
        "Cloud Storage",
        "Secret Manager",
        "Cloud Logging",
        "Cloud Monitoring",
        "IAM",
        "VPC Service Controls",
        "cloud_architecture_review",
        "security_and_secret_handling_review",
        "provider_integration_review",
        "mcp_connector_permission_review",
        "production_deployment_approval",
    ]:
        assert expected in text


def test_gcp_deployment_design_preserves_boundaries():
    text = _text()

    for expected in [
        "No remediation execution.",
        "No notification send.",
        "No benchmark scoring from runtime output.",
        "Real LLM provider calls remain disabled by default.",
        "Real MCP connectors remain disabled by default.",
        "Benchmark truth remains external.",
        "Human approval remains required",
    ]:
        assert expected in text


def test_gcp_deployment_design_documents_deployment_phases():
    text = _text()

    for expected in [
        "Phase 1: local read-only demo review.",
        "Phase 2: static artifact review.",
        "Phase 3: container packaging review.",
        "Phase 4: Cloud Run read-only preview after approval.",
        "Phase 5: provider and connector design review.",
        "Phase 6: controlled integration pilot after approval.",
    ]:
        assert expected in text


def test_gcp_deployment_design_has_no_deployment_code_or_commands():
    text = _text().lower()

    assert "gcloud run deploy" not in text
    assert "terraform apply" not in text
    assert "kubectl apply" not in text
    assert "docker push" not in text
    assert "api_key" not in text
    assert "password" not in text
