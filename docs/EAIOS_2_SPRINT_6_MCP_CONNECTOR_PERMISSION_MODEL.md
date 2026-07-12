# EAIOS 2 Sprint 6 MCP Connector Permission Model

## Status

REVIEW_ONLY_PERMISSION_MODEL

This document is an MCP connector permission model. It is not a connector implementation.

## Design Goal

Define how EAIOS could later enable real MCP connectors while preserving permission boundaries, read/write classification, sandboxing, auditability, human review, and benchmark truth isolation.

## Current Connector State

REAL_MCP_CONNECTORS_DISABLED_BY_DEFAULT

## Current Sprint 5 Connector Mode

DETERMINISTIC_CONNECTOR_FIXTURE_ONLY

## What This Model Allows

review connector inventory
review connector permission boundaries
review read-only connector patterns
review write-capable connector risk
review sandbox requirements
review audit requirements
review human approval gates
review rollback and disable requirements

## What This Model Blocks

call_real_connector
execute_tool_action
perform_external_write
modify_production_record
change_infrastructure
send_notification
load_secret_material
access_unapproved_network
score_benchmark_from_connector_output
update_benchmark_truth_from_connector_output
enable_autonomous_remediation
bypass_human_review

## Connector Boundary Principles

Connector output is evidence, not truth.
Connector output is advisory, not executable.
Connector output must not update benchmark truth.
Connector output must not score benchmarks.
Connector output must not execute remediation.
Connector output must not bypass human review.
Connector permissions must be explicit.
Connector owners must be identified.
Connector rollback must be available.

## Connector Inventory Fields

connector_id
connector_name
connector_type
owning_service
service_owner
business_owner
technical_owner
data_domain
data_classification
allowed_operations
disallowed_operations
read_write_classification
environment_scope
approval_status
risk_tier
audit_required
rollback_or_disable_switch
human_review_required

## Permission Classes

READ_ONLY
READ_WITH_FILTERED_DATA
READ_WITH_SENSITIVE_DATA
WRITE_NON_PRODUCTION
WRITE_PRODUCTION_REQUIRES_APPROVAL
WRITE_PRODUCTION_BLOCKED
ADMIN_OPERATION_BLOCKED

## Operation Classification

safe_read_operation
sensitive_read_operation
non_production_write_operation
production_write_operation
notification_operation
remediation_operation
identity_or_access_operation
benchmark_scoring_operation
benchmark_truth_update_operation

## Required Gates

connector_inventory_review
permission_model_review
read_write_classification_review
sandbox_boundary_review
secret_handling_review
network_access_review
human_approval_review
rollback_plan_review
production_deployment_approval

## Read-Only Connector Rules

Read-only connectors may retrieve approved evidence.
Read-only connectors may return structured observations.
Read-only connectors may include provenance.
Read-only connectors may include timestamps.
Read-only connectors may include confidence metadata.

Read-only connectors must not modify records.
Read-only connectors must not send notifications.
Read-only connectors must not execute remediation.
Read-only connectors must not change infrastructure.
Read-only connectors must not score benchmarks.
Read-only connectors must not update benchmark truth.

## Write-Capable Connector Rules

Write-capable connectors remain disabled by default.

Before write-capable connectors are enabled, the project needs:

explicit service owner approval
explicit business owner approval
change control mapping
environment separation
approval workflow project needs:

explicit service owner approval
explicit business owner approval
change
blast radius analysis
rollback plan
audit trail
human review requirement
production deployment approval

## Sandbox Boundary

No real connector call is performed by this model.

A future sandbox must define:

sandbox_environment
allowed_test_records
blocked_production_records
mock_write_mode
dry_run_mode
audit_capture_mode
egress_policy
timeout_policy
rate_limit_policy
disable_switch

## Audit Boundary

Every future connector interaction must record:

request_id
connector_id
operation_requested
permission_class
read_write_classification
input_evidence_references
output_evidence_references
human_review_requirement
approval_reference
blocked_actions
timestamp
latency_metadata
result_hash_or_reference

## Secret Boundary

No secret material is loaded by this model.

Before connector secret enablement, the project needs:

security_owner
secret_inventory
approved_secret_store
rotation_policy
least_privilege_runtime_identity
environment_separation
audit_logging
rollback_or_disable_switch

## Network Boundary

No external network access is performed by this model.

Before network access is enabled, the project needs:

egress_review
connector_endpoint_allowlist
timeout_policy
retry_policy
rate_limit_policy
logging_policy
incident_rollback_plan

## Benchmark Boundary

Benchmark truth remains external.

Connectors must not:

define_benchmark_truth
modify_benchmark_truth
score_benchmark_results
infer_benchmark_labels_from_connector_output
replace_benchmark_verification_targets
override_deterministic_scoring_logic

## Human Review Boundary

Human review remains required for:

write-capable connector requests
production record changes
notification operations
remediation operations
identity or access operations
high-risk recommendations
benchmark scoring requests
benchmark truth update requests

## Deployment Relationship

This permission model depends on:

docs/EAIOS_2_SPRINT_6_PROVIDER_INTEGRATION_DESIGN.md
src/eaios/sprint5/mcp_connector_harness.py
src/eaios/sprint6/portfolio_walkthrough.py

Real MCP connector enablement must remain disabled until connector inventory, permission model, sandboxing, secret handling, network access, audit, rollback, and human approval reviews are complete.

## Safe Enablement Phases

Phase 1: deterministic connector fixture only.
Phase 2: connector inventory and permission model review.
Phase 3: read-only sandbox simulation.
Phase 4: read-only non-production connector after approval.
Phase 5: write-capable dry-run connector after approval.
Phase 6: human-approved production pilot after approval.

## Required Tests Before Enablement

connector_inventory_schema_tests
permission_classification_tests
read_only_boundary_tests
write_operation_block_tests
secret_loading_block_tests
network_access_block_tests
benchmark_truth_isolation_tests
human_review_requirement_tests
audit_trace_tests
rollback_disable_switch_tests

## Explicit Non-Goals

This model does not call a real connector.
This model does not execute tool actions.
This model does not modify records.
This model does not change infrastructure.
This model does not send notifications.
This model does not load secrets.
This model does not access external networks.
This model does not score benchmarks.
This model does not update benchmark truth.
This model does not enable autonomous remediation.
This model does not bypass human review.

## Closeout Statement

Sprint 6 MCP connector enablement remains review-only.

The permission model explains how real MCP connectors can be introduced later without weakening governance, auditability, permission boundaries, benchmark truth isolation, rollback, or human review.
