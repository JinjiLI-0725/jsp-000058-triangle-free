"""Bounded independent checks of the path-selection proof; no random search."""
from itertools import combinations

from triangle_free.core import Graph, deletion_distance, is_triangle_free
from triangle_free.structural_analysis import induced


def fixture(branches, specifications, cycles=(), isolates=0):
    """Realize (endpoint, endpoint, length) paths with private interiors."""
    edges, paths, components = [], [], []
    next_vertex = branches
    for u, v, length in specifications:
        interior = tuple(range(next_vertex, next_vertex + length - 1))
        next_vertex += length - 1
        vertices = (u,) + interior + (v,)
        path_edges = tuple(zip(vertices, vertices[1:]))
        edges.extend(path_edges)
        paths.append((u, v, length, interior))
    for length in cycles:
        vertices = tuple(range(next_vertex, next_vertex + length))
        next_vertex += length
        edges.extend(zip(vertices, vertices[1:] + vertices[:1]))
        components.append(vertices)
    isolated = tuple(range(next_vertex, next_vertex + isolates))
    return (Graph(next_vertex + isolates, tuple(edges)), branches,
            tuple(paths), tuple(components), isolated)


def signed_distance(branches, paths):
    return min(sum(((cut >> u & 1) ^ (cut >> v & 1)) != length % 2
                   for u, v, length, _ in paths)
               for cut in range(1 << branches))


def remaining_distance(graph, removed):
    return deletion_distance(induced(graph, tuple(v for v in range(graph.n)
                                                if v not in removed)))


def all_subsets(vertices):
    for size in range(len(vertices) + 1):
        yield from combinations(vertices, size)


def test_exact_compression_and_every_interior_deletion():
    fixtures = [
        fixture(2, ((0, 1, 2), (0, 1, 2), (0, 1, 3), (0, 1, 3))),
        fixture(2, ((0, 1, 2), (0, 1, 3), (0, 1, 4))),
        fixture(2, ((0, 1, 1), (0, 0, 5), (1, 1, 4))),
        fixture(0, (), cycles=(5, 4), isolates=1),
        fixture(4, tuple((u, v, 3 if (u, v) in ((0, 2), (1, 3)) else 2)
                         for u, v in combinations(range(4), 2))),
    ]
    critical_statuses = set()
    subset_count = 0
    for graph, branches, paths, components, isolated in fixtures:
        assert is_triangle_free(graph)
        expected = signed_distance(branches, paths) + sum(len(c) % 2 for c in components)
        assert deletion_distance(graph) == expected
        # Compare every actual edge deletion with the compressed prediction.
        edge_distances = {
            edge: deletion_distance(Graph(graph.n, tuple(e for e in graph.edges if e != edge)))
            for edge in graph.edges
        }
        critical = all(value == expected - 1 for value in edge_distances.values())
        for i, (u, v, _, interior) in enumerate(paths):
            vertices = (u,) + interior + (v,)
            predicted = (signed_distance(branches, paths[:i] + paths[i + 1:])
                         + sum(len(c) % 2 for c in components))
            for left, right in zip(vertices, vertices[1:]):
                assert edge_distances[tuple(sorted((left, right)))] == predicted
        for vertices in components:
            for left, right in zip(vertices, vertices[1:] + vertices[:1]):
                assert edge_distances[tuple(sorted((left, right)))] == expected - len(vertices) % 2
        compressed_critical = (
            all(signed_distance(branches, paths[:i] + paths[i + 1:])
                == signed_distance(branches, paths) - 1 for i in range(len(paths)))
            and all(len(c) % 2 for c in components)
        )
        assert critical == compressed_critical
        critical_statuses.add(critical)
        interiors = tuple(v for _, _, _, interior in paths for v in interior)
        selectable = interiors + tuple(v for c in components for v in c) + isolated
        for removed_tuple in all_subsets(selectable):
            removed = set(removed_tuple)
            hit = tuple(p for p in paths if removed.intersection(p[3]))
            surviving = tuple(p for p in paths if not removed.intersection(p[3]))
            lost_cycles = sum(len(c) % 2 for c in components if removed.intersection(c))
            remainder = (signed_distance(branches, surviving)
                         + sum(len(c) % 2 for c in components) - lost_cycles)
            assert remaining_distance(graph, removed) == remainder
            gamma = expected - remainder
            budget = max(sum(((cut >> u & 1) ^ (cut >> v & 1)) != length % 2
                             for u, v, length, _ in hit)
                         for cut in range(1 << branches)) + lost_cycles
            assert 0 <= gamma <= budget <= len(hit) + lost_cycles
            subset_count += 1
    assert critical_statuses == {False, True}
    assert subset_count == 1536


def test_critical_path_losses_do_not_add():
    graph, branches, paths, _, _ = fixture(
        2, ((0, 1, 2), (0, 1, 2), (0, 1, 3), (0, 1, 3)), isolates=2)
    assert graph.n == 10 and deletion_distance(graph) == 2
    for _, _, _, interior in paths:
        assert remaining_distance(graph, {interior[0]}) == 1
    assert remaining_distance(graph, {paths[0][3][0], paths[2][3][0]}) == 1
    assert remaining_distance(graph, {paths[0][3][0], paths[1][3][0]}) == 0
    assert signed_distance(branches, paths) == 2


def test_five_separated_vertices_and_opposite_parity_selection():
    graph, _, paths, _, _ = fixture(
        2, ((0, 1, 10), (0, 1, 2), (0, 1, 3), (0, 1, 3)))
    assert graph.n == 16 and is_triangle_free(graph)
    deleted = set(paths[0][3][::2])
    assert len(deleted) == 5
    assert deletion_distance(graph) == 2
    assert remaining_distance(graph, deleted) == 1

    # The two selected paths have seven internal vertices in total, and
    # opposite parities. Every five-set in their interiors meets both.
    graph, _, paths, _, _ = fixture(
        2, ((0, 1, 4), (0, 1, 5), (0, 1, 2)))
    selectable = paths[0][3] + paths[1][3]
    assert len(selectable) == 7
    d = deletion_distance(graph)
    for deleted in combinations(selectable, 5):
        assert set(deleted).intersection(paths[0][3])
        assert set(deleted).intersection(paths[1][3])
        assert d - remaining_distance(graph, set(deleted)) == 1


def test_path_parity_with_prescribed_monochromatic_edge():
    # Enumerate actual path colorings independently of the signed formula,
    # including the parity of returning loops by allowing equal terminals.
    for length in range(1, 10):
        for right in (0, 1):
            costs = []
            singleton_positions = set()
            for cut in range(1 << (length - 1)):
                colors = (0,) + tuple(cut >> i & 1 for i in range(length - 1)) + (right,)
                mono = [i for i in range(length) if colors[i] == colors[i + 1]]
                costs.append(len(mono))
                if len(mono) == 1:
                    singleton_positions.update(mono)
            optimum = int(right != length % 2)
            assert min(costs) == optimum
            if optimum:
                assert singleton_positions == set(range(length))
