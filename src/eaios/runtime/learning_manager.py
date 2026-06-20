from .execution_trace import ExecutionTrace


class LearningManager:
    """
    Captures enterprise learning from an execution.
    """

    def capture(self, trace: ExecutionTrace) -> str:
        trace.learning_summary = (
            "Execution completed. "
            "Review what went right, what went wrong, "
            "human interventions, safety outcomes, "
            "capability gaps, and improvement opportunities."
        )

        return trace.learning_summary
