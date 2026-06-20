from .execution_trace import ExecutionTrace


class ExecutionReporter:
    """
    Generates a human-readable execution report.
    """

    def generate(self, trace: ExecutionTrace) -> str:

        return f"""
==================================================
EAIOS EXECUTION REPORT
==================================================

Business Outcome:
{trace.business_outcome}

Capability:
{trace.capability}

Tasks Planned:
{len(trace.tasks)}

Skills Required:
{len(trace.skills)}

Agents Selected:
{len(trace.agents)}

Safety Status:
{trace.safety_status}

Enterprise Learning:
{trace.learning_summary}

==================================================
"""