from itertools import combinations
import random

import pytest

from triangle_free import Graph, c5_blowup, deletion_distance, exact_max_cut, is_triangle_free, random_triangle_free
from triangle_free.search import all_labeled_graphs


def reference_cut(graph):
    # Independent full enumeration, including both complementary partitions.
    return max(sum(((mask >> u) & 1) != ((mask >> v) & 1) for u, v in graph.edges)
               for mask in range(1 << graph.n))


def reference_triangle_free(graph):
    edges = set(graph.edges)
    return not any(all(edge in edges for edge in combinations(triple, 2))
                   for triple in combinations(range(graph.n), 3))


def cycle(n):
    return Graph(n, tuple((i, (i + 1) % n) for i in range(n)))


@pytest.mark.parametrize("n", range(9))
def test_empty_and_paths(n):
    for graph in (Graph(n), Graph(n, tuple((i, i + 1) for i in range(n - 1)))):
        assert is_triangle_free(graph)
        assert exact_max_cut(graph).value == len(graph.edges)
        assert deletion_distance(graph) == 0


@pytest.mark.parametrize("n", [4, 6, 8, 10])
def test_even_cycles(n):
    assert is_triangle_free(cycle(n))
    assert exact_max_cut(cycle(n)).value == n
    assert deletion_distance(cycle(n)) == 0


def test_odd_cycles_and_blowup():
    for n in (5, 7, 9):
        assert is_triangle_free(cycle(n))
        assert exact_max_cut(cycle(n)).value == n - 1
        assert deletion_distance(cycle(n)) == 1
    assert len(c5_blowup(2).edges) == 20
    assert is_triangle_free(c5_blowup(2))
    assert exact_max_cut(c5_blowup(2)).value == 16
    assert deletion_distance(c5_blowup(2)) == 4


def test_all_graphs_through_five_vertices_against_independent_oracles():
    for n in range(6):
        for graph in all_labeled_graphs(n):
            assert is_triangle_free(graph) == reference_triangle_free(graph)
            cut = exact_max_cut(graph)
            assert cut.value == reference_cut(graph)
            side = set(cut.side)
            assert sum((u in side) != (v in side) for u, v in graph.edges) == cut.value
            assert 0 not in side
            assert cut.cuts_examined == 2 ** max(0, n - 1)


def test_larger_graph_oracle_and_relabeling():
    rng = random.Random(901)
    for _ in range(30):
        graph = Graph(10, tuple(edge for edge in combinations(range(10), 2) if rng.random() < 0.5))
        permutation = list(range(10))
        rng.shuffle(permutation)
        relabeled = Graph(10, tuple((permutation[u], permutation[v]) for u, v in graph.edges))
        assert exact_max_cut(graph).value == reference_cut(graph) == exact_max_cut(relabeled).value


def test_disconnected_and_isolated_vertices():
    graph = Graph(12, cycle(5).edges + tuple((u + 5, v + 5) for u, v in cycle(5).edges))
    assert deletion_distance(graph) == 2


@pytest.mark.parametrize("p", [0, 0.25, 0.5, 1])
def test_random_generator(p):
    for seed in range(25):
        graph = random_triangle_free(10, random.Random(seed), edge_probability=p)
        assert graph == random_triangle_free(10, random.Random(seed), edge_probability=p)
        assert reference_triangle_free(graph)
        if p == 0:
            assert graph.edges == ()
        if p == 1:
            for edge in set(combinations(range(10), 2)) - set(graph.edges):
                assert not reference_triangle_free(Graph(10, graph.edges + (edge,)))
    assert random_triangle_free(0, random.Random(0), edge_probability=p) == Graph(0)


@pytest.mark.parametrize("n,edges", [(-1, ()), (2.0, ()), (True, ()), (2, ((0, 0),)),
                                   (2, ((0, 2),)), (2, ((-1, 1),)), (2, ((0, 1.0),)),
                                   (2, ((0, 1), (1, 0)))])
def test_invalid_graph(n, edges):
    with pytest.raises(ValueError):
        Graph(n, edges)


def test_canonicalization_and_guards():
    assert Graph(3, [(2, 0), (1, 0)]).edges == ((0, 1), (0, 2))
    with pytest.raises(ValueError):
        exact_max_cut(Graph(25))
    for p in (-0.1, 1.1, float("nan")):
        with pytest.raises(ValueError):
            random_triangle_free(5, random.Random(0), edge_probability=p)
    with pytest.raises(ValueError):
        c5_blowup(0)
