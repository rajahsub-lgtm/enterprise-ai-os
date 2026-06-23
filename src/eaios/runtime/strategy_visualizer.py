class StrategyVisualizer:
    """
    Renders the selected EAIOS execution strategy.
    """

    def render(self, strategy: dict) -> str:
        skipped = "\n".join(
            f"✓ {activity}" for activity in strategy["skipped_activities"]
        )

        return f"""
==================================================
EAIOS EXECUTION STRATEGY
==================================================

Situation Assessment
--------------------
{strategy["situation"]}

Occurrences
-----------
{strategy["occurrences"]}

Historical Success Rate
-----------------------
{strategy["historical_success_rate"]}

Selected Strategy
-----------------
{strategy["strategy"]}

Skipped Activities
------------------
{skipped}

Reason
------
{strategy["reason"]}

Recommended Action
------------------
{strategy["recommended_action"]}

Human Validation
----------------
{strategy["human_validation"]}

==================================================
"""