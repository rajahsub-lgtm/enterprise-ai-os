import json
from pathlib import Path


class RegistryLoader:
    """
    Loads EAIOS governance registry data.

    Sprint 1 purpose:
    - Keep governance metadata outside code.
    - Avoid hardcoding enterprise knowledge sources.
    - Support NIST-aligned Govern / Map separation.
    """

    def __init__(self, governance_path: str = "data/governance") -> None:
        self.governance_path = Path(governance_path)

    def load_agents(self) -> list[dict]:
        return self._load_json("agents.json")

    def load_data_sources(self) -> list[dict]:
        return self._load_json("data_sources.json")

    def load_policies(self) -> list[dict]:
        return self._load_json("policies.json")

    def _load_json(self, filename: str) -> list[dict]:
        file_path = self.governance_path / filename

        if not file_path.exists():
            raise FileNotFoundError(f"Governance registry not found: {file_path}")

        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)