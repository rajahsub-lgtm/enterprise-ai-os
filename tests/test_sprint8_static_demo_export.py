from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint8.static_demo_export import (
    StaticDemoExportMode,
    StaticDemoExportStatus,
    build_static_demo_export,
    summarize_static_demo_export,
    to_view_model,
)


def _export():
    return build_static_demo_export()


def test_static_demo_export_builds_review_only_model():
    export = _export()

    assert export.export_id == "sprint8-static-demo-export-001"
    assert export.mode == StaticDemoExportMode.REVIEW_ONLY_STATIC_EXPORT
    assert export.status == StaticDemoExportStatus.RENDERED_IN_MEMORY
    assert export.title == "EAIOS Sprint 8 Static Demo Export"
    assert export.source_operator_command_id == "sprint8-operator-demo-command-001"
    assert export.provenance == "static_demo_export:model"


def test_static_demo_export_sections_are_declared():
    export = _export()

    assert len(export.sections) == 3

    assert tuple(section.section_id for section in export.sections) == (
        "static-export-section-001-overview",
        "static-export-section-002-command",
        "static-export-section-003-safety",
    )

    assert all(section.provenance == "static_demo_export:section" for section in export.sections)
    assert all(section.markdown for section in export.sections)
    assert all(section.html for section in export.sections)


def test_static_demo_export_contains_interview_demo_language():
    export = _export()

    assert "governed enterprise AI operating-system demo" in export.markdown_document
    assert "synthetic ITIL/AIOps data" in export.markdown_document
    assert "Release readiness: BLOCKED_PENDING_RELEASE_APPROVAL" in export.markdown_document
    assert "Release is review-ready but not executable as production." in export.markdown_document


def test_static_demo_export_renders_html_in_memory():
    export = _export()

    assert export.html_document.startswith("<!doctype html>")
    assert "<h1>EAIOS Sprint 8 Interview Demo Export</h1>" in export.html_document
    assert "<section><h2>Interview Demo Overview</h2>" in export.html_document
    assert "BLOCKED_PENDING_RELEASE_APPROVAL" in export.html_document



def test_static_demo_export_blocked_actions_are_explicit():
    export = _export()

    assert export.blocked_actions == (
        "write_static_export_file",
        "start_local_server",
        "publish_static_site",
        "create_release_archive",
        "build_container_image",
        "push_container_image",
        "deploy_to_cloud",
        "enable_real_provider",
        "enable_real_connector",
        "persist_approval_record_to_external_store",
        "send_notification",
        "execute_remediation",
        "score_benchmark_from_static_export",
        "update_benchmark_truth_from_static_export",
        "enable_autonomous_remediation",
        "bypass_human_review",
    )


def test_static_demo_export_preserves_no_side_effect_boundaries():
    export = _export()

    assert export.export_rendered is True
    assert export.files_written is False
    assert export.server_started is False
    assert export.static_site_published is False
    assert export.archive_created is False
    assert export.container_built is False
    assert export.cloud_deployed is False
    assert export.provider_enabled is False
    assert export.connector_enabled is False
    assert export.approval_records_persisted is False
    assert export.remediation_performed is False
    assert export.notifications_sent is False
    assert export.benchmark_scoring_performed is False
    assert export.benchmark_truth_updated is False
    assert export.autonomous_remediation_allowed is False
    assert export.human_review_required is True


def test_static_demo_export_embeds_operator_command_summary():
    export = _export()

    assert export.operator_command_summary["command_id"] == (
        "sprint8-operator-demo-command-001"
    )
    assert export.operator_command_summary["status"] == "COMPLETED_READ_ONLY"
    assert export.operator_command_summary["runtime_actions_executed"] is False
    assert export.operator_command_summary["human_review_required"] is True


def test_static_demo_export_summary_is_view_ready():
    export = _export()
    summary = summarize_static_demo_export(export)

    assert summary["export_id"] == "sprint8-static-demo-export-001"
    assert summary["mode"] == "REVIEW_ONLY_STATIC_EXPORT"
    assert summary["status"] == "RENDERED_IN_MEMORY"
    assert summary["source_operator_command_id"] == "sprint8-operator-demo-command-001"
    assert summary["section_count"] == 3
    assert summary["blocked_action_count"] == 16
    assert summary["files_written"] is False
    assert summary["server_started"] is False
    assert summary["cloud_deployed"] is False
    assert summary["human_review_required"] is True


def test_static_demo_export_view_model_is_json_serializable():
    export = _export()

    serialized = json.dumps(to_view_model(export), indent=2)

    assert "sprint8-static-demo-export-001" in serialized
    assert "REVIEW_ONLY_STATIC_EXPORT" in serialized
    assert "write_static_export_file" in serialized
    assert "BLOCKED_PENDING_RELEASE_APPROVAL" in serialized


def test_static_demo_export_module_does_not_write_or_call_external_systems():
    source = Path("src/eaios/sprint8/static_demo_export.py").read_text(
        encoding="utf-8"
    ).lower()

    assert "subprocess" not in source
    assert "os.system" not in source
    assert "requests.post" not in source
    assert "httpx.post" not in source
    assert "api_key" not in source
    assert "password" not in source
    assert "bearer " not in source
    assert "curl " not in source
    assert "write_text(" not in source
    assert "mkdir(" not in source
    assert "open(" not in source
    assert "execute_tool(" not in source
    assert "restart_service(" not in source
