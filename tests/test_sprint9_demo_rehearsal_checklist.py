from pathlib import Path


DOC = Path("docs/EAIOS_2_SPRINT_9_DEMO_REHEARSAL_CHECKLIST.md")


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_demo_rehearsal_checklist_file_exists():
    assert DOC.exists()


def test_demo_rehearsal_checklist_declares_purpose_and_goal():
    text = _text()

    assert "prepares the EAIOS portfolio for interview rehearsal" in text
    assert "Be able to explain EAIOS clearly in 5 minutes" in text
    assert "expand it in 15 minutes" in text
    assert "without overclaiming production readiness" in text


def test_demo_rehearsal_checklist_declares_current_position():
    text = _text()

    assert "EAIOS is interview-ready and review-only." in text
    assert "synthetic ITIL/AIOps data" in text
    assert "architecture maps to real enterprise systems" in text
    assert "does not connect to production systems" in text


def test_demo_rehearsal_checklist_contains_repo_and_test_checks():
    text = _text()

    for expected in [
        "current branch is sprint-9-portfolio-polish",
        "git status is clean",
        "full pytest suite passes",
        "no secrets or credentials are present",
        "python -m pytest --basetemp .pytest_tmp",
    ]:
        assert expected in text


def test_demo_rehearsal_checklist_lists_required_artifacts():
    text = _text()

    for expected in [
        "docs/EAIOS_2_SPRINT_8_DEMO_STORYBOARD.md",
        "docs/EAIOS_2_SPRINT_8_REAL_SYNTHETIC_DATA_MAP.md",
        "docs/EAIOS_2_SPRINT_8_INTERVIEW_WALKTHROUGH.md",
        "src/eaios/sprint8/operator_demo_command.py",
        "README.md",
        "docs/EAIOS_2_SPRINT_9_ARCHITECTURE_NARRATIVE.md",
        "docs/EAIOS_2_SPRINT_9_REAL_ENTERPRISE_MAPPING.md",
        "docs/EAIOS_2_SPRINT_9_INTERVIEW_QA_PACK.md",
    ]:
        assert expected in text


def test_demo_rehearsal_checklist_contains_five_minute_flow():
    text = _text()

    for expected in [
        "Five-Minute Rehearsal Flow",
        "0:00 ? Open",
        "0:45 ? Business Outcome",
        "1:30 ? Synthetic Data Position",
        "2:30 ? Centerpiece Behavior",
        "3:30 ? Safety Boundary",
        "4:30 ? Close",
    ]:
        assert expected in text



def test_demo_rehearsal_checklist_contains_fifteen_minute_flow():
    text = _text()

    for expected in [
        "Fifteen-Minute Rehearsal Flow",
        "0:00 ? Architecture Frame",
        "2:00 ? Application Health Scenario",
        "4:00 ? Enterprise Mapping",
        "6:00 ? Governance Architecture",
        "8:30 ? Centerpiece Behavior",
        "10:30 ? Human Approval",
        "12:00 ? Non-Claims",
        "13:30 ? Production Path",
        "14:30 ? Close",
    ]:
        assert expected in text


def test_demo_rehearsal_checklist_maps_to_enterprise_systems():
    text = _text()

    for expected in [
        "ServiceNow for incidents",
        "BigPanda for correlated alerts",
        "Dynatrace for telemetry",
        "SAP SolMan for SAP-specific symptoms",
        "CMDB or service graph for topology",
        "Solution 360 or BSI-style context",
        "providers for advisory reasoning after validation",
        "MCP connectors for governed integration",
    ]:
        assert expected in text


def test_demo_rehearsal_checklist_centers_high_evidence_low_confidence():
    text = _text()

    assert "HIGH evidence / LOW operational confidence" in text
    assert "A plausible recommendation does not equal permission to execute." in text
    assert "evidence does not equal permission to act" in text


def test_demo_rehearsal_checklist_preserves_blocked_actions():
    text = _text()

    for expected in [
        "Provider execution",
        "MCP connector execution",
        "cloud deployment",
        "production writes",
        "notifications",
        "remediation",
        "release creation",
        "benchmark truth updates",
        "autonomous action remain blocked",
    ]:
        assert expected in text


def test_demo_rehearsal_checklist_contains_acceptance_criteria():
    text = _text()

    for expected in [
        "Rehearsal Acceptance Criteria",
        "explain EAIOS in one sentence",
        "explain synthetic versus real clearly",
        "explain why human approval is required",
        "explain benchmark truth isolation",
        "answer whether it is production without hesitation",
    ]:
        assert expected in text


def test_demo_rehearsal_checklist_contains_red_flags_and_safe_phrases():
    text = _text()

    for expected in [
        "Red Flags To Avoid",
        "it is production-ready",
        "it calls real providers",
        "it executes remediation",
        "Safe Phrases",
        "synthetic execution, real enterprise architecture",
        "human approval is an architectural control",
        "cloud deployment is deferred until the cloud review gate",
    ]:
        assert expected in text


def test_demo_rehearsal_checklist_final_sound_bite():
    text = _text()

    assert "EAIOS is not trying to make agents more autonomous first." in text
    assert "It is trying to make enterprise AI more governable first." in text
