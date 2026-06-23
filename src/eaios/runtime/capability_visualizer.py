from .execution_trace import ExecutionTrace


class CapabilityVisualizer:
    """
    Renders a human-readable capability map.
    """

    def render(self, trace: ExecutionTrace) -> str:
        return f"""
==================================================
EAIOS CAPABILITY MAP
==================================================

Business Outcome:
{trace.business_outcome}

Capability:
{trace.capability}

Data Collection Skills
----------------------
✓ Incident Data Collection
✓ Known Error Data Collection
✓ Observability Data Collection
✓ Dependency Data Collection

Analysis Skills
---------------
✓ Log Analysis
✓ Cluster Analysis
✓ Impact Analysis
✓ Pattern Recognition

Reasoning Skills
----------------
✓ Situational Appraisal
✓ Problem Analysis
✓ Potential Problem Analysis

Decision Support Skills
-----------------------
✓ Decision Analysis
✓ Actionable Insight Generation

Skill-to-Agent Mapping
----------------------
Incident Data Collection        → Incident Analysis Agent
Known Error Data Collection     → Knowledge Agent
Observability Data Collection   → Telemetry Agent
Dependency Data Collection      → Solution 360 Agent
Log Analysis                    → Log Analysis Agent
Cluster Analysis                → Incident Analysis Agent
Impact Analysis                 → Business Impact Agent
Pattern Recognition             → Pattern Recognition Agent
Problem Analysis                → Reasoning Agent
Decision Analysis               → Recommendation Agent
Actionable Insight Generation   → Recommendation Agent

Interpretation
--------------
EAIOS shows how a business outcome is supported by an
enterprise capability, decomposed into reusable skills,
and implemented by governed agents.

==================================================
"""