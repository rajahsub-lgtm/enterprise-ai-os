from pathlib import Path


DOC = Path("docs/EAIOS_2_SPRINT_8_DEMO_STORYBOARD.md")


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_demo_storyboard_file_exists():
    assert DOC.exists()


def test_demo_storyboard_declares_interview_ready_purpose():
    text = _text()

    assert "interview-ready narrative" in text
    assert "Governed Enterprise AI for Application Health" in text
    assert "EAIOS is not an agent demo." in text


def test_demo_storyboard_starts_from_business_outcome():
    text = _text()

    assert "Maintain Application Health" in text
    assert "Business Outcome ? Capability ? Skill" in text
    assert "what enterprise outcome must be protected" in text


def test_demo_storyboard_defines_synthetic_data_position():
    text = _text()

    for expected in [
        "synthetic ITIL/AIOps-style data",
        "incident records",
        "alert and telemetry observations",
        "knowledge articles",
        "known-error patterns",
        "business-impact context",
        "operational confidence signals",
    ]:
        assert expected in text


def test_demo_storyboard_defines_real_data_position():
    text = _text()

    for expected in [
        "does not claim production data integration",
        "ServiceNow incidents and problems",
        "BigPanda correlated alerts",
        "Dynatrace telemetry",
        "SAP SolMan signals",
        "CMDB and service graph context",
        "Solution 360 or business service impact context",
    ]:
        assert expected in text



def test_demo_storyboard_high_evidence_low_confidence_is_centerpiece():
    text = _text()

    assert "HIGH while operational confidence remains LOW" in text
    assert "HIGH evidence means the evidence is coherent." in text
    assert "LOW operational confidence" in text
    assert "still does not have enough confidence to act" in text


def test_demo_storyboard_preserves_human_approval_and_blocked_actions():
    text = _text()

    for expected in [
        "requires_human_approval = true",
        "autonomous_action_allowed = false",
        "provider output is not accepted without validation",
        "connector actions remain disabled",
        "write operations remain blocked",
        "benchmark truth remains isolated",
    ]:
        assert expected in text


def test_demo_storyboard_lists_runtime_hardening_chain():
    text = _text()

    for expected in [
        "container packaging contract",
        "local web review surface",
        "cloud deploy preflight",
        "provider request and response schema",
        "provider output validator",
        "MCP connector inventory schema",
        "MCP connector permission classifier",
        "audit event envelope",
        "human approval workflow",
        "demo release checklist",
    ]:
        assert expected in text


def test_demo_storyboard_documents_claims_and_non_claims():
    text = _text()

    assert "What The Demo Proves" in text
    assert "What The Demo Does Not Claim" in text

    for expected in [
        "production deployment",
        "real cloud runtime",
        "real ServiceNow integration",
        "real MCP connector execution",
        "autonomous remediation",
        "production write approval",
    ]:
        assert expected in text


def test_demo_storyboard_contains_five_and_fifteen_minute_flows():
    text = _text()

    assert "Five-Minute Interview Flow" in text
    assert "Fifteen-Minute Interview Flow" in text
    assert "Show the application-health scenario and reasoning chain." in text
    assert "Explain the cloud review gate before any deployment." in text


def test_demo_storyboard_contains_interview_sound_bite():
    text = _text()

    assert "Most agent demos try to prove the agent can act." in text
    assert "This demo proves the enterprise can decide when an agent must not act." in text
    assert "governed enterprise AI" in text
