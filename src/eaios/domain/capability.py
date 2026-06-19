from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Optional


@dataclass
class Capability:
    """
    Represents a stable enterprise capability.

    A capability defines WHAT the enterprise is able to do.
    It does not define HOW the capability is implemented.

    Implementations may include AI agents, humans,
    enterprise applications, or combinations thereof.
    """

    # Identity
    id: str
    name: str

    # Business Definition
    description: str

    # Governance
    owner: Optional[str] = None
    status: str = "ACTIVE"

    # Audit
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))