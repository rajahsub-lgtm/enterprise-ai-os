from src.domain_adapters.it_application_health.application_health_concept_demo import (
    ApplicationHealthConceptDemo,
)


def test_real_eaios_app_health_demo_smoke_path():
    result = ApplicationHealthConceptDemo().run("GS-001")

    assert result["business_outcome"] == "Maintain Application Health"
    assert result["case_context"]
    assert result["evidence_fusion"]
    assert result["reasoning_explanation"]
    assert result["recommendation_candidate"]
    assert result["human_review_package"]

    assert result["recommendation_candidate"]["requires_human_approval"] is True
    assert result["recommendation_candidate"]["autonomous_action_allowed"] is False
    assert result["human_review_package"]["requires_human_approval"] is True
    assert result["human_review_package"]["autonomous_action_allowed"] is False
    assert result["safety_summary"]["autonomous_action_allowed"] is False
