"""
Presentation demo fixtures for Sprint 3-UI shell.

Classification: EAIOS Presentation Layer

These fixtures exist only to render the first control-room shell before the
full scenario runner is connected.

They are intentionally built through the ReplayRunViewModel composer so the UI
still consumes the same shape it will receive from tested engine outputs.
"""

from __future__ import annotations

from typing import Any

from ui.story_mode import attach_animation_events
from ui.view_models import build_comparison_view_model, build_replay_run_view_model


def build_demo_comparison_view_model() -> dict[str, Any]:
    """Build the initial same-alert side-by-side replay model."""

    runs = [
        _build_run(
            run_id="run-no-memory",
            scenario_label="First-time / no memory",
            operational_confidence="LOW",
            confidence_direction="NEW",
            pattern_maturity="NONE",
            due_diligence="FULL_DUE_DILIGENCE",
            step_count=7,
            why=[
                "No reliable prior memory pattern is available.",
                "The condition must be treated as a new operational case.",
                "Full due diligence is required before human review.",
            ],
        ),
        _build_run(
            run_id="run-trusted-memory",
            scenario_label="Trusted memory / validated pattern",
            operational_confidence="HIGH",
            confidence_direction="STABLE",
            pattern_maturity="TRUSTED",
            due_diligence="TARGETED_VALIDATION",
            step_count=3,
            why=[
                "A trusted validated memory pattern is available.",
                "Current evidence does not conflict with the trusted pattern.",
                "Targeted validation is sufficient before human review.",
            ],
        ),
        _build_run(
            run_id="run-drift-conflict",
            scenario_label="Drift or conflict",
            operational_confidence="MEDIUM",
            confidence_direction="DECREASING",
            pattern_maturity="DRIFTING",
            due_diligence="EXPANDED_VALIDATION",
            step_count=5,
            why=[
                "The memory pattern shows signs of drift.",
                "Evidence must be expanded before recommendation confidence can increase.",
                "Human review remains required.",
            ],
        ),
    ]

    return build_comparison_view_model(
        comparison_id="comparison-same-alert-memory-states",
        comparison_label="Same alert, different memory states",
        runs=runs,
    )


def _build_run(
    *,
    run_id: str,
    scenario_label: str,
    operational_confidence: str,
    confidence_direction: str,
    pattern_maturity: str,
    due_diligence: str,
    step_count: int,
    why: list[str],
) -> dict[str, Any]:
    run = build_replay_run_view_model(
        run_id=run_id,
        scenario_id=run_id,
        scenario_label=scenario_label,
        business_outcome="Maintain Application Health",
        joint_goal="Maintain service health while preserving controls",
        current_alert={
            "application": "Digital Checkout",
            "symptom": "Payment authorization latency and elevated error rate",
            "severity": "High",
        },
        operational_confidence={
            "operational_confidence": operational_confidence,
            "confidence_direction": confidence_direction,
            "pattern_maturity": pattern_maturity,
            "selected_due_diligence_level": due_diligence,
            "why": why,
            "governance_required": True,
            "human_approval_required": True,
            "autonomous_action_allowed": False,
        },
        orchestration_trace={
            "case_id": run_id,
            "agent_steps": [
                {
                    "step_id": f"{run_id}-STEP-{index:02d}",
                    "agent_id": _agent_for_index(index),
                    "status": "COMPLETED",
                }
                for index in range(1, step_count + 1)
            ],
        },
        governance_trace_view={
            "rows": _governance_rows(run_id=run_id),
        },
        governed_evidence_package=_evidence_package(run_id=run_id),
        reasoning_explanation=_reasoning_explanation(
            scenario_label=scenario_label,
            due_diligence=due_diligence,
        ),
        recommendation_candidate=_recommendation_candidate(
            scenario_label=scenario_label,
            due_diligence=due_diligence,
        ),
        animation_events=[],
    )

    return attach_animation_events(run)


def _agent_for_index(index: int) -> str:
    agents = [
        "memory_pattern_agent",
        "telemetry_agent",
        "knowledge_retrieval_agent",
        "business_impact_agent",
        "incident_correlation_agent",
        "evidence_fusion_agent",
        "recommendation_agent",
    ]

    return agents[(index - 1) % len(agents)]


def _governance_rows(*, run_id: str) -> list[dict[str, Any]]:
    return [
        {
            "agent_id": "memory_pattern_agent",
            "source_id": "enterprise_memory",
            "source_access_purpose": "Retrieve validated memory pattern",
            "governance_decision": "ALLOW",
            "audit_id": f"{run_id}-AUDIT-001",
            "evidence_id": f"{run_id}-EVIDENCE-001",
            "content_safety_status": "SAFE_BY_APPROVED_PROVENANCE",
            "allowed_for_reasoning": True,
            "required_controls": ["audit_logging"],
            "approval_state": "PENDING_HUMAN_REVIEW",
            "autonomous_action_allowed": False,
            "reason": "Agent is entitled to source.",
        },
        {
            "agent_id": "knowledge_retrieval_agent",
            "source_id": "support_knowledge",
            "source_access_purpose": "Retrieve relevant support knowledge",
            "governance_decision": "ALLOW",
            "audit_id": f"{run_id}-AUDIT-002",
            "evidence_id": f"{run_id}-EVIDENCE-EXCLUDED-001",
            "content_safety_status": "REVIEW_REQUIRED",
            "allowed_for_reasoning": False,
            "required_controls": ["human_review"],
            "approval_state": "PENDING_HUMAN_REVIEW",
            "autonomous_action_allowed": False,
            "reason": "Knowledge article requires review before reasoning.",
        },
        {
            "agent_id": "business_impact_agent",
            "source_id": "itil_business_impact_map",
            "source_access_purpose": "Assess business impact",
            "governance_decision": "DENY",
            "audit_id": f"{run_id}-AUDIT-003",
            "evidence_id": None,
            "content_safety_status": None,
            "allowed_for_reasoning": False,
            "required_controls": ["access_review"],
            "approval_state": "BLOCKED",
            "autonomous_action_allowed": False,
            "reason": "Agent is not entitled to source.",
        },
    ]


