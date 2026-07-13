# EAIOS ? Enterprise AI Operating System

EAIOS is a governed enterprise AI operating-system pattern for coordinating AI agents, skills, tools, humans, workflows, data, knowledge, context, governance, observability, and feedback around business outcomes.

This repository demonstrates EAIOS through an interview-ready application-health demo using synthetic ITIL/AIOps data and real enterprise integration architecture.

## Current Portfolio Status

Interview-ready demo package.

The repository is ready to explain governed enterprise AI orchestration in interviews.

It is not a production deployment.

It is not connected to production systems.

It does not execute autonomous remediation.

## Core Idea

Most agent demos try to prove an agent can act.

EAIOS proves the enterprise can decide when an agent must not act.

That is the difference between automation and governed enterprise AI.

## Operating Model

Business Outcome ? Capability ? Skill ? Agent / Human / Tool / Workflow ? Data + Knowledge + Context ? Governance + Observability + Feedback

The demo starts with a business outcome:

Maintain Application Health

From there, EAIOS models how enterprise AI can reason over application-health signals while preserving safety, approval, auditability, and benchmark isolation.

## Demo Summary

The demo uses a synthetic application-health scenario.

It represents an enterprise operating context with incident-like records, alert-like records, telemetry-like observations, knowledge evidence, known-error patterns, business-impact context, recommendation context, operational confidence context, and human approval boundaries.

The centerpiece behavior is the HIGH evidence / LOW operational confidence split.

HIGH evidence means the evidence is coherent enough to support a hypothesis.

LOW operational confidence means the system still lacks enough validation to act safely.

The system refuses to over-trust itself.

## What Is Real

The following are real design artifacts in this repository:

- governed architecture
- deterministic tests
- evidence-fusion semantics
- operational confidence model
- provider request and response schema
- provider output validator
- MCP connector inventory schema
- MCP connector permission classifier
- audit event envelope
- human approval workflow
- demo release checklist
- operator demo command
- static demo export model
- interview storyboard
- real and synthetic data map
- interview walkthrough script

## What Is Synthetic

The demo data is synthetic.

Synthetic data represents enterprise-shaped ITIL/AIOps operating signals.

Synthetic data is used to keep the demo safe, repeatable, private, and benchmark-controlled.

## What Is Not Connected

The repository does not connect to:

- real ServiceNow
- real BigPanda
- real Dynatrace
- real SAP SolMan
- real CMDB or service graph
- real Solution 360 or BSI platform
- real AI provider runtime
- real MCP connector runtime
- real cloud deployment
- real notification channel
- real remediation system

## Future Real Enterprise Mapping

The architecture is designed to map to real enterprise systems later.

| Demo Concept | Future Enterprise Source |
|---|---|
| Synthetic incident | ServiceNow Incident |
| Synthetic problem cluster | ServiceNow Problem |
| Synthetic alert | BigPanda or event-correlation platform |
| Synthetic telemetry | Dynatrace or observability platform |
| Synthetic SAP signal | SAP SolMan |
| Synthetic topology | CMDB or service graph |
| Synthetic business impact | Solution 360 or BSI-style context |
| Synthetic knowledge | Knowledge base, runbook, or wiki |
| Synthetic approval gate | CAB or AIAB-style review |

## Safety Posture

EAIOS is review-only in the current demo.

The following remain blocked:

- production data connection
- real provider execution
- real MCP connector execution
- production writes
- notification sending
- remediation execution
- cloud deployment
- release creation
- benchmark truth updates from runtime output
- autonomous remediation
- bypassing human review


## EAIOS 2 Sprint 3 Demo

Legacy Sprint 3 closeout: docs/EAIOS_2_SPRINT_3_CLOSEOUT.md

Sprint 3 established the earlier EAIOS 2 demo package and UI planning foundation.

That work remains part of the portfolio history and is preserved as a legacy milestone beneath the current Sprint 8 interview-ready positioning.

## Sprint Milestones

### Sprint 4 ? Benchmark-Grounded Governed AIOps

