# EAIOS 2 Sprint 9 Demo Rehearsal Checklist

## Purpose

This checklist prepares the EAIOS portfolio for interview rehearsal.

It helps confirm that the demo story, repo state, test state, safety posture, non-claims, and talk track are ready before an interview.

## Rehearsal Goal

Be able to explain EAIOS clearly in 5 minutes, expand it in 15 minutes, and answer likely follow-up questions without overclaiming production readiness.

## Current Position

EAIOS is interview-ready and review-only.

The demo uses synthetic ITIL/AIOps data.

The architecture maps to real enterprise systems.

The current repo does not connect to production systems, execute provider calls, execute MCP connector calls, deploy cloud resources, send notifications, perform remediation, write production records, or update benchmark truth from runtime output.

## Pre-Rehearsal Repo Check

Before rehearsal, confirm:

- current branch is sprint-9-portfolio-polish
- git status is clean
- full pytest suite passes
- Sprint 8 artifacts exist
- Sprint 9 portfolio artifacts exist
- README reflects interview-ready positioning
- no untracked demo artifacts are accidentally present
- no secrets or credentials are present

## Test Commands

Focused Sprint 9 tests:

    python -m pytest tests/test_sprint9_readme_refresh.py --basetemp .pytest_tmp
    python -m pytest tests/test_sprint9_architecture_narrative.py --basetemp .pytest_tmp
    python -m pytest tests/test_sprint9_real_enterprise_mapping.py --basetemp .pytest_tmp
    python -m pytest tests/test_sprint9_interview_qa_pack.py --basetemp .pytest_tmp

Full test suite:

    python -m pytest --basetemp .pytest_tmp

## Required Artifacts

Sprint 8 artifacts:

- docs/EAIOS_2_SPRINT_8_DEMO_STORYBOARD.md
- docs/EAIOS_2_SPRINT_8_REAL_SYNTHETIC_DATA_MAP.md
- docs/EAIOS_2_SPRINT_8_INTERVIEW_WALKTHROUGH.md
- docs/EAIOS_2_SPRINT_8_CLOSEOUT.md
- src/eaios/sprint8/operator_demo_command.py
- src/eaios/sprint8/static_demo_export.py

Sprint 9 artifacts:

- README.md
- docs/EAIOS_2_SPRINT_9_ARCHITECTURE_NARRATIVE.md
- docs/EAIOS_2_SPRINT_9_REAL_ENTERPRISE_MAPPING.md
- docs/EAIOS_2_SPRINT_9_INTERVIEW_QA_PACK.md
- docs/EAIOS_2_SPRINT_9_DEMO_REHEARSAL_CHECKLIST.md

## Five-Minute Rehearsal Flow

### 0:00 ? Open

EAIOS is a governed enterprise AI operating-system pattern.

It coordinates AI capabilities around business outcomes with governance, observability, human approval, provider validation, connector permissioning, benchmark isolation, and release controls.

### 0:45 ? Business Outcome

The demo outcome is Maintain Application Health.

The system starts with the outcome, not with an agent.

This is important because enterprise AI should be governed around what the business needs to protect.

### 1:30 ? Synthetic Data Position

The demo uses synthetic ITIL/AIOps data.

Synthetic data keeps the demo safe, private, repeatable, and benchmark-controlled.

The architecture maps to real systems like ServiceNow, BigPanda, Dynatrace, SAP SolMan, CMDB, Solution 360, enterprise knowledge systems, providers, and MCP connectors.

### 2:30 ? Centerpiece Behavior

The key behavior is HIGH evidence with LOW operational confidence.

HIGH evidence means the evidence is coherent enough to support a hypothesis.

LOW operational confidence means the system still lacks enough validation to act safely.

The system does not confuse evidence strength with permission to act.

### 3:30 ? Safety Boundary

The recommendation is review-only.

Human approval is required.

Provider execution, MCP connector execution, cloud deployment, production writes, notifications, remediation, release creation, benchmark truth updates, and autonomous action remain blocked.

### 4:30 ? Close

Most agent demos try to prove an agent can act.

