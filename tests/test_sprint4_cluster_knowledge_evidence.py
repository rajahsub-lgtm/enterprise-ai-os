from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint4.cluster_knowledge_evidence import (
    build_cluster_knowledge_evidence,
    summarize_cluster_knowledge_evidence,
    to_view_model,
)


def _result():
    return build_cluster_knowledge_evidence()


def test_cluster_knowledge_evidence_builds_one_bundle_per_cluster():
    result = _result()

    assert len(result.bundles) == 2
    assert {
        bundle.source_failure_case_id for bundle in result.bundles
    } == {
        "structural-failure-payment-latency-001",
        "structural-failure-inventory-errors-001",
    }


def test_payment_cluster_includes_exact_partial_stale_and_conflicting_evidence():
    result = _result()

    payment_bundle = next(
        bundle for bundle in result.bundles
        if bundle.source_failure_case_id == "structural-failure-payment-latency-001"
    )

    qualities = {evidence.quality.value for evidence in payment_bundle.evidence_items}

    assert "exact" in qualities
    assert "partial" in qualities
    assert "stale" in qualities
    assert "conflicting" in qualities
    assert payment_bundle.conflict_detected is True
    assert payment_bundle.stale_evidence_present is True
    assert payment_bundle.risky_evidence_present is False


def test_inventory_cluster_includes_risky_human_approval_and_missing_evidence():
    result = _result()

    inventory_bundle = next(
        bundle for bundle in result.bundles
        if bundle.source_failure_case_id == "structural-failure-inventory-errors-001"
    )

    qualities = {evidence.quality.value for evidence in inventory_bundle.evidence_items}

    assert "risky_remediation" in qualities
    assert "human_approval_required" in qualities
    assert "missing" in qualities
    assert inventory_bundle.missing_knowledge is True
    assert inventory_bundle.risky_evidence_present is True


def test_cluster_knowledge_evidence_never_allows_benchmark_scoring():
    result = _result()

    assert result.benchmark_scoring_allowed is False
    assert all(bundle.benchmark_scoring_allowed is False for bundle in result.bundles)
    assert all(bundle.benchmark_truth_eligible is False for bundle in result.bundles)
    assert all(
        evidence.can_score_benchmark is False
        for bundle in result.bundles
        for evidence in bundle.evidence_items
    )
    assert all(
        evidence.benchmark_truth_eligible is False
        for bundle in result.bundles
        for evidence in bundle.evidence_items
    )


def test_cluster_knowledge_evidence_preserves_human_approval_and_no_autonomous_action():
    result = _result()

    assert result.human_approval_required is True
    assert result.autonomous_action_allowed is False
    assert all(bundle.human_approval_required is True for bundle in result.bundles)
    assert all(bundle.autonomous_action_allowed is False for bundle in result.bundles)
    assert all(
        evidence.human_approval_required is True
        for bundle in result.bundles
        for evidence in bundle.evidence_items
    )
    assert all(
        evidence.autonomous_action_allowed is False
        for bundle in result.bundles
        for evidence in bundle.evidence_items
    )


def test_cluster_knowledge_evidence_reports_article_ids_and_gaps():
    result = _result()

    all_article_ids = {
        article_id
        for bundle in result.bundles
        for article_id in bundle.evidence_article_ids
    }

    assert "kb-payment-latency-exact-001" in all_article_ids
    assert "kb-payment-latency-conflict-001" in all_article_ids
    assert "kb-inventory-db-risky-001" in all_article_ids
    assert "kb-inventory-db-human-approval-001" in all_article_ids

    inventory_bundle = next(
        bundle for bundle in result.bundles
        if bundle.source_failure_case_id == "structural-failure-inventory-errors-001"
    )
    assert any(
        evidence.article_id is None and evidence.quality.value == "missing"
        for evidence in inventory_bundle.evidence_items
    )


def test_cluster_knowledge_evidence_summary_is_view_ready():
    result = _result()

    summary = summarize_cluster_knowledge_evidence(result)

    assert summary == {
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


def test_cluster_knowledge_evidence_view_model_is_json_serializable():
    result = _result()

    view_model = to_view_model(result)
    serialized = json.dumps(view_model, indent=2)

    assert "cluster::structural-failure-payment-latency-001" in serialized
    assert "cluster::structural-failure-inventory-errors-001" in serialized
    assert "conflicting" in serialized
    assert "missing" in serialized
    assert "benchmark_scoring_allowed" in serialized


def test_cluster_knowledge_evidence_module_does_not_score_benchmarks():
    source = Path("src/eaios/sprint4/cluster_knowledge_evidence.py").read_text(
        encoding="utf-8"
    )

    assert "score_benchmark_result" not in source
    assert "BenchmarkVerificationResult" not in source
    assert "BenchmarkVerificationTarget" not in source
    assert "can_score_benchmark=True" not in source
    assert "benchmark_scoring_allowed=True" not in source
