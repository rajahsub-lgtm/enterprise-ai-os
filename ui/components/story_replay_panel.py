"""
Story-ready replay presentation helpers.

Classification: EAIOS Presentation Layer

These helpers shape already-composed replay view-models into story cards and
control-room copy.

They do not make governance, confidence, evidence, approval, or remediation
decisions.
"""

from __future__ import annotations

from typing import Any


def story_thesis_model(comparison_view_model: dict[str, Any]) -> dict[str, Any]:
    summaries = comparison_view_model["summary"]

    return {
        "title": "Same alert. Different due diligence. Same governance.",
        "subtitle": comparison_view_model["comparison_label"],
        "thesis": "Behavior adapts. Governance does not relax.",
        "same_alert": _same_alert_statement(comparison_view_model["runs"]),
        "adaptive_behavior": [
            {
                "scenario_label": summary["scenario_label"],
                "confidence": summary["operational_confidence"],
                "due_diligence": summary["selected_due_diligence_level"],
                "agent_step_count": summary["agent_step_count"],
            }
            for summary in summaries
        ],
        "constant_boundaries": constant_governance_boundaries(comparison_view_model),
    }


def replay_story_cards(comparison_view_model: dict[str, Any]) -> list[dict[str, Any]]:
    cards = []

    for run, summary in zip(
        comparison_view_model["runs"],
        comparison_view_model["summary"],
    ):
        cards.append(
            {
                "run_id": run["run_id"],
                "scenario_label": run["scenario_label"],
                "story_role": _story_role(run["scenario_label"]),
                "behavior_headline": _behavior_headline(summary),
                "confidence": summary["operational_confidence"],
                "confidence_direction": run["confidence_direction"],
                "pattern_maturity": run["pattern_maturity"],
                "due_diligence": summary["selected_due_diligence_level"],
                "agent_step_count": summary["agent_step_count"],
                "evidence_count": summary["evidence_count"],
                "excluded_evidence_count": summary["excluded_evidence_count"],
                "evidence_gap_count": summary["evidence_gap_count"],
                "denied_source_access_count": summary[
                    "denied_source_access_count"
                ],
                "why": run["why"],
                "boundary_statement": _boundary_statement(summary),
            }
        )

    return cards


def constant_governance_boundaries(
    comparison_view_model: dict[str, Any],
) -> dict[str, Any]:
    summaries = comparison_view_model["summary"]

    governance_values = {
        summary["governance_required"]
        for summary in summaries
    }
    human_approval_values = {
        summary["human_approval_required"]
        for summary in summaries
    }
    autonomous_action_values = {
        summary["autonomous_action_allowed"]
        for summary in summaries
    }

    return {
        "governance_required": _single_value(governance_values),
        "human_approval_required": _single_value(human_approval_values),
        "autonomous_action_allowed": _single_value(autonomous_action_values),
        "statement": "Governance, human approval, and autonomous-action boundaries remain constant across every replay column.",
    }


def _same_alert_statement(runs: list[dict[str, Any]]) -> str:
    if not runs:
        return "No replay runs available."

    alert = runs[0]["current_alert"]
    application = alert.get("application", "Unknown application")
    symptom = alert.get("symptom", "Unknown symptom")

    return f"All columns replay the same alert: {application} — {symptom}."


def _story_role(scenario_label: str) -> str:
    mapping = {
        "First-time / no memory": "Act 1 — first-time alert",
        "Trusted memory / validated pattern": "Act 2 — trusted memory",
        "Drift or conflict": "Act 3 — drift or conflict",
    }

    return mapping.get(scenario_label, "Replay scenario")


def _behavior_headline(summary: dict[str, Any]) -> str:
    steps = summary["agent_step_count"]
    due_diligence = summary["selected_due_diligence_level"]

    return f"{steps} governed agent steps → {due_diligence}"


def _boundary_statement(summary: dict[str, Any]) -> str:
    if (
        summary["governance_required"] is True
        and summary["human_approval_required"] is True
        and summary["autonomous_action_allowed"] is False
    ):
        return "Governance required. Human approval required. Autonomous action off."

    return "Boundary differs from expected Sprint 3 safety posture."


def _single_value(values: set[Any]) -> Any:
    if len(values) != 1:
        return "MIXED"

    return next(iter(values))
