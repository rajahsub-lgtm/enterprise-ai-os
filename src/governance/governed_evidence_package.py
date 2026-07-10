"""
Governed evidence package.

Classification: EAIOS Core

A governed evidence package is the domain-neutral bridge between governed
source access and evidence fusion.

Fusion should consume this package rather than raw source records.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.governance.source_access_result import SourceAccessResult


@dataclass(frozen=True)
class GovernedEvidencePackage:
    package_id: str
    case_id: str
    evidence_items: list[dict[str, Any]]
    evidence_gaps: list[dict[str, Any]]

    @classmethod
    def from_results(
        cls,
        *,
        case_id: str,
        results: list[SourceAccessResult],
    ) -> "GovernedEvidencePackage":
        evidence_items: list[dict[str, Any]] = []
        evidence_gaps: list[dict[str, Any]] = []

        for result in results:
            if result.access_decision == "ALLOW":
                item = result.to_evidence_item()
                evidence_items.append(item)

                if not item["allowed_for_reasoning"]:
                    evidence_gaps.append(
                        {
                            "gap_id": (
                                f"GAP-{case_id}-{item['agent_id']}-{item['source_id']}"
                            ),
                            "case_id": case_id,
                            "agent_id": item["agent_id"],
                            "source_id": item["source_id"],
                            "capability": item["capability"],
                            "goal_category": item["goal_category"],
                            "purpose": item["purpose"],
                            "access_decision": item["access_decision"],
                            "audit_id": item["audit_id"],
                            "reason": (
                                "Evidence was collected but is not eligible for reasoning."
                            ),
                            "required_controls": item["required_controls"],
                        }
                    )
            else:
                evidence_gaps.append(result.to_evidence_gap())

        return cls(
            package_id=f"GEP-{case_id}",
            case_id=case_id,
            evidence_items=evidence_items,
            evidence_gaps=evidence_gaps,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "package_id": self.package_id,
            "case_id": self.case_id,
            "evidence_items": self.evidence_items,
            "evidence_gaps": self.evidence_gaps,
        }

    def evidence_for_reasoning(self) -> list[dict[str, Any]]:
        return [
            item
            for item in self.evidence_items
            if item.get("allowed_for_reasoning") is True
        ]

    def excluded_evidence(self) -> list[dict[str, Any]]:
        return [
            item
            for item in self.evidence_items
            if item.get("allowed_for_reasoning") is not True
        ]
