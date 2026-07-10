from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint4.governed_knowledge_reasoning import (
    build_governed_knowledge_reasoning,
)
from eaios.sprint4.governed_llm_output_validator import (
    LLMValidationIssueCode,
    ProposedLLMClusterOutput,
    build_deterministic_llm_draft,
    summarize_validation_result,
    to_view_model,
    validate_llm_outputs,
)


def _reasoning():
    return build_governed_knowledge_reasoning()


def test_deterministic_llm_draft_validates_successfully():
    reasoning = _reasoning()
    draft = build_deterministic_llm_draft(reasoning)

    result = validate_llm_outputs(draft, reasoning)

    assert result.accepted_cluster_count == 2
    assert result.rejected_cluster_count == 0
    assert all(validation.accepted for validation in result.validations)


def test_deterministic_llm_draft_preserves_required_uncertainty_flags():
    reasoning = _reasoning()
    draft = build_deterministic_llm_draft(reasoning)

    payment = next(
        output for output in draft
        if output.cluster_id == "cluster::structural-failure-payment-latency-001"
    )
    inventory = next(
        output for output in draft
        if output.cluster_id == "cluster::structural-failure-inventory-errors-001"
    )

    assert "human_review_required" in payment.uncertainty_flags
    assert "not_benchmark_truth" in payment.uncertainty_flags
    assert "conflict_detected" in payment.uncertainty_flags
    assert "stale_evidence_present" in payment.uncertainty_flags

    assert "human_review_required" in inventory.uncertainty_flags
    assert "not_benchmark_truth" in inventory.uncertainty_flags
    assert "knowledge_gap_present" in inventory.uncertainty_flags
    assert "risky_remediation_present" in inventory.uncertainty_flags


def test_llm_validator_rejects_missing_citations():
    reasoning = _reasoning()
    draft = list(build_deterministic_llm_draft(reasoning))
    original = draft[0]

    draft[0] = ProposedLLMClusterOutput(
        cluster_id=original.cluster_id,
        source_failure_case_id=original.source_failure_case_id,
        conclusion=original.conclusion,
        cited_evidence_ids=(),
        uncertainty_flags=original.uncertainty_flags,
        recommended_next_steps=original.recommended_next_steps,
        human_approval_required=True,
        autonomous_action_allowed=False,
        benchmark_truth_claim_allowed=False,
        benchmark_scoring_allowed=False,
        provenance=original.provenance,
    )

    result = validate_llm_outputs(tuple(draft), reasoning)
    issue_codes = {
        issue.code
        for validation in result.validations
        for issue in validation.issues
    }

    assert result.rejected_cluster_count == 1
    assert LLMValidationIssueCode.MISSING_CITATIONS in issue_codes


def test_llm_validator_rejects_unknown_citations():
    reasoning = _reasoning()
    draft = list(build_deterministic_llm_draft(reasoning))
    original = draft[0]

    draft[0] = ProposedLLMClusterOutput(
        cluster_id=original.cluster_id,
        source_failure_case_id=original.source_failure_case_id,
        conclusion=original.conclusion,
        cited_evidence_ids=original.cited_evidence_ids + ("not-a-real-evidence-id",),
        uncertainty_flags=original.uncertainty_flags,
        recommended_next_steps=original.recommended_next_steps,
        human_approval_required=True,
        autonomous_action_allowed=False,
        benchmark_truth_claim_allowed=False,
        benchmark_scoring_allowed=False,
        provenance=original.provenance,
    )

    result = validate_llm_outputs(tuple(draft), reasoning)
    issue_codes = {
        issue.code
        for validation in result.validations
        for issue in validation.issues
    }

    assert result.rejected_cluster_count == 1
    assert LLMValidationIssueCode.UNKNOWN_CITATION in issue_codes


def test_llm_validator_rejects_missing_required_uncertainty_flags():
    reasoning = _reasoning()
    draft = list(build_deterministic_llm_draft(reasoning))
    original = draft[0]

    draft[0] = ProposedLLMClusterOutput(
        cluster_id=original.cluster_id,
        source_failure_case_id=original.source_failure_case_id,
        conclusion=original.conclusion,
        cited_evidence_ids=original.cited_evidence_ids,
        uncertainty_flags=("human_review_required", "not_benchmark_truth"),
        recommended_next_steps=original.recommended_next_steps,
        human_approval_required=True,
        autonomous_action_allowed=False,
        benchmark_truth_claim_allowed=False,
        benchmark_scoring_allowed=False,
        provenance=original.provenance,
    )

    result = validate_llm_outputs(tuple(draft), reasoning)
    issue_codes = {
        issue.code
        for validation in result.validations
        for issue in validation.issues
    }

    assert result.rejected_cluster_count == 1
    assert LLMValidationIssueCode.MISSING_UNCERTAINTY_FLAG in issue_codes


