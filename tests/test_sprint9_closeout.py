from pathlib import Path


DOC = Path("docs/EAIOS_2_SPRINT_9_CLOSEOUT.md")

REQUIRED_FILES = [
    Path("README.md"),
    Path("docs/EAIOS_2_SPRINT_9_ARCHITECTURE_NARRATIVE.md"),
    Path("docs/EAIOS_2_SPRINT_9_REAL_ENTERPRISE_MAPPING.md"),
    Path("docs/EAIOS_2_SPRINT_9_INTERVIEW_QA_PACK.md"),
    Path("docs/EAIOS_2_SPRINT_9_DEMO_REHEARSAL_CHECKLIST.md"),
    Path("docs/EAIOS_2_SPRINT_9_CLOUD_GATE_PRE_REVIEW.md"),
]


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_sprint9_closeout_file_exists():
    assert DOC.exists()


def test_sprint9_closeout_required_files_exist():
    assert [str(path) for path in REQUIRED_FILES if not path.exists()] == []


def test_sprint9_closeout_declares_sprint_status_and_purpose():
    text = _text()

    assert "Sprint 9 - Portfolio Polish" in text
    assert "PORTFOLIO_READY_FOR_INTERVIEW_REVIEW" in text
    assert "polished the EAIOS repository into an interview-ready and portfolio-ready package" in text
    assert "did not enable production runtime behavior" in text


def test_sprint9_closeout_lists_completed_slices():
    text = _text()

    for expected in [
        "9-1 README refresh",
        "9-2 architecture narrative",
        "9-3 real enterprise mapping",
        "9-4 interview Q&A pack",
        "9-5 demo rehearsal checklist",
        "9-6 cloud gate pre-review notes",
        "9-7 Sprint 9 closeout",
    ]:
        assert expected in text


def test_sprint9_closeout_lists_primary_artifacts():
    text = _text()

    for expected in [
        "README.md",
        "docs/EAIOS_2_SPRINT_9_ARCHITECTURE_NARRATIVE.md",
        "docs/EAIOS_2_SPRINT_9_REAL_ENTERPRISE_MAPPING.md",
        "docs/EAIOS_2_SPRINT_9_INTERVIEW_QA_PACK.md",
        "docs/EAIOS_2_SPRINT_9_DEMO_REHEARSAL_CHECKLIST.md",
        "docs/EAIOS_2_SPRINT_9_CLOUD_GATE_PRE_REVIEW.md",
        "docs/EAIOS_2_SPRINT_9_CLOSEOUT.md",
    ]:
        assert expected in text


def test_sprint9_closeout_preserves_core_message_and_operating_model():
    text = _text()

    assert "EAIOS is not just an agent demo." in text
    assert "Most agent demos try to prove an agent can act." in text
    assert "EAIOS proves the enterprise can decide when an agent must not act." in text
    assert "Business Outcome -> Capability -> Skill" in text
    assert "Maintain Application Health" in text
    assert "Application Health Management" in text



def test_sprint9_closeout_maps_real_enterprise_systems():
    text = _text()

    for expected in [
        "ServiceNow incidents",
        "BigPanda correlated alerts",
        "Dynatrace telemetry",
        "SAP SolMan SAP-specific symptoms",
        "CMDB and service graph topology",
        "Solution 360 or BSI-style business-impact context",
        "enterprise knowledge systems",
        "governed AI provider interfaces",
        "governed MCP connector interfaces",
        "CAB and AIAB-style approval models",
        "GCP or cloud preview review gates",
    ]:
        assert expected in text


def test_sprint9_closeout_centers_high_evidence_low_confidence():
    text = _text()

    assert "HIGH evidence / LOW operational confidence split" in text
    assert "evidence is coherent enough to support a hypothesis" in text
    assert "lacks enough validation to act safely" in text
    assert "does not confuse evidence strength with permission to act" in text


def test_sprint9_closeout_preserves_safety_posture():
    text = _text()

    for expected in [
        "review-only",
        "synthetic-data-driven",
        "production-data-disconnected",
        "provider-disabled",
        "MCP-connector-disabled",
        "write-disabled",
        "notification-disabled",
        "remediation-disabled",
        "benchmark-isolated",
        "human-approval-required",
        "autonomous-action-disabled",
        "release-gated",
        "cloud-deployment-deferred",
    ]:
        assert expected in text


def test_sprint9_closeout_documents_non_claims():
    text = _text()

    for expected in [
        "production deployment",
        "real cloud runtime",
        "real production data integration",
        "real ServiceNow execution",
        "real AI provider execution",
        "real MCP connector execution",
        "production writes",
        "production notifications",
        "production remediation",
        "autonomous action",
        "benchmark truth updates from runtime output",
    ]:
        assert expected in text


def test_sprint9_closeout_defers_cloud_and_sets_sprint10_direction():
    text = _text()

    for expected in [
        "Cloud deployment remains deferred.",
        "does not approve deployment",
        "Sprint 10 cloud preview begin as static-only",
        "what remains static and read-only",
        "whether providers remain disabled",
        "whether MCP connectors remain disabled",
        "whether secrets are required",
        "IAM boundary",
        "network boundary",
        "cost boundary",
        "rollback or disable plan",
        "Sprint 10 should be a cloud preview review sprint",
        "static preview scope contract",
        "provider and connector disabled-state verification",
    ]:
        assert expected in text


def test_sprint9_closeout_final_statement_and_sound_bite():
    text = _text()

    assert "Sprint 9 is closed as portfolio polish." in text
    assert "test-backed, interview-ready, portfolio-ready explanation" in text
    assert "synthetic execution with real enterprise architecture" in text
    assert "EAIOS is not trying to make agents more autonomous first." in text
    assert "It is trying to make enterprise AI more governable first." in text
