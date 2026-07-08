"""
IT Application Health synthetic repository loader.

Classification: Domain Adapter

This module may use ITIL/application-health vocabulary because it lives inside
the domain adapter boundary. It loads the checked-in deterministic synthetic
repository files and exposes read-only lookup helpers.

It must not perform governance, evidence creation, content safety, reasoning,
or remediation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_DOMAIN_PATH = Path("data/domain/it_application_health")


class ItApplicationHealthRepository:
    def __init__(self, domain_path: str | Path = DEFAULT_DOMAIN_PATH) -> None:
        self.domain_path = Path(domain_path)

        self.golden_scenarios = self._load_json("golden_scenarios.json")
        self.business_impact_map = self._load_json("business_impact_map.json")
        self.cmdb_topology = self._load_json("cmdb_topology.json")
        self.operational_records = self._load_json("operational_records.json")

    def _load_json(self, filename: str) -> dict[str, Any]:
        path = self.domain_path / filename
        return json.loads(path.read_text(encoding="utf-8-sig"))

    def business_outcome(self) -> str:
        return self.golden_scenarios["business_outcome"]

    def scenarios(self) -> list[dict[str, Any]]:
        return list(self.golden_scenarios["scenarios"])

    def scenario_by_id(self, scenario_id: str) -> dict[str, Any]:
        for scenario in self.scenarios():
            if scenario["scenario_id"] == scenario_id:
                return scenario

        raise KeyError(f"Unknown scenario_id: {scenario_id}")

    def cis(self) -> list[dict[str, Any]]:
        return list(self.cmdb_topology["cis"])

    def ci_by_id(self, ci_id: str) -> dict[str, Any]:
        for ci in self.cis():
            if ci["ci_id"] == ci_id:
                return ci

        raise KeyError(f"Unknown ci_id: {ci_id}")

    def business_services(self) -> list[dict[str, Any]]:
        return list(self.business_impact_map["business_services"])

    def business_service_by_id(self, business_service_id: str) -> dict[str, Any]:
        for service in self.business_services():
            if service["business_service_id"] == business_service_id:
                return service

        raise KeyError(f"Unknown business_service_id: {business_service_id}")

    def unknown_impact_policy(self) -> dict[str, Any]:
        return dict(self.business_impact_map["unknown_impact_policy"])

    def records_for_scenario(self, scenario_id: str) -> dict[str, list[dict[str, Any]]]:
        records = {}

        for group_name in [
            "monitoring_events",
            "incidents",
            "problems",
            "knowledge_articles",
            "change_requests",
            "memory_patterns",
        ]:
            records[group_name] = [
                record
                for record in self.operational_records[group_name]
                if record["scenario_id"] == scenario_id
            ]

        return records

    def business_services_for_ci(self, ci_id: str) -> list[dict[str, Any]]:
        ci = self.ci_by_id(ci_id)

        return [
            self.business_service_by_id(service_id)
            for service_id in ci["mapped_business_services"]
        ]

    def is_unmapped_ci(self, ci_id: str) -> bool:
        return self.ci_by_id(ci_id)["mapped_business_services"] == []
