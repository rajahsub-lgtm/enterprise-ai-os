import json
from pathlib import Path

from src.contracts.case_context import CaseContextPhase
from src.contracts.case_context_validator import CaseContextValidator
from src.governance.evidence_fusion import EvidenceFusionEngine
from src.governance.governed_evidence_package import GovernedEvidencePackage
from src.governance.operational_confidence import OperationalConfidenceGate
from src.governance.source_access_request import SourceAccessRequest
from src.governance.source_access_result import SourceAccessResult
from src.orchestration.adaptive_orchestrator import AdaptiveOrchestrator
from src.views.governance_trace_view import GovernanceTraceView


SCENARIOS_PATH = Path(
    "data/domain/it_application_health/sprint3_demo_scenarios.json"
)
MEMORY_STATES_PATH = Path(
    "data/domain/it_application_health/sprint3_demo_memory_states.json"
)


def scenarios() -> dict[str, dict]:
    return {
        scenario["scenario_type"]: scenario
        for scenario in json.loads(SCENARIOS_PATH.read_text(encoding="utf-8"))
    }


def memory_states() -> dict[str, dict]:
    return {
        state["memory_state_id"]: state
        for state in json.loads(MEMORY_STATES_PATH.read_text(encoding="utf-8"))
    }


def case_context_for(scenario_type: str) -> dict:
    scenario = scenarios()[scenario_type]
    memory_state = memory_states()[scenario["memory_state_id"]]

    memory_context = []
    if memory_state["memory_state_id"] != "no_memory":
        memory_context = [memory_state]

    return {
        "case_id": scenario["case_id"],
        "scenario_id": scenario["scenario_id"],
        "business_outcome": "Maintain Business Capability",
        "goal_category": "capability_health_management",
        "joint_goal": "Maintain the target outcome while preserving controls.",
        "case_phase": "PARTIAL_CONTEXT",
        "initial_signal": scenario["initial_signal"],
        "impact": scenario["impact"],
        "context_records": {
            "memory_context": memory_context,
        },
    }


def fusion_for(scenario_type: str) -> dict:
    scenario = scenarios()[scenario_type]
    fusion_state = scenario["fusion_state"]

    if fusion_state == "CONFLICTING":
        return {
            "fusion_confidence": "LOW",
            "conflicting_evidence": [{"evidence_id": "conflict-001"}],
            "missing_evidence": [],
            "weakening_evidence": [],
        }

    if fusion_state == "UNKNOWN_IMPACT":
        return {
            "fusion_confidence": "LOW",
            "conflicting_evidence": [],
            "missing_evidence": [],
            "weakening_evidence": [],
        }

    return {
        "fusion_confidence": "HIGH",
        "conflicting_evidence": [],
        "missing_evidence": [],
        "weakening_evidence": [],
    }


def source_requests(case_id: str) -> list[SourceAccessRequest]:
    return [
        SourceAccessRequest(
            case_id=case_id,
            agent_id="memory_pattern_agent",
            source_id="enterprise_memory",
            capability="retrieve_memory_patterns",
            goal_category="capability_health_management",
            purpose="retrieve_memory_patterns",
            evidence_class="memory_state_evidence",
        ),
        SourceAccessRequest(
            case_id=case_id,
            agent_id="knowledge_retrieval_agent",
            source_id="support_knowledge",
            capability="retrieve_support_knowledge",
            goal_category="capability_health_management",
            purpose="retrieve_support_knowledge",
            evidence_class="free_text_evidence",
        ),
        SourceAccessRequest(
            case_id=case_id,
            agent_id="validation_agent",
            source_id="itil_operational_records",
            capability="validate_current_context",
            goal_category="capability_health_management",
            purpose="validate_current_context",
            evidence_class="structured_record_evidence",
        ),
        SourceAccessRequest(
            case_id=case_id,
            agent_id="business_impact_agent",
            source_id="itil_business_impact_map",
            capability="assess_impact_context",
            goal_category="capability_health_management",
            purpose="assess_impact_context",
            evidence_class="structured_record_evidence",
        ),
        SourceAccessRequest(
            case_id=case_id,
            agent_id="incident_correlation_agent",
            source_id="itil_incidents",
            capability="resolve_evidence_conflicts",
            goal_category="capability_health_management",
            purpose="resolve_evidence_conflicts",
            evidence_class="structured_record_evidence",
        ),
    ]


