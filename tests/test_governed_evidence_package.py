import pytest

from src.governance.governed_evidence_client import GovernedEvidenceClient
from src.governance.governed_evidence_package import GovernedEvidencePackage
from src.governance.source_access_request import SourceAccessRequest
from src.governance.source_access_result import SourceAccessResult


def request(
    *,
    agent_id: str = "memory_pattern_agent",
    source_id: str = "enterprise_memory",
    evidence_class: str = "memory_state_evidence",
) -> SourceAccessRequest:
    return SourceAccessRequest(
        case_id="CASE-S3-001",
        agent_id=agent_id,
        source_id=source_id,
        capability="retrieve_memory_patterns",
        goal_category="application_health_management",
        purpose="evaluate prior enterprise experience",
        evidence_class=evidence_class,
        query="current case pattern",
    )


class FakeExistingGovernedSeam:
    def __init__(self, output: dict):
        self.output = output
        self.received_requests = []

    def retrieve(self, action_request: dict) -> dict:
        self.received_requests.append(action_request)
        return self.output


def allowed_output() -> dict:
    return {
        "access_decision": "ALLOW",
        "audit_id": "audit-001",
        "evidence_items": [
            {
                "evidence_id": "ev-abc123",
                "content_safety_status": "SAFE_BY_APPROVED_PROVENANCE",
                "allowed_for_reasoning": True,
                "summary": "Structured record was accepted by governed provenance.",
            }
        ],
    }


def denied_output() -> dict:
    return {
        "access_decision": "DENY",
        "audit_id": "audit-deny-001",
        "reason": "Policy did not allow this source access.",
        "required_controls": ["least_privilege_enforced"],
    }


def unsafe_output() -> dict:
    return {
        "access_decision": "ALLOW",
        "audit_id": "audit-unsafe-001",
        "evidence_items": [
            {
                "evidence_id": "ev-unsafe123",
                "content_safety_status": "UNSAFE",
                "allowed_for_reasoning": False,
                "summary": "Collected evidence is not eligible for reasoning.",
            }
        ],
    }


def test_source_access_request_wraps_existing_action_request_shape():
    action_request = request().to_action_request()

    assert action_request["agent_id"] == "memory_pattern_agent"
    assert action_request["subject_agent_id"] == "memory_pattern_agent"
    assert action_request["source_id"] == "enterprise_memory"
    assert action_request["resource_id"] == "enterprise_memory"
    assert action_request["goal_category"] == "application_health_management"
    assert action_request["capability"] == "retrieve_memory_patterns"


def test_governed_evidence_client_delegates_to_existing_seam():
    existing_seam = FakeExistingGovernedSeam(allowed_output())

    package = GovernedEvidenceClient(existing_seam).collect([request()])

    assert existing_seam.received_requests
    assert package.package_id == "GEP-CASE-S3-001"
    assert package.evidence_items
    assert package.evidence_items[0]["evidence_id"] == "ev-abc123"
    assert package.evidence_items[0]["audit_id"] == "audit-001"
    assert package.evidence_items[0]["allowed_for_reasoning"] is True


def test_governed_evidence_package_exposes_only_reasoning_eligible_items():
    package = GovernedEvidenceClient(
        FakeExistingGovernedSeam(unsafe_output())
    ).collect([request(evidence_class="free_text_evidence")])

    assert package.evidence_items
    assert package.evidence_for_reasoning() == []
    assert package.excluded_evidence()
    assert package.evidence_gaps
    assert "not eligible for reasoning" in package.evidence_gaps[0]["reason"]


def test_denied_source_access_becomes_evidence_gap_not_reasoning_evidence():
    package = GovernedEvidenceClient(
        FakeExistingGovernedSeam(denied_output())
    ).collect([request()])

    assert package.evidence_items == []
    assert len(package.evidence_gaps) == 1
    assert package.evidence_gaps[0]["access_decision"] == "DENY"
    assert package.evidence_for_reasoning() == []


def test_structured_record_evidence_uses_approved_provenance_status():
    package = GovernedEvidenceClient(
        FakeExistingGovernedSeam(allowed_output())
    ).collect([request(evidence_class="structured_record_evidence")])

    evidence = package.evidence_items[0]

    assert evidence["evidence_class"] == "structured_record_evidence"
    assert evidence["content_safety_status"] == "SAFE_BY_APPROVED_PROVENANCE"
    assert evidence["allowed_for_reasoning"] is True


def test_free_text_evidence_can_use_standard_safe_status():
    output = {
        "access_decision": "ALLOW",
        "audit_id": "audit-knowledge-001",
        "evidence_items": [
            {
                "evidence_id": "ev-knowledge001",
                "content_safety_status": "SAFE",
                "allowed_for_reasoning": True,
                "summary": "Free text evidence passed content safety checks.",
            }
        ],
    }

    package = GovernedEvidenceClient(
        FakeExistingGovernedSeam(output)
    ).collect(
        [
            request(
                agent_id="knowledge_retrieval_agent",
                source_id="support_knowledge",
                evidence_class="free_text_evidence",
            )
        ]
    )

    evidence = package.evidence_items[0]

    assert evidence["evidence_class"] == "free_text_evidence"
    assert evidence["content_safety_status"] == "SAFE"
    assert evidence["allowed_for_reasoning"] is True


def test_governed_evidence_package_matches_case_context_validator_contract():
    package = GovernedEvidenceClient(
        FakeExistingGovernedSeam(allowed_output())
    ).collect([request()])

    value = package.to_dict()

    assert value["package_id"] == "GEP-CASE-S3-001"
    assert value["case_id"] == "CASE-S3-001"
    assert isinstance(value["evidence_items"], list)
    assert isinstance(value["evidence_gaps"], list)


def test_rejects_cross_case_request_collection():
    client = GovernedEvidenceClient(FakeExistingGovernedSeam(allowed_output()))

    first = request()
    second = SourceAccessRequest(
        case_id="CASE-S3-002",
        agent_id="memory_pattern_agent",
        source_id="enterprise_memory",
        capability="retrieve_memory_patterns",
        goal_category="application_health_management",
        purpose="evaluate prior enterprise experience",
        evidence_class="memory_state_evidence",
    )

    with pytest.raises(ValueError):
        client.collect([first, second])


def test_source_access_result_rejects_unsupported_evidence_class_when_packaged():
    bad_result = SourceAccessResult(
        case_id="CASE-S3-001",
        agent_id="agent",
        source_id="source",
        capability="capability",
        goal_category="application_health_management",
        purpose="purpose",
        evidence_class="unsupported_class",
        access_decision="ALLOW",
        audit_id="audit",
        evidence_id="ev-bad",
        content_safety_status="SAFE",
        allowed_for_reasoning=True,
    )

    with pytest.raises(ValueError):
        GovernedEvidencePackage.from_results(
            case_id="CASE-S3-001",
            results=[bad_result],
        )
