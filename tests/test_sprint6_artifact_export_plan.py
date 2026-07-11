from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint6.artifact_export_plan import (
    ExportArtifactState,
    ExportPlanMode,
    build_artifact_export_plan,
    render_artifact_export_plan_text,
    summarize_artifact_export_plan,
    to_view_model,
)


def _plan():
    return build_artifact_export_plan()


def test_artifact_export_plan_builds_from_manifest():
    plan = _plan()

    assert plan.export_plan_id == "sprint6-artifact-export-plan-001"
    assert plan.mode == ExportPlanMode.DRY_RUN_ONLY
    assert plan.source_manifest_id == "sprint6-demo-package-manifest-001"
    assert plan.export_root == "artifacts/eaios-demo"
    assert plan.provenance == "artifact_export_plan:dry_run"


def test_artifact_export_plan_lists_planned_artifacts():
    plan = _plan()

    assert len(plan.artifact_plans) == 6

    for artifact in plan.artifact_plans:
        assert artifact.export_path.startswith("artifacts/eaios-demo/")
        assert artifact.state == ExportArtifactState.PLANNED_NOT_WRITTEN
        assert artifact.required is True
        assert artifact.copied is False
        assert artifact.provenance == "artifact_export_plan:artifact_plan"


def test_artifact_export_plan_sections_are_derived_from_paths():
    plan = _plan()

    sections_by_path = {item.source_path: item.section for item in plan.artifact_plans}

    assert sections_by_path["docs/EAIOS_2_SPRINT_5_DEMO_NARRATIVE.md"] == "docs"
    assert sections_by_path["docs/EAIOS_2_SPRINT_5_CLOSEOUT.md"] == "docs"
    assert sections_by_path["src/eaios/sprint5/scenario_command.py"] == "source_contracts"
    assert sections_by_path["tests/test_sprint5_closeout.py"] == "test_contracts"


def test_artifact_export_plan_planned_sections_are_stable():
    plan = _plan()

    assert plan.planned_sections == (
        "docs",
        "source_contracts",
        "test_contracts",
        "rendered_views",
        "governance_summary",
    )


def test_artifact_export_plan_blocked_actions_are_explicit():
    plan = _plan()

    assert plan.blocked_actions == (
        "create_export_folder",
        "copy_artifact_files",
        "create_archive",
        "run_shell_export_command",
        "write_external_files",
        "create_cloud_resources",
        "load_secret_material",
        "call_real_provider",
        "call_real_connector",
        "execute_remediation",
        "send_notification",
        "score_benchmark_from_export",
        "enable_autonomous_remediation",
    )


def test_artifact_export_plan_embeds_manifest_summary():
    plan = _plan()

    assert plan.manifest_summary["manifest_id"] == "sprint6-demo-package-manifest-001"
    assert plan.manifest_summary["package_files_written"] is False
    assert plan.manifest_summary["human_review_required"] is True


def test_artifact_export_plan_preserves_no_export_execution_boundaries():
    plan = _plan()

    assert plan.export_folder_created is False
    assert plan.files_copied is False
    assert plan.archive_created is False
    assert plan.shell_commands_executed is False
    assert plan.external_files_written is False
    assert plan.cloud_resources_created is False
    assert plan.secrets_loaded is False
    assert plan.provider_calls_performed is False
    assert plan.real_connectors_called is False
    assert plan.remediation_performed is False
    assert plan.notifications_sent is False
    assert plan.benchmark_scoring_performed is False
    assert plan.autonomous_remediation_allowed is False
    assert plan.human_review_required is True


def test_artifact_export_plan_summary_is_view_ready():
    plan = _plan()

    assert summarize_artifact_export_plan(plan) == {
        "export_plan_id": "sprint6-artifact-export-plan-001",
        "mode": "DRY_RUN_ONLY",
        "source_manifest_id": "sprint6-demo-package-manifest-001",
        "export_root": "artifacts/eaios-demo",
        "artifact_plan_count": 6,
        "planned_section_count": 5,
        "blocked_action_count": 13,
        "export_folder_created": False,
        "files_copied": False,
        "archive_created": False,
        "shell_commands_executed": False,
        "external_files_written": False,
        "cloud_resources_created": False,
        "secrets_loaded": False,
        "provider_calls_performed": False,
        "real_connectors_called": False,
        "remediation_performed": False,
        "notifications_sent": False,
        "benchmark_scoring_performed": False,
        "autonomous_remediation_allowed": False,
        "human_review_required": True,
    }


def test_artifact_export_plan_view_model_is_json_serializable():
    plan = _plan()

    serialized = json.dumps(to_view_model(plan), indent=2)

    assert "sprint6-artifact-export-plan-001" in serialized
    assert "artifacts/eaios-demo" in serialized
    assert "score_benchmark_from_export" in serialized


def test_artifact_export_plan_text_renderer_is_readable():
    text = render_artifact_export_plan_text(_plan())

    assert "# EAIOS Dry-Run Artifact Export Plan" in text
    assert "Mode: DRY_RUN_ONLY" in text
    assert "## Planned Artifacts" in text
    assert "PLANNED_NOT_WRITTEN" in text
    assert "Files copied: false" in text
    assert "Human review required: true" in text


def test_artifact_export_plan_module_does_not_write_or_call_external_systems():
    source = Path("src/eaios/sprint6/artifact_export_plan.py").read_text(
        encoding="utf-8"
    )

    assert "subprocess" not in source
    assert "os.system" not in source
    assert "shutil" not in source
    assert "write_text(" not in source
    assert "mkdir(" not in source
    assert "import requests" not in source.lower()
    assert "import httpx" not in source.lower()
    assert "google.cloud" not in source.lower()
    assert "openai" not in source.lower()
    assert "anthropic" not in source.lower()
    assert "execute_tool(" not in source
    assert "restart_service(" not in source
    assert "score_benchmark_result(" not in source
