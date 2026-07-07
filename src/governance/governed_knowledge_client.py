from typing import Any

from .action_request import ActionRequest
from .governance_broker import GovernanceBroker


class GovernedKnowledgeClient:
    """
    Governed client exposed to the Knowledge Agent.

    Sprint 1 principle:
    The Knowledge Agent receives this governed client, not raw source handles.
    """

    def __init__(self, broker: GovernanceBroker) -> None:
        self.broker = broker

    def request_knowledge_access(self, request: ActionRequest) -> dict[str, Any]:
        return self.broker.enforce_knowledge_access(request)