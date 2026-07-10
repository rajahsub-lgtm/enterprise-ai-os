from pathlib import Path


README = Path("README.md")
CLOSEOUT = Path("docs/EAIOS_2_SPRINT_3_CLOSEOUT.md")


def test_sprint3_closeout_doc_exists():
    assert CLOSEOUT.exists()


def test_sprint3_closeout_captures_core_control_story():
    text = CLOSEOUT.read_text(encoding="utf-8-sig")

    assert "Same alert." in text
    assert "Different enterprise memory." in text
    assert "Different operational confidence." in text
    assert "Different due-diligence depth." in text
    assert "Same governance." in text
    assert "Same human approval boundary." in text
    assert "No autonomous production action." in text


def test_sprint3_closeout_documents_engine_and_ui_checkpoints():
    text = CLOSEOUT.read_text(encoding="utf-8-sig")

    assert "## Engine Checkpoint" in text
    assert "Operational confidence assessment." in text
    assert "Governed evidence packaging." in text
    assert "Governance trace view model." in text

    assert "## UI Checkpoint" in text
    assert "One-way replay JSON export." in text
    assert "Standalone animated replay canvas." in text
    assert "Export-driven visual replay paths." in text


def test_sprint3_closeout_documents_demo_entry_point():
    text = CLOSEOUT.read_text(encoding="utf-8-sig")

    assert "python scripts\\export_sprint3_ui_replay_json.py" in text
    assert "python -m http.server 8765" in text
    assert "http://localhost:8765/ui_static/replay_canvas/index.html" in text


def test_sprint3_closeout_documents_three_demo_acts():
    text = CLOSEOUT.read_text(encoding="utf-8-sig")

    assert "Act 1: First-time / no memory" in text
    assert "7 visual events" in text
    assert "FULL_DUE_DILIGENCE" in text

    assert "Act 2: Trusted memory / validated pattern" in text
    assert "3 visual events" in text
    assert "TARGETED_VALIDATION" in text

    assert "Act 3: Drift or conflict" in text
    assert "5 visual events" in text
    assert "EXPANDED_VALIDATION" in text


def test_sprint3_closeout_documents_renderer_boundary():
    text = CLOSEOUT.read_text(encoding="utf-8-sig")

    assert "The UI does not make decisions." in text
    assert "ReplayRunViewModel" in text
    assert "ComparisonViewModel" in text
    assert "JSON export contract" in text
    assert "standalone renderer" in text
    assert "Replay path length." in text


def test_sprint3_closeout_documents_safety_boundary():
    text = CLOSEOUT.read_text(encoding="utf-8-sig")

    assert "governance_required = True" in text
    assert "human_approval_required = True" in text
    assert "autonomous_action_allowed = False" in text


def test_readme_links_sprint3_demo_package():
    text = README.read_text(encoding="utf-8-sig")

    assert "## EAIOS 2 Sprint 3 Demo" in text
    assert "docs/EAIOS_2_SPRINT_3_CLOSEOUT.md" in text
    assert "docs/EAIOS_2_SPRINT_3_UI_DEMO_WALKTHROUGH.md" in text
    assert "docs/EAIOS_2_SPRINT_3_UI_ARCHITECTURE_CHECKPOINT.md" in text
    assert "Python owns decisions." in text
    assert "Renderer owns play-head." in text
    assert "Renderer must not invent replay paths." in text
