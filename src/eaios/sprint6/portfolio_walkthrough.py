"""Sprint 6 portfolio walkthrough contract.

This module defines a read-only portfolio walkthrough script for explaining
EAIOS in interviews, architecture reviews, and operator demos.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint6.static_review_page import (
    build_static_review_page_model,
    summarize_static_review_page_model,
)


class PortfolioWalkthroughMode(str, Enum):
    READ_ONLY_SCRIPT = "READ_ONLY_SCRIPT"


class PortfolioWalkthroughAudience(str, Enum):
    HIRING_MANAGER = "HIRING_MANAGER"
    ARCHITECTURE_REVIEWER = "ARCHITECTURE_REVIEWER"
    OPERATOR_REVIEWER = "OPERATOR_REVIEWER"


@dataclass(frozen=True)
class PortfolioWalkthroughStep:
    step_id: str
    order: int
    title: str
    talk_track: str
    evidence_refs: tuple[str, ...]
    safety_message: str
    duration_minutes: int
    provenance: str


@dataclass(frozen=True)
class PortfolioWalkthrough:
    walkthrough_id: str
    mode: PortfolioWalkthroughMode
    audience: PortfolioWalkthroughAudience
    title: str
    source_static_review_page_id: str
    steps: tuple[PortfolioWalkthroughStep, ...]
    transition_prompts: tuple[str, ...]
    blocked_actions: tuple[str, ...]
    static_review_summary: dict[str, object]
    rendered_markdown: str
    files_written: bool
    shell_commands_executed: bool
    cloud_resources_created: bool
    secrets_loaded: bool
    provider_calls_performed: bool
    real_connectors_called: bool
    remediation_performed: bool
    notifications_sent: bool
    benchmark_scoring_performed: bool
    autonomous_remediation_allowed: bool
    human_review_required: bool
    provenance: str


def build_portfolio_walkthrough(
    audience: PortfolioWalkthroughAudience = PortfolioWalkthroughAudience.ARCHITECTURE_REVIEWER,
) -> PortfolioWalkthrough:
    static_page = build_static_review_page_model()
    static_summary = summarize_static_review_page_model(static_page)

    steps = (
        PortfolioWalkthroughStep(
            step_id="walkthrough-step-001-north-star",
            order=1,
            title="North Star",
            talk_track=(
                "EAIOS is an enterprise AI operating model for governing, "
                "observing, and improving AI-enabled operations."
            ),
            evidence_refs=("docs/EAIOS_2_SPRINT_5_DEMO_NARRATIVE.md",),
            safety_message="This is a read-only explanation, not an execution step.",
            duration_minutes=2,
            provenance="portfolio_walkthrough:step",
        ),
        PortfolioWalkthroughStep(
            step_id="walkthrough-step-002-scenario",
            order=2,
            title="Application-Health Scenario",
            talk_track=(
                "The demo starts with benchmark-grounded application-health "
                "evidence and keeps benchmark truth outside demo output."
            ),
            evidence_refs=("src/eaios/sprint5/scenario_command.py",),
            safety_message="Benchmark scoring is not performed by the walkthrough.",
            duration_minutes=3,
            provenance="portfolio_walkthrough:step",
        ),
        PortfolioWalkthroughStep(
            step_id="walkthrough-step-003-operator-experience",
            order=3,
            title="Operator Experience",
            talk_track=(
                "The operator sees context, evidence, disabled controls, blocked "
                "actions, and human review requirements."
            ),
            evidence_refs=("src/eaios/sprint5/operator_review_screen.py",),
            safety_message="Decision controls remain disabled in the demo.",
            duration_minutes=4,
            provenance="portfolio_walkthrough:step",
        ),
        PortfolioWalkthroughStep(
            step_id="walkthrough-step-004-cloud-readiness",
            order=4,
            title="Cloud Readiness",
            talk_track=(
                "The GCP readiness checklist shows review gates without creating "
                "cloud resources or loading secrets."
            ),
            evidence_refs=("src/eaios/sprint5/gcp_readiness_checklist.py",),
            safety_message="Cloud deployment remains blocked pending approval.",
            duration_minutes=3,
            provenance="portfolio_walkthrough:step",
        ),
        PortfolioWalkthroughStep(
            step_id="walkthrough-step-005-provider-connector-seams",
            order=5,
            title="Provider and Connector Seams",
            talk_track=(
                "Provider and MCP connector seams are visible before real provider "
                "calls or real connectors are enabled."
            ),
            evidence_refs=(
                "src/eaios/sprint5/provider_plugin_seam.py",
                "src/eaios/sprint5/mcp_connector_harness.py",
            ),
            safety_message="Real providers and connectors are disabled by default.",
            duration_minutes=4,
            provenance="portfolio_walkthrough:step",
        ),
        PortfolioWalkthroughStep(
            step_id="walkthrough-step-006-package-plan",
            order=6,
            title="Portfolio Package Plan",
            talk_track=(
                "Sprint 6 describes a local package manifest, CLI contract, dry-run "
                "export plan, quickstart, and static review page."
            ),
            evidence_refs=(
                "src/eaios/sprint6/demo_package.py",
                "src/eaios/sprint6/artifact_export_plan.py",
                "docs/EAIOS_2_SPRINT_6_QUICKSTART.md",
            ),
            safety_message="The package plan does not write files or create archives.",
            duration_minutes=3,
            provenance="portfolio_walkthrough:step",
        ),
        PortfolioWalkthroughStep(
            step_id="walkthrough-step-007-governance-boundaries",
            order=7,
            title="Governance Boundaries",
            talk_track=(
                "The core value is that EAIOS makes safety boundaries explicit, "
                "reviewable, and test-backed."
            ),
            evidence_refs=("tests/test_sprint6_static_review_page.py",),
            safety_message="Unsafe actions remain blocked and auditable.",
            duration_minutes=3,
            provenance="portfolio_walkthrough:step",
        ),
        PortfolioWalkthroughStep(
            step_id="walkthrough-step-008-close",
            order=8,
            title="Close",
            talk_track=(
                "The demo is ready to discuss as a portfolio artifact: it shows "
                "enterprise AI governance, operator experience, and cloud readiness "
                "without unsafe execution."
            ),
            evidence_refs=("docs/EAIOS_2_SPRINT_5_CLOSEOUT.md",),
            safety_message="Human review remains required.",
            duration_minutes=2,
            provenance="portfolio_walkthrough:step",
        ),
    )

    blocked_actions = (
        "write_walkthrough_file",
        "run_shell_command",
        "create_export_folder",
        "copy_artifact_files",
        "create_cloud_resources",
        "load_secret_material",
        "call_real_provider",
        "call_real_connector",
        "execute_remediation",
        "send_notification",
        "score_benchmark_from_walkthrough",
        "enable_autonomous_remediation",
    )

    rendered_markdown = render_portfolio_walkthrough_markdown(
        title="EAIOS Portfolio Walkthrough",
        audience=audience,
        steps=steps,
        blocked_actions=blocked_actions,
    )

    return PortfolioWalkthrough(
        walkthrough_id="sprint6-portfolio-walkthrough-001",
        mode=PortfolioWalkthroughMode.READ_ONLY_SCRIPT,
        audience=audience,
        title="EAIOS Portfolio Walkthrough",
        source_static_review_page_id=str(static_summary["page_id"]),
        steps=steps,
        transition_prompts=(
            "Now let me show how the operator sees this.",
            "Now let me show where cloud readiness is gated.",
            "Now let me show how provider and connector seams stay disabled.",
            "Now let me close with the governance value.",
        ),
        blocked_actions=blocked_actions,
        static_review_summary=static_summary,
        rendered_markdown=rendered_markdown,
        files_written=False,
        shell_commands_executed=False,
        cloud_resources_created=False,
        secrets_loaded=False,
        provider_calls_performed=False,
        real_connectors_called=False,
        remediation_performed=False,
        notifications_sent=False,
        benchmark_scoring_performed=False,
        autonomous_remediation_allowed=False,
        human_review_required=True,
        provenance="portfolio_walkthrough:script",
    )


def summarize_portfolio_walkthrough(
    walkthrough: PortfolioWalkthrough,
) -> dict[str, object]:
    return {
        "walkthrough_id": walkthrough.walkthrough_id,
        "mode": walkthrough.mode.value,
        "audience": walkthrough.audience.value,
        "title": walkthrough.title,
        "source_static_review_page_id": walkthrough.source_static_review_page_id,
        "step_count": len(walkthrough.steps),
        "total_duration_minutes": sum(step.duration_minutes for step in walkthrough.steps),
        "transition_prompt_count": len(walkthrough.transition_prompts),
        "blocked_action_count": len(walkthrough.blocked_actions),
        "files_written": walkthrough.files_written,
        "shell_commands_executed": walkthrough.shell_commands_executed,
        "cloud_resources_created": walkthrough.cloud_resources_created,
        "secrets_loaded": walkthrough.secrets_loaded,
        "provider_calls_performed": walkthrough.provider_calls_performed,
        "real_connectors_called": walkthrough.real_connectors_called,
        "remediation_performed": walkthrough.remediation_performed,
        "notifications_sent": walkthrough.notifications_sent,
        "benchmark_scoring_performed": walkthrough.benchmark_scoring_performed,
        "autonomous_remediation_allowed": walkthrough.autonomous_remediation_allowed,
        "human_review_required": walkthrough.human_review_required,
    }


def to_view_model(walkthrough: PortfolioWalkthrough) -> dict[str, Any]:
    return {
        "summary": summarize_portfolio_walkthrough(walkthrough),
        "steps": [
            {
                "step_id": step.step_id,
                "order": step.order,
                "title": step.title,
                "talk_track": step.talk_track,
                "evidence_refs": list(step.evidence_refs),
                "safety_message": step.safety_message,
                "duration_minutes": step.duration_minutes,
                "provenance": step.provenance,
            }
            for step in walkthrough.steps
        ],
        "transition_prompts": list(walkthrough.transition_prompts),
        "blocked_actions": list(walkthrough.blocked_actions),
        "static_review_summary": walkthrough.static_review_summary,
        "rendered_markdown": walkthrough.rendered_markdown,
        "provenance": walkthrough.provenance,
    }


def render_portfolio_walkthrough_markdown(
    title: str,
    audience: PortfolioWalkthroughAudience,
    steps: tuple[PortfolioWalkthroughStep, ...],
    blocked_actions: tuple[str, ...],
) -> str:
    step_lines = "\n\n".join(
        (
            f"## {step.order}. {step.title}\n"
            f"{step.talk_track}\n\n"
            f"Safety: {step.safety_message}\n\n"
            f"Evidence: {', '.join(step.evidence_refs)}"
        )
        for step in steps
    )
    blocked_lines = "\n".join(f"- {item}" for item in blocked_actions)

    return (
        f"# {title}\n\n"
        f"Audience: {audience.value}\n\n"
        f"{step_lines}\n\n"
        "## Blocked Actions\n"
        f"{blocked_lines}\n\n"
        "Human review required: true\n"
    )
