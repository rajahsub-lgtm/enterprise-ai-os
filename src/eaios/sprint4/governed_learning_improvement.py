"""Sprint 4E governed learning improvement records.

This module converts governed collective learning events into recommendation
improvement records.

It does not update benchmark truth, score benchmarks, execute remediation, or
change autonomous policy. All improvements remain review-only candidates.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint4.governed_collective_learning import (
    GovernedCollectiveLearningSnapshot,
    build_governed_collective_learning_snapshot,
)


class ImprovementTarget(str, Enum):
    RESTORATION_DASHBOARD = "RESTORATION_DASHBOARD"
    SERVICE_OWNER_REVIEW_PROMPT = "SERVICE_OWNER_REVIEW_PROMPT"
    DEGRADED_MODE_EXPLANATION = "DEGRADED_MODE_EXPLANATION"


class ImprovementDisposition(str, Enum):
    REVIEW_ONLY_CANDIDATE = "REVIEW_ONLY_CANDIDATE"
    BLOCKED_UNSAFE_UPDATE = "BLOCKED_UNSAFE_UPDATE"


@dataclass(frozen=True)
class RecommendationImprovementRecord:
    improvement_id: str
    target: ImprovementTarget
    disposition: ImprovementDisposition
    title: str
    source_learning_event_ids: tuple[str, ...]
    source_feedback_ids: tuple[str, ...]
    proposed_change: str
    expected_operator_benefit: str
    safety_constraints: tuple[str, ...]
    blocked_updates: tuple[str, ...]
    requires_human_review: bool
    can_update_benchmark_truth: bool
    can_score_benchmark: bool
    can_enable_autonomous_remediation: bool
    can_execute_real_tools: bool
    provenance: str


@dataclass(frozen=True)
class GovernedLearningImprovementSnapshot:
    snapshot_id: str
    source_learning_snapshot_id: str
    improvement_records: tuple[RecommendationImprovementRecord, ...]
    review_queue: tuple[str, ...]
    blocked_updates: tuple[str, ...]
    learning_policy: dict[str, object]
    human_review_required: bool
    benchmark_truth_update_allowed: bool
    benchmark_scoring_allowed_from_improvements: bool
    autonomous_policy_change_allowed: bool
    real_tool_execution_performed: bool
    provenance: str


def build_governed_learning_improvement_snapshot(
    learning_snapshot: GovernedCollectiveLearningSnapshot | None = None,
) -> GovernedLearningImprovementSnapshot:
    if learning_snapshot is None:
        learning_snapshot = build_governed_collective_learning_snapshot()

    learning_event_ids = tuple(event.event_id for event in learning_snapshot.learning_events)
    feedback_ids = tuple(record.feedback_id for record in learning_snapshot.feedback_records)

    records = (
        RecommendationImprovementRecord(
            improvement_id="improvement-dashboard-conflict-staleness-001",
            target=ImprovementTarget.RESTORATION_DASHBOARD,
            disposition=ImprovementDisposition.REVIEW_ONLY_CANDIDATE,
            title="Increase conflict and staleness visibility in restoration dashboard",
            source_learning_event_ids=learning_event_ids,
            source_feedback_ids=feedback_ids,
            proposed_change=(
                "Promote payment conflict and stale-knowledge warnings into a "
                "dedicated dashboard section before restoration approval."
            ),
            expected_operator_benefit=(
                "Operators can see why more evidence was requested before manual action."
            ),
            safety_constraints=_safety_constraints(),
            blocked_updates=learning_snapshot.blocked_updates,
            requires_human_review=True,
            can_update_benchmark_truth=False,
            can_score_benchmark=False,
            can_enable_autonomous_remediation=False,
            can_execute_real_tools=False,
            provenance="governed_learning_improvement:dashboard_candidate",
        ),
        RecommendationImprovementRecord(
            improvement_id="improvement-service-owner-risk-prompt-001",
            target=ImprovementTarget.SERVICE_OWNER_REVIEW_PROMPT,
            disposition=ImprovementDisposition.REVIEW_ONLY_CANDIDATE,
            title="Add service-owner prompt for risky inventory dependency evidence",
            source_learning_event_ids=learning_event_ids,
            source_feedback_ids=feedback_ids,
            proposed_change=(
                "Add a required service-owner review prompt when inventory evidence "
                "is risky, incomplete, or dependency-impacting."
            ),
            expected_operator_benefit=(
                "Operators are guided to confirm ownership and dependency impact "
                "before preparing restoration."
            ),
            safety_constraints=_safety_constraints(),
            blocked_updates=learning_snapshot.blocked_updates,
            requires_human_review=True,
            can_update_benchmark_truth=False,
            can_score_benchmark=False,
            can_enable_autonomous_remediation=False,
            can_execute_real_tools=False,
            provenance="governed_learning_improvement:service_owner_candidate",
        ),
        RecommendationImprovementRecord(
            improvement_id="improvement-denied-tool-degraded-mode-001",
            target=ImprovementTarget.DEGRADED_MODE_EXPLANATION,
            disposition=ImprovementDisposition.REVIEW_ONLY_CANDIDATE,
            title="Explain denied remediation requests as degraded-mode evidence",
            source_learning_event_ids=learning_event_ids,
            source_feedback_ids=feedback_ids,
            proposed_change=(
                "Add degraded-mode explanation whenever a remediation tool request "
                "is denied by governance policy."
            ),
            expected_operator_benefit=(
                "Operators can distinguish blocked remediation from missing evidence "
                "and avoid assuming the action was attempted."
            ),
            safety_constraints=_safety_constraints(),
            blocked_updates=learning_snapshot.blocked_updates,
            requires_human_review=True,
            can_update_benchmark_truth=False,
            can_score_benchmark=False,
            can_enable_autonomous_remediation=False,
            can_execute_real_tools=False,
            provenance="governed_learning_improvement:degraded_mode_candidate",
        ),
    )

    return GovernedLearningImprovementSnapshot(
        snapshot_id="governed-learning-improvement::composition-structural-001",
        source_learning_snapshot_id=learning_snapshot.snapshot_id,
        improvement_records=records,
        review_queue=tuple(record.improvement_id for record in records),
        blocked_updates=learning_snapshot.blocked_updates,
        learning_policy=learning_snapshot.learning_policy,
        human_review_required=True,
        benchmark_truth_update_allowed=False,
        benchmark_scoring_allowed_from_improvements=False,
        autonomous_policy_change_allowed=False,
        real_tool_execution_performed=False,
        provenance="governed_learning_improvement:snapshot",
    )


def summarize_learning_improvement_snapshot(
    snapshot: GovernedLearningImprovementSnapshot,
) -> dict[str, object]:
    return {
        "snapshot_id": snapshot.snapshot_id,
        "source_learning_snapshot_id": snapshot.source_learning_snapshot_id,
        "improvement_record_count": len(snapshot.improvement_records),
        "review_queue_count": len(snapshot.review_queue),
        "blocked_update_count": len(snapshot.blocked_updates),
        "targets": tuple(record.target.value for record in snapshot.improvement_records),
        "dispositions": tuple(
            record.disposition.value for record in snapshot.improvement_records
        ),
        "human_review_required": snapshot.human_review_required,
        "benchmark_truth_update_allowed": snapshot.benchmark_truth_update_allowed,
        "benchmark_scoring_allowed_from_improvements": (
            snapshot.benchmark_scoring_allowed_from_improvements
        ),
        "autonomous_policy_change_allowed": snapshot.autonomous_policy_change_allowed,
        "real_tool_execution_performed": snapshot.real_tool_execution_performed,
    }


def to_view_model(snapshot: GovernedLearningImprovementSnapshot) -> dict[str, Any]:
    return {
        "summary": summarize_learning_improvement_snapshot(snapshot),
        "improvement_records": [
            {
                "improvement_id": record.improvement_id,
                "target": record.target.value,
                "disposition": record.disposition.value,
                "title": record.title,
                "source_learning_event_ids": list(record.source_learning_event_ids),
                "source_feedback_ids": list(record.source_feedback_ids),
                "proposed_change": record.proposed_change,
                "expected_operator_benefit": record.expected_operator_benefit,
                "safety_constraints": list(record.safety_constraints),
                "blocked_updates": list(record.blocked_updates),
                "requires_human_review": record.requires_human_review,
                "can_update_benchmark_truth": record.can_update_benchmark_truth,
                "can_score_benchmark": record.can_score_benchmark,
                "can_enable_autonomous_remediation": (
                    record.can_enable_autonomous_remediation
                ),
                "can_execute_real_tools": record.can_execute_real_tools,
                "provenance": record.provenance,
            }
            for record in snapshot.improvement_records
        ],
        "review_queue": list(snapshot.review_queue),
        "blocked_updates": list(snapshot.blocked_updates),
        "learning_policy": snapshot.learning_policy,
        "human_review_required": snapshot.human_review_required,
        "benchmark_truth_update_allowed": snapshot.benchmark_truth_update_allowed,
        "benchmark_scoring_allowed_from_improvements": (
            snapshot.benchmark_scoring_allowed_from_improvements
        ),
        "autonomous_policy_change_allowed": snapshot.autonomous_policy_change_allowed,
        "real_tool_execution_performed": snapshot.real_tool_execution_performed,
        "provenance": snapshot.provenance,
    }


def _safety_constraints() -> tuple[str, ...]:
    return (
        "review_only_candidate",
        "human_review_required",
        "must_not_update_benchmark_truth",
        "must_not_score_benchmark",
        "must_not_enable_autonomous_remediation",
        "must_not_execute_real_tools",
    )
