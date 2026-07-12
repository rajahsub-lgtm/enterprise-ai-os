from pathlib import Path


DOC = Path("docs/EAIOS_2_SPRINT_6_PROVIDER_INTEGRATION_DESIGN.md")

REQUIRED_FILES = [
    Path("docs/EAIOS_2_SPRINT_6_GCP_DEPLOYMENT_DESIGN.md"),
    Path("src/eaios/sprint5/provider_plugin_seam.py"),
    Path("src/eaios/sprint6/portfolio_walkthrough.py"),
]


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_provider_integration_design_file_exists():
    assert DOC.exists()


def test_provider_integration_design_required_inputs_exist():
    assert [str(path) for path in REQUIRED_FILES if not path.exists()] == []


def test_provider_integration_design_declares_review_only_state():
    text = _text()

    assert "REVIEW_ONLY_DESIGN" in text
    assert "not a provider implementation" in text
    assert "REAL_PROVIDER_DISABLED_BY_DEFAULT" in text
    assert "DETERMINISTIC_FIXTURE_ONLY" in text


def test_provider_integration_design_blocks_provider_execution():
    text = _text()

    for expected in [
        "call_real_provider",
        "load_secret_material",
        "access_external_network",
        "send_prompt_to_provider",
        "store_raw_provider_response_without_review",
        "execute_provider_suggested_action",
        "score_benchmark_from_provider_output",
        "update_benchmark_truth_from_provider_output",
        "enable_autonomous_remediation",
        "bypass_human_review",
    ]:
        assert expected in text


def test_provider_integration_design_documents_boundaries():
    text = _text()

    for expected in [
        "Provider output is evidence, not truth.",
        "Provider output is advisory, not executable.",
        "Provider output must be validated before display.",
        "Provider output must not update benchmark truth.",
        "Provider output must not score benchmarks.",
        "Provider output must not execute remediation.",
        "Provider output must not bypass human review.",
    ]:
        assert expected in text


def test_provider_integration_design_documents_request_response_and_validation():
    text = _text()

    for expected in [
        "request_id",
        "business_outcome",
        "scenario_id",
        "evidence_references",
        "prompt_purpose",
        "allowed_capability",
        "disallowed_capabilities",
        "schema_validity",
        "unsupported_action_requests",
        "benchmark_truth_claims",
        "benchmark_scoring_attempts",
        "remediation_instructions",
        "notification_instructions",
        "secret_leakage",
        "unreviewed_high_risk_recommendations",
    ]:
        assert expected in text


def test_provider_integration_design_documents_secret_network_audit_and_human_review():
    text = _text()

    for expected in [
        "security_owner",
        "secret_inventory",
        "approved_secret_store",
        "rotation_policy",
        "egress_review",
        "provider_endpoint_allowlist",
        "timeout_policy",
        "rate_limit_policy",
        "audit_correlation_id",
        "cost_metadata",
        "latency_metadata",
        "output_hash_or_reference",
        "Human review remains required",
    ]:
        assert expected in text


def test_provider_integration_design_documents_benchmark_boundary():
    text = _text()

    for expected in [
        "Benchmark truth remains external.",
        "define_benchmark_truth",
        "modify_benchmark_truth",
        "score_benchmark_results",
        "infer_benchmark_labels_from_output",
        "replace_benchmark_verification_targets",
        "override_deterministic_scoring_logic",
    ]:
        assert expected in text


def test_provider_integration_design_documents_enablement_phases_and_required_tests():
    text = _text()

    for expected in [
        "Phase 1: deterministic fixture only.",
        "Phase 2: provider request and response schema review.",
        "Phase 3: secret and network design review.",
        "Phase 4: offline provider simulation with stored fixtures.",
        "Phase 5: controlled non-production provider call after approval.",
        "Phase 6: human-reviewed production pilot after approval.",
        "provider_request_schema_tests",
        "provider_response_validation_tests",
        "benchmark_truth_isolation_tests",
        "secret_loading_block_tests",
        "network_access_block_tests",
        "autonomous_action_block_tests",
        "human_review_requirement_tests",
        "cost_latency_metadata_tests",
        "audit_trace_tests",
    ]:
        assert expected in text


def test_provider_integration_design_has_no_provider_code_or_secrets():
    text = _text().lower()

    assert "api_key" not in text
    assert "password" not in text
    assert "bearer " not in text
    assert "curl " not in text
    assert "requests.post" not in text
    assert "httpx.post" not in text
    assert "openai.chat" not in text
    assert "anthropic.messages" not in text
