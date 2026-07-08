from __future__ import annotations

import hashlib
from typing import Any

from src.governance.content_safety_gateway import ContentSafetyGateway
from src.governance.evidence_quality_scorer import EvidenceQualityScorer


class EvidenceFactory:
    """
    Creates governed Evidence objects from approved mock knowledge retrieval results.
    """

    def __init__(
        self,
        *,
        quality_scorer: EvidenceQualityScorer,
        content_safety_gateway: ContentSafetyGateway,
    ) -> None:
        self.quality_scorer = quality_scorer
        self.content_safety_gateway = content_safety_gateway

    def create_evidence(
        self,
        *,
        request_id: str,
        access_decision_audit_id: str,
        source_metadata: dict[str, Any],
        knowledge_item: dict[str, Any],
        collected_by: str,
        collected_at: str,
    ) -> dict[str, Any]:
        content = knowledge_item.get("content", "")
        content_hash = self._content_hash(content)

        trust_level = knowledge_item.get("trust_level") or source_metadata.get("trust_level") or "unknown"

        quality = self.quality_scorer.score(
            source_metadata=source_metadata,
            knowledge_item=knowledge_item,
            trust_level=trust_level,
            collected_at=collected_at,
            content_hash=content_hash,
        )

        safety_and_usage = self.content_safety_gateway.evaluate(
            content=content,
            trust_level=trust_level,
            item_owner=knowledge_item.get("item_owner"),
            item_last_validated=knowledge_item.get("item_last_validated"),
            collected_at=collected_at,
        )

        evidence_id = self._evidence_id(
            request_id=request_id,
            access_decision_audit_id=access_decision_audit_id,
            item_id=knowledge_item.get("item_id"),
            content_hash=content_hash,
        )

        return {
            "evidence_id": evidence_id,
            "request_id": request_id,
            "access_decision_audit_id": access_decision_audit_id,
            "source_id": knowledge_item.get("source_id") or source_metadata.get("source_id"),
            "source_owner": source_metadata.get("owner"),
            "item_id": knowledge_item.get("item_id"),
            "item_owner": knowledge_item.get("item_owner"),
            "item_last_validated": knowledge_item.get("item_last_validated"),
            "classification": source_metadata.get("classification"),
            "trust_level": trust_level,
            "collected_by": collected_by,
            "collection_method": "governed_mock_retrieval",
            "collected_at": collected_at,
            "content_summary": knowledge_item.get("content_summary"),
            "content_hash": content_hash,
            "quality": quality,
            "usage": safety_and_usage["usage"],
            "content_safety": safety_and_usage["content_safety"],
        }

    def _content_hash(self, content: str) -> str:
        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        return f"sha256:{digest}"

    def _evidence_id(
        self,
        *,
        request_id: str,
        access_decision_audit_id: str,
        item_id: str | None,
        content_hash: str,
    ) -> str:
        seed = f"{request_id}|{access_decision_audit_id}|{item_id}|{content_hash}"
        digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]
        return f"ev-{digest}"