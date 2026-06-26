class AgentSelectionVisualizer:
    """
    Displays how EAIOS selects the best implementation
    for a required enterprise skill.
    """

    def render(self, selection: dict) -> str:

        output = f"""
==================================================
EAIOS AGENT SELECTION
==================================================

Skill Required
--------------
{selection["skill"]}

Business Context
----------------
{selection["context"]}

Candidate Implementations
-------------------------
"""

        for candidate in selection["candidates"]:
            output += (
                f"\n• {candidate['name']}"
                f"\n    Scope   : {candidate['knowledge_scope']}"
                f"\n    Best For: {candidate['best_for']}"
                f"\n    Success : {candidate['historical_success_rate']:.0%}"
                f"\n    Cost    : {candidate['cost']}"
                f"\n    Risk    : {candidate['risk']}\n"
            )

        selected = selection["selected"]

        output += f"""

Selected Implementation
-----------------------
{selected["name"]}

Selection Reason
----------------
{selection["reason"]}

Enterprise Interpretation
-------------------------
EAIOS selected the implementation that best fits the
current business context using accumulated enterprise
learning and historical performance.

Future Evolution
----------------
Future versions will consider:

✓ Business context
✓ Situation awareness
✓ Historical success
✓ Cost
✓ Latency
✓ Governance policies
✓ Risk
✓ Human feedback
✓ Multi-agent collaboration
✓ Collective Intelligence

==================================================
"""

        return output