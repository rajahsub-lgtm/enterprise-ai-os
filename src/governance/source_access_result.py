"""
Source access result.

Classification: EAIOS Core

This module defines the normalized result of a governed source access attempt.

The result may represent:
- allowed evidence
- blocked access
- escalation / review requirement
- evidence that exists but is not eligible for reasoning
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.governance.source_access_request import SourceAccessRequest


SAFE_STATUSES = {
    "SAFE",
    "SAFE_BY_APPROVED_PROVENANCE",
}

SUPPORTED_EVIDENCE_CLASSES = {
    "free_text_evidence",
    "structured_record_evidence",
    "memory_state_evidence",
}


@dataclass(frozen=True)
class SourceAccessResult:
    case_id: str
    agent_id: str
    source_id: str
    capability: str
    goal_category: str
    purpose: str
    evidence_class: str
    access_decision: str
    audit_id: str | None
    evidence_id: str | None
    content_safety_status: str | None
    allowed_for_reasoning: bool
    payload: dict[str, Any] | None = None
    reason: str | None = None
    required_controls: list[str] = field(default_factory=list)

    @classmethod
    def denied(
        cls,
        request: SourceAccessRequest,
        *,
        reason: str,
        audit_id: str | None = None,
        required_controls: list[str] | None = None,
    ) -> "SourceAccessResult":
        return cls(
            case_id=request.case_id,
            agent_id=request.agent_id,
            source_id=request.source_id,
            capability=request.capability,
            goal_category=request.goal_category,
            purpose=request.purpose,
            evidence_class=request.evidence_class,
            access_decision="DENY",
            audit_id=audit_id,
            evidence_id=None,
            content_safety_status=None,
            allowed_for_reasoning=False,
            payload=None,
            reason=reason,
            required_controls=required_controls or [],
        )

    @classmethod
    def from_governed_output(
        cls,
        request: SourceAccessRequest,
        governed_output: dict[str, Any],
    ) -> list["SourceAccessResult"]:
        decision = (
            governed_output.get("access_decision")
            or governed_output.get("decision")
            or governed_output.get("governance_decision")
        )

        audit_id = (
            governed_output.get("audit_id")
            or governed_output.get("access_audit_id")
            or governed_output.get("governance_audit_id")
        )

        if decision != "ALLOW":
            return [
                cls.denied(
                    request,
                    reason=governed_output.get("reason", "Access was not allowed."),
                    audit_id=audit_id,
                    required_controls=governed_output.get("required_controls", []),
                )
            ]

        evidence_records = cls._extract_evidence_records(governed_output)

        if not evidence_records:
            return [
                cls.denied(
                    request,
                    reason="Governed access returned no evidence records.",
                    audit_id=audit_id,
                    required_controls=governed_output.get("required_controls", []),
                )
            ]

        return [
            cls._from_evidence_record(
                request=request,
                record=record,
                fallback_audit_id=audit_id,
                required_controls=governed_output.get("required_controls", []),
            )
            for record in evidence_records
        ]

    @staticmethod
    def _extract_evidence_records(governed_output: dict[str, Any]) -> list[dict[str, Any]]:
        for key in [
            "evidence_items",
            "evidence",
            "stored_evidence",
            "evidence_for_reasoning",
            "results",
        ]:
            value = governed_output.get(key)
            if isinstance(value, list):
                return value

        single = governed_output.get("evidence_item")
        if isinstance(single, dict):
            return [single]

        return []

    @classmethod
    def _from_evidence_record(
        cls,
        *,
        request: SourceAccessRequest,
        record: dict[str, Any],
        fallback_audit_id: str | None,
        required_controls: list[str],
    ) -> "SourceAccessResult":
        evidence_id = record.get("evidence_id") or record.get("id")
        audit_id = (
            record.get("audit_id")
            or record.get("access_audit_id")
            or fallback_audit_id
        )
        safety_status = (
            record.get("content_safety_status")
            or record.get("safety_status")
            or record.get("classification_status")
        )

        allowed_for_reasoning = bool(
            record.get("allowed_for_reasoning")
            if "allowed_for_reasoning" in record
            else safety_status in SAFE_STATUSES
        )

        return cls(
            case_id=request.case_id,
            agent_id=request.agent_id,
            source_id=request.source_id,
            capability=request.capability,
            goal_category=request.goal_category,
            purpose=request.purpose,
            evidence_class=request.evidence_class,
            access_decision="ALLOW",
            audit_id=audit_id,
            evidence_id=evidence_id,
            content_safety_status=safety_status,
            allowed_for_reasoning=allowed_for_reasoning,
            payload=record,
            reason=record.get("reason"),
            required_controls=required_controls,
        )

    def to_evidence_item(self) -> dict[str, Any]:
        if self.access_decision != "ALLOW":
            raise ValueError("Only allowed access results can become evidence items.")

        if self.evidence_class not in SUPPORTED_EVIDENCE_CLASSES:
            raise ValueError(f"Unsupported evidence_class: {self.evidence_class}")

        return {
            "case_id": self.case_id,
            "agent_id": self.agent_id,
            "source_id": self.source_id,
            "capability": self.capability,
            "goal_category": self.goal_category,
            "purpose": self.purpose,
            "access_decision": self.access_decision,
            "audit_id": self.audit_id,
            "evidence_id": self.evidence_id,
            "content_safety_status": self.content_safety_status,
            "allowed_for_reasoning": self.allowed_for_reasoning,
            "evidence_class": self.evidence_class,
            "required_controls": self.required_controls,
            "payload": self.payload or {},
        }

    def to_evidence_gap(self) -> dict[str, Any]:
        return {
            "gap_id": f"GAP-{self.case_id}-{self.agent_id}-{self.source_id}",
            "case_id": self.case_id,
            "agent_id": self.agent_id,
            "source_id": self.source_id,
            "capability": self.capability,
            "goal_category": self.goal_category,
            "purpose": self.purpose,
            "access_decision": self.access_decision,
            "audit_id": self.audit_id,
            "reason": self.reason or "No reasoning-eligible evidence was produced.",
            "required_controls": self.required_controls,
        }
