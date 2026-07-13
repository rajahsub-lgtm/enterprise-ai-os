from pathlib import Path


DOC = Path("docs/EAIOS_2_SPRINT_9_ARCHITECTURE_NARRATIVE.md")


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_architecture_narrative_file_exists():
    assert DOC.exists()


def test_architecture_narrative_declares_purpose_and_thesis():
    text = _text()

    assert "This document explains EAIOS as an enterprise architecture." in text
    assert "portfolio review" in text
    assert "interview discussion" in text
    assert "Enterprise AI needs an operating system, not just more agents." in text


def test_architecture_narrative_contains_operating_model():
    text = _text()

    assert "Business Outcome -> Capability -> Skill" in text
    assert "Data + Knowledge + Context" in text
    assert "Governance + Observability + Feedback" in text
    assert "Maintain Application Health" in text


def test_architecture_narrative_explains_outcome_first_value():
    text = _text()

    assert "what business outcome must be protected" in text
    assert "governed orchestration" in text
    assert "traceable reasoning" in text
    assert "confidence calibration" in text
    assert "human approval" in text


def test_architecture_narrative_lists_eight_layers():
    text = _text()

    for expected in [
        "### 1. Business Outcome Layer",
        "### 2. Capability Layer",
        "### 3. Skill Layer",
        "### 4. Agent / Human / Tool / Workflow Layer",
        "### 5. Data + Knowledge + Context Layer",
        "### 6. Governance Layer",
        "### 7. Observability Layer",
        "### 8. Feedback and Learning Layer",
    ]:
        assert expected in text



def test_architecture_narrative_maps_future_enterprise_sources():
    text = _text()

    for expected in [
        "ServiceNow incidents",
        "BigPanda correlated alerts",
        "Dynatrace telemetry",
        "SAP SolMan signals",
        "CMDB and service graph context",
        "Solution 360 or BSI-style business-impact context",
        "enterprise knowledge systems",
        "governed AI providers",
        "governed MCP connectors",
    ]:
        assert expected in text


def test_architecture_narrative_centers_high_evidence_low_confidence():
    text = _text()

    assert "HIGH evidence / LOW operational confidence split" in text
    assert "evidence is coherent enough to support a hypothesis" in text
    assert "lacks enough validation to act safely" in text
    assert "does not confuse evidence strength with permission to act" in text


def test_architecture_narrative_defines_human_approval_as_architecture():
    text = _text()

    assert "Human approval is not a UI button added at the end." in text
    assert "Human approval is an architectural control." in text
    assert "autonomous remediation disabled" in text


def test_architecture_narrative_defines_provider_connector_boundaries():
    text = _text()

    for expected in [
        "Providers and connectors are treated as governed integration surfaces.",
        "provider output must be validated before acceptance",
        "connector permissions must be inventoried",
        "classified, audited, approved, and release-gated",
    ]:
        assert expected in text


def test_architecture_narrative_preserves_benchmark_isolation():
    text = _text()

    assert "Benchmark truth remains separate from runtime output." in text
    assert "must not define benchmark truth" in text
    assert "evaluation integrity" in text


def test_architecture_narrative_defers_cloud_deployment():
    text = _text()

    for expected in [
        "Cloud deployment is intentionally deferred.",
        "cloud review gate",
        "what remains static and read-only",
        "whether providers remain disabled",
        "whether MCP connectors remain disabled",
        "IAM boundary",
        "cost boundary",
        "rollback or disable plan",
    ]:
        assert expected in text


def test_architecture_narrative_documents_non_claims_and_final_sound_bite():
    text = _text()

    for expected in [
        "production deployment",
        "production data integration",
        "real AI provider execution",
        "real MCP connector execution",
        "autonomous remediation",
        "production writes",
        "EAIOS is not an agent that acts.",
        "allowed, observable, reviewable, reusable, and safe",
    ]:
        assert expected in text
