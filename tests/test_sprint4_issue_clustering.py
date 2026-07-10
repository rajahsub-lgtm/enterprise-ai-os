from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint4.issue_clustering import (
    cluster_synthesized_itil_records,
    summarize_clustering_result,
)
from eaios.sprint4.itil_synthesizer import synthesize_itil_records
from eaios.sprint4.rcaeval_contracts import (
    BenchmarkVerificationState,
    build_benchmark_targets,
    load_structural_sample,
)


SAMPLE = Path(
    "data/domain/it_application_health/rcaeval_train_ticket_structural_sample.json"
)


def _cluster_result():
    sample = load_structural_sample(SAMPLE)
    records = synthesize_itil_records(sample)
    targets = build_benchmark_targets(sample)

    return cluster_synthesized_itil_records(
        records=records,
        topology=sample.service_topology,
        benchmark_targets=targets,
    )


def test_issue_clustering_creates_one_cluster_per_benchmark_target():
    result = _cluster_result()

    assert len(result.clusters) == 2
    assert {
        cluster.source_failure_case_id for cluster in result.clusters
    } == {
        "structural-failure-payment-latency-001",
        "structural-failure-inventory-errors-001",
    }


def test_issue_clustering_groups_incidents_by_source_failure_case_id():
    result = _cluster_result()

    clusters_by_failure = {
        cluster.source_failure_case_id: cluster
        for cluster in result.clusters
    }

    payment_cluster = clusters_by_failure[
        "structural-failure-payment-latency-001"
    ]
    inventory_cluster = clusters_by_failure[
        "structural-failure-inventory-errors-001"
    ]

    assert set(payment_cluster.symptom_ids) == {
        "symptom-payment-p95-latency",
        "symptom-checkout-errors",
        "symptom-order-timeouts",
    }
    assert set(inventory_cluster.symptom_ids) == {
        "symptom-inventory-db-errors",
        "symptom-route-planning-degraded",
    }


def test_issue_clustering_excludes_noise_incidents():
    result = _cluster_result()

    assert result.excluded_noise_incident_ids == (
        "incident::symptom-notification-background-retry",
    )

    all_cluster_incidents = {
        incident_id
        for cluster in result.clusters
        for incident_id in cluster.incident_ids
    }

    assert "incident::symptom-notification-background-retry" not in all_cluster_incidents


def test_issue_clustering_preserves_root_cause_target_from_problem_candidate():
    result = _cluster_result()

    clusters_by_failure = {
        cluster.source_failure_case_id: cluster
        for cluster in result.clusters
    }

    assert (
        clusters_by_failure[
            "structural-failure-payment-latency-001"
        ].suspected_root_cause_service
        == "payment-service"
    )
    assert (
        clusters_by_failure[
            "structural-failure-payment-latency-001"
        ].suspected_root_cause_indicator
        == "latency_p95_ms"
    )

    assert (
        clusters_by_failure[
            "structural-failure-inventory-errors-001"
        ].suspected_root_cause_service
        == "inventory-service"
    )
    assert (
        clusters_by_failure[
            "structural-failure-inventory-errors-001"
        ].suspected_root_cause_indicator
        == "db_connection_errors"
    )


def test_issue_clustering_records_topology_and_composition_basis():
    result = _cluster_result()

    for cluster in result.clusters:
        assert "source_failure_case_id" in cluster.clustering_basis
        assert "benchmark_composition_membership" in cluster.clustering_basis
        assert "synthetic_itil_incident_wrapper" in cluster.clustering_basis
        assert "root_service_in_cluster" in cluster.clustering_basis


def test_issue_clustering_scores_all_structural_clusters_as_matched():
    result = _cluster_result()

    assert len(result.benchmark_results) == 2
    assert {
        benchmark_result.state
        for benchmark_result in result.benchmark_results
    } == {BenchmarkVerificationState.MATCHED}

    assert all(
        benchmark_result.noise_excluded is True
        for benchmark_result in result.benchmark_results
    )
    assert all(
        benchmark_result.missed_issue_ids == ()
        for benchmark_result in result.benchmark_results
    )


def test_issue_clustering_result_is_view_ready_summary():
    result = _cluster_result()

    summary = summarize_clustering_result(result)

    assert summary == {
        "cluster_count": 2,
        "excluded_noise_incident_count": 1,
        "benchmark_states": ("MATCHED", "MATCHED"),
        "matched_count": 2,
        "partial_count": 0,
        "missed_count": 0,
    }


def test_issue_clustering_does_not_use_knowledge_base_as_answer_key():
    source = Path("src/eaios/sprint4/issue_clustering.py").read_text(
        encoding="utf-8"
    )

    assert "SyntheticKnowledgeArticle" not in source
    assert "from eaios.sprint4.knowledge" not in source
    assert "import eaios.sprint4.knowledge" not in source
    assert "source_failure_case_id" in source
    assert "BenchmarkVerificationTarget" in source