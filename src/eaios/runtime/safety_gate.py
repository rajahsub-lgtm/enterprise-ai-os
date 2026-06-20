from .execution_trace import ExecutionTrace


class SafetyGate:
    """
    Evaluates whether execution is safe to continue.

    Rev 1 keeps safety simple:
    all executions pass, but the safety checkpoint
    is explicitly recorded.
    """

    def evaluate(self, trace: ExecutionTrace) -> str:
        trace.safety_status = "PASS"

        return trace.safety_status