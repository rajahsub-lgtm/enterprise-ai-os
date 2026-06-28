import json
from pathlib import Path

from src.eaios.runtime.pattern import Pattern


class EnterpriseMemory:
    """
    Enterprise Memory stores organizational learning.

    This is not agent memory.

    It represents distilled enterprise experience from
    prior executions, incidents, resolutions, failures,
    human interventions, and governance outcomes.
    """

    def __init__(
        self,
        memory_path: str = "data/memory/application_health_memory.json",
    ) -> None:
        self.memory_path = Path(memory_path)

    def lookup(self, issue: str) -> Pattern:
        memory = self._load_memory()

        if issue in memory:
            data = memory[issue]

        return Pattern(
            issue=data["issue"],
            occurrences=data["occurrences"],
            historical_success_rate=data["historical_success_rate"],
            average_resolution=data["average_resolution"],
            known_resolution=data["known_resolution"],
            recent_failures=data["recent_failures"],
            strength=data.get("strength", 50),
            trend=data.get("trend", "Stable"),
            last_validated=data.get("last_validated", "Unknown"),
        )

        return Pattern(
            issue=issue,
            occurrences=0,
            historical_success_rate=0.0,
            average_resolution="Unknown",
            known_resolution="Unknown",
            recent_failures=0,
            strength=0,
            trend="Unknown",
            last_validated="Never",
        )

    def _load_memory(self) -> dict:
        if not self.memory_path.exists():
            return {}

        with self.memory_path.open("r", encoding="utf-8") as file:
            return json.load(file)