import json

from src.domain_adapters.it_application_health.application_health_concept_demo import (
    ApplicationHealthConceptDemo,
)


def main() -> None:
    result = ApplicationHealthConceptDemo().run("GS-001")

    summary = {
        "demo": "EAIOS 2 Application Health Concept Demo",
        "business_outcome": result["business_outcome"],
        "scenario_id": result["scenario_id"],
        "case_summary": result["case_context"]["case_summary"],
        "fusion_confidence": result["evidence_fusion"]["fusion_confidence"],
        "reasoning_summary": result["reasoning_explanation"]["reasoning_summary"],
        "recommendation_summary": result["recommendation_candidate"]["summary"],
        "requires_human_approval": result["safety_summary"]["requires_human_approval"],
        "autonomous_action_allowed": result["safety_summary"]["autonomous_action_allowed"],
    }

    if "operational_confidence" in result:
        summary["operational_confidence"] = result["operational_confidence"][
            "operational_confidence"
        ]
        summary["selected_due_diligence_level"] = result["operational_confidence"][
            "selected_due_diligence_level"
        ]
        summary["knowledge_retrieval_required"] = result["operational_confidence"][
            "knowledge_retrieval_required"
        ]

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
