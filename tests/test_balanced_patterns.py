"""Targeted coverage regressions, not a repeat of the balanced enumeration."""

import json
from itertools import combinations, product
from pathlib import Path

from triangle_free.balanced_patterns import extension_graph, mixed_extension_distance
from triangle_free.core import deletion_distance, is_triangle_free


def test_cover_bound_on_all_five_vertex_triangle_free_graphs():
    """Check the combinatorial ingredients, not extension enumerations."""
    pairs = tuple(combinations(range(5), 2))
    count = 0
    for mask in range(1 << len(pairs)):
        edges = tuple(edge for i, edge in enumerate(pairs) if mask >> i & 1)
        if any(all(edge in edges for edge in combinations(triple, 2))
               for triple in combinations(range(5), 3)):
            continue
        count += 1
        degrees = [sum(v in edge for edge in edges) for v in range(5)]
        maximum_degree = max(degrees)
        assert len(edges) <= 6
        assert len(edges) <= 4 or maximum_degree <= 3
        for subset in range(32):
            induced = [(u, v) for u, v in edges
                       if subset >> u & 1 and subset >> v & 1]
            cover = min(c.bit_count() for c in range(32)
                        if c & ~subset == 0
                        and all(c >> u & 1 or c >> v & 1 for u, v in induced))
            assert len(induced) <= maximum_degree * cover
    assert count == 388


def test_type_overlap_identity_and_averaging_threshold_obstruction():
    cycle = tuple((i, (i + 1) % 5) for i in range(5))
    # Independently construct each cut by its sole monochromatic cycle edge.
    cuts = []
    for sole in range(5):
        cut = next(c for c in product(range(2), repeat=5)
                   if c[0] == 0 and all(
                       (c[u] == c[v]) == (i == sole)
                       for i, (u, v) in enumerate(cycle)))
        cuts.append(cut)
    allowed = [set(((i - 1) % 5, (i + 1) % 5)) for i in range(5)]
    for u, v in product(range(5), repeat=2):
        weight = sum(c[u] == c[v] for c in cuts)
        assert weight == 1 + 2 * len(allowed[u] & allowed[v])
    # Star: all four edges share one allowed part; its minimum cover is 1.
    star = tuple((0, v) for v in range(1, 5))
    types = (0, 2, 2, 2, 2)
    weight = sum(c[types[u]] == c[types[v]] for c in cuts for u, v in star)
    cover_sum = 0
    for j in range(5):
        support = {v for v in range(5) if j in allowed[types[v]]}
        induced = [(u, v) for u, v in star if u in support and v in support]
        cover_sum += min(c.bit_count() for c in range(32)
                         if all(c >> u & 1 or c >> v & 1 for u, v in induced))
    assert (weight, cover_sum) == (12, 1)
    assert weight - 8 * cover_sum == 4
    assert weight - 7 * cover_sum == 5


def test_mixed_part_has_no_homogeneous_triangle_free_supergraph():
    # F contains xy. Two vertices in A_1 attach separately to x and y.
    edges = ((0, 1),)
    patterns = ((0, 0), (1, 2), (0, 0), (0, 0), (0, 0))
    graph = extension_graph(edges, patterns)
    assert is_triangle_free(graph)
    # Any common neighborhood containing both original neighborhoods has xy.
    for common in range(32):
        if common & 1 and common & 2:
            completed = list(patterns)
            completed[1] = (common, common)
            assert not is_triangle_free(extension_graph(edges, completed))
    assert mixed_extension_distance(edges, patterns) == deletion_distance(graph)


def test_sorted_unary_identity_against_independent_full_cuts():
    cycle = ((0, 1), (1, 2), (2, 3), (3, 4), (4, 0))
    masks = tuple((1 << ((j-1) % 5)) | (1 << ((j+1) % 5)) for j in range(5))
    cases = [
        (cycle, tuple((mask,) for mask in masks)),
        (cycle, tuple((mask, mask) for mask in masks)),
        (cycle, tuple((mask, mask & -mask) for mask in masks)),
        (((0, 1),), ((0, 0), (1, 2), (0, 0), (0, 0), (1, 2))),
        ((), ((31, 0), (0, 0), (31, 0), (0, 0), (0, 0))),
    ]
    for edges, patterns in cases:
        graph = extension_graph(edges, patterns)
        assert is_triangle_free(graph)
        assert mixed_extension_distance(edges, patterns) == deletion_distance(graph)


def test_completed_homogeneous_artifacts_without_rerunning_search():
    root = Path(__file__).resolve().parents[1]
    for t in range(1, 26):
        result = json.loads((root / f"results/balanced_extension/t{t}.json").read_text())
        assert result["t"] == t and result["complete"]
        assert result["triangle_free_graphs"] == 388
        assert result["next_configuration"] == result["configurations_checked"] == 242500
        assert result["maximal_neighborhood_configurations_checked"] == 1245367
        assert result["max_gap"] == 0
