"""Sprint 4B cluster knowledge evidence adapter.

Classification: governed uncertain evidence layer.

This module attaches governed KB evidence to 4A issue clusters.

Important boundary:
- KB evidence can inform reasoning.
- KB evidence cannot define benchmark truth.
- KB evidence cannot score benchmark results.
- Human approval remains required.
- Autonomous action remains disabled.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from eaios.sprint4.governed_knowledge_base import (
    DEFAULT_KB_PATH,
    GovernedKnowledgeEvidence,
    KnowledgeQuery,
    KnowledgeRetrievalResult,
    load_governed_knowledge_base,
    retrieve_knowledge,
    summarize_retrieval_result,
)
from eaios.sprint4.issue_clustering import cluster_synthesized_itil_records
from eaios.sprint4.itil_synthesizer import synthesize_itil_records
from eaios.sprint4.rcaeval_contracts import (
    load_structural_sample,
    build_benchmark_targets,
)


DEFAULT_STRUCTURAL_SAMPLE_PATH = Path(
    "data/domain/it_application_health/rcaeval_train_ticket_structural_sample.json"
)


@dataclass(frozen=True)
class ClusterKnowledgeEvidenceBundle:
    cluster_id: str
    source_failure_case_id: str
    evidence_items: tuple[GovernedKnowledgeEvidence, ...]
    retrieval_summaries: tuple[dict[str, object], ...]
    evidence_article_ids: tuple[str, ...]
    missing_knowledge: bool
    conflict_detected: bool
    stale_evidence_present: bool
    risky_evidence_present: bool
    human_approval_required: bool
    benchmark_truth_eligible: bool
    benchmark_scoring_allowed: bool
    autonomous_action_allowed: bool
    provenance: str


@dataclass(frozen=True)
class ClusterKnowledgeEvidenceResult:
    bundles: tuple[ClusterKnowledgeEvidenceBundle, ...]
    total_evidence_items: int
    clusters_with_missing_knowledge: tuple[str, ...]
    clusters_with_conflicts: tuple[str, ...]
    clusters_with_stale_evidence: tuple[str, ...]
    clusters_with_risky_evidence: tuple[str, ...]
    human_approval_required: bool
    benchmark_scoring_allowed: bool
    autonomous_action_allowed: bool


def build_cluster_knowledge_evidence(
    sample_path: str | Path = DEFAULT_STRUCTURAL_SAMPLE_PATH,
    kb_path: str | Path = DEFAULT_KB_PATH,
    application: str = "train-ticket-structural",
) -> ClusterKnowledgeEvidenceResult:
    sample = load_structural_sample(sample_path)
    records = synthesize_itil_records(sample)
    targets = build_benchmark_targets(sample)
    clustering_result = cluster_synthesized_itil_records(
        records=records,
        topology=sample.service_topology,
        benchmark_targets=targets,
    )
    knowledge_base = load_governed_knowledge_base(kb_path)

    alert_by_symptom_id = {
        alert.source_symptom_id: alert
        for alert in records.alerts
    }
    fault_type_by_failure_id = {
        fault.failure_case_id: fault.fault_type
        for fault in sample.fault_scenarios
    }

    bundles = tuple(
        _build_bundle_for_cluster(
            cluster=cluster,
            alert_by_symptom_id=alert_by_symptom_id,
            fault_type=fault_type_by_failure_id[cluster.source_failure_case_id],
            knowledge_base=knowledge_base,
            application=application,
        )
        for cluster in clustering_result.clusters
    )

    return ClusterKnowledgeEvidenceResult(
        bundles=bundles,
        total_evidence_items=sum(len(bundle.evidence_items) for bundle in bundles),
        clusters_with_missing_knowledge=tuple(
            bundle.cluster_id for bundle in bundles if bundle.missing_knowledge
        ),
        clusters_with_conflicts=tuple(
            bundle.cluster_id for bundle in bundles if bundle.conflict_detected
        ),
        clusters_with_stale_evidence=tuple(
            bundle.cluster_id for bundle in bundles if bundle.stale_evidence_present
        ),
        clusters_with_risky_evidence=tuple(
            bundle.cluster_id for bundle in bundles if bundle.risky_evidence_present
        ),
        human_approval_required=True,
        benchmark_scoring_allowed=False,
        autonomous_action_allowed=False,
    )


def summarize_cluster_knowledge_evidence(
    result: ClusterKnowledgeEvidenceResult,
) -> dict[str, object]:
    return {
        "cluster_count": len(result.bundles),
        "total_evidence_items": result.total_evidence_items,
        "clusters_with_missing_knowledge": result.clusters_with_missing_knowledge,
        "clusters_with_conflicts": result.clusters_with_conflicts,
        "clusters_with_stale_evidence": result.clusters_with_stale_evidence,
        "clusters_with_risky_evidence": result.clusters_with_risky_evidence,
        "human_approval_required": result.human_approval_required,
        "benchmark_scoring_allowed": result.benchmark_scoring_allowed,
        "autonomous_action_allowed": result.autonomous_action_allowed,
    }


def to_view_model(
    result: ClusterKnowledgeEvidenceResult,
) -> dict[str, Any]:
    return {
        "summary": summarize_cluster_knowledge_evidence(result),
        "bundles": [
            {
                "cluster_id": bundle.cluster_id,
                "source_failure_case_id": bundle.source_failure_case_id,
                "evidence_article_ids": list(bundle.evidence_article_ids),
                "evidence_count": len(bundle.evidence_items),
                "qualities": [
                    evidence.quality.value for evidence in bundle.evidence_items
                ],
                "safety_states": [
                    evidence.safety.value for evidence in bundle.evidence_items
                ],
                "missing_knowledge": bundle.missing_knowledge,
                "conflict_detected": bundle.conflict_detected,
                "stale_evidence_present": bundle.stale_evidence_present,
                "risky_evidence_present": bundle.risky_evidence_present,
                "human_approval_required": bundle.human_approval_required,
                "benchmark_truth_eligible": bundle.benchmark_truth_eligible,
                "benchmark_scoring_allowed": bundle.benchmark_scoring_allowed,
                "autonomous_action_allowed": bundle.autonomous_action_allowed,
                "retrieval_summaries": list(bundle.retrieval_summaries),
                "provenance": bundle.provenance,
            }
            for bundle in result.bundles
        ],
    }


def _build_bundle_for_cluster(
    cluster: Any,
    alert_by_symptom_id: dict[str, Any],
    fault_type: str,
    knowledge_base: Any,
    application: str,
) -> ClusterKnowledgeEvidenceBundle:
    retrieval_results = tuple(
        retrieve_knowledge(
            knowledge_base,
            KnowledgeQuery(
                application=application,
                service=alert_by_symptom_id[symptom_id].affected_service,
                indicator=alert_by_symptom_id[symptom_id].indicator,
                fault_type=fault_type,
            ),
        )
        for symptom_id in cluster.symptom_ids
    )

    evidence_items = tuple(
        evidence
        for result in retrieval_results
        for evidence in result.evidence_items
    )

    return ClusterKnowledgeEvidenceBundle(
        cluster_id=cluster.cluster_id,
        source_failure_case_id=cluster.source_failure_case_id,
        evidence_items=evidence_items,
        retrieval_summaries=tuple(
            summarize_retrieval_result(result)
            for result in retrieval_results
        ),
        evidence_article_ids=tuple(
            evidence.article_id
            for evidence in evidence_items
            if evidence.article_id is not None
        ),
        missing_knowledge=any(result.missing_knowledge for result in retrieval_results),
        conflict_detected=any(result.conflict_detected for result in retrieval_results),
        stale_evidence_present=any(
            result.stale_evidence_present for result in retrieval_results
        ),
        risky_evidence_present=any(
            result.risky_evidence_present for result in retrieval_results
        ),
        human_approval_required=True,
        benchmark_truth_eligible=False,
        benchmark_scoring_allowed=False,
        autonomous_action_allowed=False,
        provenance="synthetic_kb:cluster_knowledge_evidence_bundle",
    )
