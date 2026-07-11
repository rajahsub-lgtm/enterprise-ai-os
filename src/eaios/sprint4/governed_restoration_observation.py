"""Sprint 4D governed restoration observation snapshot.

This module packages the restoration plan, human approval packet, operator
decision validation, and safe restoration state into one dashboard/export
contract.

It does not execute remediation, call tools, send notifications, or score
benchmarks.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from eaios.sprint4.governed_restoration_approval_packet import (
    build_restoration_approval_packet,
    summarize_approval_packet,
    to_view_model as approval_packet_to_view_model,
)
from eaios.sprint4.governed_restoration_decision import (
    build_default_operator_decision_validation,
    summarize_operator_decision_validation,
    to_view_model as decision_to_view_model,
)
from eaios.sprint4.governed_restoration_orchestration import (
    build_cross_cluster_restoration_plan,
    summarize_restoration_plan,
    to_view_model as restoration_plan_to_view_model,
)


@dataclass(frozen=True)
class GovernedRestorationObservationSnapshot:
    snapshot_id: str
    source_plan_id: str
    source_packet_id: str
    decision_validation_id: str
    restoration_summary: dict[str, object]
    approval_summary: dict[str, object]
    decision_summary: dict[str, object]
    dashboard_sections: tuple[str, ...]
    governance_boundaries: tuple[str, ...]
    action_cards: tuple[dict[str, object], ...]
    blocked_actions: tuple[str, ...]
    restoration_plan_view: dict[str, Any]
    approval_packet_view: dict[str, Any]
    decision_view: dict[str, Any]
    real_tool_execution_performed: bool
    autonomous_remediation_allowed: bool
    benchmark_scoring_allowed_from_restoration: bool
    human_approval_required: bool
    provenance: str


def build_governed_restoration_observation_snapshot() -> GovernedRestorationObservationSnapshot:
    plan = build_cross_cluster_restoration_plan()
    packet = build_restoration_approval_packet(plan)
    decision = build_default_operator_decision_validation()

    return GovernedRestorationObservationSnapshot(
        snapshot_id="governed-restoration-observation::composition-structural-001",
        source_plan_id=plan.plan_id,
        source_packet_id=packet.packet_id,
        decision_validation_id=decision.validation_id,
        restoration_summary=summarize_restoration_plan(plan),
        approval_summary=summarize_approval_packet(packet),
        decision_summary=summarize_operator_decision_validation(decision),
        dashboard_sections=(
            "cross_cluster_restoration_plan",
            "human_approval_packet",
            "operator_decision_record",
            "safe_restoration_state",
            "blocked_actions",
            "governance_boundaries",
        ),
        governance_boundaries=(
            "cross_cluster_restoration_plan_required",
            "human_approval_packet_required",
            "operator_decision_record_required",
            "safe_state_machine_required",
            "manual_execution_only",
            "autonomous_remediation_disabled",
            "real_tool_execution_blocked",
            "benchmark_scoring_from_restoration_blocked",
            "denied_tool_constraints_preserved",
            "service_owner_review_required",
            "rollback_review_required",
            "communications_review_required",
            "human_approval_required",
        ),
        action_cards=tuple(
            {
                "action_id": action.action_id,
                "cluster_id": action.cluster_id,
                "source_failure_case_id": action.source_failure_case_id,
                "action_type": action.action_type.value,
                "title": action.title,
                "risk_level": action.risk_level.value,
                "human_approval_required": action.human_approval_required,
                "can_execute_autonomously": action.can_execute_autonomously,
                "benchmark_scoring_allowed": action.benchmark_scoring_allowed,
            }
            for action in plan.action_candidates
        ),
        blocked_actions=packet.blocked_actions,
        restoration_plan_view=restoration_plan_to_view_model(plan),
        approval_packet_view=approval_packet_to_view_model(packet),
        decision_view=decision_to_view_model(decision),
        real_tool_execution_performed=False,
        autonomous_remediation_allowed=False,
        benchmark_scoring_allowed_from_restoration=False,
        human_approval_required=True,
        provenance="governed_restoration_observation:dashboard_snapshot",
    )


def summarize_restoration_observation(
    snapshot: GovernedRestorationObservationSnapshot,
) -> dict[str, object]:
    return {
        "snapshot_id": snapshot.snapshot_id,
        "source_plan_id": snapshot.source_plan_id,
        "source_packet_id": snapshot.source_packet_id,
        "decision_validation_id": snapshot.decision_validation_id,
        "restoration_plan_state": snapshot.restoration_summary["plan_state"],
        "approval_packet_state": snapshot.approval_summary["packet_state"],
        "safe_restoration_state": snapshot.decision_summary["safe_restoration_state"],
        "action_candidate_count": snapshot.restoration_summary["action_candidate_count"],
        "evidence_reference_count": snapshot.approval_summary["evidence_reference_count"],
        "operator_decision_accepted": snapshot.decision_summary["accepted"],
        "blocked_action_count": len(snapshot.blocked_actions),
        "real_tool_execution_performed": snapshot.real_tool_execution_performed,
        "autonomous_remediation_allowed": snapshot.autonomous_remediation_allowed,
        "benchmark_scoring_allowed_from_restoration": (
            snapshot.benchmark_scoring_allowed_from_restoration
        ),
        "human_approval_required": snapshot.human_approval_required,
    }


def to_view_model(snapshot: GovernedRestorationObservationSnapshot) -> dict[str, Any]:
    return {
        "summary": summarize_restoration_observation(snapshot),
        "dashboard_sections": list(snapshot.dashboard_sections),
        "governance_boundaries": list(snapshot.governance_boundaries),
        "action_cards": list(snapshot.action_cards),
        "blocked_actions": list(snapshot.blocked_actions),
        "restoration_plan": snapshot.restoration_plan_view,
        "approval_packet": snapshot.approval_packet_view,
        "operator_decision": snapshot.decision_view,
        "real_tool_execution_performed": snapshot.real_tool_execution_performed,
        "autonomous_remediation_allowed": snapshot.autonomous_remediation_allowed,
        "benchmark_scoring_allowed_from_restoration": (
            snapshot.benchmark_scoring_allowed_from_restoration
        ),
        "human_approval_required": snapshot.human_approval_required,
        "provenance": snapshot.provenance,
    }
