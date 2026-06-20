from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4


@dataclass
class ExecutionTrace:
    """
    Records what happened during one EAIOS execution.

    Rev 1 traceability is intentionally lightweight.
    Full AgentOps comes later.
    """

    id: UUID = field(default_factory=uuid4)

    business_outcome: str = ""
    capability: str = ""

    tasks: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    agents: list[str] = field(default_factory=list)

    safety_status: str = "NOT_EVALUATED"
    reasoning_summary: str = ""
    recommendation: str = ""
    learning_summary: str = ""

    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def record_task(self, task: str) -> None:
        self.tasks.append(task)

    def record_skill(self, skill: str) -> None:
        self.skills.append(skill)

    def record_agent(self, agent: str) -> None:
        self.agents.append(agent)