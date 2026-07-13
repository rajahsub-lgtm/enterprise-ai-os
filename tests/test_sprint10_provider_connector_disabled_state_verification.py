from pathlib import Path


DOC = Path("docs/EAIOS_2_SPRINT_10_PROVIDER_CONNECTOR_DISABLED_STATE_VERIFICATION.md")


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_provider_connector_disabled_state_file_exists():
    assert DOC.exists()


def test_provider_connector_disabled_state_declares_purpose_and_non_actions():
    text = _text()

    assert "verifies that providers and MCP connectors remain disabled" in text
    assert "It does not approve deployment." in text
    assert "It does not enable providers." in text
    assert "It does not enable MCP connectors." in text
    assert "It does not create credentials." in text
    assert "It does not call external APIs." in text


def test_provider_connector_disabled_state_declares_sprint10_position_and_principle():
    text = _text()

    assert "Sprint 10 remains a cloud preview review sprint." in text
    assert "preferred preview remains static-only" in text
    assert "Disabled means more than not used." in text
    assert "no credentials" in text
    assert "no endpoint calls" in text
    assert "no hidden fallback path" in text


def test_provider_connector_disabled_state_preserves_static_preview_assumption():
    text = _text()

    for expected in [
        "STATIC_REVIEW_PREVIEW",
        "static documentation and precomputed demo artifacts only",
        "must not run EAIOS orchestration",
        "must not call providers",
        "must not call MCP connectors",
        "must not require secrets",
        "must not use production data",
    ]:
        assert expected in text


def test_provider_disabled_state_requirements_are_explicit():
    text = _text()

    for expected in [
        "Providers must remain disabled.",
        "providers_enabled is false",
        "provider_runtime_enabled is false",
        "provider_credentials_present is false",
        "provider_api_keys_present is false",
        "provider_endpoint_configured is false",
        "provider_invocation_allowed is false",
        "provider_retry_allowed is false",
        "provider_fallback_allowed is false",
        "provider_output_authoritative is false",
        "provider_cost_enabled is false",
    ]:
        assert expected in text


def test_provider_disabled_state_questions_and_evidence_are_explicit():
    text = _text()

    for expected in [
        "Are any provider credentials present?",
        "Are any provider endpoints configured?",
        "Can the preview invoke a provider?",
        "Can provider output influence benchmark truth?",
        "Can provider output bypass human approval?",
        "manifest providers_enabled equals false",
        "source review confirms no provider call path",
        "source review confirms no provider credential path",
        "preview content states providers remain disabled",
    ]:
        assert expected in text



def test_connector_disabled_state_requirements_are_explicit():
    text = _text()

    for expected in [
        "MCP connectors must remain disabled.",
        "mcp_connectors_enabled is false",
        "connector_runtime_enabled is false",
        "connector_credentials_present is false",
        "connector_endpoints_configured is false",
        "connector_invocation_allowed is false",
        "connector_write_allowed is false",
        "connector_notification_allowed is false",
        "connector_remediation_allowed is false",
        "connector_benchmark_mutation_allowed is false",
        "connector_cost_enabled is false",
    ]:
        assert expected in text


def test_connector_disabled_state_questions_and_evidence_are_explicit():
    text = _text()

    for expected in [
        "Are any connector credentials present?",
        "Are any connector endpoints configured?",
        "Can the preview invoke a connector?",
        "Can the preview read production data through a connector?",
        "Can the preview write production data through a connector?",
        "Can connector output influence benchmark truth?",
        "Can connector execution bypass human approval?",
        "manifest mcp_connectors_enabled equals false",
        "source review confirms no connector call path",
        "preview content states MCP connectors remain disabled",
    ]:
        assert expected in text


def test_manifest_disabled_state_fields_are_defined():
    text = _text()

    for expected in [
        "providers_enabled",
        "provider_runtime_enabled",
        "provider_credentials_present",
        "provider_endpoint_configured",
        "provider_invocation_allowed",
        "provider_cost_enabled",
        "mcp_connectors_enabled",
        "connector_runtime_enabled",
        "connector_credentials_present",
        "connector_endpoints_configured",
        "connector_invocation_allowed",
        "connector_write_allowed",
        "connector_notification_allowed",
        "connector_remediation_allowed",
        "connector_benchmark_mutation_allowed",
        "connector_cost_enabled",
        "human_approval_required",
        "autonomous_action_enabled",
        "benchmark_truth_mutation_enabled",
    ]:
        assert expected in text


def test_source_and_static_content_checks_are_defined():
    text = _text()

    for expected in [
        "no provider SDK invocation",
        "no provider HTTP invocation",
        "no MCP connector invocation",
        "no credential loading path",
        "no secret manager read path",
        "no production data read path",
        "no production write path",
        "no notification send path",
        "no remediation execution path",
        "no benchmark truth mutation path",
        "providers remain disabled",
        "MCP connectors remain disabled",
    ]:
        assert expected in text


def test_failure_conditions_and_required_actions_are_defined():
    text = _text()

    for expected in [
        "Disabled-state verification fails if",
        "a provider credential is present",
        "a connector credential is present",
        "provider invocation is possible",
        "connector invocation is possible",
        "provider usage can create cost",
        "connector usage can create cost",
        "human approval can be bypassed",
        "autonomous action is enabled",
        "do not approve preview deployment",
        "remove the unsafe path",
        "rerun full suite",
    ]:
        assert expected in text


def test_disabled_state_relationships_and_non_approval_are_defined():
    text = _text()

    for expected in [
        "must not make provider or connector behavior executable",
        "Provider and connector disabled state prevents hidden execution paths.",
        "Human approval remains required",
        "Provider and connector output must not define benchmark truth.",
        "Benchmark truth remains isolated from preview output.",
        "This document does not approve provider enablement.",
        "does not approve MCP connector enablement",
        "does not approve preview deployment",
    ]:
        assert expected in text


def test_disabled_state_interview_explanation_and_sound_bite_are_defined():
    text = _text()

    assert "providers and MCP connectors are not just unused, but truly disabled" in text
    assert "no credentials, no endpoints, no invocation path" in text
    assert "Disabled is a control state, not an assumption." in text
    assert "For enterprise AI, unused is not enough." in text
