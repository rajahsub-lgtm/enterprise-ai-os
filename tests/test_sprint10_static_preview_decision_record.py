from pathlib import Path


DOC = Path("docs/EAIOS_2_SPRINT_10_STATIC_PREVIEW_DECISION_RECORD.md")

REQUIRED_FILES = [
    Path("docs/EAIOS_2_SPRINT_10_STATIC_PREVIEW_SCOPE_CONTRACT.md"),
    Path("docs/EAIOS_2_SPRINT_10_STATIC_EXPORT_MATERIALIZATION_PLAN.md"),
    Path("docs/EAIOS_2_SPRINT_10_CLOUD_IAM_COST_BOUNDARY.md"),
    Path("docs/EAIOS_2_SPRINT_10_ROLLBACK_DISABLE_PLAN.md"),
    Path("docs/EAIOS_2_SPRINT_10_PROVIDER_CONNECTOR_DISABLED_STATE_VERIFICATION.md"),
    Path("docs/EAIOS_2_SPRINT_10_STATIC_CLOUD_PREVIEW_APPROVAL_CHECKLIST.md"),
]


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_static_preview_decision_record_file_exists():
    assert DOC.exists()


def test_static_preview_decision_record_required_prior_artifacts_exist():
    assert [str(path) for path in REQUIRED_FILES if not path.exists()] == []


def test_static_preview_decision_record_declares_purpose_and_non_actions():
    text = _text()

    assert "records the current decision" in text
    assert "It does not approve deployment." in text
    assert "It does not create cloud resources." in text
    assert "It does not materialize static files." in text
    assert "It does not start a runtime." in text
    assert "It does not enable providers." in text
    assert "It does not enable MCP connectors." in text
    assert "prevent the approval checklist from being mistaken for actual approval" in text


def test_static_preview_decision_record_declares_current_decision():
    text = _text()

    assert "DO_NOT_DEPLOY_YET" in text
    assert "RECORDED_REVIEW_DECISION" in text
    assert "EAIOS is not approved for cloud deployment yet." in text
    assert "EAIOS is not approved for static preview deployment yet." in text


def test_static_preview_decision_record_explains_reason_for_decision():
    text = _text()

    assert "The current Sprint 10 work is review-first." in text
    assert "Those artifacts define what must be true before approval." in text
    assert "They do not themselves approve deployment." in text


def test_static_preview_decision_record_lists_approved_and_blocked_activity():
    text = _text()

    for expected in [
        "Approved activities",
        "maintain local repository artifacts",
        "run local tests",
        "review static preview scope",
        "Blocked activities",
        "deploy to cloud",
        "create cloud resources",
        "publish static site",
        "call providers",
        "call MCP connectors",
        "mutate benchmark truth",
        "enable autonomous action",
    ]:
        assert expected in text



def test_static_preview_decision_record_lists_decision_inputs_and_future_evidence():
    text = _text()

    for expected in [
        "docs/EAIOS_2_SPRINT_10_STATIC_PREVIEW_SCOPE_CONTRACT.md",
        "docs/EAIOS_2_SPRINT_10_STATIC_EXPORT_MATERIALIZATION_PLAN.md",
        "docs/EAIOS_2_SPRINT_10_CLOUD_IAM_COST_BOUNDARY.md",
        "docs/EAIOS_2_SPRINT_10_ROLLBACK_DISABLE_PLAN.md",
        "docs/EAIOS_2_SPRINT_10_PROVIDER_CONNECTOR_DISABLED_STATE_VERIFICATION.md",
        "docs/EAIOS_2_SPRINT_10_STATIC_CLOUD_PREVIEW_APPROVAL_CHECKLIST.md",
        "full test suite passes",
        "git status is clean",
        "providers remain disabled",
        "MCP connectors remain disabled",
        "benchmark truth remains isolated",
        "human approval remains required",
    ]:
        assert expected in text


def test_static_preview_decision_record_preserves_provider_disabled_state():
    text = _text()

    for expected in [
        "Provider state remains:",
        "providers_enabled = false",
        "provider_runtime_enabled = false",
        "provider_credentials_present = false",
        "provider_endpoint_configured = false",
        "provider_invocation_allowed = false",
        "provider_cost_enabled = false",
        "Provider enablement is not approved.",
    ]:
        assert expected in text


def test_static_preview_decision_record_preserves_mcp_disabled_state():
    text = _text()

    for expected in [
        "MCP connector state remains:",
        "mcp_connectors_enabled = false",
        "connector_runtime_enabled = false",
        "connector_credentials_present = false",
        "connector_endpoints_configured = false",
        "connector_invocation_allowed = false",
        "connector_write_allowed = false",
        "connector_notification_allowed = false",
        "connector_remediation_allowed = false",
        "connector_benchmark_mutation_allowed = false",
        "connector_cost_enabled = false",
        "MCP connector enablement is not approved.",
    ]:
        assert expected in text


def test_static_preview_decision_record_preserves_deployment_state():
    text = _text()

    for expected in [
        "cloud_deployment_approved = false",
        "static_preview_approved = false",
        "implementation_approved = false",
        "runtime_enabled = false",
        "production_data_used = false",
        "secrets_required = false",
        "writes_enabled = false",
        "notifications_enabled = false",
        "remediation_enabled = false",
        "benchmark_truth_mutation_enabled = false",
        "autonomous_action_enabled = false",
        "human_approval_required = true",
    ]:
        assert expected in text


def test_static_preview_decision_record_defines_change_conditions_and_outcomes():
    text = _text()

    for expected in [
        "Decision Change Conditions",
        "required Sprint 10 review artifacts exist",
        "provider disabled-state verification passes",
        "MCP connector disabled-state verification passes",
        "IAM and cost boundaries are approved",
        "rollback and disable plan is approved",
        "explicit approval is recorded",
        "APPROVED_FOR_STATIC_PREVIEW_ONLY",
        "BLOCKED_PROVIDER_OR_CONNECTOR_RISK",
        "BLOCKED_IAM_OR_COST_RISK",
        "BLOCKED_ROLLBACK_RISK",
        "The current decision remains DO_NOT_DEPLOY_YET.",
    ]:
        assert expected in text


def test_static_preview_decision_record_explains_prevented_drift():
    text = _text()

    for expected in [
        "prevents accidental drift from review into deployment",
        "prevents the team from treating documentation as approval",
        "prevents a static preview from becoming a runtime",
        "prevents disabled providers or connectors from becoming implicit integrations",
        "bypassing enterprise controls",
    ]:
        assert expected in text


def test_static_preview_decision_record_contains_interview_explanation_and_sound_bite():
    text = _text()

    assert "I intentionally recorded the current decision as DO_NOT_DEPLOY_YET" in text
    assert "deployment still requires explicit approval" in text
    assert "A gate is not approval." in text
    assert "A checklist is not approval." in text
    assert "A decision record prevents accidental deployment." in text
