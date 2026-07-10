from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint4.application_health_observation import (
    build_application_health_observation_snapshot,
    to_view_model,
)


def _snapshot():
    return build_application_health_observation_snapshot()


def test_application_health_observation_builds_end_to_end_snapshot():
    snapshot = _snapshot()

    assert snapshot.snapshot_id == "application-health::composition-structural-001"
    assert snapshot.composition_scenario_id == "composition-structural-001"
    assert snapshot.source_dataset_role == "benchmark_truth_layer_structural_sample"
    assert snapshot.provenance == "structural_sample:application_health_observation_snapshot"


def test_application_health_observation_does_not_contain_copied_or_raw_benchmark_data():
    snapshot = _snapshot()

    assert snapshot.copied_from_rcaeval is False
    assert snapshot.raw_benchmark_data is False
    assert "data/domain/it_application_health/" in snapshot.sample_path
    assert "data/domain/app_health/" not in snapshot.sample_path


def test_application_health_observation_counts_pipeline_outputs():
    snapshot = _snapshot()

    assert snapshot.counts == {
        "fault_scenarios": 2,
        "services": 6,
        "alerts": 6,
        "incidents": 6,
        "problem_candidates": 2,
        "change_contexts": 2,
        "health_snapshots": 6,
        "clusters": 2,
        "benchmark_results": 2,
        "excluded_noise_incidents": 1,
    }


def test_application_health_observation_includes_service_health_states():
    snapshot = _snapshot()

    service_states = {
        service.service_id: service.health_state
        for service in snapshot.service_health
    }

    assert service_states["payment-service"] == "CRITICAL"
    assert service_states["checkout-service"] == "CRITICAL"
    assert service_states["route-planning-service"] == "DEGRADED"
    assert service_states["notification-service"] == "NOISE"


def test_application_health_observation_preserves_source_failure_case_ids():
    snapshot = _snapshot()

    payment = next(
        service for service in snapshot.service_health
        if service.service_id == "payment-service"
    )
    notification = next(
        service for service in snapshot.service_health
        if service.service_id == "notification-service"
    )

    assert payment.source_failure_case_ids == (
        "structural-failure-payment-latency-001",
    )
    assert payment.benchmark_scoring_eligible is True

    assert notification.source_failure_case_ids == ()
    assert notification.benchmark_scoring_eligible is False
    assert notification.noise_record is True


def test_application_health_observation_clusters_are_benchmark_eligible_and_noise_excluded():
    snapshot = _snapshot()

    assert len(snapshot.clusters) == 2
    assert all(cluster.benchmark_scoring_eligible is True for cluster in snapshot.clusters)
    assert all(cluster.noise_excluded is True for cluster in snapshot.clusters)
    assert {
        cluster.source_failure_case_id for cluster in snapshot.clusters
    } == {
        "structural-failure-payment-latency-001",
        "structural-failure-inventory-errors-001",
    }


def test_application_health_observation_benchmark_results_match_structural_targets():
    snapshot = _snapshot()

    assert len(snapshot.benchmark_results) == 2
    assert {result.state for result in snapshot.benchmark_results} == {"MATCHED"}
    assert all(result.missed_issue_ids == () for result in snapshot.benchmark_results)
    assert all(result.noise_excluded is True for result in snapshot.benchmark_results)


def test_application_health_observation_summary_is_dashboard_ready():
    snapshot = _snapshot()

    assert snapshot.clustering_summary == {
        "cluster_count": 2,
        "excluded_noise_incident_count": 1,
        "benchmark_states": ("MATCHED", "MATCHED"),
        "matched_count": 2,
        "partial_count": 0,
        "missed_count": 0,
    }


def test_application_health_observation_declares_governance_boundaries():
    snapshot = _snapshot()

    assert "human_approval_required" in snapshot.governance_boundaries
    assert "autonomous_action_disabled" in snapshot.governance_boundaries
    assert "benchmark_truth_external" in snapshot.governance_boundaries
    assert "composition_based_cluster_truth" in snapshot.governance_boundaries
    assert "noise_excluded_from_benchmark_scoring" in snapshot.governance_boundaries
    assert "kb_not_answer_key" in snapshot.governance_boundaries


def test_application_health_observation_view_model_is_json_serializable():
    snapshot = _snapshot()

    view_model = to_view_model(snapshot)
    serialized = json.dumps(view_model, indent=2)

    assert "application-health::composition-structural-001" in serialized
    assert "MATCHED" in serialized
    assert "payment-service" in serialized
    assert "kb_not_answer_key" in serialized


def test_application_health_observation_view_model_uses_primitives():
    snapshot = _snapshot()

    view_model = to_view_model(snapshot)

    assert isinstance(view_model["service_health"], list)
    assert isinstance(view_model["clusters"], list)
    assert isinstance(view_model["benchmark_results"], list)
    assert isinstance(view_model["governance_boundaries"], list)
    assert isinstance(
        view_model["clusters"][0]["affected_services"],
        list,
    )
