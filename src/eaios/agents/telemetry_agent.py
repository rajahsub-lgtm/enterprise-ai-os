class TelemetryAgent:
    """
    Converts an enterprise telemetry signal into an observation.

    The Telemetry Agent observes. It does not diagnose.
    """

    def execute(self, alert: dict) -> dict:
        return {
            "observation": (
                f"Abnormal {alert['metric'].lower()} detected."
            ),
            "source": alert["source"],
            "service": alert["service"],
            "business_service": alert["business_service"],
            "severity": alert["severity"],
            "signal_type": alert["event_type"],
            "current_value": alert["current_value"],
            "threshold": alert["threshold"],
            "requires_enterprise_reasoning": True,
        }