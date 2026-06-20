from .execution_trace import ExecutionTrace


class SafetyGate:
    def evaluate(self, trace: ExecutionTrace) -> str:
        if trace.capability == "Application Health Management":
            trace.safety_status = "REQUIRES_HUMAN_APPROVAL"
        else:
            trace.safety_status = "PASS"

        return trace.safety_status