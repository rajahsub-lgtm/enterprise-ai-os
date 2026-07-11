# EAIOS 2 Sprint 6 GCP Deployment Design

## Status

REVIEW_ONLY_DESIGN

This document is a deployment design artifact. It is not a deployment script.

## Design Goal

Define how EAIOS could later be packaged for GCP while preserving the Sprint 5 and Sprint 6 governance boundaries.

## Target Environment

GCP_READINESS_REVIEW_ONLY

## Readiness State

REVIEW_READY_NOT_DEPLOYED

## What This Design Allows

review architecture
review runtime packaging
review configuration boundary
review secret handling requirements
review provider integration gates
review MCP connector permission gates
review audit export requirements
review human approval gates

## What This Design Blocks

create_cloud_resources
run_gcloud_command
run_terraform_apply
run_shell_deployment_command
load_secret_material
enable_real_provider
enable_real_mcp_connectors
perform_external_write
execute_remediation
send_notification
score_benchmark_from_deployment
enable_autonomous_remediation

## Proposed GCP Components

Cloud Run for a future read-only web review surface.
Artifact Registry for container image storage after approval.
Cloud Storage for approved static artifacts after approval.
Secret Manager for approved secret boundaries after security review.
Cloud Logging for audit logs.
Cloud Monitoring for runtime health.
IAM for least-privilege service accounts.
VPC Service Controls for future data boundary review.

## Required Reviews Before Deployment

cloud_architecture_review
security_and_secret_handling_review
provider_integration_review
mcp_connector_permission_review
production_deployment_approval

## Runtime Boundary

The first deployable target must remain read-only.

No remediation execution.
No notification send.
No benchmark scoring from runtime output.
No provider call unless the provider integration gate is approved.
No MCP connector call unless the connector permission gate is approved.

## Secret Boundary

Secrets are not loaded by this design.

Before any secret is introduced, the project needs:

security owner
secret inventory
rotation policy
least-privilege access
audit logging
environment separation
rollback plan

## Provider Boundary

Real LLM provider calls remain disabled by default.

Provider enablement requires:

provider integration review
output validation boundary
prompt and response audit trail
secret handling review
cost and latency controls
human review gate
benchmark truth isolation

## MCP Connector Boundary

Real MCP connectors remain disabled by default.

Connector enablement requires:

connector inventory
permission model
read/write classification
sandbox boundary
audit logging
owner approval
rollback or disable switch
human review gate

## Benchmark Boundary

Benchmark truth remains external.

The deployment must not allow:

benchmark truth updates from runtime output
benchmark scoring from operator output
benchmark scoring from provider output
benchmark scoring from connector output
benchmark scoring from dashboard output

## Human Approval Boundary

Human approval remains required for any action that could affect production, users, records, notifications, infrastructure, or benchmark scoring.

## Deployment Phases

Phase 1: local read-only demo review.
Phase 2: static artifact review.
Phase 3: container packaging review.
Phase 4: Cloud Run read-only preview after approval.
Phase 5: provider and connector design review.
Phase 6: controlled integration pilot after approval.

## Sprint 6 Inputs

docs/EAIOS_2_SPRINT_6_QUICKSTART.md
src/eaios/sprint6/demo_package.py
src/eaios/sprint6/local_cli.py
src/eaios/sprint6/artifact_export_plan.py
src/eaios/sprint6/static_review_page.py
src/eaios/sprint6/portfolio_walkthrough.py

## Closeout Statement

This GCP deployment design makes cloud readiness explicit without creating cloud resources.

It preserves read-only packaging, human review, provider gating, connector gating, secret gating, and benchmark isolation.
