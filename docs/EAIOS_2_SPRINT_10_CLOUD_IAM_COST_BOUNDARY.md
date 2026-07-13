# EAIOS 2 Sprint 10 Cloud IAM and Cost Boundary Model

## Purpose

This document defines the IAM and cost boundaries for a possible future EAIOS static cloud preview.

It does not approve deployment.

It does not create cloud resources.

It does not create IAM roles.

It does not create service accounts.

It does not configure billing.

It does not enable providers, MCP connectors, secrets, production data, writes, notifications, remediation, benchmark truth updates, release creation, or autonomous action.

The purpose is to define the minimum acceptable IAM and cost posture before any preview deployment is considered.

## Sprint 10 Position

Sprint 10 remains a cloud preview review sprint.

The preferred preview remains static-only.

Any preview must preserve the local review-only safety posture.

## Boundary Principle

The cloud preview should require the least possible authority and the lowest predictable cost.

If a static preview can be served without operational runtime permissions, no runtime permissions should be granted.

If a static preview can be served without secrets, no secrets should exist.

If a static preview can be served without provider or connector access, those access paths must remain disabled.

## Preview Assumption

The assumed preview type is:

STATIC_REVIEW_PREVIEW

The preview may display static documentation and precomputed demo artifacts.

The preview must not run EAIOS orchestration.

The preview must not call providers.

The preview must not call MCP connectors.

The preview must not read production data.

The preview must not write production data.

The preview must not send notifications.

The preview must not execute remediation.

## IAM Scope Model

The preferred IAM model is static hosting only.

The model should avoid:

- broad administrator roles
- production system access
- provider execution roles
- MCP connector execution roles
- database write roles
- notification sending roles
- remediation execution roles
- secrets administration roles
- benchmark mutation roles
- background job execution roles

The model may allow only the minimum permissions required to host static content if a preview is later approved.

## Identity Boundary

Any future preview identity must have a documented purpose.

Required identity metadata:

- identity name
- identity owner
- business owner
- technical owner
- purpose
- allowed operations
- blocked operations
- expiration or review date
- rollback or disable owner

No identity should be created during Sprint 10 review slices.

This document only defines the boundary.

## Allowed IAM Capabilities

A future static preview may need only:

- read access to static preview artifacts
- serve access for static content
- basic logging for access or hosting status
- delete or disable ability for rollback

Even these capabilities require explicit approval before implementation.

## Disallowed IAM Capabilities

A future static preview must not have:

- production ITSM access
- ServiceNow write access
- BigPanda API access
- Dynatrace API access
- SAP SolMan access
- CMDB write access
- Solution 360 or BSI write access
- AI provider invocation access
- MCP connector invocation access
- secret manager read access
- notification sending permission
- remediation execution permission
- benchmark truth write permission
- broad project administrator access
- unrestricted network administration

## Secrets Boundary

The static preview should require no secrets.

The preview must not require:

- API keys
- passwords
- bearer tokens
- service account keys
- OAuth client secrets
- webhook secrets
- connector credentials
- provider credentials
- database credentials

If a future implementation requires a secret, it is no longer within the default static preview posture and must be reviewed separately.

## Network Access Boundary

The static preview should not require outbound calls.

Disallowed network dependencies:

- production ServiceNow endpoint
- production BigPanda endpoint
- production Dynatrace endpoint
- production SAP SolMan endpoint
- production CMDB endpoint
- production Solution 360 or BSI endpoint
- AI provider endpoint
- MCP connector endpoint
- notification endpoint
- remediation endpoint
- private enterprise network endpoint

## Cost Boundary

The preview must be cost bounded.

Preferred posture:

- static hosting only
- no always-on compute runtime
- no background worker
- no scheduled job
- no database
- no vector store
- no provider invocation cost
- no connector invocation cost
- no high-volume logging
- no autoscaling runtime
- no production data transfer

The cost model should be predictable before deployment.

## Required Cost Metadata

Before any preview deployment, document:

- expected monthly cost
- maximum monthly cost
- cost owner
- billing project or account
- resource types
- scale limits
- storage limits
- logging limits
- shutdown date or review date
- disable plan
- cost alert threshold

## Cost Stop Conditions

The preview should be disabled or reviewed if:

- cost exceeds approved threshold
- unexpected runtime cost appears
- provider usage cost appears
- connector usage cost appears
- database cost appears
- network egress cost appears
- logging cost exceeds approved limit
- owner cannot be identified
- rollback path is unclear

## Logging Boundary

Logging should be minimal and non-sensitive.

Allowed logs:

- static preview access status
- static hosting health
- deployment metadata after approval
- rollback or disable events

Disallowed logs:

- production incidents
- production alerts
- production telemetry
- production traces
- production logs
- production knowledge content
- credentials
- secrets
- provider prompts
- connector payloads
- personal data
- confidential enterprise data

## Runtime Cost Boundary

The default approved posture should be no runtime.

If runtime is proposed later, it must be reviewed separately.

Runtime proposals must answer:

- why static hosting is insufficient
- what code runs
- what triggers execution
- what data is read
- what systems are called
- what costs are created
- how execution is disabled
- how human approval is preserved
- how benchmark truth remains isolated

## Provider Cost Boundary

Provider cost must be zero for the static preview.

Providers remain disabled.

Any future provider cost requires separate approval and must include:

- provider purpose
- task scope
- invocation limits
- cost estimate
- cost ceiling
- logging posture
- data boundary
- human review posture
- disable path

## MCP Connector Cost Boundary

MCP connector cost must be zero for the static preview.

MCP connectors remain disabled.

Any future connector-related cost requires separate approval and must include:

- connector purpose
- allowed operations
- blocked operations
- owner
- permission class
- audit posture
- cost estimate
- disable path

## Benchmark Cost Boundary

Benchmark truth remains isolated and should not create preview runtime cost.

The static preview may display benchmark-isolation explanation.

The preview must not run benchmark scoring.

The preview must not update benchmark truth.

The preview must not create a benchmark authority.

## Approval Criteria

The IAM and cost boundary is acceptable only if:

- no production system access is required
- no secrets are required
- providers remain disabled
- MCP connectors remain disabled
- no write permissions are granted
- no notification permissions are granted
- no remediation permissions are granted
- no benchmark mutation permissions are granted
- cost is predictable
- cost owner is documented
- cost stop conditions are documented
- rollback or disable owner is documented
- least privilege is preserved

## Explicit Non-Approval

This document does not approve deployment.

This document does not approve IAM creation.

This document does not approve billing configuration.

This document defines the boundary that a later approval checklist must evaluate.

## Interview Explanation

The safe explanation is:

Before any cloud preview, I would define the IAM and cost boundary. For the first preview, the target is static hosting only: no secrets, no providers, no MCP connectors, no production data, no writes, no notifications, no remediation, bounded cost, and a documented rollback path.

## Final Sound Bite

Cloud preview authority should be smaller than the demo story.

The preview should show EAIOS, not become a new uncontrolled runtime.
