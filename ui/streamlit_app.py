"""
EAIOS 2 Sprint 3-UI Streamlit entrypoint.

Canonical UI entrypoint:

    streamlit run ui/streamlit_app.py

This app renders the governed orchestration replay view-model. It does not make
governance, confidence, evidence, approval, or remediation decisions.
"""

from __future__ import annotations

from ui.components.confidence_panel import confidence_panel_model
from ui.components.control_header import control_header_model
from ui.components.evidence_workbench import evidence_workbench_model
from ui.components.governance_trace_panel import governance_passport_rows
from ui.components.human_review_panel import human_review_boundary_model
from ui.components.story_replay_panel import replay_story_cards, story_thesis_model
from ui.components.reasoning_board import reasoning_board_model, recommendation_review_model
from ui.components.replay_canvas import replay_canvas_model
from ui.components.scenario_selector import scenario_selector_options
from ui.components.side_by_side_replay import side_by_side_columns
from ui.demo_fixtures import build_demo_comparison_view_model


def main() -> None:
    import streamlit as st

    comparison = build_demo_comparison_view_model()
    header = control_header_model()

    st.set_page_config(
        page_title="EAIOS 2 Control Room",
        layout="wide",
    )

    st.title("EAIOS 2 Control Room")
    st.caption("Governed adaptive orchestration replay")

    header_columns = st.columns(5)
    header_columns[0].metric("Business outcome", header["business_outcome"])
    header_columns[1].metric("Governance", header["governance"])
    header_columns[2].metric("Human approval", header["human_approval"])
    header_columns[3].metric("Autonomous action", header["autonomous_action"])
    header_columns[4].metric("Memory", header["memory"])

    st.markdown("---")

    thesis = story_thesis_model(comparison)
    st.subheader(thesis["title"])
    st.caption(thesis["same_alert"])
    st.info(thesis["thesis"])

    options = scenario_selector_options(comparison)
    selected_label = st.selectbox(
        "Replay scenario",
        [option["label"] for option in options],
    )

    selected_run = next(
        run
        for run in comparison["runs"]
        if run["scenario_label"] == selected_label
    )

    st.markdown("### Side-by-side replay")
    st.caption("The columns replay the same alert under different memory and confidence states.")

    columns = st.columns(len(comparison["summary"]))

    for column, card in zip(columns, replay_story_cards(comparison)):
        with column:
            st.markdown(f"#### {card['story_role']}")
            st.markdown(f"**{card['scenario_label']}**")
            st.metric("Confidence", card["confidence"])
            st.metric("Due diligence", card["due_diligence"])
            st.metric("Governed agent steps", card["agent_step_count"])
            st.caption(card["behavior_headline"])
            st.write(
                {
                    "evidence": card["evidence_count"],
                    "excluded": card["excluded_evidence_count"],
                    "gaps": card["evidence_gap_count"],
                    "denied": card["denied_source_access_count"],
                }
            )
            st.success(card["boundary_statement"])

            with st.expander("Why this depth?"):
                for reason in card["why"]:
                    st.write(f"- {reason}")

    st.markdown("---")

    left, right = st.columns([2, 1])

    with left:
        st.markdown("### Orchestration replay canvas")
        canvas = replay_canvas_model(selected_run)
        st.graphviz_chart(canvas["dot"], use_container_width=True)

        st.markdown("### Evidence workbench")
        workbench = evidence_workbench_model(selected_run)

        summary_cols = st.columns(3)
        summary_cols[0].metric(
            "Reasoning eligible",
            workbench["summary"]["reasoning_eligible_count"],
        )
        summary_cols[1].metric(
            "Excluded",
            workbench["summary"]["excluded_count"],
        )
        summary_cols[2].metric(
            "Evidence gaps",
            workbench["summary"]["gap_count"],
        )

        st.caption(workbench["story"])

        evidence_tabs = st.tabs(
            [
                "Reasoning eligible",
                "Excluded",
                "Evidence gaps",
                "Evidence semantics",
            ]
        )

        with evidence_tabs[0]:
            st.dataframe(
                workbench["reasoning_eligible"],
                use_container_width=True,
            )

        with evidence_tabs[1]:
            st.dataframe(
                workbench["excluded"],
                use_container_width=True,
            )

        with evidence_tabs[2]:
            st.dataframe(
                workbench["gaps"],
                use_container_width=True,
            )

        with evidence_tabs[3]:
            st.write(workbench["evidence_class_semantics"])

        st.markdown("### Governance passport")
        st.dataframe(governance_passport_rows(selected_run), use_container_width=True)

        st.markdown("### Animation events")
        st.dataframe(selected_run["animation_events"], use_container_width=True)

    with right:
        st.markdown("### Confidence and due diligence")
        st.write(confidence_panel_model(selected_run))

        st.markdown("### Reasoning detective board")
        reasoning = reasoning_board_model(selected_run)
        st.caption(reasoning["story"])
        st.write(
            {
                "situation": reasoning["situation"],
                "selected_hypothesis": reasoning["selected_hypothesis"],
            }
        )

        with st.expander("Is / Is not"):
            st.markdown("**Is**")
            for item in reasoning["is"]:
                st.write(f"- {item}")

            st.markdown("**Is not**")
            for item in reasoning["is_not"]:
                st.write(f"- {item}")

        with st.expander("Hypotheses and why-chain"):
            st.markdown("**Candidate hypotheses**")
            for item in reasoning["candidate_hypotheses"]:
                st.write(f"- {item}")

            st.markdown("**Why-chain**")
            for item in reasoning["why_chain"]:
                st.write(f"- {item}")

            st.markdown("**Limits**")
            for item in reasoning["limits"]:
                st.write(f"- {item}")

        st.markdown("### Recommendation review")
        recommendation = recommendation_review_model(selected_run)
        st.caption(recommendation["story"])
        st.write(recommendation)

        st.markdown("### Human review boundary")
        st.write(human_review_boundary_model(selected_run))


if __name__ == "__main__":
    main()
