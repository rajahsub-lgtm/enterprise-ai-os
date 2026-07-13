# EAIOS 2 Sprint 8 Real + Synthetic Data Map

## Purpose

This document explains how the EAIOS interview demo uses synthetic ITIL/AIOps data today and how that data maps to future real enterprise systems.

The goal is to make the demo honest, interview-ready, and governance-safe.

## Demo Data Position

The current demo uses synthetic enterprise-shaped data.

It does not connect to production systems.

It does not use real ServiceNow, BigPanda, Dynatrace, SAP SolMan, CMDB, Solution 360, provider, MCP connector, or cloud runtime data.

The synthetic data is designed to model realistic enterprise operating signals while preserving privacy, safety, repeatability, and benchmark control.

## Core Principle

Synthetic execution, real enterprise architecture.

The demo is synthetic in data execution but real in architecture, governance, controls, and integration design.

## Why Synthetic Data Is Used

Synthetic data is used because it allows EAIOS to demonstrate enterprise AI governance safely.

It supports:

- repeatable interview demo runs
- controlled benchmark expectations
- safe incident and alert simulation
- no exposure of production records
- no secrets or credentials
- no production writes
- no real connector execution
- no provider dependency
- no cloud dependency
- deterministic regression testing
- benchmark truth isolation

## What Synthetic Data Represents

The synthetic scenario represents a realistic application-health operating context.

It includes:

- application symptoms
- telemetry observations
- incident-like signals
- alert-like signals
- knowledge evidence
- known-error patterns
- reasoning context
- recommendation context
- operational confidence signals
- human approval boundaries

## Data Boundary

Synthetic data can provide operating context.

Synthetic data can support deterministic tests.

Synthetic data can provide benchmark scenarios.

Synthetic data must not be confused with production truth.

Synthetic data must not authorize real-world action.

Runtime output, provider output, connector output, audit output, approval output, and release output must not define benchmark truth.

## Mapping Table

| Synthetic Demo Data | Real Enterprise Equivalent | Example System | EAIOS Role | Governance Boundary |
|---|---|---|---|---|
| Synthetic incident record | Incident ticket | ServiceNow Incident | Case signal and user-impact context | Read-only until connector review |
| Synthetic problem cluster | Problem record or recurring issue cluster | ServiceNow Problem | Pattern and recurrence analysis | Human review required |
| Synthetic alert | Correlated monitoring alert | BigPanda | Operational signal | Read-only and source-authorized |
| Synthetic telemetry | Metrics, traces, logs, health signals | Dynatrace | Observability evidence | Content safety and provenance required |
| Synthetic SAP signal | SAP application or transaction symptom | SAP SolMan | Domain-specific application evidence | Domain owner review required |
| Synthetic knowledge article | KB article or runbook | ServiceNow Knowledge / Wiki | Free-text evidence | Injection, staleness, and trust checks required |
| Synthetic known error | Known-error database entry | ServiceNow KEDB | Known issue matching | Approved provenance required |
| Synthetic topology context | Application dependency graph | CMDB / Service Graph | Upstream and downstream impact | Ownership and freshness required |
| Synthetic business impact | Service or business capability impact | Solution 360 / BSI | Prioritization and risk context | Business owner review required |
| Synthetic recommendation | Proposed operator action | EAIOS Recommendation Agent | Human-review proposal | Not executable without approval |
| Synthetic confidence score | Operational confidence assessment | EAIOS Governance Layer | Action gating | Cannot override human approval |
| Synthetic approval gate | Human approval workflow | CAB / AIAB-style review | Control boundary | Approval not auto-granted |

## Real System Integration Direction

Future real-data integration should follow a governed sequence:

1. register the source
2. define source owner and data owner
3. classify data sensitivity
4. define read/write permissions
5. define allowed operations
6. define blocked operations
7. validate provenance
8. validate content safety
9. preserve benchmark truth isolation
10. require human approval for high-risk actions
11. audit every decision
12. provide rollback or disable switch

## ServiceNow Mapping

ServiceNow is the future source for incidents, problems, knowledge, known errors, changes, and workflow approvals.

