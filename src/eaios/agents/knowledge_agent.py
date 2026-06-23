class KnowledgeAgent:

    def execute(self, incidents, knowledge):

        symptom = incidents["recent_incidents"][0]["symptom"]

        for error in knowledge["known_errors"]:

            if error["symptom"] == symptom:

                return {
                    "finding": "Known error matched",
                    "probable_cause": error["probable_cause"],
                    "recommended_action": error["recommended_action"]
                }

        return {
            "finding": "No known error found"
        }