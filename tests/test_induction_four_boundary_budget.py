"""Audit the five-outside-vertex recoloring certificate, not an extension search."""
from itertools import product

from test_induction_four_boundary_selection import canonical, count_cost, rows


CASES = (
    ((0, 0, 2, 2), (0, 1, 0, 1), 2, (0, 0, 0, 0), 2),
    ((0, 0, 2, 3), (0, 1, 0, 0), 2, (2, 0, 0, 0), 2),
    ((0, 1, 2, 3), (0, 0, 1, 1), 1, (0, 2, 2, 0), 1),
)
COLORS = tuple(product((0, 1), repeat=4))


def neighborhoods(parts):
    return tuple(mask for mask in range(16)
                 if all(not (mask >> i & 1 and mask >> j & 1)
                        for i in range(4) for j in range(i)
                        if (parts[i]-parts[j]) % 5 in (1, 4)))


def test_flip_profiles_and_all_local_outside_budgets():
    table = rows()
    assert {canonical(p, a) for p, a, _, _, _ in CASES} == {
        key for key, (_, slope, _, _) in table.items() if slope == 2
    }
    for parts, colors, m, penalties, budget in CASES:
        assert table[canonical(parts, colors)][:3] == (m, 2, 0)
        for i, delta in enumerate(penalties):
            flipped = tuple(a ^ (j == i) for j, a in enumerate(colors))
            assert table[canonical(parts, flipped)][:3] == (m, 0, delta)
        contributions = {
            tuple((1 if colors[i] != color else -1) if mask >> i & 1 else 0
                  for i in range(4))
            for mask in neighborhoods(parts) for color in (0, 1)
        }
        assert max(map(sum, contributions)) == budget
        # Enumerate reachable cost vectors, not graphs: the outside internal
        # edges cancel when its coloring is kept fixed, whatever those edges.
        reachable = {(0, 0, 0, 0)}
        for n in range(6):
            bound = (budget*n + sum(penalties)) // 4
            assert bound <= 2*m
            for vector in reachable:
                assert min(d+p for d, p in zip(vector, penalties)) <= bound
            if n < 5:
                reachable = {tuple(x+y for x, y in zip(v, w))
                             for v in reachable for w in contributions}


def direct_piece_profile(size, parts, colors):
    # Enumerate every feasible count, independently of the endpoint templates
    # and polynomial classification used in the proof.
    zeros = [sum(p == i and a == 0 for p, a in zip(parts, colors))
             for i in range(5)]
    intervals = [range(zeros[i], zeros[i]+size-parts.count(i)+1)
                 for i in range(5)]
    return min(count_cost(size, counts) for counts in product(*intervals))


def test_glued_minima_and_optimal_remainder_extension():
    table = rows()
    for parts, _, m, _, _ in CASES:
        allowed = neighborhoods(parts)
        # Fixed examples with five outside vertices, including nonempty
        # outside edges. No random generation or exhaustive extension search.
        examples = (
            (tuple(1 << i for i in range(4)) + (0,),
             ((0, 1), (1, 2), (2, 3), (3, 4), (0, 4))),
            (tuple(allowed[-1-i % len(allowed)] for i in range(5)), ()),
        )
        for attachments, outside_edges in examples:
            assert all(mask in allowed for mask in attachments)
            assert all(not attachments[u] & attachments[v]
                       for u, v in outside_edges)
            outside_profile = {}
            for colors in COLORS:
                outside_profile[colors] = min(
                    sum(y[u] == y[v] for u, v in outside_edges)
                    + sum(colors[i] == y[v] for v, mask in enumerate(attachments)
                          for i in range(4) if mask >> i & 1)
                    for y in product((0, 1), repeat=5)
                )
            minima = []
            for size in (m, m+1):
                direct = {a: direct_piece_profile(size, parts, a)
                          for a in COLORS}
                optimum = min(direct[a]+outside_profile[a] for a in COLORS)
                flat = min(size*size+table[canonical(parts, a)][2]
                           + outside_profile[a] for a in COLORS
                           if table[canonical(parts, a)][1] == 0)
                assert optimum == flat
                minima.append(optimum)
            s = m+1
            assert minima[1]-minima[0] == 2*s-1
            # Construct a nested optimum and check q=0 and extension cost.
            a = min((a for a in COLORS if table[canonical(parts, a)][1] == 0),
                    key=lambda a: table[canonical(parts, a)][2]+outside_profile[a])
            # Work in original coordinates: find a template by full endpoint
            # enumeration instead of transporting a canonical row's bits.
            z = [sum(p == i and c == 0 for p, c in zip(parts, a)) for i in range(5)]
            r = [parts.count(i) for i in range(5)]
            delta = table[canonical(parts, a)][2]
            witness = next(bits for bits in product((0, 1), repeat=5)
                           if all(count_cost(t, [z[i]+bits[i]*(t-r[i])
                                                for i in range(5)]) == t*t+delta
                                  for t in (s-1, s)))
            costs = [count_cost(t, [z[i]+witness[i]*(t-r[i]) for i in range(5)])
                     + outside_profile[a] for t in (s-1, s)]
            assert costs == minima
            assert costs[0]-minima[0] == 0
            assert costs[1]-costs[0] == 2*s-1
