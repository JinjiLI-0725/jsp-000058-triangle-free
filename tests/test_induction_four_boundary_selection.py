"""Audit the explicit all-size certificate and independently check small cuts."""
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path

from triangle_free.core import c5_blowup

BITS = tuple(product((0, 1), repeat=5))
NOTE = Path(__file__).resolve().parents[1] / 'notes/INDUCTION_FOUR_BOUNDARY_SELECTION.md'


def rows():
    result = {}
    for line in NOTE.read_text().splitlines():
        cells = [v.strip() for v in line.split('|')[1:-1]]
        if len(cells) != 6 or not cells[0].isdigit():
            continue
        parts, colors, m, slope, delta, bits = cells
        key = tuple(zip(map(int, parts), map(int, colors)))
        assert key not in result
        result[key] = (int(m), int(slope), int(delta), tuple(map(int, bits)))
    return result


def canonical(parts, colors):
    return min(tuple(sorted(((sign*p+rot) % 5, c^flip)
                            for p, c in zip(parts, colors)))
               for sign in (-1, 1) for rot in range(5) for flip in (0, 1))


def count_cost(s, x):
    return sum(x[i]*x[(i+1) % 5] + (s-x[i])*(s-x[(i+1) % 5])
               for i in range(5))


def template_cost(s, parts, colors, bits):
    r = [parts.count(i) for i in range(5)]
    z = [sum(p == i and c == 0 for p, c in zip(parts, colors)) for i in range(5)]
    return count_cost(s, [z[i]+bits[i]*(s-r[i]) for i in range(5)])


def test_all_size_polynomial_certificate_and_orbit_coverage():
    table = rows()
    all_orbits = {canonical(p, c)
                  for p in combinations_with_replacement(range(5), 4)
                  for c in product((0, 1), repeat=4)}
    assert set(table) == all_orbits
    assert len(table) == 47
    for row, (m, slope, delta, witness) in table.items():
        parts, colors = map(tuple, zip(*row))
        assert m == max(parts.count(i) for i in range(5))
        assert (slope, delta) in {(0, 0), (0, 2), (0, 4), (2, 0)}
        for bits in BITS:
            # Independent finite differences recover the exact quadratic.
            values = [template_cost(s, parts, colors, bits)-s*s-slope*s-delta
                      for s in range(m, m+3)]
            second = values[2]-2*values[1]+values[0]
            assert second % 2 == 0
            A = second // 2
            B = values[1]-values[0]-A
            assert min(A, B, values[0]) >= 0
            if bits == witness:
                assert values == [0, 0, 0]


def test_full_cuts_all_small_four_root_sets():
    table = rows()
    for s in (1, 2):
        graph = c5_blowup(s)
        roots_list = tuple(combinations(range(graph.n), 4))
        profiles = {roots: [len(graph.edges)+1]*16 for roots in roots_list}
        for mask in range(1 << graph.n):
            cost = sum(((mask >> u) & 1) == ((mask >> v) & 1)
                       for u, v in graph.edges)
            for roots in roots_list:
                state = sum(((mask >> v) & 1) << j for j, v in enumerate(roots))
                profiles[roots][state] = min(profiles[roots][state], cost)
        for roots, profile in profiles.items():
            parts = tuple(v // s for v in roots)
            for state, value in enumerate(profile):
                colors = tuple((state >> j) & 1 for j in range(4))
                _, slope, delta, _ = table[canonical(parts, colors)]
                assert value == s*s+slope*s+delta


def test_glued_obstruction_with_independent_part_counts_and_path_cuts():
    parts = (0, 0, 2, 2)
    for s in (3, 4, 5):
        M = 2*s+1
        minima = []
        for size in (s-1, s):
            best = 10**9
            for colors in product((0, 1), repeat=4):
                z = [sum(p == i and c == 0 for p, c in zip(parts, colors))
                     for i in range(5)]
                intervals = [range(z[i], z[i]+size-parts.count(i)+1)
                             for i in range(5)]
                # All feasible part counts, without endpoint rounding.
                piece = min(count_cost(size, x) for x in product(*intervals))
                outside = 0
                for u, v in ((colors[0], colors[1]), (colors[2], colors[3])):
                    path = min((u == a)+(a == b)+(b == v)
                               for a, b in product((0, 1), repeat=2))
                    outside += M*path
                best = min(best, piece+outside)
            minima.append(best)
        assert minima == [(s-1)**2+2*(s-1), s*s+2*s]
        assert minima[1]-minima[0] == 2*s+1
        k = (5*s+4*M+4)//5
        assert s <= k-2
        assert 2*s+1 <= 2*k-2
