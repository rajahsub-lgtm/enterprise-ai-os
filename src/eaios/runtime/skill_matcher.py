from .execution_trace import ExecutionTrace


class SkillMatcher:
    """
    Determines what skills are required
    for completing a task.
    """

    TASK_SKILL_MAP = {

        "Collect Telemetry": [
            "Incident Data Collection",
            "Known Error Data Collection",
            "Observability Data Collection",
            "Dependency Data Collection"
        ],

        "Analyze Logs": [
            "Log Analysis",
            "Cluster Analysis",
            "Impact Analysis",
            "Pattern Recognition"
        ],

        "Search Knowledge": [
            "Information Retrieval",
            "Knowledge Base Navigation"
        ],

        "Perform KT Analysis": [
            "Situational Appraisal",
            "Problem Analysis",
            "Potential Problem Analysis"
        ],

        "Recommend Action": [
            "Decision Analysis",
            "Actionable Insight Generation"
        ]
    }

    def match(self, trace: ExecutionTrace) -> list[str]:

        skills = []

        for task in trace.tasks:
            skills.extend(
                self.TASK_SKILL_MAP.get(task, [])
            )

        trace.skills = skills

        return skills