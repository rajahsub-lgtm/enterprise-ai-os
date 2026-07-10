"""
Reasoning explanation contract.

Classification: EAIOS Core

This module accepts a core-facing case context and an evidence fusion package,
then produces a lightweight KT-style hypothesis explanation.

It does not create final truth.
It does not authorize action.
It does not execute anything.
"""

from __future__ import annotations

from typing import Any


class ReasoningExplanationEngine:
    def explain(
        self,
        *,
        case_context: dict[str, Any],
        fusion: dict[str, Any],
    ) -> dict[str, Any]:
        hypotheses = self._build_hypotheses(
            case_context=case_context,
            fusion=fusion,
        )
        selected_hypothesis = self._select_hypothesis(hypotheses)

        return {
            "reasoning_id": f"REASON-{case_context['case_id']}",
            "case_id": case_context["case_id"],
            "scenario_id": case_context["scenario_id"],
            "business_outcome": case_context["business_outcome"],
            "goal_category": case_context["goal_category"],
            "method": "lightweight_kt_problem_analysis",
            "kt_problem_analysis": self._kt_problem_analysis(
                case_context=case_context,
                hypotheses=hypotheses,
                selected_hypothesis=selected_hypothesis,
            ),
            "hypotheses": hypotheses,
            "selected_hypothesis_id": selected_hypothesis["hypothesis_id"],
            "reasoning_confidence": selected_hypothesis["confidence"],
            "reasoning_summary": selected_hypothesis["summary"],
            "why_chain": self._why_chain(
                case_context=case_context,
                fusion=fusion,
                selected_hypothesis=selected_hypothesis,
            ),
            "limits": [
                "Reasoning is an explanation package, not a final truth claim.",
                "Reasoning does not authorize production action.",
                "Recommendation remains human-review only.",
            ],
            "requires_human_review": True,
            "autonomous_action_allowed": False,
        }

    def _build_hypotheses(
        self,
        *,
        case_context: dict[str, Any],
        fusion: dict[str, Any],
    ) -> list[dict[str, Any]]:
        hypotheses: list[dict[str, Any]] = []

        impact = case_context.get("impact", {})
        impact_tier = impact.get("impact_tier", "UNKNOWN")

        if impact_tier == "UNKNOWN":
            hypotheses.append(
                {
                    "hypothesis_id": f"HYP-{case_context['case_id']}-UNKNOWN-IMPACT",
                    "summary": (
                        "Business impact cannot be established because required "
                        "impact mapping is missing."
                    ),
                    "hypothesis_type": "missing_context",
                    "supporting_evidence_ids": self._ids(fusion["supporting_evidence"]),
                    "weakening_evidence_ids": self._ids(fusion["weakening_evidence"]),
                    "conflicting_evidence_ids": self._ids(fusion["conflicting_evidence"]),
                    "missing_evidence_ids": self._ids(fusion["missing_evidence"]),
                    "confidence": "LOW",
                    "why_this_matters": (
                        "Unknown impact must be escalated rather than treated as low risk."
                    ),
                    "requires_additional_evidence": True,
                }
            )

        if fusion["conflicting_evidence"]:
            hypotheses.append(
                {
                    "hypothesis_id": f"HYP-{case_context['case_id']}-CONFLICTING-SIGNALS",
                    "summary": (
                        "Multiple observed entities may explain the condition; "
                        "current evidence is not sufficient to select a single explanation."
                    ),
                    "hypothesis_type": "conflicting_evidence",
                    "supporting_evidence_ids": self._ids(fusion["supporting_evidence"]),
                    "weakening_evidence_ids": self._ids(fusion["weakening_evidence"]),
                    "conflicting_evidence_ids": self._ids(fusion["conflicting_evidence"]),
                    "missing_evidence_ids": self._ids(fusion["missing_evidence"]),
                    "confidence": "LOW",
                    "why_this_matters": (
                        "The system should gather more evidence instead of forcing a single explanation."
                    ),
                    "requires_additional_evidence": True,
                }
            )

        memory_records = (
            case_context.get("context_records", {}).get("memory_context", [])
        )
        validated_memory = [
            record
            for record in memory_records
            if record.get("validation_state") == "HUMAN_VALIDATED"
        ]

        if validated_memory:
            hypotheses.append(
                {
                    "hypothesis_id": f"HYP-{case_context['case_id']}-VALIDATED-MEMORY-PATTERN",
                    "summary": (
                        "A prior human-validated pattern may explain the current condition, "
                        "but it remains evidence rather than truth."
                    ),
                    "hypothesis_type": "memory_supported_pattern",
                    "supporting_evidence_ids": self._ids_by_type(
                        fusion["supporting_evidence"],
                        "memory_context",
                    ),
                    "weakening_evidence_ids": self._ids(fusion["weakening_evidence"]),
                    "conflicting_evidence_ids": self._ids(fusion["conflicting_evidence"]),
                    "missing_evidence_ids": self._ids(fusion["missing_evidence"]),
                    "confidence": self._bounded_confidence(fusion["fusion_confidence"]),
                    "why_this_matters": (
                        "Prior validated outcomes can improve reasoning, but cannot authorize action."
                    ),
                    "requires_additional_evidence": fusion["fusion_confidence"] != "HIGH",
                }
            )

        should_add_evidence_aligned = (
            not hypotheses
            or (
                fusion["fusion_confidence"] == "HIGH"
                and not fusion["conflicting_evidence"]
                and not fusion["missing_evidence"]
                and impact_tier != "UNKNOWN"
            )
        )

        if should_add_evidence_aligned:
            hypotheses.append(
                {
                    "hypothesis_id": f"HYP-{case_context['case_id']}-EVIDENCE-ALIGNED",
                    "summary": (
                        "The fused evidence supports a coherent explanation for the case, "
                        "pending human review."
                    ),
                    "hypothesis_type": "evidence_aligned_explanation",
                    "supporting_evidence_ids": self._ids(fusion["supporting_evidence"]),
                    "weakening_evidence_ids": self._ids(fusion["weakening_evidence"]),
                    "conflicting_evidence_ids": self._ids(fusion["conflicting_evidence"]),
                    "missing_evidence_ids": self._ids(fusion["missing_evidence"]),
                    "confidence": fusion["fusion_confidence"],
                    "why_this_matters": (
                        "The explanation is supported by fused evidence but still requires approval."
                    ),
                    "requires_additional_evidence": fusion["fusion_confidence"] != "HIGH",
                }
            )

        return hypotheses

    def _select_hypothesis(self, hypotheses: list[dict[str, Any]]) -> dict[str, Any]:
        priority = {
            "missing_context": 0,
            "conflicting_evidence": 1,
            "evidence_aligned_explanation": 2,
            "memory_supported_pattern": 3,
        }

        return sorted(
            hypotheses,
            key=lambda hypothesis: priority[hypothesis["hypothesis_type"]],
        )[0]

    def _kt_problem_analysis(
        self,
        *,
        case_context: dict[str, Any],
        hypotheses: list[dict[str, Any]],
        selected_hypothesis: dict[str, Any],
    ) -> dict[str, Any]:
        impact = case_context.get("impact", {})

        return {
            "situation": case_context["case_summary"],
            "is": self._is_statements(case_context),
            "is_not": [
                "Not a final truth claim.",
                "Not approval for production action.",
                "Not an autonomous execution decision.",
            ],
            "distinctions": [
                f"Impact tier: {impact.get('impact_tier', 'UNKNOWN')}",
                f"Impact confidence: {impact.get('impact_confidence', 'UNKNOWN')}",
                f"Observed signals: {len(case_context.get('observations', []))}",
                (
                    "Human approval required: "
                    f"{case_context['human_approval_required']}"
                ),
            ],
            "recent_lifecycle_events": [
                record.get("summary", "")
                for record in case_context.get("context_records", {}).get(
                    "change_context",
                    [],
                )
                if record.get("summary")
            ],
            "possible_causes": [
                {
                    "hypothesis_id": hypothesis["hypothesis_id"],
                    "summary": hypothesis["summary"],
                    "confidence": hypothesis["confidence"],
                }
                for hypothesis in hypotheses
            ],
            "most_probable_hypothesis": selected_hypothesis["hypothesis_id"],
        }

    def _is_statements(self, case_context: dict[str, Any]) -> list[str]:
        observations = [
            observation.get("summary", "")
            for observation in case_context.get("observations", [])[:5]
            if observation.get("summary")
        ]

        if observations:
            return observations

        return [case_context["case_summary"]]

    def _why_chain(
        self,
        *,
        case_context: dict[str, Any],
        fusion: dict[str, Any],
        selected_hypothesis: dict[str, Any],
    ) -> list[dict[str, str]]:
        return [
            {
                "question": "Why is this case being reasoned about?",
                "answer": case_context["case_summary"],
            },
            {
                "question": "Why is this hypothesis selected?",
                "answer": selected_hypothesis["summary"],
            },
            {
                "question": "Why is confidence bounded?",
                "answer": (
                    f"Fusion confidence is {fusion['fusion_confidence']} with "
                    f"{len(fusion['weakening_evidence'])} weakening, "
                    f"{len(fusion['conflicting_evidence'])} conflicting, and "
                    f"{len(fusion['missing_evidence'])} missing evidence items."
                ),
            },
            {
                "question": "Why is human review still required?",
                "answer": (
                    "The reasoning package explains evidence fit but does not authorize action."
                ),
            },
        ]

    def _ids(self, records: list[dict[str, Any]]) -> list[str]:
        return [
            record["evidence_id"]
            for record in records
            if "evidence_id" in record
        ]

    def _ids_by_type(
        self,
        records: list[dict[str, Any]],
        evidence_type: str,
    ) -> list[str]:
        return [
            record["evidence_id"]
            for record in records
            if record.get("evidence_type") == evidence_type
            and "evidence_id" in record
        ]

    def _bounded_confidence(self, confidence: str) -> str:
        if confidence == "HIGH":
            return "MEDIUM"

        return confidence
