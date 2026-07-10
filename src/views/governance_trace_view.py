"""
Governance trace view-model.

Classification: EAIOS Core

This module converts orchestration trace data into a UI-ready governance trace
view. It does not invent governance state, approval state, evidence state, or
safety state.

The future UI should render this view-model directly.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class GovernanceTraceRow:
    agent_id: str
    source_id: str
    source_access_purpose: str | None
    governance_decision: str | None
    audit_id: str | None
    evidence_id: str | None
    content_safety_status: str | None
    allowed_for_reasoning: bool | None
    required_controls: list[str]
    approval_state: str
    autonomous_action_allowed: bool
    reason: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "source_id": self.source_id,
            "source_access_purpose": self.source_access_purpose,
            "governance_decision": self.governance_decision,
            "audit_id": self.audit_id,
            "evidence_id": self.evidence_id,
            "content_safety_status": self.content_safety_status,
            "allowed_for_reasoning": self.allowed_for_reasoning,
            "required_controls": self.required_controls,
            "approval_state": self.approval_state,
            "autonomous_action_allowed": self.autonomous_action_allowed,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class GovernanceTraceView:
    trace_id: str
    case_id: str
    rows: list[GovernanceTraceRow] = field(default_factory=list)
    governance_required: bool = True
    human_approval_required: bool = True
    autonomous_action_allowed: bool = False

    @classmethod
    def from_orchestration_trace(
        cls,
        trace: dict[str, Any],
    ) -> "GovernanceTraceView":
        if trace.get("governance_required") is not True:
            raise ValueError("governance_required must be True in trace view input.")

        if trace.get("human_approval_required") is not True:
            raise ValueError("human_approval_required must be True in trace view input.")

        if trace.get("autonomous_action_allowed") is not False:
            raise ValueError(
                "autonomous_action_allowed must be False in trace view input."
            )

        rows = [
            cls._row_from_step(
                step=step,
                human_approval_required=trace.get("human_approval_required", True),
                autonomous_action_allowed=trace.get(
                    "autonomous_action_allowed",
                    False,
                ),
            )
            for step in trace.get("agent_steps", [])
            if step.get("source_id") is not None
            and step.get("governance_decision") not in {None, "PENDING"}
        ]

        return cls(
            trace_id=trace["trace_id"],
            case_id=trace["case_id"],
            rows=rows,
            governance_required=True,
            human_approval_required=True,
            autonomous_action_allowed=False,
        )

    @staticmethod
    def _row_from_step(
        *,
        step: dict[str, Any],
        human_approval_required: bool,
        autonomous_action_allowed: bool,
    ) -> GovernanceTraceRow:
        return GovernanceTraceRow(
            agent_id=step["agent_id"],
            source_id=step["source_id"],
            source_access_purpose=step.get("source_access_purpose"),
            governance_decision=step.get("governance_decision"),
            audit_id=step.get("audit_id"),
            evidence_id=step.get("evidence_id"),
            content_safety_status=step.get("content_safety_status"),
            allowed_for_reasoning=step.get("allowed_for_reasoning"),
            required_controls=list(step.get("required_controls", [])),
            approval_state=GovernanceTraceView._approval_state(
                human_approval_required=human_approval_required,
                governance_decision=step.get("governance_decision"),
                allowed_for_reasoning=step.get("allowed_for_reasoning"),
            ),
            autonomous_action_allowed=autonomous_action_allowed,
            reason=step.get("reason"),
        )

    @staticmethod
    def _approval_state(
        *,
        human_approval_required: bool,
        governance_decision: str | None,
        allowed_for_reasoning: bool | None,
    ) -> str:
        if governance_decision == "DENY":
            return "BLOCKED_BY_GOVERNANCE"

        if allowed_for_reasoning is False:
            return "NOT_ELIGIBLE_FOR_REASONING"

        if human_approval_required:
            return "PENDING_HUMAN_REVIEW"

        return "NOT_REQUIRED"

    def rows_for_decision(self, governance_decision: str) -> list[dict[str, Any]]:
        return [
            row.to_dict()
            for row in self.rows
            if row.governance_decision == governance_decision
        ]

    def reasoning_eligible_rows(self) -> list[dict[str, Any]]:
        return [
            row.to_dict()
            for row in self.rows
            if row.allowed_for_reasoning is True
        ]

    def blocked_rows(self) -> list[dict[str, Any]]:
        return [
            row.to_dict()
            for row in self.rows
            if row.governance_decision == "DENY"
            or row.allowed_for_reasoning is False
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "case_id": self.case_id,
            "rows": [row.to_dict() for row in self.rows],
            "governance_required": self.governance_required,
            "human_approval_required": self.human_approval_required,
            "autonomous_action_allowed": self.autonomous_action_allowed,
            "summary": {
                "total_rows": len(self.rows),
                "allowed_rows": len(self.rows_for_decision("ALLOW")),
                "denied_rows": len(self.rows_for_decision("DENY")),
                "reasoning_eligible_rows": len(self.reasoning_eligible_rows()),
                "blocked_rows": len(self.blocked_rows()),
            },
        }
