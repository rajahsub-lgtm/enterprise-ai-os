from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Optional


@dataclass
class Goal:
    id: str
    title: str
    description: str
    owner: str

    priority: str
    status: str = "NEW"

    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    completed_at: Optional[datetime] = None

    assigned_agent: Optional[str] = None