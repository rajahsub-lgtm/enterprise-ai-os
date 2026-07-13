from pathlib import Path


README = Path("README.md")


def _text() -> str:
    return README.read_text(encoding="utf-8")


def test_readme_exists():
    assert README.exists()


def test_readme_declares_eaios_positioning():
    text = _text()

    assert "EAIOS ? Enterprise AI Operating System" in text
    assert "governed enterprise AI operating-system pattern" in text
    assert "interview-ready application-health demo" in text
    assert "synthetic ITIL/AIOps data" in text


def test_readme_declares_current_portfolio_status():
    text = _text()

    assert "Interview-ready demo package." in text
    assert "It is not a production deployment." in text
    assert "It is not connected to production systems." in text
    assert "It does not execute autonomous remediation." in text


def test_readme_preserves_core_message():
    text = _text()

    assert "Most agent demos try to prove an agent can act." in text
    assert "EAIOS proves the enterprise can decide when an agent must not act." in text
    assert "governed enterprise AI" in text


def test_readme_includes_operating_model_and_business_outcome():
    text = _text()

    assert "Business Outcome ? Capability ? Skill" in text
    assert "Maintain Application Health" in text
    assert "Governance + Observability + Feedback" in text


def test_readme_centers_high_evidence_low_confidence():
    text = _text()

    assert "HIGH evidence / LOW operational confidence split" in text
    assert "evidence is coherent enough to support a hypothesis" in text
    assert "lacks enough validation to act safely" in text
    assert "The system refuses to over-trust itself." in text



def test_readme_distinguishes_real_synthetic_and_not_connected():
    text = _text()

    for expected in [
        "What Is Real",
        "What Is Synthetic",
        "What Is Not Connected",
        "real ServiceNow",
        "real BigPanda",
        "real Dynatrace",
        "real SAP SolMan",
        "real AI provider runtime",
        "real MCP connector runtime",
    ]:
        assert expected in text


def test_readme_contains_future_enterprise_mapping():
    text = _text()

    for expected in [
        "Future Real Enterprise Mapping",
        "ServiceNow Incident",
        "ServiceNow Problem",
        "BigPanda or event-correlation platform",
        "Dynatrace or observability platform",
        "SAP SolMan",
        "CMDB or service graph",
        "Solution 360 or BSI-style context",
        "CAB or AIAB-style review",
    ]:
        assert expected in text


def test_readme_preserves_safety_posture():
    text = _text()

    for expected in [
        "EAIOS is review-only in the current demo.",
        "production data connection",
        "real provider execution",
        "real MCP connector execution",
        "production writes",
        "notification sending",
        "remediation execution",
        "cloud deployment",
        "release creation",
        "benchmark truth updates from runtime output",
        "autonomous remediation",
        "bypassing human review",
    ]:
        assert expected in text


def test_readme_lists_sprint_milestones():
    text = _text()

    for expected in [
        "Sprint 4 ? Benchmark-Grounded Governed AIOps",
        "Sprint 5 ? Operator Experience and Cloud Readiness",
        "Sprint 6 ? Portfolio Readiness",
        "Sprint 7 ? Controlled Runtime Hardening",
        "Sprint 8 ? Interview Demo Readiness",
    ]:
        assert expected in text


def test_readme_lists_interview_artifacts_and_walkthrough():
    text = _text()

    for expected in [
        "Interview Artifacts",
        "docs/EAIOS_2_SPRINT_8_DEMO_STORYBOARD.md",
        "docs/EAIOS_2_SPRINT_8_REAL_SYNTHETIC_DATA_MAP.md",
        "docs/EAIOS_2_SPRINT_8_INTERVIEW_WALKTHROUGH.md",
        "5-minute walkthrough",
        "15-minute walkthrough",
    ]:
        assert expected in text


def test_readme_defers_cloud_deployment_to_review_gate():
    text = _text()

    for expected in [
        "Cloud deployment is intentionally deferred.",
        "cloud review gate",
        "what is deployed",
        "what remains static and read-only",
        "whether providers remain disabled",
        "whether MCP connectors remain disabled",
        "IAM boundary",
        "cost boundary",
        "rollback or disable plan",
    ]:
        assert expected in text


def test_readme_has_no_secret_or_execution_snippets():
    text = _text().lower()

    assert "api_key" not in text
    assert "password" not in text
    assert "bearer " not in text
    assert "requests.post" not in text
    assert "httpx.post" not in text
