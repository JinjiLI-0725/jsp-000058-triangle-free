"""Full-cut checks of two-boundary flexibility and private transversals."""
from itertools import combinations

from triangle_free.core import Graph, c5_blowup, deletion_distance, is_triangle_free
from triangle_free.structural_analysis import induced


def profile(graph, roots):
    values = [len(graph.edges) + 1] * 4
    for mask in range(1 << graph.n):
        state = ((mask >> roots[0]) & 1) + 2 * ((mask >> roots[1]) & 1)
        cost = sum(((mask >> u) & 1) == ((mask >> v) & 1) for u, v in graph.edges)
        values[state] = min(values[state], cost)
    return values


def glue(left, right, roots, other_roots):
    mapping = dict(zip(other_roots, roots))
    for v in range(right.n):
        if v not in mapping:
            mapping[v] = left.n + len(mapping) - 2
    # Assign any boundary edge solely to left.
    edges = set(left.edges)
    edges.update(tuple(sorted((mapping[u], mapping[v]))) for u, v in right.edges)
    return Graph(left.n + right.n - 2, tuple(edges))


def test_every_pair_profile_in_small_balanced_graphs():
    for s in (1, 2):
        graph = c5_blowup(s)
        for roots in combinations(range(graph.n), 2):
            assert profile(graph, roots) == [s * s] * 4
    # Three pair orbits, including opposite-colored roots in one part.
    graph = c5_blowup(3)
    for roots in ((0, 1), (0, 3), (0, 6)):
        assert profile(graph, roots) == [9] * 4


def test_gluing_to_pieces_with_conflicting_boundary_preferences():
    left = c5_blowup(2)
    # Adjacent and nonadjacent roots; the same-part case has no private
    # transversal at s=2, so only its undeleted additive identity is tested.
    pieces = (Graph(3, ((0, 2), (2, 1))),
              Graph(4, ((0, 2), (2, 3), (3, 1))))
    for roots in ((0, 1), (0, 2), (0, 4)):
        for right in pieces:
            graph = glue(left, right, roots, (0, 1))
            assert deletion_distance(graph) == 4 + deletion_distance(right)
            if roots == (0, 1):
                continue
            x = {next(v for v in range(2*i, 2*i+2) if v not in roots)
                 for i in range(5)}
            keep = tuple(v for v in range(graph.n) if v not in x)
            assert deletion_distance(graph) - deletion_distance(induced(graph, keep)) == 3
    # Shared edge is counted once: R is the right piece minus that edge.
    right = c5_blowup(1)
    graph = glue(left, right, (0, 2), (0, 1))
    assert is_triangle_free(graph)
    assert deletion_distance(graph) == 4  # R is a four-edge path.


def test_same_part_roots_after_private_transversal():
    graph = c5_blowup(3)
    x = {2, 3, 6, 9, 12}
    keep = tuple(v for v in range(15) if v not in x)
    assert profile(induced(graph, keep), (0, 1)) == [4] * 4
    # Full-boundary flatness is false: the all-zero coloring has 45 edges.
    assert len(graph.edges) == 45 > deletion_distance(graph) == 9


def test_nonautomatic_critical_core_with_two_attachments():
    joined = glue(c5_blowup(2), c5_blowup(2), (0, 4), (0, 4))
    graph = Graph(20, joined.edges)  # Two isolates preserve order 5k.
    assert is_triangle_free(graph)
    assert deletion_distance(graph) == 8  # k=4; neither A nor B automatic.
    x = {1, 2, 5, 6, 8}
    keep = tuple(v for v in range(20) if v not in x)
    assert deletion_distance(induced(graph, keep)) == 5
    degrees = [sum(v in edge for edge in graph.edges) for v in range(20)]
    assert sum(d <= 3 for d in degrees) == 2
    # Criticality is checked on the unpadded graph to avoid redundant cuts.
    for edge in joined.edges:
        assert deletion_distance(Graph(joined.n, tuple(e for e in joined.edges if e != edge))) == 7