def test_llm_validator_rejects_benchmark_truth_and_scoring_claims():
    reasoning = _reasoning()
    draft = list(build_deterministic_llm_draft(reasoning))
    original = draft[0]

    draft[0] = ProposedLLMClusterOutput(
        cluster_id=original.cluster_id,
        source_failure_case_id=original.source_failure_case_id,
        conclusion="This is benchmark truth and proves the root cause.",
        cited_evidence_ids=original.cited_evidence_ids,
        uncertainty_flags=original.uncertainty_flags,
        recommended_next_steps=original.recommended_next_steps,
        human_approval_required=True,
        autonomous_action_allowed=False,
        benchmark_truth_claim_allowed=True,
        benchmark_scoring_allowed=True,
        provenance=original.provenance,
    )

    result = validate_llm_outputs(tuple(draft), reasoning)
    issue_codes = {
        issue.code
        for validation in result.validations
        for issue in validation.issues
    }

    assert result.rejected_cluster_count == 1
    assert LLMValidationIssueCode.BENCHMARK_TRUTH_CLAIM_BLOCKED in issue_codes
    assert LLMValidationIssueCode.BENCHMARK_SCORING_BLOCKED in issue_codes
    assert LLMValidationIssueCode.OVERCONFIDENT_CONCLUSION_BLOCKED in issue_codes


def test_llm_validator_rejects_autonomous_action_or_missing_human_approval():
    reasoning = _reasoning()
    draft = list(build_deterministic_llm_draft(reasoning))
    original = draft[0]

    draft[0] = ProposedLLMClusterOutput(
        cluster_id=original.cluster_id,
        source_failure_case_id=original.source_failure_case_id,
        conclusion="Governed evidence suggests a reviewable hypothesis.",
        cited_evidence_ids=original.cited_evidence_ids,
        uncertainty_flags=original.uncertainty_flags,
        recommended_next_steps=original.recommended_next_steps,
        human_approval_required=False,
        autonomous_action_allowed=True,
        benchmark_truth_claim_allowed=False,
        benchmark_scoring_allowed=False,
        provenance=original.provenance,
    )

    result = validate_llm_outputs(tuple(draft), reasoning)
    issue_codes = {
        issue.code
        for validation in result.validations
        for issue in validation.issues
    }

    assert result.rejected_cluster_count == 1
    assert LLMValidationIssueCode.HUMAN_APPROVAL_REQUIRED in issue_codes
    assert LLMValidationIssueCode.AUTONOMOUS_ACTION_BLOCKED in issue_codes


def test_llm_validator_summary_is_view_ready():
    reasoning = _reasoning()
    draft = build_deterministic_llm_draft(reasoning)

    result = validate_llm_outputs(draft, reasoning)
    summary = summarize_validation_result(result)

    assert summary == {
        "accepted_cluster_count": 2,
        "rejected_cluster_count": 0,
        "issue_codes": (),
        "human_approval_required": True,
        "benchmark_scoring_allowed": False,
        "autonomous_action_allowed": False,
    }


def test_llm_validator_view_model_is_json_serializable():
    reasoning = _reasoning()
    draft = build_deterministic_llm_draft(reasoning)

    result = validate_llm_outputs(draft, reasoning)
    view_model = to_view_model(result)
    serialized = json.dumps(view_model, indent=2)

    assert "accepted_cluster_count" in serialized
    assert "required_uncertainty_flags" in serialized
    assert "benchmark_scoring_allowed" in serialized
    assert "autonomous_action_allowed" in serialized


def test_llm_validator_module_does_not_call_real_provider_or_benchmark_scorer():
    source = Path("src/eaios/sprint4/governed_llm_output_validator.py").read_text(
        encoding="utf-8"
    )

    assert "openai" not in source.lower()
    assert "anthropic" not in source.lower()
    assert "requests" not in source.lower()
    assert "httpx" not in source.lower()
    assert "from eaios.sprint4.rcaeval_contracts import" not in source
    assert "score_benchmark_result(" not in source
