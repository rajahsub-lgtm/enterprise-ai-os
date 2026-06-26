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

Enterprise Experience
---------------------
{strategy["occurrences"]} previous occurrences

Historical Resolution Success
-----------------------------
{strategy["historical_success_rate"]}

Selected Strategy
-----------------
{strategy["strategy"]}

Activities Deferred
-------------------
{skipped}

Execution Rationale
-------------------
{strategy["reason"]}

Recommended Action
------------------
{strategy["recommended_action"]}

Human Validation
----------------
{strategy["human_validation"]}

Operational Principle
---------------------
Enterprise learning reduces uncertainty.

It never replaces professional judgment.

==================================================
"""