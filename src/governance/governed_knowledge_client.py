from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .action_request import ActionRequest
from .governance_broker import GovernanceBroker


class GovernedKnowledgeClient:
    """
    Governed client exposed to the Knowledge Agent.

    Sprint 1 principle:
    The Knowledge Agent receives this governed client, not raw source handles.

    Sprint 2.5 Phase 0.5 seam:
    When repository/evidence dependencies are injected, approved access flows
    through retrieval, EvidenceFactory, ContentSafetyGateway, EvidenceStore,
    and a second append-only audit event.
    """

    def __init__(
        self,
        broker: GovernanceBroker,
        knowledge_repository=None,
        evidence_factory=None,
        evidence_store=None,
        audit_logger=None,
    ) -> None:
        self.broker = broker
        self.knowledge_repository = knowledge_repository
        self.evidence_factory = evidence_factory
        self.evidence_store = evidence_store
        self.audit_logger = audit_logger

    def request_knowledge_access(self, request: ActionRequest) -> dict[str, Any]:
        result = self.broker.enforce_knowledge_access(request)

        if not result.get("allowed"):
            return result

        if not self._evidence_seam_enabled():
            return result

        decision = result["decision"]
        access_audit_id = decision["audit_id"]

        evidence_records: list[dict[str, Any]] = []
        evidence_ids: list[str] = []

        for source_id in result["accessible_sources"]:
            source_metadata = self.knowledge_repository.source_metadata(source_id)

            for knowledge_item in self.knowledge_repository.items_for(source_id):
                evidence = self.evidence_factory.create_evidence(
                    request_id=request.request_id,
                    access_decision_audit_id=access_audit_id,
                    source_metadata=source_metadata,
                    knowledge_item=knowledge_item,
                    collected_by=request.target_agent_id,
                    collected_at=self._now_iso(),
                )

                self.evidence_store.append(evidence)

                evidence_records.append(evidence)
                evidence_ids.append(evidence["evidence_id"])

        self.audit_logger.log_decision(
            {
                "request_id": request.request_id,
                "event": "evidence_created",
                "decision": "EVIDENCE_CREATED",
                "access_decision_audit_id": access_audit_id,
                "evidence_ids": evidence_ids,
            }
        )

        result["evidence"] = evidence_records
        result["evidence_for_reasoning"] = [
            evidence
            for evidence in evidence_records
            if evidence["content_safety"]["allowed_for_reasoning"]
        ]

        return result

    def _evidence_seam_enabled(self) -> bool:
        return all(
            [
                self.knowledge_repository is not None,
                self.evidence_factory is not None,
                self.evidence_store is not None,
                self.audit_logger is not None,
            ]
        )

    def _now_iso(self) -> str:
        return (
            datetime.now(timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z")
        )