class E2EGovernedEvidenceClient:
    def __init__(self, mode: str = "allowed") -> None:
        self.mode = mode
        self.received_requests: list[SourceAccessRequest] = []

    def collect(
        self,
        selected_requests: list[SourceAccessRequest],
    ) -> GovernedEvidencePackage:
        self.received_requests = selected_requests
        results: list[SourceAccessResult] = []

        for index, request in enumerate(selected_requests, start=1):
            if self.mode == "deny_wrong_source" and (
                request.agent_id == "memory_pattern_agent"
                and request.source_id == "itil_business_impact_map"
            ):
                results.append(
                    SourceAccessResult.denied(
                        request,
                        reason="Agent is not entitled to this source.",
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
                        payload={"summary": "Collected but excluded by safety controls."},
                        required_controls=["content_safety_required"],
                    )
                )
                continue

            if self.mode == "review_required":
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
                        audit_id=f"audit-review-{index}",
                        evidence_id=f"ev-review-{index}",
                        content_safety_status="NEEDS_HUMAN_REVIEW",
                        allowed_for_reasoning=False,
                        payload={"summary": "Collected but requires human review."},
                        required_controls=["human_review_required"],
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
                    content_safety_status="SAFE_BY_APPROVED_PROVENANCE"
                    if request.evidence_class != "free_text_evidence"
                    else "SAFE",
                    allowed_for_reasoning=True,
                    payload={
                        "summary": f"Governed evidence from {request.source_id}.",
                        "trust_level": "APPROVED_HIGH",
                    },
                    required_controls=["governed_access_required"],
                )
            )

        return GovernedEvidencePackage.from_results(
            case_id=selected_requests[0].case_id,
            results=results,
        )


def run_headless_engine(
    scenario_type: str,
    *,
    source_client_mode: str = "allowed",
    requests_override: list[SourceAccessRequest] | None = None,
) -> dict:
    context = case_context_for(scenario_type)

    operational_decision = OperationalConfidenceGate().evaluate(
        case_context=context,
        fusion=fusion_for(scenario_type),
    )

    client = E2EGovernedEvidenceClient(mode=source_client_mode)
    orchestration_result = AdaptiveOrchestrator(client).orchestrate(
        case_context=context,
        operational_decision=operational_decision,
        source_requests=requests_override or source_requests(context["case_id"]),
    )

    governed_context = orchestration_result["case_context"]

    validation = CaseContextValidator().validate(
        governed_context,
        CaseContextPhase.GOVERNED_EVIDENCE_COLLECTED,
    )

    fusion_result = EvidenceFusionEngine().fuse(governed_context)

    trace_view = GovernanceTraceView.from_orchestration_trace(
        orchestration_result["orchestration_trace"]
    ).to_dict()

    return {
        "case_context": governed_context,
        "operational_decision": operational_decision,
        "selected_requests": client.received_requests,
        "governed_evidence_package": orchestration_result["governed_evidence_package"],
        "case_context_validation": validation,
        "fusion": fusion_result,
        "orchestration_trace": orchestration_result["orchestration_trace"],
        "governance_trace_view": trace_view,
    }


def test_same_alert_no_memory_runs_full_due_diligence():
    result = run_headless_engine("same_alert_no_memory")

    assert result["operational_decision"]["operational_confidence"] == "LOW"
    assert result["operational_decision"]["confidence_direction"] == "NEW"
    assert result["operational_decision"]["selected_due_diligence_level"] == "FULL_DUE_DILIGENCE"
    assert len(result["selected_requests"]) == 5
    assert result["case_context_validation"]["valid"] is True
    assert result["fusion"]["autonomous_action_allowed"] is False


def test_same_alert_trusted_memory_runs_targeted_validation():
    result = run_headless_engine("same_alert_trusted_memory")

    assert result["operational_decision"]["operational_confidence"] == "HIGH"
    assert result["operational_decision"]["selected_due_diligence_level"] == "TARGETED_VALIDATION"
    assert [request.capability for request in result["selected_requests"]] == [
        "retrieve_memory_patterns",
        "validate_current_context",
    ]
    assert result["case_context_validation"]["valid"] is True
    assert result["governance_trace_view"]["summary"]["reasoning_eligible_rows"] == 2


