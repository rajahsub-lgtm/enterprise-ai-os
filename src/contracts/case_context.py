"""
Case context contract.

Classification: EAIOS Core

This module defines phase names and required field groups for incremental
case-context assembly.

It is domain-neutral. Domain adapters may populate the context, but core
validation must not depend on domain vocabulary.
"""

from __future__ import annotations

from enum import StrEnum


class CaseContextPhase(StrEnum):
    INITIAL_SIGNAL = "INITIAL_SIGNAL"
    PARTIAL_CONTEXT = "PARTIAL_CONTEXT"
    GOVERNED_EVIDENCE_COLLECTED = "GOVERNED_EVIDENCE_COLLECTED"
    FUSION_READY = "FUSION_READY"
    REASONING_READY = "REASONING_READY"
    RECOMMENDATION_READY = "RECOMMENDATION_READY"
    HUMAN_REVIEW_READY = "HUMAN_REVIEW_READY"


CORE_FIELDS = {
    "case_id",
    "business_outcome",
    "goal_category",
}

INITIAL_SIGNAL_FIELDS = CORE_FIELDS | {
    "initial_signal",
}

PARTIAL_CONTEXT_FIELDS = CORE_FIELDS | {
    "joint_goal",
    "initial_signal",
}

GOVERNED_EVIDENCE_FIELDS = CORE_FIELDS | {
    "governed_evidence_package",
}

FUSION_READY_FIELDS = GOVERNED_EVIDENCE_FIELDS | {
    "case_phase",
}

REASONING_READY_FIELDS = FUSION_READY_FIELDS | {
    "evidence_fusion",
}

RECOMMENDATION_READY_FIELDS = REASONING_READY_FIELDS | {
    "reasoning_explanation",
}

HUMAN_REVIEW_READY_FIELDS = RECOMMENDATION_READY_FIELDS | {
    "recommendation_candidate",
    "human_approval_required",
    "autonomous_action_allowed",
}


PHASE_REQUIRED_FIELDS = {
    CaseContextPhase.INITIAL_SIGNAL: INITIAL_SIGNAL_FIELDS,
    CaseContextPhase.PARTIAL_CONTEXT: PARTIAL_CONTEXT_FIELDS,
    CaseContextPhase.GOVERNED_EVIDENCE_COLLECTED: GOVERNED_EVIDENCE_FIELDS,
    CaseContextPhase.FUSION_READY: FUSION_READY_FIELDS,
    CaseContextPhase.REASONING_READY: REASONING_READY_FIELDS,
    CaseContextPhase.RECOMMENDATION_READY: RECOMMENDATION_READY_FIELDS,
    CaseContextPhase.HUMAN_REVIEW_READY: HUMAN_REVIEW_READY_FIELDS,
}


def phase_value(phase: CaseContextPhase | str) -> str:
    if isinstance(phase, CaseContextPhase):
        return phase.value

    return phase
