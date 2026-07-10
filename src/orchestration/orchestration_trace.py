"""
Orchestration trace contract.

Classification: EAIOS Core

An OrchestrationTrace records the path selected by the engine, the governed
source requests made along the way, the governance decisions received, and the
evidence eligibility state exposed to downstream components.

This module does not choose the path. It records the path.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.governance.source_access_request import SourceAccessRequest
from src.orchestration.agent_step import AgentStep


@dataclass
class OrchestrationTrace:
    trace_id: str
    case_id: str
    joint_goal: str
    current_phase: str
    selected_due_diligence_level: str
    why_path_selected: str
    agent_steps: list[AgentStep] = field(default_factory=list)
    governed_source_requests: list[dict[str, Any]] = field(default_factory=list)
    governance_required: bool = True
    human_approval_required: bool = True
    autonomous_action_allowed: bool = False

    def add_step(self, step: AgentStep) -> None:
        self.agent_steps.append(step)

    def add_source_request(self, request: SourceAccessRequest) -> None:
        self.governed_source_requests.append(
            {
                "case_id": request.case_id,
                "agent_id": request.agent_id,
                "source_id": request.source_id,
                "capability": request.capability,
                "goal_category": request.goal_category,
                "purpose": request.purpose,
                "evidence_class": request.evidence_class,
            }
        )

    def audit_ids(self) -> list[str]:
        return sorted(
            {
                step.audit_id
                for step in self.agent_steps
                if step.audit_id is not None
            }
        )

    def evidence_ids(self) -> list[str]:
        return sorted(
            {
                step.evidence_id
                for step in self.agent_steps
                if step.evidence_id is not None
            }
        )

    def access_decisions(self) -> list[dict[str, Any]]:
        return [
            {
                "step_id": step.step_id,
                "agent_id": step.agent_id,
                "source_id": step.source_id,
                "governance_decision": step.governance_decision,
                "audit_id": step.audit_id,
                "reason": step.reason,
            }
            for step in self.agent_steps
            if step.source_id is not None
        ]

    def reasoning_eligibility(self) -> list[dict[str, Any]]:
        return [
            {
                "step_id": step.step_id,
                "agent_id": step.agent_id,
                "source_id": step.source_id,
                "evidence_id": step.evidence_id,
                "content_safety_status": step.content_safety_status,
                "allowed_for_reasoning": step.allowed_for_reasoning,
            }
            for step in self.agent_steps
            if step.source_id is not None
        ]

    def validation_errors(self) -> list[str]:
        errors: list[str] = []

        required_text_fields = {
            "trace_id": self.trace_id,
            "case_id": self.case_id,
            "joint_goal": self.joint_goal,
            "current_phase": self.current_phase,
            "selected_due_diligence_level": self.selected_due_diligence_level,
            "why_path_selected": self.why_path_selected,
        }

        for field_name, value in required_text_fields.items():
            if not value:
                errors.append(f"{field_name} is required")

        if self.governance_required is not True:
            errors.append("governance_required must be True")

        if self.human_approval_required is not True:
            errors.append("human_approval_required must be True")

        if self.autonomous_action_allowed is not False:
            errors.append("autonomous_action_allowed must be False")

        for step in self.agent_steps:
            if step.is_source_access_step() and step.governance_decision is None:
                errors.append(
                    f"{step.step_id} is a source access step without governance_decision"
                )

        return errors

    def is_valid(self) -> bool:
        return self.validation_errors() == []

    def to_dict(self) -> dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "case_id": self.case_id,
            "joint_goal": self.joint_goal,
            "current_phase": self.current_phase,
            "selected_due_diligence_level": self.selected_due_diligence_level,
            "why_path_selected": self.why_path_selected,
            "agent_steps": [step.to_dict() for step in self.agent_steps],
            "governed_source_requests": self.governed_source_requests,
            "access_decisions": self.access_decisions(),
            "audit_ids": self.audit_ids(),
            "evidence_ids": self.evidence_ids(),
            "reasoning_eligibility": self.reasoning_eligibility(),
            "governance_required": self.governance_required,
            "human_approval_required": self.human_approval_required,
            "autonomous_action_allowed": self.autonomous_action_allowed,
            "valid": self.is_valid(),
            "validation_errors": self.validation_errors(),
        }
