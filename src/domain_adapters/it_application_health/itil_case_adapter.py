"""
IT Application Health case adapter.

Classification: Domain Adapter

This module converts IT application-health synthetic records into a core-facing
case context. It may read ITIL/application-health terms internally, but the
returned case context uses neutral EAIOS concepts:

- business_outcome
- goal_category
- case_id
- entities
- observations
- impact
- governance_flags
- human_approval_required

It must not perform evidence fusion, recommendation generation, execution,
or autonomous action.
"""

from __future__ import annotations

from typing import Any

from .itil_repository_loader import ItApplicationHealthRepository


class ItApplicationHealthCaseAdapter:
    def __init__(self, repository: ItApplicationHealthRepository) -> None:
        self.repository = repository

    def build_case(self, scenario_id: str) -> dict[str, Any]:
        scenario = self.repository.scenario_by_id(scenario_id)
        records = self.repository.records_for_scenario(scenario_id)

        affected_ci_ids = scenario["primary_entities"]["affected_cis"]

        return {
            "case_id": f"CASE-{scenario_id}",
            "scenario_id": scenario_id,
            "business_outcome": scenario["business_outcome"],
            "goal_category": scenario["goal_category"],
            "case_summary": scenario["story"],
            "entities": self._build_entities(scenario),
            "observations": self._build_observations(records),
            "context_records": self._build_context_records(records),
            "impact": self._build_impact(scenario),
            "governance_flags": self._build_governance_flags(scenario),
            "human_approval_required": scenario["requires_human_approval"],
            "autonomous_action_allowed": scenario["autonomous_action_allowed"],
            "source_record_counts": {
                "affected_entities": len(affected_ci_ids),
                "monitoring_events": len(records["monitoring_events"]),
                "incidents": len(records["incidents"]),
                "problems": len(records["problems"]),
                "knowledge_articles": len(records["knowledge_articles"]),
                "change_requests": len(records["change_requests"]),
                "memory_patterns": len(records["memory_patterns"]),
            },
        }

    def _build_entities(self, scenario: dict[str, Any]) -> list[dict[str, Any]]:
        entities: list[dict[str, Any]] = []

        business_service_id = scenario["primary_entities"]["business_service"]

        if business_service_id is not None:
            service = self.repository.business_service_by_id(business_service_id)
            entities.append(
                {
                    "entity_id": service["business_service_id"],
                    "entity_type": "business_service",
                    "name": service["name"],
                    "owner": service["business_owner"],
                    "impact_tier": service["impact_tier"],
                    "criticality": service["criticality"],
                }
            )

        for ci_id in scenario["primary_entities"]["affected_cis"]:
            ci = self.repository.ci_by_id(ci_id)
            entities.append(
                {
                    "entity_id": ci["ci_id"],
                    "entity_type": ci["ci_type"],
                    "name": ci["name"],
                    "owner": ci["owner"],
                    "environment": ci["environment"],
                    "mapped_business_services": list(ci["mapped_business_services"]),
                }
            )

        return entities

    def _build_observations(
        self,
        records: dict[str, list[dict[str, Any]]],
    ) -> list[dict[str, Any]]:
        observations: list[dict[str, Any]] = []

        for event in records["monitoring_events"]:
            observations.append(
                {
                    "observation_id": f"OBS-{event['event_id']}",
                    "observation_type": "telemetry_signal",
                    "source_record_id": event["event_id"],
                    "entity_id": event["related_ci"],
                    "severity": event["severity"],
                    "summary": event["summary"],
                    "signal_type": event["signal_type"],
                }
            )

        for incident in records["incidents"]:
            observations.append(
                {
                    "observation_id": f"OBS-{incident['incident_id']}",
                    "observation_type": "reported_symptom",
                    "source_record_id": incident["incident_id"],
                    "entity_id": incident["related_ci"],
                    "priority": incident["priority"],
                    "summary": incident["summary"],
                    "user_reported": incident["user_reported"],
                }
            )

        return observations

    def _build_context_records(
        self,
        records: dict[str, list[dict[str, Any]]],
    ) -> dict[str, list[dict[str, Any]]]:
        return {
            "problem_context": [
                {
                    "record_id": problem["problem_id"],
                    "entity_id": problem["related_ci"],
                    "summary": problem["summary"],
                    "known_pattern": problem["known_error"],
                    "known_pattern_id": problem.get("known_error_id"),
                }
                for problem in records["problems"]
            ],
            "knowledge_context": [
                {
                    "record_id": article["knowledge_id"],
                    "entity_id": article["related_ci"],
                    "owner": article["item_owner"],
                    "last_validated": article["item_last_validated"],
                    "trust_level": article["trust_level"],
                    "expected_content_safety": article["content_safety_expected"],
                    "summary": article["summary"],
                }
                for article in records["knowledge_articles"]
            ],
            "change_context": [
                {
                    "record_id": change["change_id"],
                    "entity_id": change["related_ci"],
                    "change_type": change["change_type"],
                    "status": change["status"],
                    "implemented_at": change["implemented_at"],
                    "summary": change["summary"],
                }
                for change in records["change_requests"]
            ],
            "memory_context": [
                {
                    "record_id": memory["memory_id"],
                    "entity_id": memory["related_ci"],
                    "memory_type": memory["memory_type"],
                    "validation_state": memory["validation_state"],
                    "confidence": memory["confidence"],
                    "last_confirmed": memory["last_confirmed"],
                    "summary": memory["summary"],
                    "outcome_history": memory["outcome_history"],
                }
                for memory in records["memory_patterns"]
            ],
        }

    def _build_impact(self, scenario: dict[str, Any]) -> dict[str, Any]:
        business_service_id = scenario["primary_entities"]["business_service"]

        if business_service_id is None or scenario["impact_tier"] == "UNKNOWN":
            policy = self.repository.unknown_impact_policy()

            return {
                "business_service_id": None,
                "impact_tier": policy["impact_tier"],
                "impact_confidence": policy["impact_confidence"],
                "required_action": policy["required_action"],
                "governance_debt": policy["governance_debt"],
                "autonomous_action_allowed": policy["autonomous_action_allowed"],
            }

        service = self.repository.business_service_by_id(business_service_id)

        return {
            "business_service_id": business_service_id,
            "impact_tier": scenario["impact_tier"],
            "impact_confidence": scenario["impact_confidence"],
            "criticality": service["criticality"],
            "business_owner": service["business_owner"],
            "required_action": scenario["expected_result"]["required_action"],
            "autonomous_action_allowed": scenario["autonomous_action_allowed"],
        }

    def _build_governance_flags(self, scenario: dict[str, Any]) -> dict[str, Any]:
        flags = {
            "requires_human_approval": scenario["requires_human_approval"],
            "autonomous_action_allowed": scenario["autonomous_action_allowed"],
            "recommendation_type": scenario["expected_result"]["recommendation_type"],
            "governance_debt": scenario.get("governance_debt"),
        }

        if scenario["impact_tier"] == "UNKNOWN":
            flags["requires_impact_assessment"] = True
        else:
            flags["requires_impact_assessment"] = False

        return flags