def _evidence_package(*, run_id: str) -> dict[str, Any]:
    return {
        "evidence_items": [
            {
                "evidence_id": f"{run_id}-EVIDENCE-001",
                "audit_id": f"{run_id}-AUDIT-001",
                "source_id": "enterprise_memory",
                "evidence_class": "memory_state_evidence",
                "content_safety_status": "SAFE_BY_APPROVED_PROVENANCE",
                "allowed_for_reasoning": True,
                "payload": {"pattern": "validated memory pattern"},
            },
            {
                "evidence_id": f"{run_id}-EVIDENCE-EXCLUDED-001",
                "audit_id": f"{run_id}-AUDIT-002",
                "source_id": "support_knowledge",
                "evidence_class": "free_text_evidence",
                "content_safety_status": "REVIEW_REQUIRED",
                "allowed_for_reasoning": False,
                "payload": {"article": "Review required before reasoning."},
            },
        ],
        "evidence_gaps": [
            {
                "gap_id": f"{run_id}-GAP-001",
                "audit_id": f"{run_id}-AUDIT-003",
                "agent_id": "business_impact_agent",
                "source_id": "itil_business_impact_map",
                "reason": "Agent is not entitled to source.",
            }
        ],
    }

def _reasoning_explanation(
    *,
    scenario_label: str,
    due_diligence: str,
) -> dict[str, Any]:
    return {
        "situation": "Digital Checkout shows payment authorization latency and elevated error rate.",
        "is": [
            "Digital Checkout is affected.",
            "Payment authorization path is affected.",
            "Latency and error symptoms are present.",
        ],
        "is_not": [
            "Product Catalog is not identified as affected.",
            "Autonomous production action is not approved.",
            "Review-required evidence is not allowed into reasoning.",
        ],
        "distinctions": [
            "The same alert receives different due-diligence depth depending on memory and confidence.",
            "Governance gates remain constant across memory states.",
        ],
        "candidate_hypotheses": _candidate_hypotheses(scenario_label),
        "selected_hypothesis": _selected_hypothesis(scenario_label),
        "why_chain": [
            f"EAIOS selected {due_diligence} from operational-confidence output.",
            "Only reasoning-eligible governed evidence is used.",
            "Evidence gaps and excluded evidence remain visible for human review.",
        ],
        "limits": [
            "This is a Sprint 3-UI replay fixture.",
            "No production action is executed.",
            "Human approval remains required.",
        ],
    }


def _candidate_hypotheses(scenario_label: str) -> list[str]:
    if scenario_label == "First-time / no memory":
        return [
            "New operational degradation requiring full due diligence.",
            "Known payment authorization issue not yet validated as memory.",
        ]

    if scenario_label == "Trusted memory / validated pattern":
        return [
            "Previously validated payment authorization pattern has recurred.",
            "A new unrelated degradation is possible but less likely.",
        ]

    return [
        "Known memory pattern may be drifting.",
        "Current evidence may conflict with prior validated memory.",
    ]


def _selected_hypothesis(scenario_label: str) -> str:
    if scenario_label == "First-time / no memory":
        return "Treat as a new operational degradation until evidence matures."

    if scenario_label == "Trusted memory / validated pattern":
        return "Validated payment authorization pattern likely recurred, pending targeted human validation."

    return "Treat as drift or conflict and expand validation before relying on memory."


def _recommendation_candidate(
    *,
    scenario_label: str,
    due_diligence: str,
) -> dict[str, Any]:
    return {
        "title": "Human-reviewed operational recommendation",
        "summary": _recommendation_summary(scenario_label),
        "risk_level": _risk_level(scenario_label),
        "selected_due_diligence_level": due_diligence,
        "required_controls": [
            "Human approval",
            "Audit logging",
            "No autonomous production action",
        ],
        "prohibited_actions": [
            "Do not execute remediation automatically.",
            "Do not use review-required evidence for reasoning.",
            "Do not treat memory as truth.",
        ],
        "approval_state": "PENDING_HUMAN_REVIEW",
        "autonomous_action_allowed": False,
    }


def _recommendation_summary(scenario_label: str) -> str:
    if scenario_label == "First-time / no memory":
        return "Collect full due-diligence evidence and route recommendation package to human review."

    if scenario_label == "Trusted memory / validated pattern":
        return "Perform targeted validation against the trusted memory pattern before human approval."

    return "Expand validation because memory drift or evidence conflict is present."


def _risk_level(scenario_label: str) -> str:
    if scenario_label == "Trusted memory / validated pattern":
        return "Medium"

    return "High"

