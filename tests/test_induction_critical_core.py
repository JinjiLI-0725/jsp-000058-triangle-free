"""Bounded exact checks of the critical-core induction reduction."""

from itertools import combinations

from triangle_free.core import Graph, c5_blowup, deletion_distance, is_triangle_free
from triangle_free.structural_analysis import induced


def core(graph):
    target = deletion_distance(graph)
    while True:
        for edge in graph.edges:
            smaller = Graph(graph.n, tuple(e for e in graph.edges if e != edge))
            if deletion_distance(smaller) == target:
                graph = smaller
                break
        else:
            return graph


def blowup(weights):
    parts = [i for i, size in enumerate(weights) for _ in range(size)]
    return Graph(len(parts), tuple((u, v) for u, v in combinations(range(len(parts)), 2)
                                  if (parts[u] - parts[v]) % 5 in (1, 4)))


def test_core_transfer_for_every_five_set():
    balanced = c5_blowup(2)
    fixtures = [balanced, Graph(10, balanced.edges[1:]),
                blowup((3, 2, 2, 2, 1)), blowup((6, 1, 1, 1, 1)),
                Graph(10, tuple((u, v) for u in range(4) for v in range(4, 10)))]
    strict_slack = False
    for graph in fixtures:
        critical = core(graph)
        d = deletion_distance(graph)
        assert critical.n == graph.n and deletion_distance(critical) == d
        assert is_triangle_free(critical)
        for edge in critical.edges:
            assert deletion_distance(Graph(10, tuple(e for e in critical.edges if e != edge))) == d - 1
        for remaining in combinations(range(10), 5):
            original_d = deletion_distance(induced(graph, remaining))
            core_d = deletion_distance(induced(critical, remaining))
            delta = original_d - core_d
            assert delta >= 0
            assert d - original_d == (d - core_d) - delta
            strict_slack |= delta > 0
    assert strict_slack


def test_critical_edges_equal_union_of_optimal_monochromatic_sets():
    pairs = tuple(combinations(range(5), 2))
    count = 0
    for mask in range(1 << len(pairs)):
        graph = Graph(5, tuple(e for i, e in enumerate(pairs) if mask >> i & 1))
        if not is_triangle_free(graph):
            continue
        count += 1
        d = deletion_distance(graph)
        union = set()
        # Direct cut enumeration is independent of the Gray-code solver.
        for cut in range(16):
            mono = {e for e in graph.edges if ((cut >> e[0]) & 1) == ((cut >> e[1]) & 1)}
            if len(mono) == d:
                union.update(mono)
        for edge in graph.edges:
            smaller = Graph(5, tuple(e for e in graph.edges if e != edge))
            assert (deletion_distance(smaller) == d - 1) == (edge in union)
    assert count == 388


def test_blowup_critical_edge_criterion_with_split_cuts_allowed():
    count = 0
    for bars in combinations(range(1, 10), 4):
        weights = tuple(b - a for a, b in zip((0,) + bars, bars + (10,)))
        graph = blowup(weights)
        parts = [i for i, size in enumerate(weights) for _ in range(size)]
        products = [weights[i] * weights[(i + 1) % 5] for i in range(5)]
        d = min(products)
        assert deletion_distance(graph) == d
        for edge in graph.edges:
            u, v = edge
            pair_product = weights[parts[u]] * weights[parts[v]]
            smaller = Graph(10, tuple(e for e in graph.edges if e != edge))
            assert deletion_distance(smaller) == d - int(pair_product == d)
        count += 1
    assert count == 126


def test_transfer_requires_equal_distance_and_balanced_is_maximal():
    cycle = c5_blowup(1)
    graph = Graph(10, cycle.edges)
    smaller = Graph(10, cycle.edges[1:])
    remaining = (1, 2, 3, 4, 9)
    assert deletion_distance(graph) - deletion_distance(induced(graph, remaining)) == 1
    assert deletion_distance(smaller) - deletion_distance(induced(smaller, remaining)) == 0
    for k in (1, 2):
        balanced = c5_blowup(k)
        for edge in combinations(range(5 * k), 2):
            if edge not in balanced.edges:
                assert not is_triangle_free(Graph(5 * k, balanced.edges + (edge,)))
