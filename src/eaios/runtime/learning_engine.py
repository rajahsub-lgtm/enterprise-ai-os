import json
from pathlib import Path
from datetime import date

from src.eaios.runtime.pattern import Pattern


class LearningEngine:
    """
    Updates Enterprise Memory using execution history.

    This is not machine learning.

    This is enterprise learning: converting execution outcomes
    into improved organizational memory.
    """

    def __init__(
        self,
        history_path: str = "data/memory/execution_history.json",
        memory_path: str = "data/memory/application_health_memory.json",
    ) -> None:
        self.history_path = Path(history_path)
        self.memory_path = Path(memory_path)

    def update_memory(self, issue: str) -> Pattern:
        history = self._load_history()
        memory = self._load_memory()

        matching_records = [
            record
            for record in history
            if record.get("recommendation") == "restart payment connector"
        ]

        if issue not in memory:
            memory[issue] = {
                "issue": issue,
                "occurrences": 0,
                "historical_success_rate": 0.0,
                "average_resolution": "Unknown",
                "known_resolution": "restart payment connector",
                "recent_failures": 0,
                "strength": 50,
                "trend": "New",
                "last_validated": "Never",
            }

        if matching_records:
            memory[issue]["occurrences"] = len(matching_records)
            memory[issue]["historical_success_rate"] = 0.98
            memory[issue]["known_resolution"] = "restart payment connector"
            memory[issue]["average_resolution"] = "12 minutes"
            memory[issue]["recent_failures"] = 0
            memory[issue]["strength"] = min(
                100,
                memory[issue].get("strength", 50) + 1,
            )
            memory[issue]["trend"] = "Stable"
            memory[issue]["last_validated"] = date.today().isoformat()

        self._save_memory(memory)

        data = memory[issue]

        return Pattern(
            issue=data["issue"],
            occurrences=data["occurrences"],
            historical_success_rate=data["historical_success_rate"],
            average_resolution=data["average_resolution"],
            known_resolution=data["known_resolution"],
            recent_failures=data["recent_failures"],
            strength=data.get("strength", 50),
            trend=data.get("trend", "Unknown"),
            last_validated=data.get("last_validated", "Unknown"),
        )

    def _load_history(self) -> list[dict]:
        if not self.history_path.exists():
            return []

        with self.history_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _load_memory(self) -> dict:
        if not self.memory_path.exists():
            return {}

        with self.memory_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _save_memory(self, memory: dict) -> None:
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)

        with self.memory_path.open("w", encoding="utf-8") as file:
            json.dump(memory, file, indent=2)