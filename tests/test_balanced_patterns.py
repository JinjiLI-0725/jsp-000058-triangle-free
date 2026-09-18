"""Targeted coverage regressions, not a repeat of the balanced enumeration."""

import json
from pathlib import Path

from triangle_free.balanced_patterns import extension_graph, mixed_extension_distance
from triangle_free.core import deletion_distance, is_triangle_free


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
