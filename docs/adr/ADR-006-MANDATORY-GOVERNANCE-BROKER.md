\# ADR-006: Mandatory Governance Broker for Agent and Data Access



\## Status



Proposed



\## Context



EAIOS 2 introduces Zero Trust Agent Governance.



If agents can call each other directly, access data sources directly, or invoke tools directly, governance becomes advisory rather than enforceable.



Runtime governance requires that agent actions be intercepted before execution.



This is especially important for agentic AI because agents may dynamically choose tools, retrieve context, call other agents, summarize evidence, recommend actions, and learn from outcomes.



\## Decision



All agent-to-agent calls and all data-source access must route through a mandatory Governance Broker.



Agents must not receive raw data-source endpoints, direct tool handles, or direct references to other agents.



Agents receive governed clients only.



The governed client routes requests through the Governance Broker.



The Governance Broker consults the Access Governance System before allowing the call to proceed.



Direct calls should be structurally impossible, not merely discouraged.



\## Architecture



```text

Agent

&#x20; ↓

Governed Client

&#x20; ↓

Governance Broker

&#x20; ↓

Access Governance System

&#x20; ↓

Approve / Deny / Escalate

&#x20; ↓

Data Source / Tool / Agent

