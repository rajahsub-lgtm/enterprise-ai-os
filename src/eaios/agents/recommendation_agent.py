class RecommendationAgent:

    def execute(self, reasoning_result, knowledge_result):

        return {
            "recommendation":
                knowledge_result.get(
                    "recommended_action",
                    "Investigate manually"
                ),
            "requires_human_approval": True
        }