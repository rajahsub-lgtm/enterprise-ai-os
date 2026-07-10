"""Sprint 4B governed reasoning observation snapshot.

Classification: Sprint 4B stable output contract.

This module packages the full 4B path:

4A application health observation
-> governed imperfect KB evidence
-> governed knowledge reasoning
-> governed LLM prompt/output validation seam
-> dashboard/export-ready view model

It does not call a real LLM provider and does not score benchmarks from KB or
LLM output.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from eaios.sprint4.application_health_observation import (
    build_application_health_observation_snapshot,
    to_view_model as application_health_to_view_model,
)
from eaios.sprint4.cluster_knowledge_evidence import (
    build_cluster_knowledge_evidence,
    summarize_cluster_knowledge_evidence,
    to_view_model as cluster_knowledge_to_view_model,
)
from eaios.sprint4.governed_knowledge_reasoning import (
    build_governed_knowledge_reasoning,
    summarize_governed_knowledge_reasoning,
    to_view_model as knowledge_reasoning_to_view_model,
)
from eaios.sprint4.governed_llm_reasoning_engine import (
    run_governed_llm_reasoning_engine,
    summarize_engine_run,
    to_view_model as llm_engine_to_view_model,
)


@dataclass(frozen=True)
class GovernedReasoningObservationSnapshot:
    snapshot_id: str
    application_health_snapshot_id: str
    source_dataset_role: str
    cluster_count: int
    benchmark_result_states: tuple[str, ...]
    knowledge_evidence_summary: dict[str, object]
    knowledge_reasoning_summary: dict[str, object]
    llm_engine_summary: dict[str, object]
    governance_boundaries: tuple[str, ...]
    application_health_view: dict[str, Any]
    cluster_knowledge_view: dict[str, Any]
    knowledge_reasoning_view: dict[str, Any]
    llm_engine_view: dict[str, Any]
    human_approval_required: bool
    benchmark_scoring_allowed_from_kb_or_llm: bool
    autonomous_action_allowed: bool
    provider_call_made: bool
    provenance: str


def build_governed_reasoning_observation_snapshot() -> GovernedReasoningObservationSnapshot:
    application_health = build_application_health_observation_snapshot()
    cluster_knowledge = build_cluster_knowledge_evidence()
    knowledge_reasoning = build_governed_knowledge_reasoning(cluster_knowledge)
    llm_engine_run = run_governed_llm_reasoning_engine(knowledge_reasoning)

    return GovernedReasoningObservationSnapshot(
        snapshot_id=(
            "governed-reasoning::"
            f"{application_health.composition_scenario_id}"
        ),
        application_health_snapshot_id=application_health.snapshot_id,
        source_dataset_role=application_health.source_dataset_role,
        cluster_count=len(application_health.clusters),
        benchmark_result_states=tuple(
            result.state for result in application_health.benchmark_results
        ),
        knowledge_evidence_summary=summarize_cluster_knowledge_evidence(
            cluster_knowledge
        ),
        knowledge_reasoning_summary=summarize_governed_knowledge_reasoning(
            knowledge_reasoning
        ),
        llm_engine_summary=summarize_engine_run(llm_engine_run),
        governance_boundaries=(
            "benchmark_truth_external",
            "benchmark_scoring_from_4a_only",
            "kb_evidence_cannot_define_truth",
            "llm_output_cannot_score_benchmark",
            "citations_required",
            "uncertainty_required",
            "human_approval_required",
            "autonomous_action_disabled",
            "provider_call_blocked",
        ),
        application_health_view=application_health_to_view_model(application_health),
        cluster_knowledge_view=cluster_knowledge_to_view_model(cluster_knowledge),
        knowledge_reasoning_view=knowledge_reasoning_to_view_model(
            knowledge_reasoning
        ),
        llm_engine_view=llm_engine_to_view_model(llm_engine_run),
        human_approval_required=True,
        benchmark_scoring_allowed_from_kb_or_llm=False,
        autonomous_action_allowed=False,
        provider_call_made=False,
        provenance="sprint4b:governed_reasoning_observation_snapshot",
    )


def summarize_governed_reasoning_observation(
    snapshot: GovernedReasoningObservationSnapshot,
) -> dict[str, object]:
    return {
        "snapshot_id": snapshot.snapshot_id,
        "application_health_snapshot_id": snapshot.application_health_snapshot_id,
        "cluster_count": snapshot.cluster_count,
        "benchmark_result_states": snapshot.benchmark_result_states,
        "knowledge_evidence_total_items": snapshot.knowledge_evidence_summary[
            "total_evidence_items"
        ],
        "knowledge_reasoning_states": snapshot.knowledge_reasoning_summary[
            "reasoning_states"
        ],
        "llm_accepted_output_count": snapshot.llm_engine_summary[
            "accepted_output_count"
        ],
        "llm_rejected_output_count": snapshot.llm_engine_summary[
            "rejected_output_count"
        ],
        "provider_call_made": snapshot.provider_call_made,
        "human_approval_required": snapshot.human_approval_required,
        "benchmark_scoring_allowed_from_kb_or_llm": (
            snapshot.benchmark_scoring_allowed_from_kb_or_llm
        ),
        "autonomous_action_allowed": snapshot.autonomous_action_allowed,
    }


def to_view_model(
    snapshot: GovernedReasoningObservationSnapshot,
) -> dict[str, Any]:
    application_health_view = {
        "summary": {
            "snapshot_id": snapshot.application_health_snapshot_id,
            "cluster_count": snapshot.cluster_count,
            "benchmark_result_states": snapshot.benchmark_result_states,
        },
        **snapshot.application_health_view,
    }

    return {
        "summary": summarize_governed_reasoning_observation(snapshot),
        "governance_boundaries": list(snapshot.governance_boundaries),
        "application_health": application_health_view,
        "cluster_knowledge": snapshot.cluster_knowledge_view,
        "knowledge_reasoning": snapshot.knowledge_reasoning_view,
        "llm_engine": snapshot.llm_engine_view,
        "human_approval_required": snapshot.human_approval_required,
        "benchmark_scoring_allowed_from_kb_or_llm": (
            snapshot.benchmark_scoring_allowed_from_kb_or_llm
        ),
        "autonomous_action_allowed": snapshot.autonomous_action_allowed,
        "provider_call_made": snapshot.provider_call_made,
        "provenance": snapshot.provenance,
    }
