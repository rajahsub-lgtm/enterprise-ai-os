# EAIOS 2 Sprint 10 Rollback and Disable Plan

## Purpose

This document defines the rollback and disable plan required before any future EAIOS static cloud preview.

It does not approve deployment.

It does not create cloud resources.

It does not disable any live resource.

It does not create runtime behavior.

It does not enable providers, MCP connectors, secrets, production data, writes, notifications, remediation, benchmark truth updates, release creation, or autonomous action.

The purpose is to ensure that any future preview can be stopped, removed, or disabled safely.

## Sprint 10 Position

Sprint 10 remains a cloud preview review sprint.

Rollback planning must happen before deployment planning.

A preview is not safe to approve unless the disable path is clear.

## Rollback Principle

If we cannot turn it off safely, we should not turn it on.

A cloud preview must be reversible, bounded, owned, and auditable.

For the first preview, rollback should be simple because the preferred preview is static-only.

## Preview Assumption

The assumed preview type is:

STATIC_REVIEW_PREVIEW

The preview may display static documentation and precomputed demo artifacts only.

The preview must not run EAIOS orchestration.

The preview must not call providers.

The preview must not call MCP connectors.

The preview must not read production data.

The preview must not write production data.

The preview must not send notifications.

The preview must not execute remediation.

## Rollback Scope

Rollback means disabling or removing the preview.

Rollback does not include:

- reversing production writes
- reversing remediation
- revoking provider actions
- revoking MCP connector actions
- restoring benchmark truth
- reversing notification side effects

Those actions should not be possible in the static preview.

The rollback plan exists to disable the preview surface and remove preview artifacts.

## Required Rollback Metadata

Before any preview deployment, document:

- preview id
- preview type
- deployment owner
- rollback owner
- business owner
- technical owner
- deployed branch
- deployed commit
- deployed artifact list
- deployment location
- public or private access posture
- disable method
- artifact removal method
- expected rollback time
- validation method
- escalation path

## Disable Triggers

The preview must be disabled or reviewed if:

- unexpected runtime behavior appears
- provider call is detected
- MCP connector call is detected
- production data appears
- secret appears
- credential appears
- production write path appears
- notification path appears
- remediation path appears
- benchmark truth mutation path appears
- autonomous action path appears
- cost exceeds approved threshold
- IAM scope exceeds approved boundary
- network access exceeds approved boundary
- owner cannot be identified
- rollback procedure fails

## Disable Methods

Allowed disable methods may include:

- remove static hosting route
- disable static site serving
- remove preview artifact folder
- revoke preview access
- disable preview identity
- remove preview storage object
- remove DNS or routing entry if applicable
- disable deployment pipeline if applicable

This plan does not execute those methods.

It only defines what the approved implementation must document.

## Artifact Removal Requirements

Artifact removal must identify:

- generated static HTML files
- generated JSON view models
- manifest file
- static assets
- deployment metadata
- hosting configuration
- access configuration

Artifact removal must not affect source repository history.

Artifact removal must not delete source documentation.

Artifact removal must not delete benchmark fixtures.

Artifact removal must not delete local development files outside the approved preview output.

## Access Disable Requirements

Access disable must confirm:

- preview URL no longer serves content
- preview route is removed or disabled
- preview identity is disabled if created
- preview storage is removed or inaccessible
- preview permissions are revoked
- no public access remains if public access was used
- no private access remains if private access was used

## Validation Requirements

Rollback is complete only when validation confirms:

- preview is not reachable
- preview artifacts are removed or inaccessible
- no runtime exists
- no provider access exists
- no MCP connector access exists
- no secrets exist
- no production data exists
- no write permissions exist
- no notification permissions exist
- no remediation permissions exist
- no benchmark truth mutation permissions exist
- no autonomous action permissions exist
- cost-generating resources are stopped or removed

## Rollback Evidence

Rollback evidence should include:

- rollback timestamp
- rollback owner
- rollback reason
- artifacts removed
- access disabled
- identities disabled
- resources stopped or removed
- validation result
- remaining known risks
- follow-up actions

## Emergency Disable

Emergency disable should be allowed when a critical boundary is violated.

Critical boundary violations include:

- secret exposure
- production data exposure
- production write capability
- provider execution
- MCP connector execution
- notification execution
- remediation execution
- benchmark truth mutation
- autonomous action capability

Emergency disable should favor safety over availability.

## Owner Responsibilities

The deployment owner is responsible for ensuring the preview matches the approved scope.

The rollback owner is responsible for disabling or removing the preview.

The business owner is responsible for confirming whether the preview should remain available.

The technical owner is responsible for confirming that access, IAM, network, cost, and artifact boundaries remain valid.

## Rollback Time Objective

The default rollback time objective for a static preview should be short.

Target posture:

- disable access quickly
- remove artifacts after access is disabled
- validate no runtime remains
- validate no cost-generating resources remain
- document completion

A precise time target must be defined before any real preview deployment.

## Cost Shutdown

Rollback must stop cost-generating resources.

For a static preview, cost shutdown should include:

- disabling hosting if needed
- removing storage if needed
- stopping deployment pipeline if needed
- disabling logs if needed
- confirming no runtime cost
- confirming no provider cost
- confirming no connector cost
- confirming no database cost

## IAM Shutdown

Rollback must remove or disable unnecessary access.

IAM shutdown should confirm:

- no production access
- no provider invocation access
- no MCP connector invocation access
- no notification permission
- no remediation permission
- no benchmark truth write permission
- no broad admin permission
- no unused preview identity remains active

## Benchmark Protection

Rollback must preserve benchmark truth isolation.

Rollback must not:

- modify benchmark fixtures
- overwrite benchmark truth
- generate new benchmark truth
- treat preview output as benchmark authority
- treat rollback output as benchmark authority

## Human Approval Protection

Rollback must preserve human approval boundaries.

The preview must not allow actions before rollback.

The rollback process must not create approvals retroactively.

The rollback process must not persist approval records to a production system.


## Benchmark and Human Approval Exact Safeguards

Rollback must preserve benchmark truth isolation.

Rollback must not modify benchmark fixtures.

Rollback must not overwrite benchmark truth.

Rollback must not generate new benchmark truth.

Rollback must not treat preview output as benchmark authority.

Rollback must not treat rollback output as benchmark authority.

Rollback must preserve human approval boundaries.

Rollback must not create approvals retroactively.

Rollback must not persist approval records to a production system.

## Explicit Non-Approval

This rollback plan does not approve deployment.

This rollback plan does not approve implementation.

This rollback plan defines a required safety condition for any later preview approval.

A separate static cloud preview approval checklist is required before deployment.

## Interview Explanation

The safe explanation is:

Before deploying even a static preview, I would define the rollback and disable path. If the preview ever violates scope, exposes data, requires unexpected IAM, creates unexpected cost, or shows runtime behavior, it should be disabled quickly and validated as removed.

## Final Sound Bite

A safe preview is not just something we can show.

It is something we can turn off.
