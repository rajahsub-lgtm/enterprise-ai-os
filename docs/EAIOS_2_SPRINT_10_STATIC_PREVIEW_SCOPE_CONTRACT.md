# EAIOS 2 Sprint 10 Static Preview Scope Contract

## Purpose

This document defines the approved scope for a possible static cloud preview of EAIOS.

It does not approve deployment.

It does not create cloud resources.

It does not enable a runtime.

It does not enable providers, MCP connectors, secrets, production data, writes, notifications, remediation, benchmark truth updates, release creation, or autonomous action.

The purpose is to define what a safe static preview may include before any implementation decision.

## Sprint 10 Position

Sprint 10 is a cloud preview review sprint.

It is not an automatic deployment sprint.

The first Sprint 10 decision is scope control.

## Preview Type

The only preview type considered by this contract is:

STATIC_REVIEW_PREVIEW

A static review preview may display portfolio content and precomputed demo artifacts.

It must not execute live orchestration.

It must not start an agent runtime.

It must not call external APIs.

It must not require secrets.

It must not connect to production systems.

## Allowed Preview Content

The static preview may include:

- README content
- Sprint 8 demo storyboard
- Sprint 8 real and synthetic data map
- Sprint 8 interview walkthrough
- Sprint 8 closeout
- Sprint 9 architecture narrative
- Sprint 9 real enterprise mapping
- Sprint 9 interview Q&A pack
- Sprint 9 demo rehearsal checklist
- Sprint 9 cloud gate pre-review notes
- Sprint 9 closeout
- precomputed static demo export
- precomputed operator demo command output
- static explanation of blocked actions
- static explanation of human approval
- static explanation of benchmark isolation
- static explanation of provider and MCP connector disabled posture

## Disallowed Preview Content

The static preview must not include:

- production data
- real ServiceNow records
- real BigPanda alerts
- real Dynatrace telemetry
- real SAP SolMan signals
- real CMDB data
- real Solution 360 or BSI records
- secrets or credentials
- real provider prompts or responses
- real MCP connector responses
- production approval records
- production notification content
- production remediation output
- mutable benchmark truth
- executable remediation controls
- executable connector controls
- executable provider controls
- runtime deployment controls

## Runtime Boundary

The static preview must not run the EAIOS runtime.

It may display precomputed artifacts.

It may display static documentation.

It may display static JSON-like view models that were generated locally before deployment.

It must not perform live reasoning, live retrieval, live evidence fusion, live provider validation, live connector classification, live approval persistence, live audit persistence, or live release creation.

## Provider Boundary

Providers remain disabled.

The static preview may describe provider validation.

The static preview may display provider schema documentation.

The static preview may display provider disabled-state posture.

The static preview must not call a provider.

The static preview must not store provider credentials.

The static preview must not simulate a real provider as if it were live.

## MCP Connector Boundary

MCP connectors remain disabled.

The static preview may describe MCP connector inventory and permission classification.

The static preview may display connector disabled-state posture.

The static preview must not call a connector.

The static preview must not store connector credentials.

The static preview must not expose connector endpoints.

The static preview must not simulate a real connector as if it were live.

## Data Boundary

Allowed data classes:

- repository documentation
- synthetic demo data
- precomputed local demo output
- static architecture explanation
- static safety explanation
- static review checklist content

Disallowed data classes:

- production incidents
- production alerts
- production telemetry
- production logs
- production traces
- production knowledge exports
- production topology exports
- production business-impact exports
- production approval records
- credentials
- secrets
- personal data
- confidential enterprise data

## Security Boundary

The static preview must require no secrets.

The static preview must not contain:

- api keys
- passwords
- bearer tokens
- service account keys
- connector credentials
- provider credentials
- webhook URLs
- production hostnames
- internal endpoint details

## IAM Boundary

The preferred preview model requires no operational IAM beyond static hosting.

If IAM is required, it must be least privilege.

IAM must not include:

- production system access
- connector execution roles
- provider execution roles
- remediation roles
- notification sending roles
- write permissions to operational systems
- broad administrator roles

## Network Boundary

The static preview should not require outbound network calls.

It should not depend on:

- provider endpoints
- MCP connector endpoints
- production system endpoints
- notification endpoints
- remediation endpoints
- private enterprise network access

## Benchmark Boundary

Benchmark truth remains isolated.

The static preview may explain benchmark isolation.

The static preview must not create, modify, infer, or overwrite benchmark truth.

Static export output, preview output, approval output, audit output, release output, provider output, and connector output must not define benchmark truth.

## Human Approval Boundary

Human approval remains required.

The static preview may display human approval posture.

The static preview must not approve actions.

The static preview must not persist approval records.

The static preview must not execute any action after approval.

## Cost Boundary

The static preview must be cost bounded.

Preferred cost posture:

- static hosting only
- no always-on runtime
- no provider usage cost
- no connector usage cost
- no database cost unless separately reviewed
- no background workers
- no scheduled jobs
- no autoscaling runtime

## Rollback Boundary

A static preview must have a disable plan before deployment.

The disable plan must define:

- who owns rollback
- how to disable access
- how to stop serving the preview
- how to remove preview artifacts
- how to confirm removal
- expected rollback time

## Scope Approval Criteria

The static preview scope is acceptable only if:

- it is static or review-only
- it does not run EAIOS runtime orchestration
- it does not use production data
- it does not require secrets
- providers remain disabled
- MCP connectors remain disabled
- writes remain disabled
- notifications remain disabled
- remediation remains disabled
- autonomous action remains disabled
- benchmark truth remains isolated
- human approval remains required
- rollback is documented
- cost is bounded
- IAM is minimal

## Explicit Non-Approval

This contract does not approve deployment.

This contract only defines the scope that a later deployment approval checklist may evaluate.

A separate approval checklist is required before any cloud preview implementation.

## Interview Explanation

The safe explanation is:

Sprint 10 begins by defining the static preview scope before deploying anything. The preview, if approved later, would show documentation and precomputed demo artifacts only. It would not run agents, call providers, call MCP connectors, use production data, write records, send notifications, remediate, or update benchmark truth.

## Final Sound Bite

Static preview means show the governed architecture.

It does not mean run the enterprise AI system in the cloud.
