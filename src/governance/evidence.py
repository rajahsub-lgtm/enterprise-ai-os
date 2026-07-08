from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    request_id: str
    access_decision_audit_id: str
    source_id: str
    source_owner: str | None
    item_id: str | None
    item_owner: str | None
    item_last_validated: str | None
    content_hash: str
    quality: dict[str, Any]
    usage: dict[str, Any]
    content_safety: dict[str, Any]