def test_same_alert_trusted_memory_with_conflict_expands_validation():
    result = run_headless_engine("same_alert_conflicting_evidence")

    assert result["operational_decision"]["pattern_maturity"] == "UNRELIABLE_FOR_CURRENT_CASE"
    assert result["operational_decision"]["selected_due_diligence_level"] == "EXPANDED_VALIDATION"
    assert "resolve_evidence_conflicts" in [
        request.capability for request in result["selected_requests"]
    ]
    assert result["case_context_validation"]["valid"] is True


def test_same_alert_unknown_impact_escalates_for_impact_assessment():
    result = run_headless_engine("same_alert_unknown_impact")

    assert result["operational_decision"]["pattern_maturity"] == "UNKNOWN_IMPACT"
    assert result["operational_decision"]["selected_due_diligence_level"] == "ESCALATE_FOR_IMPACT_ASSESSMENT"
    assert [request.capability for request in result["selected_requests"]] == [
        "retrieve_support_knowledge",
        "assess_impact_context",
    ]
    assert result["fusion"]["fusion_confidence"] == "LOW"
    assert result["fusion"]["requires_human_review"] is True


def test_governance_denial_creates_gap_and_no_reasoning_evidence():
    context = case_context_for("same_alert_no_memory")
    bad_request = SourceAccessRequest(
        case_id=context["case_id"],
        agent_id="memory_pattern_agent",
        source_id="itil_business_impact_map",
        capability="assess_impact_context",
        goal_category="capability_health_management",
        purpose="assess_impact_context",
        evidence_class="structured_record_evidence",
    )

    result = run_headless_engine(
        "same_alert_no_memory",
        source_client_mode="deny_wrong_source",
        requests_override=[bad_request],
    )

    assert result["governed_evidence_package"]["evidence_items"] == []
    assert result["governed_evidence_package"]["evidence_gaps"]
    assert result["fusion"]["supporting_evidence"] == []
    assert result["fusion"]["evidence_gaps"]
    assert result["governance_trace_view"]["summary"]["denied_rows"] == 1
    assert result["governance_trace_view"]["summary"]["reasoning_eligible_rows"] == 0


def test_unsafe_content_is_excluded_from_reasoning():
    result = run_headless_engine(
        "same_alert_trusted_memory",
        source_client_mode="unsafe",
    )

    assert result["fusion"]["supporting_evidence"] == []
    assert result["fusion"]["missing_evidence"]
    assert result["fusion"]["missing_evidence"][0]["evidence_type"] == "excluded_unsafe_content"
    assert result["governance_trace_view"]["summary"]["reasoning_eligible_rows"] == 0
    assert result["governance_trace_view"]["summary"]["blocked_rows"] >= 1


def test_review_required_content_is_excluded_and_flagged():
    result = run_headless_engine(
        "same_alert_trusted_memory",
        source_client_mode="review_required",
    )

    assert result["fusion"]["supporting_evidence"] == []
    assert result["fusion"]["missing_evidence"]
    assert result["fusion"]["missing_evidence"][0]["evidence_type"] == "missing_human_validation"
    assert result["fusion"]["requires_human_review"] is True
    assert result["governance_trace_view"]["summary"]["reasoning_eligible_rows"] == 0


def test_same_alert_drifting_memory_decreases_confidence_and_expands_validation():
    result = run_headless_engine("same_alert_trusted_but_drifting_memory")

    assert result["operational_decision"]["pattern_maturity"] == "TRUSTED_BUT_DRIFTING"
    assert result["operational_decision"]["confidence_direction"] == "DECREASING"
    assert result["operational_decision"]["selected_due_diligence_level"] == "EXPANDED_VALIDATION"
    assert "resolve_evidence_conflicts" in [
        request.capability for request in result["selected_requests"]
    ]
    assert result["case_context_validation"]["valid"] is True


def test_headless_engine_keeps_governance_and_human_review_boundaries():
    result = run_headless_engine("same_alert_trusted_memory")

    assert result["operational_decision"]["governance_required"] is True
    assert result["operational_decision"]["human_approval_required"] is True
    assert result["operational_decision"]["autonomous_action_allowed"] is False

    assert result["orchestration_trace"]["governance_required"] is True
    assert result["orchestration_trace"]["human_approval_required"] is True
    assert result["orchestration_trace"]["autonomous_action_allowed"] is False

    assert result["governance_trace_view"]["governance_required"] is True
    assert result["governance_trace_view"]["human_approval_required"] is True
    assert result["governance_trace_view"]["autonomous_action_allowed"] is False

    assert result["fusion"]["autonomous_action_allowed"] is False
