from .execution_trace import ExecutionTrace


class ExecutionReporter:
    """
    Generates a human-readable execution report.
    """

    def generate(
        self,
        trace: ExecutionTrace,
        telemetry_result: dict | None = None,
        knowledge_result: dict | None = None,
        reasoning_result: dict | None = None,
        recommendation_result: dict | None = None,
    ) -> str:

        evidence = "No telemetry evidence available"

        if telemetry_result:
            evidence = telemetry_result.get(
                "observation",
                telemetry_result.get(
                    "finding",
                    "No telemetry evidence available",
                ),
            )

        return f"""
==================================================
EAIOS EXECUTION REPORT
==================================================

Business Outcome:
{trace.business_outcome}

Capability:
{trace.capability}

Current Assessment:
{telemetry_result.get("severity", "UNKNOWN") if telemetry_result else "UNKNOWN"}

Service:
{telemetry_result.get("service", "UNKNOWN") if telemetry_result else "UNKNOWN"}

Evidence:
---------
{evidence}

Knowledge Match:
{knowledge_result.get("finding", "No knowledge match available") if knowledge_result else "No knowledge match available"}

Probable Cause:
{knowledge_result.get("probable_cause", "UNKNOWN") if knowledge_result else "UNKNOWN"}

Reasoning Summary:
{reasoning_result.get("summary", "No reasoning summary available") if reasoning_result else "No reasoning summary available"}

Recommendation:
{recommendation_result.get("recommendation", "No recommendation available") if recommendation_result else "No recommendation available"}

Human Approval Required:
{recommendation_result.get("requires_human_approval", "UNKNOWN") if recommendation_result else "UNKNOWN"}

Safety Status:
{trace.safety_status}

Enterprise Learning:
{trace.learning_summary}

==================================================
"""