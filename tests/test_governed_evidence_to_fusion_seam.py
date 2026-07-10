import pytest

from src.governance.evidence_fusion import EvidenceFusionEngine, FusionInputError


def governed_context(package: dict | None = None) -> dict:
    return {
        "case_id": "CASE-S3-001",
        "scenario_id": "SCENARIO-S3-001",
        "business_outcome": "Maintain Business Capability",
        "goal_category": "application_health_management",
        "human_approval_required": True,
        "impact": {
            "impact_tier": "HIGH",
            "impact_confidence": "HIGH",
        },
        "governed_evidence_package": package or governed_package(),
    }


def governed_package() -> dict:
    return {
        "package_id": "GEP-CASE-S3-001",
        "case_id": "CASE-S3-001",
        "evidence_items": [
            {
                "evidence_id": "ev-memory-001",
                "source_id": "enterprise_memory",
                "agent_id": "memory_pattern_agent",
                "capability": "retrieve_memory_patterns",
                "goal_category": "application_health_management",
                "purpose": "evaluate prior enterprise experience",
                "access_decision": "ALLOW",
                "audit_id": "audit-memory-001",
                "content_safety_status": "SAFE_BY_APPROVED_PROVENANCE",
                "allowed_for_reasoning": True,
                "evidence_class": "memory_state_evidence",
                "payload": {
                    "summary": "Prior governed experience supports this pattern.",
                    "trust_level": "APPROVED_HIGH",
                },
            },
            {
                "evidence_id": "ev-knowledge-001",
                "source_id": "support_knowledge",
                "agent_id": "knowledge_retrieval_agent",
                "capability": "retrieve_support_knowledge",
                "goal_category": "application_health_management",
                "purpose": "retrieve governed support knowledge",
                "access_decision": "ALLOW",
                "audit_id": "audit-knowledge-001",
                "content_safety_status": "SAFE",
                "allowed_for_reasoning": True,
                "evidence_class": "free_text_evidence",
                "payload": {
                    "summary": "Governed support knowledge supports the hypothesis.",
                    "trust_level": "APPROVED_HIGH",
                },
            },
        ],
        "evidence_gaps": [],
    }


def test_fusion_accepts_governed_evidence_package():
    result = EvidenceFusionEngine().fuse(governed_context())

    assert result["governed_package_id"] == "GEP-CASE-S3-001"
    assert result["fusion_confidence"] == "HIGH"
    assert result["autonomous_action_allowed"] is False
    assert len(result["supporting_evidence"]) == 2


def test_reasoning_eligible_governed_evidence_enters_supporting_fusion():
    result = EvidenceFusionEngine().fuse(governed_context())

    supporting_ids = {
        evidence["evidence_id"] for evidence in result["supporting_evidence"]
    }

    assert supporting_ids == {"ev-memory-001", "ev-knowledge-001"}
    assert result["reasoning_eligible_evidence_ids"] == [
        "ev-memory-001",
        "ev-knowledge-001",
    ]


def test_audit_ids_are_preserved_in_fusion_result():
    result = EvidenceFusionEngine().fuse(governed_context())

    assert result["audit_ids"] == ["audit-knowledge-001", "audit-memory-001"]

    supporting_audit_ids = {
        evidence["audit_id"] for evidence in result["supporting_evidence"]
    }

    assert supporting_audit_ids == {"audit-memory-001", "audit-knowledge-001"}


def test_unsafe_governed_evidence_is_excluded_from_reasoning():
    package = governed_package()
    package["evidence_items"][0]["content_safety_status"] = "UNSAFE"
    package["evidence_items"][0]["allowed_for_reasoning"] = False

    result = EvidenceFusionEngine().fuse(governed_context(package))

    supporting_ids = {
        evidence["evidence_id"] for evidence in result["supporting_evidence"]
    }

    assert "ev-memory-001" not in supporting_ids
    assert "ev-memory-001" in result["excluded_evidence_ids"]
    assert result["missing_evidence"][0]["evidence_type"] == "excluded_unsafe_content"
    assert result["fusion_confidence"] == "LOW"


def test_review_required_evidence_is_excluded_and_flagged_for_review():
    package = governed_package()
    package["evidence_items"][1]["content_safety_status"] = "NEEDS_HUMAN_REVIEW"
    package["evidence_items"][1]["allowed_for_reasoning"] = False

    result = EvidenceFusionEngine().fuse(governed_context(package))

    supporting_ids = {
        evidence["evidence_id"] for evidence in result["supporting_evidence"]
    }

    assert "ev-knowledge-001" not in supporting_ids
    assert "ev-knowledge-001" in result["excluded_evidence_ids"]
    assert result["missing_evidence"][0]["evidence_type"] == "missing_human_validation"
    assert result["requires_human_review"] is True


def test_denied_access_gap_flows_into_fusion():
    package = governed_package()
    package["evidence_items"] = []
    package["evidence_gaps"] = [
        {
            "gap_id": "GAP-DENIED-001",
            "source_id": "itil_business_impact_map",
            "agent_id": "memory_pattern_agent",
            "audit_id": "audit-denied-001",
            "reason": "Agent is not entitled to this source.",
        }
    ]

    result = EvidenceFusionEngine().fuse(governed_context(package))

    assert result["supporting_evidence"] == []
    assert result["evidence_gaps"][0]["gap_id"] == "GAP-DENIED-001"
    assert result["audit_ids"] == ["audit-denied-001"]
    assert result["fusion_confidence"] == "LOW"


def test_low_trust_governed_evidence_weakens_confidence():
    package = governed_package()
    package["evidence_items"][0]["payload"]["trust_level"] = "CONDITIONAL"

    result = EvidenceFusionEngine().fuse(governed_context(package))

    assert result["weakening_evidence"]
    assert result["fusion_confidence"] == "MEDIUM"


def test_conflicting_governed_evidence_creates_conflict_and_low_confidence():
    package = governed_package()
    package["evidence_items"][0]["payload"]["conflicts_with"] = "recent validation"

    result = EvidenceFusionEngine().fuse(governed_context(package))

    assert result["conflicting_evidence"]
    assert result["fusion_confidence"] == "LOW"


def test_raw_ungoverned_records_are_rejected():
    context = {
        "case_id": "CASE-S3-RAW",
        "business_outcome": "Maintain Business Capability",
        "goal_category": "application_health_management",
        "raw_source_records": [
            {
                "source_id": "enterprise_memory",
                "summary": "Raw record bypassed governed evidence package.",
            }
        ],
    }

    with pytest.raises(FusionInputError):
        EvidenceFusionEngine().fuse(context)


def test_denied_access_cannot_be_disguised_as_evidence_item():
    package = governed_package()
    package["evidence_items"][0]["access_decision"] = "DENY"

    with pytest.raises(FusionInputError):
        EvidenceFusionEngine().fuse(governed_context(package))
