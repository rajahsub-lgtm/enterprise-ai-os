from .execution_trace import ExecutionTrace


class AgentOrchestrator:
    """
    Selects agents that can perform the required skills.
    """

    SKILL_AGENT_MAP = {
        "Incident Data Collection": "Telemetry Agent",
        "Known Error Data Collection": "Knowledge Agent",
        "Observability Data Collection": "Telemetry Agent",
        "Dependency Data Collection": "Solution 360 Agent",

        "Log Analysis": "Log Analysis Agent",
        "Cluster Analysis": "Incident Analysis Agent",
        "Impact Analysis": "Business Impact Agent",
        "Pattern Recognition": "Pattern Recognition Agent",

        "Information Retrieval": "Knowledge Agent",
        "Knowledge Base Navigation": "Knowledge Agent",

        "Situational Appraisal": "Reasoning Agent",
        "Problem Analysis": "Reasoning Agent",
        "Potential Problem Analysis": "Reasoning Agent",

        "Decision Analysis": "Recommendation Agent",
        "Actionable Insight Generation": "Recommendation Agent",
    }

    def orchestrate(self, trace: ExecutionTrace) -> list[str]:
        agents = []

        for skill in trace.skills:
            agent = self.SKILL_AGENT_MAP.get(skill)

            if agent and agent not in agents:
                agents.append(agent)

        trace.agents = agents

        return agents