EAIOS proves the enterprise can decide when an agent must not act.

That is the difference between automation and governed enterprise AI.

## Fifteen-Minute Rehearsal Flow

### 0:00 ? Architecture Frame

Explain EAIOS as an enterprise AI operating-system pattern.

Use the operating model:

Business Outcome -> Capability -> Skill -> Agent / Human / Tool / Workflow -> Data + Knowledge + Context -> Governance + Observability + Feedback

### 2:00 ? Application Health Scenario

Explain that the current demo focuses on Application Health Management.

The synthetic scenario models incident-like signals, alert-like signals, telemetry-like observations, knowledge evidence, known-error patterns, business-impact context, operational confidence, recommendation, and approval boundaries.

### 4:00 ? Enterprise Mapping

Map the synthetic data to real enterprise systems:

- ServiceNow for incidents, problems, known errors, knowledge, changes, and approvals
- BigPanda for correlated alerts
- Dynatrace for telemetry, traces, logs, and health signals
- SAP SolMan for SAP-specific symptoms
- CMDB or service graph for topology
- Solution 360 or BSI-style context for business impact
- enterprise knowledge systems for runbooks and articles
- providers for advisory reasoning after validation
- MCP connectors for governed integration after inventory and approval

### 6:00 ? Governance Architecture

Explain that governance is built into the architecture.

Cover provider validation, MCP connector permissioning, audit events, human approval workflow, benchmark truth isolation, release checklist, blocked action controls, and cloud review gate.

### 8:30 ? Centerpiece Behavior

Spend time on HIGH evidence / LOW operational confidence.

Explain why this matters to enterprise safety.

A plausible recommendation does not equal permission to execute.

### 10:30 ? Human Approval

Explain that human approval is an architectural control.

The system creates a proposal.

It does not execute remediation.

The human remains accountable for high-risk operational action.

### 12:00 ? Non-Claims

Be explicit.

The demo does not claim production deployment, live cloud runtime, real ServiceNow execution, real provider execution, real MCP connector execution, autonomous remediation, production writes, production notifications, or benchmark truth updates from runtime output.

### 13:30 ? Production Path

Explain the safe path forward:

1. preserve synthetic replay baseline
2. document real source purpose
3. identify business, technical, and data owners
4. classify sensitivity
5. define read-only use case
6. define blocked actions
7. define audit and approval requirements
8. enable controlled read-only integration
9. compare real evidence with synthetic expectations
10. expand only after governance approval

### 14:30 ? Close

The future of enterprise AI is governed orchestration of AI capabilities around business outcomes.

EAIOS demonstrates that pattern with synthetic execution, real enterprise architecture, and strict safety boundaries.

## Rehearsal Acceptance Criteria

The rehearsal is ready when you can:

- explain EAIOS in one sentence
- explain why it is not just an agent demo
- explain synthetic versus real clearly
- describe the business outcome
- describe the application-health scenario
- explain HIGH evidence / LOW operational confidence
- explain why human approval is required
- explain what is blocked
- map the demo to ServiceNow and observability systems
- explain provider and MCP connector boundaries
- explain benchmark truth isolation
- explain why cloud deployment is deferred
- answer whether it is production without hesitation
- close with the governed enterprise AI message

## Red Flags To Avoid

Avoid saying:

- it is production-ready
- it is connected to production systems
- it calls real providers
- it calls real MCP connectors
- it executes remediation
- it sends notifications
- it writes to ServiceNow
- it deploys to cloud
- it updates benchmark truth from runtime output
- it enables autonomous action

## Safe Phrases

Use these phrases:

- synthetic execution, real enterprise architecture
- interview-ready and review-only
- evidence does not equal permission to act
- human approval is an architectural control
- provider output is advisory until validated
- connectors are disabled until inventoried, permissioned, approved, audited, and release-gated
- cloud deployment is deferred until the cloud review gate
- benchmark truth remains isolated from runtime output
- EAIOS governs AI work around business outcomes

## Final Rehearsal Sound Bite

EAIOS is not trying to make agents more autonomous first.

It is trying to make enterprise AI more governable first.
