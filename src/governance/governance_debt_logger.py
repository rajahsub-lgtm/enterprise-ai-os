import json
from datetime import datetime
from pathlib import Path
from typing import Any


class GovernanceDebtLogger:
    """
    Lightweight governance debt queue.

    Sprint 1 scope:
    - Record unknown or incomplete governance metadata.
    - Full ownership, SLA, aging, and recommended_follow_up workflow comes later.
    """

    def __init__(self, debt_path: str = "data/governance/governance_debt.json") -> None:
        self.debt_path = Path(debt_path)

    def log_debt_items(
        self,
        request_id: str,
        debt_items: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        if not debt_items:
            return []

        existing_records = self._load_existing_records()
        new_records = []

        for index, item in enumerate(debt_items, start=1):
            record = {
                "debt_id": f"gd-{request_id}-{index}",
                "request_id": request_id,
                "created_at": datetime.now().isoformat(timespec="seconds"),
                "created_by": "access_governance_system",
                "status": item.get("status", "OPEN"),
                "debt_type": item.get("debt_type", "unknown_governance_debt"),
                "missing_item": item.get("missing_item"),
                "decision": "ESCALATE",
            }
            new_records.append(record)

        existing_records.extend(new_records)
        self.debt_path.parent.mkdir(parents=True, exist_ok=True)
        self.debt_path.write_text(
            json.dumps(existing_records, indent=2),
            encoding="utf-8",
        )

        return new_records

    def _load_existing_records(self) -> list[dict[str, Any]]:
        if not self.debt_path.exists():
            return []

        return json.loads(self.debt_path.read_text(encoding="utf-8"))