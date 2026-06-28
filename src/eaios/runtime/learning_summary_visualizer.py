class LearningSummaryVisualizer:
    """
    Displays how EAIOS learning changed Enterprise Memory.
    """

    def render(self, updated_memory) -> str:

        return f"""
==================================================
EAIOS LEARNING SUMMARY
==================================================

Pattern Learned
---------------
{updated_memory.issue}

Updated Occurrences
-------------------
{updated_memory.occurrences}

Historical Resolution Success
-----------------------------
{updated_memory.historical_success_rate:.0%}

Known Resolution
----------------
{updated_memory.known_resolution}

Recent Failures
---------------
{updated_memory.recent_failures}

Pattern Strength
----------------
{updated_memory.strength} / 100

Pattern Trend
-------------
{updated_memory.trend}

Last Validated
--------------
{updated_memory.last_validated}

Learning Interpretation
-----------------------
EAIOS recorded this execution as part of enterprise
learning.

Enterprise Memory now reflects updated experience
for this issue pattern.

Future executions can use this pattern to improve
operational confidence, due diligence, and strategy
selection.

Architectural Principle
-----------------------
Agents do not own learning.

The enterprise owns learning.

==================================================
"""