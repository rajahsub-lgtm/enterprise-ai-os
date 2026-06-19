from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from .reasoning_method import ReasoningMethod


@dataclass
class Reasoning:
    """
    Represents an execution of an enterprise reasoning method.
    """

    id: UUID = field(default_factory=uuid4)

    purpose: str = ""
    method: ReasoningMethod | None = None

    confidence: float = 0.0

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )