from pathlib import Path

from ui.components.story_replay_panel import (
    constant_governance_boundaries,
    replay_story_cards,
    story_thesis_model,
)
from ui.demo_fixtures import build_demo_comparison_view_model


STREAMLIT_APP = Path("ui/streamlit_app.py")


def test_story_thesis_states_same_alert_and_governance_message():
    comparison = build_demo_comparison_view_model()

    thesis = story_thesis_model(comparison)

    assert thesis["title"] == "Same alert. Different due diligence. Same governance."
    assert thesis["thesis"] == "Behavior adapts. Governance does not relax."
    assert "All columns replay the same alert" in thesis["same_alert"]
    assert "Digital Checkout" in thesis["same_alert"]


def test_story_thesis_shows_adaptive_behavior_per_column():
    comparison = build_demo_comparison_view_model()

    thesis = story_thesis_model(comparison)

    assert thesis["adaptive_behavior"] == [
        {
            "scenario_label": "First-time / no memory",
            "confidence": "LOW",
            "due_diligence": "FULL_DUE_DILIGENCE",
            "agent_step_count": 7,
        },
        {
            "scenario_label": "Trusted memory / validated pattern",
            "confidence": "HIGH",
            "due_diligence": "TARGETED_VALIDATION",
            "agent_step_count": 3,
        },
        {
            "scenario_label": "Drift or conflict",
            "confidence": "MEDIUM",
            "due_diligence": "EXPANDED_VALIDATION",
            "agent_step_count": 5,
        },
    ]


def test_constant_governance_boundaries_are_identical_across_replay_columns():
    comparison = build_demo_comparison_view_model()

    boundaries = constant_governance_boundaries(comparison)

    assert boundaries["governance_required"] is True
    assert boundaries["human_approval_required"] is True
    assert boundaries["autonomous_action_allowed"] is False
    assert "remain constant" in boundaries["statement"]


def test_replay_story_cards_show_three_act_demo_roles_and_step_contrast():
    comparison = build_demo_comparison_view_model()

    cards = replay_story_cards(comparison)

    assert [
        card["story_role"]
        for card in cards
    ] == [
        "Act 1 — first-time alert",
        "Act 2 — trusted memory",
        "Act 3 — drift or conflict",
    ]

    assert [
        card["behavior_headline"]
        for card in cards
    ] == [
        "7 governed agent steps → FULL_DUE_DILIGENCE",
        "3 governed agent steps → TARGETED_VALIDATION",
        "5 governed agent steps → EXPANDED_VALIDATION",
    ]


def test_replay_story_cards_surface_failures_as_governance_features():
    comparison = build_demo_comparison_view_model()

    cards = replay_story_cards(comparison)

    for card in cards:
        assert card["excluded_evidence_count"] == 1
        assert card["evidence_gap_count"] == 1
        assert card["denied_source_access_count"] == 1
        assert card["boundary_statement"] == (
            "Governance required. Human approval required. Autonomous action off."
        )


def test_streamlit_app_renders_story_ready_replay_language():
    text = STREAMLIT_APP.read_text(encoding="utf-8")

    assert "story_thesis_model" in text
    assert "replay_story_cards" in text
    assert "The columns replay the same alert" in text
    assert "Why this depth?" in text
