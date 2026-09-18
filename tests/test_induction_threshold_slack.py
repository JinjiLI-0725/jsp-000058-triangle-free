"""Bounded inference checks for the uniform-budget threshold theorem."""
from itertools import combinations

from triangle_free.core import Graph, c5_blowup, deletion_distance
from triangle_free.structural_analysis import induced


def cut_rows(graph):
    return [frozenset((u, v) for u, v in graph.edges
                      if (c >> u & 1) == (c >> v & 1))
            for c in range(1 << graph.n)]


def check_set(graph, cuts, d, vertices):
    x = set(vertices)
    remainder = sorted(set(range(graph.n)) - x)
    h = sum(u in x and v in x for u, v in graph.edges)
    z = sum((u in x) != (v in x) for u, v in graph.edges)
    dx = deletion_distance(induced(graph, sorted(x)))
    budget = min((h + z) // 2, dx + z // 2)
    dh = deletion_distance(induced(graph, remainder))
    gamma = d - dh
    rows = []
    by_remainder = {}
    for coloring, mono in enumerate(cuts):
        r = sum(u in x or v in x for u, v in mono)
        slack = len(mono) - d
        rows.append((slack, r - slack))
        key = tuple(coloring >> v & 1 for v in remainder)
        by_remainder[key] = min(by_remainder.get(key, len(graph.edges) + 1), r)
    assert len(by_remainder) == 1 << len(remainder)
    assert max(by_remainder.values()) <= budget
    lower = max(score for slack, score in rows if slack == 0)
    assert max(score for slack, score in rows) == gamma
    assert min(slack for slack, score in rows if score == gamma) <= budget - gamma
    assert max(score for slack, score in rows if slack <= budget - lower) == gamma
    for threshold in range(budget + 2):
        passes_window = all(score <= threshold for slack, score in rows
                            if slack <= budget - threshold - 1)
        assert passes_window == (gamma <= threshold)
        if budget <= threshold + 1 and lower <= threshold:
            assert gamma <= threshold
    return budget, gamma, lower


def petersen():
    return Graph(10, tuple(e for i in range(5) for e in
                          ((i, (i + 1) % 5), (i, i + 5),
                           (i + 5, 5 + (i + 2) % 5))))


def test_budget_window_on_all_five_sets_of_fixed_graphs():
    graphs = [petersen(), c5_blowup(2),
              Graph(10, tuple((i, (i + 1) % 5) for i in range(5))),
              Graph(10, tuple((u, v) for u in range(5) for v in range(5, 10)))]
    for graph in graphs:
        cuts = cut_rows(graph)
        d = deletion_distance(graph)
        for x in combinations(range(10), 5):
            check_set(graph, cuts, d, x)


def test_positive_slack_obstruction_survives_budget_localization():
    graph = petersen()
    budget, gamma, lower = check_set(graph, cut_rows(graph), 3, {0, 1, 3, 8})
    assert (budget, gamma, lower) == (4, 3, 2)
    # At T=2 the exact window includes slack one; optimal cuts alone fail.
    assert budget - 2 - 1 == 1
