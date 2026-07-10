from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint4.governed_reasoning_observation import (
    build_governed_reasoning_observation_snapshot,
    summarize_governed_reasoning_observation,
    to_view_model,
)


def _snapshot():
    return build_governed_reasoning_observation_snapshot()


def test_governed_reasoning_observation_builds_end_to_end_4b_snapshot():
    snapshot = _snapshot()

    assert snapshot.snapshot_id == "governed-reasoning::composition-structural-001"
    assert snapshot.application_health_snapshot_id == (
        "application-health::composition-structural-001"
    )
    assert snapshot.source_dataset_role == "benchmark_truth_layer_structural_sample"
    assert snapshot.cluster_count == 2
    assert snapshot.provenance == "sprint4b:governed_reasoning_observation_snapshot"


def test_governed_reasoning_observation_preserves_4a_benchmark_results():
    snapshot = _snapshot()

    assert snapshot.benchmark_result_states == ("MATCHED", "MATCHED")
    assert snapshot.application_health_view["clustering_summary"] == {
        "cluster_count": 2,
        "excluded_noise_incident_count": 1,
        "benchmark_states": ("MATCHED", "MATCHED"),
        "matched_count": 2,
        "partial_count": 0,
        "missed_count": 0,
    }


def test_governed_reasoning_observation_includes_kb_evidence_summary():
    snapshot = _snapshot()

    assert snapshot.knowledge_evidence_summary == {
        "cluster_count": 2,
        "total_evidence_items": 7,
        "clusters_with_missing_knowledge": (
            "cluster::structural-failure-inventory-errors-001",
        ),
        "clusters_with_conflicts": (
            "cluster::structural-failure-payment-latency-001",
        ),
        "clusters_with_stale_evidence": (
            "cluster::structural-failure-payment-latency-001",
        ),
        "clusters_with_risky_evidence": (
            "cluster::structural-failure-inventory-errors-001",
        ),
        "human_approval_required": True,
        "benchmark_scoring_allowed": False,
        "autonomous_action_allowed": False,
    }


def test_governed_reasoning_observation_includes_reasoning_summary():
    snapshot = _snapshot()

    assert snapshot.knowledge_reasoning_summary["total_clusters"] == 2
    assert snapshot.knowledge_reasoning_summary["reasoning_states"] == (
        "SUPPORTED_WITH_CONFLICTS",
        "RISKY_OR_INCOMPLETE",
    )
    assert snapshot.knowledge_reasoning_summary["human_approval_required"] is True
    assert snapshot.knowledge_reasoning_summary["benchmark_scoring_allowed"] is False
    assert snapshot.knowledge_reasoning_summary["autonomous_action_allowed"] is False


def test_governed_reasoning_observation_includes_llm_engine_summary():
    snapshot = _snapshot()

    assert snapshot.llm_engine_summary == {
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


def test_governed_reasoning_observation_preserves_governance_boundaries():
    snapshot = _snapshot()

    assert "benchmark_truth_external" in snapshot.governance_boundaries
    assert "benchmark_scoring_from_4a_only" in snapshot.governance_boundaries
    assert "kb_evidence_cannot_define_truth" in snapshot.governance_boundaries
    assert "llm_output_cannot_score_benchmark" in snapshot.governance_boundaries
    assert "citations_required" in snapshot.governance_boundaries
    assert "uncertainty_required" in snapshot.governance_boundaries
    assert "human_approval_required" in snapshot.governance_boundaries
    assert "autonomous_action_disabled" in snapshot.governance_boundaries
    assert "provider_call_blocked" in snapshot.governance_boundaries


def test_governed_reasoning_observation_never_allows_kb_or_llm_benchmark_scoring():
    snapshot = _snapshot()

    assert snapshot.human_approval_required is True
    assert snapshot.benchmark_scoring_allowed_from_kb_or_llm is False
    assert snapshot.autonomous_action_allowed is False
    assert snapshot.provider_call_made is False

    assert snapshot.cluster_knowledge_view["summary"]["benchmark_scoring_allowed"] is False
    assert snapshot.knowledge_reasoning_view["benchmark_scoring_allowed"] is False
    assert snapshot.llm_engine_view["summary"]["benchmark_scoring_allowed"] is False


def test_governed_reasoning_observation_summary_is_view_ready():
    snapshot = _snapshot()

    summary = summarize_governed_reasoning_observation(snapshot)

    assert summary == {
        "snapshot_id": "governed-reasoning::composition-structural-001",
        "application_health_snapshot_id": (
            "application-health::composition-structural-001"
        ),
        "cluster_count": 2,
        "benchmark_result_states": ("MATCHED", "MATCHED"),
        "knowledge_evidence_total_items": 7,
        "knowledge_reasoning_states": (
            "SUPPORTED_WITH_CONFLICTS",
            "RISKY_OR_INCOMPLETE",
        ),
        "llm_accepted_output_count": 2,
        "llm_rejected_output_count": 0,
        "provider_call_made": False,
        "human_approval_required": True,
        "benchmark_scoring_allowed_from_kb_or_llm": False,
        "autonomous_action_allowed": False,
    }


def test_governed_reasoning_observation_view_model_is_json_serializable():
    snapshot = _snapshot()

    view_model = to_view_model(snapshot)
    serialized = json.dumps(view_model, indent=2)

    assert "governed-reasoning::composition-structural-001" in serialized
    assert "application_health" in serialized
    assert "cluster_knowledge" in serialized
    assert "knowledge_reasoning" in serialized
    assert "llm_engine" in serialized
    assert "benchmark_scoring_allowed_from_kb_or_llm" in serialized
    assert "provider_call_made" in serialized


def test_governed_reasoning_observation_view_model_contains_nested_contracts():
    snapshot = _snapshot()

    view_model = to_view_model(snapshot)

    assert "summary" in view_model["application_health"]
    assert "summary" in view_model["cluster_knowledge"]
    assert "summary" in view_model["knowledge_reasoning"]
    assert "summary" in view_model["llm_engine"]
    assert view_model["llm_engine"]["validation"]["accepted_cluster_count"] == 2
    assert view_model["llm_engine"]["validation"]["rejected_cluster_count"] == 0


def test_governed_reasoning_observation_module_does_not_call_real_provider_or_score_benchmark():
    source = Path("src/eaios/sprint4/governed_reasoning_observation.py").read_text(
        encoding="utf-8"
    )

    assert "openai" not in source.lower()
    assert "anthropic" not in source.lower()
    assert "requests" not in source.lower()
    assert "httpx" not in source.lower()
    assert "score_benchmark_result(" not in source
    assert "BenchmarkVerificationTarget" not in source
    assert "BenchmarkVerificationResult" not in source
