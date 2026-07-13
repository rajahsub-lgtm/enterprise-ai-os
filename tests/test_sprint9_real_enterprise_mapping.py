from pathlib import Path


DOC = Path("docs/EAIOS_2_SPRINT_9_REAL_ENTERPRISE_MAPPING.md")


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_real_enterprise_mapping_file_exists():
    assert DOC.exists()


def test_real_enterprise_mapping_declares_purpose_and_positioning():
    text = _text()

    assert "maps the EAIOS interview demo to a real enterprise operating environment" in text
    assert "synthetic in data execution and real in enterprise architecture" in text
    assert "does not connect to production systems" in text
    assert "credible enterprise path" in text


def test_real_enterprise_mapping_declares_core_message():
    text = _text()

    assert "Synthetic execution proves the operating model safely." in text
    assert "Real enterprise mapping proves the architecture is relevant." in text
    assert "Governance decides when each integration is allowed" in text


def test_real_enterprise_mapping_lists_business_outcome_and_capabilities():
    text = _text()

    assert "Maintain Application Health" in text
    assert "Application Health Management" in text

    for expected in [
        "Major Incident Prevention",
        "Early Problem Detection",
        "Problem Management Intelligence",
        "Knowledge Quality Management",
        "Change Risk Review",
        "Operational Resilience Review",
        "AI Provider Governance",
        "MCP Connector Governance",
        "Agent Portfolio Governance",
    ]:
        assert expected in text


def test_real_enterprise_mapping_contains_system_mapping_table():
    text = _text()

    for expected in [
        "EAIOS Concept",
        "Real Enterprise Equivalent",
        "Example Platform",
        "ServiceNow Incident",
        "ServiceNow Problem",
        "ServiceNow Known Error",
        "ServiceNow Knowledge / Wiki",
        "BigPanda",
        "Dynatrace",
        "SAP SolMan",
        "CMDB / Service Graph",
        "Solution 360 / BSI",
        "CAB / AIAB-style review",
        "GCP Cloud Run review",
    ]:
        assert expected in text



def test_real_enterprise_mapping_explains_each_major_platform():
    text = _text()

    for expected in [
        "## ServiceNow Mapping",
        "## BigPanda Mapping",
        "## Dynatrace Mapping",
        "## SAP SolMan Mapping",
        "## CMDB and Service Graph Mapping",
        "## Solution 360 or BSI Mapping",
        "## Provider Integration Mapping",
        "## MCP Connector Mapping",
        "## CAB and AIAB Mapping",
        "## Cloud Mapping",
    ]:
        assert expected in text


def test_real_enterprise_mapping_preserves_provider_connector_boundaries():
    text = _text()

    for expected in [
        "AI providers are not enabled in the current demo.",
        "Provider output is advisory until validated and reviewed.",
        "MCP connectors are not enabled in the current demo.",
        "connector inventory",
        "permission class",
        "rollback or disable switch",
        "release gate",
    ]:
        assert expected in text


def test_real_enterprise_mapping_includes_cloud_review_gate():
    text = _text()

    for expected in [
        "Cloud deployment is deferred.",
        "cloud review gate",
        "what remains static and read-only",
        "whether providers remain disabled",
        "whether MCP connectors remain disabled",
        "IAM boundary",
        "network boundary",
        "cost boundary",
        "benchmark truth isolation",
        "human approval boundary",
    ]:
        assert expected in text


def test_real_enterprise_mapping_defines_safe_integration_sequence():
    text = _text()

    for expected in [
        "document source purpose",
        "identify business owner",
        "identify technical owner",
        "identify data owner",
        "classify data sensitivity",
        "define read-only use case",
        "define blocked actions",
        "validate with synthetic replay",
        "enable controlled read-only integration",
        "expand only after governance approval",
    ]:
        assert expected in text


def test_real_enterprise_mapping_preserves_read_only_first_principle():
    text = _text()

    assert "Every enterprise integration should begin read-only." in text
    assert "Read-only does not mean risk-free." in text
    assert "Write, notification, remediation, and workflow mutation capabilities require a higher approval tier." in text


def test_real_enterprise_mapping_documents_non_claims():
    text = _text()

    for expected in [
        "real ServiceNow execution",
        "real BigPanda execution",
        "real Dynatrace execution",
        "real SAP SolMan execution",
        "real provider execution",
        "real MCP connector execution",
        "real cloud deployment",
        "production writes",
        "production notifications",
        "production remediation",
        "autonomous action",
    ]:
        assert expected in text


def test_real_enterprise_mapping_contains_interview_talk_track_and_sound_bite():
    text = _text()

    assert "The demo is synthetic so it is safe and repeatable." in text
    assert "Enterprise mapping makes the architecture credible." in text
    assert "Governance decides when integration becomes execution." in text
