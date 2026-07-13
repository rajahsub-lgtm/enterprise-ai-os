# EAIOS 2 Sprint 10 Static Export Materialization Plan

## Purpose

This document defines how a possible static preview export would be assembled.

It does not create the export.

It does not write deployment files.

It does not publish a static site.

It does not create cloud resources.

It does not start a runtime.

It does not enable providers, MCP connectors, secrets, production data, writes, notifications, remediation, benchmark truth updates, release creation, or autonomous action.

The purpose is to define the materialization plan before implementation.

## Relationship To Scope Contract

This plan follows the Sprint 10 static preview scope contract.

The only allowed preview type remains:

STATIC_REVIEW_PREVIEW

The materialized export, if later approved, must display portfolio content and precomputed demo artifacts only.

It must not execute live orchestration.

## Materialization Principle

Materialize only what is already safe.

Do not create new runtime behavior.

Do not create new integration behavior.

Do not create new authority.

The static export is a presentation artifact, not an operating system runtime.

## Candidate Export Name

EAIOS_STATIC_REVIEW_PREVIEW

## Candidate Output Form

The preferred output form is a static folder containing:

- index.html
- architecture.html
- demo-storyboard.html
- real-enterprise-mapping.html
- interview-qa.html
- rehearsal-checklist.html
- cloud-gate.html
- safety-boundaries.html
- static-demo-export.json
- manifest.json

This document does not create those files.

It only defines what a later approved implementation may create.

## Source Artifact Inventory

The static export may draw from these repository artifacts:

- README.md
- docs/EAIOS_2_SPRINT_8_DEMO_STORYBOARD.md
- docs/EAIOS_2_SPRINT_8_REAL_SYNTHETIC_DATA_MAP.md
- docs/EAIOS_2_SPRINT_8_INTERVIEW_WALKTHROUGH.md
- docs/EAIOS_2_SPRINT_8_CLOSEOUT.md
- docs/EAIOS_2_SPRINT_9_ARCHITECTURE_NARRATIVE.md
- docs/EAIOS_2_SPRINT_9_REAL_ENTERPRISE_MAPPING.md
- docs/EAIOS_2_SPRINT_9_INTERVIEW_QA_PACK.md
- docs/EAIOS_2_SPRINT_9_DEMO_REHEARSAL_CHECKLIST.md
- docs/EAIOS_2_SPRINT_9_CLOUD_GATE_PRE_REVIEW.md
- docs/EAIOS_2_SPRINT_9_CLOSEOUT.md
- docs/EAIOS_2_SPRINT_10_STATIC_PREVIEW_SCOPE_CONTRACT.md
- src/eaios/sprint8/static_demo_export.py
- src/eaios/sprint8/operator_demo_command.py

## Source Artifact Rules

Each source artifact must be treated as read-only input.

The materialization process must not modify source artifacts.

The materialization process must not infer production readiness.

The materialization process must not invent live integration status.

The materialization process must preserve all non-claims and blocked action statements.

## Proposed Page Map

### index.html

Purpose:

- introduce EAIOS
- state current portfolio status
- explain synthetic execution and real enterprise architecture
- link to the rest of the preview

Required messages:

- interview-ready and review-only
- not production deployed
- no production data
- no runtime execution
- no provider calls
- no MCP connector calls
- no remediation
- human approval required

### architecture.html

Purpose:

- present the Sprint 9 architecture narrative
- explain the operating model
- explain architecture layers

Required messages:

- Business Outcome -> Capability -> Skill -> Agent / Human / Tool / Workflow -> Data + Knowledge + Context -> Governance + Observability + Feedback
- EAIOS is not just an agent demo
- enterprise AI needs an operating system, not just more agents

### demo-storyboard.html

Purpose:

- present the Sprint 8 demo storyboard
- explain the application-health demo flow

Required messages:

- Maintain Application Health
- synthetic ITIL/AIOps scenario
- HIGH evidence / LOW operational confidence
- human approval required
- autonomous action disabled

### real-enterprise-mapping.html

Purpose:

