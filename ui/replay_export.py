"""
Sprint 3-UI one-way replay JSON export.

Classification: EAIOS Presentation Layer

This module exports deterministic replay view-models for external renderers.

Default rich-render path:

    Python -> replay JSON -> standalone React Flow / HTML replay canvas

The exported JSON is a rendering contract, not a decision engine.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ui.demo_fixtures import build_demo_comparison_view_model
from ui.visual_replay_paths import (
    build_demo_story_contract,
    build_visual_paths_by_run,
)


EXPORT_SCHEMA_VERSION = "eaios-ui-replay-v1"


def build_replay_export_payload(
    comparison_view_model: dict[str, Any] | None = None,
) -> dict[str, Any]:
    comparison = comparison_view_model or build_demo_comparison_view_model()

    payload = {
        "schema_version": EXPORT_SCHEMA_VERSION,
        "export_purpose": "standalone_replay_renderer",
        "source_of_truth": "Sprint 3 tested headless view-model outputs",
        "renderer_contract": {
            "direction": "one_way_json",
            "python_owns_decisions": True,
            "renderer_owns_playhead": True,
            "renderer_must_not_invent_decisions": True,
        },
        "comparison": comparison,
        "runs": comparison["runs"],
        "demo_story": build_demo_story_contract(),
        "visual_paths_by_run": build_visual_paths_by_run(comparison),
        "visual_event_count": sum(
            len(events)
            for events in build_visual_paths_by_run(comparison).values()
        ),
        "animation_event_count": sum(
            len(run.get("animation_events", []))
            for run in comparison["runs"]
        ),
        "safety_boundaries": _collect_safety_boundaries(comparison),
        "provenance_summary": _collect_provenance_summary(comparison),
    }

    return payload


def write_replay_export(
    path: str | Path,
    comparison_view_model: dict[str, Any] | None = None,
) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    payload = build_replay_export_payload(comparison_view_model)

    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    return output_path


def _collect_safety_boundaries(comparison: dict[str, Any]) -> dict[str, Any]:
    summaries = comparison["summary"]

    return {
        "governance_required_values": sorted(
            {
                summary["governance_required"]
                for summary in summaries
            },
            key=str,
        ),
        "human_approval_required_values": sorted(
            {
                summary["human_approval_required"]
                for summary in summaries
            },
            key=str,
        ),
        "autonomous_action_allowed_values": sorted(
            {
                summary["autonomous_action_allowed"]
                for summary in summaries
            },
            key=str,
        ),
    }


def _collect_provenance_summary(comparison: dict[str, Any]) -> dict[str, Any]:
    audit_ids = set()
    evidence_ids = set()
    decisions = set()
    approval_states = set()
    confidence_values = set()
    due_diligence_values = set()

    for run in comparison["runs"]:
        provenance = run.get("provenance", {})

        audit_ids.update(provenance.get("audit_ids", []))
        evidence_ids.update(provenance.get("evidence_ids", []))
        decisions.update(provenance.get("governance_decisions", []))
        approval_states.update(provenance.get("approval_states", []))

        if run.get("operational_confidence"):
            confidence_values.add(run["operational_confidence"])

        if run.get("selected_due_diligence_level"):
            due_diligence_values.add(run["selected_due_diligence_level"])

    return {
        "audit_ids": sorted(audit_ids),
        "evidence_ids": sorted(evidence_ids),
        "governance_decisions": sorted(decisions),
        "approval_states": sorted(approval_states),
        "operational_confidence_values": sorted(confidence_values),
        "due_diligence_values": sorted(due_diligence_values),
    }
