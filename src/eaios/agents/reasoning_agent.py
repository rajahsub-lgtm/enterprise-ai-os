class ReasoningAgent:

    def execute(self, telemetry_result, knowledge_result):

        return {
            "summary":
                f"Service degradation detected. "
                f"Most likely cause: "
                f"{knowledge_result.get('probable_cause','Unknown')}."
        }