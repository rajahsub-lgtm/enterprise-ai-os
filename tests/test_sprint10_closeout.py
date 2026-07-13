from pathlib import Path


DOC = Path("docs/EAIOS_2_SPRINT_10_CLOSEOUT.md")

REQUIRED_FILES = [
    Path("docs/EAIOS_2_SPRINT_10_STATIC_PREVIEW_SCOPE_CONTRACT.md"),
    Path("docs/EAIOS_2_SPRINT_10_STATIC_EXPORT_MATERIALIZATION_PLAN.md"),
    Path("docs/EAIOS_2_SPRINT_10_CLOUD_IAM_COST_BOUNDARY.md"),
    Path("docs/EAIOS_2_SPRINT_10_ROLLBACK_DISABLE_PLAN.md"),
    Path("docs/EAIOS_2_SPRINT_10_PROVIDER_CONNECTOR_DISABLED_STATE_VERIFICATION.md"),
    Path("docs/EAIOS_2_SPRINT_10_STATIC_CLOUD_PREVIEW_APPROVAL_CHECKLIST.md"),
    Path("docs/EAIOS_2_SPRINT_10_STATIC_PREVIEW_DECISION_RECORD.md"),
]


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_sprint10_closeout_file_exists():
    assert DOC.exists()


def test_sprint10_closeout_required_files_exist():
    assert [str(path) for path in REQUIRED_FILES if not path.exists()] == []


def test_sprint10_closeout_declares_status_and_decision():
    text = _text()

    assert "Sprint 10 - Cloud Preview Review" in text
    assert "CLOUD_PREVIEW_REVIEW_COMPLETE_DO_NOT_DEPLOY_YET" in text
    assert "Final Decision" in text
    assert "DO_NOT_DEPLOY_YET" in text


def test_sprint10_closeout_declares_non_actions():
    text = _text()

    for expected in [
        "It did not approve cloud deployment.",
        "It did not create cloud resources.",
        "It did not materialize static deployment files.",
        "It did not start a runtime.",
        "It did not enable providers.",
        "It did not enable MCP connectors.",
        "It did not create secrets.",
        "It did not use production data.",
    ]:
        assert expected in text


def test_sprint10_closeout_lists_completed_slices():
    text = _text()

    for expected in [
        "10-1 static preview scope contract",
        "10-2 static export materialization plan",
        "10-3 cloud IAM and cost boundary",
        "10-4 rollback and disable plan",
        "10-5 provider and connector disabled-state verification",
        "10-6 static cloud preview approval checklist",
        "10-7 static preview decision record",
        "10-8 Sprint 10 closeout",
    ]:
        assert expected in text


def test_sprint10_closeout_lists_primary_artifacts():
    text = _text()

    for expected in [
        "docs/EAIOS_2_SPRINT_10_STATIC_PREVIEW_SCOPE_CONTRACT.md",
        "docs/EAIOS_2_SPRINT_10_STATIC_EXPORT_MATERIALIZATION_PLAN.md",
        "docs/EAIOS_2_SPRINT_10_CLOUD_IAM_COST_BOUNDARY.md",
        "docs/EAIOS_2_SPRINT_10_ROLLBACK_DISABLE_PLAN.md",
        "docs/EAIOS_2_SPRINT_10_PROVIDER_CONNECTOR_DISABLED_STATE_VERIFICATION.md",
        "docs/EAIOS_2_SPRINT_10_STATIC_CLOUD_PREVIEW_APPROVAL_CHECKLIST.md",
        "docs/EAIOS_2_SPRINT_10_STATIC_PREVIEW_DECISION_RECORD.md",
        "docs/EAIOS_2_SPRINT_10_CLOSEOUT.md",
    ]:
        assert expected in text



def test_sprint10_closeout_preserves_blocked_activity_and_static_scope():
    text = _text()

    for expected in [
        "Blocked activities",
        "deploy to cloud",
        "create cloud resources",
        "publish static site",
        "call providers",
        "call MCP connectors",
        "mutate benchmark truth",
        "enable autonomous action",
        "STATIC_REVIEW_PREVIEW",
        "must not execute live orchestration",
        "must not start an agent runtime",
    ]:
        assert expected in text


def test_sprint10_closeout_preserves_iam_cost_and_rollback_positions():
    text = _text()

    for expected in [
        "static hosting only",
        "least privilege",
        "no broad administrator role",
        "no production system access",
        "bounded cost",
        "documented cost owner",
        "If we cannot turn it off safely, we should not turn it on.",
        "rollback owner",
        "expected rollback time",
        "emergency disable triggers",
    ]:
        assert expected in text


def test_sprint10_closeout_preserves_provider_connector_disabled_position():
    text = _text()

    for expected in [
        "Providers remain disabled.",
        "MCP connectors remain disabled.",
        "Disabled means more than unused.",
        "no credentials",
        "no endpoints",
        "no invocation path",
        "no cost path",
        "no write path",
        "no benchmark mutation path",
        "no hidden fallback path",
    ]:
        assert expected in text


def test_sprint10_closeout_preserves_decision_record_position():
    text = _text()

    for expected in [
        "The checklist is not approval.",
        "The default approval decision remains:",
        "DO_NOT_DEPLOY_YET",
        "This prevents accidental drift from review into deployment.",
        "A gate is not approval.",
        "A checklist is not approval.",
        "A decision record prevents accidental deployment.",
    ]:
        assert expected in text


def test_sprint10_closeout_documents_what_it_proves_and_does_not_claim():
    text = _text()

    for expected in [
        "cloud preview planning can be governed before implementation",
        "architecture review from deployment",
        "checklist definition from approval",
        "static preview from runtime",
        "provider documentation from provider enablement",
        "MCP connector documentation from connector execution",
        "production deployment",
        "cloud deployment approval",
        "real provider execution",
        "real MCP connector execution",
        "autonomous action",
    ]:
        assert expected in text


def test_sprint10_closeout_lists_future_conditions_and_portfolio_position():
    text = _text()

    for expected in [
        "full test suite passes",
        "git status is clean",
        "scope remains static-only",
        "providers remain disabled",
        "MCP connectors remain disabled",
        "benchmark truth remains isolated",
        "explicit approval is recorded",
        "interview-ready",
        "portfolio-ready",
        "cloud-review-ready",
        "deployment-not-approved",
    ]:
        assert expected in text


def test_sprint10_closeout_contains_next_direction_and_final_sound_bite():
    text = _text()

    for expected in [
        "The next sprint should not automatically deploy.",
        "create local static preview generator only if explicitly approved",
        "keep cloud deployment blocked unless a separate approval decision changes",
        "Sprint 10 is closed as cloud preview review.",
        "Cloud readiness is not deployment.",
        "Governed decision-making comes first.",
    ]:
        assert expected in text