In the demo, ServiceNow is represented by synthetic incident, problem, knowledge, and known-error records.

Future integration must remain read-only until MCP connector inventory, permission classification, audit, approval, and release gates are complete.

ServiceNow writes, updates, approvals, and notifications remain blocked in the demo.

## Observability Mapping

BigPanda, Dynatrace, SAP SolMan, and similar systems are represented by synthetic alert and telemetry records.

These signals help EAIOS reason about application health, but they do not authorize autonomous action.

Future integration must distinguish source authorization from content safety.

A trusted source can still contain stale, incomplete, misleading, or unsafe content.

## Topology and Business Impact Mapping

CMDB, service graph, and Solution 360-style context are represented by synthetic topology and business-impact evidence.

This data helps the system understand upstream and downstream risk.

Future integration must include service ownership, data freshness, and business owner accountability.

## Knowledge Mapping

Knowledge articles, runbooks, and wiki content are represented by synthetic knowledge evidence.

Knowledge is useful but risky because free text can be stale, incomplete, contradictory, or injection-prone.

Future integration must apply content safety checks, freshness checks, trust-level checks, and citation/provenance requirements.

## Benchmark Mapping

Benchmark truth remains separate from runtime output.

Benchmark truth can come from controlled benchmark fixtures and verification targets.

Benchmark truth cannot be created by:

- runtime reasoning
- provider output
- connector output
- audit events
- approval decisions
- release checklist output
- static export output

## Provider Boundary

Real LLM or AI provider integration is not enabled in the demo.

Provider integration remains represented by schemas, validators, and blocked actions.

Future provider output must pass:

- schema validation
- evidence reference validation
- unsupported action checks
- benchmark truth claim checks
- benchmark scoring checks
- remediation instruction checks
- notification instruction checks
- secret leakage checks
- unsafe certainty checks
- human review checks

## MCP Connector Boundary

Real MCP connectors are not enabled in the demo.

MCP connector integration remains represented by inventory schema, permission classification, audit events, approval workflow, and release gating.

Future connectors must be registered with:

- connector id
- connector owner
- business owner
- technical owner
- data domain
- data classification
- permission class
- allowed operations
- disallowed operations
- approval status
- risk tier
- audit requirement
- rollback or disable switch

## What Is Real Today

The following are real today:

- architecture contracts
- governance model
- safety boundaries
- test-backed modules
- deterministic demo behavior
- synthetic ITIL/AIOps scenario structure
- benchmark isolation design
- provider validation design
- MCP connector permission design
- audit event design
- human approval design
- release checklist design

## What Is Synthetic Today

The following are synthetic today:

- application-health scenario data
- incident-like records
- alert-like records
- telemetry-like records
- knowledge evidence
- known-error patterns
- business-impact context
- recommendation context
- operational confidence context

## What Is Not Connected Today

The following are not connected today:

- real ServiceNow instance
- real BigPanda instance
- real Dynatrace instance
- real SAP SolMan instance
- real CMDB or service graph
- real Solution 360 or BSI platform
- real LLM provider call
- real MCP connector call
- real cloud deployment
- real approval persistence
- real notification channel
- real remediation action

## Interview Explanation

The safest interview explanation is:

This demo uses synthetic ITIL/AIOps data to simulate a realistic enterprise application-health scenario. The architecture is designed for real ServiceNow, observability, knowledge, topology, and business-impact integration, but those integrations are deliberately disabled until governance, ownership, permissions, audit, approval, and release controls are reviewed.

## Interview Sound Bite

The data is synthetic so the demo is safe and repeatable.

The architecture is real so the governance problem is enterprise-grade.

## Cloud Deployment Implication

Cloud deployment should not happen until the cloud review gate confirms:

- what is deployed
- what remains static
- whether providers remain disabled
- whether MCP connectors remain disabled
- whether secrets are required
- whether benchmark truth remains isolated
- whether human approval remains required
- IAM boundary
- cost boundary
- rollback or disable plan

## Close

This data map anchors Sprint 8 interview readiness.

It allows EAIOS to be presented honestly as a synthetic-data demo with real enterprise integration architecture and strict governance boundaries.
