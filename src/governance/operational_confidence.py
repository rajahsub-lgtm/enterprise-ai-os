"""
Operational confidence gate.

Classification: EAIOS Core

This module evaluates whether prior enterprise experience is reliable enough
to optimize the next governed due-diligence path.

It is adaptive, but not random.
It explains why behavior changes.
It does not bypass governance.
It does not authorize production action.
"""

from __future__ import annotations

from typing import Any


class OperationalConfidenceGate:
    def evaluate(
        self,
        *,
        case_context: dict[str, Any],
        fusion: dict[str, Any] | None = None,
        previous_operational_confidence: str | None = None,
    ) -> dict[str, Any]:
        memory_records = case_context.get("context_records", {}).get(
            "memory_context",
            [],
        )
        strongest_memory = self._strongest_memory(memory_records)

        impact = case_context.get("impact", {})
        impact_tier = impact.get("impact_tier", "UNKNOWN")

        conflicting_count = len(fusion.get("conflicting_evidence", [])) if fusion else 0
        missing_count = len(fusion.get("missing_evidence", [])) if fusion else 0
        weakening_count = len(fusion.get("weakening_evidence", [])) if fusion else 0
        fusion_confidence = fusion.get("fusion_confidence", "LOW") if fusion else "LOW"

        decision = self._decision(
            case_context=case_context,
            strongest_memory=strongest_memory,
            impact_tier=impact_tier,
            fusion_confidence=fusion_confidence,
            conflicting_count=conflicting_count,
            missing_count=missing_count,
            weakening_count=weakening_count,
        )

        previous_confidence = (
            previous_operational_confidence
            or self._prior_confidence_from_memory(strongest_memory)
        )

        decision["confidence_direction"] = self._confidence_direction(
            previous=previous_confidence,
            current=decision["operational_confidence"],
            pattern_maturity=decision["pattern_maturity"],
        )

        decision.update(self._adaptive_depth_controls(decision))

        return {
            "operational_confidence_id": f"OC-{case_context['case_id']}",
            "case_id": case_context["case_id"],
            "scenario_id": case_context["scenario_id"],
            "business_outcome": case_context["business_outcome"],
            "goal_category": case_context["goal_category"],
            **decision,
            "governance_required": True,
            "human_approval_required": True,
            "autonomous_action_allowed": False,
            "limits": [
                "Operational confidence determines due-diligence depth.",
                "Operational confidence does not remove governance.",
                "Operational confidence does not authorize production action.",
                "Human approval remains required for production-impacting decisions.",
            ],
        }

    def _decision(
        self,
        *,
        case_context: dict[str, Any],
        strongest_memory: dict[str, Any] | None,
        impact_tier: str,
        fusion_confidence: str,
        conflicting_count: int,
        missing_count: int,
        weakening_count: int,
    ) -> dict[str, Any]:
        if impact_tier == "UNKNOWN":
            return {
                "pattern_maturity": "UNKNOWN_IMPACT",
                "operational_confidence": "LOW",
                "selected_due_diligence_level": "ESCALATE_FOR_IMPACT_ASSESSMENT",
                "knowledge_retrieval_required": True,
                "why": [
                    "Business impact is unknown.",
                    "Unknown impact must not be treated as low risk.",
                    "Additional due diligence is required before recommendation review.",
                ],
            }

        if conflicting_count > 0:
            return {
                "pattern_maturity": "UNRELIABLE_FOR_CURRENT_CASE",
                "operational_confidence": "LOW",
                "selected_due_diligence_level": "EXPANDED_VALIDATION",
                "knowledge_retrieval_required": True,
                "why": [
                    "Current evidence contains conflicting signals.",
                    "Prior experience is not reliable enough for an optimized path.",
                    "Expanded due diligence is required.",
                ],
            }

        if missing_count > 0:
            return {
                "pattern_maturity": "INCOMPLETE_CONTEXT",
                "operational_confidence": "LOW",
                "selected_due_diligence_level": "EXPANDED_VALIDATION",
                "knowledge_retrieval_required": True,
                "why": [
                    "Required evidence is missing.",
                    "The system cannot rely on an optimized path without sufficient context.",
                    "Additional due diligence is required.",
                ],
            }

        if strongest_memory is None:
            return {
                "pattern_maturity": "NONE",
                "operational_confidence": "LOW",
                "selected_due_diligence_level": "FULL_DUE_DILIGENCE",
                "knowledge_retrieval_required": True,
                "why": [
                    "No reliable prior memory pattern is available.",
                    "The condition should be treated as a new case.",
                    "Broad due diligence is required.",
                ],
            }

        memory_quality = self._memory_quality(strongest_memory)

        if (
            memory_quality["is_human_validated"]
            and memory_quality["successful_uses"] >= 50
            and memory_quality["failed_uses"] == 0
            and memory_quality["similarity"] >= 0.85
            and not memory_quality["is_stale"]
            and fusion_confidence == "HIGH"
            and weakening_count == 0
        ):
            return {
                "pattern_maturity": "TRUSTED",
                "operational_confidence": "HIGH",
                "selected_due_diligence_level": "TARGETED_VALIDATION",
                "knowledge_retrieval_required": False,
                "why": [
                    "A human-validated memory pattern strongly matches the current condition.",
                    (
                        "The pattern has at least 50 successful prior uses and no recorded failures."
                    ),
                    "Current evidence does not conflict with the trusted pattern.",
                    "Targeted validation is sufficient before human review.",
                ],
            }

        if (
            memory_quality["is_human_validated"]
            and memory_quality["similarity"] >= 0.65
            and memory_quality["failed_uses"] <= 2
            and not memory_quality["is_stale"]
        ):
            return {
                "pattern_maturity": "EMERGING",
                "operational_confidence": "MEDIUM",
                "selected_due_diligence_level": "TARGETED_KNOWLEDGE_RETRIEVAL",
                "knowledge_retrieval_required": True,
                "why": [
                    "A prior validated pattern partially matches the current condition.",
                    "The pattern is useful but not mature enough to avoid additional due diligence.",
                    "Targeted knowledge retrieval is required.",
                ],
            }

        return {
            "pattern_maturity": "TRUSTED_BUT_DRIFTING",
            "operational_confidence": "LOW",
            "selected_due_diligence_level": "EXPANDED_VALIDATION",
            "knowledge_retrieval_required": True,
            "why": [
                "Prior memory exists but is stale, weak, failed, or insufficiently similar.",
                "Operational confidence is reduced for the current condition.",
                "Expanded due diligence is required.",
            ],
        }

    def _adaptive_depth_controls(
        self,
        decision: dict[str, Any],
    ) -> dict[str, Any]:
        level = decision["selected_due_diligence_level"]
        direction = decision["confidence_direction"]

        required_steps_by_level = {
            "ESCALATE_FOR_IMPACT_ASSESSMENT": [
                "assess_impact_context",
                "retrieve_support_knowledge",
            ],
            "FULL_DUE_DILIGENCE": [
                "retrieve_memory_patterns",
                "retrieve_support_knowledge",
                "validate_current_context",
                "assess_impact_context",
                "resolve_evidence_conflicts",
            ],
            "EXPANDED_VALIDATION": [
                "retrieve_memory_patterns",
                "retrieve_support_knowledge",
                "validate_current_context",
                "resolve_evidence_conflicts",
            ],
            "TARGETED_KNOWLEDGE_RETRIEVAL": [
                "retrieve_memory_patterns",
                "retrieve_support_knowledge",
            ],
            "TARGETED_VALIDATION": [
                "retrieve_memory_patterns",
                "validate_current_context",
            ],
        }

        required_agent_steps = list(required_steps_by_level.get(level, []))

        if direction == "DECREASING" and level != "ESCALATE_FOR_IMPACT_ASSESSMENT":
            required_agent_steps = sorted(
                set(required_agent_steps)
                | {
                    "retrieve_support_knowledge",
                    "validate_current_context",
                    "resolve_evidence_conflicts",
                }
            )

        prohibited_shortcuts = [
            "skip_governance",
            "skip_human_review",
            "allow_autonomous_production_action",
            "treat_memory_as_truth",
        ]

        if decision["operational_confidence"] == "LOW":
            prohibited_shortcuts.extend(
                [
                    "skip_knowledge_retrieval",
                    "skip_context_validation",
                    "skip_impact_assessment",
                ]
            )

        if level in {
            "TARGETED_VALIDATION",
            "TARGETED_KNOWLEDGE_RETRIEVAL",
        }:
            prohibited_shortcuts.extend(
                [
                    "bypass_validation",
                    "bypass_audit_trace",
                ]
            )

        return {
            "required_agent_steps": required_agent_steps,
            "prohibited_shortcuts": sorted(set(prohibited_shortcuts)),
        }

    def _strongest_memory(
        self,
        memory_records: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        if not memory_records:
            return None

        return sorted(
            memory_records,
            key=lambda record: (
                self._memory_quality(record)["similarity"],
                self._memory_quality(record)["successful_uses"],
                -self._memory_quality(record)["failed_uses"],
            ),
            reverse=True,
        )[0]

    def _memory_quality(self, record: dict[str, Any]) -> dict[str, Any]:
        successful_uses = int(
            record.get(
                "successful_uses",
                record.get(
                    "success_count",
                    record.get("prior_success_count", 0),
                ),
            )
        )
        failed_uses = int(
            record.get(
                "failed_uses",
                record.get(
                    "failure_count",
                    record.get("prior_failure_count", 0),
                ),
            )
        )
        similarity = float(
            record.get(
                "similarity",
                record.get(
                    "match_strength",
                    record.get("pattern_match_score", 0.0),
                ),
            )
        )

        validation_state = record.get("validation_state", "UNVALIDATED")
        freshness = record.get("freshness", record.get("freshness_state", "CURRENT"))

        return {
            "successful_uses": successful_uses,
            "failed_uses": failed_uses,
            "similarity": similarity,
            "is_human_validated": validation_state == "HUMAN_VALIDATED",
            "is_stale": freshness == "STALE",
        }

    def _prior_confidence_from_memory(
        self,
        strongest_memory: dict[str, Any] | None,
    ) -> str | None:
        if strongest_memory is None:
            return None

        value = strongest_memory.get("prior_confidence")
        if isinstance(value, str):
            return value

        return None

    def _confidence_direction(
        self,
        *,
        previous: str | None,
        current: str,
        pattern_maturity: str,
    ) -> str:
        if previous is None:
            if pattern_maturity == "NONE":
                return "NEW"
            return "STABLE"

        rank = {
            "LOW": 1,
            "MEDIUM": 2,
            "HIGH": 3,
        }

        previous_rank = rank.get(previous, 1)
        current_rank = rank.get(current, 1)

        if current_rank > previous_rank:
            return "INCREASING"

        if current_rank < previous_rank:
            return "DECREASING"

        return "STABLE"
