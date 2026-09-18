"""Exact rooted-table check of the connected slack obstruction."""
from triangle_free.core import Graph, c5_blowup, is_triangle_free
from test_induction_slack_amplification import gadget


def rooted_table(graph, root, deleted):
    states = set()
    best = len(graph.edges) + 1
    covered = set()
    for cut in range(1 << graph.n):
        if cut >> root & 1:
            continue
        mono = {e for e in graph.edges
                if (cut >> e[0] & 1) == (cut >> e[1] & 1)}
        cost = len(mono)
        remainder = sum(u not in deleted and v not in deleted for u, v in mono)
        states.add((cost, remainder))
        if cost < best:
            best, covered = cost, set(mono)
        elif cost == best:
            covered.update(mono)
    assert covered == set(graph.edges)  # All blocks are edge-critical.
    return states


def test_connected_one_vertex_gluing_exact_tables():
    q = gadget()
    cycle = Graph(13, tuple((i, (i + 1) % 13) for i in range(13)))
    balanced = c5_blowup(3)
    blocks = ((q, 9, {0, 1, 3, 8}), (cycle, 0, {1}), (balanced, 0, set()))
    states = {(0, 0)}
    edges, deleted = [], set()
    next_vertex = 1
    for block, root, local_deleted in blocks:
        assert is_triangle_free(block)
        table = rooted_table(block, root, local_deleted)
        states = {(b + c, r + t) for b, r in states for c, t in table}
        mapping = {root: 0}
        for v in range(block.n):
            if v != root:
                mapping[v] = next_vertex
                next_vertex += 1
        edges.extend((mapping[u], mapping[v]) for u, v in block.edges)
        deleted.update(mapping[v] for v in local_deleted)
    joined = Graph(next_vertex, tuple(edges))
    assert joined.n == 40 and len(deleted) == 5 and 0 not in deleted
    assert is_triangle_free(joined)
    reached = {0}
    while True:
        expanded = reached | {v for u, v in joined.edges if u in reached}
        expanded |= {u for u, v in joined.edges if v in reached}
        if expanded == reached:
            break
        reached = expanded
    assert len(reached) == joined.n
    d = min(b for b, r in states)
    remainder_d = min(r for b, r in states)
    assert (d, remainder_d) == (13, 9)
    assert d - remainder_d == max(d - r for b, r in states) == 4
    assert max(b - r for b, r in states if b == d) == 3
    assert min(b - d for b, r in states if r == remainder_d) == 1
