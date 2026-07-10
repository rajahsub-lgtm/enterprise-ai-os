"""
Sprint 3-UI replay view-model composition.

Classification: EAIOS Presentation Layer

This module is intentionally outside the Sprint 3 core boundary.

It composes tested headless engine outputs into renderable dictionaries for the
EAIOS 2 governed orchestration replay UI.

Rules:
- no governance decisions are made here
- no confidence decisions are made here
- no evidence eligibility decisions are made here
- no approval or autonomous-action decisions are made here
- IDs and statuses must come from supplied engine objects
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any


def build_replay_run_view_model(
    *,
    run_id: str,
    scenario_id: str,
    scenario_label: str,
    business_outcome: str,
    joint_goal: str,
    current_alert: dict[str, Any],
    operational_confidence: Any,
    orchestration_trace: Any,
    governance_trace_view: Any,
    governed_evidence_package: Any,
    safety_boundaries: dict[str, Any] | None = None,
    fusion_result: Any | None = None,
    reasoning_explanation: Any | None = None,
    recommendation_candidate: Any | None = None,
    animation_events: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build a renderable replay view-model from engine outputs.

    This function performs presentation composition only.
    """

    confidence = _to_plain(operational_confidence)
    trace = _to_plain(orchestration_trace)
    governance_rows = _governance_rows(governance_trace_view)
    evidence_for_reasoning = _evidence_for_reasoning(governed_evidence_package)
    excluded_evidence = _excluded_evidence(governed_evidence_package)
    evidence_gaps = _evidence_gaps(governed_evidence_package)

    boundaries = safety_boundaries or {
        "governance_required": confidence.get("governance_required"),
        "human_approval_required": confidence.get("human_approval_required"),
        "autonomous_action_allowed": confidence.get("autonomous_action_allowed"),
    }

    view_model = {
        "run_id": run_id,
        "scenario_id": scenario_id,
        "scenario_label": scenario_label,
        "business_outcome": business_outcome,
        "joint_goal": joint_goal,
        "current_alert": _to_plain(current_alert),
        "operational_confidence": confidence.get("operational_confidence"),
        "confidence_direction": confidence.get("confidence_direction"),
        "pattern_maturity": confidence.get("pattern_maturity"),
        "selected_due_diligence_level": confidence.get("selected_due_diligence_level"),
        "why": confidence.get("why", []),
        "orchestration_trace": trace,
        "governance_trace_view": {
            "rows": governance_rows,
        },
        "evidence_for_reasoning": evidence_for_reasoning,
        "excluded_evidence": excluded_evidence,
        "evidence_gaps": evidence_gaps,
        "fusion_result": _to_plain(fusion_result),
        "reasoning_explanation": _to_plain(reasoning_explanation),
        "recommendation_candidate": _to_plain(recommendation_candidate),
        "safety_boundaries": _to_plain(boundaries),
        "animation_events": animation_events or [],
        "provenance": _build_provenance_index(
            confidence=confidence,
            governance_rows=governance_rows,
            evidence_for_reasoning=evidence_for_reasoning,
            excluded_evidence=excluded_evidence,
            evidence_gaps=evidence_gaps,
            safety_boundaries=boundaries,
        ),
    }

    return view_model


