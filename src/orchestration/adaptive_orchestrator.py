"""
Adaptive orchestrator.

Classification: EAIOS Core

The adaptive orchestrator selects a governed execution path from an operational
confidence decision, delegates source access through the governed evidence
client, and records the resulting orchestration trace.

This module is domain-neutral.
"""

from __future__ import annotations

from typing import Any

from src.governance.governed_evidence_package import GovernedEvidencePackage
from src.governance.source_access_request import SourceAccessRequest
from src.orchestration.agent_step import AgentStep
from src.orchestration.orchestration_trace import OrchestrationTrace


class AdaptiveOrchestrationError(ValueError):
    pass


class AdaptiveOrchestrator:
    def __init__(self, governed_evidence_client: Any) -> None:
        self.governed_evidence_client = governed_evidence_client

    def orchestrate(
        self,
        *,
        case_context: dict[str, Any],
        operational_decision: dict[str, Any],
        source_requests: list[SourceAccessRequest | dict[str, Any]],
    ) -> dict[str, Any]:
        self._validate_safety_boundary(operational_decision)

        normalized_requests = self._normalize_requests(source_requests)
        if not normalized_requests:
            raise AdaptiveOrchestrationError(
                "At least one governed source request is required."
            )

        selected_due_diligence_level = self._selected_due_diligence_level(
            operational_decision
        )
        selected_requests = self._select_requests(
            requests=normalized_requests,
            operational_decision=operational_decision,
            selected_due_diligence_level=selected_due_diligence_level,
        )

        if not selected_requests:
            raise AdaptiveOrchestrationError(
                "Adaptive path selected no governed source requests."
            )

        trace = OrchestrationTrace(
            trace_id=f"TRACE-{case_context['case_id']}",
            case_id=case_context["case_id"],
            joint_goal=case_context["joint_goal"],
            current_phase=case_context.get("case_phase", "PARTIAL_CONTEXT"),
            selected_due_diligence_level=selected_due_diligence_level,
            why_path_selected=self._why_path_selected(operational_decision),
            governance_required=True,
            human_approval_required=True,
            autonomous_action_allowed=False,
        )

        for index, request in enumerate(selected_requests, start=1):
            trace.add_source_request(request)
            trace.add_step(
                AgentStep.planned_source_access(
                    step_id=f"STEP-PLAN-{index:03d}",
                    step_name=f"Planned governed source access {index}",
                    request=request,
                )
            )

        package = self.governed_evidence_client.collect(selected_requests)

        if not isinstance(package, GovernedEvidencePackage):
            raise AdaptiveOrchestrationError(
                "Governed evidence client must return GovernedEvidencePackage."
            )

        self._record_package_results(trace, package)

        updated_context = dict(case_context)
        updated_context["case_phase"] = "GOVERNED_EVIDENCE_COLLECTED"
        updated_context["governed_evidence_package"] = package.to_dict()
        updated_context["human_approval_required"] = True
        updated_context["autonomous_action_allowed"] = False

        return {
            "case_context": updated_context,
            "governed_evidence_package": package.to_dict(),
            "orchestration_trace": trace.to_dict(),
        }

    def _validate_safety_boundary(
        self,
        operational_decision: dict[str, Any],
    ) -> None:
        if operational_decision.get("governance_required", True) is not True:
            raise AdaptiveOrchestrationError("governance_required must be True.")

        if operational_decision.get("human_approval_required", True) is not True:
            raise AdaptiveOrchestrationError("human_approval_required must be True.")

        if operational_decision.get("autonomous_action_allowed", False) is not False:
            raise AdaptiveOrchestrationError(
                "autonomous_action_allowed must be False."
            )

    def _normalize_requests(
        self,
        source_requests: list[SourceAccessRequest | dict[str, Any]],
    ) -> list[SourceAccessRequest]:
        return [
            request
            if isinstance(request, SourceAccessRequest)
            else SourceAccessRequest.from_dict(request)
            for request in source_requests
        ]

    def _selected_due_diligence_level(
        self,
        operational_decision: dict[str, Any],
    ) -> str:
        explicit_level = operational_decision.get("selected_due_diligence_level")
        if explicit_level:
            return explicit_level

        confidence_direction = operational_decision.get("confidence_direction")
        if confidence_direction == "DECREASING":
            return "EXPANDED_VALIDATION"

        confidence = operational_decision.get("operational_confidence")

        if confidence == "LOW":
            return "FULL_DILIGENCE"

        if confidence == "MEDIUM":
            return "TARGETED_VALIDATION"

        if confidence == "HIGH":
            return "VALIDATE_ONLY"

        return "EXPANDED_VALIDATION"

    def _select_requests(
        self,
        *,
        requests: list[SourceAccessRequest],
        operational_decision: dict[str, Any],
        selected_due_diligence_level: str,
    ) -> list[SourceAccessRequest]:
        if selected_due_diligence_level in {
            "FULL_DILIGENCE",
            "EXPANDED_VALIDATION",
        }:
            return requests

        required_steps = operational_decision.get("required_agent_steps", [])
        matched = self._requests_matching_required_steps(
            requests=requests,
            required_steps=required_steps,
        )

        if matched:
            return matched

        if selected_due_diligence_level in {
            "TARGETED_VALIDATION",
            "TARGETED_RETRIEVAL",
        }:
            return requests[:1]

        if selected_due_diligence_level == "VALIDATE_ONLY":
            validation_requests = [
                request
                for request in requests
                if "validat" in request.capability.lower()
                or "validat" in request.purpose.lower()
            ]
            return validation_requests or requests[:1]

        return requests

    def _requests_matching_required_steps(
        self,
        *,
        requests: list[SourceAccessRequest],
        required_steps: list[str],
    ) -> list[SourceAccessRequest]:
        if not required_steps:
            return []

        required = set(required_steps)

        return [
            request
            for request in requests
            if request.agent_id in required
            or request.source_id in required
            or request.capability in required
            or request.purpose in required
        ]

    def _why_path_selected(
        self,
        operational_decision: dict[str, Any],
    ) -> str:
        why = operational_decision.get("why")
        if isinstance(why, str):
            return why

        if isinstance(why, list):
            return " ".join(str(item) for item in why)

        return "Operational confidence selected the governed path."

    def _record_package_results(
        self,
        trace: OrchestrationTrace,
        package: GovernedEvidencePackage,
    ) -> None:
        step_index = 1

        for evidence in package.evidence_items:
            trace.add_step(
                AgentStep(
                    step_id=f"STEP-RESULT-{step_index:03d}",
                    agent_id=evidence["agent_id"],
                    step_name="Governed evidence collected",
                    status="COMPLETED",
                    source_id=evidence["source_id"],
                    source_access_purpose=evidence.get("purpose"),
                    governance_decision=evidence.get("access_decision"),
                    audit_id=evidence.get("audit_id"),
                    evidence_id=evidence.get("evidence_id"),
                    content_safety_status=evidence.get("content_safety_status"),
                    allowed_for_reasoning=evidence.get("allowed_for_reasoning"),
                    required_controls=evidence.get("required_controls", []),
                    reason=evidence.get("reason"),
                    details={
                        "case_id": evidence.get("case_id"),
                        "capability": evidence.get("capability"),
                        "goal_category": evidence.get("goal_category"),
                        "evidence_class": evidence.get("evidence_class"),
                    },
                )
            )
            step_index += 1

        for gap in package.evidence_gaps:
            decision = gap.get("access_decision")
            status = "BLOCKED" if decision == "DENY" else "COMPLETED"

            trace.add_step(
                AgentStep(
                    step_id=f"STEP-RESULT-{step_index:03d}",
                    agent_id=gap["agent_id"],
                    step_name="Governed evidence gap recorded",
                    status=status,
                    source_id=gap["source_id"],
                    source_access_purpose=gap.get("purpose"),
                    governance_decision=decision,
                    audit_id=gap.get("audit_id"),
                    evidence_id=None,
                    content_safety_status=None,
                    allowed_for_reasoning=False,
                    required_controls=gap.get("required_controls", []),
                    reason=gap.get("reason"),
                    details={
                        "case_id": gap.get("case_id"),
                        "capability": gap.get("capability"),
                        "goal_category": gap.get("goal_category"),
                    },
                )
            )
            step_index += 1
