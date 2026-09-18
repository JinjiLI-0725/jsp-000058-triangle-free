"""Finite checks of the shared-boundary gadget, not a general A/B search."""
from triangle_free.core import Graph, deletion_distance, is_triangle_free
from triangle_free.structural_analysis import induced


def gadget():
    edges = {tuple(sorted(e)) for i in range(5) for e in
             ((i, (i + 1) % 5), (i, i + 5),
              (i + 5, 5 + (i + 2) % 5))}
    for u, v, a, b in ((0, 1, 10, 11), (3, 8, 12, 13)):
        edges.remove((u, v))
        edges.update(((u, a), (a, b), (b, v)))
    return Graph(14, tuple(edges))


def test_shared_boundary_gadget_all_cuts():
    graph = gadget()
    y = {0, 1, 3, 8}
    assert is_triangle_free(graph)
    assert deletion_distance(graph) == 3
    assert deletion_distance(induced(graph, sorted(set(range(14)) - y))) == 0
    by_boundary = {}
    optimal_union = set()
    for cut in range(1 << graph.n):
        mono = {e for e in graph.edges if (cut >> e[0] & 1) == (cut >> e[1] & 1)}
        r = sum(u in y or v in y for u, v in mono)
        boundary = tuple(cut >> v & 1 for v in sorted(y))
        by_boundary.setdefault(boundary, []).append((len(mono), r))
        if len(mono) == 3:
            optimal_union.update(mono)
            assert r <= 2
    assert optimal_union == set(graph.edges)  # Critical-edge criterion.
    assert max(r for rows in by_boundary.values() for b, r in rows if b == 3) == 2
    assert min(b for rows in by_boundary.values() for b, r in rows if b == r) == 4

    # Exact dynamic programming joins copies ONLY with identical Y colors.
    # This includes every coloring for each stated copy count without full
    # enumeration of the much larger amalgamated graph.
    for copies in (1, 2, 3, 5):
        joined = set()
        for rows in by_boundary.values():
            states = {(0, 0)}
            for _ in range(copies):
                states = {(b + db, r + dr) for b, r in states for db, dr in set(rows)}
            joined.update(states)
        d = min(b for b, r in joined)
        assert d == 3 * copies
        assert max(r for b, r in joined if b == d) == 2 * copies
        assert max(r - (b - d) for b, r in joined) == 3 * copies
        assert min(b - d for b, r in joined if b == r) == copies
        assert max(r - (b - d) for b, r in joined if b - d < copies) < 3 * copies
