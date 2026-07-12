from pathlib import Path


DOC = Path("docs/EAIOS_2_SPRINT_7_CLOSEOUT.md")

REQUIRED_FILES = [
    Path("src/eaios/sprint7/container_packaging_contract.py"),
    Path("src/eaios/sprint7/local_web_review_surface.py"),
    Path("src/eaios/sprint7/cloud_deploy_preflight.py"),
    Path("src/eaios/sprint7/provider_exchange_schema.py"),
    Path("src/eaios/sprint7/provider_output_validator.py"),
    Path("src/eaios/sprint7/mcp_connector_inventory_schema.py"),
    Path("src/eaios/sprint7/mcp_connector_permission_classifier.py"),
    Path("src/eaios/sprint7/audit_event_envelope.py"),
    Path("src/eaios/sprint7/human_approval_workflow.py"),
    Path("src/eaios/sprint7/demo_release_checklist.py"),
]


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_sprint7_closeout_file_exists():
    assert DOC.exists()


def test_sprint7_closeout_required_files_exist():
    assert [str(path) for path in REQUIRED_FILES if not path.exists()] == []


def test_sprint7_closeout_declares_sprint_closed():
    text = _text()

    assert "Sprint 7 ? Controlled Runtime Hardening" in text
    assert "CLOSED" in text
    assert "controlled runtime hardening" in text


def test_sprint7_closeout_lists_completed_slices():
    text = _text()

    for expected in [
        "7-1 container packaging contract",
        "7-2 local web review surface model",
        "7-3 cloud deploy preflight model",
        "7-4 provider request and response schema",
        "7-5 provider output validator",
        "7-6 MCP connector inventory schema",
        "7-7 MCP connector permission classifier",
        "7-8 audit event envelope",
        "7-9 human approval workflow model",
        "7-10 demo release checklist",
        "7-11 Sprint 7 closeout",
    ]:
        assert expected in text


def test_sprint7_closeout_lists_primary_module_artifacts():
    text = _text()

    for expected in [
        "src/eaios/sprint7/container_packaging_contract.py",
        "src/eaios/sprint7/local_web_review_surface.py",
        "src/eaios/sprint7/cloud_deploy_preflight.py",
        "src/eaios/sprint7/provider_exchange_schema.py",
        "src/eaios/sprint7/provider_output_validator.py",
        "src/eaios/sprint7/mcp_connector_inventory_schema.py",
        "src/eaios/sprint7/mcp_connector_permission_classifier.py",
        "src/eaios/sprint7/audit_event_envelope.py",
        "src/eaios/sprint7/human_approval_workflow.py",
        "src/eaios/sprint7/demo_release_checklist.py",
    ]:
        assert expected in text



def test_sprint7_closeout_preserves_review_only_modes():
    text = _text()

    for expected in [
        "REVIEW_ONLY_CONTRACT",
        "SURFACE_MODEL_ONLY",
        "REVIEW_ONLY_PREFLIGHT",
        "REVIEW_ONLY_SCHEMA",
        "REVIEW_ONLY_VALIDATOR",
        "REVIEW_ONLY_INVENTORY_SCHEMA",
        "REVIEW_ONLY_CLASSIFIER",
        "REVIEW_ONLY_AUDIT_ENVELOPE",
        "REVIEW_ONLY_WORKFLOW",
        "REVIEW_ONLY_RELEASE_CHECKLIST",
    ]:
        assert expected in text


def test_sprint7_closeout_preserves_readiness_statuses():
    text = _text()

    for expected in [
        "BLOCKED_PENDING_REVIEWS",
        "BLOCKED_PENDING_VALIDATION",
        "BLOCKED_PENDING_RELEASE_APPROVAL",
        "BLOCKED_UNTIL_APPROVED",
        "PENDING_HUMAN_REVIEW",
        "REVIEW_READY_NOT_DEPLOYED",
    ]:
        assert expected in text


def test_sprint7_closeout_preserves_governance_boundaries():
    text = _text()

    for expected in [
        "human_review_required",
        "benchmark_truth_isolated",
        "provider_output_not_accepted_without_validation",
        "connector_calls_disabled",
        "write_operations_blocked",
        "audit_events_not_persisted",
        "approval_records_not_persisted",
        "release_not_created",
        "cloud_not_deployed",
        "container_not_built",
        "autonomous_remediation_disabled",
    ]:
        assert expected in text


def test_sprint7_closeout_preserves_blocked_actions():
    text = _text()

    for expected in [
        "build_container_image",
        "run_container",
        "push_container_image",
        "create_cloud_resources",
        "deploy_to_cloud",
        "enable_real_provider",
        "call_real_provider",
        "enable_real_connector",
        "call_real_connector",
        "execute_tool_action",
        "perform_external_write",
        "modify_production_record",
        "change_infrastructure",
        "load_secret_material",
        "access_external_network",
        "persist_audit_events_to_external_store",
        "persist_approval_record_to_external_store",
        "approve_without_human",
        "reject_without_human",
        "execute_approved_action",
        "execute_remediation",
        "send_notification",
        "score_benchmark_from_release",
        "update_benchmark_truth_from_release",
        "enable_autonomous_remediation",
        "bypass_human_review",
    ]:
        assert expected in text


def test_sprint7_closeout_documents_release_position_and_non_claims():
    text = _text()

    assert "release-ready for review, but not executable as a production release" in text
    assert "The demo release checklist remains BLOCKED_PENDING_RELEASE_APPROVAL." in text
    assert "Sprint 7 does not claim production deployment." in text
    assert "Sprint 7 does not claim real provider execution." in text
    assert "Sprint 7 does not claim real MCP connector execution." in text
    assert "Sprint 7 does not claim autonomous remediation." in text


def test_sprint7_closeout_documents_sprint8_direction():
    text = _text()

    for expected in [
        "Sprint 8 can move into operator-facing release polish",
        "operator demo command",
        "read-only local HTML export",
        "release notes generator",
        "portfolio walkthrough script",
        "interview demo script",
        "provider validator examples",
        "connector inventory examples",
        "approval workflow examples",
        "audit trace examples",
    ]:
        assert expected in text


def test_sprint7_closeout_has_no_secret_or_shell_execution_snippets():
    text = _text().lower()

    assert "api_key" not in text
    assert "password" not in text
    assert "bearer " not in text
    assert "curl " not in text
    assert "requests.post" not in text
    assert "httpx.post" not in text
