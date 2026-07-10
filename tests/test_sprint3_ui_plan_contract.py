from pathlib import Path


UI_PLAN = Path("docs/EAIOS_2_SPRINT_3_UI_PLAN.md")
CONTRACT_MAP = Path("docs/EAIOS_2_UI_VIEW_MODEL_CONTRACT_MAP.md")


def test_sprint3_ui_plan_exists_and_defines_replay_not_dashboard():
    assert UI_PLAN.exists()

    text = UI_PLAN.read_text(encoding="utf-8")

    assert "Do not build a dashboard." in text
    assert "Build a governed orchestration replay." in text
    assert "Behavior adapts." in text
    assert "Governance does not relax." in text


def test_sprint3_ui_plan_commits_to_one_way_json_visualization_strategy():
    text = UI_PLAN.read_text(encoding="utf-8")

    assert "one-way JSON export" in text
    assert "standalone React/HTML replay canvas" in text
    assert "bidirectional Streamlit component" in text
    assert "optional future polish" in text


def test_sprint3_ui_plan_keeps_ui_outside_core_boundary():
    text = UI_PLAN.read_text(encoding="utf-8")

    assert "src/views" in text
    assert "headless, domain-neutral, tested core view-model layer" in text
    assert "ui" in text
    assert "domain-aware presentation layer" in text
    assert "must not be added to core vocabulary-boundary tests" in text


def test_sprint3_ui_contract_map_exists():
    assert CONTRACT_MAP.exists()

    text = CONTRACT_MAP.read_text(encoding="utf-8")

    assert "The UI must render engine state." in text
    assert "The UI must not invent runtime state." in text


def test_sprint3_ui_contract_map_names_provenance_invariants():
    text = CONTRACT_MAP.read_text(encoding="utf-8")

    required_invariants = [
        "audit_id",
        "evidence_id",
        "governance_decision",
        "content_safety_status",
        "allowed_for_reasoning",
        "approval_state",
        "operational_confidence",
        "confidence_direction",
        "pattern_maturity",
        "selected_due_diligence_level",
        "autonomous_action_allowed",
    ]

    for invariant in required_invariants:
        assert invariant in text


def test_sprint3_ui_contract_map_defines_comparison_view_model():
    text = CONTRACT_MAP.read_text(encoding="utf-8")

    assert "ComparisonViewModel" in text
    assert "collection of ReplayRunViewModel instances" in text
    assert "First-time / no memory" in text
    assert "Trusted memory / validated pattern" in text
    assert "Drift or conflict" in text


def test_sprint3_ui_contract_map_reconciles_app_py_entrypoint():
    text = CONTRACT_MAP.read_text(encoding="utf-8")

    assert "ui/streamlit_app.py" in text
    assert "root-level `app.py`" in text
    assert "deprecated or quarantined" in text
