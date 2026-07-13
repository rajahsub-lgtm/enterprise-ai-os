from pathlib import Path


DOC = Path("docs/EAIOS_2_SPRINT_10_STATIC_CLOUD_PREVIEW_APPROVAL_CHECKLIST.md")

REQUIRED_FILES = [
    Path("docs/EAIOS_2_SPRINT_10_STATIC_PREVIEW_SCOPE_CONTRACT.md"),
    Path("docs/EAIOS_2_SPRINT_10_STATIC_EXPORT_MATERIALIZATION_PLAN.md"),
    Path("docs/EAIOS_2_SPRINT_10_CLOUD_IAM_COST_BOUNDARY.md"),
    Path("docs/EAIOS_2_SPRINT_10_ROLLBACK_DISABLE_PLAN.md"),
    Path("docs/EAIOS_2_SPRINT_10_PROVIDER_CONNECTOR_DISABLED_STATE_VERIFICATION.md"),
]


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_static_cloud_preview_approval_checklist_file_exists():
    assert DOC.exists()


def test_static_cloud_preview_approval_required_prior_artifacts_exist():
    assert [str(path) for path in REQUIRED_FILES if not path.exists()] == []


def test_static_cloud_preview_approval_declares_purpose_and_non_actions():
    text = _text()

    assert "defines the approval checklist required" in text
    assert "It does not approve deployment." in text
    assert "It does not create cloud resources." in text
    assert "It does not materialize static files." in text
    assert "It does not start a runtime." in text
    assert "It does not enable providers." in text
    assert "It does not enable MCP connectors." in text


def test_static_cloud_preview_approval_declares_sprint_position_and_default_decision():
    text = _text()

    assert "Sprint 10 remains a cloud preview review sprint." in text
    assert "This checklist is an approval gate, not an implementation step." in text
    assert "DO_NOT_DEPLOY_YET" in text
    assert "A preview may only be approved if every required safety condition is satisfied." in text


def test_static_cloud_preview_approval_preserves_required_safety_posture():
    text = _text()

    for expected in [
        "static",
        "review-only",
        "provider-disabled",
        "MCP-connector-disabled",
        "secret-free",
        "production-data-free",
        "write-disabled",
        "notification-disabled",
        "remediation-disabled",
        "benchmark-isolated",
        "human-approval-required",
        "rollback-ready",
        "cost-bounded",
        "IAM-bounded",
        "audit-ready",
    ]:
        assert expected in text


def test_static_cloud_preview_approval_defines_repo_scope_and_static_content_checks():
    text = _text()

    for expected in [
        "current branch is sprint-10-cloud-preview-review",
        "git status is clean",
        "full pytest suite passes",
        "STATIC_REVIEW_PREVIEW",
        "no live orchestration",
        "no agent runtime",
        "precomputed static demo export",
        "precomputed operator demo command output",
    ]:
        assert expected in text



def test_static_cloud_preview_approval_blocks_disallowed_content():
    text = _text()

    for expected in [
        "production incidents",
        "production telemetry",
        "production knowledge exports",
        "secrets",
        "credentials",
        "provider credentials",
        "connector credentials",
        "provider endpoint configuration",
        "connector endpoint configuration",
        "executable remediation controls",
        "mutable benchmark truth",
    ]:
        assert expected in text


def test_static_cloud_preview_approval_defines_provider_and_connector_checks():
    text = _text()

    for expected in [
        "providers_enabled is false",
        "provider_runtime_enabled is false",
        "provider_credentials_present is false",
        "provider_invocation_allowed is false",
        "provider output cannot define benchmark truth",
        "mcp_connectors_enabled is false",
        "connector_runtime_enabled is false",
        "connector_credentials_present is false",
        "connector_invocation_allowed is false",
        "connector_benchmark_mutation_allowed is false",
    ]:
        assert expected in text


def test_static_cloud_preview_approval_defines_iam_cost_network_checks():
    text = _text()

    for expected in [
        "least privilege is preserved",
        "no broad administrator role is required",
        "no production system access is required",
        "no secret manager read role is required",
        "expected monthly cost is documented",
        "maximum monthly cost is documented",
        "cost stop conditions are documented",
        "no production network dependency",
        "no AI provider endpoint dependency",
        "no MCP connector endpoint dependency",
    ]:
        assert expected in text


def test_static_cloud_preview_approval_preserves_benchmark_and_human_approval():
    text = _text()

    for expected in [
        "benchmark truth remains isolated",
        "preview does not create benchmark truth",
        "preview does not modify benchmark truth",
        "preview does not infer benchmark truth",
        "preview does not overwrite benchmark truth",
        "preview output is not a benchmark authority",
        "human approval remains required",
        "preview cannot approve actions",
        "preview cannot bypass human review",
        "autonomous action remains disabled",
    ]:
        assert expected in text


def test_static_cloud_preview_approval_defines_rollback_and_decision_model():
    text = _text()

    for expected in [
        "rollback owner is documented",
        "disable method is documented",
        "expected rollback time is documented",
        "emergency disable triggers are documented",
        "APPROVED_FOR_STATIC_PREVIEW_ONLY",
        "BLOCKED_PENDING_EVIDENCE",
        "BLOCKED_SCOPE_VIOLATION",
        "BLOCKED_PROVIDER_OR_CONNECTOR_RISK",
        "BLOCKED_IAM_OR_COST_RISK",
        "BLOCKED_ROLLBACK_RISK",
        "DO_NOT_DEPLOY_YET",
    ]:
        assert expected in text


def test_static_cloud_preview_approval_defines_record_and_non_approval_conditions():
    text = _text()

    for expected in [
        "approval decision",
        "approved branch",
        "approved commit",
        "unresolved risks",
        "expiration or review date",
        "tests fail",
        "git status is not clean",
        "providers are enabled",
        "MCP connectors are enabled",
        "rollback is unclear",
        "This checklist does not approve deployment by itself.",
    ]:
        assert expected in text


def test_static_cloud_preview_approval_contains_interview_explanation_and_sound_bite():
    text = _text()

    assert "Before any cloud preview, I would require an approval checklist" in text
    assert "static, provider-disabled, connector-disabled" in text
    assert "Preview approval is not a technical checkbox." in text
    assert "It is an enterprise control decision." in text
