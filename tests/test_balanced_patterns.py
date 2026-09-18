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


def test_t7_exceptional_types_force_unbalanced_compatible_containment():
    """Audit only the two exceptional F shapes, not extension enumeration.

    Union all patterns allowed by the total surplus budget. A compatible
    type map for these unions also works for every actual mixed assignment.
    Compute W from actual cuts, independently of the cover identity.
    """
    cycle = tuple((i, (i + 1) % 5) for i in range(5))
    cuts = [c for c in product(range(2), repeat=5) if c[0] == 0
            and sum(c[u] == c[v] for u, v in cycle) == 1]
    maps = [(0,) + tail for tail in product(range(5), repeat=4)]
    shapes = (
        (tuple((0, v) for v in range(1, 5)), {(1, 12, 0): 2, (2, 20, 1): 1}),
        (tuple((u, v) for u in (0, 1) for v in (2, 3, 4)), {(1, 12, 0): 8}),
    )
    for edges, expected in shapes:
        exceptions = {}
        for types in maps:
            supports = [sum(1 << v for v in range(5)
                            if (types[v] - j) % 5 in (1, 4)) for j in range(5)]
            patterns = [[i for i in range(32) if not i & ~s
                         and all(not (i >> u & 1 and i >> v & 1)
                                 for u, v in edges)] for s in supports]
            alpha = [max(i.bit_count() for i in part) for part in patterns]
            cover_sum = 10 - sum(alpha)
            weight = sum(c[types[u]] == c[types[v]] for c in cuts for u, v in edges)
            budget = weight - 5 - 7 * cover_sum
            if not cover_sum or budget < 0:
                continue
            key = cover_sum, weight, budget
            exceptions[key] = exceptions.get(key, 0) + 1
            unions = []
            for maximum, part in zip(alpha, patterns):
                union = 0
                for pattern in part:
                    if maximum - pattern.bit_count() <= budget:
                        union |= pattern
                unions.append(union)
            # At least one compatible map supports every possible actual edge.
            # Rotation permits fixing the first type to zero only in the
            # original classification; the new map uses fixed H part labels.
            witness = next((new for new in product(range(5), repeat=5)
                            if all((new[u] - new[v]) % 5 in (1, 4) for u, v in edges)
                            and all(not (union >> v & 1) or (new[v] - j) % 5 in (1, 4)
                                    for j, union in enumerate(unions) for v in range(5))), None)
            assert witness is not None
            sizes = [7 + witness.count(j) for j in range(5)]
            assert max(sizes) >= 10
            assert min(sizes[j] * sizes[(j + 1) % 5] for j in range(5)) <= 63
        assert exceptions == expected


def test_t6_exceptions_admit_bounded_repair_for_all_mixed_patterns():
    """Audit repaired blow-up bounds under the exact global loss budget.

    Enumerate only three internal shapes and type maps. A small knapsack
    bounds every assignment of 30 individual patterns, including mixed and
    nonmaximal patterns. No full extension enumeration or MaxCut search.
    """
    cycle = tuple((i, (i + 1) % 5) for i in range(5))
    cuts = [c for c in product(range(2), repeat=5) if c[0] == 0
            and sum(c[u] == c[v] for u, v in cycle) == 1]
    shapes = (
        tuple((0, v) for v in range(1, 5)),
        ((0, 2), (0, 3), (0, 4), (1, 2), (1, 3)),
        tuple((u, v) for u in (0, 1) for v in (2, 3, 4)),
    )
    for edges in shapes:
        compatible = [new for new in product(range(5), repeat=5)
                      if all((new[u] - new[v]) % 5 in (1, 4) for u, v in edges)]
        exceptions = 0
        for tail in product(range(5), repeat=4):
            types = (0,) + tail
            supports = [sum(1 << v for v in range(5)
                            if (types[v] - j) % 5 in (1, 4)) for j in range(5)]
            patterns = [[i for i in range(32) if not i & ~support
                         and all(not (i >> u & 1 and i >> v & 1)
                                 for u, v in edges)] for support in supports]
            alpha = [max(i.bit_count() for i in part) for part in patterns]
            cover_sum = 10 - sum(alpha)
            weight = sum(c[types[u]] == c[types[v]] for c in cuts for u, v in edges)
            budget = weight - 6 * cover_sum - 5
            if cover_sum == 0 or budget < 0:
                continue
            exceptions += 1
            assert budget <= (3 if len(edges) == 4 else len(edges) - 5)
            certified = False
            for new in compatible:
                sizes = [6 + new.count(j) for j in range(5)]
                blowup_bound = min(sizes[j] * sizes[(j + 1) % 5] for j in range(5))
                # The proof supplies a cut of cost 36 before repair.
                if blowup_bound != 36:
                    continue
                dp = {0: 0}
                for j, part in enumerate(patterns):
                    allowed = sum(1 << v for v in range(5)
                                  if (new[v] - j) % 5 in (1, 4))
                    options = {(alpha[j] - i.bit_count(), (i & ~allowed).bit_count())
                               for i in part if alpha[j] - i.bit_count() <= budget}
                    for _ in range(6):
                        updated = {}
                        for spent, removed in dp.items():
                            for loss, extra in options:
                                if spent + loss <= budget:
                                    key = spent + loss
                                    updated[key] = max(updated.get(key, -1), removed + extra)
                        dp = updated
                assert dp
                repair_bound = 1 if len(edges) == 4 else 2 * (len(edges) - 5)
                if max(dp.values()) <= repair_bound:
                    certified = True
                    break
            assert certified, (edges, types, cover_sum, weight, budget)
        assert exceptions > 0
