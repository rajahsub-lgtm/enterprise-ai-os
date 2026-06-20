from .execution_trace import ExecutionTrace


class BusinessOutcomeManager:
    """
    Entry point for EAIOS runtime execution.

    Accepts a business outcome and creates the initial
    execution trace for the orchestration flow.
    """

    def start(self, business_outcome: str) -> ExecutionTrace:
        trace = ExecutionTrace(
            business_outcome=business_outcome
        )

        return trace