from pathlib import Path


DOC = Path("docs/EAIOS_2_SPRINT_8_REAL_SYNTHETIC_DATA_MAP.md")


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_real_synthetic_data_map_file_exists():
    assert DOC.exists()


def test_real_synthetic_data_map_declares_purpose_and_position():
    text = _text()

    assert "synthetic ITIL/AIOps data today" in text
    assert "future real enterprise systems" in text
    assert "does not connect to production systems" in text
    assert "Synthetic execution, real enterprise architecture." in text


def test_real_synthetic_data_map_explains_why_synthetic_data_is_used():
    text = _text()

    for expected in [
        "repeatable interview demo runs",
        "controlled benchmark expectations",
        "safe incident and alert simulation",
        "no exposure of production records",
        "no secrets or credentials",
        "no production writes",
        "no real connector execution",
        "benchmark truth isolation",
    ]:
        assert expected in text


def test_real_synthetic_data_map_lists_synthetic_operating_context():
    text = _text()

    for expected in [
        "application symptoms",
        "telemetry observations",
        "incident-like signals",
        "alert-like signals",
        "knowledge evidence",
        "known-error patterns",
        "operational confidence signals",
        "human approval boundaries",
    ]:
        assert expected in text


def test_real_synthetic_data_map_contains_enterprise_mapping_table():
    text = _text()

    for expected in [
        "Synthetic Demo Data",
        "Real Enterprise Equivalent",
        "ServiceNow Incident",
        "ServiceNow Problem",
        "BigPanda",
        "Dynatrace",
        "SAP SolMan",
        "CMDB / Service Graph",
        "Solution 360 / BSI",
        "CAB / AIAB-style review",
    ]:
        assert expected in text



def test_real_synthetic_data_map_preserves_benchmark_boundary():
    text = _text()

    assert "Benchmark truth remains separate from runtime output." in text

    for expected in [
        "runtime reasoning",
        "provider output",
        "connector output",
        "audit events",
        "approval decisions",
        "release checklist output",
        "static export output",
    ]:
        assert expected in text


def test_real_synthetic_data_map_defines_provider_and_connector_boundaries():
    text = _text()

    for expected in [
        "Real LLM or AI provider integration is not enabled",
        "schema validation",
        "unsupported action checks",
        "benchmark truth claim checks",
        "secret leakage checks",
        "Real MCP connectors are not enabled",
        "permission classification",
        "rollback or disable switch",
    ]:
        assert expected in text


def test_real_synthetic_data_map_distinguishes_real_synthetic_and_not_connected():
    text = _text()

    for expected in [
        "What Is Real Today",
        "architecture contracts",
        "test-backed modules",
        "What Is Synthetic Today",
        "application-health scenario data",
        "What Is Not Connected Today",
        "real ServiceNow instance",
        "real LLM provider call",
        "real MCP connector call",
        "real cloud deployment",
    ]:
        assert expected in text


def test_real_synthetic_data_map_contains_interview_explanation_and_sound_bite():
    text = _text()

    assert "The safest interview explanation is:" in text
    assert "synthetic ITIL/AIOps data to simulate" in text
    assert "The data is synthetic so the demo is safe and repeatable." in text
    assert "The architecture is real so the governance problem is enterprise-grade." in text


def test_real_synthetic_data_map_includes_cloud_gate_implications():
    text = _text()

    for expected in [
        "Cloud deployment should not happen until the cloud review gate confirms",
        "what is deployed",
        "what remains static",
        "whether providers remain disabled",
        "whether MCP connectors remain disabled",
        "IAM boundary",
        "cost boundary",
        "rollback or disable plan",
    ]:
        assert expected in text


def test_real_synthetic_data_map_does_not_claim_live_integrations():
    text = _text()

    forbidden_claims = [
        "is connected to production",
        "uses real ServiceNow data",
        "uses real BigPanda data",
        "uses real Dynatrace data",
        "executes real MCP connectors",
        "deploys to cloud",
        "performs autonomous remediation",
    ]

    for forbidden in forbidden_claims:
        assert forbidden not in text
