from pathlib import Path


WALKTHROUGH = Path("docs/EAIOS_2_SPRINT_3_UI_DEMO_WALKTHROUGH.md")
ARCHITECTURE = Path("docs/EAIOS_2_SPRINT_3_UI_ARCHITECTURE_CHECKPOINT.md")


def test_sprint3_ui_demo_walkthrough_exists():
    assert WALKTHROUGH.exists()


def test_sprint3_ui_architecture_checkpoint_exists():
    assert ARCHITECTURE.exists()


def test_demo_walkthrough_captures_same_alert_adaptive_diligence_story():
    text = WALKTHROUGH.read_text(encoding="utf-8")

    assert "The demo is not a dashboard. It is a governed orchestration replay." in text
    assert "Same alert." in text
    assert "Different enterprise memory state." in text
    assert "Different due-diligence depth." in text
    assert "Same governance boundary." in text
    assert "Autonomous production action remains disabled." in text


def test_demo_walkthrough_documents_three_acts_and_event_counts():
    text = WALKTHROUGH.read_text(encoding="utf-8-sig")

    assert "Act 1" in text
    assert "First-time Alert / No Memory" in text
    assert "Act 1 stops at 7 / 7 visual events." in text

    assert "Act 2" in text
    assert "Trusted Memory / Validated Pattern" in text
    assert "Act 2 stops at 3 / 3 visual events." in text

    assert "Act 3" in text
    assert "Drift or Conflict" in text
    assert "Act 3 stops at 5 / 5 visual events." in text

def test_demo_walkthrough_documents_memory_evidence_not_truth():
    text = WALKTHROUGH.read_text(encoding="utf-8")

    assert "Memory increases confidence but is still evidence, not truth." in text
    assert "memory is evidence, not truth" in text.lower()
    assert "review-required evidence is excluded from reasoning" in text.lower()
    assert "evidence gaps remain visible" in text.lower()


def test_demo_walkthrough_documents_renderer_contract():
    text = WALKTHROUGH.read_text(encoding="utf-8")

    assert "Python exports the visual replay contract." in text
    assert "The browser only plays it." in text
    assert "The renderer owns the play-head." in text
    assert "The renderer must not invent decisions or path length." in text


def test_architecture_checkpoint_documents_ui_boundary():
    text = ARCHITECTURE.read_text(encoding="utf-8")

    assert "The UI must not become the decision engine." in text
    assert "Sprint 3 engine outputs" in text
    assert "ReplayRunViewModel" in text
    assert "ComparisonViewModel" in text
    assert "JSON export contract" in text
    assert "standalone renderer" in text


def test_architecture_checkpoint_documents_renderer_must_not_own_decisions():
    text = ARCHITECTURE.read_text(encoding="utf-8")

    assert "The renderer may own:" in text
    assert "The renderer must not own:" in text
    assert "Operational confidence decisions." in text
    assert "Due-diligence selection." in text
    assert "Governance gate decisions." in text
    assert "Scenario path length." in text


def test_architecture_checkpoint_documents_export_driven_paths():
    text = ARCHITECTURE.read_text(encoding="utf-8")

    assert "ui/visual_replay_paths.py" in text
    assert "payload.visual_paths_by_run[currentRun.run_id]" in text
    assert "payload.demo_story.path_story_by_scenario" in text
    assert "const VISUAL_PATHS_BY_SCENARIO" in text
    assert "const PATH_STORY_BY_SCENARIO" in text


def test_architecture_checkpoint_documents_scenario_path_lengths():
    text = ARCHITECTURE.read_text(encoding="utf-8")

    assert "run-no-memory        ? 7 visual events" in text
    assert "run-trusted-memory   ? 3 visual events" in text
    assert "run-drift-conflict   ? 5 visual events" in text
    assert "FULL_DUE_DILIGENCE" in text
    assert "TARGETED_VALIDATION" in text
    assert "EXPANDED_VALIDATION" in text


def test_architecture_checkpoint_documents_constant_governance_boundary():
    text = ARCHITECTURE.read_text(encoding="utf-8")

    assert "governance_required = True" in text
    assert "human_approval_required = True" in text
    assert "autonomous_action_allowed = False" in text
    assert "Behavior adapts. Governance does not relax." in text
