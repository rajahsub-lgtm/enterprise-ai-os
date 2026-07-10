import pytest

from src.governance.governed_evidence_package import GovernedEvidencePackage
from src.governance.source_access_request import SourceAccessRequest
from src.governance.source_access_result import SourceAccessResult
from src.orchestration.adaptive_orchestrator import (
    AdaptiveOrchestrationError,
    AdaptiveOrchestrator,
)


def case_context() -> dict:
    return {
        "case_id": "CASE-S3-ORCH-001",
        "business_outcome": "Maintain Business Capability",
        "goal_category": "capability_health_management",
        "joint_goal": "Maintain the target outcome while preserving controls.",
        "case_phase": "PARTIAL_CONTEXT",
    }


def decision(
    *,
    confidence: str = "LOW",
    level: str | None = None,
    required_steps: list[str] | None = None,
    direction: str | None = None,
) -> dict:
    value = {
        "operational_confidence": confidence,
        "confidence_direction": direction or "STABLE",
        "selected_due_diligence_level": level,
        "required_agent_steps": required_steps or [],
        "why": "Operational confidence requires this governed path.",
        "governance_required": True,
        "human_approval_required": True,
        "autonomous_action_allowed": False,
    }

    return {key: item for key, item in value.items() if item is not None}


def requests() -> list[SourceAccessRequest]:
    return [
        SourceAccessRequest(
            case_id="CASE-S3-ORCH-001",
            agent_id="memory_pattern_agent",
            source_id="enterprise_memory",
            capability="retrieve_memory_patterns",
            goal_category="capability_health_management",
            purpose="evaluate prior governed experience",
            evidence_class="memory_state_evidence",
        ),
        SourceAccessRequest(
            case_id="CASE-S3-ORCH-001",
            agent_id="knowledge_retrieval_agent",
            source_id="support_knowledge",
            capability="retrieve_support_knowledge",
            goal_category="capability_health_management",
            purpose="retrieve governed knowledge",
            evidence_class="free_text_evidence",
        ),
        SourceAccessRequest(
            case_id="CASE-S3-ORCH-001",
            agent_id="validation_agent",
            source_id="validation_source",
            capability="validate_current_context",
            goal_category="capability_health_management",
            purpose="validate current hypothesis",
            evidence_class="structured_record_evidence",
        ),
    ]


class FakeGovernedEvidenceClient:
    def __init__(self, mode: str = "allowed") -> None:
        self.mode = mode
        self.received_requests = []

    def collect(self, selected_requests: list[SourceAccessRequest]) -> GovernedEvidencePackage:
        self.received_requests = selected_requests

        results: list[SourceAccessResult] = []

        for index, request in enumerate(selected_requests, start=1):
            if self.mode == "denied":
                results.append(
                    SourceAccessResult.denied(
                        request,
                        reason="Source access denied by policy.",
                        audit_id=f"audit-denied-{index}",
                        required_controls=["least_privilege_enforced"],
                    )
                )
                continue

            if self.mode == "unsafe":
                results.append(
                    SourceAccessResult(
                        case_id=request.case_id,
                        agent_id=request.agent_id,
                        source_id=request.source_id,
                        capability=request.capability,
                        goal_category=request.goal_category,
                        purpose=request.purpose,
                        evidence_class=request.evidence_class,
                        access_decision="ALLOW",
                        audit_id=f"audit-unsafe-{index}",
                        evidence_id=f"ev-unsafe-{index}",
                        content_safety_status="UNSAFE",
                        allowed_for_reasoning=False,
                        payload={"summary": "Collected but excluded."},
                    )
                )
                continue

            results.append(
                SourceAccessResult(
                    case_id=request.case_id,
                    agent_id=request.agent_id,
                    source_id=request.source_id,
                    capability=request.capability,
                    goal_category=request.goal_category,
                    purpose=request.purpose,
                    evidence_class=request.evidence_class,
                    access_decision="ALLOW",
                    audit_id=f"audit-allowed-{index}",
                    evidence_id=f"ev-allowed-{index}",
                    content_safety_status="SAFE_BY_APPROVED_PROVENANCE",
                    allowed_for_reasoning=True,
                    payload={"summary": "Governed evidence collected."},
                )
            )

        return GovernedEvidencePackage.from_results(
            case_id=selected_requests[0].case_id,
            results=results,
        )


def test_low_confidence_path_selects_all_source_requests():
    client = FakeGovernedEvidenceClient()
    result = AdaptiveOrchestrator(client).orchestrate(
        case_context=case_context(),
        operational_decision=decision(confidence="LOW"),
        source_requests=requests(),
    )

    assert len(client.received_requests) == 3
    assert result["orchestration_trace"]["selected_due_diligence_level"] == "FULL_DILIGENCE"
    assert result["orchestration_trace"]["valid"] is True
    assert result["case_context"]["case_phase"] == "GOVERNED_EVIDENCE_COLLECTED"


