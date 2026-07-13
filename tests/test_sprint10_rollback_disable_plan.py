from pathlib import Path


DOC = Path("docs/EAIOS_2_SPRINT_10_ROLLBACK_DISABLE_PLAN.md")


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_rollback_disable_plan_file_exists():
    assert DOC.exists()


def test_rollback_disable_plan_declares_purpose_and_non_actions():
    text = _text()

    assert "defines the rollback and disable plan" in text
    assert "It does not approve deployment." in text
    assert "It does not create cloud resources." in text
    assert "It does not disable any live resource." in text
    assert "It does not create runtime behavior." in text


def test_rollback_disable_plan_declares_sprint10_position_and_principle():
    text = _text()

    assert "Sprint 10 remains a cloud preview review sprint." in text
    assert "Rollback planning must happen before deployment planning." in text
    assert "If we cannot turn it off safely, we should not turn it on." in text
    assert "reversible, bounded, owned, and auditable" in text


def test_rollback_disable_plan_preserves_static_preview_assumption():
    text = _text()

    for expected in [
        "STATIC_REVIEW_PREVIEW",
        "static documentation and precomputed demo artifacts only",
        "must not run EAIOS orchestration",
        "must not call providers",
        "must not call MCP connectors",
        "must not read production data",
        "must not write production data",
        "must not send notifications",
        "must not execute remediation",
    ]:
        assert expected in text


def test_rollback_disable_plan_defines_scope_and_metadata():
    text = _text()

    for expected in [
        "Rollback means disabling or removing the preview.",
        "reversing production writes",
        "reversing remediation",
        "revoking provider actions",
        "revoking MCP connector actions",
        "preview id",
        "deployment owner",
        "rollback owner",
        "deployed branch",
        "deployed commit",
        "expected rollback time",
        "escalation path",
    ]:
        assert expected in text


def test_rollback_disable_plan_lists_disable_triggers():
    text = _text()

    for expected in [
        "unexpected runtime behavior appears",
        "provider call is detected",
        "MCP connector call is detected",
        "production data appears",
        "secret appears",
        "production write path appears",
        "notification path appears",
        "remediation path appears",
        "benchmark truth mutation path appears",
        "autonomous action path appears",
        "cost exceeds approved threshold",
        "rollback procedure fails",
    ]:
        assert expected in text



def test_rollback_disable_plan_defines_disable_artifact_access_and_validation_requirements():
    text = _text()

    for expected in [
        "remove static hosting route",
        "disable static site serving",
        "remove preview artifact folder",
        "revoke preview access",
        "generated static HTML files",
        "manifest file",
        "preview URL no longer serves content",
        "preview is not reachable",
        "no runtime exists",
        "no provider access exists",
        "no MCP connector access exists",
        "cost-generating resources are stopped or removed",
    ]:
        assert expected in text


def test_rollback_disable_plan_defines_rollback_evidence_and_emergency_disable():
    text = _text()

    for expected in [
        "rollback timestamp",
        "rollback owner",
        "rollback reason",
        "artifacts removed",
        "validation result",
        "Emergency disable",
        "secret exposure",
        "production data exposure",
        "provider execution",
        "MCP connector execution",
        "Emergency disable should favor safety over availability.",
    ]:
        assert expected in text


def test_rollback_disable_plan_defines_owner_and_time_responsibilities():
    text = _text()

    for expected in [
        "The deployment owner is responsible",
        "The rollback owner is responsible",
        "The business owner is responsible",
        "The technical owner is responsible",
        "Rollback Time Objective",
        "disable access quickly",
        "document completion",
    ]:
        assert expected in text


def test_rollback_disable_plan_defines_cost_and_iam_shutdown():
    text = _text()

    for expected in [
        "Cost Shutdown",
        "stop cost-generating resources",
        "confirming no runtime cost",
        "confirming no provider cost",
        "confirming no connector cost",
        "IAM Shutdown",
        "no production access",
        "no provider invocation access",
        "no MCP connector invocation access",
        "no unused preview identity remains active",
    ]:
        assert expected in text


def test_rollback_disable_plan_preserves_benchmark_and_human_approval():
    text = _text()

    for expected in [
        "Rollback must preserve benchmark truth isolation.",
        "must not modify benchmark fixtures",
        "must not overwrite benchmark truth",
        "must not generate new benchmark truth",
        "Rollback must preserve human approval boundaries.",
        "must not create approvals retroactively",
        "must not persist approval records to a production system",
    ]:
        assert expected in text


def test_rollback_disable_plan_declares_non_approval_and_interview_explanation():
    text = _text()

    for expected in [
        "This rollback plan does not approve deployment.",
        "does not approve implementation",
        "required safety condition",
        "static cloud preview approval checklist is required before deployment",
        "Before deploying even a static preview",
        "disabled quickly and validated as removed",
    ]:
        assert expected in text


def test_rollback_disable_plan_final_sound_bite():
    text = _text()

    assert "A safe preview is not just something we can show." in text
    assert "It is something we can turn off." in text
