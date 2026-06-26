class ConfidenceVisualizer:
    """
    Displays how EAIOS evaluates operational confidence
    using both enterprise memory and current context.
    """

    def render(self, confidence: dict) -> str:
        validations = "\n".join(
            f"✓ {item}" for item in confidence["required_validation"]
        )

        return f"""
==================================================
EAIOS OPERATIONAL CONFIDENCE
==================================================

Known Issue
-----------
{confidence["issue"]}

Historical Resolution Success
-----------------------------
{confidence["historical_success_rate"]:.0%}

Current Situation Match
-----------------------
{confidence["context_match_score"]:.0%}

Recent Failure Signal
---------------------
{confidence["recent_failure_signal"]}

Business Risk
-------------
{confidence["business_risk"]}

Operational Confidence
----------------------
{confidence["operational_confidence"]}

Recommended Strategy
--------------------
{confidence["recommended_strategy"]}

Known Resolution
----------------
{confidence["known_resolution"]}

Targeted Due Diligence
----------------------
{validations}

Interpretation
--------------
Operational confidence accelerates execution,
but it does not eliminate due diligence.

EAIOS combines enterprise learning with current
situation validation before selecting an
execution strategy.

==================================================
"""