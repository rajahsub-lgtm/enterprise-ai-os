"""
Visual replay path contract for Sprint 3-UI standalone renderers.

Classification: EAIOS Presentation Layer

These visual paths are demo-oriented renderer events derived from tested
ReplayRunViewModel scenarios. The browser renderer must consume these paths;
it must not invent path length or due-diligence story.
"""

from __future__ import annotations

from typing import Any


PATH_STORY_BY_SCENARIO: dict[str, dict[str, str]] = {
    "First-time / no memory": {
        "path_class": "path-full-diligence",
        "title": "Full due diligence",
        "explanation": (
            "No reliable memory exists, so EAIOS must gather broader evidence "
            "before recommending anything."
        ),
        "end_title": "Full diligence complete",
        "end_summary": (
            "EAIOS completed the seven-step replay, preserved evidence "
            "exclusions and gaps, and routed the package to human review."
        ),
    },
    "Trusted memory / validated pattern": {
        "path_class": "path-targeted-validation",
        "title": "Targeted validation",
        "explanation": (
            "Trusted memory raises confidence, so EAIOS validates the known "
            "pattern instead of repeating full due diligence."
        ),
        "end_title": "Targeted validation complete",
        "end_summary": (
            "EAIOS stopped after three focused events because memory supported "
            "confidence, while human approval remained required."
        ),
    },
    "Drift or conflict": {
        "path_class": "path-expanded-validation",
        "title": "Expanded validation",
        "explanation": (
            "Memory exists but may be drifting or conflicting, so EAIOS expands "
            "validation before relying on prior knowledge."
        ),
        "end_title": "Expanded validation complete",
        "end_summary": (
            "EAIOS exposed drift, evidence gaps, and uncertainty before routing "
            "the review package to the human reviewer."
        ),
    },
}


VISUAL_PATHS_BY_SCENARIO: dict[str, list[dict[str, str]]] = {
    "First-time / no memory": [
        {
            "event_type": "NODE_ACTIVATED",
            "node_id": "joint_goal",
            "label": "Joint goal accepted",
            "caption": (
                "EAIOS begins with the joint goal: maintain service health "
                "while preserving controls."
            ),
        },
        {
            "event_type": "NODE_ACTIVATED",
            "node_id": "visual::memory_pattern_agent",
            "label": "Memory pattern check",
            "caption": (
                "No reliable prior memory pattern is available, so EAIOS "
                "cannot shortcut the investigation."
            ),
        },
        {
            "event_type": "NODE_ACTIVATED",
            "node_id": "visual::telemetry_agent",
            "label": "Telemetry collection",
            "caption": (
                "Telemetry is collected to establish current operational state."
            ),
        },
        {
            "event_type": "NODE_ACTIVATED",
            "node_id": "visual::knowledge_retrieval_agent",
            "label": "Knowledge retrieval",
            "caption": (
                "Knowledge evidence is requested, but review-required evidence "
                "cannot enter reasoning."
            ),
        },
        {
            "event_type": "EVIDENCE_TOKEN_MOVED",
            "node_id": "evidence_fusion",
            "label": "Evidence fusion",
            "caption": (
                "Only reasoning-eligible governed evidence enters fusion."
            ),
        },
        {
            "event_type": "DUE_DILIGENCE_SELECTED",
            "node_id": "due_diligence",
            "label": "Full due diligence selected",
            "caption": "Low confidence selects FULL_DUE_DILIGENCE.",
        },
        {
            "event_type": "HUMAN_REVIEW_REQUIRED",
            "node_id": "human_review",
            "label": "Human review package",
            "caption": (
                "The recommendation package is routed to human review. "
                "Autonomous action remains off."
            ),
        },
    ],
    "Trusted memory / validated pattern": [
        {
            "event_type": "NODE_ACTIVATED",
            "node_id": "joint_goal",
            "label": "Joint goal accepted",
            "caption": (
                "EAIOS begins with the same Digital Checkout alert and the "
                "same control boundary."
            ),
        },
        {
            "event_type": "NODE_ACTIVATED",
            "node_id": "visual::memory_pattern_agent",
            "label": "Trusted memory validated",
            "caption": (
                "A validated memory pattern increases confidence, but memory "
                "is still evidence, not truth."
            ),
        },
        {
            "event_type": "HUMAN_REVIEW_REQUIRED",
            "node_id": "human_review",
            "label": "Targeted human validation",
            "caption": (
                "The replay stops after targeted validation. Human approval "
                "remains required."
            ),
        },
    ],
    "Drift or conflict": [
        {
            "event_type": "NODE_ACTIVATED",
            "node_id": "joint_goal",
            "label": "Joint goal accepted",
            "caption": (
                "EAIOS begins with the same alert and checks whether memory "
                "still applies."
            ),
        },
        {
            "event_type": "NODE_ACTIVATED",
            "node_id": "visual::memory_pattern_agent",
            "label": "Memory drift detected",
            "caption": (
                "Memory exists, but drift or conflict prevents blind reuse."
            ),
        },
        {
            "event_type": "NODE_ACTIVATED",
            "node_id": "visual::telemetry_agent",
            "label": "Expanded validation",
            "caption": (
                "Additional telemetry validation is required because confidence "
                "is not stable."
            ),
        },
        {
            "event_type": "EVIDENCE_GAP_CREATED",
            "node_id": "visual::evidence_gap",
            "label": "Evidence gap exposed",
            "caption": (
                "Denied source access and missing evidence stay visible for "
                "the reviewer."
            ),
        },
        {
            "event_type": "HUMAN_REVIEW_REQUIRED",
            "node_id": "human_review",
            "label": "Human review package",
            "caption": (
                "The reviewer receives the drift-aware package. Autonomous "
                "action remains off."
            ),
        },
    ],
}


def build_visual_paths_by_run(
    comparison_view_model: dict[str, Any],
) -> dict[str, list[dict[str, Any]]]:
    visual_paths: dict[str, list[dict[str, Any]]] = {}

    for run in comparison_view_model["runs"]:
        scenario_label = run["scenario_label"]
        run_id = run["run_id"]
        scenario_events = VISUAL_PATHS_BY_SCENARIO[scenario_label]
        total = len(scenario_events)

        visual_paths[run_id] = [
            {
                **event,
                "event_id": f"{run_id}-VISUAL-{index:02d}",
                "run_id": run_id,
                "visual_step_number": index,
                "visual_step_total": total,
            }
            for index, event in enumerate(scenario_events, start=1)
        ]

    return visual_paths


def build_demo_story_contract() -> dict[str, Any]:
    return {
        "same_alert": {
            "application": "Digital Checkout",
            "symptom": (
                "Payment authorization latency and elevated error rate"
            ),
        },
        "path_story_by_scenario": PATH_STORY_BY_SCENARIO,
    }
