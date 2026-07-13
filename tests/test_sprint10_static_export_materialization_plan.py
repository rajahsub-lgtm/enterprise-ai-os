from pathlib import Path


DOC = Path("docs/EAIOS_2_SPRINT_10_STATIC_EXPORT_MATERIALIZATION_PLAN.md")


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_static_export_materialization_plan_file_exists():
    assert DOC.exists()


def test_static_export_materialization_plan_declares_purpose_and_non_actions():
    text = _text()

    assert "defines how a possible static preview export would be assembled" in text
    assert "It does not create the export." in text
    assert "It does not write deployment files." in text
    assert "It does not publish a static site." in text
    assert "It does not create cloud resources." in text
    assert "It does not start a runtime." in text


def test_static_export_materialization_plan_follows_scope_contract():
    text = _text()

    assert "follows the Sprint 10 static preview scope contract" in text
    assert "STATIC_REVIEW_PREVIEW" in text
    assert "portfolio content and precomputed demo artifacts only" in text
    assert "must not execute live orchestration" in text


def test_static_export_materialization_plan_declares_materialization_principle():
    text = _text()

    assert "Materialize only what is already safe." in text
    assert "Do not create new runtime behavior." in text
    assert "Do not create new integration behavior." in text
    assert "Do not create new authority." in text
    assert "presentation artifact, not an operating system runtime" in text


def test_static_export_materialization_plan_defines_candidate_output_form():
    text = _text()

    for expected in [
        "EAIOS_STATIC_REVIEW_PREVIEW",
        "index.html",
        "architecture.html",
        "demo-storyboard.html",
        "real-enterprise-mapping.html",
        "interview-qa.html",
        "rehearsal-checklist.html",
        "cloud-gate.html",
        "safety-boundaries.html",
        "static-demo-export.json",
        "manifest.json",
    ]:
        assert expected in text



def test_static_export_materialization_plan_lists_source_artifacts():
    text = _text()

    for expected in [
        "README.md",
        "docs/EAIOS_2_SPRINT_8_DEMO_STORYBOARD.md",
        "docs/EAIOS_2_SPRINT_9_ARCHITECTURE_NARRATIVE.md",
        "docs/EAIOS_2_SPRINT_9_REAL_ENTERPRISE_MAPPING.md",
        "docs/EAIOS_2_SPRINT_9_INTERVIEW_QA_PACK.md",
        "docs/EAIOS_2_SPRINT_9_CLOUD_GATE_PRE_REVIEW.md",
        "docs/EAIOS_2_SPRINT_10_STATIC_PREVIEW_SCOPE_CONTRACT.md",
        "src/eaios/sprint8/static_demo_export.py",
        "src/eaios/sprint8/operator_demo_command.py",
    ]:
        assert expected in text


def test_static_export_materialization_plan_defines_page_map():
    text = _text()

    for expected in [
        "### index.html",
        "### architecture.html",
        "### demo-storyboard.html",
        "### real-enterprise-mapping.html",
        "### interview-qa.html",
        "### rehearsal-checklist.html",
        "### cloud-gate.html",
        "### safety-boundaries.html",
        "### static-demo-export.json",
        "### manifest.json",
    ]:
        assert expected in text


def test_static_export_materialization_plan_preserves_safety_boundaries():
    text = _text()

    for expected in [
        "production data connection",
        "provider execution",
        "MCP connector execution",
        "production writes",
        "notifications",
        "remediation",
        "release creation",
        "benchmark truth updates",
        "autonomous action",
        "bypassing human approval",
    ]:
        assert expected in text


def test_static_export_materialization_plan_defines_manifest_fields():
    text = _text()

    for expected in [
        "preview_id",
        "preview_type",
        "generated_from_branch",
        "generated_from_commit",
        "source_artifacts",
        "generated_artifacts",
        "providers_enabled",
        "mcp_connectors_enabled",
        "production_data_used",
        "secrets_required",
        "runtime_enabled",
        "writes_enabled",
        "notifications_enabled",
        "remediation_enabled",
        "benchmark_truth_mutation_enabled",
        "autonomous_action_enabled",
        "human_approval_required",
        "rollback_required",
    ]:
        assert expected in text


def test_static_export_materialization_plan_defines_steps_and_non_steps():
    text = _text()

    for expected in [
        "verify git status is clean",
        "verify full test suite passes",
        "record current branch",
        "record current commit",
        "read approved source artifacts",
        "render markdown into static HTML",
        "generate manifest.json",
        "deploy to cloud",
        "start a local server",
        "call providers",
        "call MCP connectors",
        "mutate benchmark truth",
        "enable autonomous action",
    ]:
        assert expected in text


def test_static_export_materialization_plan_defines_validation_and_approval_boundary():
    text = _text()

    for expected in [
        "Validation Checklist",
        "all generated files are static",
        "generated files contain no secrets",
        "generated manifest says providers_enabled = false",
        "generated manifest says mcp_connectors_enabled = false",
        "generated manifest says runtime_enabled = false",
        "generated manifest says autonomous_action_enabled = false",
        "This plan does not approve materialization.",
        "A separate approval checklist is still required before cloud deployment.",
    ]:
        assert expected in text


def test_static_export_materialization_plan_contains_interview_explanation_and_sound_bite():
    text = _text()

    assert "Sprint 10 is still review-first." in text
    assert "does not deploy anything or enable runtime behavior" in text
    assert "Static export materialization should package the story." in text
    assert "It should not change the system." in text
