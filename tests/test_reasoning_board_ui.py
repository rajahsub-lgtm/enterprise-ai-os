from pathlib import Path

from ui.components.reasoning_board import (
    reasoning_board_model,
    recommendation_review_model,
)
from ui.demo_fixtures import build_demo_comparison_view_model


STREAMLIT_APP = Path("ui/streamlit_app.py")


def selected_run(label: str):
    comparison = build_demo_comparison_view_model()

    return next(
        run
        for run in comparison["runs"]
        if run["scenario_label"] == label
    )


def test_reasoning_board_renders_structured_investigation_sections():
    run = selected_run("First-time / no memory")

    board = reasoning_board_model(run)

    assert board["title"] == "Reasoning detective board"
    assert "Digital Checkout" in board["situation"]
    assert "Digital Checkout is affected." in board["is"]
    assert "Autonomous production action is not approved." in board["is_not"]
    assert board["distinctions"]
    assert board["candidate_hypotheses"]
    assert board["selected_hypothesis"] == (
        "Treat as a new operational degradation until evidence matures."
    )
    assert board["why_chain"]
    assert board["limits"]
    assert "structured investigation board" in board["story"]


def test_reasoning_board_changes_story_by_memory_state_without_changing_boundaries():
    trusted = selected_run("Trusted memory / validated pattern")
    drift = selected_run("Drift or conflict")

    trusted_board = reasoning_board_model(trusted)
    drift_board = reasoning_board_model(drift)

    assert trusted_board["selected_hypothesis"] == (
        "Validated payment authorization pattern likely recurred, pending targeted human validation."
    )
    assert drift_board["selected_hypothesis"] == (
        "Treat as drift or conflict and expand validation before relying on memory."
    )

    assert trusted["safety_boundaries"] == {
        "governance_required": True,
        "human_approval_required": True,
        "autonomous_action_allowed": False,
    }
    assert drift["safety_boundaries"] == trusted["safety_boundaries"]


def test_recommendation_review_renders_candidate_without_approving_it():
    run = selected_run("Trusted memory / validated pattern")

    review = recommendation_review_model(run)

    assert review["title"] == "Human-reviewed operational recommendation"
    assert review["risk_level"] == "Medium"
    assert review["selected_due_diligence_level"] == "TARGETED_VALIDATION"
    assert "Human approval" in review["required_controls"]
    assert "No autonomous production action" in review["required_controls"]
    assert "Do not execute remediation automatically." in review[
        "prohibited_actions"
    ]
    assert "Do not treat memory as truth." in review["prohibited_actions"]
    assert review["approval_state"] == "PENDING_HUMAN_REVIEW"
    assert review["autonomous_action_allowed"] is False
    assert review["human_approval_required"] is True
    assert review["governance_required"] is True
    assert "Request more evidence" in review["available_actions"]


def test_recommendation_review_surfaces_higher_risk_for_first_time_and_drift():
    first_time = recommendation_review_model(
        selected_run("First-time / no memory")
    )
    drift = recommendation_review_model(
        selected_run("Drift or conflict")
    )

    assert first_time["risk_level"] == "High"
    assert drift["risk_level"] == "High"
    assert first_time["autonomous_action_allowed"] is False
    assert drift["autonomous_action_allowed"] is False


def test_streamlit_app_renders_reasoning_and_recommendation_sections():
    text = STREAMLIT_APP.read_text(encoding="utf-8")

    assert "reasoning_board_model" in text
    assert "recommendation_review_model" in text
    assert "Reasoning detective board" in text
    assert "Recommendation review" in text
    assert "Is / Is not" in text
    assert "Hypotheses and why-chain" in text
