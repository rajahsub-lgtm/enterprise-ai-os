"""Sprint 4B governed LLM reasoning engine seam.

Classification: provider-neutral LLM orchestration boundary.

This module still does not call a hosted model. It creates the seam for a future
real LLM adapter by defining:

- prompt packets
- evidence citations
- uncertainty instructions
- policy/cost/loop limits
- deterministic draft generation
- validation through the governed LLM output validator

A future provider must plug into this seam and still pass the same validation.
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
from eaios.sprint4.governed_llm_output_validator import (
    LLMOutputValidationResult,
    ProposedLLMClusterOutput,
    build_deterministic_llm_draft,
    validate_llm_outputs,
)


class LLMRunMode(str, Enum):
    DETERMINISTIC_CONTRACT = "DETERMINISTIC_CONTRACT"
    PROVIDER_READY_BLOCKED = "PROVIDER_READY_BLOCKED"


@dataclass(frozen=True)
class LLMSafetyEnvelope:
    human_approval_required: bool
    autonomous_action_allowed: bool
    benchmark_truth_claim_allowed: bool
    benchmark_scoring_allowed: bool
    max_prompt_evidence_items: int
    max_reasoning_loops: int
    max_estimated_tokens: int
    max_estimated_cost_usd: float
    provider_call_allowed: bool


@dataclass(frozen=True)
class LLMReasoningPromptPacket:
    packet_id: str
    cluster_id: str
    source_failure_case_id: str
    task: str
    evidence_ids: tuple[str, ...]
    evidence_summaries: tuple[str, ...]
    required_uncertainty_flags: tuple[str, ...]
    prohibited_claims: tuple[str, ...]
    required_output_fields: tuple[str, ...]
    safety_envelope: LLMSafetyEnvelope
    provenance: str


@dataclass(frozen=True)
class LLMReasoningEngineRun:
    run_id: str
    mode: LLMRunMode
    prompt_packets: tuple[LLMReasoningPromptPacket, ...]
    proposed_outputs: tuple[ProposedLLMClusterOutput, ...]
    validation_result: LLMOutputValidationResult
    accepted_outputs: tuple[ProposedLLMClusterOutput, ...]
    rejected_outputs: tuple[ProposedLLMClusterOutput, ...]
    provider_call_made: bool
    human_approval_required: bool
    benchmark_scoring_allowed: bool
    autonomous_action_allowed: bool
    provenance: str


def run_governed_llm_reasoning_engine(
    reasoning_result: GovernedKnowledgeReasoningResult | None = None,
    mode: LLMRunMode = LLMRunMode.DETERMINISTIC_CONTRACT,
) -> LLMReasoningEngineRun:
    if reasoning_result is None:
        reasoning_result = build_governed_knowledge_reasoning()

    prompt_packets = tuple(
        build_prompt_packet(reasoning)
        for reasoning in reasoning_result.cluster_reasoning
    )

    proposed_outputs = _build_outputs_for_mode(
        reasoning_result=reasoning_result,
        mode=mode,
    )
    validation_result = validate_llm_outputs(
        outputs=proposed_outputs,
        reasoning_result=reasoning_result,
    )

    accepted_outputs = tuple(
        output
        for output, validation in zip(proposed_outputs, validation_result.validations)
        if validation.accepted
    )
    rejected_outputs = tuple(
        output
        for output, validation in zip(proposed_outputs, validation_result.validations)
        if not validation.accepted
    )

    return LLMReasoningEngineRun(
        run_id="sprint4b-governed-llm-reasoning-engine-run-001",
        mode=mode,
        prompt_packets=prompt_packets,
        proposed_outputs=proposed_outputs,
        validation_result=validation_result,
        accepted_outputs=accepted_outputs,
        rejected_outputs=rejected_outputs,
        provider_call_made=False,
        human_approval_required=True,
        benchmark_scoring_allowed=False,
        autonomous_action_allowed=False,
        provenance="governed_llm_reasoning_engine:provider_neutral_contract_run",
    )


def build_prompt_packet(
    reasoning: ClusterKnowledgeReasoning,
) -> LLMReasoningPromptPacket:
    safety_envelope = LLMSafetyEnvelope(
        human_approval_required=True,
        autonomous_action_allowed=False,
        benchmark_truth_claim_allowed=False,
        benchmark_scoring_allowed=False,
        max_prompt_evidence_items=20,
        max_reasoning_loops=1,
        max_estimated_tokens=2400,
        max_estimated_cost_usd=0.05,
        provider_call_allowed=False,
    )

    return LLMReasoningPromptPacket(
        packet_id=f"llm-prompt::{reasoning.cluster_id}",
        cluster_id=reasoning.cluster_id,
        source_failure_case_id=reasoning.source_failure_case_id,
        task=(
            "Produce a tentative, cited, human-reviewable operational hypothesis "
            "from governed evidence. Do not claim benchmark truth."
        ),
        evidence_ids=tuple(
            signal.evidence_id for signal in reasoning.evidence_signals
        ),
        evidence_summaries=tuple(
            _evidence_summary(signal)
            for signal in reasoning.evidence_signals
        ),
        required_uncertainty_flags=_required_uncertainty_flags(reasoning),
        prohibited_claims=(
            "benchmark truth",
            "benchmark score",
            "autonomous approval",
            "remediation authorization",
            "root cause proven by knowledge",
        ),
        required_output_fields=(
            "cluster_id",
            "source_failure_case_id",
            "conclusion",
            "cited_evidence_ids",
            "uncertainty_flags",
            "recommended_next_steps",
            "human_approval_required",
            "autonomous_action_allowed",
            "benchmark_truth_claim_allowed",
            "benchmark_scoring_allowed",
            "provenance",
        ),
        safety_envelope=safety_envelope,
        provenance="governed_llm_reasoning_engine:prompt_packet",
    )


def summarize_engine_run(
    run: LLMReasoningEngineRun,
) -> dict[str, object]:
    return {
        "run_id": run.run_id,
        "mode": run.mode.value,
        "prompt_packet_count": len(run.prompt_packets),
        "proposed_output_count": len(run.proposed_outputs),
        "accepted_output_count": len(run.accepted_outputs),
        "rejected_output_count": len(run.rejected_outputs),
        "provider_call_made": run.provider_call_made,
        "human_approval_required": run.human_approval_required,
        "benchmark_scoring_allowed": run.benchmark_scoring_allowed,
        "autonomous_action_allowed": run.autonomous_action_allowed,
        "validation_issue_codes": tuple(
            issue.code.value
            for validation in run.validation_result.validations
            for issue in validation.issues
        ),
    }


def to_view_model(
    run: LLMReasoningEngineRun,
) -> dict[str, Any]:
    return {
        "summary": summarize_engine_run(run),
        "prompt_packets": [
            {
                "packet_id": packet.packet_id,
                "cluster_id": packet.cluster_id,
                "source_failure_case_id": packet.source_failure_case_id,
                "task": packet.task,
                "evidence_ids": list(packet.evidence_ids),
                "evidence_summaries": list(packet.evidence_summaries),
                "required_uncertainty_flags": list(
                    packet.required_uncertainty_flags
                ),
                "prohibited_claims": list(packet.prohibited_claims),
                "required_output_fields": list(packet.required_output_fields),
                "safety_envelope": {
                    "human_approval_required": (
                        packet.safety_envelope.human_approval_required
                    ),
                    "autonomous_action_allowed": (
                        packet.safety_envelope.autonomous_action_allowed
                    ),
                    "benchmark_truth_claim_allowed": (
                        packet.safety_envelope.benchmark_truth_claim_allowed
                    ),
                    "benchmark_scoring_allowed": (
                        packet.safety_envelope.benchmark_scoring_allowed
                    ),
                    "max_prompt_evidence_items": (
                        packet.safety_envelope.max_prompt_evidence_items
                    ),
                    "max_reasoning_loops": (
                        packet.safety_envelope.max_reasoning_loops
                    ),
                    "max_estimated_tokens": (
                        packet.safety_envelope.max_estimated_tokens
                    ),
                    "max_estimated_cost_usd": (
                        packet.safety_envelope.max_estimated_cost_usd
                    ),
                    "provider_call_allowed": (
                        packet.safety_envelope.provider_call_allowed
                    ),
                },
                "provenance": packet.provenance,
            }
            for packet in run.prompt_packets
        ],
        "accepted_outputs": [
            {
                "cluster_id": output.cluster_id,
                "source_failure_case_id": output.source_failure_case_id,
                "conclusion": output.conclusion,
                "cited_evidence_ids": list(output.cited_evidence_ids),
                "uncertainty_flags": list(output.uncertainty_flags),
                "recommended_next_steps": list(output.recommended_next_steps),
                "human_approval_required": output.human_approval_required,
                "autonomous_action_allowed": output.autonomous_action_allowed,
                "benchmark_truth_claim_allowed": (
                    output.benchmark_truth_claim_allowed
                ),
                "benchmark_scoring_allowed": output.benchmark_scoring_allowed,
                "provenance": output.provenance,
            }
            for output in run.accepted_outputs
        ],
        "validation": {
            "accepted_cluster_count": run.validation_result.accepted_cluster_count,
            "rejected_cluster_count": run.validation_result.rejected_cluster_count,
            "human_approval_required": run.validation_result.human_approval_required,
            "benchmark_scoring_allowed": run.validation_result.benchmark_scoring_allowed,
            "autonomous_action_allowed": run.validation_result.autonomous_action_allowed,
        },
        "provenance": run.provenance,
    }


def _build_outputs_for_mode(
    reasoning_result: GovernedKnowledgeReasoningResult,
    mode: LLMRunMode,
) -> tuple[ProposedLLMClusterOutput, ...]:
    if mode == LLMRunMode.DETERMINISTIC_CONTRACT:
        return build_deterministic_llm_draft(reasoning_result)

    if mode == LLMRunMode.PROVIDER_READY_BLOCKED:
        return build_deterministic_llm_draft(reasoning_result)

    raise ValueError(f"Unsupported LLM run mode: {mode}")


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


def _evidence_summary(signal: Any) -> str:
    article = signal.article_id or "knowledge-gap"
    return (
        f"{signal.evidence_id} | article={article} | "
        f"service={signal.service} | indicator={signal.indicator} | "
        f"quality={signal.quality} | safety={signal.safety} | "
        f"contribution={signal.contribution} | limitation={signal.limitation}"
    )
