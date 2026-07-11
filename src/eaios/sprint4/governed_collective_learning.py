"""Sprint 4E governed collective learning event contract.

This module captures operator feedback and decision outcome history as governed
learning events.

It does not update benchmark truth, score benchmarks, execute remediation, or
enable autonomous policy changes.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint4.governed_restoration_observation import (
    build_governed_restoration_observation_snapshot,
)


class FeedbackSignal(str, Enum):
    REQUESTED_MORE_EVIDENCE = "REQUESTED_MORE_EVIDENCE"
    EVIDENCE_CONFLICT_CONFIRMED = "EVIDENCE_CONFLICT_CONFIRMED"
    RISK_REVIEW_REQUIRED = "RISK_REVIEW_REQUIRED"
    RESTORATION_DEFERRED = "RESTORATION_DEFERRED"


class LearningEventType(str, Enum):
    OPERATOR_FEEDBACK_CAPTURED = "OPERATOR_FEEDBACK_CAPTURED"
    DECISION_OUTCOME_RECORDED = "DECISION_OUTCOME_RECORDED"
    RECOMMENDATION_IMPROVEMENT_CANDIDATE = "RECOMMENDATION_IMPROVEMENT_CANDIDATE"


class LearningSafetyState(str, Enum):
    GOVERNED_LEARNING_ALLOWED = "GOVERNED_LEARNING_ALLOWED"
    BLOCKED_FROM_AUTONOMOUS_ACTION = "BLOCKED_FROM_AUTONOMOUS_ACTION"


@dataclass(frozen=True)
class OperatorFeedbackRecord:
    feedback_id: str
    source_snapshot_id: str
    operator_id: str
    feedback_signal: FeedbackSignal
    comment: str
    related_action_ids: tuple[str, ...]
    related_evidence_ids: tuple[str, ...]
    learning_allowed: bool
    can_update_benchmark_truth: bool
    can_score_benchmark: bool
    can_enable_autonomous_remediation: bool
    human_review_required: bool
    provenance: str


@dataclass(frozen=True)
class DecisionOutcomeHistory:
    outcome_history_id: str
    source_decision_validation_id: str
    decision: str
    safe_restoration_state: str
    operator_decision_accepted: bool
    outcome_label: str
    lessons: tuple[str, ...]
    benchmark_truth_updated: bool
    benchmark_score_updated: bool
    autonomous_policy_changed: bool
    human_review_required: bool
    provenance: str


@dataclass(frozen=True)
class GovernedLearningEvent:
    event_id: str
    event_type: LearningEventType
    safety_state: LearningSafetyState
    source_snapshot_id: str
    summary: str
    learning_inputs: tuple[str, ...]
    improvement_candidates: tuple[str, ...]
    blocked_updates: tuple[str, ...]
    requires_human_review: bool
    can_update_benchmark_truth: bool
    can_score_benchmark: bool
    can_enable_autonomous_remediation: bool
    provenance: str


@dataclass(frozen=True)
class GovernedCollectiveLearningSnapshot:
    snapshot_id: str
    source_restoration_snapshot_id: str
    feedback_records: tuple[OperatorFeedbackRecord, ...]
    outcome_history: DecisionOutcomeHistory
    learning_events: tuple[GovernedLearningEvent, ...]
    learning_policy: dict[str, object]
    improvement_candidates: tuple[str, ...]
    blocked_updates: tuple[str, ...]
    human_review_required: bool
    benchmark_truth_update_allowed: bool
    benchmark_scoring_allowed_from_learning: bool
    autonomous_policy_change_allowed: bool
    real_tool_execution_performed: bool
    provenance: str


def build_governed_collective_learning_snapshot() -> GovernedCollectiveLearningSnapshot:
    restoration = build_governed_restoration_observation_snapshot()

    feedback_records = (
        OperatorFeedbackRecord(
            feedback_id="operator-feedback-more-evidence-001",
            source_snapshot_id=restoration.snapshot_id,
            operator_id="operator-demo-001",
            feedback_signal=FeedbackSignal.REQUESTED_MORE_EVIDENCE,
            comment=(
                "Operator requested more evidence because payment knowledge has "
                "conflict/staleness and inventory knowledge is risky/incomplete."
            ),
            related_action_ids=(
                "restore-candidate-payment-validate-evidence",
                "restore-candidate-inventory-validate-topology",
            ),
            related_evidence_ids=(
                "mcp-tool-evidence::mcp-request-read-telemetry-payment",
                "mcp-tool-evidence::mcp-request-search-knowledge-payment",
                "mcp-tool-evidence::mcp-request-read-topology-inventory",
            ),
            learning_allowed=True,
            can_update_benchmark_truth=False,
            can_score_benchmark=False,
            can_enable_autonomous_remediation=False,
            human_review_required=True,
            provenance="governed_collective_learning:operator_feedback",
        ),
        OperatorFeedbackRecord(
            feedback_id="operator-feedback-denied-tool-001",
            source_snapshot_id=restoration.snapshot_id,
            operator_id="operator-demo-001",
            feedback_signal=FeedbackSignal.RESTORATION_DEFERRED,
            comment=(
                "Denied remediation request should remain visible as degraded-mode "
                "evidence and must not be converted into autonomous remediation."
            ),
            related_action_ids=(
                "restore-candidate-cross-cluster-approval-hold",
            ),
            related_evidence_ids=(
                "mcp-tool-evidence::mcp-request-denied-remediation-payment",
            ),
            learning_allowed=True,
            can_update_benchmark_truth=False,
            can_score_benchmark=False,
            can_enable_autonomous_remediation=False,
            human_review_required=True,
            provenance="governed_collective_learning:operator_feedback",
        ),
    )

    outcome_history = DecisionOutcomeHistory(
        outcome_history_id="decision-outcome-history-001",
        source_decision_validation_id=restoration.decision_validation_id,
        decision=restoration.decision_summary["decision"],
        safe_restoration_state=restoration.decision_summary["safe_restoration_state"],
        operator_decision_accepted=bool(restoration.decision_summary["accepted"]),
        outcome_label="MORE_EVIDENCE_REQUESTED_BY_OPERATOR",
        lessons=(
            "Improve evidence completeness before restoration approval.",
            "Surface stale and conflicting payment knowledge more prominently.",
            "Keep denied remediation attempts visible as governance constraints.",
            "Do not convert operator feedback into benchmark truth.",
        ),
        benchmark_truth_updated=False,
        benchmark_score_updated=False,
        autonomous_policy_changed=False,
        human_review_required=True,
        provenance="governed_collective_learning:decision_outcome_history",
    )

    improvement_candidates = (
        "Increase prominence of conflict/staleness warnings in restoration dashboard.",
        "Add service-owner review prompt for risky inventory dependency evidence.",
        "Add degraded-mode explanation when remediation tool requests are denied.",
    )

    blocked_updates = (
        "benchmark_truth_update",
        "benchmark_score_update",
        "autonomous_remediation_policy_change",
        "real_tool_execution",
        "production_knowledge_auto_approval",
    )

    learning_events = (
        GovernedLearningEvent(
            event_id="learning-event-operator-feedback-001",
            event_type=LearningEventType.OPERATOR_FEEDBACK_CAPTURED,
            safety_state=LearningSafetyState.GOVERNED_LEARNING_ALLOWED,
            source_snapshot_id=restoration.snapshot_id,
            summary="Operator feedback captured for more evidence and denied-tool visibility.",
            learning_inputs=tuple(record.feedback_id for record in feedback_records),
            improvement_candidates=improvement_candidates,
            blocked_updates=blocked_updates,
            requires_human_review=True,
            can_update_benchmark_truth=False,
            can_score_benchmark=False,
            can_enable_autonomous_remediation=False,
            provenance="governed_collective_learning:event",
        ),
        GovernedLearningEvent(
            event_id="learning-event-decision-outcome-001",
            event_type=LearningEventType.DECISION_OUTCOME_RECORDED,
            safety_state=LearningSafetyState.GOVERNED_LEARNING_ALLOWED,
            source_snapshot_id=restoration.snapshot_id,
            summary="Operator decision outcome recorded as request for more evidence.",
            learning_inputs=(outcome_history.outcome_history_id,),
            improvement_candidates=improvement_candidates,
            blocked_updates=blocked_updates,
            requires_human_review=True,
            can_update_benchmark_truth=False,
            can_score_benchmark=False,
            can_enable_autonomous_remediation=False,
            provenance="governed_collective_learning:event",
        ),
    )

    return GovernedCollectiveLearningSnapshot(
        snapshot_id="governed-collective-learning::composition-structural-001",
        source_restoration_snapshot_id=restoration.snapshot_id,
        feedback_records=feedback_records,
        outcome_history=outcome_history,
        learning_events=learning_events,
        learning_policy={
            "learning_allowed": True,
            "human_review_required": True,
            "benchmark_truth_update_allowed": False,
            "benchmark_scoring_allowed_from_learning": False,
            "autonomous_policy_change_allowed": False,
            "real_tool_execution_allowed": False,
            "production_knowledge_auto_approval_allowed": False,
        },
        improvement_candidates=improvement_candidates,
        blocked_updates=blocked_updates,
        human_review_required=True,
        benchmark_truth_update_allowed=False,
        benchmark_scoring_allowed_from_learning=False,
        autonomous_policy_change_allowed=False,
        real_tool_execution_performed=False,
        provenance="governed_collective_learning:snapshot",
    )


def summarize_collective_learning_snapshot(
    snapshot: GovernedCollectiveLearningSnapshot,
) -> dict[str, object]:
    return {
        "snapshot_id": snapshot.snapshot_id,
        "source_restoration_snapshot_id": snapshot.source_restoration_snapshot_id,
        "feedback_record_count": len(snapshot.feedback_records),
        "learning_event_count": len(snapshot.learning_events),
        "improvement_candidate_count": len(snapshot.improvement_candidates),
        "blocked_update_count": len(snapshot.blocked_updates),
        "outcome_label": snapshot.outcome_history.outcome_label,
        "safe_restoration_state": snapshot.outcome_history.safe_restoration_state,
        "human_review_required": snapshot.human_review_required,
        "benchmark_truth_update_allowed": snapshot.benchmark_truth_update_allowed,
        "benchmark_scoring_allowed_from_learning": (
            snapshot.benchmark_scoring_allowed_from_learning
        ),
        "autonomous_policy_change_allowed": snapshot.autonomous_policy_change_allowed,
        "real_tool_execution_performed": snapshot.real_tool_execution_performed,
    }


def to_view_model(snapshot: GovernedCollectiveLearningSnapshot) -> dict[str, Any]:
    return {
        "summary": summarize_collective_learning_snapshot(snapshot),
        "feedback_records": [
            {
                "feedback_id": record.feedback_id,
                "source_snapshot_id": record.source_snapshot_id,
                "operator_id": record.operator_id,
                "feedback_signal": record.feedback_signal.value,
                "comment": record.comment,
                "related_action_ids": list(record.related_action_ids),
                "related_evidence_ids": list(record.related_evidence_ids),
                "learning_allowed": record.learning_allowed,
                "can_update_benchmark_truth": record.can_update_benchmark_truth,
                "can_score_benchmark": record.can_score_benchmark,
                "can_enable_autonomous_remediation": (
                    record.can_enable_autonomous_remediation
                ),
                "human_review_required": record.human_review_required,
                "provenance": record.provenance,
            }
            for record in snapshot.feedback_records
        ],
        "outcome_history": {
            "outcome_history_id": snapshot.outcome_history.outcome_history_id,
            "source_decision_validation_id": (
                snapshot.outcome_history.source_decision_validation_id
            ),
            "decision": snapshot.outcome_history.decision,
            "safe_restoration_state": snapshot.outcome_history.safe_restoration_state,
            "operator_decision_accepted": (
                snapshot.outcome_history.operator_decision_accepted
            ),
            "outcome_label": snapshot.outcome_history.outcome_label,
            "lessons": list(snapshot.outcome_history.lessons),
            "benchmark_truth_updated": snapshot.outcome_history.benchmark_truth_updated,
            "benchmark_score_updated": snapshot.outcome_history.benchmark_score_updated,
            "autonomous_policy_changed": snapshot.outcome_history.autonomous_policy_changed,
            "human_review_required": snapshot.outcome_history.human_review_required,
            "provenance": snapshot.outcome_history.provenance,
        },
        "learning_events": [
            {
                "event_id": event.event_id,
                "event_type": event.event_type.value,
                "safety_state": event.safety_state.value,
                "source_snapshot_id": event.source_snapshot_id,
                "summary": event.summary,
                "learning_inputs": list(event.learning_inputs),
                "improvement_candidates": list(event.improvement_candidates),
                "blocked_updates": list(event.blocked_updates),
                "requires_human_review": event.requires_human_review,
                "can_update_benchmark_truth": event.can_update_benchmark_truth,
                "can_score_benchmark": event.can_score_benchmark,
                "can_enable_autonomous_remediation": (
                    event.can_enable_autonomous_remediation
                ),
                "provenance": event.provenance,
            }
            for event in snapshot.learning_events
        ],
        "learning_policy": snapshot.learning_policy,
        "improvement_candidates": list(snapshot.improvement_candidates),
        "blocked_updates": list(snapshot.blocked_updates),
        "human_review_required": snapshot.human_review_required,
        "benchmark_truth_update_allowed": snapshot.benchmark_truth_update_allowed,
        "benchmark_scoring_allowed_from_learning": (
            snapshot.benchmark_scoring_allowed_from_learning
        ),
        "autonomous_policy_change_allowed": snapshot.autonomous_policy_change_allowed,
        "real_tool_execution_performed": snapshot.real_tool_execution_performed,
        "provenance": snapshot.provenance,
    }
