from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4


@dataclass
class Decision:
    """
    Represents an enterprise decision.

    Decisions authorize recommendations.
    """

    id: UUID = field(default_factory=uuid4)

    status: str = ""

    rationale: str = ""

    approved_by: str = ""

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )