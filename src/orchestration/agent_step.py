"""
Agent step contract.

Classification: EAIOS Core

An AgentStep records what an orchestration participant attempted, what the
governance decision was, and whether any resulting evidence is eligible for
reasoning.

This module is domain-neutral.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.governance.source_access_request import SourceAccessRequest
from src.governance.source_access_result import SourceAccessResult


@dataclass(frozen=True)
class AgentStep:
    step_id: str
    agent_id: str
    step_name: str
    status: str
    source_id: str | None = None
    source_access_purpose: str | None = None
    governance_decision: str | None = None
    audit_id: str | None = None
    evidence_id: str | None = None
    content_safety_status: str | None = None
    allowed_for_reasoning: bool | None = None
    required_controls: list[str] = field(default_factory=list)
    reason: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def planned_source_access(
        cls,
        *,
        step_id: str,
        step_name: str,
        request: SourceAccessRequest,
    ) -> "AgentStep":
        return cls(
            step_id=step_id,
            agent_id=request.agent_id,
            step_name=step_name,
            status="PLANNED",
            source_id=request.source_id,
            source_access_purpose=request.purpose,
            governance_decision="PENDING",
            allowed_for_reasoning=False,
            details={
                "case_id": request.case_id,
                "capability": request.capability,
                "goal_category": request.goal_category,
                "evidence_class": request.evidence_class,
            },
        )

    @classmethod
    def from_source_access_result(
        cls,
        *,
        step_id: str,
        step_name: str,
        result: SourceAccessResult,
    ) -> "AgentStep":
        status = "COMPLETED" if result.access_decision == "ALLOW" else "BLOCKED"

        return cls(
            step_id=step_id,
            agent_id=result.agent_id,
            step_name=step_name,
            status=status,
            source_id=result.source_id,
            source_access_purpose=result.purpose,
            governance_decision=result.access_decision,
            audit_id=result.audit_id,
            evidence_id=result.evidence_id,
            content_safety_status=result.content_safety_status,
            allowed_for_reasoning=result.allowed_for_reasoning,
            required_controls=result.required_controls,
            reason=result.reason,
            details={
                "case_id": result.case_id,
                "capability": result.capability,
                "goal_category": result.goal_category,
                "evidence_class": result.evidence_class,
            },
        )

    def is_source_access_step(self) -> bool:
        return self.source_id is not None

    def has_audit_linkage(self) -> bool:
        return self.audit_id is not None

    def has_reasoning_eligible_evidence(self) -> bool:
        return self.allowed_for_reasoning is True and self.evidence_id is not None

    def to_dict(self) -> dict[str, Any]:
        return {
            "step_id": self.step_id,
            "agent_id": self.agent_id,
            "step_name": self.step_name,
            "status": self.status,
            "source_id": self.source_id,
            "source_access_purpose": self.source_access_purpose,
            "governance_decision": self.governance_decision,
            "audit_id": self.audit_id,
            "evidence_id": self.evidence_id,
            "content_safety_status": self.content_safety_status,
            "allowed_for_reasoning": self.allowed_for_reasoning,
            "required_controls": self.required_controls,
            "reason": self.reason,
            "details": self.details,
        }
