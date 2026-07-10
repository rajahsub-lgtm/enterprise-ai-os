"""
Source access request.

Classification: EAIOS Core

This module defines a domain-neutral wrapper around the existing governed
access request concept.

It does not replace the existing access-governance request.
It creates a stable Sprint 3 contract that the adaptive orchestrator can emit.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SourceAccessRequest:
    case_id: str
    agent_id: str
    source_id: str
    capability: str
    goal_category: str
    purpose: str
    evidence_class: str
    query: str | None = None
    context: dict[str, Any] = field(default_factory=dict)

    def to_action_request(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "agent_id": self.agent_id,
            "subject_agent_id": self.agent_id,
            "target_agent_id": self.agent_id,
            "source_id": self.source_id,
            "resource_id": self.source_id,
            "capability": self.capability,
            "goal_category": self.goal_category,
            "purpose": self.purpose,
            "query": self.query,
            "context": self.context,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "SourceAccessRequest":
        return cls(
            case_id=value["case_id"],
            agent_id=value["agent_id"],
            source_id=value["source_id"],
            capability=value["capability"],
            goal_category=value["goal_category"],
            purpose=value["purpose"],
            evidence_class=value["evidence_class"],
            query=value.get("query"),
            context=value.get("context", {}),
        )
