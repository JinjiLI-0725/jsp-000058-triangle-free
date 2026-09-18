"""Independent finite checks of the structural formulas and experiment helpers."""

from itertools import combinations
import random

from triangle_free.core import Graph, c5_blowup, deletion_distance
from triangle_free.structural_analysis import balanced, induced, reduction_test, vertex_patterns


def blowup(weights):
    parts = [i for i, size in enumerate(weights) for _ in range(size)]
    return Graph(len(parts), tuple((u, v) for u, v in combinations(range(len(parts)), 2)
                                  if (parts[u] - parts[v]) % 5 in (1, 4)))


def test_formula_and_vertex_transfers_against_full_cuts():
    rng = random.Random(58)
    vectors = [(2, 2, 2, 2, 2), (0, 1, 2, 3, 4)]
    for _ in range(20):
        weights = [0]*5
        for _ in range(10):
            weights[rng.randrange(5)] += 1
        vectors.append(tuple(weights))
    for weights in vectors:
        assert deletion_distance(blowup(weights)) == min(weights[i]*weights[(i+1) % 5] for i in range(5))
    for p, q in combinations(range(5), 2):
        weights = [2]*5
        weights[p] -= 1
        weights[q] += 1
        assert deletion_distance(blowup(weights)) == 2


def test_edge_deletion_and_balanced_detection():
    graph = c5_blowup(2)
    assert balanced(graph)
    for edge in graph.edges:
        reduced = Graph(10, tuple(e for e in graph.edges if e != edge))
        assert deletion_distance(reduced) == 3
        assert not balanced(reduced)
    assert deletion_distance(induced(graph, [0, 2, 4, 6, 8])) == 1


def test_neighborhood_oracle_and_reduction_checks():
    result = vertex_patterns(2)
    assert result['patterns'] == 47
    assert result['histogram'] == {2: 38, 3: 8, 4: 1}
    assert result['non_C5_equality'] == 0
    graph = c5_blowup(2)
    reduced = Graph(10, graph.edges[1:])
    check = reduction_test([(graph, 4), (reduced, 3)])
    assert not check['A_failures'] and not check['B_failures']
