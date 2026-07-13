# EAIOS 2 Sprint 10 Provider and Connector Disabled-State Verification

## Purpose

This document defines how EAIOS verifies that providers and MCP connectors remain disabled before any future static cloud preview.

It does not approve deployment.

It does not enable providers.

It does not enable MCP connectors.

It does not create credentials.

It does not call external APIs.

It does not create cloud resources.

It does not start runtime behavior.

It does not enable production data, writes, notifications, remediation, benchmark truth updates, release creation, or autonomous action.

The purpose is to define disabled-state verification before any preview approval.

## Sprint 10 Position

Sprint 10 remains a cloud preview review sprint.

The preferred preview remains static-only.

Provider and connector disabled-state verification must happen before any preview implementation or deployment approval.

## Verification Principle

Disabled means more than not used.

Disabled means:

- no credentials
- no endpoint calls
- no runtime invocation path
- no permission to execute
- no write capability
- no notification capability
- no remediation capability
- no benchmark mutation capability
- no bypass of human approval
- no hidden fallback path

## Preview Assumption

The assumed preview type is:

STATIC_REVIEW_PREVIEW

The preview may display static documentation and precomputed demo artifacts only.

The preview must not run EAIOS orchestration.

The preview must not call providers.

The preview must not call MCP connectors.

The preview must not require secrets.

The preview must not use production data.

## Provider Disabled-State Requirements

Providers must remain disabled.

A valid disabled provider state requires:

- providers_enabled is false
- provider_runtime_enabled is false
- provider_credentials_present is false
- provider_api_keys_present is false
- provider_endpoint_configured is false
- provider_invocation_allowed is false
- provider_retry_allowed is false
- provider_fallback_allowed is false
- provider_output_authoritative is false
- provider_cost_enabled is false

## Provider Verification Questions

Before preview approval, answer:

1. Are any provider credentials present?
2. Are any provider endpoints configured?
3. Can the preview invoke a provider?
4. Can the preview retry or fallback to a provider?
5. Can provider output influence benchmark truth?
6. Can provider output trigger remediation?
7. Can provider output trigger notification?
8. Can provider output bypass human approval?
9. Can provider usage create cost?
10. Is provider-disabled posture visible in the manifest?

## Provider Disabled Evidence

Provider disabled evidence should include:

- manifest providers_enabled equals false
- manifest provider_runtime_enabled equals false
- manifest provider_credentials_present equals false
- manifest provider_invocation_allowed equals false
- source review confirms no provider call path
- source review confirms no provider credential path
- source review confirms no provider endpoint path
- source review confirms no provider cost path
- preview content states providers remain disabled

## MCP Connector Disabled-State Requirements

MCP connectors must remain disabled.

A valid disabled connector state requires:

- mcp_connectors_enabled is false
- connector_runtime_enabled is false
- connector_credentials_present is false
- connector_endpoints_configured is false
- connector_invocation_allowed is false
- connector_write_allowed is false
- connector_notification_allowed is false
- connector_remediation_allowed is false
- connector_benchmark_mutation_allowed is false
- connector_cost_enabled is false

## MCP Connector Verification Questions

Before preview approval, answer:

1. Are any connector credentials present?
2. Are any connector endpoints configured?
3. Can the preview invoke a connector?
4. Can the preview read production data through a connector?
5. Can the preview write production data through a connector?
6. Can the preview send notifications through a connector?
7. Can the preview execute remediation through a connector?
8. Can connector output influence benchmark truth?
9. Can connector execution bypass human approval?
10. Is connector-disabled posture visible in the manifest?

## MCP Connector Disabled Evidence

Connector disabled evidence should include:

- manifest mcp_connectors_enabled equals false
- manifest connector_runtime_enabled equals false
- manifest connector_credentials_present equals false
- manifest connector_invocation_allowed equals false
- source review confirms no connector call path
- source review confirms no connector credential path
- source review confirms no connector endpoint path
- source review confirms no connector write path
- source review confirms no connector remediation path
- preview content states MCP connectors remain disabled

## Manifest Disabled-State Fields

A future static preview manifest should include:

- providers_enabled
- provider_runtime_enabled
- provider_credentials_present
- provider_endpoint_configured
- provider_invocation_allowed
- provider_cost_enabled
- mcp_connectors_enabled
- connector_runtime_enabled
- connector_credentials_present
- connector_endpoints_configured
- connector_invocation_allowed
- connector_write_allowed
- connector_notification_allowed
- connector_remediation_allowed
- connector_benchmark_mutation_allowed
- connector_cost_enabled
- human_approval_required
- autonomous_action_enabled
- benchmark_truth_mutation_enabled

## Source Review Checks

Before preview approval, the source review should confirm:

- no provider SDK invocation
- no provider HTTP invocation
- no MCP connector invocation
- no connector endpoint configuration
- no credential loading path
- no secret manager read path
- no production data read path
- no production write path
- no notification send path
- no remediation execution path
- no benchmark truth mutation path
- no autonomous action path

## Static Preview Content Checks

The static preview content should clearly state:

- providers remain disabled
- MCP connectors remain disabled
- no provider credentials are present
- no connector credentials are present
- no provider endpoints are configured
- no connector endpoints are configured
- no provider calls occur
- no connector calls occur
- no production data is used
- no production writes occur
- no notifications are sent
- no remediation is executed
- human approval remains required
- benchmark truth remains isolated

## Failure Conditions

Disabled-state verification fails if:

- a provider credential is present
- a connector credential is present
- a provider endpoint is configured
- a connector endpoint is configured
- provider invocation is possible
- connector invocation is possible
- provider usage can create cost
- connector usage can create cost
- production data can be read
- production data can be written
- notifications can be sent
- remediation can be executed
- benchmark truth can be mutated
- human approval can be bypassed
- autonomous action is enabled

## Required Action On Failure

If disabled-state verification fails:

1. do not approve preview deployment
2. remove the unsafe path
3. remove credentials or endpoints
4. update the manifest
5. rerun source review
6. rerun tests
7. rerun full suite
8. document the failure and correction
9. require approval before reconsidering preview

## Relationship To Static Preview

The static preview may explain providers and MCP connectors.

The static preview may display diagrams or documentation about provider and connector governance.

The static preview must not make provider or connector behavior executable.

The preview should show disabled-state posture as part of the safety model.

## Relationship To Human Approval

Disabled-state verification supports human approval.

Provider and connector disabled state prevents hidden execution paths.

Human approval remains required for high-risk recommendations.

Human approval must not be weakened by static preview deployment.

## Relationship To Benchmark Isolation

Provider and connector output must not define benchmark truth.

Because providers and connectors remain disabled, they cannot create, modify, infer, or overwrite benchmark truth in the static preview.

Benchmark truth remains isolated from preview output.

## Explicit Non-Approval

This document does not approve provider enablement.

This document does not approve MCP connector enablement.

This document does not approve preview deployment.

It defines a required verification condition for a later static preview approval checklist.

## Interview Explanation

The safe explanation is:

Before any cloud preview, I would verify that providers and MCP connectors are not just unused, but truly disabled: no credentials, no endpoints, no invocation path, no cost path, no write path, no remediation path, and no benchmark mutation path.

## Final Sound Bite

Disabled is a control state, not an assumption.

For enterprise AI, unused is not enough.
