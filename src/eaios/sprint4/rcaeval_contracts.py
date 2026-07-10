"""RCAEval / Train Ticket structural contracts for Sprint 4.

Classification: EAIOS Sprint 4 domain adapter boundary.

The structural sample is hand-authored. It exists to lock adapter shape before
raw RCAEval ingestion. It must not contain copied benchmark records.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import json
from pathlib import Path
from typing import Any


class SignalType(str, Enum):
    METRIC = "metric"
    LOG = "log"
    TRACE = "trace"


class BenchmarkVerificationState(str, Enum):
    MATCHED = "MATCHED"
    PARTIAL = "PARTIAL"
    MISSED = "MISSED"
    NOT_SCORABLE = "NOT_SCORABLE"


@dataclass(frozen=True)
class TimeWindow:
    start: str
    end: str


@dataclass(frozen=True)
class TelemetrySymptom:
    symptom_id: str
    service: str
    signal_type: SignalType
    indicator: str
    observed_value: float
    baseline_value: float
    severity: str
    source_failure_case_id: str | None
    noise_record: bool
    benchmark_scoring_eligible: bool


@dataclass(frozen=True)
class TrainTicketFaultScenario:
    failure_case_id: str
    root_cause_service: str
    root_cause_indicator: str
    fault_type: str
    time_window: TimeWindow
    affected_services: tuple[str, ...]
    telemetry_symptoms: tuple[TelemetrySymptom, ...]


@dataclass(frozen=True)
class ServiceDependency:
    source_service: str
    target_service: str
    dependency_type: str


@dataclass(frozen=True)
class ServiceTopology:
    services: tuple[str, ...]
    dependencies: tuple[ServiceDependency, ...]

    def downstream_of(self, service_id: str) -> tuple[str, ...]:
        return tuple(
            dependency.target_service
            for dependency in self.dependencies
            if dependency.source_service == service_id
        )

    def upstream_of(self, service_id: str) -> tuple[str, ...]:
        return tuple(
            dependency.source_service
            for dependency in self.dependencies
            if dependency.target_service == service_id
        )


@dataclass(frozen=True)
class BenchmarkVerificationTarget:
    composition_scenario_id: str
    source_failure_case_id: str
    expected_issue_ids: tuple[str, ...]
    expected_root_cause_service: str
    expected_root_cause_indicator: str
    noise_issue_ids: tuple[str, ...]


@dataclass(frozen=True)
class BenchmarkVerificationResult:
    state: BenchmarkVerificationState
    target: BenchmarkVerificationTarget
    predicted_issue_ids: tuple[str, ...]
    predicted_root_cause_service: str | None
    predicted_root_cause_indicator: str | None
    matched_issue_ids: tuple[str, ...]
    missed_issue_ids: tuple[str, ...]
    noise_excluded: bool
    comparison_note: str


@dataclass(frozen=True)
class StructuralSample:
    composition_scenario_id: str
    fault_scenarios: tuple[TrainTicketFaultScenario, ...]
    noise_symptoms: tuple[TelemetrySymptom, ...]
    service_topology: ServiceTopology
    copied_from_rcaeval: bool
    raw_benchmark_data: bool


def load_structural_sample(path: str | Path) -> StructuralSample:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))

    policy = payload["sample_policy"]
    if policy["copied_from_rcaeval"] is not False:
        raise ValueError("Structural sample must not copy RCAEval records.")
    if policy["raw_benchmark_data"] is not False:
        raise ValueError("Structural sample must not contain raw benchmark data.")

    fault_scenarios = tuple(
        _parse_fault_scenario(raw_fault)
        for raw_fault in payload["fault_scenarios"]
    )

    noise_symptoms = tuple(
        _parse_symptom(
            raw_symptom=raw_symptom,
            source_failure_case_id=None,
            noise_record=True,
            benchmark_scoring_eligible=False,
        )
        for raw_symptom in payload.get("noise_symptoms", ())
    )

    return StructuralSample(
        composition_scenario_id=payload["composition_scenario_id"],
        fault_scenarios=fault_scenarios,
        noise_symptoms=noise_symptoms,
        service_topology=_parse_topology(payload["service_topology"]),
        copied_from_rcaeval=policy["copied_from_rcaeval"],
        raw_benchmark_data=policy["raw_benchmark_data"],
    )


def build_benchmark_targets(
    sample: StructuralSample,
) -> tuple[BenchmarkVerificationTarget, ...]:
    noise_issue_ids = tuple(symptom.symptom_id for symptom in sample.noise_symptoms)

    return tuple(
        BenchmarkVerificationTarget(
            composition_scenario_id=sample.composition_scenario_id,
            source_failure_case_id=fault.failure_case_id,
            expected_issue_ids=tuple(
                symptom.symptom_id for symptom in fault.telemetry_symptoms
            ),
            expected_root_cause_service=fault.root_cause_service,
            expected_root_cause_indicator=fault.root_cause_indicator,
            noise_issue_ids=noise_issue_ids,
        )
        for fault in sample.fault_scenarios
    )


def score_benchmark_result(
    target: BenchmarkVerificationTarget,
    predicted_issue_ids: tuple[str, ...],
    predicted_root_cause_service: str | None,
    predicted_root_cause_indicator: str | None,
) -> BenchmarkVerificationResult:
    expected = set(target.expected_issue_ids)
    predicted = set(predicted_issue_ids)

    matched = tuple(sorted(expected.intersection(predicted)))
    missed = tuple(sorted(expected.difference(predicted)))
    noise_excluded = not bool(predicted.intersection(target.noise_issue_ids))

    root_service_match = (
        predicted_root_cause_service == target.expected_root_cause_service
    )
    indicator_match = (
        predicted_root_cause_indicator == target.expected_root_cause_indicator
    )
    all_issues_matched = expected == predicted.intersection(expected)

    if all_issues_matched and root_service_match and indicator_match and noise_excluded:
        state = BenchmarkVerificationState.MATCHED
        note = "Cluster membership and root cause matched benchmark target."
    elif matched or root_service_match or indicator_match:
        state = BenchmarkVerificationState.PARTIAL
        note = "Some benchmark expectations matched, but result is incomplete."
    else:
        state = BenchmarkVerificationState.MISSED
        note = "No meaningful benchmark target match."

    if not target.expected_issue_ids:
        state = BenchmarkVerificationState.NOT_SCORABLE
        note = "Benchmark target had no expected issue ids."

    return BenchmarkVerificationResult(
        state=state,
        target=target,
        predicted_issue_ids=predicted_issue_ids,
        predicted_root_cause_service=predicted_root_cause_service,
        predicted_root_cause_indicator=predicted_root_cause_indicator,
        matched_issue_ids=matched,
        missed_issue_ids=missed,
        noise_excluded=noise_excluded,
        comparison_note=note,
    )


def _parse_fault_scenario(raw_fault: dict[str, Any]) -> TrainTicketFaultScenario:
    failure_case_id = raw_fault["failure_case_id"]
    symptoms = tuple(
        _parse_symptom(
            raw_symptom=raw_symptom,
            source_failure_case_id=failure_case_id,
            noise_record=False,
            benchmark_scoring_eligible=True,
        )
        for raw_symptom in raw_fault["telemetry_symptoms"]
    )

    return TrainTicketFaultScenario(
        failure_case_id=failure_case_id,
        root_cause_service=raw_fault["root_cause_service"],
        root_cause_indicator=raw_fault["root_cause_indicator"],
        fault_type=raw_fault["fault_type"],
        time_window=TimeWindow(**raw_fault["time_window"]),
        affected_services=tuple(raw_fault["affected_services"]),
        telemetry_symptoms=symptoms,
    )


def _parse_symptom(
    raw_symptom: dict[str, Any],
    source_failure_case_id: str | None,
    noise_record: bool,
    benchmark_scoring_eligible: bool,
) -> TelemetrySymptom:
    return TelemetrySymptom(
        symptom_id=raw_symptom["symptom_id"],
        service=raw_symptom["service"],
        signal_type=SignalType(raw_symptom["signal_type"]),
        indicator=raw_symptom["indicator"],
        observed_value=float(raw_symptom["observed_value"]),
        baseline_value=float(raw_symptom["baseline_value"]),
        severity=raw_symptom["severity"],
        source_failure_case_id=source_failure_case_id,
        noise_record=noise_record,
        benchmark_scoring_eligible=benchmark_scoring_eligible,
    )


def _parse_topology(raw_topology: dict[str, Any]) -> ServiceTopology:
    services = tuple(service["service_id"] for service in raw_topology["services"])
    dependencies = tuple(
        ServiceDependency(
            source_service=raw_dependency["source_service"],
            target_service=raw_dependency["target_service"],
            dependency_type=raw_dependency["dependency_type"],
        )
        for raw_dependency in raw_topology["dependencies"]
    )

    return ServiceTopology(services=services, dependencies=dependencies)
