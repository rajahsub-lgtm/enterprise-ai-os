"""Sprint 4B governed knowledge reasoning contract.

Classification: governed uncertain reasoning layer.

This module converts governed KB evidence bundles into a reasoning-safe output
contract. It intentionally does not call a real LLM provider yet.

Purpose of this slice:
- define the output schema a real LLM must obey later
- preserve uncertainty, conflicts, staleness, gaps, and risky remediation
- keep benchmark scoring independent from KB/LLM reasoning
- keep human approval required
- keep autonomous action disabled
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint4.cluster_knowledge_evidence import (
    ClusterKnowledgeEvidenceBundle,
    ClusterKnowledgeEvidenceResult,
    build_cluster_knowledge_evidence,
)
from eaios.sprint4.governed_knowledge_base import (
    GovernedKnowledgeEvidence,
    KnowledgeQuality,
    KnowledgeSafety,
)


class ReasoningState(str, Enum):
    SUPPORTED = "SUPPORTED"
    SUPPORTED_WITH_CONFLICTS = "SUPPORTED_WITH_CONFLICTS"
    STALE_OR_INCOMPLETE = "STALE_OR_INCOMPLETE"
    RISKY_OR_INCOMPLETE = "RISKY_OR_INCOMPLETE"
    MISSING_KNOWLEDGE = "MISSING_KNOWLEDGE"


class ReasoningConfidence(str, Enum):
    HIGH_WITH_REVIEW = "HIGH_WITH_REVIEW"
    MEDIUM_WITH_REVIEW = "MEDIUM_WITH_REVIEW"
    LOW_WITH_REVIEW = "LOW_WITH_REVIEW"


@dataclass(frozen=True)
class EvidenceReasoningSignal:
    evidence_id: str
    article_id: str | None
    service: str
    indicator: str
    quality: str
    safety: str
    evidence_weight: float
    contribution: str
    limitation: str


@dataclass(frozen=True)
class ClusterKnowledgeReasoning:
    cluster_id: str
    source_failure_case_id: str
    reasoning_state: ReasoningState
    confidence: ReasoningConfidence
    evidence_signals: tuple[EvidenceReasoningSignal, ...]
    supported_observations: tuple[str, ...]
    conflict_warnings: tuple[str, ...]
    stale_warnings: tuple[str, ...]
    knowledge_gaps: tuple[str, ...]
    risky_action_warnings: tuple[str, ...]
    human_review_questions: tuple[str, ...]
    benchmark_truth_claim_allowed: bool
    benchmark_scoring_allowed: bool
    human_approval_required: bool
    autonomous_action_allowed: bool
    provenance: str


@dataclass(frozen=True)
class GovernedKnowledgeReasoningResult:
    cluster_reasoning: tuple[ClusterKnowledgeReasoning, ...]
    reasoning_contract: tuple[str, ...]
    total_clusters: int
    clusters_with_conflicts: tuple[str, ...]
    clusters_with_stale_evidence: tuple[str, ...]
    clusters_with_knowledge_gaps: tuple[str, ...]
    clusters_with_risky_evidence: tuple[str, ...]
    human_approval_required: bool
    benchmark_scoring_allowed: bool
    autonomous_action_allowed: bool
    provenance: str


def build_governed_knowledge_reasoning(
    evidence_result: ClusterKnowledgeEvidenceResult | None = None,
) -> GovernedKnowledgeReasoningResult:
    if evidence_result is None:
        evidence_result = build_cluster_knowledge_evidence()

    cluster_reasoning = tuple(
        _reason_over_bundle(bundle)
        for bundle in evidence_result.bundles
    )

    return GovernedKnowledgeReasoningResult(
        cluster_reasoning=cluster_reasoning,
        reasoning_contract=(
            "llm_output_must_be_schema_valid",
            "llm_output_must_cite_governed_evidence",
            "llm_output_must_preserve_uncertainty",
            "llm_output_must_not_define_benchmark_truth",
            "llm_output_must_not_score_benchmark_results",
            "llm_output_must_require_human_approval_for_actions",
            "llm_output_must_not_enable_autonomous_action",
        ),
        total_clusters=len(cluster_reasoning),
        clusters_with_conflicts=tuple(
            reasoning.cluster_id
            for reasoning in cluster_reasoning
            if reasoning.conflict_warnings
        ),
        clusters_with_stale_evidence=tuple(
            reasoning.cluster_id
            for reasoning in cluster_reasoning
            if reasoning.stale_warnings
        ),
        clusters_with_knowledge_gaps=tuple(
            reasoning.cluster_id
            for reasoning in cluster_reasoning
            if reasoning.knowledge_gaps
        ),
        clusters_with_risky_evidence=tuple(
            reasoning.cluster_id
            for reasoning in cluster_reasoning
            if reasoning.risky_action_warnings
        ),
        human_approval_required=True,
        benchmark_scoring_allowed=False,
        autonomous_action_allowed=False,
        provenance="synthetic_kb:governed_knowledge_reasoning_contract",
    )


def summarize_governed_knowledge_reasoning(
    result: GovernedKnowledgeReasoningResult,
) -> dict[str, object]:
    return {
        "total_clusters": result.total_clusters,
        "reasoning_states": tuple(
            reasoning.reasoning_state.value
            for reasoning in result.cluster_reasoning
        ),
        "clusters_with_conflicts": result.clusters_with_conflicts,
        "clusters_with_stale_evidence": result.clusters_with_stale_evidence,
        "clusters_with_knowledge_gaps": result.clusters_with_knowledge_gaps,
        "clusters_with_risky_evidence": result.clusters_with_risky_evidence,
        "human_approval_required": result.human_approval_required,
        "benchmark_scoring_allowed": result.benchmark_scoring_allowed,
        "autonomous_action_allowed": result.autonomous_action_allowed,
    }


def to_view_model(
    result: GovernedKnowledgeReasoningResult,
) -> dict[str, Any]:
    return {
        "summary": summarize_governed_knowledge_reasoning(result),
        "reasoning_contract": list(result.reasoning_contract),
        "cluster_reasoning": [
            {
                "cluster_id": reasoning.cluster_id,
                "source_failure_case_id": reasoning.source_failure_case_id,
                "reasoning_state": reasoning.reasoning_state.value,
                "confidence": reasoning.confidence.value,
                "supported_observations": list(reasoning.supported_observations),
                "conflict_warnings": list(reasoning.conflict_warnings),
                "stale_warnings": list(reasoning.stale_warnings),
                "knowledge_gaps": list(reasoning.knowledge_gaps),
                "risky_action_warnings": list(reasoning.risky_action_warnings),
                "human_review_questions": list(reasoning.human_review_questions),
                "benchmark_truth_claim_allowed": (
                    reasoning.benchmark_truth_claim_allowed
                ),
                "benchmark_scoring_allowed": reasoning.benchmark_scoring_allowed,
                "human_approval_required": reasoning.human_approval_required,
                "autonomous_action_allowed": reasoning.autonomous_action_allowed,
                "evidence_signals": [
                    {
                        "evidence_id": signal.evidence_id,
                        "article_id": signal.article_id,
                        "service": signal.service,
                        "indicator": signal.indicator,
                        "quality": signal.quality,
                        "safety": signal.safety,
                        "evidence_weight": signal.evidence_weight,
                        "contribution": signal.contribution,
                        "limitation": signal.limitation,
                    }
                    for signal in reasoning.evidence_signals
                ],
                "provenance": reasoning.provenance,
            }
            for reasoning in result.cluster_reasoning
        ],
        "human_approval_required": result.human_approval_required,
        "benchmark_scoring_allowed": result.benchmark_scoring_allowed,
        "autonomous_action_allowed": result.autonomous_action_allowed,
        "provenance": result.provenance,
    }


def _reason_over_bundle(
    bundle: ClusterKnowledgeEvidenceBundle,
) -> ClusterKnowledgeReasoning:
    evidence_items = bundle.evidence_items

    supported_observations = tuple(
        _supported_observation(evidence)
        for evidence in evidence_items
        if evidence.usable_for_reasoning
        and evidence.quality
        not in {
            KnowledgeQuality.MISSING,
            KnowledgeQuality.WRONG_APPLICATION,
        }
    )
    conflict_warnings = tuple(
        _warning_for_evidence(evidence)
        for evidence in evidence_items
        if evidence.quality == KnowledgeQuality.CONFLICTING
        or evidence.safety == KnowledgeSafety.CONFLICT_REVIEW_REQUIRED
    )
    stale_warnings = tuple(
        _warning_for_evidence(evidence)
        for evidence in evidence_items
        if evidence.quality == KnowledgeQuality.STALE
        or evidence.safety == KnowledgeSafety.STALE_REVIEW_REQUIRED
    )
    knowledge_gaps = tuple(
        f"{evidence.service}::{evidence.indicator}"
        for evidence in evidence_items
        if evidence.quality == KnowledgeQuality.MISSING
    )
    risky_action_warnings = tuple(
        _warning_for_evidence(evidence)
        for evidence in evidence_items
        if evidence.quality == KnowledgeQuality.RISKY_REMEDIATION
        or evidence.safety == KnowledgeSafety.RISKY_REMEDIATION
    )

    return ClusterKnowledgeReasoning(
        cluster_id=bundle.cluster_id,
        source_failure_case_id=bundle.source_failure_case_id,
        reasoning_state=_reasoning_state(
            conflict_warnings=conflict_warnings,
            stale_warnings=stale_warnings,
            knowledge_gaps=knowledge_gaps,
            risky_action_warnings=risky_action_warnings,
            supported_observations=supported_observations,
        ),
        confidence=_confidence(
            evidence_items=evidence_items,
            conflict_warnings=conflict_warnings,
            stale_warnings=stale_warnings,
            knowledge_gaps=knowledge_gaps,
            risky_action_warnings=risky_action_warnings,
        ),
        evidence_signals=tuple(
            _evidence_signal(evidence)
            for evidence in evidence_items
        ),
        supported_observations=supported_observations,
        conflict_warnings=conflict_warnings,
        stale_warnings=stale_warnings,
        knowledge_gaps=knowledge_gaps,
        risky_action_warnings=risky_action_warnings,
        human_review_questions=_human_review_questions(
            conflict_warnings=conflict_warnings,
            stale_warnings=stale_warnings,
            knowledge_gaps=knowledge_gaps,
            risky_action_warnings=risky_action_warnings,
        ),
        benchmark_truth_claim_allowed=False,
        benchmark_scoring_allowed=False,
        human_approval_required=True,
        autonomous_action_allowed=False,
        provenance="synthetic_kb:cluster_reasoning_from_governed_evidence",
    )


def _supported_observation(evidence: GovernedKnowledgeEvidence) -> str:
    return (
        f"{evidence.service}:{evidence.indicator} supported by "
        f"{evidence.quality.value} governed evidence"
    )


def _warning_for_evidence(evidence: GovernedKnowledgeEvidence) -> str:
    article = evidence.article_id or "knowledge-gap"
    return (
        f"{article} requires review: "
        f"quality={evidence.quality.value}, safety={evidence.safety.value}"
    )


def _evidence_signal(
    evidence: GovernedKnowledgeEvidence,
) -> EvidenceReasoningSignal:
    return EvidenceReasoningSignal(
        evidence_id=evidence.evidence_id,
        article_id=evidence.article_id,
        service=evidence.service,
        indicator=evidence.indicator,
        quality=evidence.quality.value,
        safety=evidence.safety.value,
        evidence_weight=evidence.evidence_weight,
        contribution=_contribution_for_quality(evidence.quality),
        limitation=_limitation_for_quality(evidence.quality),
    )


def _reasoning_state(
    conflict_warnings: tuple[str, ...],
    stale_warnings: tuple[str, ...],
    knowledge_gaps: tuple[str, ...],
    risky_action_warnings: tuple[str, ...],
    supported_observations: tuple[str, ...],
) -> ReasoningState:
    if risky_action_warnings or knowledge_gaps:
        return ReasoningState.RISKY_OR_INCOMPLETE
    if conflict_warnings:
        return ReasoningState.SUPPORTED_WITH_CONFLICTS
    if stale_warnings:
        return ReasoningState.STALE_OR_INCOMPLETE
    if supported_observations:
        return ReasoningState.SUPPORTED
    return ReasoningState.MISSING_KNOWLEDGE


def _confidence(
    evidence_items: tuple[GovernedKnowledgeEvidence, ...],
    conflict_warnings: tuple[str, ...],
    stale_warnings: tuple[str, ...],
    knowledge_gaps: tuple[str, ...],
    risky_action_warnings: tuple[str, ...],
) -> ReasoningConfidence:
    if knowledge_gaps or risky_action_warnings:
        return ReasoningConfidence.LOW_WITH_REVIEW
    if conflict_warnings or stale_warnings:
        return ReasoningConfidence.MEDIUM_WITH_REVIEW

    max_weight = max(
        (evidence.evidence_weight for evidence in evidence_items),
        default=0.0,
    )
    if max_weight >= 0.8:
        return ReasoningConfidence.HIGH_WITH_REVIEW
    return ReasoningConfidence.MEDIUM_WITH_REVIEW


def _human_review_questions(
    conflict_warnings: tuple[str, ...],
    stale_warnings: tuple[str, ...],
    knowledge_gaps: tuple[str, ...],
    risky_action_warnings: tuple[str, ...],
) -> tuple[str, ...]:
    questions: list[str] = [
        "Does current telemetry support this evidence-backed hypothesis?",
        "Is there recent change context that explains the symptoms?",
    ]

    if conflict_warnings:
        questions.append("Which conflicting article should be trusted for this incident?")
    if stale_warnings:
        questions.append("Is stale guidance still valid for the current topology?")
    if knowledge_gaps:
        questions.append("Should a new knowledge article be created for this gap?")
    if risky_action_warnings:
        questions.append("Is the risky remediation justified by blast-radius analysis?")

    return tuple(questions)


def _contribution_for_quality(quality: KnowledgeQuality) -> str:
    if quality == KnowledgeQuality.EXACT:
        return "supports hypothesis"
    if quality == KnowledgeQuality.PARTIAL:
        return "supports context only"
    if quality == KnowledgeQuality.STALE:
        return "historical context only"
    if quality == KnowledgeQuality.CONFLICTING:
        return "raises contradiction"
    if quality == KnowledgeQuality.RISKY_REMEDIATION:
        return "raises remediation risk"
    if quality == KnowledgeQuality.HUMAN_APPROVAL_REQUIRED:
        return "requires approval context"
    if quality == KnowledgeQuality.MISSING:
        return "identifies knowledge gap"
    return "excluded from reasoning"


def _limitation_for_quality(quality: KnowledgeQuality) -> str:
    if quality == KnowledgeQuality.EXACT:
        return "still not benchmark truth"
    if quality == KnowledgeQuality.PARTIAL:
        return "insufficient for root-cause conclusion"
    if quality == KnowledgeQuality.STALE:
        return "may not reflect current topology"
    if quality == KnowledgeQuality.CONFLICTING:
        return "must be reconciled before conclusion"
    if quality == KnowledgeQuality.RISKY_REMEDIATION:
        return "action requires explicit human approval"
    if quality == KnowledgeQuality.HUMAN_APPROVAL_REQUIRED:
        return "cannot authorize action"
    if quality == KnowledgeQuality.MISSING:
        return "cannot support conclusion"
    return "not usable"
