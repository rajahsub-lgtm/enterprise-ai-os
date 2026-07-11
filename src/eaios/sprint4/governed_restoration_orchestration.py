"""Sprint 4D governed restoration orchestration.

This module creates a cross-cluster restoration orchestration plan.

It does not execute remediation. It packages candidate restoration steps,
risk controls, rollback notes, and human approval requirements across multiple
application-health issue clusters.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint4.governed_mcp_observation import (
    build_governed_mcp_observation_snapshot,
)
from eaios.sprint4.governed_reasoning_observation import (
    build_governed_reasoning_observation_snapshot,
)


class RestorationActionType(str, Enum):
    INVESTIGATE = "INVESTIGATE"
    VALIDATE_EVIDENCE = "VALIDATE_EVIDENCE"
    PREPARE_CHANGE = "PREPARE_CHANGE"
    PREPARE_COMMUNICATION = "PREPARE_COMMUNICATION"
    HOLD_FOR_APPROVAL = "HOLD_FOR_APPROVAL"


class RestorationRiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class RestorationPlanState(str, Enum):
    DRAFT_FOR_HUMAN_REVIEW = "DRAFT_FOR_HUMAN_REVIEW"
    BLOCKED_PENDING_APPROVAL = "BLOCKED_PENDING_APPROVAL"


@dataclass(frozen=True)
class RestorationActionCandidate:
    action_id: str
    cluster_id: str
    source_failure_case_id: str
    action_type: RestorationActionType
    title: str
    rationale: str
    required_evidence_ids: tuple[str, ...]
    risk_level: RestorationRiskLevel
    rollback_note: str
    operator_question: str
    can_execute_autonomously: bool
    human_approval_required: bool
    benchmark_scoring_allowed: bool
    provenance: str


@dataclass(frozen=True)
class CrossClusterRestorationPlan:
    plan_id: str
    source_reasoning_snapshot_id: str
    source_mcp_snapshot_id: str
    plan_state: RestorationPlanState
    cluster_count: int
    action_candidates: tuple[RestorationActionCandidate, ...]
    shared_risks: tuple[str, ...]
    rollback_notes: tuple[str, ...]
    operator_decision_questions: tuple[str, ...]
    denied_tool_constraints: tuple[str, ...]
    approval_packet_required: bool
    autonomous_remediation_allowed: bool
    real_tool_execution_performed: bool
    benchmark_scoring_allowed_from_restoration: bool
    human_approval_required: bool
    provenance: str


def build_cross_cluster_restoration_plan() -> CrossClusterRestorationPlan:
    reasoning = build_governed_reasoning_observation_snapshot()
    mcp = build_governed_mcp_observation_snapshot()

    actions = (
        RestorationActionCandidate(
            action_id="restore-candidate-payment-validate-evidence",
            cluster_id="cluster::structural-failure-payment-latency-001",
            source_failure_case_id="structural-failure-payment-latency-001",
            action_type=RestorationActionType.VALIDATE_EVIDENCE,
            title="Validate payment latency evidence before remediation planning",
            rationale=(
                "Payment cluster has matching benchmark observation, governed "
                "knowledge support, stale evidence, and conflicting evidence. "
                "Operator should validate current telemetry and knowledge conflicts."
            ),
            required_evidence_ids=(
                "mcp-tool-evidence::mcp-request-read-telemetry-payment",
                "mcp-tool-evidence::mcp-request-search-knowledge-payment",
            ),
            risk_level=RestorationRiskLevel.MEDIUM,
            rollback_note="No system change prepared until conflicting evidence is resolved.",
            operator_question=(
                "Does current telemetry confirm payment latency is still active "
                "and aligned to the suspected service?"
            ),
            can_execute_autonomously=False,
            human_approval_required=True,
            benchmark_scoring_allowed=False,
            provenance="governed_restoration_orchestration:payment_validation",
        ),
        RestorationActionCandidate(
            action_id="restore-candidate-inventory-validate-topology",
            cluster_id="cluster::structural-failure-inventory-errors-001",
            source_failure_case_id="structural-failure-inventory-errors-001",
            action_type=RestorationActionType.INVESTIGATE,
            title="Validate inventory dependency impact before restoration package",
            rationale=(
                "Inventory cluster has risky and incomplete knowledge. Topology "
                "evidence should be reviewed before drafting any restoration steps."
            ),
            required_evidence_ids=(
                "mcp-tool-evidence::mcp-request-read-topology-inventory",
            ),
            risk_level=RestorationRiskLevel.HIGH,
            rollback_note="Avoid database or service changes until dependency impact is reviewed.",
            operator_question=(
                "Is route-planning impact caused by inventory dependency failure "
                "or by a downstream consumer issue?"
            ),
            can_execute_autonomously=False,
            human_approval_required=True,
            benchmark_scoring_allowed=False,
            provenance="governed_restoration_orchestration:inventory_investigation",
        ),
        RestorationActionCandidate(
            action_id="restore-candidate-cross-cluster-approval-hold",
            cluster_id="cross-cluster",
            source_failure_case_id="composition-structural-001",
            action_type=RestorationActionType.HOLD_FOR_APPROVAL,
            title="Hold restoration for human approval packet",
            rationale=(
                "Sprint 4D starts cross-cluster coordination, but remediation "
                "must remain blocked until an operator approves the package."
            ),
            required_evidence_ids=(
                "mcp-tool-evidence::mcp-request-denied-remediation-payment",
            ),
            risk_level=RestorationRiskLevel.HIGH,
            rollback_note="No rollback required because no action has been executed.",
            operator_question=(
                "Should the operator approve a restoration package after reviewing "
                "evidence, risks, and rollback notes?"
            ),
            can_execute_autonomously=False,
            human_approval_required=True,
            benchmark_scoring_allowed=False,
            provenance="governed_restoration_orchestration:approval_hold",
        ),
    )

    return CrossClusterRestorationPlan(
        plan_id="sprint4d-cross-cluster-restoration-plan-001",
        source_reasoning_snapshot_id=reasoning.snapshot_id,
        source_mcp_snapshot_id=mcp.snapshot_id,
        plan_state=RestorationPlanState.BLOCKED_PENDING_APPROVAL,
        cluster_count=reasoning.cluster_count,
        action_candidates=actions,
        shared_risks=(
            "Payment evidence contains stale and conflicting knowledge.",
            "Inventory evidence contains risky and incomplete knowledge.",
            "A remediation request was denied and must be represented as degraded-mode evidence.",
            "Cross-cluster restoration may create unintended downstream impact.",
        ),
        rollback_notes=(
            "No production action has been executed by this plan.",
            "Any future restoration package must include explicit backout criteria.",
            "Operator must verify service owner approval before action.",
        ),
        operator_decision_questions=tuple(action.operator_question for action in actions),
        denied_tool_constraints=tuple(
            f"{record['tool_id']}::{record['operation']}::{record['denied_reason_summary']}"
            for record in mcp.denied_tool_records
        ),
        approval_packet_required=True,
        autonomous_remediation_allowed=False,
        real_tool_execution_performed=False,
        benchmark_scoring_allowed_from_restoration=False,
        human_approval_required=True,
        provenance="governed_restoration_orchestration:cross_cluster_plan",
    )


def summarize_restoration_plan(plan: CrossClusterRestorationPlan) -> dict[str, object]:
    return {
        "plan_id": plan.plan_id,
        "source_reasoning_snapshot_id": plan.source_reasoning_snapshot_id,
        "source_mcp_snapshot_id": plan.source_mcp_snapshot_id,
        "plan_state": plan.plan_state.value,
        "cluster_count": plan.cluster_count,
        "action_candidate_count": len(plan.action_candidates),
        "shared_risk_count": len(plan.shared_risks),
        "rollback_note_count": len(plan.rollback_notes),
        "operator_question_count": len(plan.operator_decision_questions),
        "denied_tool_constraint_count": len(plan.denied_tool_constraints),
        "approval_packet_required": plan.approval_packet_required,
        "autonomous_remediation_allowed": plan.autonomous_remediation_allowed,
        "real_tool_execution_performed": plan.real_tool_execution_performed,
        "benchmark_scoring_allowed_from_restoration": (
            plan.benchmark_scoring_allowed_from_restoration
        ),
        "human_approval_required": plan.human_approval_required,
    }


def to_view_model(plan: CrossClusterRestorationPlan) -> dict[str, Any]:
    return {
        "summary": summarize_restoration_plan(plan),
        "actions": [
            {
                "action_id": action.action_id,
                "cluster_id": action.cluster_id,
                "source_failure_case_id": action.source_failure_case_id,
                "action_type": action.action_type.value,
                "title": action.title,
                "rationale": action.rationale,
                "required_evidence_ids": list(action.required_evidence_ids),
                "risk_level": action.risk_level.value,
                "rollback_note": action.rollback_note,
                "operator_question": action.operator_question,
                "can_execute_autonomously": action.can_execute_autonomously,
                "human_approval_required": action.human_approval_required,
                "benchmark_scoring_allowed": action.benchmark_scoring_allowed,
                "provenance": action.provenance,
            }
            for action in plan.action_candidates
        ],
        "shared_risks": list(plan.shared_risks),
        "rollback_notes": list(plan.rollback_notes),
        "operator_decision_questions": list(plan.operator_decision_questions),
        "denied_tool_constraints": list(plan.denied_tool_constraints),
        "approval_packet_required": plan.approval_packet_required,
        "autonomous_remediation_allowed": plan.autonomous_remediation_allowed,
        "real_tool_execution_performed": plan.real_tool_execution_performed,
        "benchmark_scoring_allowed_from_restoration": (
            plan.benchmark_scoring_allowed_from_restoration
        ),
        "human_approval_required": plan.human_approval_required,
        "provenance": plan.provenance,
    }
