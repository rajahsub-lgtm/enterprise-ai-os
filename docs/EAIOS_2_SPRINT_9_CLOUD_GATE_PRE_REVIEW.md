# EAIOS 2 Sprint 9 Cloud Gate Pre-Review Notes

## Purpose

This document defines the pre-review gate that must be completed before any EAIOS cloud preview.

It does not approve cloud deployment.

It does not create cloud resources.

It does not enable providers, MCP connectors, secrets, writes, notifications, remediation, benchmark truth updates, or autonomous action.

The purpose is to make the cloud decision reviewable before any deployment step.

## Current Decision

Cloud deployment is deferred.

The current EAIOS portfolio is interview-ready and review-only.

A future cloud preview may be considered only after this gate confirms the exact scope, boundaries, risks, controls, and rollback plan.

## Cloud Review Principle

Do not deploy because the demo is impressive.

Deploy only if the cloud preview preserves the same safety posture as the local interview demo.

The cloud preview must remain:

- static or review-only
- provider-disabled
- connector-disabled
- write-disabled
- notification-disabled
- remediation-disabled
- benchmark-isolated
- human-approval-required
- rollback-ready
- cost-bounded
- IAM-bounded
- audit-ready

## Allowed Cloud Preview Scope

A future cloud preview may include:

- static documentation
- static portfolio pages
- static architecture narrative
- static interview walkthrough
- static real enterprise mapping
- static Q&A pack
- static demo rehearsal checklist
- static generated demo export
- read-only display of precomputed demo artifacts

A cloud preview should not include live reasoning, live provider calls, live connector calls, live remediation, live notifications, production data access, or benchmark truth mutation.

## Disallowed Cloud Preview Scope

The cloud preview must not include:

- production data connection
- real ServiceNow execution
- real BigPanda execution
- real Dynatrace execution
- real SAP SolMan execution
- real CMDB execution
- real Solution 360 execution
- real AI provider execution
- real MCP connector execution
- production writes
- production notifications
- production remediation
- autonomous action
- benchmark truth updates from runtime output
- release creation without approval

## Deployment Candidate

Preferred candidate for an initial cloud preview:

Static review site only.

The static review site should expose portfolio content and precomputed demo output.

It should not start an agent runtime.

It should not call external APIs.

It should not require secrets.

It should not write to any external system.

It should not imply production readiness.

## Provider Gate

Providers remain disabled by default.

Before any provider is enabled, the review must confirm:

- provider purpose
- provider owner
- provider risk tier
- allowed prompts or tasks
- disallowed prompts or tasks
- schema validation
- evidence reference validation
- unsupported action checks
- unsafe certainty checks
- benchmark truth claim checks
- benchmark scoring checks
- remediation instruction checks
- notification instruction checks
- secret leakage checks
- human review checks
- logging and audit posture

For Sprint 9, provider execution remains out of scope.

## MCP Connector Gate

MCP connectors remain disabled by default.

Before any connector is enabled, the review must confirm:

- connector id
- connector purpose
- business owner
- technical owner
- data owner
- data classification
- permission class
- allowed operations
- blocked operations
- audit events
- approval boundary
- release gate
- rollback or disable switch
- read-only first posture

For Sprint 9, MCP connector execution remains out of scope.

## Data Gate

The cloud preview must not use production data.

Allowed data:

- static docs
- synthetic demo data
- precomputed demo output
- generated static export
- non-sensitive architecture narrative

Disallowed data:

- production incidents
- production alerts
- production telemetry
- production logs
- production traces
- production knowledge exports
- production CMDB exports
- production business-impact records
- production approval records
- credentials
- personal data
- confidential enterprise data

## IAM Gate

Before cloud preview, IAM scope must be minimal.

Required posture:

- least privilege
- no broad admin role
- no production system access
- no connector execution role
- no remediation execution role
- no notification sending role
- no write permission to operational systems
- separate deployment identity if needed
- documented owner
- documented disable path

## Network Gate

The initial preview should not require outbound calls to enterprise systems.

Required posture:

- no production network dependency
- no connector endpoint dependency
- no provider endpoint dependency
- no notification endpoint dependency
- no remediation endpoint dependency
- no private enterprise network dependency

If network access is later required, it must be reviewed separately.

## Cost Gate

A cloud preview must have a bounded cost posture.

The review should define:

- expected monthly cost
- maximum acceptable monthly cost
- resource types
- scale limits
- logging limits
- storage limits
- shutdown plan
- owner responsible for cost review

A static preview is preferred because it keeps cost predictable.

## Audit Gate

The preview should be auditable even if it is static.

The review should capture:

- what was deployed
- when it was deployed
- who approved it
- what artifacts were included
- what capabilities were disabled
- what data was included
- what external calls were blocked
- rollback or disable instructions

## Benchmark Gate

Benchmark truth remains isolated.

The cloud preview must not create, modify, infer, or overwrite benchmark truth.

The cloud preview may display benchmark-related explanation, but it must not become a benchmark authority.

Runtime output, provider output, connector output, approval output, audit output, release output, and static export output must not define benchmark truth.

## Human Approval Gate

Human approval remains required.

The cloud preview must not weaken the local demo posture.

Any recommendation shown in the preview remains a proposal.

No action should be executable from the preview.

## Rollback or Disable Gate

Before any cloud preview, there must be a simple disable plan.

The plan should include:

- how to disable access
- how to stop serving the preview
- how to remove deployed artifacts
- who owns rollback
- expected rollback time
- how to confirm rollback is complete

## Review Questions

Before cloud deployment, answer:

1. What exactly is being deployed?
2. Is it static or runtime-enabled?
3. Does it require secrets?
4. Does it call any provider?
5. Does it call any MCP connector?
6. Does it read production data?
7. Does it write production data?
8. Does it send notifications?
9. Does it execute remediation?
10. Does it update benchmark truth?
11. Is human approval still required?
12. What IAM roles are required?
13. What network access is required?
14. What is the cost boundary?
15. What is the rollback or disable plan?

## Required Approval Before Deployment

A cloud preview should not proceed until the review confirms:

- deployment scope is static or review-only
- providers remain disabled
- MCP connectors remain disabled
- secrets are not required
- production data is not used
- writes are disabled
- notifications are disabled
- remediation is disabled
- autonomous action is disabled
- benchmark truth remains isolated
- human approval remains required
- IAM is least privilege
- cost is bounded
- rollback or disable path is documented

## Sprint 9 Recommendation

Do not deploy yet.

Complete Sprint 9 portfolio polish first.

Then review whether a Sprint 10 static cloud preview is worth doing.

If Sprint 10 proceeds, the first preview should be static-only and should preserve every current safety boundary.

## Interview Explanation

The safe interview explanation is:

Cloud deployment is intentionally deferred. I want the portfolio to be interview-ready first, then I would run a cloud review gate covering static scope, provider and connector status, secrets, IAM, cost, benchmark isolation, human approval, and rollback before any preview deployment.

## Final Sound Bite

Cloud is not the milestone.

Governed readiness is the milestone.

A cloud preview should preserve the enterprise safety model, not bypass it.
