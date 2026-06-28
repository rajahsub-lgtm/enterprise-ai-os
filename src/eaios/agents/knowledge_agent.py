class KnowledgeAgent:
    """
    Searches enterprise knowledge using incident context.

    MVP behavior:
    - Accepts either old incident format or new realistic list format.
    - Looks for a knowledge article whose symptoms appear in incident summaries.
    """

    def execute(self, incidents, knowledge) -> dict:
        incident_list = self._normalize_incidents(incidents)

        incident_text = " ".join(
            incident.get("summary", "").lower()
            for incident in incident_list
        )

        best_article = None

        for article in knowledge:
            symptoms = article.get("symptoms", [])

            for symptom in symptoms:
                if symptom.lower() in incident_text:
                    best_article = article
                    break

            if best_article:
                break

        if best_article:
            return {
                "finding": "Knowledge match found",
                "article": best_article["id"],
                "title": best_article["title"],
                "probable_cause": best_article["probable_cause"].lower(),
                "recommended_action": best_article["resolution"].lower(),
                "knowledge_status": best_article["status"],
                "success_rate": best_article["success_rate"],
            }

        return {
            "finding": "No knowledge match found",
            "probable_cause": "unknown",
            "recommended_action": "escalate for investigation",
            "knowledge_status": "Missing",
            "success_rate": 0.0,
        }

    def _normalize_incidents(self, incidents):
        if isinstance(incidents, list):
            return incidents

        if isinstance(incidents, dict):
            return incidents.get("recent_incidents", [])

        return []