from dataclasses import dataclass, field
from typing import Any


@dataclass
class ActionRequest:
    """
    Runtime request for an agent action.

    This is the EAIOS Map object:
    - Who is calling?
    - Which agent is being invoked?
    - What capability is requested?
    - Under what Goal Context?
    - Which sources are requested?
    """

    request_id: str
    caller_agent_id: str
    target_agent_id: str
    requested_capability: str
    goal_context: dict[str, Any]
    requested_sources: list[str]
    risk_context: dict[str, Any] = field(default_factory=dict)
    business_justification: str | None = None