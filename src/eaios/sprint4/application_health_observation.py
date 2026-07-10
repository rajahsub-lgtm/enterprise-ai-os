"""Sprint 4 application health observation adapter.

Classification: EAIOS Sprint 4 stable adapter output.

This module creates the 4A end-to-end observation snapshot:

structural Train Ticket sample
-> benchmark targets
-> synthesized ITIL records
-> application health snapshots
-> issue clusters
-> benchmark verification results
-> dashboard/export-ready view model

The adapter preserves Sprint 4 governance boundaries:
- benchmark truth remains external/composition-based
- KB content is not used as answer key
- noise is excluded from benchmark scoring
- human approval remains required
- autonomous action remains disabled
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from eaios.sprint4.issue_clustering import (
    cluster_synthesized_itil_records,
    summarize_clustering_result,
)
from eaios.sprint4.itil_synthesizer import synthesize_itil_records
from eaios.sprint4.rcaeval_contracts import (
    build_benchmark_targets,
    load_structural_sample,
)


DEFAULT_STRUCTURAL_SAMPLE_PATH = Path(
    "data/domain/it_application_health/rcaeval_train_ticket_structural_sample.json"
)


@dataclass(frozen=True)
class ServiceHealthObservation:
    service_id: str
    health_state: str
    active_alert_count: int
    active_incident_count: int
    source_failure_case_ids: tuple[str, ...]
    benchmark_scoring_eligible: bool
    noise_record: bool


@dataclass(frozen=True)
class ClusterObservation:
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


@dataclass(frozen=True)
class BenchmarkResultObservation:
    source_failure_case_id: str
    state: str
    expected_issue_ids: tuple[str, ...]
    predicted_issue_ids: tuple[str, ...]
    matched_issue_ids: tuple[str, ...]
    missed_issue_ids: tuple[str, ...]
    expected_root_cause_service: str
    predicted_root_cause_service: str | None
    expected_root_cause_indicator: str
    predicted_root_cause_indicator: str | None
    noise_excluded: bool
    comparison_note: str


@dataclass(frozen=True)
class ApplicationHealthObservationSnapshot:
    snapshot_id: str
    composition_scenario_id: str
    source_dataset_role: str
    sample_path: str
    copied_from_rcaeval: bool
    raw_benchmark_data: bool
    counts: dict[str, int]
    service_health: tuple[ServiceHealthObservation, ...]
    clusters: tuple[ClusterObservation, ...]
    benchmark_results: tuple[BenchmarkResultObservation, ...]
    clustering_summary: dict[str, object]
    governance_boundaries: tuple[str, ...]
    provenance: str


def build_application_health_observation_snapshot(
    sample_path: str | Path = DEFAULT_STRUCTURAL_SAMPLE_PATH,
) -> ApplicationHealthObservationSnapshot:
    sample = load_structural_sample(sample_path)
    targets = build_benchmark_targets(sample)
    records = synthesize_itil_records(sample)
    clustering_result = cluster_synthesized_itil_records(
        records=records,
        topology=sample.service_topology,
        benchmark_targets=targets,
    )

    _assert_governance_boundaries(records)

    service_health = tuple(
        ServiceHealthObservation(
            service_id=snapshot.service_id,
            health_state=snapshot.health_state.value,
            active_alert_count=len(snapshot.active_alert_ids),
            active_incident_count=len(snapshot.active_incident_ids),
            source_failure_case_ids=snapshot.source_failure_case_ids,
            benchmark_scoring_eligible=snapshot.benchmark_scoring_eligible,
            noise_record=snapshot.noise_record,
        )
        for snapshot in sorted(
            records.health_snapshots,
            key=lambda item: item.service_id,
        )
    )

    clusters = tuple(
        ClusterObservation(
            cluster_id=cluster.cluster_id,
            source_failure_case_id=cluster.source_failure_case_id,
            incident_ids=cluster.incident_ids,
            symptom_ids=cluster.symptom_ids,
            affected_services=cluster.affected_services,
            suspected_root_cause_service=cluster.suspected_root_cause_service,
            suspected_root_cause_indicator=cluster.suspected_root_cause_indicator,
            benchmark_scoring_eligible=cluster.benchmark_scoring_eligible,
            noise_excluded=cluster.noise_excluded,
            clustering_basis=cluster.clustering_basis,
        )
        for cluster in clustering_result.clusters
    )

    benchmark_results = tuple(
        BenchmarkResultObservation(
            source_failure_case_id=result.target.source_failure_case_id,
            state=result.state.value,
            expected_issue_ids=result.target.expected_issue_ids,
            predicted_issue_ids=result.predicted_issue_ids,
            matched_issue_ids=result.matched_issue_ids,
            missed_issue_ids=result.missed_issue_ids,
            expected_root_cause_service=result.target.expected_root_cause_service,
            predicted_root_cause_service=result.predicted_root_cause_service,
            expected_root_cause_indicator=result.target.expected_root_cause_indicator,
            predicted_root_cause_indicator=result.predicted_root_cause_indicator,
            noise_excluded=result.noise_excluded,
            comparison_note=result.comparison_note,
        )
        for result in clustering_result.benchmark_results
    )

    return ApplicationHealthObservationSnapshot(
        snapshot_id=f"application-health::{sample.composition_scenario_id}",
        composition_scenario_id=sample.composition_scenario_id,
        source_dataset_role="benchmark_truth_layer_structural_sample",
        sample_path=Path(sample_path).as_posix(),
        copied_from_rcaeval=sample.copied_from_rcaeval,
        raw_benchmark_data=sample.raw_benchmark_data,
        counts={
            "fault_scenarios": len(sample.fault_scenarios),
            "services": len(sample.service_topology.services),
            "alerts": len(records.alerts),
            "incidents": len(records.incidents),
            "problem_candidates": len(records.problem_candidates),
            "change_contexts": len(records.change_contexts),
            "health_snapshots": len(records.health_snapshots),
            "clusters": len(clustering_result.clusters),
            "benchmark_results": len(clustering_result.benchmark_results),
            "excluded_noise_incidents": len(
                clustering_result.excluded_noise_incident_ids
            ),
        },
        service_health=service_health,
        clusters=clusters,
        benchmark_results=benchmark_results,
        clustering_summary=summarize_clustering_result(clustering_result),
        governance_boundaries=(
            "human_approval_required",
            "autonomous_action_disabled",
            "benchmark_truth_external",
            "composition_based_cluster_truth",
            "noise_excluded_from_benchmark_scoring",
            "kb_not_answer_key",
        ),
        provenance="structural_sample:application_health_observation_snapshot",
    )


def to_view_model(
    snapshot: ApplicationHealthObservationSnapshot,
) -> dict[str, Any]:
    """Return a JSON/dashboard-ready primitive view model."""

    return {
        "snapshot_id": snapshot.snapshot_id,
        "composition_scenario_id": snapshot.composition_scenario_id,
        "source_dataset_role": snapshot.source_dataset_role,
        "sample_path": snapshot.sample_path,
        "copied_from_rcaeval": snapshot.copied_from_rcaeval,
        "raw_benchmark_data": snapshot.raw_benchmark_data,
        "counts": snapshot.counts,
        "service_health": [
            {
                "service_id": service.service_id,
                "health_state": service.health_state,
                "active_alert_count": service.active_alert_count,
                "active_incident_count": service.active_incident_count,
                "source_failure_case_ids": list(service.source_failure_case_ids),
                "benchmark_scoring_eligible": service.benchmark_scoring_eligible,
                "noise_record": service.noise_record,
            }
            for service in snapshot.service_health
        ],
        "clusters": [
            {
                "cluster_id": cluster.cluster_id,
                "source_failure_case_id": cluster.source_failure_case_id,
                "incident_ids": list(cluster.incident_ids),
                "symptom_ids": list(cluster.symptom_ids),
                "affected_services": list(cluster.affected_services),
                "suspected_root_cause_service": (
                    cluster.suspected_root_cause_service
                ),
                "suspected_root_cause_indicator": (
                    cluster.suspected_root_cause_indicator
                ),
                "benchmark_scoring_eligible": cluster.benchmark_scoring_eligible,
                "noise_excluded": cluster.noise_excluded,
                "clustering_basis": list(cluster.clustering_basis),
            }
            for cluster in snapshot.clusters
        ],
        "benchmark_results": [
            {
                "source_failure_case_id": result.source_failure_case_id,
                "state": result.state,
                "expected_issue_ids": list(result.expected_issue_ids),
                "predicted_issue_ids": list(result.predicted_issue_ids),
                "matched_issue_ids": list(result.matched_issue_ids),
                "missed_issue_ids": list(result.missed_issue_ids),
                "expected_root_cause_service": result.expected_root_cause_service,
                "predicted_root_cause_service": result.predicted_root_cause_service,
                "expected_root_cause_indicator": (
                    result.expected_root_cause_indicator
                ),
                "predicted_root_cause_indicator": (
                    result.predicted_root_cause_indicator
                ),
                "noise_excluded": result.noise_excluded,
                "comparison_note": result.comparison_note,
            }
            for result in snapshot.benchmark_results
        ],
        "clustering_summary": snapshot.clustering_summary,
        "governance_boundaries": list(snapshot.governance_boundaries),
        "provenance": snapshot.provenance,
    }


def _assert_governance_boundaries(records: Any) -> None:
    if any(
        incident.human_approval_required is not True
        for incident in records.incidents
    ):
        raise ValueError("All synthesized incidents must require human approval.")

    if any(
        incident.autonomous_action_allowed is not False
        for incident in records.incidents
    ):
        raise ValueError("Autonomous action must remain disabled.")

    if any(
        change.autonomous_action_allowed is not False
        for change in records.change_contexts
    ):
        raise ValueError("Change contexts must not allow autonomous action.")
