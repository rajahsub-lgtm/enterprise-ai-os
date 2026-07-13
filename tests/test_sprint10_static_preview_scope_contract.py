from pathlib import Path


DOC = Path("docs/EAIOS_2_SPRINT_10_STATIC_PREVIEW_SCOPE_CONTRACT.md")


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_static_preview_scope_contract_file_exists():
    assert DOC.exists()


def test_static_preview_scope_contract_declares_purpose_and_non_approval():
    text = _text()

    assert "defines the approved scope for a possible static cloud preview" in text
    assert "It does not approve deployment." in text
    assert "It does not create cloud resources." in text
    assert "It does not enable a runtime." in text


def test_static_preview_scope_contract_declares_sprint10_position():
    text = _text()

    assert "Sprint 10 is a cloud preview review sprint." in text
    assert "not an automatic deployment sprint" in text
    assert "scope control" in text


def test_static_preview_scope_contract_limits_preview_type():
    text = _text()

    assert "STATIC_REVIEW_PREVIEW" in text
    assert "display portfolio content and precomputed demo artifacts" in text
    assert "must not execute live orchestration" in text
    assert "must not start an agent runtime" in text
    assert "must not call external APIs" in text
    assert "must not require secrets" in text


def test_static_preview_scope_contract_lists_allowed_content():
    text = _text()

    for expected in [
        "README content",
        "Sprint 8 demo storyboard",
        "Sprint 8 real and synthetic data map",
        "Sprint 8 interview walkthrough",
        "Sprint 9 architecture narrative",
        "Sprint 9 real enterprise mapping",
        "Sprint 9 interview Q&A pack",
        "Sprint 9 demo rehearsal checklist",
        "Sprint 9 cloud gate pre-review notes",
        "precomputed static demo export",
        "precomputed operator demo command output",
    ]:
        assert expected in text


def test_static_preview_scope_contract_lists_disallowed_content():
    text = _text()

    for expected in [
        "production data",
        "real ServiceNow records",
        "real BigPanda alerts",
        "real Dynatrace telemetry",
        "real SAP SolMan signals",
        "secrets or credentials",
        "real provider prompts or responses",
        "real MCP connector responses",
        "mutable benchmark truth",
        "executable remediation controls",
        "runtime deployment controls",
    ]:
        assert expected in text



def test_static_preview_scope_contract_preserves_runtime_provider_and_mcp_boundaries():
    text = _text()

    for expected in [
        "The static preview must not run the EAIOS runtime.",
        "It must not perform live reasoning",
        "Providers remain disabled.",
        "The static preview must not call a provider.",
        "MCP connectors remain disabled.",
        "The static preview must not call a connector.",
        "The static preview must not expose connector endpoints.",
    ]:
        assert expected in text


def test_static_preview_scope_contract_defines_data_security_iam_and_network_boundaries():
    text = _text()

    for expected in [
        "Allowed data classes",
        "Disallowed data classes",
        "The static preview must require no secrets.",
        "api keys",
        "service account keys",
        "least privilege",
        "production system access",
        "The static preview should not require outbound network calls.",
        "private enterprise network access",
    ]:
        assert expected in text


def test_static_preview_scope_contract_preserves_benchmark_and_human_approval():
    text = _text()

    for expected in [
        "Benchmark truth remains isolated.",
        "must not create, modify, infer, or overwrite benchmark truth",
        "must not define benchmark truth",
        "Human approval remains required.",
        "must not approve actions",
        "must not persist approval records",
        "must not execute any action after approval",
    ]:
        assert expected in text


def test_static_preview_scope_contract_defines_cost_and_rollback():
    text = _text()

    for expected in [
        "The static preview must be cost bounded.",
        "static hosting only",
        "no always-on runtime",
        "no provider usage cost",
        "no connector usage cost",
        "A static preview must have a disable plan before deployment.",
        "who owns rollback",
        "how to disable access",
        "expected rollback time",
    ]:
        assert expected in text


def test_static_preview_scope_contract_defines_approval_criteria_and_non_approval():
    text = _text()

    for expected in [
        "Scope Approval Criteria",
        "it is static or review-only",
        "it does not run EAIOS runtime orchestration",
        "providers remain disabled",
        "MCP connectors remain disabled",
        "autonomous action remains disabled",
        "benchmark truth remains isolated",
        "This contract does not approve deployment.",
        "A separate approval checklist is required",
    ]:
        assert expected in text


def test_static_preview_scope_contract_contains_interview_explanation_and_sound_bite():
    text = _text()

    assert "Sprint 10 begins by defining the static preview scope before deploying anything." in text
    assert "It would not run agents, call providers, call MCP connectors" in text
    assert "Static preview means show the governed architecture." in text
    assert "It does not mean run the enterprise AI system in the cloud." in text
