"""Sprint 4 ITIL record synthesizer.

Classification: EAIOS Sprint 4 domain adapter.

This module maps benchmark-derived Train Ticket structural symptoms into
governed ITIL-style records. It does not create benchmark truth. It preserves
source_failure_case_id and benchmark_scoring_eligible so verification remains
external/composition-based.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from eaios.sprint4.rcaeval_contracts import (
    StructuralSample,
    TelemetrySymptom,
    TrainTicketFaultScenario,
)


class SyntheticRecordType(str, Enum):
    ALERT = "SyntheticAlert"
    INCIDENT = "SyntheticIncident"
    PROBLEM_CANDIDATE = "SyntheticProblemCandidate"
    CHANGE_CONTEXT = "SyntheticChangeContext"
    APPLICATION_HEALTH_SNAPSHOT = "ApplicationHealthSnapshot"


class IncidentPriority(str, Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


class HealthState(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    CRITICAL = "CRITICAL"
    NOISE = "NOISE"


@dataclass(frozen=True)
class SyntheticAlert:
    alert_id: str
    source_symptom_id: str
    affected_service: str
    indicator: str
    signal_type: str
    severity: str
    observed_value: float
    baseline_value: float
    source_failure_case_id: str | None
    benchmark_scoring_eligible: bool
    noise_record: bool
    provenance: str


@dataclass(frozen=True)
class SyntheticIncident:
    incident_id: str
    source_alert_id: str
    source_symptom_id: str
    short_description: str
    affected_service: str
    priority: IncidentPriority
    impact: str
    urgency: str
    assignment_group: str
    source_failure_case_id: str | None
    benchmark_scoring_eligible: bool
    noise_record: bool
    human_approval_required: bool
    autonomous_action_allowed: bool
    provenance: str


@dataclass(frozen=True)
class SyntheticProblemCandidate:
    problem_candidate_id: str
    source_failure_case_id: str
    candidate_incident_ids: tuple[str, ...]
    candidate_symptom_ids: tuple[str, ...]
    suspected_root_cause_service: str
    suspected_root_cause_indicator: str
    benchmark_scoring_eligible: bool
    provenance: str


@dataclass(frozen=True)
class SyntheticChangeContext:
    change_context_id: str
    source_failure_case_id: str
    affected_services: tuple[str, ...]
    fault_type: str
    change_category: str
    human_approval_required: bool
    autonomous_action_allowed: bool
    provenance: str


@dataclass(frozen=True)
class ApplicationHealthSnapshot:
    snapshot_id: str
    service_id: str
    health_state: HealthState
    active_alert_ids: tuple[str, ...]
    active_incident_ids: tuple[str, ...]
    source_failure_case_ids: tuple[str, ...]
    noise_record: bool
    benchmark_scoring_eligible: bool
    provenance: str


@dataclass(frozen=True)
class SyntheticITILRecordSet:
    alerts: tuple[SyntheticAlert, ...]
    incidents: tuple[SyntheticIncident, ...]
    problem_candidates: tuple[SyntheticProblemCandidate, ...]
    change_contexts: tuple[SyntheticChangeContext, ...]
    health_snapshots: tuple[ApplicationHealthSnapshot, ...]


def synthesize_itil_records(sample: StructuralSample) -> SyntheticITILRecordSet:
    alerts = tuple(
        _build_alert(symptom)
        for symptom in _all_symptoms(sample)
    )
    incidents = tuple(
        _build_incident(alert)
        for alert in alerts
    )
    problem_candidates = tuple(
        _build_problem_candidate(fault, incidents)
        for fault in sample.fault_scenarios
    )
    change_contexts = tuple(
        _build_change_context(fault)
        for fault in sample.fault_scenarios
    )
    health_snapshots = _build_health_snapshots(alerts, incidents)

    return SyntheticITILRecordSet(
        alerts=alerts,
        incidents=incidents,
        problem_candidates=problem_candidates,
        change_contexts=change_contexts,
        health_snapshots=health_snapshots,
    )


def _all_symptoms(sample: StructuralSample) -> tuple[TelemetrySymptom, ...]:
    benchmark_symptoms = tuple(
        symptom
        for fault in sample.fault_scenarios
        for symptom in fault.telemetry_symptoms
    )

    return benchmark_symptoms + sample.noise_symptoms


def _build_alert(symptom: TelemetrySymptom) -> SyntheticAlert:
    return SyntheticAlert(
        alert_id=f"alert::{symptom.symptom_id}",
        source_symptom_id=symptom.symptom_id,
        affected_service=symptom.service,
        indicator=symptom.indicator,
        signal_type=symptom.signal_type.value,
        severity=symptom.severity,
        observed_value=symptom.observed_value,
        baseline_value=symptom.baseline_value,
        source_failure_case_id=symptom.source_failure_case_id,
        benchmark_scoring_eligible=symptom.benchmark_scoring_eligible,
        noise_record=symptom.noise_record,
        provenance="structural_sample:telemetry_symptom",
    )


def _build_incident(alert: SyntheticAlert) -> SyntheticIncident:
    return SyntheticIncident(
        incident_id=f"incident::{alert.source_symptom_id}",
        source_alert_id=alert.alert_id,
        source_symptom_id=alert.source_symptom_id,
        short_description=(
            f"{alert.affected_service} {alert.indicator} anomaly "
            f"from {alert.signal_type}"
        ),
        affected_service=alert.affected_service,
        priority=_priority_for_severity(alert.severity, alert.noise_record),
        impact=_impact_for_severity(alert.severity),
        urgency=_urgency_for_severity(alert.severity, alert.noise_record),
        assignment_group=f"{alert.affected_service}-support",
        source_failure_case_id=alert.source_failure_case_id,
        benchmark_scoring_eligible=alert.benchmark_scoring_eligible,
        noise_record=alert.noise_record,
        human_approval_required=True,
        autonomous_action_allowed=False,
        provenance="structural_sample:synthetic_incident_from_alert",
    )


def _build_problem_candidate(
    fault: TrainTicketFaultScenario,
    incidents: tuple[SyntheticIncident, ...],
) -> SyntheticProblemCandidate:
    candidate_incidents = tuple(
        incident
        for incident in incidents
        if incident.source_failure_case_id == fault.failure_case_id
        and incident.benchmark_scoring_eligible
        and not incident.noise_record
    )

    return SyntheticProblemCandidate(
        problem_candidate_id=f"problem-candidate::{fault.failure_case_id}",
        source_failure_case_id=fault.failure_case_id,
        candidate_incident_ids=tuple(
            incident.incident_id for incident in candidate_incidents
        ),
        candidate_symptom_ids=tuple(
            incident.source_symptom_id for incident in candidate_incidents
        ),
        suspected_root_cause_service=fault.root_cause_service,
        suspected_root_cause_indicator=fault.root_cause_indicator,
        benchmark_scoring_eligible=True,
        provenance="structural_sample:composition_based_problem_candidate",
    )


def _build_change_context(
    fault: TrainTicketFaultScenario,
) -> SyntheticChangeContext:
    return SyntheticChangeContext(
        change_context_id=f"change-context::{fault.failure_case_id}",
        source_failure_case_id=fault.failure_case_id,
        affected_services=fault.affected_services,
        fault_type=fault.fault_type,
        change_category="benchmark_fault_context",
        human_approval_required=True,
        autonomous_action_allowed=False,
        provenance="structural_sample:benchmark_fault_as_change_context",
    )


def _build_health_snapshots(
    alerts: tuple[SyntheticAlert, ...],
    incidents: tuple[SyntheticIncident, ...],
) -> tuple[ApplicationHealthSnapshot, ...]:
    services = sorted({alert.affected_service for alert in alerts})
    snapshots: list[ApplicationHealthSnapshot] = []

    for service_id in services:
        service_alerts = tuple(
            alert for alert in alerts if alert.affected_service == service_id
        )
        service_incidents = tuple(
            incident
            for incident in incidents
            if incident.affected_service == service_id
        )
        benchmark_alerts = tuple(
            alert for alert in service_alerts if alert.benchmark_scoring_eligible
        )
        noise_only = bool(service_alerts) and not bool(benchmark_alerts)

        snapshots.append(
            ApplicationHealthSnapshot(
                snapshot_id=f"health::{service_id}",
                service_id=service_id,
                health_state=_health_state_for_alerts(service_alerts),
                active_alert_ids=tuple(alert.alert_id for alert in service_alerts),
                active_incident_ids=tuple(
                    incident.incident_id for incident in service_incidents
                ),
                source_failure_case_ids=tuple(
                    sorted(
                        {
                            alert.source_failure_case_id
                            for alert in benchmark_alerts
                            if alert.source_failure_case_id is not None
                        }
                    )
                ),
                noise_record=noise_only,
                benchmark_scoring_eligible=bool(benchmark_alerts),
                provenance="structural_sample:derived_application_health",
            )
        )

    return tuple(snapshots)


def _priority_for_severity(
    severity: str,
    noise_record: bool,
) -> IncidentPriority:
    if noise_record:
        return IncidentPriority.P4
    if severity == "HIGH":
        return IncidentPriority.P1
    if severity == "MEDIUM":
        return IncidentPriority.P2
    if severity == "LOW":
        return IncidentPriority.P3
    return IncidentPriority.P4


def _impact_for_severity(severity: str) -> str:
    if severity == "HIGH":
        return "HIGH"
    if severity == "MEDIUM":
        return "MEDIUM"
    return "LOW"


def _urgency_for_severity(
    severity: str,
    noise_record: bool,
) -> str:
    if noise_record:
        return "LOW"
    if severity in {"HIGH", "MEDIUM"}:
        return "HIGH"
    return "LOW"


def _health_state_for_alerts(
    alerts: tuple[SyntheticAlert, ...],
) -> HealthState:
    if alerts and all(alert.noise_record for alert in alerts):
        return HealthState.NOISE
    if any(alert.severity == "HIGH" for alert in alerts):
        return HealthState.CRITICAL
    if any(alert.severity == "MEDIUM" for alert in alerts):
        return HealthState.DEGRADED
    return HealthState.HEALTHY
