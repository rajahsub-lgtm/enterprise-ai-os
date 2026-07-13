from pathlib import Path


DOC = Path("docs/EAIOS_2_SPRINT_8_CLOSEOUT.md")

REQUIRED_FILES = [
    Path("src/eaios/sprint8/operator_demo_command.py"),
    Path("src/eaios/sprint8/static_demo_export.py"),
    Path("docs/EAIOS_2_SPRINT_8_DEMO_STORYBOARD.md"),
    Path("docs/EAIOS_2_SPRINT_8_REAL_SYNTHETIC_DATA_MAP.md"),
    Path("docs/EAIOS_2_SPRINT_8_INTERVIEW_WALKTHROUGH.md"),
]


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_sprint8_closeout_file_exists():
    assert DOC.exists()


def test_sprint8_closeout_required_files_exist():
    assert [str(path) for path in REQUIRED_FILES if not path.exists()] == []


def test_sprint8_closeout_declares_interview_ready_status():
    text = _text()

    assert "Sprint 8 ? Interview Demo Readiness" in text
    assert "INTERVIEW_READY" in text
    assert "interview-ready demo package" in text


def test_sprint8_closeout_lists_completed_slices():
    text = _text()

    for expected in [
        "8-1 canonical operator demo command",
        "8-2 demo storyboard",
        "8-3 real and synthetic data map",
        "8-4 interview walkthrough script",
        "8-5 static demo export",
        "8-6 Sprint 8 closeout",
    ]:
        assert expected in text


def test_sprint8_closeout_lists_primary_artifacts():
    text = _text()

    for expected in [
        "src/eaios/sprint8/operator_demo_command.py",
        "src/eaios/sprint8/static_demo_export.py",
        "docs/EAIOS_2_SPRINT_8_DEMO_STORYBOARD.md",
        "docs/EAIOS_2_SPRINT_8_REAL_SYNTHETIC_DATA_MAP.md",
        "docs/EAIOS_2_SPRINT_8_INTERVIEW_WALKTHROUGH.md",
        "docs/EAIOS_2_SPRINT_8_CLOSEOUT.md",
    ]:
        assert expected in text


def test_sprint8_closeout_preserves_safety_posture():
    text = _text()

    for expected in [
        "review-only demo execution",
        "synthetic ITIL/AIOps data",
        "no production data connection",
        "no provider execution",
        "no real MCP connector execution",
        "no cloud deployment",
        "no release creation",
        "no notifications",
        "no remediation",
        "no production writes",
        "no benchmark truth updates",
        "human approval required",
        "autonomous remediation disabled",
    ]:
        assert expected in text



def test_sprint8_closeout_centers_high_evidence_low_confidence():
    text = _text()

    assert "HIGH evidence / LOW operational confidence split" in text
    assert "evidence is coherent enough to support a hypothesis" in text
    assert "lacks enough validation to act safely" in text
    assert "The system refuses to over-trust itself." in text


def test_sprint8_closeout_maps_real_and_synthetic_data():
    text = _text()

    for expected in [
        "synthetic in execution and real in architecture",
        "incident-like records",
        "alert-like records",
        "telemetry-like records",
        "ServiceNow incidents",
        "BigPanda correlated alerts",
        "Dynatrace telemetry",
        "SAP SolMan signals",
        "CMDB and service graph context",
        "Solution 360 or BSI-style business impact",
    ]:
        assert expected in text


def test_sprint8_closeout_declares_what_is_interview_ready():
    text = _text()

    for expected in [
        "canonical operator demo command",
        "static demo export model",
        "demo storyboard",
        "real and synthetic data map",
        "five-minute interview script",
        "fifteen-minute interview script",
        "Q&A anchors",
        "Sprint 7 runtime hardening chain",
        "release checklist posture",
        "explicit cloud review gate",
    ]:
        assert expected in text


def test_sprint8_closeout_documents_non_claims():
    text = _text()

    for expected in [
        "production deployment",
        "real cloud runtime",
        "real production data integration",
        "real ServiceNow execution",
        "real provider execution",
        "real MCP connector execution",
        "autonomous remediation",
        "production writes",
        "benchmark truth updates from runtime output",
    ]:
        assert expected in text


def test_sprint8_closeout_defers_cloud_deployment_to_review_gate():
    text = _text()

    for expected in [
        "Cloud deployment is intentionally deferred",
        "what is deployed",
        "what remains static and read-only",
        "whether providers remain disabled",
        "whether MCP connectors remain disabled",
        "whether secrets are required",
        "IAM boundary",
        "cost boundary",
        "rollback or disable plan",
    ]:
        assert expected in text


def test_sprint8_closeout_sets_sprint9_direction():
    text = _text()

    for expected in [
        "Sprint 9 should focus on portfolio polish.",
        "GitHub README refresh",
        "architecture narrative",
        "real enterprise mapping",
        "interview Q&A pack",
        "demo rehearsal checklist",
        "cloud gate pre-review notes",
        "Sprint 9 closeout",
    ]:
        assert expected in text


def test_sprint8_closeout_has_no_secret_or_execution_snippets():
    text = _text().lower()

    assert "api_key" not in text
    assert "password" not in text
    assert "bearer " not in text
    assert "curl " not in text
    assert "requests.post" not in text
    assert "httpx.post" not in text
