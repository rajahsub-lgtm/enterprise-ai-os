from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint4.itil_synthesizer import (
    HealthState,
    IncidentPriority,
    synthesize_itil_records,
)
from eaios.sprint4.rcaeval_contracts import (
    build_benchmark_targets,
    load_structural_sample,
)


SAMPLE = Path(
    "data/domain/it_application_health/rcaeval_train_ticket_structural_sample.json"
)


def test_itil_synthesizer_creates_alerts_and_incidents_for_all_symptoms():
    sample = load_structural_sample(SAMPLE)

    records = synthesize_itil_records(sample)

    benchmark_symptom_count = sum(
        len(fault.telemetry_symptoms) for fault in sample.fault_scenarios
    )
    expected_count = benchmark_symptom_count + len(sample.noise_symptoms)

    assert len(records.alerts) == expected_count
    assert len(records.incidents) == expected_count


def test_synthesized_alerts_preserve_benchmark_source_failure_case_ids():
    sample = load_structural_sample(SAMPLE)

    records = synthesize_itil_records(sample)

    benchmark_alerts = [
        alert for alert in records.alerts if alert.benchmark_scoring_eligible
    ]

    assert benchmark_alerts
    assert all(alert.source_failure_case_id for alert in benchmark_alerts)
    assert all(alert.provenance == "structural_sample:telemetry_symptom" for alert in benchmark_alerts)


def test_synthesized_noise_alert_is_not_benchmark_scorable():
    sample = load_structural_sample(SAMPLE)

    records = synthesize_itil_records(sample)

    noise_alerts = [alert for alert in records.alerts if alert.noise_record]

    assert len(noise_alerts) == 1
    assert noise_alerts[0].benchmark_scoring_eligible is False
    assert noise_alerts[0].source_failure_case_id is None


def test_incidents_preserve_human_approval_and_no_autonomous_action_boundary():
    sample = load_structural_sample(SAMPLE)

    records = synthesize_itil_records(sample)

    assert records.incidents
    assert all(incident.human_approval_required is True for incident in records.incidents)
    assert all(incident.autonomous_action_allowed is False for incident in records.incidents)


def test_incident_priority_is_derived_from_severity_and_noise():
    sample = load_structural_sample(SAMPLE)

    records = synthesize_itil_records(sample)

    high_incidents = [
        incident for incident in records.incidents
        if incident.source_symptom_id in {
            "symptom-payment-p95-latency",
            "symptom-checkout-errors",
            "symptom-inventory-db-errors",
        }
    ]
    noise_incident = next(
        incident for incident in records.incidents if incident.noise_record
    )

    assert all(incident.priority == IncidentPriority.P1 for incident in high_incidents)
    assert noise_incident.priority == IncidentPriority.P4


def test_problem_candidates_group_incidents_by_source_failure_case_id():
    sample = load_structural_sample(SAMPLE)

    records = synthesize_itil_records(sample)
    targets = build_benchmark_targets(sample)

    problems_by_failure = {
        problem.source_failure_case_id: problem
        for problem in records.problem_candidates
    }

    assert set(problems_by_failure) == {
        target.source_failure_case_id for target in targets
    }

    for target in targets:
        problem = problems_by_failure[target.source_failure_case_id]
        assert set(problem.candidate_symptom_ids) == set(target.expected_issue_ids)
        assert problem.suspected_root_cause_service == target.expected_root_cause_service
        assert problem.suspected_root_cause_indicator == target.expected_root_cause_indicator


def test_problem_candidates_exclude_noise_records():
    sample = load_structural_sample(SAMPLE)

    records = synthesize_itil_records(sample)

    all_problem_symptoms = {
        symptom_id
        for problem in records.problem_candidates
        for symptom_id in problem.candidate_symptom_ids
    }

    assert "symptom-notification-background-retry" not in all_problem_symptoms


def test_change_contexts_are_derived_from_fault_scenarios_not_remediation_actions():
    sample = load_structural_sample(SAMPLE)

    records = synthesize_itil_records(sample)

    assert len(records.change_contexts) == len(sample.fault_scenarios)
    assert all(
        change.change_category == "benchmark_fault_context"
        for change in records.change_contexts
    )
    assert all(change.human_approval_required is True for change in records.change_contexts)
    assert all(change.autonomous_action_allowed is False for change in records.change_contexts)


def test_application_health_snapshots_are_derived_from_active_alerts():
    sample = load_structural_sample(SAMPLE)

    records = synthesize_itil_records(sample)

    snapshots_by_service = {
        snapshot.service_id: snapshot
        for snapshot in records.health_snapshots
    }

    assert snapshots_by_service["payment-service"].health_state == HealthState.CRITICAL
    assert snapshots_by_service["route-planning-service"].health_state == HealthState.DEGRADED
    assert snapshots_by_service["notification-service"].health_state == HealthState.NOISE


def test_application_health_snapshots_preserve_benchmark_eligibility():
    sample = load_structural_sample(SAMPLE)

    records = synthesize_itil_records(sample)

    payment = next(
        snapshot for snapshot in records.health_snapshots
        if snapshot.service_id == "payment-service"
    )
    notification = next(
        snapshot for snapshot in records.health_snapshots
        if snapshot.service_id == "notification-service"
    )

    assert payment.benchmark_scoring_eligible is True
    assert payment.source_failure_case_ids == (
        "structural-failure-payment-latency-001",
    )

    assert notification.benchmark_scoring_eligible is False
    assert notification.noise_record is True
    assert notification.source_failure_case_ids == ()
