from pathlib import Path


DOC = Path("docs/EAIOS_2_SPRINT_10_CLOUD_IAM_COST_BOUNDARY.md")


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_cloud_iam_cost_boundary_file_exists():
    assert DOC.exists()


def test_cloud_iam_cost_boundary_declares_purpose_and_non_actions():
    text = _text()

    assert "defines the IAM and cost boundaries" in text
    assert "It does not approve deployment." in text
    assert "It does not create cloud resources." in text
    assert "It does not create IAM roles." in text
    assert "It does not configure billing." in text


def test_cloud_iam_cost_boundary_declares_sprint10_position_and_principle():
    text = _text()

    assert "Sprint 10 remains a cloud preview review sprint." in text
    assert "preferred preview remains static-only" in text
    assert "least possible authority" in text
    assert "lowest predictable cost" in text
    assert "no runtime permissions should be granted" in text


def test_cloud_iam_cost_boundary_preserves_static_preview_assumption():
    text = _text()

    for expected in [
        "STATIC_REVIEW_PREVIEW",
        "static documentation and precomputed demo artifacts",
        "must not run EAIOS orchestration",
        "must not call providers",
        "must not call MCP connectors",
        "must not read production data",
        "must not write production data",
        "must not send notifications",
        "must not execute remediation",
    ]:
        assert expected in text


def test_cloud_iam_cost_boundary_defines_iam_scope_and_identity_metadata():
    text = _text()

    for expected in [
        "preferred IAM model is static hosting only",
        "broad administrator roles",
        "provider execution roles",
        "MCP connector execution roles",
        "benchmark mutation roles",
        "identity name",
        "identity owner",
        "business owner",
        "technical owner",
        "rollback or disable owner",
    ]:
        assert expected in text


def test_cloud_iam_cost_boundary_lists_allowed_and_disallowed_iam():
    text = _text()

    for expected in [
        "read access to static preview artifacts",
        "serve access for static content",
        "delete or disable ability for rollback",
        "production ITSM access",
        "ServiceNow write access",
        "AI provider invocation access",
        "MCP connector invocation access",
        "secret manager read access",
        "notification sending permission",
        "remediation execution permission",
        "benchmark truth write permission",
    ]:
        assert expected in text



def test_cloud_iam_cost_boundary_defines_secrets_and_network_boundaries():
    text = _text()

    for expected in [
        "The static preview should require no secrets.",
        "API keys",
        "service account keys",
        "provider credentials",
        "connector credentials",
        "The static preview should not require outbound calls.",
        "production ServiceNow endpoint",
        "AI provider endpoint",
        "MCP connector endpoint",
        "private enterprise network endpoint",
    ]:
        assert expected in text


def test_cloud_iam_cost_boundary_defines_cost_model_and_metadata():
    text = _text()

    for expected in [
        "The preview must be cost bounded.",
        "static hosting only",
        "no always-on compute runtime",
        "no provider invocation cost",
        "no connector invocation cost",
        "expected monthly cost",
        "maximum monthly cost",
        "cost owner",
        "cost alert threshold",
    ]:
        assert expected in text


def test_cloud_iam_cost_boundary_defines_cost_stop_conditions():
    text = _text()

    for expected in [
        "cost exceeds approved threshold",
        "unexpected runtime cost appears",
        "provider usage cost appears",
        "connector usage cost appears",
        "database cost appears",
        "network egress cost appears",
        "rollback path is unclear",
    ]:
        assert expected in text


def test_cloud_iam_cost_boundary_defines_logging_and_runtime_boundaries():
    text = _text()

    for expected in [
        "Logging should be minimal and non-sensitive.",
        "static preview access status",
        "production incidents",
        "provider prompts",
        "connector payloads",
        "The default approved posture should be no runtime.",
        "why static hosting is insufficient",
        "how human approval is preserved",
        "how benchmark truth remains isolated",
    ]:
        assert expected in text


def test_cloud_iam_cost_boundary_preserves_provider_mcp_and_benchmark_cost_boundaries():
    text = _text()

    for expected in [
        "Provider cost must be zero for the static preview.",
        "Providers remain disabled.",
        "MCP connector cost must be zero for the static preview.",
        "MCP connectors remain disabled.",
        "Benchmark truth remains isolated",
        "must not run benchmark scoring",
        "must not update benchmark truth",
        "must not create a benchmark authority",
    ]:
        assert expected in text


def test_cloud_iam_cost_boundary_defines_approval_criteria_and_non_approval():
    text = _text()

    for expected in [
        "Approval Criteria",
        "no production system access is required",
        "no secrets are required",
        "providers remain disabled",
        "MCP connectors remain disabled",
        "cost is predictable",
        "cost stop conditions are documented",
        "This document does not approve deployment.",
        "does not approve IAM creation",
        "does not approve billing configuration",
    ]:
        assert expected in text


def test_cloud_iam_cost_boundary_contains_interview_explanation_and_sound_bite():
    text = _text()

    assert "Before any cloud preview, I would define the IAM and cost boundary." in text
    assert "static hosting only: no secrets, no providers, no MCP connectors" in text
    assert "Cloud preview authority should be smaller than the demo story." in text
    assert "not become a new uncontrolled runtime" in text
