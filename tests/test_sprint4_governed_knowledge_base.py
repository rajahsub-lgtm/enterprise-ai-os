from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint4.governed_knowledge_base import (
    KnowledgeQuality,
    KnowledgeQuery,
    KnowledgeSafety,
    load_governed_knowledge_base,
    retrieve_knowledge,
    summarize_retrieval_result,
)


def _kb():
    return load_governed_knowledge_base()


def test_governed_knowledge_base_loads_policy_boundary():
    kb = _kb()

    assert kb.knowledge_base_id == "it-application-health-governed-kb-structural-v1"
    assert kb.domain == "it_application_health"
    assert kb.policy["source_layer"] == "synthetic_imperfect_knowledge_layer"
    assert kb.policy["benchmark_truth_source"] is False
    assert kb.policy["benchmark_scoring_allowed"] is False
    assert kb.policy["knowledge_can_define_benchmark_truth"] is False
    assert kb.policy["knowledge_can_be_answer_key"] is False
    assert kb.policy["autonomous_action_allowed"] is False


def test_governed_knowledge_base_contains_imperfect_knowledge_types():
    kb = _kb()

    qualities = {article.quality for article in kb.articles}

    assert KnowledgeQuality.EXACT in qualities
    assert KnowledgeQuality.PARTIAL in qualities
    assert KnowledgeQuality.STALE in qualities
    assert KnowledgeQuality.CONFLICTING in qualities
    assert KnowledgeQuality.RISKY_REMEDIATION in qualities
    assert KnowledgeQuality.WRONG_APPLICATION in qualities
    assert KnowledgeQuality.HUMAN_APPROVAL_REQUIRED in qualities


def test_governed_knowledge_articles_cannot_be_benchmark_truth_or_actions():
    kb = _kb()

    assert all(article.benchmark_truth_eligible is False for article in kb.articles)
    assert all(article.can_score_benchmark is False for article in kb.articles)
    assert all(article.human_approval_required is True for article in kb.articles)
    assert all(article.autonomous_action_allowed is False for article in kb.articles)


def test_payment_latency_retrieval_returns_exact_and_conflicting_evidence():
    kb = _kb()

    result = retrieve_knowledge(
        kb,
        KnowledgeQuery(
            application="train-ticket-structural",
            service="payment-service",
            indicator="latency_p95_ms",
            fault_type="service_latency_injection",
        ),
    )

    qualities = {evidence.quality for evidence in result.evidence_items}

    assert KnowledgeQuality.EXACT in qualities
    assert KnowledgeQuality.CONFLICTING in qualities
    assert result.conflict_detected is True
    assert result.human_approval_required is True
    assert result.benchmark_scoring_allowed is False


def test_checkout_retrieval_returns_partial_evidence_only():
    kb = _kb()

    result = retrieve_knowledge(
        kb,
        KnowledgeQuery(
            application="train-ticket-structural",
            service="checkout-service",
            indicator="http_5xx_rate",
            fault_type="service_latency_injection",
        ),
    )

    assert tuple(evidence.quality for evidence in result.evidence_items) == (
        KnowledgeQuality.PARTIAL,
    )
    assert result.conflict_detected is False
    assert result.missing_knowledge is False


def test_order_timeout_retrieval_marks_stale_evidence():
    kb = _kb()

    result = retrieve_knowledge(
        kb,
        KnowledgeQuery(
            application="train-ticket-structural",
            service="order-service",
            indicator="downstream_timeout_count",
            fault_type="service_latency_injection",
        ),
    )

    assert result.stale_evidence_present is True
    assert result.evidence_items[0].quality == KnowledgeQuality.STALE
    assert result.evidence_items[0].safety == KnowledgeSafety.STALE_REVIEW_REQUIRED


def test_inventory_retrieval_marks_risky_and_human_approval_evidence():
    kb = _kb()

    result = retrieve_knowledge(
        kb,
        KnowledgeQuery(
            application="train-ticket-structural",
            service="inventory-service",
            indicator="db_connection_errors",
            fault_type="database_connection_error",
        ),
    )

    qualities = {evidence.quality for evidence in result.evidence_items}

    assert KnowledgeQuality.RISKY_REMEDIATION in qualities
    assert KnowledgeQuality.HUMAN_APPROVAL_REQUIRED in qualities
    assert result.risky_evidence_present is True
    assert result.human_approval_required is True


def test_wrong_application_articles_are_excluded_but_reported():
    kb = _kb()

    result = retrieve_knowledge(
        kb,
        KnowledgeQuery(
            application="train-ticket-structural",
            service="inventory-service",
            indicator="db_connection_errors",
            fault_type="database_connection_error",
        ),
    )

    assert result.excluded_wrong_application_article_ids == (
        "kb-wrong-app-inventory-001",
    )
    assert all(
        evidence.article_id != "kb-wrong-app-inventory-001"
        for evidence in result.evidence_items
    )


def test_missing_knowledge_returns_gap_evidence_not_truth():
    kb = _kb()

    result = retrieve_knowledge(
        kb,
        KnowledgeQuery(
            application="train-ticket-structural",
            service="route-planning-service",
            indicator="dependency_error_rate",
            fault_type="database_connection_error",
        ),
    )

    assert result.missing_knowledge is True
    assert len(result.evidence_items) == 1

    gap = result.evidence_items[0]

    assert gap.quality == KnowledgeQuality.MISSING
    assert gap.safety == KnowledgeSafety.MISSING_KNOWLEDGE
    assert gap.usable_for_reasoning is False
    assert gap.can_score_benchmark is False
    assert gap.benchmark_truth_eligible is False


def test_retrieved_evidence_preserves_no_autonomous_action_boundary():
    kb = _kb()

    result = retrieve_knowledge(
        kb,
        KnowledgeQuery(
            application="train-ticket-structural",
            service="payment-service",
            indicator="latency_p95_ms",
            fault_type="service_latency_injection",
        ),
    )

    assert all(evidence.human_approval_required is True for evidence in result.evidence_items)
    assert all(evidence.autonomous_action_allowed is False for evidence in result.evidence_items)
    assert all(evidence.can_score_benchmark is False for evidence in result.evidence_items)
    assert all(evidence.benchmark_truth_eligible is False for evidence in result.evidence_items)


def test_knowledge_retrieval_summary_is_view_ready():
    kb = _kb()

    result = retrieve_knowledge(
        kb,
        KnowledgeQuery(
            application="train-ticket-structural",
            service="payment-service",
            indicator="latency_p95_ms",
            fault_type="service_latency_injection",
        ),
    )

    summary = summarize_retrieval_result(result)

    assert summary["service"] == "payment-service"
    assert summary["indicator"] == "latency_p95_ms"
    assert summary["evidence_count"] == 2
    assert summary["missing_knowledge"] is False
    assert summary["conflict_detected"] is True
    assert summary["human_approval_required"] is True
    assert summary["benchmark_scoring_allowed"] is False


def test_governed_kb_module_does_not_import_benchmark_scoring_contracts():
    source = Path("src/eaios/sprint4/governed_knowledge_base.py").read_text(
        encoding="utf-8"
    )

    assert "BenchmarkVerificationTarget" not in source
    assert "BenchmarkVerificationResult" not in source
    assert "score_benchmark_result" not in source
