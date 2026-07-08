import json
from collections import defaultdict, deque
from pathlib import Path


TOPOLOGY_PATH = Path("data/domain/it_application_health/cmdb_topology.json")
IMPACT_MAP_PATH = Path("data/domain/it_application_health/business_impact_map.json")


def load_topology() -> dict:
    return json.loads(TOPOLOGY_PATH.read_text(encoding="utf-8"))


def load_impact_map() -> dict:
    return json.loads(IMPACT_MAP_PATH.read_text(encoding="utf-8"))


def build_undirected_graph(topology: dict) -> dict[str, set[str]]:
    graph = defaultdict(set)

    for relationship in topology["relationships"]:
        from_ci = relationship["from_ci"]
        to_ci = relationship["to_ci"]

        graph[from_ci].add(to_ci)
        graph[to_ci].add(from_ci)

    return graph


def blast_radius(topology: dict, starting_ci: str, max_depth: int = 2) -> set[str]:
    graph = build_undirected_graph(topology)
    visited = {starting_ci}
    queue = deque([(starting_ci, 0)])

    while queue:
        current, depth = queue.popleft()

        if depth >= max_depth:
            continue

        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, depth + 1))

    return visited


def test_cmdb_topology_exists_and_has_expected_counts():
    topology = load_topology()

    assert topology["business_outcome"] == "Maintain Application Health"
    assert topology["ci_count"] == 24
    assert topology["relationship_count"] == 28
    assert len(topology["cis"]) == 24
    assert len(topology["relationships"]) == 28


def test_cmdb_ci_ids_are_unique():
    topology = load_topology()

    ci_ids = [ci["ci_id"] for ci in topology["cis"]]

    assert len(ci_ids) == len(set(ci_ids))


def test_cmdb_relationships_reference_existing_cis():
    topology = load_topology()

    ci_ids = {ci["ci_id"] for ci in topology["cis"]}

    for relationship in topology["relationships"]:
        assert relationship["from_ci"] in ci_ids
        assert relationship["to_ci"] in ci_ids


def test_checkout_blast_radius_includes_payment_auth_and_compute_host():
    topology = load_topology()

    radius = blast_radius(topology, "CI-CHECKOUT-API-001", max_depth=1)

    assert "CI-PAYMENT-SVC-001" in radius
    assert "CI-AUTH-SVC-001" in radius
    assert "CI-COMPUTE-HOST-007" in radius


def test_shared_compute_host_blast_radius_reaches_checkout_payment_and_auth():
    topology = load_topology()

    radius = blast_radius(topology, "CI-COMPUTE-HOST-007", max_depth=1)

    assert "CI-CHECKOUT-API-001" in radius
    assert "CI-PAYMENT-SVC-001" in radius
    assert "CI-AUTH-SVC-001" in radius


def test_business_impact_map_cis_exist_in_cmdb_topology():
    topology = load_topology()
    impact_map = load_impact_map()

    ci_ids = {ci["ci_id"] for ci in topology["cis"]}

    mapped_cis = set()

    for service in impact_map["business_services"]:
        mapped_cis.update(service["mapped_cis"])

    for unmapped in impact_map["unmapped_cis"]:
        mapped_cis.add(unmapped["ci_id"])

    assert mapped_cis.issubset(ci_ids)


def test_unmapped_ci_has_no_business_service_mapping():
    topology = load_topology()

    unmapped = next(
        ci for ci in topology["cis"] if ci["ci_id"] == "CI-UNMAPPED-API-001"
    )

    assert unmapped["mapped_business_services"] == []