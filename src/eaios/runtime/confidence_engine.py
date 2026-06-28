class ConfidenceEngine:
    """
    Calculates operational confidence using both
    enterprise memory and current situation validation.

    Confidence is not based only on past success.

    EAIOS must validate whether the current situation
    sufficiently matches the historical pattern before
    applying a learned strategy.
    """

    def evaluate(self, memory_result: dict, current_context: dict) -> dict:
        historical_success = memory_result.historical_success_rate
        context_match = current_context["context_match_score"]
        recent_failure_signal = current_context["recent_failure_signal"]
        business_risk = current_context["business_risk"]

        if (
            historical_success >= 0.95
            and context_match >= 0.90
            and recent_failure_signal == "LOW"
        ):
            operational_confidence = "HIGH"
            recommended_strategy = "Known Error Accelerated Validation"
            required_validation = [
                "Confirm dependency health",
                "Confirm no recent change introduced",
                "Confirm symptom signature still matches known error",
            ]

        elif historical_success >= 0.80 and context_match >= 0.70:
            operational_confidence = "MEDIUM"
            recommended_strategy = "Targeted Investigation"
            required_validation = [
                "Search recent incidents",
                "Review dependency health",
                "Review recent changes",
                "Validate known error match",
            ]

        else:
            operational_confidence = "LOW"
            recommended_strategy = "Full Investigation"
            required_validation = [
                "Run broad knowledge search",
                "Perform full root cause analysis",
                "Escalate to human expert",
            ]

        return {
            "issue": memory_result.issue,
            "historical_success_rate": historical_success,
            "context_match_score": context_match,
            "recent_failure_signal": recent_failure_signal,
            "business_risk": business_risk,
            "operational_confidence": operational_confidence,
            "recommended_strategy": recommended_strategy,
            "required_validation": required_validation,
            "known_resolution": memory_result.known_resolution,
        }