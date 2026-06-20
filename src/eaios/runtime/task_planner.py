from .execution_trace import ExecutionTrace


class TaskPlanner:
    """
    Determines what tasks are required
    for a capability.
    """

    TASK_MAP = {
        "Application Health Management": [
            "Collect Telemetry",
            "Analyze Logs",
            "Search Knowledge",
            "Perform KT Analysis",
            "Recommend Action"
        ]
    }

    def plan(self, trace: ExecutionTrace) -> list[str]:

        tasks = self.TASK_MAP.get(
            trace.capability,
            []
        )

        trace.tasks = tasks

        return tasks