import json
from pathlib import Path
from typing import Any


class EvidenceStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def append(self, evidence: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)

        if self.path.exists():
            records = json.loads(self.path.read_text(encoding="utf-8"))
        else:
            records = []

        records.append(evidence)
        self.path.write_text(json.dumps(records, indent=2), encoding="utf-8")
