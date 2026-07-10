from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint4.governed_llm_reasoning_engine import (
    LLMRunMode,
    build_prompt_packet,
    run_governed_llm_reasoning_engine,
    summarize_engine_run,
    to_view_model,
)
from eaios.sprint4.governed_knowledge_reasoning import (
    build_governed_knowledge_reasoning,
)


def test_llm_reasoning_engine_runs_in_deterministic_contract_mode():
    run = run_governed_llm_reasoning_engine()

    assert run.run_id == "sprint4b-governed-llm-reasoning-engine-run-001"
    assert run.mode == LLMRunMode.DETERMINISTIC_CONTRACT
    assert run.provider_call_made is False
    assert len(run.prompt_packets) == 2
    assert len(run.proposed_outputs) == 2
    assert len(run.accepted_outputs) == 2
    assert len(run.rejected_outputs) == 0


def test_llm_reasoning_engine_validates_all_deterministic_outputs():
    run = run_governed_llm_reasoning_engine()

    assert run.validation_result.accepted_cluster_count == 2
    assert run.validation_result.rejected_cluster_count == 0
    assert all(validation.accepted for validation in run.validation_result.validations)


def test_prompt_packets_preserve_citations_and_uncertainty_instructions():
    reasoning = build_governed_knowledge_reasoning()
    payment = next(
        item for item in reasoning.cluster_reasoning
        if item.cluster_id == "cluster::structural-failure-payment-latency-001"
    )

    packet = build_prompt_packet(payment)

    assert packet.packet_id == "llm-prompt::cluster::structural-failure-payment-latency-001"
    assert packet.evidence_ids
    assert all("knowledge-evidence::" in evidence_id or "knowledge-gap::" in evidence_id for evidence_id in packet.evidence_ids)
    assert "human_review_required" in packet.required_uncertainty_flags
    assert "not_benchmark_truth" in packet.required_uncertainty_flags
    assert "conflict_detected" in packet.required_uncertainty_flags
    assert "stale_evidence_present" in packet.required_uncertainty_flags


def test_prompt_packets_block_benchmark_truth_scoring_and_autonomous_action():
    run = run_governed_llm_reasoning_engine()

    for packet in run.prompt_packets:
        assert "benchmark truth" in packet.prohibited_claims
        assert "benchmark score" in packet.prohibited_claims
        assert "autonomous approval" in packet.prohibited_claims
        assert packet.safety_envelope.human_approval_required is True
        assert packet.safety_envelope.autonomous_action_allowed is False
        assert packet.safety_envelope.benchmark_truth_claim_allowed is False
        assert packet.safety_envelope.benchmark_scoring_allowed is False
        assert packet.safety_envelope.provider_call_allowed is False


def test_prompt_packets_include_cost_loop_and_token_limits():
    run = run_governed_llm_reasoning_engine()

    for packet in run.prompt_packets:
        assert packet.safety_envelope.max_prompt_evidence_items == 20
        assert packet.safety_envelope.max_reasoning_loops == 1
        assert packet.safety_envelope.max_estimated_tokens == 2400
        assert packet.safety_envelope.max_estimated_cost_usd == 0.05


def test_llm_reasoning_engine_preserves_global_governance_boundaries():
    run = run_governed_llm_reasoning_engine()

    assert run.human_approval_required is True
    assert run.benchmark_scoring_allowed is False
    assert run.autonomous_action_allowed is False

    for output in run.accepted_outputs:
        assert output.human_approval_required is True
        assert output.autonomous_action_allowed is False
        assert output.benchmark_truth_claim_allowed is False
        assert output.benchmark_scoring_allowed is False


def test_llm_reasoning_engine_summary_is_view_ready():
    run = run_governed_llm_reasoning_engine()

    summary = summarize_engine_run(run)

    assert summary == {
        "run_id": "sprint4b-governed-llm-reasoning-engine-run-001",
        "mode": "DETERMINISTIC_CONTRACT",
        "prompt_packet_count": 2,
        "proposed_output_count": 2,
        "accepted_output_count": 2,
        "rejected_output_count": 0,
        "provider_call_made": False,
        "human_approval_required": True,
        "benchmark_scoring_allowed": False,
        "autonomous_action_allowed": False,
        "validation_issue_codes": (),
    }


def test_llm_reasoning_engine_view_model_is_json_serializable():
    run = run_governed_llm_reasoning_engine()

    view_model = to_view_model(run)
    serialized = json.dumps(view_model, indent=2)

    assert "sprint4b-governed-llm-reasoning-engine-run-001" in serialized
    assert "prompt_packets" in serialized
    assert "accepted_outputs" in serialized
    assert "provider_call_allowed" in serialized
    assert "benchmark_scoring_allowed" in serialized
    assert "autonomous_action_allowed" in serialized


def test_provider_ready_blocked_mode_still_makes_no_provider_call():
    run = run_governed_llm_reasoning_engine(mode=LLMRunMode.PROVIDER_READY_BLOCKED)

    assert run.mode == LLMRunMode.PROVIDER_READY_BLOCKED
    assert run.provider_call_made is False
    assert len(run.accepted_outputs) == 2
    assert run.validation_result.accepted_cluster_count == 2


def test_llm_reasoning_engine_module_does_not_call_real_provider_or_benchmark_scorer():
    source = Path("src/eaios/sprint4/governed_llm_reasoning_engine.py").read_text(
        encoding="utf-8"
    )

    assert "openai" not in source.lower()
    assert "anthropic" not in source.lower()
    assert "requests" not in source.lower()
    assert "httpx" not in source.lower()
    assert "from eaios.sprint4.rcaeval_contracts import" not in source
    assert "score_benchmark_result(" not in source
