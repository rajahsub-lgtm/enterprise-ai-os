class StrategySelector:
    """
    Selects an execution strategy based on
    operational confidence.
    """

    def select(self, confidence: dict | None = None) -> dict:

        strategy = (
            confidence["recommended_strategy"]
            if confidence
            else "Known Error Accelerated Validation"
        )

        return {
            "situation": "Known Error Detected",
            "occurrences": 147,
            "historical_success_rate": "98%",
            "strategy": strategy,
            "skipped_activities": [
                "Broad Knowledge Search",
                "Full Root Cause Investigation",
            ],
            "reason": (
                "This issue has been successfully resolved repeatedly.\n\n"
                "Enterprise learning indicates a high-confidence historical resolution.\n\n"
                "EAIOS performs targeted due diligence to validate the current "
                "situation before following the Accelerated Validation Path."
            ),
            "recommended_action": "restart payment connector",
            "human_validation": "Required",
        }