- present the Sprint 9 real enterprise mapping
- map synthetic artifacts to real systems

Required systems:

- ServiceNow
- BigPanda
- Dynatrace
- SAP SolMan
- CMDB
- Solution 360 or BSI
- enterprise knowledge systems
- AI providers
- MCP connectors
- CAB and AIAB-style approval

### interview-qa.html

Purpose:

- present interview Q&A pack
- support quick rehearsal before interview

Required topics:

- what EAIOS is
- synthetic versus real
- ServiceNow mapping
- observability mapping
- provider boundary
- MCP connector boundary
- benchmark isolation
- cloud deferral

### rehearsal-checklist.html

Purpose:

- present demo rehearsal checklist
- support 5-minute and 15-minute walkthrough practice

Required topics:

- pre-rehearsal repo check
- five-minute flow
- fifteen-minute flow
- red flags to avoid
- safe phrases
- final sound bite

### cloud-gate.html

Purpose:

- present cloud gate pre-review notes
- explain why cloud deployment remains deferred

Required topics:

- static or review-only
- providers disabled
- MCP connectors disabled
- secrets not required
- production data excluded
- IAM boundary
- cost boundary
- rollback or disable plan

### safety-boundaries.html

Purpose:

- summarize what remains blocked

Required blocked items:

- production data connection
- provider execution
- MCP connector execution
- production writes
- notifications
- remediation
- release creation
- benchmark truth updates
- autonomous action
- bypassing human approval

### static-demo-export.json

Purpose:

- include precomputed Sprint 8 static demo export view model

Required posture:

- generated locally before preview
- read-only
- no provider calls
- no MCP connector calls
- no runtime execution
- no benchmark truth mutation

### manifest.json

Purpose:

- describe static preview contents and safety posture

Required fields:

- preview_id
- preview_type
- generated_from_branch
- generated_from_commit
- source_artifacts
- generated_artifacts
- providers_enabled
- mcp_connectors_enabled
- production_data_used
- secrets_required
- runtime_enabled
- writes_enabled
- notifications_enabled
- remediation_enabled
- benchmark_truth_mutation_enabled
- autonomous_action_enabled
- human_approval_required
- rollback_required

## Materialization Steps

A future implementation may follow these steps only after approval:

1. verify git status is clean
2. verify full test suite passes
3. record current branch
4. record current commit
5. read approved source artifacts
6. render markdown into static HTML
7. generate static demo export view model locally
8. write static files to a local preview folder
9. generate manifest.json
10. verify no secrets are present
11. verify no runtime code is included
12. verify providers remain disabled
13. verify MCP connectors remain disabled
14. verify no production data is included
15. verify no benchmark truth mutation is possible
16. verify rollback or delete instructions exist

## Materialization Non-Steps

The materialization process must not:

- deploy to cloud
- start a local server
- open a browser automatically
- call providers
- call MCP connectors
- read production data
- write production data
- send notifications
- execute remediation
- create release approval
- mutate benchmark truth
- enable autonomous action
- create secrets
- require credentials

## Validation Checklist

Before any generated static export is considered review-ready, confirm:

- all generated files are static
- generated files contain no secrets
- generated files contain no production data
- generated files contain no executable remediation controls
- generated files contain no connector endpoints
- generated files contain no provider credentials
- generated files preserve non-claims
- generated files preserve human approval requirement
- generated files preserve benchmark isolation
- generated manifest says providers_enabled = false
- generated manifest says mcp_connectors_enabled = false
- generated manifest says runtime_enabled = false
- generated manifest says autonomous_action_enabled = false

## Approval Boundary

This plan does not approve materialization.

A later Sprint 10 implementation slice may materialize local static files only after this plan and the scope contract remain green under tests.

A separate approval checklist is still required before cloud deployment.

## Interview Explanation

The safe explanation is:

Sprint 10 is still review-first. This plan defines how a static preview could be assembled from approved documentation and precomputed demo output, but it does not deploy anything or enable runtime behavior.

## Final Sound Bite

Static export materialization should package the story.

It should not change the system.
