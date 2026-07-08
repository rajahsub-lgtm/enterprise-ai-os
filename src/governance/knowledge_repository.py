"""
Classification: EAIOS Core

Loads governed mock knowledge items for the governed retrieval seam.

This repository is a test harness for Sprint 2.5 Phase 0.5. It does not
bypass Governance Broker, EvidenceFactory, ContentSafetyGateway, Audit, or
EvidenceStore. It only returns items after the caller has received an allowed
broker decision.
"""

import json
from pathlib import Path
from typing import Any


class KnowledgeRepository:
    """
    Lightweight governed mock knowledge repository.

    The repository is intentionally simple:
    - source metadata comes from the governance data source registry
    - knowledge items come from mock_knowledge_items.json
    - callers must request items by approved source_id
    """

    def __init__(
        self,
        *,
        items_path: str | Path,
        data_sources: list[dict[str, Any]],
    ) -> None:
        self.items_path = Path(items_path)
        self.source_by_id = {
            source["source_id"]: source for source in data_sources
        }

    def source_metadata(self, source_id: str) -> dict[str, Any]:
        return self.source_by_id.get(source_id, {"source_id": source_id})

    def items_for(self, source_id: str) -> list[dict[str, Any]]:
        items_by_source = self._load_items()
        return list(items_by_source.get(source_id, []))

    def _load_items(self) -> dict[str, list[dict[str, Any]]]:
        if not self.items_path.exists():
            return {}

        return json.loads(self.items_path.read_text(encoding="utf-8"))