from typing import Any

from .action_request import ActionRequest


class GovernanceBroker:
    """
    Policy Enforcement Point (PEP) for governed EAIOS access.

    Sprint 1 scope:
    - Enforce AGS/PDP decisions for Knowledge Agent source access.
    - Write audit records before allowing governed access.
    - Fail closed if mandatory audit cannot be written.
    """

    def __init__(
        self,
        ags,
        audit_logger,
        governance_debt_logger,
    ) -> None:
        self.ags = ags
        self.audit_logger = audit_logger
        self.governance_debt_logger = governance_debt_logger

    def enforce_knowledge_access(self, request: ActionRequest) -> dict[str, Any]:
        decision = self.ags.evaluate(request)

        if decision.get("governance_debt"):
            self.governance_debt_logger.log_debt_items(
                request_id=request.request_id,
                debt_items=decision["governance_debt"],
            )

        try:
            audit_record = self.audit_logger.log_decision(decision)
        except Exception as error:
            fail_closed_decision = self._fail_closed_decision(
                request=request,
                reason=f"Mandatory audit failed: {error}",
            )
            return {
                "allowed": False,
                "accessible_sources": [],
                "decision": fail_closed_decision,
            }

        decision["audit_id"] = audit_record.get("audit_id")

        if "record_hash" in audit_record:
            decision["record_hash"] = audit_record["record_hash"]

        if decision["decision"] == "APPROVED_WITH_CONTROLS":
            return {
                "allowed": True,
                "accessible_sources": decision["approved_sources"],
                "decision": decision,
                "retrieval_result": {
                    "type": "mock_governed_retrieval_result",
                    "source_count": len(decision["approved_sources"]),
                },
            }

        return {
            "allowed": False,
            "accessible_sources": [],
            "decision": decision,
        }

    def _fail_closed_decision(
        self,
        request: ActionRequest,
        reason: str,
    ) -> dict[str, Any]:
        return {
            "request_id": request.request_id,
            "caller_agent_id": request.caller_agent_id,
            "target_agent_id": request.target_agent_id,
            "requested_capability": request.requested_capability,
            "requested_sources": request.requested_sources,
            "goal_context": request.goal_context,
            "risk_context": request.risk_context,
            "business_justification": request.business_justification,
            "decision": "FAIL_CLOSED",
            "reason": reason,
            "policy_id": "POL-FAIL-CLOSED-001",
            "approved_sources": [],
            "denied_sources": request.requested_sources,
            "escalated_sources": [],
            "required_controls": [
                "manual_review_required",
                "governance_recovery_required",
            ],
            "governance_debt": [],
            "nist_trace": {
                "govern": "Mandatory auditability is required.",
                "map": "Governed request could not be safely completed.",
                "measure": "Audit control failure detected.",
                "manage": "Access blocked fail-closed.",
            },
        }