from pathlib import Path


DOC = Path("docs/EAIOS_2_SPRINT_6_MCP_CONNECTOR_PERMISSION_MODEL.md")

REQUIRED_FILES = [
    Path("docs/EAIOS_2_SPRINT_6_PROVIDER_INTEGRATION_DESIGN.md"),
    Path("src/eaios/sprint5/mcp_connector_harness.py"),
    Path("src/eaios/sprint6/portfolio_walkthrough.py"),
]


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_mcp_connector_permission_model_file_exists():
    assert DOC.exists()


def test_mcp_connector_permission_model_required_inputs_exist():
    assert [str(path) for path in REQUIRED_FILES if not path.exists()] == []


def test_mcp_connector_permission_model_declares_review_only_state():
    text = _text()

    assert "REVIEW_ONLY_PERMISSION_MODEL" in text
    assert "not a connector implementation" in text
    assert "REAL_MCP_CONNECTORS_DISABLED_BY_DEFAULT" in text
    assert "DETERMINISTIC_CONNECTOR_FIXTURE_ONLY" in text


def test_mcp_connector_permission_model_blocks_real_connector_actions():
    text = _text()

    for expected in [
        "call_real_connector",
        "execute_tool_action",
        "perform_external_write",
        "modify_production_record",
        "change_infrastructure",
        "send_notification",
        "load_secret_material",
        "access_unapproved_network",
        "score_benchmark_from_connector_output",
        "update_benchmark_truth_from_connector_output",
        "enable_autonomous_remediation",
        "bypass_human_review",
    ]:
        assert expected in text


def test_mcp_connector_permission_model_documents_boundary_principles():
    text = _text()

    for expected in [
        "Connector output is evidence, not truth.",
        "Connector output is advisory, not executable.",
        "Connector output must not update benchmark truth.",
        "Connector output must not score benchmarks.",
        "Connector output must not execute remediation.",
        "Connector output must not bypass human review.",
        "Connector permissions must be explicit.",
        "Connector owners must be identified.",
        "Connector rollback must be available.",
    ]:
        assert expected in text


def test_mcp_connector_permission_model_documents_inventory_fields():
    text = _text()

    for expected in [
        "connector_id",
        "connector_name",
        "connector_type",
        "owning_service",
        "service_owner",
        "business_owner",
        "technical_owner",
        "data_domain",
        "data_classification",
        "allowed_operations",
        "disallowed_operations",
        "read_write_classification",
        "environment_scope",
        "approval_status",
        "risk_tier",
        "audit_required",
        "rollback_or_disable_switch",
        "human_review_required",
    ]:
        assert expected in text


def test_mcp_connector_permission_model_documents_permission_classes_and_operations():
    text = _text()

    for expected in [
        "READ_ONLY",
        "READ_WITH_FILTERED_DATA",
        "READ_WITH_SENSITIVE_DATA",
        "WRITE_NON_PRODUCTION",
        "WRITE_PRODUCTION_REQUIRES_APPROVAL",
        "WRITE_PRODUCTION_BLOCKED",
        "ADMIN_OPERATION_BLOCKED",
        "safe_read_operation",
        "sensitive_read_operation",
        "non_production_write_operation",
        "production_write_operation",
        "notification_operation",
        "remediation_operation",
        "identity_or_access_operation",
        "benchmark_scoring_operation",
        "benchmark_truth_update_operation",
    ]:
        assert expected in text


def test_mcp_connector_permission_model_documents_required_gates():
    text = _text()

    for expected in [
        "connector_inventory_review",
        "permission_model_review",
        "read_write_classification_review",
        "sandbox_boundary_review",
        "secret_handling_review",
        "network_access_review",
        "human_approval_review",
        "rollback_plan_review",
        "production_deployment_approval",
    ]:
        assert expected in text


def test_mcp_connector_permission_model_documents_read_and_write_rules():
    text = _text()

    for expected in [
        "Read-only connectors may retrieve approved evidence.",
        "Read-only connectors must not modify records.",
        "Read-only connectors must not send notifications.",
        "Read-only connectors must not execute remediation.",
        "Read-only connectors must not score benchmarks.",
        "Write-capable connectors remain disabled by default.",
        "explicit service owner approval",
        "blast radius analysis",
        "rollback plan",
    ]:
        assert expected in text


def test_mcp_connector_permission_model_documents_sandbox_secret_network_audit():
    text = _text()

    for expected in [
        "sandbox_environment",
        "allowed_test_records",
        "blocked_production_records",
        "mock_write_mode",
        "dry_run_mode",
        "audit_capture_mode",
        "request_id",
        "operation_requested",
        "permission_class",
        "approval_reference",
        "result_hash_or_reference",
        "security_owner",
        "approved_secret_store",
        "egress_review",
        "connector_endpoint_allowlist",
    ]:
        assert expected in text


def test_mcp_connector_permission_model_documents_benchmark_and_human_boundaries():
    text = _text()

    for expected in [
        "Benchmark truth remains external.",
        "define_benchmark_truth",
        "modify_benchmark_truth",
        "score_benchmark_results",
        "infer_benchmark_labels_from_connector_output",
        "replace_benchmark_verification_targets",
        "override_deterministic_scoring_logic",
        "Human review remains required",
        "write-capable connector requests",
        "production record changes",
        "identity or access operations",
        "benchmark truth update requests",
    ]:
        assert expected in text


def test_mcp_connector_permission_model_documents_enablement_phases_and_tests():
    text = _text()

    for expected in [
        "Phase 1: deterministic connector fixture only.",
        "Phase 2: connector inventory and permission model review.",
        "Phase 3: read-only sandbox simulation.",
        "Phase 4: read-only non-production connector after approval.",
        "Phase 5: write-capable dry-run connector after approval.",
        "Phase 6: human-approved production pilot after approval.",
        "connector_inventory_schema_tests",
        "permission_classification_tests",
        "read_only_boundary_tests",
        "write_operation_block_tests",
        "secret_loading_block_tests",
        "network_access_block_tests",
        "benchmark_truth_isolation_tests",
        "human_review_requirement_tests",
        "audit_trace_tests",
        "rollback_disable_switch_tests",
    ]:
        assert expected in text


def test_mcp_connector_permission_model_has_no_connector_code_or_secrets():
    text = _text().lower()

    assert "api_key" not in text
    assert "password" not in text
    assert "bearer " not in text
    assert "curl " not in text
    assert "requests.post" not in text
    assert "httpx.post" not in text
    assert "execute(" not in text
    assert "subprocess" not in text
