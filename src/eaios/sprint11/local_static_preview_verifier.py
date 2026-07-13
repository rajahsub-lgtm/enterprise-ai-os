"""Sprint 11 local static preview bundle safety verifier.

This module verifies an in-memory static preview bundle before any future
materialization decision.

It does not persist files, publish a site, start a server, launch a browser,
create cloud resources, call providers, call MCP connectors, load credentials,
read production data, send notifications, execute remediation, mutate benchmark
truth, approve actions, or enable autonomous action.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint11.local_static_preview_bundle import (
    LocalStaticPreviewBundle,
    LocalStaticPreviewBundleStatus,
    validate_bundle_is_in_memory_static_only,
)


class LocalStaticPreviewVerificationStatus(str, Enum):
    VERIFIED_SAFE_FOR_LOCAL_REVIEW = "VERIFIED_SAFE_FOR_LOCAL_REVIEW"
    BLOCKED_SAFETY_VIOLATIONS = "BLOCKED_SAFETY_VIOLATIONS"


class LocalStaticPreviewCheckCategory(str, Enum):
    BUNDLE_STATE = "BUNDLE_STATE"
    CONTENT_BOUNDARY = "CONTENT_BOUNDARY"
    DECISION_BOUNDARY = "DECISION_BOUNDARY"
    INTEGRATION_BOUNDARY = "INTEGRATION_BOUNDARY"
    RUNTIME_BOUNDARY = "RUNTIME_BOUNDARY"
    APPROVAL_BOUNDARY = "APPROVAL_BOUNDARY"


@dataclass(frozen=True)
class LocalStaticPreviewSafetyCheck:
    check_id: str
    category: LocalStaticPreviewCheckCategory
    description: str
    passed: bool
    evidence: str


@dataclass(frozen=True)
class LocalStaticPreviewVerificationResult:
    verification_id: str
    status: LocalStaticPreviewVerificationStatus
    bundle_id: str
    decision: str
    checks: tuple[LocalStaticPreviewSafetyCheck, ...]
    violations: tuple[str, ...]
    check_count: int
    passed_count: int
    failed_count: int
    files_persisted: bool
    site_published: bool
    server_started: bool
    browser_opened: bool
    cloud_resources_created: bool
    providers_enabled: bool
    mcp_connectors_enabled: bool
    production_data_used: bool
    credentials_required: bool
    runtime_enabled: bool
    writes_enabled: bool
    notifications_enabled: bool
    remediation_enabled: bool
    benchmark_truth_mutation_enabled: bool
    autonomous_action_enabled: bool
    human_approval_required: bool
    rollback_required: bool
    materialization_allowed: bool
    cloud_deployment_allowed: bool
    provenance: str


_FORBIDDEN_OVERCLAIMS = (
    "production deployed",
    "cloud deployed",
    "deployment approved",
    "Providers enabled: True",
    "MCP connectors enabled: True",
    "Autonomous action enabled: True",
    "Production data used: True",
    "Runtime enabled: True",
    "Writes enabled: True",
    "Notifications enabled: True",
    "Remediation enabled: True",
    "Benchmark truth mutation enabled: True",
    "real ServiceNow connected",
    "real BigPanda connected",
    "real Dynatrace connected",
    "real SAP SolMan connected",
)


_REQUIRED_SAFETY_PHRASES = (
    "DO_NOT_DEPLOY_YET",
    "STATIC_REVIEW_PREVIEW",
    "Providers enabled: False",
    "MCP connectors enabled: False",
    "Production data used: False",
    "Human approval required: True",
)


def _bundle_content(bundle: LocalStaticPreviewBundle) -> str:
    return "\n".join(item.content for item in bundle.files)


def _check(
    *,
    check_id: str,
    category: LocalStaticPreviewCheckCategory,
    description: str,
    passed: bool,
    evidence: str,
) -> LocalStaticPreviewSafetyCheck:
    return LocalStaticPreviewSafetyCheck(
        check_id=check_id,
        category=category,
        description=description,
        passed=passed,
        evidence=evidence,
    )


def _collect_violations(
    checks: tuple[LocalStaticPreviewSafetyCheck, ...],
    bundle_violations: tuple[str, ...],
) -> tuple[str, ...]:
    failed = tuple(
        f"{check.check_id}: {check.description}"
        for check in checks
        if not check.passed
    )
    return bundle_violations + failed


def verify_local_static_preview_bundle_safety(
    bundle: LocalStaticPreviewBundle,
) -> LocalStaticPreviewVerificationResult:
    bundle_valid, bundle_violations = validate_bundle_is_in_memory_static_only(bundle)
    content = _bundle_content(bundle)

    missing_required_phrases = tuple(
        phrase for phrase in _REQUIRED_SAFETY_PHRASES if phrase not in content
    )
    forbidden_overclaims = tuple(
        claim for claim in _FORBIDDEN_OVERCLAIMS if claim in content
    )

    checks = (
        _check(
            check_id="bundle-assembled-in-memory",
            category=LocalStaticPreviewCheckCategory.BUNDLE_STATE,
            description="bundle is assembled in memory",
            passed=bundle.status == LocalStaticPreviewBundleStatus.ASSEMBLED_IN_MEMORY,
            evidence=bundle.status.value,
        ),
        _check(
            check_id="bundle-validator-clean",
            category=LocalStaticPreviewCheckCategory.BUNDLE_STATE,
            description="bundle validator reports no static-only violations",
            passed=bundle_valid,
            evidence="; ".join(bundle_violations) or "no bundle violations",
        ),
        _check(
            check_id="files-not-persisted",
            category=LocalStaticPreviewCheckCategory.RUNTIME_BOUNDARY,
            description="files remain in memory and are not persisted",
            passed=bundle.files_persisted is False
            and all(item.persisted is False for item in bundle.files),
            evidence=f"files_persisted={bundle.files_persisted}",
        ),
        _check(
            check_id="no-site-server-browser-or-cloud",
            category=LocalStaticPreviewCheckCategory.RUNTIME_BOUNDARY,
            description="no site publishing, server, browser, or cloud resource creation",
            passed=not any(
                (
                    bundle.site_published,
                    bundle.server_started,
                    bundle.browser_opened,
                    bundle.cloud_resources_created,
                )
            ),
            evidence=(
                f"site_published={bundle.site_published}, "
                f"server_started={bundle.server_started}, "
                f"browser_opened={bundle.browser_opened}, "
                f"cloud_resources_created={bundle.cloud_resources_created}"
            ),
        ),
        _check(
            check_id="decision-remains-do-not-deploy",
            category=LocalStaticPreviewCheckCategory.DECISION_BOUNDARY,
            description="decision remains DO_NOT_DEPLOY_YET",
            passed=bundle.decision == "DO_NOT_DEPLOY_YET",
            evidence=bundle.decision,
        ),
        _check(
            check_id="providers-and-connectors-disabled",
            category=LocalStaticPreviewCheckCategory.INTEGRATION_BOUNDARY,
            description="providers and MCP connectors remain disabled",
            passed=bundle.providers_enabled is False
            and bundle.mcp_connectors_enabled is False,
            evidence=(
                f"providers_enabled={bundle.providers_enabled}, "
                f"mcp_connectors_enabled={bundle.mcp_connectors_enabled}"
            ),
        ),
        _check(
            check_id="no-production-data-or-credentials",
            category=LocalStaticPreviewCheckCategory.CONTENT_BOUNDARY,
            description="production data and credentials are not required or used",
            passed=bundle.production_data_used is False
            and bundle.credentials_required is False,
            evidence=(
                f"production_data_used={bundle.production_data_used}, "
                f"credentials_required={bundle.credentials_required}"
            ),
        ),
        _check(
            check_id="no-actions-or-benchmark-mutation",
            category=LocalStaticPreviewCheckCategory.APPROVAL_BOUNDARY,
            description="writes, notifications, remediation, benchmark mutation, and autonomous action remain disabled",
            passed=not any(
                (
                    bundle.writes_enabled,
                    bundle.notifications_enabled,
                    bundle.remediation_enabled,
                    bundle.benchmark_truth_mutation_enabled,
                    bundle.autonomous_action_enabled,
                )
            ),
            evidence=(
                f"writes_enabled={bundle.writes_enabled}, "
                f"notifications_enabled={bundle.notifications_enabled}, "
                f"remediation_enabled={bundle.remediation_enabled}, "
                f"benchmark_truth_mutation_enabled={bundle.benchmark_truth_mutation_enabled}, "
                f"autonomous_action_enabled={bundle.autonomous_action_enabled}"
            ),
        ),
        _check(
            check_id="human-approval-and-rollback-required",
            category=LocalStaticPreviewCheckCategory.APPROVAL_BOUNDARY,
            description="human approval and rollback remain required",
            passed=bundle.human_approval_required is True
            and bundle.rollback_required is True,
            evidence=(
                f"human_approval_required={bundle.human_approval_required}, "
                f"rollback_required={bundle.rollback_required}"
            ),
        ),
        _check(
            check_id="required-safety-phrases-present",
            category=LocalStaticPreviewCheckCategory.CONTENT_BOUNDARY,
            description="required safety phrases are present in rendered content",
            passed=missing_required_phrases == (),
            evidence=", ".join(missing_required_phrases) or "all required phrases present",
        ),
        _check(
            check_id="no-forbidden-overclaims",
            category=LocalStaticPreviewCheckCategory.CONTENT_BOUNDARY,
            description="rendered content contains no forbidden deployment or integration overclaims",
            passed=forbidden_overclaims == (),
            evidence=", ".join(forbidden_overclaims) or "no forbidden overclaims",
        ),
    )

    violations = _collect_violations(checks, bundle_violations)
    status = (
        LocalStaticPreviewVerificationStatus.VERIFIED_SAFE_FOR_LOCAL_REVIEW
        if violations == ()
        else LocalStaticPreviewVerificationStatus.BLOCKED_SAFETY_VIOLATIONS
    )

    return LocalStaticPreviewVerificationResult(
        verification_id="sprint11-local-static-preview-verification-001",
        status=status,
        bundle_id=bundle.bundle_id,
        decision=bundle.decision,
        checks=checks,
        violations=violations,
        check_count=len(checks),
        passed_count=sum(1 for check in checks if check.passed),
        failed_count=sum(1 for check in checks if not check.passed),
        files_persisted=bundle.files_persisted,
        site_published=bundle.site_published,
        server_started=bundle.server_started,
        browser_opened=bundle.browser_opened,
        cloud_resources_created=bundle.cloud_resources_created,
        providers_enabled=bundle.providers_enabled,
        mcp_connectors_enabled=bundle.mcp_connectors_enabled,
        production_data_used=bundle.production_data_used,
        credentials_required=bundle.credentials_required,
        runtime_enabled=bundle.runtime_enabled,
        writes_enabled=bundle.writes_enabled,
        notifications_enabled=bundle.notifications_enabled,
        remediation_enabled=bundle.remediation_enabled,
        benchmark_truth_mutation_enabled=bundle.benchmark_truth_mutation_enabled,
        autonomous_action_enabled=bundle.autonomous_action_enabled,
        human_approval_required=bundle.human_approval_required,
        rollback_required=bundle.rollback_required,
        materialization_allowed=False,
        cloud_deployment_allowed=False,
        provenance="local_static_preview_verifier:in_memory",
    )


def verification_to_view_model(
    result: LocalStaticPreviewVerificationResult,
) -> dict[str, Any]:
    return {
        "verification_id": result.verification_id,
        "status": result.status.value,
        "bundle_id": result.bundle_id,
        "decision": result.decision,
        "checks": [
            {
                "check_id": check.check_id,
                "category": check.category.value,
                "description": check.description,
                "passed": check.passed,
                "evidence": check.evidence,
            }
            for check in result.checks
        ],
        "violations": list(result.violations),
        "check_count": result.check_count,
        "passed_count": result.passed_count,
        "failed_count": result.failed_count,
        "files_persisted": result.files_persisted,
        "site_published": result.site_published,
        "server_started": result.server_started,
        "browser_opened": result.browser_opened,
        "cloud_resources_created": result.cloud_resources_created,
        "providers_enabled": result.providers_enabled,
        "mcp_connectors_enabled": result.mcp_connectors_enabled,
        "production_data_used": result.production_data_used,
        "credentials_required": result.credentials_required,
        "runtime_enabled": result.runtime_enabled,
        "writes_enabled": result.writes_enabled,
        "notifications_enabled": result.notifications_enabled,
        "remediation_enabled": result.remediation_enabled,
        "benchmark_truth_mutation_enabled": result.benchmark_truth_mutation_enabled,
        "autonomous_action_enabled": result.autonomous_action_enabled,
        "human_approval_required": result.human_approval_required,
        "rollback_required": result.rollback_required,
        "materialization_allowed": result.materialization_allowed,
        "cloud_deployment_allowed": result.cloud_deployment_allowed,
        "provenance": result.provenance,
    }
