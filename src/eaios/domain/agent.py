from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Optional


@dataclass
class Agent:
    """
    An AI implementation of one or more enterprise capabilities.
    """

    # Identity
    id: str
    name: str

    # Business
    capability_id: str

    # Lifecycle
    version: str = "0.1"
    status: str = "AVAILABLE"

    # Governance
    owner: Optional[str] = None

    # Audit
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))