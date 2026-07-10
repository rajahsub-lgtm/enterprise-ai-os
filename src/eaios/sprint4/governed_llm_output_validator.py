"""Sprint 4B governed LLM output validator.

Classification: LLM boundary validation gate.

This module does not call a real LLM provider. It defines and validates the
output contract that a future real LLM must satisfy.

The validator enforces:
- schema-shaped cluster reasoning output
- governed evidence citations
- uncertainty preservation
- no benchmark truth claims from KB/LLM output
- no benchmark scoring from KB/LLM output
- human approval required
- autonomous action disabled
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint4.governed_knowledge_reasoning import (
    ClusterKnowledgeReasoning,
    GovernedKnowledgeReasoningResult,
    build_governed_knowledge_reasoning,
)


class LLMValidationIssueCode(str, Enum):
    UNKNOWN_CLUSTER = "UNKNOWN_CLUSTER"
    MISSING_CITATIONS = "MISSING_CITATIONS"
    UNKNOWN_CITATION = "UNKNOWN_CITATION"
    MISSING_UNCERTAINTY_FLAG = "MISSING_UNCERTAINTY_FLAG"
    BENCHMARK_TRUTH_CLAIM_BLOCKED = "BENCHMARK_TRUTH_CLAIM_BLOCKED"
    BENCHMARK_SCORING_BLOCKED = "BENCHMARK_SCORING_BLOCKED"
    HUMAN_APPROVAL_REQUIRED = "HUMAN_APPROVAL_REQUIRED"
    AUTONOMOUS_ACTION_BLOCKED = "AUTONOMOUS_ACTION_BLOCKED"
    OVERCONFIDENT_CONCLUSION_BLOCKED = "OVERCONFIDENT_CONCLUSION_BLOCKED"


@dataclass(frozen=True)
class ProposedLLMClusterOutput:
    cluster_id: str
    source_failure_case_id: str
    conclusion: str
    cited_evidence_ids: tuple[str, ...]
    uncertainty_flags: tuple[str, ...]
    recommended_next_steps: tuple[str, ...]
    human_approval_required: bool
    autonomous_action_allowed: bool
    benchmark_truth_claim_allowed: bool
    benchmark_scoring_allowed: bool
    provenance: str


@dataclass(frozen=True)
class LLMOutputValidationIssue:
    code: LLMValidationIssueCode
    message: str


@dataclass(frozen=True)
class LLMClusterOutputValidation:
    cluster_id: str
    accepted: bool
    known_cluster: bool
    cited_evidence_ids: tuple[str, ...]
    unknown_citation_ids: tuple[str, ...]
    required_uncertainty_flags: tuple[str, ...]
    missing_uncertainty_flags: tuple[str, ...]
    issues: tuple[LLMOutputValidationIssue, ...]


@dataclass(frozen=True)
class LLMOutputValidationResult:
    validations: tuple[LLMClusterOutputValidation, ...]
    accepted_cluster_count: int
    rejected_cluster_count: int
    human_approval_required: bool
    benchmark_scoring_allowed: bool
    autonomous_action_allowed: bool
    provenance: str


def build_deterministic_llm_draft(
    reasoning_result: GovernedKnowledgeReasoningResult | None = None,
) -> tuple[ProposedLLMClusterOutput, ...]:
    """Create a deterministic valid draft that mimics future LLM output shape."""

    if reasoning_result is None:
        reasoning_result = build_governed_knowledge_reasoning()

    return tuple(
        ProposedLLMClusterOutput(
            cluster_id=reasoning.cluster_id,
            source_failure_case_id=reasoning.source_failure_case_id,
            conclusion=_safe_conclusion(reasoning),
            cited_evidence_ids=tuple(
                signal.evidence_id for signal in reasoning.evidence_signals
            ),
            uncertainty_flags=_required_uncertainty_flags(reasoning),
            recommended_next_steps=_safe_next_steps(reasoning),
            human_approval_required=True,
            autonomous_action_allowed=False,
            benchmark_truth_claim_allowed=False,
            benchmark_scoring_allowed=False,
            provenance="deterministic_llm_draft:validated_contract_shape",
        )
        for reasoning in reasoning_result.cluster_reasoning
    )


def validate_llm_outputs(
    outputs: tuple[ProposedLLMClusterOutput, ...],
    reasoning_result: GovernedKnowledgeReasoningResult | None = None,
) -> LLMOutputValidationResult:
    if reasoning_result is None:
        reasoning_result = build_governed_knowledge_reasoning()

    reasoning_by_cluster = {
        reasoning.cluster_id: reasoning
        for reasoning in reasoning_result.cluster_reasoning
    }

    validations = tuple(
        _validate_output(output, reasoning_by_cluster)
        for output in outputs
    )

    return LLMOutputValidationResult(
        validations=validations,
        accepted_cluster_count=sum(
            1 for validation in validations if validation.accepted
        ),
        rejected_cluster_count=sum(
            1 for validation in validations if not validation.accepted
        ),
        human_approval_required=True,
        benchmark_scoring_allowed=False,
        autonomous_action_allowed=False,
        provenance="governed_llm_output_validator:validation_result",
    )


def summarize_validation_result(
    result: LLMOutputValidationResult,
) -> dict[str, object]:
    return {
        "accepted_cluster_count": result.accepted_cluster_count,
        "rejected_cluster_count": result.rejected_cluster_count,
        "issue_codes": tuple(
            issue.code.value
            for validation in result.validations
            for issue in validation.issues
        ),
        "human_approval_required": result.human_approval_required,
        "benchmark_scoring_allowed": result.benchmark_scoring_allowed,
        "autonomous_action_allowed": result.autonomous_action_allowed,
    }


def to_view_model(
    result: LLMOutputValidationResult,
) -> dict[str, Any]:
    return {
        "summary": summarize_validation_result(result),
        "validations": [
            {
                "cluster_id": validation.cluster_id,
                "accepted": validation.accepted,
                "known_cluster": validation.known_cluster,
                "cited_evidence_ids": list(validation.cited_evidence_ids),
                "unknown_citation_ids": list(validation.unknown_citation_ids),
                "required_uncertainty_flags": list(
                    validation.required_uncertainty_flags
                ),
                "missing_uncertainty_flags": list(
                    validation.missing_uncertainty_flags
                ),
                "issues": [
                    {
                        "code": issue.code.value,
                        "message": issue.message,
                    }
                    for issue in validation.issues
                ],
            }
            for validation in result.validations
        ],
        "human_approval_required": result.human_approval_required,
        "benchmark_scoring_allowed": result.benchmark_scoring_allowed,
        "autonomous_action_allowed": result.autonomous_action_allowed,
        "provenance": result.provenance,
    }


def _validate_output(
    output: ProposedLLMClusterOutput,
    reasoning_by_cluster: dict[str, ClusterKnowledgeReasoning],
) -> LLMClusterOutputValidation:
    issues: list[LLMOutputValidationIssue] = []

    reasoning = reasoning_by_cluster.get(output.cluster_id)
    if reasoning is None:
        issues.append(
            LLMOutputValidationIssue(
                code=LLMValidationIssueCode.UNKNOWN_CLUSTER,
                message="LLM output referenced a cluster that was not produced by governed reasoning.",
            )
        )
        return LLMClusterOutputValidation(
            cluster_id=output.cluster_id,
            accepted=False,
            known_cluster=False,
            cited_evidence_ids=output.cited_evidence_ids,
            unknown_citation_ids=output.cited_evidence_ids,
            required_uncertainty_flags=(),
            missing_uncertainty_flags=(),
            issues=tuple(issues),
        )

    known_evidence_ids = {
        signal.evidence_id for signal in reasoning.evidence_signals
    }
    cited_evidence_ids = set(output.cited_evidence_ids)
    unknown_citation_ids = tuple(
        sorted(cited_evidence_ids.difference(known_evidence_ids))
    )

    if not output.cited_evidence_ids:
        issues.append(
            LLMOutputValidationIssue(
                code=LLMValidationIssueCode.MISSING_CITATIONS,
                message="LLM output must cite governed evidence.",
            )
        )

    if unknown_citation_ids:
        issues.append(
            LLMOutputValidationIssue(
                code=LLMValidationIssueCode.UNKNOWN_CITATION,
                message="LLM output cited evidence that is not in the governed bundle.",
            )
        )

    required_flags = _required_uncertainty_flags(reasoning)
    missing_flags = tuple(
        flag for flag in required_flags if flag not in output.uncertainty_flags
    )

    if missing_flags:
        issues.append(
            LLMOutputValidationIssue(
                code=LLMValidationIssueCode.MISSING_UNCERTAINTY_FLAG,
                message="LLM output omitted required uncertainty flags.",
            )
        )

    if output.benchmark_truth_claim_allowed:
        issues.append(
            LLMOutputValidationIssue(
                code=LLMValidationIssueCode.BENCHMARK_TRUTH_CLAIM_BLOCKED,
                message="LLM output cannot claim benchmark truth from KB evidence.",
            )
        )

    if output.benchmark_scoring_allowed:
        issues.append(
            LLMOutputValidationIssue(
                code=LLMValidationIssueCode.BENCHMARK_SCORING_BLOCKED,
                message="LLM output cannot score benchmark results.",
            )
        )

    if output.human_approval_required is not True:
        issues.append(
            LLMOutputValidationIssue(
                code=LLMValidationIssueCode.HUMAN_APPROVAL_REQUIRED,
                message="LLM output must preserve human approval.",
            )
        )

    if output.autonomous_action_allowed is not False:
        issues.append(
            LLMOutputValidationIssue(
                code=LLMValidationIssueCode.AUTONOMOUS_ACTION_BLOCKED,
                message="LLM output must not enable autonomous action.",
            )
        )

    if _is_overconfident(output.conclusion):
        issues.append(
            LLMOutputValidationIssue(
                code=LLMValidationIssueCode.OVERCONFIDENT_CONCLUSION_BLOCKED,
                message="LLM output must remain tentative and evidence-grounded.",
            )
        )

    return LLMClusterOutputValidation(
        cluster_id=output.cluster_id,
        accepted=not issues,
        known_cluster=True,
        cited_evidence_ids=output.cited_evidence_ids,
        unknown_citation_ids=unknown_citation_ids,
        required_uncertainty_flags=required_flags,
        missing_uncertainty_flags=missing_flags,
        issues=tuple(issues),
    )


def _required_uncertainty_flags(
    reasoning: ClusterKnowledgeReasoning,
) -> tuple[str, ...]:
    flags = ["human_review_required", "not_benchmark_truth"]

    if reasoning.conflict_warnings:
        flags.append("conflict_detected")
    if reasoning.stale_warnings:
        flags.append("stale_evidence_present")
    if reasoning.knowledge_gaps:
        flags.append("knowledge_gap_present")
    if reasoning.risky_action_warnings:
        flags.append("risky_remediation_present")

    return tuple(flags)


def _safe_conclusion(reasoning: ClusterKnowledgeReasoning) -> str:
    return (
        f"Governed evidence suggests a reviewable hypothesis for "
        f"{reasoning.cluster_id}; this is not benchmark truth and requires "
        f"human approval."
    )


def _safe_next_steps(
    reasoning: ClusterKnowledgeReasoning,
) -> tuple[str, ...]:
    steps = [
        "Review cited governed evidence.",
        "Compare hypothesis with current telemetry and change context.",
        "Keep benchmark verification separate from KB reasoning.",
        "Request human approval before any operational action.",
    ]

    if reasoning.conflict_warnings:
        steps.append("Resolve conflicting knowledge before final conclusion.")
    if reasoning.stale_warnings:
        steps.append("Validate stale guidance against current topology.")
    if reasoning.knowledge_gaps:
        steps.append("Create or update knowledge article for the gap.")
    if reasoning.risky_action_warnings:
        steps.append("Perform blast-radius review before remediation.")

    return tuple(steps)


def _is_overconfident(conclusion: str) -> bool:
    lowered = conclusion.lower()
    blocked_phrases = (
        "proves the root cause",
        "is benchmark truth",
        "is the benchmark truth",
        "can be scored as benchmark",
        "no human approval required",
        "autonomous action approved",
    )
    return any(phrase in lowered for phrase in blocked_phrases)
