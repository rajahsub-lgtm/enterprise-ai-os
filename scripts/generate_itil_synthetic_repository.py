"""
Seeded synthetic ITIL repository generator.

Sprint 2.5b principle:
- Golden scenarios are checked in and stable.
- Background noise is generated deterministically from a seed.
- Large generated noise files are not committed by default.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any


DOMAIN_PATH = Path("data/domain/it_application_health")

SCENARIOS_PATH = DOMAIN_PATH / "golden_scenarios.json"
IMPACT_MAP_PATH = DOMAIN_PATH / "business_impact_map.json"
TOPOLOGY_PATH = DOMAIN_PATH / "cmdb_topology.json"
RECORDS_PATH = DOMAIN_PATH / "operational_records.json"

DEFAULT_EVENT_COUNT = 5000
DEFAULT_INCIDENT_COUNT = 2400
DEFAULT_SEED = 2525
DEFAULT_OUTPUT_PATH = DOMAIN_PATH / "itil_synthetic_repository.generated.json"

FIXED_GENERATED_AT = "2026-07-07T00:00:00Z"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def choose_ci(rng: random.Random, ci_ids: list[str]) -> str:
    return rng.choice(ci_ids)


def generate_noise_events(
    *,
    rng: random.Random,
    ci_ids: list[str],
    count: int,
) -> list[dict[str, Any]]:
    severities = ["INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
    signal_types = [
        "latency",
        "error_rate",
        "timeout",
        "resource_contention",
        "connection_exhaustion",
        "packet_loss",
        "batch_delay",
        "dependency_warning",
    ]

    events = []

    for index in range(1, count + 1):
        ci_id = choose_ci(rng, ci_ids)
        severity = rng.choices(
            severities,
            weights=[35, 25, 20, 15, 5],
            k=1,
        )[0]
        signal_type = rng.choice(signal_types)

        events.append(
            {
                "event_id": f"EVT-NOISE-{index:06d}",
                "scenario_id": "NOISE",
                "source_system": "synthetic_observability",
                "severity": severity,
                "related_ci": ci_id,
                "summary": f"Synthetic {signal_type} signal observed on {ci_id}.",
                "signal_type": signal_type,
            }
        )

    return events


def generate_noise_incidents(
    *,
    rng: random.Random,
    ci_ids: list[str],
    service_ids: list[str],
    count: int,
) -> list[dict[str, Any]]:
    priorities = ["P4", "P3", "P2", "P1"]
    summaries = [
        "Synthetic user-reported degradation.",
        "Synthetic monitoring-created ticket.",
        "Synthetic intermittent service warning.",
        "Synthetic dependency symptom requiring triage.",
    ]

    incidents = []

    for index in range(1, count + 1):
        ci_id = choose_ci(rng, ci_ids)
        priority = rng.choices(
            priorities,
            weights=[45, 35, 17, 3],
            k=1,
        )[0]

        # Most noise incidents are mapped. A small number intentionally remain
        # unmapped to preserve unknown-impact test coverage.
        if rng.random() < 0.95:
            business_service_id = rng.choice(service_ids)
        else:
            business_service_id = None
            priority = "IMPACT_UNKNOWN"

        incidents.append(
            {
                "incident_id": f"INC-NOISE-{index:06d}",
                "scenario_id": "NOISE",
                "priority": priority,
                "related_ci": ci_id,
                "business_service_id": business_service_id,
                "summary": rng.choice(summaries),
                "user_reported": rng.choice([True, False]),
            }
        )

    return incidents


def generate_repository(
    *,
    seed: int = DEFAULT_SEED,
    event_count: int = DEFAULT_EVENT_COUNT,
    incident_count: int = DEFAULT_INCIDENT_COUNT,
) -> dict[str, Any]:
    rng = random.Random(seed)

    scenarios = load_json(SCENARIOS_PATH)
    impact_map = load_json(IMPACT_MAP_PATH)
    topology = load_json(TOPOLOGY_PATH)
    operational_records = load_json(RECORDS_PATH)

    ci_ids = [ci["ci_id"] for ci in topology["cis"]]
    service_ids = [
        service["business_service_id"]
        for service in impact_map["business_services"]
    ]

    noise_events = generate_noise_events(
        rng=rng,
        ci_ids=ci_ids,
        count=event_count,
    )
    noise_incidents = generate_noise_incidents(
        rng=rng,
        ci_ids=ci_ids,
        service_ids=service_ids,
        count=incident_count,
    )

    return {
        "repository_name": "EAIOS Generated Synthetic ITIL Repository",
        "version": "0.1.0",
        "business_outcome": "Maintain Application Health",
        "seed": seed,
        "generated_at": FIXED_GENERATED_AT,
        "golden": {
            "scenarios": scenarios,
            "impact_map": impact_map,
            "topology": topology,
            "operational_records": operational_records,
        },
        "generated_noise": {
            "monitoring_events": noise_events,
            "incidents": noise_incidents,
        },
        "counts": {
            "golden_scenarios": len(scenarios["scenarios"]),
            "golden_monitoring_events": len(operational_records["monitoring_events"]),
            "golden_incidents": len(operational_records["incidents"]),
            "generated_monitoring_events": len(noise_events),
            "generated_incidents": len(noise_incidents),
            "total_monitoring_events": (
                len(operational_records["monitoring_events"]) + len(noise_events)
            ),
            "total_incidents": (
                len(operational_records["incidents"]) + len(noise_incidents)
            ),
        },
    }


def write_repository(repository: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(repository, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate deterministic synthetic ITIL repository noise."
    )
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--events", type=int, default=DEFAULT_EVENT_COUNT)
    parser.add_argument("--incidents", type=int, default=DEFAULT_INCIDENT_COUNT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write generated repository JSON to disk.",
    )

    args = parser.parse_args()

    repository = generate_repository(
        seed=args.seed,
        event_count=args.events,
        incident_count=args.incidents,
    )

    if args.write:
        write_repository(repository, args.output)
        print(f"Wrote generated repository to {args.output}")
    else:
        print(
            json.dumps(
                {
                    "repository_name": repository["repository_name"],
                    "seed": repository["seed"],
                    "counts": repository["counts"],
                },
                indent=2,
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
