from pathlib import Path


DOC = Path("docs/EAIOS_2_SPRINT_8_INTERVIEW_WALKTHROUGH.md")


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_interview_walkthrough_file_exists():
    assert DOC.exists()


def test_interview_walkthrough_declares_positioning():
    text = _text()

    assert "interview-ready scripts" in text
    assert "enterprise AI architect" in text
    assert "EAIOS is a governed enterprise AI operating-system pattern." in text
    assert "This is not a demo of an agent acting autonomously." in text


def test_interview_walkthrough_contains_one_sentence_summary():
    text = _text()

    assert "One-Sentence Summary" in text
    assert "coordinate AI agents around application health" in text
    assert "evidence governance" in text
    assert "human approval" in text
    assert "benchmark isolation" in text


def test_interview_walkthrough_contains_five_minute_script():
    text = _text()

    for expected in [
        "Five-Minute Walkthrough",
        "0:00 ? Opening",
        "0:30 ? Why This Matters",
        "1:15 ? Data Posture",
        "2:00 ? Demo Flow",
        "3:00 ? Governance Moment",
        "4:00 ? Enterprise Readiness",
        "4:45 ? Close",
    ]:
        assert expected in text


def test_interview_walkthrough_contains_fifteen_minute_script():
    text = _text()

    for expected in [
        "Fifteen-Minute Walkthrough",
        "0:00 ? Opening Frame",
        "1:30 ? Business Problem",
        "3:00 ? Synthetic But Enterprise-Shaped Data",
        "4:30 ? Governed Reasoning",
        "6:00 ? The Centerpiece Behavior",
        "7:30 ? Human Approval",
        "9:00 ? Provider and Connector Safety",
        "10:45 ? Audit and Release Gating",
        "12:00 ? Cloud Deployment Posture",
        "13:30 ? Why This Is Different",
        "14:30 ? Close",
    ]:
        assert expected in text



def test_interview_walkthrough_centers_high_evidence_low_confidence():
    text = _text()

    assert "HIGH evidence / LOW operational confidence split" in text
    assert "coherent enough to support a hypothesis" in text
    assert "lacks enough validation to act safely" in text
    assert "prevent over-automation" in text


def test_interview_walkthrough_maps_synthetic_to_real_enterprise_sources():
    text = _text()

    for expected in [
        "ServiceNow incidents",
        "BigPanda or similar event-correlation systems",
        "Dynatrace and observability platforms",
        "SAP SolMan",
        "CMDB or service graph",
        "Solution 360 or BSI-style context",
        "KB articles, runbooks, and wikis",
    ]:
        assert expected in text


def test_interview_walkthrough_preserves_blocked_action_story():
    text = _text()

    for expected in [
        "No remediation is executed.",
        "No notification is sent.",
        "No connector write occurs.",
        "No production record is modified.",
        "No benchmark truth is updated.",
        "Real connectors are not enabled in the demo.",
    ]:
        assert expected in text


def test_interview_walkthrough_includes_cloud_gate_story():
    text = _text()

    for expected in [
        "Cloud deployment is intentionally deferred.",
        "cloud review gate",
        "whether providers and connectors remain disabled",
        "whether secrets are required",
        "IAM boundary",
        "cost boundary",
        "rollback or disable plan",
    ]:
        assert expected in text


def test_interview_walkthrough_contains_qa_anchors():
    text = _text()

    for expected in [
        "Interview Q&A Anchors",
        "Why synthetic data?",
        "What is real?",
        "What is not real yet?",
        "Why is HIGH evidence but LOW confidence important?",
        "What prevents unsafe action?",
        "What would come before cloud deployment?",
    ]:
        assert expected in text


def test_interview_walkthrough_contains_final_sound_bite():
    text = _text()

    assert "EAIOS is not trying to make agents more autonomous first." in text
    assert "It is trying to make enterprise AI more governable first." in text
