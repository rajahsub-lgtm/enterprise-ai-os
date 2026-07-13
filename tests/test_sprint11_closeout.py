from pathlib import Path


DOC = Path("docs/EAIOS_2_SPRINT_11_CLOSEOUT.md")

REQUIRED_FILES = [
    Path("src/eaios/sprint11/local_static_preview_generator.py"),
    Path("src/eaios/sprint11/local_static_preview_manifest.py"),
    Path("src/eaios/sprint11/local_static_preview_renderer.py"),
    Path("src/eaios/sprint11/local_static_preview_bundle.py"),
    Path("src/eaios/sprint11/local_static_preview_verifier.py"),
    Path("src/eaios/sprint11/local_static_preview_dry_run.py"),
]


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_sprint11_closeout_file_exists():
    assert DOC.exists()


def test_sprint11_closeout_required_files_exist():
    assert [str(path) for path in REQUIRED_FILES if not path.exists()] == []


def test_sprint11_closeout_declares_status_and_decision():
    text = _text()

    assert "Sprint 11 - Local Static Preview" in text
    assert "LOCAL_STATIC_PREVIEW_COMPLETE_REVIEW_ONLY" in text
    assert "Final Decision" in text
    assert "DO_NOT_DEPLOY_YET" in text


def test_sprint11_closeout_declares_non_actions():
    text = _text()

    for expected in [
        "It did not approve deployment.",
        "It did not create cloud resources.",
        "It did not publish a static site.",
        "It did not write local preview files.",
        "It did not start a runtime.",
        "It did not start a server.",
        "It did not open a browser.",
        "It did not enable providers.",
        "It did not enable MCP connectors.",
        "It did not use production data.",
    ]:
        assert expected in text


def test_sprint11_closeout_lists_completed_slices():
    text = _text()

    for expected in [
        "11-1 local static preview generator contract",
        "11-2 local static preview manifest builder",
        "11-3 local static preview page renderer",
        "11-4 local static preview bundle assembler",
        "11-5 local static preview bundle safety verifier",
        "11-6 local static preview dry-run command",
        "11-7 Sprint 11 closeout",
    ]:
        assert expected in text


def test_sprint11_closeout_lists_primary_artifacts():
    text = _text()

    for expected in [
        "src/eaios/sprint11/local_static_preview_generator.py",
        "src/eaios/sprint11/local_static_preview_manifest.py",
        "src/eaios/sprint11/local_static_preview_renderer.py",
        "src/eaios/sprint11/local_static_preview_bundle.py",
        "src/eaios/sprint11/local_static_preview_verifier.py",
        "src/eaios/sprint11/local_static_preview_dry_run.py",
        "docs/EAIOS_2_SPRINT_11_CLOSEOUT.md",
    ]:
        assert expected in text


def test_sprint11_closeout_preserves_safety_posture():
    text = _text()

    for expected in [
        "files_persisted = false",
        "site_published = false",
        "server_started = false",
        "browser_opened = false",
        "cloud_resources_created = false",
        "providers_enabled = false",
        "mcp_connectors_enabled = false",
        "production_data_used = false",
        "credentials_required = false",
        "runtime_enabled = false",
        "writes_enabled = false",
        "notifications_enabled = false",
        "remediation_enabled = false",
        "benchmark_truth_mutation_enabled = false",
        "autonomous_action_enabled = false",
        "human_approval_required = true",
        "rollback_required = true",
        "materialization_allowed = false",
        "cloud_deployment_allowed = false",
    ]:
        assert expected in text


def test_sprint11_closeout_describes_preview_flow_components():
    text = _text()

    for expected in [
        "The generator contract defines approved source artifacts",
        "The manifest builder creates an in-memory manifest.",
        "The renderer creates page view models in memory.",
        "The bundle assembler packages rendered pages and manifest content in memory.",
        "The verifier checks the in-memory bundle",
        "The dry-run command wires together",
        "The dry-run command blocks invalid context.",
    ]:
        assert expected in text


def test_sprint11_closeout_documents_what_it_proves_and_does_not_claim():
    text = _text()

    for expected in [
        "create a preview package safely before creating any actual preview files",
        "preview planning from materialization",
        "materialization from deployment",
        "rendering from publishing",
        "bundle assembly from persistence",
        "verification from approval",
        "production deployment",
        "cloud deployment",
        "materialized preview files",
        "published static site",
        "provider execution",
        "MCP connector execution",
        "autonomous action",
    ]:
        assert expected in text


def test_sprint11_closeout_lists_portfolio_position_and_next_direction():
    text = _text()

    for expected in [
        "interview-ready",
        "portfolio-ready",
        "cloud-review-ready",
        "local-static-preview-ready",
        "deployment-not-approved",
        "materialization-not-approved",
        "in-memory-preview-verified",
        "The next sprint should not automatically deploy.",
        "optionally materialize local static preview files only if explicitly approved",
        "keep cloud deployment blocked unless a separate approval decision changes",
    ]:
        assert expected in text


def test_sprint11_closeout_contains_interview_explanation_and_final_sound_bite():
    text = _text()

    assert "Sprint 11 created a local in-memory static preview flow." in text
    assert "without writing files, publishing a site, starting a runtime" in text
    assert "The decision remains DO_NOT_DEPLOY_YET." in text
    assert "A preview should be verified before it is materialized." in text
    assert "A demo should not become a deployment by accident." in text
