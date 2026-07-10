from ui.view_models import (
    build_comparison_view_model,
    build_replay_run_view_model,
)


def sample_confidence():
    return {
        "operational_confidence": "HIGH",
        "confidence_direction": "STABLE",
        "pattern_maturity": "TRUSTED",
        "selected_due_diligence_level": "TARGETED_VALIDATION",
        "why": [
            "Trusted memory pattern exists.",
            "Current evidence does not conflict with memory.",
        ],
        "governance_required": True,
        "human_approval_required": True,
        "autonomous_action_allowed": False,
    }


def sample_trace(step_count=3):
    return {
        "case_id": "CASE-UI-001",
        "agent_steps": [
            {
                "step_id": f"STEP-{index}",
                "agent_id": f"agent_{index}",
                "status": "COMPLETED",
            }
            for index in range(step_count)
        ],
    }


def sample_governance_rows():
    return [
        {
            "agent_id": "memory_pattern_agent",
            "source_id": "enterprise_memory",
            "source_access_purpose": "Retrieve validated memory pattern",
            "governance_decision": "ALLOW",
            "audit_id": "AUDIT-001",
            "evidence_id": "EVIDENCE-001",
            "content_safety_status": "SAFE_BY_APPROVED_PROVENANCE",
            "allowed_for_reasoning": True,
            "required_controls": ["audit_logging"],
            "approval_state": "PENDING_HUMAN_REVIEW",
            "autonomous_action_allowed": False,
            "reason": "Agent is entitled to source.",
        },
        {
            "agent_id": "impact_agent",
            "source_id": "itil_business_impact_map",
            "source_access_purpose": "Assess business impact",
            "governance_decision": "DENY",
            "audit_id": "AUDIT-002",
            "evidence_id": None,
            "content_safety_status": None,
            "allowed_for_reasoning": False,
            "required_controls": ["access_review"],
            "approval_state": "BLOCKED",
            "autonomous_action_allowed": False,
            "reason": "Agent is not entitled to source.",
        },
    ]


def sample_package():
    return {
        "evidence_items": [
            {
                "evidence_id": "EVIDENCE-001",
                "audit_id": "AUDIT-001",
                "source_id": "enterprise_memory",
                "evidence_class": "memory_state_evidence",
                "content_safety_status": "SAFE_BY_APPROVED_PROVENANCE",
                "allowed_for_reasoning": True,
                "payload": {"validated_count": 50},
            },
            {
                "evidence_id": "EVIDENCE-EXCLUDED-001",
                "audit_id": "AUDIT-003",
                "source_id": "support_knowledge",
                "evidence_class": "free_text_evidence",
                "content_safety_status": "REVIEW_REQUIRED",
                "allowed_for_reasoning": False,
                "payload": {"article": "Needs review"},
            },
        ],
        "evidence_gaps": [
            {
                "gap_id": "GAP-001",
                "audit_id": "AUDIT-002",
                "agent_id": "impact_agent",
                "source_id": "itil_business_impact_map",
                "reason": "Agent is not entitled to source.",
            }
        ],
    }


def build_sample_run(
    *,
    run_id="run-trusted",
    scenario_label="Trusted memory / validated pattern",
    confidence=None,
    step_count=3,
):
    return build_replay_run_view_model(
        run_id=run_id,
        scenario_id=run_id,
        scenario_label=scenario_label,
        business_outcome="Maintain Application Health",
        joint_goal="Maintain service health while preserving controls",
        current_alert={
            "application": "Digital Checkout",
            "symptom": "Payment authorization latency",
        },
        operational_confidence=confidence or sample_confidence(),
        orchestration_trace=sample_trace(step_count=step_count),
        governance_trace_view={"rows": sample_governance_rows()},
        governed_evidence_package=sample_package(),
        animation_events=[],
    )


def test_replay_run_view_model_is_pure_composition_of_engine_outputs():
    run = build_sample_run()

    assert run["operational_confidence"] == "HIGH"
    assert run["confidence_direction"] == "STABLE"
    assert run["pattern_maturity"] == "TRUSTED"
    assert run["selected_due_diligence_level"] == "TARGETED_VALIDATION"
    assert run["why"] == [
        "Trusted memory pattern exists.",
        "Current evidence does not conflict with memory.",
    ]

    assert run["safety_boundaries"]["governance_required"] is True
    assert run["safety_boundaries"]["human_approval_required"] is True
    assert run["safety_boundaries"]["autonomous_action_allowed"] is False


def test_replay_run_view_model_preserves_governance_trace_values_without_invention():
    run = build_sample_run()
    rows = run["governance_trace_view"]["rows"]

    assert rows == sample_governance_rows()

    provenance = run["provenance"]

    assert provenance["audit_ids"] == ["AUDIT-001", "AUDIT-002"]
    assert provenance["governance_decisions"] == ["ALLOW", "DENY"]
    assert provenance["content_safety_statuses"] == [
        "REVIEW_REQUIRED",
        "SAFE_BY_APPROVED_PROVENANCE",
    ]
    assert provenance["allowed_for_reasoning_values"] == [False, True]
    assert provenance["approval_states"] == ["BLOCKED", "PENDING_HUMAN_REVIEW"]


def test_replay_run_view_model_preserves_evidence_ids_and_evidence_gaps():
    run = build_sample_run()

    assert [
        item["evidence_id"]
        for item in run["evidence_for_reasoning"]
    ] == ["EVIDENCE-001"]

    assert [
        item["evidence_id"]
        for item in run["excluded_evidence"]
    ] == ["EVIDENCE-EXCLUDED-001"]

    assert run["evidence_gaps"] == sample_package()["evidence_gaps"]

    assert run["provenance"]["evidence_ids"] == [
        "EVIDENCE-001",
        "EVIDENCE-EXCLUDED-001",
    ]


def test_replay_run_view_model_keeps_autonomous_action_disabled_from_source_output():
    run = build_sample_run()

    assert run["safety_boundaries"]["autonomous_action_allowed"] is False
    assert run["provenance"]["safety_boundaries"]["autonomous_action_allowed"] is False

    for row in run["governance_trace_view"]["rows"]:
        assert row["autonomous_action_allowed"] is False


def test_comparison_view_model_is_collection_of_replay_runs_not_new_decision_layer():
    no_memory_confidence = {
        **sample_confidence(),
        "operational_confidence": "LOW",
        "confidence_direction": "NEW",
        "pattern_maturity": "NONE",
        "selected_due_diligence_level": "FULL_DUE_DILIGENCE",
    }

    trusted = build_sample_run()
    no_memory = build_sample_run(
        run_id="run-no-memory",
        scenario_label="First-time / no memory",
        confidence=no_memory_confidence,
        step_count=7,
    )

    comparison = build_comparison_view_model(
        comparison_id="comparison-application-health",
        comparison_label="Same alert, different memory states",
        runs=[no_memory, trusted],
    )

    assert comparison["runs"] == [no_memory, trusted]

    assert comparison["summary"][0]["operational_confidence"] == "LOW"
    assert comparison["summary"][0]["selected_due_diligence_level"] == (
        "FULL_DUE_DILIGENCE"
    )
    assert comparison["summary"][0]["agent_step_count"] == 7

    assert comparison["summary"][1]["operational_confidence"] == "HIGH"
    assert comparison["summary"][1]["selected_due_diligence_level"] == (
        "TARGETED_VALIDATION"
    )
    assert comparison["summary"][1]["agent_step_count"] == 3

    for summary in comparison["summary"]:
        assert summary["governance_required"] is True
        assert summary["human_approval_required"] is True
        assert summary["autonomous_action_allowed"] is False
