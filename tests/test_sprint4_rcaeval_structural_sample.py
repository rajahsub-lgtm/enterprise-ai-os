from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint4.rcaeval_contracts import (
    BenchmarkVerificationState,
    SignalType,
    build_benchmark_targets,
    load_structural_sample,
    score_benchmark_result,
)


SAMPLE = Path(
    "data/domain/it_application_health/rcaeval_train_ticket_structural_sample.json"
)


def test_structural_sample_exists_and_is_not_copied_benchmark_data():
    sample = load_structural_sample(SAMPLE)

    assert sample.copied_from_rcaeval is False
    assert sample.raw_benchmark_data is False


def test_structural_sample_loads_fault_scenarios_and_topology():
    sample = load_structural_sample(SAMPLE)

    assert sample.composition_scenario_id == "composition-structural-001"
    assert len(sample.fault_scenarios) == 2
    assert "checkout-service" in sample.service_topology.services
    assert "payment-service" in sample.service_topology.services
    assert sample.service_topology.downstream_of("checkout-service") == (
        "payment-service",
        "order-service",
    )


def test_fault_symptoms_preserve_source_failure_case_id_for_cluster_truth():
    sample = load_structural_sample(SAMPLE)

    for fault in sample.fault_scenarios:
        assert fault.telemetry_symptoms
        assert {
            symptom.source_failure_case_id
            for symptom in fault.telemetry_symptoms
        } == {fault.failure_case_id}
        assert all(
            symptom.benchmark_scoring_eligible is True
            for symptom in fault.telemetry_symptoms
        )
        assert all(
            symptom.noise_record is False
            for symptom in fault.telemetry_symptoms
        )


def test_noise_symptoms_are_not_benchmark_scorable():
    sample = load_structural_sample(SAMPLE)

    assert len(sample.noise_symptoms) == 1
    noise = sample.noise_symptoms[0]

    assert noise.noise_record is True
    assert noise.benchmark_scoring_eligible is False
    assert noise.source_failure_case_id is None


def test_signal_types_are_explicit_metric_log_or_trace():
    sample = load_structural_sample(SAMPLE)

    all_symptoms = tuple(
        symptom
        for fault in sample.fault_scenarios
        for symptom in fault.telemetry_symptoms
    ) + sample.noise_symptoms

    assert {symptom.signal_type for symptom in all_symptoms} >= {
        SignalType.METRIC,
        SignalType.LOG,
        SignalType.TRACE,
    }


def test_benchmark_targets_derive_cluster_membership_from_composition():
    sample = load_structural_sample(SAMPLE)

    targets = build_benchmark_targets(sample)

    assert len(targets) == 2
    for target in targets:
        assert target.source_failure_case_id.startswith("structural-failure-")
        assert target.expected_issue_ids
        assert target.expected_root_cause_service
        assert target.expected_root_cause_indicator
        assert target.noise_issue_ids == (
            "symptom-notification-background-retry",
        )


def test_benchmark_score_matches_when_cluster_and_root_cause_match():
    sample = load_structural_sample(SAMPLE)
    target = build_benchmark_targets(sample)[0]

    result = score_benchmark_result(
        target=target,
        predicted_issue_ids=target.expected_issue_ids,
        predicted_root_cause_service=target.expected_root_cause_service,
        predicted_root_cause_indicator=target.expected_root_cause_indicator,
    )

    assert result.state == BenchmarkVerificationState.MATCHED
    assert result.missed_issue_ids == ()
    assert result.noise_excluded is True


def test_benchmark_score_partial_when_noise_included_or_indicator_missed():
    sample = load_structural_sample(SAMPLE)
    target = build_benchmark_targets(sample)[0]

    result = score_benchmark_result(
        target=target,
        predicted_issue_ids=target.expected_issue_ids + target.noise_issue_ids,
        predicted_root_cause_service=target.expected_root_cause_service,
        predicted_root_cause_indicator="wrong_indicator",
    )

    assert result.state == BenchmarkVerificationState.PARTIAL
    assert result.noise_excluded is False
    assert result.matched_issue_ids


def test_benchmark_score_missed_when_nothing_matches():
    sample = load_structural_sample(SAMPLE)
    target = build_benchmark_targets(sample)[0]

    result = score_benchmark_result(
        target=target,
        predicted_issue_ids=("unrelated-symptom",),
        predicted_root_cause_service="unrelated-service",
        predicted_root_cause_indicator="unrelated_indicator",
    )

    assert result.state == BenchmarkVerificationState.MISSED
    assert result.matched_issue_ids == ()
