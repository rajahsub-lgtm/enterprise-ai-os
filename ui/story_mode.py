"""
Sprint 3-UI Story Mode event stream.

Classification: EAIOS Presentation Layer

This module converts a ReplayRunViewModel into deterministic animation events.

It does not make governance, confidence, evidence, approval, or remediation
decisions. It projects existing view-model values into replay events.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any


EVENT_NODE_ACTIVATED = "NODE_ACTIVATED"
EVENT_GOVERNANCE_GATE_STAMPED = "GOVERNANCE_GATE_STAMPED"
EVENT_EVIDENCE_TOKEN_MOVED = "EVIDENCE_TOKEN_MOVED"
EVENT_EVIDENCE_EXCLUDED = "EVIDENCE_EXCLUDED"
EVENT_EVIDENCE_GAP_CREATED = "EVIDENCE_GAP_CREATED"
EVENT_CONFIDENCE_UPDATED = "CONFIDENCE_UPDATED"
EVENT_DUE_DILIGENCE_SELECTED = "DUE_DILIGENCE_SELECTED"
EVENT_HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"

SUPPORTED_EVENT_TYPES = {
    EVENT_NODE_ACTIVATED,
    EVENT_GOVERNANCE_GATE_STAMPED,
    EVENT_EVIDENCE_TOKEN_MOVED,
    EVENT_EVIDENCE_EXCLUDED,
    EVENT_EVIDENCE_GAP_CREATED,
    EVENT_CONFIDENCE_UPDATED,
    EVENT_DUE_DILIGENCE_SELECTED,
    EVENT_HUMAN_REVIEW_REQUIRED,
}


def build_animation_events(run_view_model: dict[str, Any]) -> list[dict[str, Any]]:
    """Build deterministic replay events from a ReplayRunViewModel."""

    run_id = run_view_model["run_id"]
    events: list[dict[str, Any]] = []

    _append_event(
        events,
        run_id=run_id,
        event_type=EVENT_NODE_ACTIVATED,
        node_id="joint_goal",
        caption="EAIOS begins with the joint goal.",
    )

    for row in _governance_rows(run_view_model):
        decision = _decision(row)
        agent_id = row.get("agent_id")
        source_id = row.get("source_id")
        audit_id = row.get("audit_id")
        evidence_id = row.get("evidence_id")

        _append_event(
            events,
            run_id=run_id,
            event_type=EVENT_NODE_ACTIVATED,
            node_id=_agent_node_id(agent_id),
            agent_id=agent_id,
            source_id=source_id,
            caption=f"{agent_id} requests governed access to {source_id}.",
        )

        _append_event(
            events,
            run_id=run_id,
            event_type=EVENT_GOVERNANCE_GATE_STAMPED,
            node_id=_gate_node_id(agent_id, source_id),
            agent_id=agent_id,
            source_id=source_id,
            audit_id=audit_id,
            evidence_id=evidence_id,
            decision=decision,
            caption=f"Governance stamps {decision} for {agent_id} → {source_id}.",
        )

        if decision == "DENY":
            _append_event(
                events,
                run_id=run_id,
                event_type=EVENT_EVIDENCE_GAP_CREATED,
                node_id=_gap_node_id(agent_id, source_id),
                agent_id=agent_id,
                source_id=source_id,
                audit_id=audit_id,
                decision=decision,
                caption="Denied source access creates an evidence gap.",
            )

    for item in run_view_model.get("evidence_for_reasoning", []):
        _append_event(
            events,
            run_id=run_id,
            event_type=EVENT_EVIDENCE_TOKEN_MOVED,
            node_id=_evidence_node_id(item.get("evidence_id")),
            from_node=_source_node_id(item.get("source_id")),
            to_node="evidence_fusion",
            source_id=item.get("source_id"),
            audit_id=item.get("audit_id"),
            evidence_id=item.get("evidence_id"),
            content_safety_status=item.get("content_safety_status"),
            allowed_for_reasoning=item.get("allowed_for_reasoning"),
            caption="Reasoning-eligible governed evidence flows into fusion.",
        )

    for item in run_view_model.get("excluded_evidence", []):
        _append_event(
            events,
            run_id=run_id,
            event_type=EVENT_EVIDENCE_EXCLUDED,
            node_id=_evidence_node_id(item.get("evidence_id")),
            from_node=_source_node_id(item.get("source_id")),
            to_node="excluded_evidence",
            source_id=item.get("source_id"),
            audit_id=item.get("audit_id"),
            evidence_id=item.get("evidence_id"),
            content_safety_status=item.get("content_safety_status"),
            allowed_for_reasoning=item.get("allowed_for_reasoning"),
            caption="Evidence is excluded and does not enter reasoning.",
        )

    for gap in run_view_model.get("evidence_gaps", []):
        _append_event(
            events,
            run_id=run_id,
            event_type=EVENT_EVIDENCE_GAP_CREATED,
            node_id=_gap_node_id(gap.get("agent_id"), gap.get("source_id")),
            agent_id=gap.get("agent_id"),
            source_id=gap.get("source_id"),
            audit_id=gap.get("audit_id"),
            caption="Evidence gap is visible in the replay.",
        )

    _append_event(
        events,
        run_id=run_id,
        event_type=EVENT_CONFIDENCE_UPDATED,
        node_id="operational_confidence",
        confidence=run_view_model.get("operational_confidence"),
        confidence_direction=run_view_model.get("confidence_direction"),
        pattern_maturity=run_view_model.get("pattern_maturity"),
        caption="Operational confidence is updated from engine output.",
    )

    _append_event(
        events,
        run_id=run_id,
        event_type=EVENT_DUE_DILIGENCE_SELECTED,
        node_id="due_diligence",
        due_diligence=run_view_model.get("selected_due_diligence_level"),
        caption="Due-diligence depth is selected from engine output.",
    )

    _append_event(
        events,
        run_id=run_id,
        event_type=EVENT_HUMAN_REVIEW_REQUIRED,
        node_id="human_review",
        governance_required=run_view_model.get("safety_boundaries", {}).get(
            "governance_required"
        ),
        human_approval_required=run_view_model.get("safety_boundaries", {}).get(
            "human_approval_required"
        ),
        autonomous_action_allowed=run_view_model.get("safety_boundaries", {}).get(
            "autonomous_action_allowed"
        ),
        caption="Replay stops at human review. Autonomous action remains disabled.",
    )

    return _with_event_ids_and_timing(events)


def attach_animation_events(
    run_view_model: dict[str, Any],
) -> dict[str, Any]:
    """Return a copy of the run view-model with deterministic events attached."""

    updated = deepcopy(run_view_model)
    updated["animation_events"] = build_animation_events(updated)
    return updated


def _append_event(
    events: list[dict[str, Any]],
    *,
    run_id: str,
    event_type: str,
    caption: str,
    **values: Any,
) -> None:
    if event_type not in SUPPORTED_EVENT_TYPES:
        raise ValueError(f"Unsupported event type: {event_type}")

    event = {
        "event_type": event_type,
        "run_id": run_id,
        "caption": caption,
    }

    for key, value in values.items():
        if value is not None:
            event[key] = value

    events.append(event)


def _with_event_ids_and_timing(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    enriched = []

    for index, event in enumerate(events, start=1):
        run_id = event["run_id"]
        enriched.append(
            {
                "event_id": f"{run_id}-EVT-{index:03d}",
                "timestamp_offset_ms": (index - 1) * 900,
                **event,
            }
        )

    return enriched


def _governance_rows(run_view_model: dict[str, Any]) -> list[dict[str, Any]]:
    return run_view_model.get("governance_trace_view", {}).get("rows", [])


def _decision(row: dict[str, Any]) -> str:
    return (
        row.get("governance_decision")
        or row.get("access_decision")
        or row.get("decision")
        or "UNKNOWN"
    )


def _agent_node_id(agent_id: str | None) -> str:
    return f"agent::{agent_id or 'unknown'}"


def _gate_node_id(agent_id: str | None, source_id: str | None) -> str:
    return f"gate::{agent_id or 'unknown'}::{source_id or 'unknown'}"


def _gap_node_id(agent_id: str | None, source_id: str | None) -> str:
    return f"gap::{agent_id or 'unknown'}::{source_id or 'unknown'}"


def _source_node_id(source_id: str | None) -> str:
    return f"source::{source_id or 'unknown'}"


def _evidence_node_id(evidence_id: str | None) -> str:
    return f"evidence::{evidence_id or 'unknown'}"
