# Enterprise AI Operating System Domain Model

The Enterprise AI Operating System is built around a small set of fundamental business concepts.

These concepts remain stable regardless of cloud provider, LLM, or implementation technology.

---

# Goal

A persistent business objective that the enterprise wants to achieve.

Examples

- Restore Online Banking
- Reduce Fraud
- Onboard Employee
- Resolve Critical Incident

---

# Agent

A reusable intelligent capability responsible for performing one well-defined task.

Examples

- Observability Agent
- Change Agent
- Knowledge Agent
- Security Agent

---

# Capability

A reusable business capability provided by one or more agents.

Examples

- Event Correlation
- Root Cause Analysis
- Change Risk Assessment

---

# Knowledge

Enterprise information used to reason about goals.

Examples

- CMDB
- Runbooks
- Knowledge Articles
- Architecture
- Previous Incidents

---

# Observation

Evidence collected from the enterprise.

Examples

- Alert
- Metric
- Log
- Change
- Ticket

---

# Recommendation

The proposed action generated after reasoning across available evidence.

Examples

- Roll back deployment
- Restart service
- Escalate to CAB
- Notify business owner

---

# Policy

Enterprise rules governing agent behavior.

Examples

- Human approval required
- Financial systems require CAB review
- Production changes require change window

---

# Human Approval

Enterprise checkpoint before executing high-risk actions.

Examples

- AI Advisory Board
- CAB
- Operations Manager