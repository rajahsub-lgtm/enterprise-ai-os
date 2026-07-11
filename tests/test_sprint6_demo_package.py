from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint6.demo_package import (
    DemoPackageArtifactType,
    DemoPackageMode,
    build_demo_package_manifest,
    render_demo_package_manifest_text,
    summarize_demo_package_manifest,
    to_view_model,
)


def _manifest():
    return build_demo_package_manifest()


def test_demo_package_manifest_builds_from_gcp_readiness():
    manifest = _manifest()

    assert manifest.manifest_id == "sprint6-demo-package-manifest-001"
    assert manifest.mode == DemoPackageMode.LOCAL_MANIFEST_ONLY
    assert manifest.source_readiness_checklist_id == "sprint5-gcp-readiness-checklist-001"
    assert manifest.provenance == "demo_package:manifest"


def test_demo_package_manifest_lists_required_artifacts():
    manifest = _manifest()

    assert len(manifest.artifacts) == 6
    assert all(item.required for item in manifest.artifacts)
    assert all(item.read_only for item in manifest.artifacts)

    paths = tuple(item.path for item in manifest.artifacts)
    assert "docs/EAIOS_2_SPRINT_5_DEMO_NARRATIVE.md" in paths
    assert "docs/EAIOS_2_SPRINT_5_CLOSEOUT.md" in paths
    assert "src/eaios/sprint5/scenario_command.py" in paths
    assert "src/eaios/sprint5/operator_review_screen.py" in paths
    assert "src/eaios/sprint5/gcp_readiness_checklist.py" in paths
    assert "tests/test_sprint5_closeout.py" in paths


def test_demo_package_manifest_artifact_types_are_explicit():
    manifest = _manifest()

    types = tuple(item.artifact_type for item in manifest.artifacts)
    assert types == (
        DemoPackageArtifactType.DOCUMENT,
        DemoPackageArtifactType.DOCUMENT,
        DemoPackageArtifactType.SOURCE_CONTRACT,
        DemoPackageArtifactType.SOURCE_CONTRACT,
        DemoPackageArtifactType.SOURCE_CONTRACT,
        DemoPackageArtifactType.TEST_CONTRACT,
    )


def test_demo_package_manifest_sections_and_blocked_actions_are_stable():
    manifest = _manifest()

    assert manifest.package_sections == (
        "demo_story",
        "operator_experience",
        "governance_boundaries",
        "cloud_readiness",
        "test_evidence",
        "next_steps",
    )

    assert "write_package_artifacts" in manifest.blocked_actions
    assert "create_cloud_resources" in manifest.blocked_actions
    assert "call_real_provider" in manifest.blocked_actions
    assert "call_real_connector" in manifest.blocked_actions
    assert "score_benchmark_from_package" in manifest.blocked_actions


def test_demo_package_manifest_preserves_no_execution_boundaries():
    manifest = _manifest()

    assert manifest.package_files_written is False
    assert manifest.external_files_written is False
    assert manifest.shell_commands_executed is False
    assert manifest.cloud_resources_created is False
    assert manifest.secrets_loaded is False
    assert manifest.provider_calls_performed is False
    assert manifest.real_connectors_called is False
    assert manifest.remediation_performed is False
    assert manifest.notifications_sent is False
    assert manifest.benchmark_scoring_performed is False
    assert manifest.autonomous_remediation_allowed is False
    assert manifest.human_review_required is True


def test_demo_package_manifest_summary_is_view_ready():
    manifest = _manifest()

    assert summarize_demo_package_manifest(manifest) == {
        "manifest_id": "sprint6-demo-package-manifest-001",
        "mode": "LOCAL_MANIFEST_ONLY",
        "title": "EAIOS Portfolio Demo Package Manifest",
        "source_readiness_checklist_id": "sprint5-gcp-readiness-checklist-001",
        "artifact_count": 6,
        "required_artifact_count": 6,
        "package_section_count": 6,
        "blocked_action_count": 11,
        "package_files_written": False,
        "external_files_written": False,
        "shell_commands_executed": False,
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


def test_demo_package_manifest_view_model_is_json_serializable():
    manifest = _manifest()

    serialized = json.dumps(to_view_model(manifest), indent=2)

    assert "sprint6-demo-package-manifest-001" in serialized
    assert "docs/EAIOS_2_SPRINT_5_DEMO_NARRATIVE.md" in serialized
    assert "score_benchmark_from_package" in serialized


def test_demo_package_manifest_text_renderer_is_readable():
    text = render_demo_package_manifest_text(_manifest())

    assert "# EAIOS Portfolio Demo Package Manifest" in text
    assert "Manifest: sprint6-demo-package-manifest-001" in text
    assert "Mode: LOCAL_MANIFEST_ONLY" in text
    assert "## Artifacts" in text
    assert "## Blocked Actions" in text
    assert "Human review required: true" in text


def test_demo_package_module_does_not_write_package_or_call_external_systems():
    source = Path("src/eaios/sprint6/demo_package.py").read_text(encoding="utf-8")

    assert "subprocess" not in source
    assert "import requests" not in source.lower()
    assert "import httpx" not in source.lower()
    assert "google.cloud" not in source.lower()
    assert "openai" not in source.lower()
    assert "anthropic" not in source.lower()
    assert "execute_tool(" not in source
    assert "restart_service(" not in source
    assert "score_benchmark_result(" not in source
