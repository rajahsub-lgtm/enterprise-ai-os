"""Sprint 4E governed learning dashboard snapshot.

This module packages restoration observation, collective learning, and governed
improvement records into a before/after dashboard contract.

It does not update benchmark truth, score benchmarks, execute remediation, or
apply improvements automatically. All dashboard improvements remain review-only.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint4.governed_collective_learning import (
    build_governed_collective_learning_snapshot,
    summarize_collective_learning_snapshot,
    to_view_model as collective_learning_to_view_model,
)
from eaios.sprint4.governed_learning_improvement import (
    build_governed_learning_improvement_snapshot,
    summarize_learning_improvement_snapshot,
    to_view_model as improvement_to_view_model,
)
from eaios.sprint4.governed_restoration_observation import (
    build_governed_restoration_observation_snapshot,
    summarize_restoration_observation,
    to_view_model as restoration_observation_to_view_model,
)


class DashboardDeltaType(str, Enum):
    VISIBILITY_IMPROVEMENT = "VISIBILITY_IMPROVEMENT"
    REVIEW_PROMPT_IMPROVEMENT = "REVIEW_PROMPT_IMPROVEMENT"
    DEGRADED_MODE_IMPROVEMENT = "DEGRADED_MODE_IMPROVEMENT"


@dataclass(frozen=True)
class GovernedDashboardDelta:
    delta_id: str
    delta_type: DashboardDeltaType
    source_improvement_id: str
    before_state: str
    after_state_candidate: str
    expected_operator_benefit: str
    review_only: bool
    applied_automatically: bool
    human_review_required: bool
    can_update_benchmark_truth: bool
    can_score_benchmark: bool
    can_enable_autonomous_remediation: bool
    can_execute_real_tools: bool
    provenance: str


@dataclass(frozen=True)
class GovernedLearningDashboardSnapshot:
    snapshot_id: str
    source_restoration_snapshot_id: str
    source_learning_snapshot_id: str
    source_improvement_snapshot_id: str
    restoration_summary: dict[str, object]
    learning_summary: dict[str, object]
    improvement_summary: dict[str, object]
    before_dashboard_state: tuple[str, ...]
    after_dashboard_candidates: tuple[str, ...]
    dashboard_deltas: tuple[GovernedDashboardDelta, ...]
    review_queue: tuple[str, ...]
    blocked_updates: tuple[str, ...]
    restoration_view: dict[str, Any]
    learning_view: dict[str, Any]
    improvement_view: dict[str, Any]
    human_review_required: bool
    benchmark_truth_update_allowed: bool
    benchmark_scoring_allowed_from_dashboard: bool
    autonomous_policy_change_allowed: bool
    real_tool_execution_performed: bool
    dashboard_changes_applied: bool
    provenance: str


def build_governed_learning_dashboard_snapshot() -> GovernedLearningDashboardSnapshot:
    restoration = build_governed_restoration_observation_snapshot()
    learning = build_governed_collective_learning_snapshot()
    improvements = build_governed_learning_improvement_snapshot(learning)

    before_state = (
        "Restoration dashboard shows action cards and blocked actions.",
        "Payment conflict and stale evidence are present but not promoted as a dedicated learning improvement.",
        "Inventory risky dependency evidence requires service-owner review but prompt is not yet improved.",
        "Denied remediation request is recorded but degraded-mode explanation can be more explicit.",
    )

    after_candidates = tuple(record.proposed_change for record in improvements.improvement_records)

    deltas = tuple(
        GovernedDashboardDelta(
            delta_id=f"dashboard-delta::{record.improvement_id}",
            delta_type=_delta_type_for_target(record.target.value),
            source_improvement_id=record.improvement_id,
            before_state=_before_state_for_target(record.target.value),
            after_state_candidate=record.proposed_change,
            expected_operator_benefit=record.expected_operator_benefit,
            review_only=True,
            applied_automatically=False,
            human_review_required=True,
            can_update_benchmark_truth=False,
            can_score_benchmark=False,
            can_enable_autonomous_remediation=False,
            can_execute_real_tools=False,
            provenance="governed_learning_dashboard:delta",
        )
        for record in improvements.improvement_records
    )

    return GovernedLearningDashboardSnapshot(
        snapshot_id="governed-learning-dashboard::composition-structural-001",
        source_restoration_snapshot_id=restoration.snapshot_id,
        source_learning_snapshot_id=learning.snapshot_id,
        source_improvement_snapshot_id=improvements.snapshot_id,
        restoration_summary=summarize_restoration_observation(restoration),
        learning_summary=summarize_collective_learning_snapshot(learning),
        improvement_summary=summarize_learning_improvement_snapshot(improvements),
        before_dashboard_state=before_state,
        after_dashboard_candidates=after_candidates,
        dashboard_deltas=deltas,
        review_queue=improvements.review_queue,
        blocked_updates=improvements.blocked_updates,
        restoration_view=restoration_observation_to_view_model(restoration),
        learning_view=collective_learning_to_view_model(learning),
        improvement_view=improvement_to_view_model(improvements),
        human_review_required=True,
        benchmark_truth_update_allowed=False,
        benchmark_scoring_allowed_from_dashboard=False,
        autonomous_policy_change_allowed=False,
        real_tool_execution_performed=False,
        dashboard_changes_applied=False,
        provenance="governed_learning_dashboard:snapshot",
    )


def summarize_learning_dashboard_snapshot(
    snapshot: GovernedLearningDashboardSnapshot,
) -> dict[str, object]:
    return {
        "snapshot_id": snapshot.snapshot_id,
        "source_restoration_snapshot_id": snapshot.source_restoration_snapshot_id,
        "source_learning_snapshot_id": snapshot.source_learning_snapshot_id,
        "source_improvement_snapshot_id": snapshot.source_improvement_snapshot_id,
        "before_state_count": len(snapshot.before_dashboard_state),
        "after_candidate_count": len(snapshot.after_dashboard_candidates),
        "dashboard_delta_count": len(snapshot.dashboard_deltas),
        "review_queue_count": len(snapshot.review_queue),
        "blocked_update_count": len(snapshot.blocked_updates),
        "dashboard_changes_applied": snapshot.dashboard_changes_applied,
        "human_review_required": snapshot.human_review_required,
        "benchmark_truth_update_allowed": snapshot.benchmark_truth_update_allowed,
        "benchmark_scoring_allowed_from_dashboard": (
            snapshot.benchmark_scoring_allowed_from_dashboard
        ),
        "autonomous_policy_change_allowed": snapshot.autonomous_policy_change_allowed,
        "real_tool_execution_performed": snapshot.real_tool_execution_performed,
    }


def to_view_model(snapshot: GovernedLearningDashboardSnapshot) -> dict[str, Any]:
    return {
        "summary": summarize_learning_dashboard_snapshot(snapshot),
        "before_dashboard_state": list(snapshot.before_dashboard_state),
        "after_dashboard_candidates": list(snapshot.after_dashboard_candidates),
        "dashboard_deltas": [
            {
                "delta_id": delta.delta_id,
                "delta_type": delta.delta_type.value,
                "source_improvement_id": delta.source_improvement_id,
                "before_state": delta.before_state,
                "after_state_candidate": delta.after_state_candidate,
                "expected_operator_benefit": delta.expected_operator_benefit,
                "review_only": delta.review_only,
                "applied_automatically": delta.applied_automatically,
                "human_review_required": delta.human_review_required,
                "can_update_benchmark_truth": delta.can_update_benchmark_truth,
                "can_score_benchmark": delta.can_score_benchmark,
                "can_enable_autonomous_remediation": (
                    delta.can_enable_autonomous_remediation
                ),
                "can_execute_real_tools": delta.can_execute_real_tools,
                "provenance": delta.provenance,
            }
            for delta in snapshot.dashboard_deltas
        ],
        "review_queue": list(snapshot.review_queue),
        "blocked_updates": list(snapshot.blocked_updates),
        "restoration": snapshot.restoration_view,
        "learning": snapshot.learning_view,
        "improvements": snapshot.improvement_view,
        "human_review_required": snapshot.human_review_required,
        "benchmark_truth_update_allowed": snapshot.benchmark_truth_update_allowed,
        "benchmark_scoring_allowed_from_dashboard": (
            snapshot.benchmark_scoring_allowed_from_dashboard
        ),
        "autonomous_policy_change_allowed": snapshot.autonomous_policy_change_allowed,
        "real_tool_execution_performed": snapshot.real_tool_execution_performed,
        "dashboard_changes_applied": snapshot.dashboard_changes_applied,
        "provenance": snapshot.provenance,
    }


def _delta_type_for_target(target: str) -> DashboardDeltaType:
    if target == "RESTORATION_DASHBOARD":
        return DashboardDeltaType.VISIBILITY_IMPROVEMENT
    if target == "SERVICE_OWNER_REVIEW_PROMPT":
        return DashboardDeltaType.REVIEW_PROMPT_IMPROVEMENT
    return DashboardDeltaType.DEGRADED_MODE_IMPROVEMENT


def _before_state_for_target(target: str) -> str:
    if target == "RESTORATION_DASHBOARD":
        return "Conflict and stale evidence are available but not highlighted enough."
    if target == "SERVICE_OWNER_REVIEW_PROMPT":
        return "Risky inventory dependency evidence lacks a stronger service-owner prompt."
    return "Denied remediation request is recorded but degraded-mode explanation can be clearer."
