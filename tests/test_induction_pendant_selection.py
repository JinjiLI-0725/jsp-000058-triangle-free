"""Exact inference checks for rooted pendant five-set selection."""
from itertools import combinations

from triangle_free.core import Graph, c5_blowup, deletion_distance, is_triangle_free
from triangle_free.structural_analysis import induced


def remaining(graph, deleted):
    return induced(graph, tuple(v for v in range(graph.n) if v not in deleted))


def glue(left, right):
    """Identify vertex zero, preserving all left labels."""
    mapping = {0: 0, **{v: left.n + v - 1 for v in range(1, right.n)}}
    return Graph(left.n + right.n - 1, left.edges + tuple(
        (mapping[u], mapping[v]) for u, v in right.edges))


def test_root_avoiding_profiles_by_full_cuts():
    for s in (1, 2):
        graph = c5_blowup(s)
        d = deletion_distance(graph)
        assert d == s * s
        for j in range(min(5, graph.n - 1) + 1):
            costs = [d - deletion_distance(remaining(graph, set(x)))
                     for x in combinations(range(1, graph.n), j)]
            expected = 0 if j == 0 else (1 if s == 1 else s if j <= 2 else 2 * s - 1)
            assert min(costs) == expected


def test_gluing_preserves_every_local_deletion_increment():
    left = c5_blowup(2)
    pieces = (c5_blowup(1), Graph(5, tuple((u, v) for u in range(2) for v in range(2, 5))))
    for right in pieces:
        graph = glue(left, right)
        assert is_triangle_free(graph)
        d = deletion_distance(graph)
        local_d = deletion_distance(left)
        assert d == local_d + deletion_distance(right)
        for j in range(6):
            for x in combinations(range(1, left.n), j):
                deleted = set(x)
                assert d - deletion_distance(remaining(graph, deleted)) == (
                    local_d - deletion_distance(remaining(left, deleted)))


def test_five_set_witnesses_and_boundary_limit():
    # Root is zero in the first size-s part. Avoid it in the transversal.
    for s in (2, 3):
        graph = c5_blowup(s)
        x = {1, s, 2 * s, 3 * s, 4 * s}
        assert deletion_distance(graph) - deletion_distance(remaining(graph, x)) == 2 * s - 1
    first = glue(c5_blowup(1), c5_blowup(1))
    # Two pendant cycles share a root, which is retained.
    x = {1, 2, 3, 4, 5}
    assert deletion_distance(first) - deletion_distance(remaining(first, x)) == 2
    # Two retained boundary vertices cannot in general be aligned by reversal.
    short = Graph(3, ((0, 2), (1, 2)))
    long = Graph(4, ((0, 2), (2, 3), (1, 3)))
    union = Graph(5, ((0, 2), (1, 2), (0, 3), (3, 4), (1, 4)))
    assert deletion_distance(short) == deletion_distance(long) == 0
    assert is_triangle_free(union) and deletion_distance(union) == 1


def test_nonautomatic_high_degree_core_and_zero_q_witness():
    joined = glue(c5_blowup(2), c5_blowup(2))
    graph = Graph(20, joined.edges)  # One retained isolate; k=4.
    x = {1, 2, 4, 6, 8}
    assert deletion_distance(graph) == 8
    assert deletion_distance(remaining(graph, x)) == 5
    degrees = [sum(v in edge for edge in graph.edges) for v in range(20)]
    assert sum(d <= 3 for d in degrees) == 1
    # Parts 0 and 1 are the sole monochromatic pair in each block.
    part_colors = (0, 0, 1, 0, 1)
    colors = [part_colors[v // 2] for v in range(10)]
    colors += [part_colors[v // 2] for v in range(1, 10)] + [0]
    mono = [(u, v) for u, v in graph.edges if colors[u] == colors[v]]
    remainder_cost = sum(u not in x and v not in x for u, v in mono)
    assert len(mono) == 8 and remainder_cost == 5  # q=0, e=3.