def build_comparison_view_model(
    *,
    comparison_id: str,
    comparison_label: str,
    runs: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build a side-by-side replay view-model from run view-models."""

    return {
        "comparison_id": comparison_id,
        "comparison_label": comparison_label,
        "runs": runs,
        "summary": [
            {
                "run_id": run["run_id"],
                "scenario_label": run["scenario_label"],
                "operational_confidence": run["operational_confidence"],
                "selected_due_diligence_level": run["selected_due_diligence_level"],
                "agent_step_count": _agent_step_count(run.get("orchestration_trace", {})),
                "evidence_count": len(run.get("evidence_for_reasoning", [])),
                "excluded_evidence_count": len(run.get("excluded_evidence", [])),
                "evidence_gap_count": len(run.get("evidence_gaps", [])),
                "denied_source_access_count": _denied_source_access_count(
                    run.get("governance_trace_view", {}).get("rows", [])
                ),
                "governance_required": run.get("safety_boundaries", {}).get(
                    "governance_required"
                ),
                "human_approval_required": run.get("safety_boundaries", {}).get(
                    "human_approval_required"
                ),
                "autonomous_action_allowed": run.get("safety_boundaries", {}).get(
                    "autonomous_action_allowed"
                ),
            }
            for run in runs
        ],
    }


def _to_plain(value: Any) -> Any:
    if value is None:
        return None

    if is_dataclass(value):
        return _to_plain(asdict(value))

    if isinstance(value, dict):
        return {key: _to_plain(inner) for key, inner in value.items()}

    if isinstance(value, list):
        return [_to_plain(item) for item in value]

    if isinstance(value, tuple):
        return [_to_plain(item) for item in value]

    if hasattr(value, "to_dict") and callable(value.to_dict):
        return _to_plain(value.to_dict())

    if hasattr(value, "__dict__") and not isinstance(value, type):
        return {
            key: _to_plain(inner)
            for key, inner in vars(value).items()
            if not key.startswith("_")
        }

    return value


def _governance_rows(governance_trace_view: Any) -> list[dict[str, Any]]:
    plain = _to_plain(governance_trace_view)

    if plain is None:
        return []

    if isinstance(plain, list):
        return plain

    if isinstance(plain, dict):
        if isinstance(plain.get("rows"), list):
            return plain["rows"]

        if isinstance(plain.get("trace_rows"), list):
            return plain["trace_rows"]

        if isinstance(plain.get("governance_trace"), list):
            return plain["governance_trace"]

    return []


def _evidence_for_reasoning(package: Any) -> list[dict[str, Any]]:
    if package is None:
        return []

    if hasattr(package, "evidence_for_reasoning") and callable(
        package.evidence_for_reasoning
    ):
        return _to_plain(package.evidence_for_reasoning())

    plain = _to_plain(package)

    if isinstance(plain, dict):
        for key in ["evidence_for_reasoning", "reasoning_evidence"]:
            value = plain.get(key)
            if isinstance(value, list):
                return value

        evidence_items = plain.get("evidence_items")
        if isinstance(evidence_items, list):
            return [
                item
                for item in evidence_items
                if item.get("allowed_for_reasoning") is True
            ]

    return []


def _excluded_evidence(package: Any) -> list[dict[str, Any]]:
    if package is None:
        return []

    if hasattr(package, "excluded_evidence") and callable(package.excluded_evidence):
        return _to_plain(package.excluded_evidence())

    plain = _to_plain(package)

    if isinstance(plain, dict):
        value = plain.get("excluded_evidence")
        if isinstance(value, list):
            return value

        evidence_items = plain.get("evidence_items")
        if isinstance(evidence_items, list):
            return [
                item
                for item in evidence_items
                if item.get("allowed_for_reasoning") is False
            ]

    return []


def _evidence_gaps(package: Any) -> list[dict[str, Any]]:
    plain = _to_plain(package)

    if isinstance(plain, dict):
        value = plain.get("evidence_gaps")
        if isinstance(value, list):
            return value

    return []


def _build_provenance_index(
    *,
    confidence: dict[str, Any],
    governance_rows: list[dict[str, Any]],
    evidence_for_reasoning: list[dict[str, Any]],
    excluded_evidence: list[dict[str, Any]],
    evidence_gaps: list[dict[str, Any]],
    safety_boundaries: dict[str, Any],
) -> dict[str, Any]:
    evidence_items = evidence_for_reasoning + excluded_evidence

    return {
        "audit_ids": sorted(
            _non_empty_values(governance_rows + evidence_gaps, "audit_id")
        ),
        "evidence_ids": sorted(_non_empty_values(evidence_items, "evidence_id")),
        "governance_decisions": sorted(
            _non_empty_values(governance_rows, "governance_decision")
            | _non_empty_values(governance_rows, "access_decision")
            | _non_empty_values(governance_rows, "decision")
        ),
        "content_safety_statuses": sorted(
            _non_empty_values(governance_rows + evidence_items, "content_safety_status")
        ),
        "allowed_for_reasoning_values": sorted(
            {
                row["allowed_for_reasoning"]
                for row in governance_rows + evidence_items
                if "allowed_for_reasoning" in row
            },
            key=str,
        ),
        "approval_states": sorted(_non_empty_values(governance_rows, "approval_state")),
        "confidence_values": {
            "operational_confidence": confidence.get("operational_confidence"),
            "confidence_direction": confidence.get("confidence_direction"),
            "pattern_maturity": confidence.get("pattern_maturity"),
            "selected_due_diligence_level": confidence.get(
                "selected_due_diligence_level"
            ),
        },
        "safety_boundaries": {
            "governance_required": safety_boundaries.get("governance_required"),
            "human_approval_required": safety_boundaries.get("human_approval_required"),
            "autonomous_action_allowed": safety_boundaries.get(
                "autonomous_action_allowed"
            ),
        },
    }


def _non_empty_values(rows: list[dict[str, Any]], key: str) -> set[Any]:
    return {
        row[key]
        for row in rows
        if isinstance(row, dict) and row.get(key) not in [None, ""]
    }


def _agent_step_count(orchestration_trace: dict[str, Any]) -> int:
    for key in ["agent_steps", "steps", "trace"]:
        value = orchestration_trace.get(key)
        if isinstance(value, list):
            return len(value)

    return 0


def _denied_source_access_count(governance_rows: list[dict[str, Any]]) -> int:
    denied = 0

    for row in governance_rows:
        decision = (
            row.get("governance_decision")
            or row.get("access_decision")
            or row.get("decision")
        )

        if decision == "DENY":
            denied += 1

    return denied
