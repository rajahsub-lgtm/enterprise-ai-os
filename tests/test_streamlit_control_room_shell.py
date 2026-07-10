from pathlib import Path

from ui.components.confidence_panel import confidence_panel_model
from ui.components.control_header import control_header_model
from ui.components.governance_trace_panel import governance_passport_rows
from ui.components.human_review_panel import human_review_boundary_model
from ui.components.scenario_selector import scenario_selector_options
from ui.components.side_by_side_replay import side_by_side_columns
from ui.demo_fixtures import build_demo_comparison_view_model


STREAMLIT_APP = Path("ui/streamlit_app.py")


def test_streamlit_entrypoint_exists_and_is_canonical():
    assert STREAMLIT_APP.exists()

    text = STREAMLIT_APP.read_text(encoding="utf-8")

    assert "streamlit run ui/streamlit_app.py" in text
    assert "EAIOS 2 Control Room" in text
    assert "governed orchestration replay view-model" in text


def test_control_header_uses_sentence_case_safety_language():
    header = control_header_model()

    assert header == {
        "business_outcome": "Maintain Application Health",
        "joint_goal": "Maintain service health while preserving controls",
        "governance": "Mandatory",
        "human_approval": "Required",
        "autonomous_action": "Off",
        "memory": "Evidence, not truth",
    }


def test_demo_comparison_has_same_alert_across_memory_states():
    comparison = build_demo_comparison_view_model()

    assert comparison["comparison_label"] == "Same alert, different memory states"
    assert [
        run["scenario_label"]
        for run in comparison["runs"]
    ] == [
        "First-time / no memory",
        "Trusted memory / validated pattern",
        "Drift or conflict",
    ]

    alerts = [
        run["current_alert"]
        for run in comparison["runs"]
    ]

    assert alerts[0] == alerts[1] == alerts[2]


def test_side_by_side_replay_shows_adaptive_depth_and_constant_governance():
    comparison = build_demo_comparison_view_model()
    columns = side_by_side_columns(comparison)

    assert [
        column["agent_step_count"]
        for column in columns
    ] == [7, 3, 5]

    assert [
        column["selected_due_diligence_level"]
        for column in columns
    ] == [
        "FULL_DUE_DILIGENCE",
        "TARGETED_VALIDATION",
        "EXPANDED_VALIDATION",
    ]

    for column in columns:
        assert column["governance_required"] is True
        assert column["human_approval_required"] is True
        assert column["autonomous_action_allowed"] is False


def test_scenario_selector_uses_run_view_models_without_recomputing_decisions():
    comparison = build_demo_comparison_view_model()
    options = scenario_selector_options(comparison)

    assert options == [
        {
            "run_id": "run-no-memory",
            "label": "First-time / no memory",
            "confidence": "LOW",
            "due_diligence": "FULL_DUE_DILIGENCE",
        },
        {
            "run_id": "run-trusted-memory",
            "label": "Trusted memory / validated pattern",
            "confidence": "HIGH",
            "due_diligence": "TARGETED_VALIDATION",
        },
        {
            "run_id": "run-drift-conflict",
            "label": "Drift or conflict",
            "confidence": "MEDIUM",
            "due_diligence": "EXPANDED_VALIDATION",
        },
    ]


def test_confidence_panel_and_governance_passport_render_selected_run_values():
    comparison = build_demo_comparison_view_model()
    selected = comparison["runs"][1]

    confidence = confidence_panel_model(selected)
    rows = governance_passport_rows(selected)

    assert confidence["operational_confidence"] == "HIGH"
    assert confidence["selected_due_diligence_level"] == "TARGETED_VALIDATION"
    assert confidence["why"]

    assert rows == selected["governance_trace_view"]["rows"]
    assert {row["governance_decision"] for row in rows} == {"ALLOW", "DENY"}


def test_human_review_boundary_remains_visible_and_non_autonomous():
    comparison = build_demo_comparison_view_model()
    selected = comparison["runs"][0]

    boundary = human_review_boundary_model(selected)

    assert boundary["title"] == "Human approval required"
    assert boundary["governance_required"] is True
    assert boundary["human_approval_required"] is True
    assert boundary["autonomous_action_allowed"] is False
    assert "Request more evidence" in boundary["available_actions"]
    assert "No production action is executed." in boundary["note"]
