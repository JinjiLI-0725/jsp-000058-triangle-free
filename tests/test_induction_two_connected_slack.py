"""Exact boundary tables for one symbolic family; no general graph search."""
from itertools import product

from triangle_free.core import Graph, c5_blowup, is_triangle_free
from test_induction_slack_amplification import gadget

Y = (0, 1, 3, 8)


def keep_min(table, remainder, cost):
    table[remainder] = min(table.get(remainder, cost), cost)


def q_tables():
    graph = gadget()
    tables = {bits: {} for bits in product(range(2), repeat=4)}
    optimal_edges = set()
    equal_terminal_optimum = False
    for cut in range(1 << graph.n):
        bits = tuple(cut >> v & 1 for v in Y)
        mono = {e for e in graph.edges if (cut >> e[0] & 1) == (cut >> e[1] & 1)}
        remainder = sum(u not in Y and v not in Y for u, v in mono)
        keep_min(tables[bits], remainder, len(mono))
        if len(mono) == 3:
            optimal_edges.update(mono)
            equal_terminal_optimum |= bits[0] == bits[1]
    assert optimal_edges == set(graph.edges)
    assert equal_terminal_optimum
    return tables


def balanced_tables(h):
    # Every coloring is represented: the three deleted vertices of A0
    # are distinguished, and all other vertices have identical adjacency
    # within their respective parts. Multiplicities do not affect minima.
    tables = {bits: {} for bits in product(range(2), repeat=2)}
    for bits in product(range(2), repeat=3):
        for counts in product(range(h - 2), *([range(h + 1)] * 4)):
            full = (counts[0] + sum(bits),) + counts[1:]
            cost = sum(full[i] * full[(i + 1) % 5]
                       + (h - full[i]) * (h - full[(i + 1) % 5])
                       for i in range(5))
            sizes = (h - 3, h, h, h, h)
            remainder = sum(counts[i] * counts[(i + 1) % 5]
                            + (sizes[i] - counts[i])
                            * (sizes[(i + 1) % 5] - counts[(i + 1) % 5])
                            for i in range(5))
            keep_min(tables[bits[:2]], remainder, cost)
    return tables


def join_tables(left, right):
    joined = {}
    for r, b in left.items():
        for rr, bb in right.items():
            keep_min(joined, r + rr, b + bb)
    return joined


def family_graph(a, h):
    q = gadget()
    edges = []
    next_vertex = 4
    first = None
    for _ in range(a):
        mapping = dict(zip(Y, range(4)))
        for v in range(q.n):
            if v not in mapping:
                mapping[v] = next_vertex
                next_vertex += 1
        edges.extend(tuple(sorted((mapping[u], mapping[v]))) for u, v in q.edges)
        if first is None:
            first = mapping
    b = c5_blowup(h)
    mapping = {0: 0, 1: 1}
    for v in range(b.n):
        if v not in mapping:
            mapping[v] = next_vertex
            next_vertex += 1
    deleted = set(range(4)) | {mapping[2]}
    edges.extend(tuple(sorted((mapping[u], mapping[v]))) for u, v in b.edges)
    u, v = first[7], first[9]
    edges.remove(tuple(sorted((u, v))))
    path = [u] + list(range(next_vertex, next_vertex + 8)) + [v]
    edges.extend(zip(path, path[1:]))
    return Graph(next_vertex + 8, tuple(edges)), deleted


def test_two_connected_threshold_false_positives():
    qt = q_tables()
    for a in (1, 2, 3):
        jt = {}
        for bits, table in qt.items():
            joined = {0: 0}
            for _ in range(a):
                joined = join_tables(joined, table)
            jt[bits] = joined
        for offset, strict in ((3, True), (4, False)):
            h = a + offset
            bt = balanced_tables(h)
            states = {}
            for bits, table in jt.items():
                for r, b in join_tables(table, bt[bits[:2]]).items():
                    keep_min(states, r, b)
            d = min(states.values())
            remainder_d = min(states)
            gamma = d - remainder_d
            k = 2 * a + h + 2
            threshold = 2 * k - (2 if strict else 1)
            assert d == 3 * a + h * h >= 2 * k
            assert remainder_d == h * (h - 3)
            assert gamma == 3 * a + 3 * h == threshold + 1
            assert max(d - r for r, b in states.items() if b == d) == 2 * a + 3 * h
            assert states[remainder_d] - d == a
            # For each remainder cost the cheapest full coloring decides
            # whether ANY cut of that score fits the specified slack window.
            assert max(d - r for r, b in states.items() if b - d < a) <= threshold
            assert max(d - r for r, b in states.items() if b - d <= a) > threshold

            graph, deleted = family_graph(a, h)
            assert graph.n == 5 * k and len(deleted) == 5
            assert is_triangle_free(graph)
            adjacency = [set() for _ in range(graph.n)]
            for u, v in graph.edges:
                adjacency[u].add(v)
                adjacency[v].add(u)
            # Independent graph test: no articulation vertex.
            for removed in range(graph.n):
                start = next(v for v in range(graph.n) if v != removed)
                seen, stack = {start}, [start]
                while stack:
                    for v in adjacency[stack.pop()] - {removed} - seen:
                        seen.add(v)
                        stack.append(v)
                assert len(seen) == graph.n - 1


def test_nine_edge_path_parities_and_witness_positions():
    for left, right in product(range(2), repeat=2):
        rows = []
        for middle in product(range(2), repeat=8):
            colors = (left,) + middle + (right,)
            mono = {i for i in range(9) if colors[i] == colors[i + 1]}
            rows.append(mono)
        minimum = int(left == right)
        assert min(map(len, rows)) == minimum
        if minimum:
            assert {next(iter(row)) for row in rows if len(row) == 1} == set(range(9))
        # Five consecutive internal vertices can always be restored at
        # incident cost <=1, for any fixed colors outside them.
    for left, right in product(range(2), repeat=2):
        costs = []
        for deleted_colors in product(range(2), repeat=5):
            colors = (left,) + deleted_colors + (right,)
            costs.append(sum(colors[i] == colors[i + 1] for i in range(6)))
        assert min(costs) <= 1