def test_decreasing_confidence_selects_expanded_validation():
    client = FakeGovernedEvidenceClient()
    result = AdaptiveOrchestrator(client).orchestrate(
        case_context=case_context(),
        operational_decision=decision(confidence="HIGH", direction="DECREASING"),
        source_requests=requests(),
    )

    assert len(client.received_requests) == 3
    assert result["orchestration_trace"]["selected_due_diligence_level"] == "EXPANDED_VALIDATION"


def test_targeted_path_uses_required_agent_steps():
    client = FakeGovernedEvidenceClient()
    result = AdaptiveOrchestrator(client).orchestrate(
        case_context=case_context(),
        operational_decision=decision(
            confidence="MEDIUM",
            required_steps=["knowledge_retrieval_agent"],
        ),
        source_requests=requests(),
    )

    assert [request.agent_id for request in client.received_requests] == [
        "knowledge_retrieval_agent"
    ]
    assert result["orchestration_trace"]["selected_due_diligence_level"] == "TARGETED_VALIDATION"


def test_validate_only_path_prefers_validation_request():
    client = FakeGovernedEvidenceClient()
    result = AdaptiveOrchestrator(client).orchestrate(
        case_context=case_context(),
        operational_decision=decision(confidence="HIGH"),
        source_requests=requests(),
    )

    assert [request.agent_id for request in client.received_requests] == [
        "validation_agent"
    ]
    assert result["orchestration_trace"]["selected_due_diligence_level"] == "VALIDATE_ONLY"


def test_trace_records_governed_source_requests_and_results():
    client = FakeGovernedEvidenceClient()
    result = AdaptiveOrchestrator(client).orchestrate(
        case_context=case_context(),
        operational_decision=decision(confidence="MEDIUM"),
        source_requests=requests(),
    )

    trace = result["orchestration_trace"]

    assert trace["governed_source_requests"]
    assert trace["access_decisions"]
    assert trace["audit_ids"]
    assert trace["evidence_ids"]
    assert trace["reasoning_eligibility"]
    assert trace["why_path_selected"] == "Operational confidence requires this governed path."


def test_denied_source_access_creates_blocked_trace_step_without_evidence_id():
    client = FakeGovernedEvidenceClient(mode="denied")
    result = AdaptiveOrchestrator(client).orchestrate(
        case_context=case_context(),
        operational_decision=decision(confidence="MEDIUM"),
        source_requests=requests(),
    )

    trace = result["orchestration_trace"]

    assert trace["access_decisions"][1]["governance_decision"] == "DENY"
    assert trace["evidence_ids"] == []
    assert trace["reasoning_eligibility"][1]["allowed_for_reasoning"] is False
    assert result["governed_evidence_package"]["evidence_gaps"]


def test_unsafe_evidence_is_recorded_as_not_reasoning_eligible():
    client = FakeGovernedEvidenceClient(mode="unsafe")
    result = AdaptiveOrchestrator(client).orchestrate(
        case_context=case_context(),
        operational_decision=decision(confidence="MEDIUM"),
        source_requests=requests(),
    )

    trace = result["orchestration_trace"]

    assert trace["reasoning_eligibility"][1]["allowed_for_reasoning"] is False
    assert result["governed_evidence_package"]["evidence_gaps"]


def test_orchestrator_rejects_optional_governance():
    bad_decision = decision()
    bad_decision["governance_required"] = False

    with pytest.raises(AdaptiveOrchestrationError):
        AdaptiveOrchestrator(FakeGovernedEvidenceClient()).orchestrate(
            case_context=case_context(),
            operational_decision=bad_decision,
            source_requests=requests(),
        )


def test_orchestrator_rejects_missing_human_approval_boundary():
    bad_decision = decision()
    bad_decision["human_approval_required"] = False

    with pytest.raises(AdaptiveOrchestrationError):
        AdaptiveOrchestrator(FakeGovernedEvidenceClient()).orchestrate(
            case_context=case_context(),
            operational_decision=bad_decision,
            source_requests=requests(),
        )


def test_orchestrator_rejects_autonomous_action_allowed():
    bad_decision = decision()
    bad_decision["autonomous_action_allowed"] = True

    with pytest.raises(AdaptiveOrchestrationError):
        AdaptiveOrchestrator(FakeGovernedEvidenceClient()).orchestrate(
            case_context=case_context(),
            operational_decision=bad_decision,
            source_requests=requests(),
        )
