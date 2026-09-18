"""Exact inference checks for the full-cut-slack obstruction, not an A/B search."""
from itertools import combinations

from triangle_free.core import Graph, c5_blowup, deletion_distance, is_triangle_free
from triangle_free.structural_analysis import induced


def petersen():
    return Graph(10, tuple((u, v) for i in range(5) for u, v in
                          ((i, (i + 1) % 5), (i, i + 5),
                           (i + 5, 5 + (i + 2) % 5))))


def monochromatic_sets(graph):
    # Vertex n-1 stays on side zero; all cuts modulo reversal are present.
    return [frozenset((u, v) for u, v in graph.edges
                      if (cut >> u & 1) == (cut >> v & 1))
            for cut in range(1 << (graph.n - 1))]


def incident_count(edges, vertices):
    return sum(u in vertices or v in vertices for u, v in edges)


def test_petersen_optimal_cuts_and_slack_one_counterexample():
    graph = petersen()
    cuts = monochromatic_sets(graph)
    assert is_triangle_free(graph)
    assert min(map(len, cuts)) == deletion_distance(graph) == 3
    optimal = {m for m in cuts if len(m) == 3}
    expected = {frozenset(t) for t in (
        ((0, 1), (3, 8), (7, 9)), ((1, 2), (4, 9), (5, 8)),
        ((1, 6), (3, 4), (5, 7)), ((0, 5), (2, 3), (6, 9)),
        ((0, 4), (2, 7), (6, 8)))}
    assert optimal == expected
    assert set().union(*optimal) == set(graph.edges)
    for edge in graph.edges:
        assert deletion_distance(Graph(10, tuple(e for e in graph.edges if e != edge))) == 2
    y = {0, 1, 3, 8}
    assert {incident_count(m, y) for m in optimal} == {2}
    assert deletion_distance(induced(graph, sorted(set(range(10)) - y))) == 0
    witness = cuts[217]  # side {0,3,4,6,7}
    assert witness == frozenset(((0, 4), (1, 2), (3, 4), (5, 8)))
    assert len(witness) - 3 == 1
    assert incident_count(witness, y) - (len(witness) - 3) == 3


def test_full_cut_identity_and_slack_cutoff_for_all_small_deletions():
    graph = petersen()
    cuts = monochromatic_sets(graph)
    d = deletion_distance(graph)
    for size in range(6):
        for vertices in combinations(range(10), size):
            x = set(vertices)
            remaining = sorted(set(range(10)) - x)
            gamma = d - deletion_distance(induced(graph, remaining))
            lower = max(incident_count(m, x) for m in cuts if len(m) == d)
            total = incident_count(graph.edges, x)
            scores = [incident_count(m, x) - (len(m) - d) for m in cuts]
            assert max(scores) == gamma >= lower
            for m, score in zip(cuts, scores):
                if len(m) - d >= total - lower:
                    assert score <= lower
            compatible = any(len(m) == d and len(m) - incident_count(m, x) == d - gamma
                             for m in cuts)
            assert (lower == gamma) == compatible


def test_nonautomatic_order_25_component_certificate():
    # Additivity is proved in the note; enumerate the two components separately.
    graph = c5_blowup(3)
    cuts = monochromatic_sets(graph)
    assert deletion_distance(graph) == min(map(len, cuts)) == 9
    assert deletion_distance(induced(graph, tuple(range(1, 15)))) == 6
    assert max(incident_count(m, {0}) for m in cuts if len(m) == 9) == 3
    k = (10 + graph.n) // 5
    full_d = 3 + 9
    gamma = (3 - 0) + (9 - 6)
    optimal_only = 2 + 3
    assert k == 5 and full_d >= 2 * k
    assert gamma == 6 > optimal_only == 5
    assert gamma <= 2 * k - 2  # This is not a counterexample to B.
