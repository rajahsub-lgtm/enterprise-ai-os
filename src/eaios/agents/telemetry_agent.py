class TelemetryAgent:

    def execute(self, telemetry):

        if telemetry["error_rate"] > 5:

            return {
                "finding": "High error rate detected",
                "severity": "HIGH",
                "service": telemetry["service"]
            }

        return {
            "finding": "No issues detected",
            "severity": "LOW"
        }