Established synthetic ITIL/AIOps data, benchmark isolation, governed evidence, and application-health scenario semantics.

### Sprint 5 ? Operator Experience and Cloud Readiness

Added operator review surfaces, scenario commands, provider seams, MCP connector harness concepts, and GCP readiness posture.

### Sprint 6 ? Portfolio Readiness

Added local demo packaging, CLI contract, dry-run export plan, quickstart, static review design, portfolio walkthrough, GCP deployment design, provider integration design, MCP connector permission model, and closeout.

### Sprint 7 ? Controlled Runtime Hardening

Added container packaging contract, local web review surface, cloud deploy preflight, provider schema and validator, MCP connector inventory and classifier, audit event envelope, human approval workflow, demo release checklist, and closeout.

### Sprint 8 ? Interview Demo Readiness

Added canonical operator demo command, static demo export model, demo storyboard, real and synthetic data map, interview walkthrough script, and closeout.

## Interview Artifacts

Key Sprint 8 interview artifacts:

- docs/EAIOS_2_SPRINT_8_DEMO_STORYBOARD.md
- docs/EAIOS_2_SPRINT_8_REAL_SYNTHETIC_DATA_MAP.md
- docs/EAIOS_2_SPRINT_8_INTERVIEW_WALKTHROUGH.md
- docs/EAIOS_2_SPRINT_8_CLOSEOUT.md

Key Sprint 7 hardening artifacts:

- docs/EAIOS_2_SPRINT_7_CLOSEOUT.md
- src/eaios/sprint7/provider_output_validator.py
- src/eaios/sprint7/mcp_connector_inventory_schema.py
- src/eaios/sprint7/mcp_connector_permission_classifier.py
- src/eaios/sprint7/audit_event_envelope.py
- src/eaios/sprint7/human_approval_workflow.py
- src/eaios/sprint7/demo_release_checklist.py

## Running Tests

Run a focused Sprint 8 test:

    python -m pytest tests/test_sprint8_operator_demo_command.py --basetemp .pytest_tmp

Run the full suite:

    python -m pytest --basetemp .pytest_tmp

## Interview Walkthrough

A 5-minute walkthrough should cover:

1. Business outcome: Maintain Application Health.
2. Synthetic ITIL/AIOps scenario.
3. Evidence, reasoning, and recommendation.
4. HIGH evidence / LOW operational confidence.
5. Human approval requirement.
6. Blocked provider, connector, cloud, release, notification, remediation, and benchmark-update actions.
7. Future real enterprise integration path.

A 15-minute walkthrough should additionally cover:

- outcome-to-capability operating model
- synthetic-to-real data mapping
- governed evidence semantics
- provider output validation
- MCP connector inventory and permissioning
- audit event envelope
- human approval workflow
- release checklist
- cloud review gate

## Cloud Deployment Status

Cloud deployment is intentionally deferred.

Before cloud deployment, the project requires a cloud review gate covering what is deployed, what remains static and read-only, whether providers remain disabled, whether MCP connectors remain disabled, whether secrets are required, IAM boundary, cost boundary, benchmark truth isolation, human approval boundary, and rollback or disable plan.

## Non-Claims

This repository does not claim production deployment, real cloud runtime, real production data integration, real ServiceNow execution, real BigPanda execution, real Dynatrace execution, real SAP SolMan execution, real provider execution, real MCP connector execution, autonomous remediation, production writes, production notifications, or benchmark truth updates from runtime output.

## Final Positioning

EAIOS is synthetic in demo data execution and real in enterprise architecture.

It is designed to show how agentic AI can be made governable, observable, auditable, permissioned, human-approved, and safe before production integration.


## Sprint 3 Legacy Compatibility References

These references preserve legacy Sprint 3 README expectations while Sprint 9 updates the main portfolio positioning.

- docs/EAIOS_2_SPRINT_3_UI_DEMO_WALKTHROUGH.md
- docs/EAIOS_2_SPRINT_3_UI_ARCHITECTURE_CHECKPOINT.md
- Python owns decisions.
- Renderer owns play-head.
- Renderer must not invent replay paths.
