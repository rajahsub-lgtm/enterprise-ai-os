from typing import Any

from .action_request import ActionRequest


class AccessGovernanceSystem:
    """
    Policy Decision Point (PDP) for EAIOS governed actions.

    Sprint 1 scope:
    - Evaluate caller, target, capability, Goal Context, source metadata, and policies.
    - Return APPROVED_WITH_CONTROLS / DENIED / ESCALATE.
    - Keep behavior policy/data-driven where possible.
    """

    def __init__(
        self,
        agents: list[dict[str, Any]],
        data_sources: list[dict[str, Any]],
        policies: list[dict[str, Any]],
    ) -> None:
        self.agents = agents
        self.data_sources = data_sources
        self.policies = policies

        self.agent_by_id = {agent["agent_id"]: agent for agent in agents}
        self.source_by_id = {source["source_id"]: source for source in data_sources}
        self.policy_by_id = {policy["policy_id"]: policy for policy in policies}

    def evaluate(self, request: ActionRequest) -> dict[str, Any]:
        base = self._base_decision(request)

        caller = self.agent_by_id.get(request.caller_agent_id)
        if caller is None:
            return self._deny(
                base,
                reason="Caller agent is not registered.",
                policy_id="POL-AGENT-IDENTITY-001",
            )

        target = self.agent_by_id.get(request.target_agent_id)
        if target is None:
            return self._deny(
                base,
                reason="Target agent is not registered.",
                policy_id="POL-AGENT-IDENTITY-002",
            )

        if request.target_agent_id not in caller.get("allowed_target_agents", []):
            return self._deny(
                base,
                reason="Caller is not authorized to invoke target agent.",
                policy_id="POL-AGENT-CALL-001",
            )

        if request.requested_capability not in target.get("capabilities", []):
            return self._deny(
                base,
                reason="Target agent does not support requested capability.",
                policy_id="POL-CAPABILITY-001",
            )

        if not request.goal_context:
            return self._deny(
                base,
                reason="Goal Context is required for governed action.",
                policy_id="POL-GOAL-CONTEXT-001",
            )

        goal_category = request.goal_context.get("goal_category")
        if not goal_category:
            return self._deny(
                base,
                reason="Goal category is required in Goal Context.",
                policy_id="POL-GOAL-CONTEXT-001",
            )

        allowed_goal_categories = caller.get("allowed_goal_categories", [])
        if goal_category not in allowed_goal_categories:
            return self._deny(
                base,
                reason="Caller is not entitled to claimed Goal Context category.",
                policy_id="POL-GOAL-CATEGORY-ENTITLEMENT-001",
            )

        unknown_sources = [
            source_id
            for source_id in request.requested_sources
            if source_id not in self.source_by_id
        ]
        if unknown_sources:
            base["governance_debt"] = [
                {
                    "debt_type": "unknown_source",
                    "missing_item": source_id,
                    "status": "OPEN",
                }
                for source_id in unknown_sources
            ]
            return self._escalate(
                base,
                reason="Unknown source metadata is governance debt.",
                policy_id="POL-GOVERNANCE-DEBT-001",
            )

        requested_sources = [
            self.source_by_id[source_id] for source_id in request.requested_sources
        ]

        identity_decision = self._evaluate_identity_policy(
            request=request,
            goal_category=goal_category,
            base=base,
        )
        if identity_decision:
            return identity_decision

        hr_decision = self._evaluate_hr_policy(
            request=request,
            goal_category=goal_category,
            base=base,
        )
        if hr_decision:
            return hr_decision

        write_decision = self._evaluate_write_policy(
            request=request,
            base=base,
        )
        if write_decision:
            return write_decision

        for source in requested_sources:
            if not source.get("metadata_complete", True):
                if source.get("high_impact_signals"):
                    return self._deny(
                        base,
                        reason="High-risk uncertainty: required metadata is missing for a high-impact source.",
                        policy_id="POL-RISK-HIGH-UNCERTAINTY-001",
                    )

                base["governance_debt"] = [
                    {
                        "debt_type": "missing_source_metadata",
                        "missing_item": source["source_id"],
                        "status": "OPEN",
                    }
                ]
                return self._escalate(
                    base,
                    reason="Ambiguous risk: source metadata is incomplete.",
                    policy_id="POL-GOVERNANCE-DEBT-001",
                )

            if request.requested_capability not in source.get("allowed_capabilities", []):
                return self._deny(
                    base,
                    reason="Requested capability is not allowed for source.",
                    policy_id="POL-CAPABILITY-SOURCE-001",
                )

            if goal_category not in source.get("allowed_goal_categories", []):
                return self._deny(
                    base,
                    reason="Source is not allowed for this Goal Context.",
                    policy_id="POL-SOURCE-GOAL-001",
                )

        allowed_policy = self._find_allowed_policy(
            target_agent_id=request.target_agent_id,
            capability=request.requested_capability,
            goal_category=goal_category,
            requested_source_ids=request.requested_sources,
        )

        if allowed_policy is None:
            return self._escalate(
                base,
                reason="No policy mapping found for requested Goal Context and sources.",
                policy_id="POL-GOVERNANCE-DEBT-001",
            )

        required_controls = self._collect_required_controls(
            requested_sources=requested_sources,
            policy=allowed_policy,
        )

        base.update(
            {
                "decision": "APPROVED_WITH_CONTROLS",
                "reason": "Request is allowed by policy with required controls.",
                "policy_id": allowed_policy["policy_id"],
                "approved_sources": request.requested_sources,
                "denied_sources": [],
                "escalated_sources": [],
                "required_controls": required_controls,
            }
        )
        return base

    def _evaluate_identity_policy(
        self,
        request: ActionRequest,
        goal_category: str,
        base: dict[str, Any],
    ) -> dict[str, Any] | None:
        identity_policy = self.policy_by_id.get("POL-KNOWLEDGE-IDENTITY-001")
        if identity_policy is None:
            return None

        condition = identity_policy.get("condition", {})
        identity_source = condition.get("requested_source")

        if identity_source not in request.requested_sources:
            return None

        required_capability = condition.get("required_capability")
        required_goal_category = condition.get("required_goal_category")

        if request.requested_capability != required_capability:
            return self._deny(
                base,
                reason="Identity source cannot be accessed through generic retrieval.",
                policy_id=identity_policy["policy_id"],
            )

        if goal_category != required_goal_category:
            return self._deny(
                base,
                reason="Identity source is restricted to HR support Goal Context.",
                policy_id=identity_policy["policy_id"],
            )

        if condition.get("requires_business_justification") and not request.business_justification:
            return self._deny(
                base,
                reason="High-risk uncertainty: identity access requires business justification.",
                policy_id=identity_policy["policy_id"],
            )

        source = self.source_by_id[identity_source]
        base.update(
            {
                "required_controls": source.get("required_controls", []),
                "escalated_sources": [identity_source],
            }
        )
        return self._escalate(
            base,
            reason="Identity access requires human review.",
            policy_id=identity_policy["policy_id"],
        )

    def _evaluate_hr_policy(
        self,
        request: ActionRequest,
        goal_category: str,
        base: dict[str, Any],
    ) -> dict[str, Any] | None:
        hr_policy = self.policy_by_id.get("POL-KNOWLEDGE-HR-001")
        if hr_policy is None:
            return None

        condition = hr_policy.get("condition", {})
        hr_source = condition.get("requested_source")

        if hr_source not in request.requested_sources:
            return None

        allowed_goal_categories = condition.get("allowed_goal_categories", [])

        if goal_category not in allowed_goal_categories:
            base["required_controls"] = hr_policy.get("controls", [])
            return self._deny(
                base,
                reason="Human Resources Knowledge is restricted to HR Goal Contexts.",
                policy_id=hr_policy["policy_id"],
            )

        return None

    def _evaluate_write_policy(
        self,
        request: ActionRequest,
        base: dict[str, Any],
    ) -> dict[str, Any] | None:
        write_policy = self.policy_by_id.get("POL-KNOWLEDGE-WRITE-001")
        if write_policy is None:
            return None

        subject = write_policy.get("subject", {})
        condition = write_policy.get("condition", {})

        if (
            request.requested_capability == subject.get("capability")
            and condition.get("requested_source") in request.requested_sources
        ):
            source = self.source_by_id[condition["requested_source"]]
            base.update(
                {
                    "required_controls": source.get("required_controls", []),
                    "escalated_sources": [condition["requested_source"]],
                }
            )
            return self._escalate(
                base,
                reason="Validated learning writes require human approval.",
                policy_id=write_policy["policy_id"],
            )

        return None

    def _find_allowed_policy(
        self,
        target_agent_id: str,
        capability: str,
        goal_category: str,
        requested_source_ids: list[str],
    ) -> dict[str, Any] | None:
        for policy in self.policies:
            subject = policy.get("subject", {})
            condition = policy.get("condition", {})

            if subject.get("target_agent_id") != target_agent_id:
                continue

            if subject.get("capability") != capability:
                continue

            if condition.get("goal_category") != goal_category:
                continue

            allowed_sources = condition.get("allowed_sources", [])
            if all(source_id in allowed_sources for source_id in requested_source_ids):
                return policy

        return None

    def _collect_required_controls(
        self,
        requested_sources: list[dict[str, Any]],
        policy: dict[str, Any],
    ) -> list[str]:
        controls = set(policy.get("controls", []))

        for source in requested_sources:
            controls.update(source.get("required_controls", []))

        return sorted(controls)

    def _base_decision(self, request: ActionRequest) -> dict[str, Any]:
        return {
            "request_id": request.request_id,
            "caller_agent_id": request.caller_agent_id,
            "target_agent_id": request.target_agent_id,
            "requested_capability": request.requested_capability,
            "requested_sources": request.requested_sources,
            "goal_context": request.goal_context,
            "risk_context": request.risk_context,
            "business_justification": request.business_justification,
            "decision": "UNDECIDED",
            "reason": "",
            "policy_id": None,
            "approved_sources": [],
            "denied_sources": [],
            "escalated_sources": [],
            "required_controls": [],
            "governance_debt": [],
            "nist_trace": {
                "govern": "Policy, ownership, and accountability evaluated.",
                "map": "Caller, target, capability, Goal Context, and sources mapped.",
                "measure": "Risk, trust, controls, and metadata evaluated.",
                "manage": "Approve, deny, escalate, or fail closed decision produced.",
            },
        }

    def _deny(
        self,
        decision: dict[str, Any],
        reason: str,
        policy_id: str,
    ) -> dict[str, Any]:
        decision.update(
            {
                "decision": "DENIED",
                "reason": reason,
                "policy_id": policy_id,
                "approved_sources": [],
                "denied_sources": decision.get("requested_sources", []),
                "escalated_sources": [],
            }
        )
        return decision

    def _escalate(
        self,
        decision: dict[str, Any],
        reason: str,
        policy_id: str,
    ) -> dict[str, Any]:
        decision.update(
            {
                "decision": "ESCALATE",
                "reason": reason,
                "policy_id": policy_id,
                "approved_sources": [],
                "denied_sources": [],
                "escalated_sources": decision.get(
                    "escalated_sources",
                    decision.get("requested_sources", []),
                ),
            }
        )
        return decision