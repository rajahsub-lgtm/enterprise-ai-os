"""
Reasoning detective board component model.

Classification: EAIOS Presentation Layer

This component renders reasoning and recommendation outputs already present in
the ReplayRunViewModel.

It does not generate reasoning.
It does not select hypotheses.
It does not approve recommendations.
"""

from __future__ import annotations

from typing import Any


def reasoning_board_model(run_view_model: dict[str, Any]) -> dict[str, Any]:
    reasoning = run_view_model.get("reasoning_explanation") or {}

    return {
        "title": "Reasoning detective board",
        "situation": reasoning.get("situation"),
        "is": reasoning.get("is", []),
        "is_not": reasoning.get("is_not", []),
        "distinctions": reasoning.get("distinctions", []),
        "candidate_hypotheses": reasoning.get("candidate_hypotheses", []),
        "selected_hypothesis": reasoning.get("selected_hypothesis"),
        "why_chain": reasoning.get("why_chain", []),
        "limits": reasoning.get("limits", []),
        "story": "Reasoning is rendered as a structured investigation board, not a free-form answer.",
    }


def recommendation_review_model(run_view_model: dict[str, Any]) -> dict[str, Any]:
    recommendation = run_view_model.get("recommendation_candidate") or {}
    boundaries = run_view_model.get("safety_boundaries", {})

    return {
        "title": recommendation.get(
            "title",
            "Human-reviewed operational recommendation",
        ),
        "summary": recommendation.get("summary"),
        "risk_level": recommendation.get("risk_level"),
        "selected_due_diligence_level": recommendation.get(
            "selected_due_diligence_level"
        ),
        "required_controls": recommendation.get("required_controls", []),
        "prohibited_actions": recommendation.get("prohibited_actions", []),
        "approval_state": recommendation.get("approval_state"),
        "autonomous_action_allowed": recommendation.get(
            "autonomous_action_allowed",
            boundaries.get("autonomous_action_allowed"),
        ),
        "human_approval_required": boundaries.get("human_approval_required"),
        "governance_required": boundaries.get("governance_required"),
        "available_actions": [
            "Approve recommendation",
            "Reject recommendation",
            "Request more evidence",
        ],
        "story": "The replay ends with a review package. EAIOS can recommend, but cannot bypass human approval.",
    }
