import json
from datetime import datetime
from pathlib import Path
from typing import Any


class AuditLogger:
    """
    Writes governance decisions to an audit log.

    Sprint 1 purpose:
    - Make AGS decisions auditable.
    - Preserve NIST Govern / Map / Measure / Manage trace.
    - Support future Enterprise Command Center visibility.
    """

    def __init__(self, audit_path: str = "data/governance/audit_log.json") -> None:
        self.audit_path = Path(audit_path)

    def log_decision(self, decision: dict[str, Any]) -> dict[str, Any]:
        audit_record = {
            "audit_id": self._build_audit_id(decision),
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "decision": decision,
        }

        existing_records = self._load_existing_records()
        existing_records.append(audit_record)

        self.audit_path.parent.mkdir(parents=True, exist_ok=True)

        with self.audit_path.open("w", encoding="utf-8") as file:
            json.dump(existing_records, file, indent=2)

        return audit_record

    def _load_existing_records(self) -> list[dict[str, Any]]:
        if not self.audit_path.exists():
            return []

        with self.audit_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _build_audit_id(self, decision: dict[str, Any]) -> str:
        request_id = decision.get("request_id", "unknown")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"audit-{request_id}-{timestamp}"