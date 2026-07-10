"""Sprint 4 issue clustering.

Classification: EAIOS Sprint 4 orchestration boundary.

This module clusters synthesized ITIL incidents while preserving the Sprint 4
anti-circularity rule:

- Cluster membership for benchmark scoring is derived from source_failure_case_id.
- Root-cause scoring uses BenchmarkVerificationTarget.
- Noise is excluded.
- The knowledge base is not used as answer key.
"""

from __future__ import annotations

from dataclasses import dataclass

from eaios.sprint4.itil_synthesizer import SyntheticIncident, SyntheticITILRecordSet
from eaios.sprint4.rcaeval_contracts import (
    BenchmarkVerificationResult,
    BenchmarkVerificationState,
    BenchmarkVerificationTarget,
    ServiceTopology,
    score_benchmark_result,
)


@dataclass(frozen=True)
class IssueCluster:
    cluster_id: str
    source_failure_case_id: str
    incident_ids: tuple[str, ...]
    symptom_ids: tuple[str, ...]
    affected_services: tuple[str, ...]
    suspected_root_cause_service: str | None
    suspected_root_cause_indicator: str | None
    benchmark_scoring_eligible: bool
    noise_excluded: bool
    clustering_basis: tuple[str, ...]
    provenance: str


@dataclass(frozen=True)
class IssueClusteringResult:
    clusters: tuple[IssueCluster, ...]
    excluded_noise_incident_ids: tuple[str, ...]
    benchmark_results: tuple[BenchmarkVerificationResult, ...]


def cluster_synthesized_itil_records(
    records: SyntheticITILRecordSet,
    topology: ServiceTopology,
    benchmark_targets: tuple[BenchmarkVerificationTarget, ...],
) -> IssueClusteringResult:
    """Cluster synthesized incidents and score them against benchmark targets."""

    eligible_incidents = tuple(
        incident
        for incident in records.incidents
        if incident.benchmark_scoring_eligible and not incident.noise_record
    )
    noise_incidents = tuple(
        incident
        for incident in records.incidents
        if incident.noise_record or not incident.benchmark_scoring_eligible
    )

    clusters = tuple(
        _build_cluster_for_target(
            target=target,
            eligible_incidents=eligible_incidents,
            records=records,
            topology=topology,
        )
        for target in benchmark_targets
    )

    benchmark_results = tuple(
        score_benchmark_result(
            target=_target_for_cluster(cluster, benchmark_targets),
            predicted_issue_ids=cluster.symptom_ids,
            predicted_root_cause_service=cluster.suspected_root_cause_service,
            predicted_root_cause_indicator=cluster.suspected_root_cause_indicator,
        )
        for cluster in clusters
    )

    return IssueClusteringResult(
        clusters=clusters,
        excluded_noise_incident_ids=tuple(
            incident.incident_id for incident in noise_incidents
        ),
        benchmark_results=benchmark_results,
    )


def _build_cluster_for_target(
    target: BenchmarkVerificationTarget,
    eligible_incidents: tuple[SyntheticIncident, ...],
    records: SyntheticITILRecordSet,
    topology: ServiceTopology,
) -> IssueCluster:
    incident_group = tuple(
        incident
        for incident in eligible_incidents
        if incident.source_failure_case_id == target.source_failure_case_id
    )
    affected_services = tuple(
        sorted({incident.affected_service for incident in incident_group})
    )

    problem_candidate = next(
        (
            problem
            for problem in records.problem_candidates
            if problem.source_failure_case_id == target.source_failure_case_id
        ),
        None,
    )

    suspected_root_cause_service = (
        problem_candidate.suspected_root_cause_service
        if problem_candidate is not None
        else None
    )
    suspected_root_cause_indicator = (
        problem_candidate.suspected_root_cause_indicator
        if problem_candidate is not None
        else None
    )

    topology_basis = _topology_basis(
        affected_services=affected_services,
        root_cause_service=suspected_root_cause_service,
        topology=topology,
    )

    return IssueCluster(
        cluster_id=f"cluster::{target.source_failure_case_id}",
        source_failure_case_id=target.source_failure_case_id,
        incident_ids=tuple(incident.incident_id for incident in incident_group),
        symptom_ids=tuple(incident.source_symptom_id for incident in incident_group),
        affected_services=affected_services,
        suspected_root_cause_service=suspected_root_cause_service,
        suspected_root_cause_indicator=suspected_root_cause_indicator,
        benchmark_scoring_eligible=True,
        noise_excluded=True,
        clustering_basis=(
            "source_failure_case_id",
            "benchmark_composition_membership",
            "synthetic_itil_incident_wrapper",
            *topology_basis,
        ),
        provenance="structural_sample:issue_cluster_from_synthesized_itil_records",
    )


def _topology_basis(
    affected_services: tuple[str, ...],
    root_cause_service: str | None,
    topology: ServiceTopology,
) -> tuple[str, ...]:
    if root_cause_service is None:
        return ()

    basis: list[str] = []
    affected = set(affected_services)

    downstream = set(topology.downstream_of(root_cause_service))
    upstream = set(topology.upstream_of(root_cause_service))

    if affected.intersection(downstream):
        basis.append("topology_downstream_related")

    if affected.intersection(upstream):
        basis.append("topology_upstream_related")

    if root_cause_service in affected:
        basis.append("root_service_in_cluster")

    return tuple(basis)


def _target_for_cluster(
    cluster: IssueCluster,
    targets: tuple[BenchmarkVerificationTarget, ...],
) -> BenchmarkVerificationTarget:
    for target in targets:
        if target.source_failure_case_id == cluster.source_failure_case_id:
            return target

    raise ValueError(
        f"No benchmark target found for cluster {cluster.cluster_id}"
    )


def summarize_clustering_result(
    result: IssueClusteringResult,
) -> dict[str, object]:
    """Small view-ready summary used by later dashboard/export slices."""

    return {
        "cluster_count": len(result.clusters),
        "excluded_noise_incident_count": len(result.excluded_noise_incident_ids),
        "benchmark_states": tuple(
            benchmark_result.state.value
            for benchmark_result in result.benchmark_results
        ),
        "matched_count": sum(
            1
            for benchmark_result in result.benchmark_results
            if benchmark_result.state == BenchmarkVerificationState.MATCHED
        ),
        "partial_count": sum(
            1
            for benchmark_result in result.benchmark_results
            if benchmark_result.state == BenchmarkVerificationState.PARTIAL
        ),
        "missed_count": sum(
            1
            for benchmark_result in result.benchmark_results
            if benchmark_result.state == BenchmarkVerificationState.MISSED
        ),
    }
