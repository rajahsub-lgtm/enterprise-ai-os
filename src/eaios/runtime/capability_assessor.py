from .execution_trace import ExecutionTrace


class CapabilityAssessor:
    """
    Determines whether an AI capability exists
    for a business outcome.
    """

    CAPABILITY_MAP = {
        "Maintain Application Health":
            "Application Health Management"
    }

    def assess(self, trace: ExecutionTrace) -> str | None:

        capability = self.CAPABILITY_MAP.get(
            trace.business_outcome
        )

        if capability:
            trace.capability = capability

        return capability
