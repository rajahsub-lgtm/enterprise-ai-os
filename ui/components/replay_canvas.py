"""
Static orchestration replay canvas model.

Classification: EAIOS Presentation Layer

This module projects animation_events into a static DOT graph for the first
Streamlit replay canvas.

It does not make governance, evidence, confidence, approval, or remediation
decisions.
"""

from __future__ import annotations

from typing import Any


def replay_canvas_model(run_view_model: dict[str, Any]) -> dict[str, Any]:
    events = run_view_model.get("animation_events", [])

    nodes = _nodes_from_events(events)
    edges = _edges_from_events(events)

    return {
        "run_id": run_view_model["run_id"],
        "scenario_label": run_view_model["scenario_label"],
        "nodes": nodes,
        "edges": edges,
        "dot": replay_canvas_dot(
            run_view_model["scenario_label"],
            nodes,
            edges,
        ),
    }


def replay_canvas_dot(
    scenario_label: str,
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> str:
    lines = [
        "digraph EAIOSReplay {",
        '  graph [rankdir=LR, bgcolor="transparent", labelloc="t"];',
        f'  label="{_escape(scenario_label)}";',
        '  node [shape=box, style="rounded,filled", fontname="Arial", fontsize=10];',
        '  edge [fontname="Arial", fontsize=9];',
    ]

    for node in nodes:
        lines.append(
            f'  "{_escape(node["node_id"])}" '
            f'[label="{_escape(node["label"])}", fillcolor="{node["fillcolor"]}"];'
        )

    for edge in edges:
        lines.append(
            f'  "{_escape(edge["from_node"])}" -> "{_escape(edge["to_node"])}" '
            f'[label="{_escape(edge["label"])}", color="{edge["color"]}"];'
        )

    lines.append("}")

    return "\n".join(lines)


def _nodes_from_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    node_map: dict[str, dict[str, Any]] = {}

    _put_node(
        node_map,
        "joint_goal",
        "Joint Goal",
        "white",
    )
    _put_node(
        node_map,
        "evidence_fusion",
        "Evidence Fusion",
        "lightblue",
    )
    _put_node(
        node_map,
        "operational_confidence",
        "Operational Confidence",
        "lightyellow",
    )
    _put_node(
        node_map,
        "due_diligence",
        "Due Diligence",
        "lightyellow",
    )
    _put_node(
        node_map,
        "human_review",
        "Human Review Required",
        "lightgrey",
    )
    _put_node(
        node_map,
        "excluded_evidence",
        "Excluded Evidence",
        "mistyrose",
    )

    for event in events:
        event_type = event["event_type"]

        if event_type == "NODE_ACTIVATED":
            node_id = event.get("node_id")
            if node_id and node_id != "joint_goal":
                _put_node(
                    node_map,
                    node_id,
                    _agent_label(event.get("agent_id"), node_id),
                    "white",
                )

        if event_type == "GOVERNANCE_GATE_STAMPED":
            node_id = event["node_id"]
            _put_node(
                node_map,
                node_id,
                _gate_label(event),
                _gate_color(event.get("decision")),
            )

        if event_type == "EVIDENCE_TOKEN_MOVED":
            node_id = event["node_id"]
            _put_node(
                node_map,
                node_id,
                _evidence_label(event),
                "honeydew",
            )

        if event_type == "EVIDENCE_EXCLUDED":
            node_id = event["node_id"]
            _put_node(
                node_map,
                node_id,
                _evidence_label(event),
                "mistyrose",
            )

        if event_type == "EVIDENCE_GAP_CREATED":
            node_id = event["node_id"]
            _put_node(
                node_map,
                node_id,
                _gap_label(event),
                "mistyrose",
            )

    return list(node_map.values())


def _edges_from_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    edges: list[dict[str, Any]] = []

    current_agent_node: str | None = None

    for event in events:
        event_type = event["event_type"]

        if event_type == "NODE_ACTIVATED" and event.get("node_id") != "joint_goal":
            current_agent_node = event["node_id"]
            edges.append(
                {
                    "from_node": "joint_goal",
                    "to_node": current_agent_node,
                    "label": "orchestrates",
                    "color": "gray",
                }
            )

        if event_type == "GOVERNANCE_GATE_STAMPED":
            gate_node = event["node_id"]
            decision = event.get("decision", "UNKNOWN")

            if current_agent_node:
                edges.append(
                    {
                        "from_node": current_agent_node,
                        "to_node": gate_node,
                        "label": "governed access",
                        "color": _decision_color(decision),
                    }
                )

            if decision == "ALLOW" and event.get("evidence_id"):
                edges.append(
                    {
                        "from_node": gate_node,
                        "to_node": f'evidence::{event["evidence_id"]}',
                        "label": "evidence",
                        "color": _decision_color(decision),
                    }
                )

            if decision == "DENY":
                edges.append(
                    {
                        "from_node": gate_node,
                        "to_node": _gap_node_id_from_gate(event),
                        "label": "gap created",
                        "color": _decision_color(decision),
                    }
                )

        if event_type == "EVIDENCE_TOKEN_MOVED":
            edges.append(
                {
                    "from_node": event["node_id"],
                    "to_node": "evidence_fusion",
                    "label": "eligible",
                    "color": "green",
                }
            )

        if event_type == "EVIDENCE_EXCLUDED":
            edges.append(
                {
                    "from_node": event["node_id"],
                    "to_node": "excluded_evidence",
                    "label": "excluded",
                    "color": "red",
                }
            )

    edges.extend(
        [
            {
                "from_node": "evidence_fusion",
                "to_node": "operational_confidence",
                "label": "fuses",
                "color": "blue",
            },
            {
                "from_node": "operational_confidence",
                "to_node": "due_diligence",
                "label": "selects depth",
                "color": "blue",
            },
            {
                "from_node": "due_diligence",
                "to_node": "human_review",
                "label": "stops at review",
                "color": "gray",
            },
        ]
    )

    return _dedupe_edges(edges)


def _put_node(
    node_map: dict[str, dict[str, Any]],
    node_id: str,
    label: str,
    fillcolor: str,
) -> None:
    if node_id not in node_map:
        node_map[node_id] = {
            "node_id": node_id,
            "label": label,
            "fillcolor": fillcolor,
        }


def _agent_label(agent_id: str | None, node_id: str) -> str:
    if agent_id:
        return agent_id.replace("_", " ").title()

    return node_id.replace("::", "\n").replace("_", " ").title()


def _gate_label(event: dict[str, Any]) -> str:
    decision = event.get("decision", "UNKNOWN")
    source_id = event.get("source_id", "unknown_source")

    return f"Gate: {decision}\\n{source_id}"


def _evidence_label(event: dict[str, Any]) -> str:
    evidence_id = event.get("evidence_id", "unknown_evidence")
    status = event.get("content_safety_status", "unknown_status")

    return f"Evidence\\n{evidence_id}\\n{status}"


def _gap_label(event: dict[str, Any]) -> str:
    source_id = event.get("source_id", "unknown_source")

    return f"Evidence Gap\\n{source_id}"


def _gate_color(decision: str | None) -> str:
    if decision == "ALLOW":
        return "palegreen"

    if decision == "DENY":
        return "mistyrose"

    if decision == "ESCALATE":
        return "khaki"

    return "lightgrey"


def _decision_color(decision: str | None) -> str:
    if decision == "ALLOW":
        return "green"

    if decision == "DENY":
        return "red"

    if decision == "ESCALATE":
        return "orange"

    return "gray"


def _gap_node_id_from_gate(event: dict[str, Any]) -> str:
    return f'gap::{event.get("agent_id", "unknown")}::{event.get("source_id", "unknown")}'


def _dedupe_edges(edges: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen = set()
    unique = []

    for edge in edges:
        key = (
            edge["from_node"],
            edge["to_node"],
            edge["label"],
            edge["color"],
        )

        if key not in seen:
            seen.add(key)
            unique.append(edge)

    return unique


def _escape(value: Any) -> str:
    return str(value).replace('"', '\\"')
