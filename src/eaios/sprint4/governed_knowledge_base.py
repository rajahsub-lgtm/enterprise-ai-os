"""Sprint 4B governed imperfect knowledge base.

Classification: governed uncertain evidence layer.

This module introduces synthetic imperfect knowledge for Sprint 4B. It is not a
truth source and cannot score benchmark results. It returns governed evidence
that later LLM reasoning can use with citations, uncertainty, safety state, and
human-approval boundaries.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import json
from pathlib import Path
from typing import Any


DEFAULT_KB_PATH = Path(
    "data/domain/it_application_health/governed_imperfect_knowledge_base.json"
)


class KnowledgeQuality(str, Enum):
    EXACT = "exact"
    PARTIAL = "partial"
    STALE = "stale"
    CONFLICTING = "conflicting"
    RISKY_REMEDIATION = "risky_remediation"
    WRONG_APPLICATION = "wrong_application"
    HUMAN_APPROVAL_REQUIRED = "human_approval_required"
    MISSING = "missing"


class KnowledgeSafety(str, Enum):
    HUMAN_APPROVAL_REQUIRED = "human_approval_required"
    STALE_REVIEW_REQUIRED = "stale_review_required"
    CONFLICT_REVIEW_REQUIRED = "conflict_review_required"
    RISKY_REMEDIATION = "risky_remediation"
    WRONG_APPLICATION = "wrong_application"
    MISSING_KNOWLEDGE = "missing_knowledge"


@dataclass(frozen=True)
class GovernedKnowledgeArticle:
    article_id: str
    title: str
    application: str
    service: str
    indicators: tuple[str, ...]
    related_services: tuple[str, ...]
    fault_types: tuple[str, ...]
    quality: KnowledgeQuality
    safety: KnowledgeSafety
    summary: str
    recommended_actions: tuple[str, ...]
    staleness_days: int
    confidence_hint: float
    contradicted_by: tuple[str, ...]
    benchmark_truth_eligible: bool
    can_score_benchmark: bool
    human_approval_required: bool
    autonomous_action_allowed: bool
    provenance: str


@dataclass(frozen=True)
class GovernedKnowledgeBase:
    knowledge_base_id: str
    domain: str
    policy: dict[str, Any]
    articles: tuple[GovernedKnowledgeArticle, ...]


@dataclass(frozen=True)
class KnowledgeQuery:
    application: str
    service: str
    indicator: str
    fault_type: str | None = None


@dataclass(frozen=True)
class GovernedKnowledgeEvidence:
    evidence_id: str
    article_id: str | None
    title: str
    quality: KnowledgeQuality
    safety: KnowledgeSafety
    service: str
    indicator: str
    summary: str
    recommended_actions: tuple[str, ...]
    evidence_weight: float
    usable_for_reasoning: bool
    benchmark_truth_eligible: bool
    can_score_benchmark: bool
    human_approval_required: bool
    autonomous_action_allowed: bool
    provenance: str


@dataclass(frozen=True)
class KnowledgeRetrievalResult:
    query: KnowledgeQuery
    evidence_items: tuple[GovernedKnowledgeEvidence, ...]
    excluded_wrong_application_article_ids: tuple[str, ...]
    missing_knowledge: bool
    conflict_detected: bool
    stale_evidence_present: bool
    risky_evidence_present: bool
    human_approval_required: bool
    benchmark_scoring_allowed: bool


def load_governed_knowledge_base(
    path: str | Path = DEFAULT_KB_PATH,
) -> GovernedKnowledgeBase:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    policy = payload["policy"]

    if policy["benchmark_truth_source"] is not False:
        raise ValueError("Knowledge base must not be marked as benchmark truth.")
    if policy["benchmark_scoring_allowed"] is not False:
        raise ValueError("Knowledge base must not be allowed to score benchmarks.")
    if policy["knowledge_can_be_answer_key"] is not False:
        raise ValueError("Knowledge base cannot be the answer key.")
    if policy["autonomous_action_allowed"] is not False:
        raise ValueError("Knowledge base must not allow autonomous action.")

    articles = tuple(_parse_article(raw) for raw in payload["articles"])

    if any(article.benchmark_truth_eligible for article in articles):
        raise ValueError("Knowledge articles must not be benchmark truth.")
    if any(article.can_score_benchmark for article in articles):
        raise ValueError("Knowledge articles must not score benchmarks.")
    if any(article.autonomous_action_allowed for article in articles):
        raise ValueError("Knowledge articles must not allow autonomous action.")

    return GovernedKnowledgeBase(
        knowledge_base_id=payload["knowledge_base_id"],
        domain=payload["domain"],
        policy=policy,
        articles=articles,
    )


def retrieve_knowledge(
    knowledge_base: GovernedKnowledgeBase,
    query: KnowledgeQuery,
) -> KnowledgeRetrievalResult:
    valid_articles = tuple(
        article
        for article in knowledge_base.articles
        if _matches_query(article, query)
    )
    wrong_application_articles = tuple(
        article
        for article in knowledge_base.articles
        if _matches_service_indicator(article, query)
        and article.application != query.application
    )

    evidence_items = tuple(
        _article_to_evidence(article, query)
        for article in valid_articles
    )

    if not evidence_items:
        evidence_items = (_missing_evidence(query),)

    return KnowledgeRetrievalResult(
        query=query,
        evidence_items=evidence_items,
        excluded_wrong_application_article_ids=tuple(
            article.article_id for article in wrong_application_articles
        ),
        missing_knowledge=all(
            evidence.quality == KnowledgeQuality.MISSING
            for evidence in evidence_items
        ),
        conflict_detected=any(
            evidence.quality == KnowledgeQuality.CONFLICTING
            for evidence in evidence_items
        ),
        stale_evidence_present=any(
            evidence.quality == KnowledgeQuality.STALE
            for evidence in evidence_items
        ),
        risky_evidence_present=any(
            evidence.quality == KnowledgeQuality.RISKY_REMEDIATION
            or evidence.safety == KnowledgeSafety.RISKY_REMEDIATION
            for evidence in evidence_items
        ),
        human_approval_required=True,
        benchmark_scoring_allowed=False,
    )


def summarize_retrieval_result(
    result: KnowledgeRetrievalResult,
) -> dict[str, object]:
    return {
        "service": result.query.service,
        "indicator": result.query.indicator,
        "evidence_count": len(result.evidence_items),
        "qualities": tuple(
            evidence.quality.value for evidence in result.evidence_items
        ),
        "missing_knowledge": result.missing_knowledge,
        "conflict_detected": result.conflict_detected,
        "stale_evidence_present": result.stale_evidence_present,
        "risky_evidence_present": result.risky_evidence_present,
        "human_approval_required": result.human_approval_required,
        "benchmark_scoring_allowed": result.benchmark_scoring_allowed,
        "excluded_wrong_application_article_ids": (
            result.excluded_wrong_application_article_ids
        ),
    }


def _parse_article(raw: dict[str, Any]) -> GovernedKnowledgeArticle:
    return GovernedKnowledgeArticle(
        article_id=raw["article_id"],
        title=raw["title"],
        application=raw["application"],
        service=raw["service"],
        indicators=tuple(raw["indicators"]),
        related_services=tuple(raw["related_services"]),
        fault_types=tuple(raw["fault_types"]),
        quality=KnowledgeQuality(raw["quality"]),
        safety=KnowledgeSafety(raw["safety"]),
        summary=raw["summary"],
        recommended_actions=tuple(raw["recommended_actions"]),
        staleness_days=int(raw["staleness_days"]),
        confidence_hint=float(raw["confidence_hint"]),
        contradicted_by=tuple(raw.get("contradicted_by", ())),
        benchmark_truth_eligible=bool(raw["benchmark_truth_eligible"]),
        can_score_benchmark=bool(raw["can_score_benchmark"]),
        human_approval_required=bool(raw["human_approval_required"]),
        autonomous_action_allowed=bool(raw["autonomous_action_allowed"]),
        provenance=raw["provenance"],
    )


def _matches_query(
    article: GovernedKnowledgeArticle,
    query: KnowledgeQuery,
) -> bool:
    if article.application != query.application:
        return False
    if not _matches_service_indicator(article, query):
        return False
    if query.fault_type is None:
        return True
    if query.fault_type in article.fault_types:
        return True

    # Conflicting evidence must still surface when app/service/indicator match.
    # Otherwise the governed KB would hide a contradiction before human review.
    return article.quality == KnowledgeQuality.CONFLICTING


def _matches_service_indicator(
    article: GovernedKnowledgeArticle,
    query: KnowledgeQuery,
) -> bool:
    return article.service == query.service and query.indicator in article.indicators


def _article_to_evidence(
    article: GovernedKnowledgeArticle,
    query: KnowledgeQuery,
) -> GovernedKnowledgeEvidence:
    return GovernedKnowledgeEvidence(
        evidence_id=f"knowledge-evidence::{article.article_id}",
        article_id=article.article_id,
        title=article.title,
        quality=article.quality,
        safety=article.safety,
        service=query.service,
        indicator=query.indicator,
        summary=article.summary,
        recommended_actions=article.recommended_actions,
        evidence_weight=_weight_for_quality(article.quality),
        usable_for_reasoning=article.quality != KnowledgeQuality.WRONG_APPLICATION,
        benchmark_truth_eligible=False,
        can_score_benchmark=False,
        human_approval_required=True,
        autonomous_action_allowed=False,
        provenance=f"{article.provenance}:governed_evidence",
    )


def _missing_evidence(query: KnowledgeQuery) -> GovernedKnowledgeEvidence:
    return GovernedKnowledgeEvidence(
        evidence_id=f"knowledge-gap::{query.service}::{query.indicator}",
        article_id=None,
        title="Missing governed knowledge",
        quality=KnowledgeQuality.MISSING,
        safety=KnowledgeSafety.MISSING_KNOWLEDGE,
        service=query.service,
        indicator=query.indicator,
        summary=(
            "No governed knowledge article matched this service, indicator, "
            "application, and fault context."
        ),
        recommended_actions=(
            "Record knowledge gap for review.",
            "Do not infer benchmark truth from missing knowledge.",
        ),
        evidence_weight=0.0,
        usable_for_reasoning=False,
        benchmark_truth_eligible=False,
        can_score_benchmark=False,
        human_approval_required=True,
        autonomous_action_allowed=False,
        provenance="synthetic_kb:missing_knowledge_gap",
    )


def _weight_for_quality(quality: KnowledgeQuality) -> float:
    if quality == KnowledgeQuality.EXACT:
        return 0.86
    if quality == KnowledgeQuality.HUMAN_APPROVAL_REQUIRED:
        return 0.72
    if quality == KnowledgeQuality.RISKY_REMEDIATION:
        return 0.48
    if quality == KnowledgeQuality.PARTIAL:
        return 0.45
    if quality == KnowledgeQuality.CONFLICTING:
        return 0.31
    if quality == KnowledgeQuality.STALE:
        return 0.24
    return 0.0
