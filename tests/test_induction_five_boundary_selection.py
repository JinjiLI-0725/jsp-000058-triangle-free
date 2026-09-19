"""Audit all-size certificates and independent cuts for five retained roots."""
import json
from collections import Counter
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path

from triangle_free.core import c5_blowup

ROOT = Path(__file__).resolve().parents[1]
BITS = tuple(product((0, 1), repeat=5))
NOTE = ROOT / 'notes/INDUCTION_FIVE_BOUNDARY_SELECTION.md'


def canonical(parts, colors):
    return min(tuple(sorted(((sign*p+rot) % 5, c ^ flip)
                            for p, c in zip(parts, colors)))
               for sign in (-1, 1) for rot in range(5) for flip in (0, 1))


def profiles():
    data = json.loads((ROOT / 'results/induction_five_boundary/profiles.json').read_text())
    result = {}
    for row in data['rows']:
        key = tuple(zip(map(int, row['parts']), map(int, row['colors'])))
        assert key not in result
        result[key] = row
    assert data['orbits'] == len(result) == 111
    return result


def coefficients(parts, colors, bits):
    r = [parts.count(j) for j in range(5)]
    z = [sum(p == j and c == 0 for p, c in zip(parts, colors)) for j in range(5)]
    v = [z[j]-bits[j]*r[j] for j in range(5)]
    A = sum(bits[j]*bits[(j+1) % 5]+(1-bits[j])*(1-bits[(j+1) % 5])
            for j in range(5))
    L = sum((2*bits[j]-1)*v[(j+1) % 5]+(2*bits[(j+1) % 5]-1)*v[j]
            for j in range(5))
    H = 2*sum(v[j]*v[(j+1) % 5] for j in range(5))
    return A, L, H


def count_cost(t, counts):
    return sum(counts[j]*counts[(j+1) % 5]
               +(t-counts[j])*(t-counts[(j+1) % 5]) for j in range(5))


def direct_profile(t, parts, colors):
    zeros = [sum(p == j and c == 0 for p, c in zip(parts, colors)) for j in range(5)]
    intervals = [range(zeros[j], zeros[j]+t-parts.count(j)+1) for j in range(5)]
    return min(count_cost(t, x) for x in product(*intervals))


def certified_profile(t, row):
    values = [t*t+r['slope']*t+r['constant'] for r in row['regions']
              if r['lo'] <= t and (r['hi'] is None or t <= r['hi'])]
    assert values and len(set(values)) == 1
    return values[0]


def test_all_size_certificate_and_complete_orbit_coverage():
    table = profiles()
    expected = {canonical(p, c)
                for p in combinations_with_replacement(range(5), 5)
                for c in BITS}
    assert set(table) == expected
    histogram = Counter()
    for key, row in table.items():
        parts, colors = map(tuple, zip(*key))
        m = max(parts.count(j) for j in range(5))
        assert row['minimum_size'] == m == row['regions'][0]['lo']
        if len(row['regions']) == 2:
            assert (row['parts'], row['colors']) == ('00113', '00001')
            assert [(r['lo'], r['hi'], r['slope'], r['constant'])
                    for r in row['regions']] == [(2, 4, 2, 0), (4, None, 0, 8)]
            histogram['piecewise'] += 1
        else:
            assert len(row['regions']) == 1
            assert row['regions'][0]['hi'] is None
            r = row['regions'][0]
            histogram[r['slope'], r['constant']] += 1
        for r in row['regions']:
            lo, hi, slope, delta = (r[n] for n in ('lo', 'hi', 'slope', 'constant'))
            witness = tuple(map(int, r['bits']))
            assert witness in BITS
            assert coefficients(parts, colors, witness) == (1, slope, delta)
            for bits in BITS:
                A, L, H = coefficients(parts, colors, bits)
                if hi is None:
                    # Integer Newton basis u(u-1), u, 1. This checks all t>=lo.
                    assert min(A-1, (2*lo+1)*(A-1)+L-slope,
                               lo*lo*(A-1)+lo*(L-slope)+H-delta) >= 0
                else:
                    assert all((A-1)*t*t+(L-slope)*t+H-delta >= 0
                               for t in range(lo, hi+1))
    assert histogram == {(0, 0): 66, (0, 2): 18, (0, 4): 11, (0, 6): 2,
                         (2, 0): 12, (2, 2): 1, 'piecewise': 1}


def test_every_small_five_root_profile_by_full_vertex_cuts():
    table = profiles()
    for t in (1, 2):
        graph = c5_blowup(t)
        root_sets = tuple(combinations(range(graph.n), 5))
        exact = {roots: [len(graph.edges)+1]*32 for roots in root_sets}
        for mask in range(1 << graph.n):
            cost = sum((mask >> u & 1) == (mask >> v & 1) for u, v in graph.edges)
            for roots in root_sets:
                state = sum((mask >> v & 1) << i for i, v in enumerate(roots))
                exact[roots][state] = min(exact[roots][state], cost)
        for roots, values in exact.items():
            parts = tuple(v // t for v in roots)
            for state, cost in enumerate(values):
                colors = tuple(state >> i & 1 for i in range(5))
                assert cost == certified_profile(t, table[canonical(parts, colors)])


def budget_rows():
    result = []
    for line in NOTE.read_text().splitlines():
        cells = [s.strip() for s in line.split('|')[1:-1]]
        if len(cells) != 7 or not cells[0].isdigit():
            continue
        p, a, m, actions, c, bound, target = cells
        parsed = []
        # Protect the comma inside a two-root action before splitting actions.
        for action in actions.replace('{0,4}', '{0;4}').split(', '):
            ids, delta = action.split(':')
            ids = tuple(map(int, ids.strip('{}').split(';')))
            parsed.append((ids, int(delta)))
        result.append((tuple(map(int, p)), tuple(map(int, a)), int(m),
                       tuple(parsed), int(c), int(bound), int(target)))
    return result


def neighborhoods(parts):
    return tuple(mask for mask in range(32)
                 if all(not(mask >> i & 1 and mask >> j & 1)
                        for i in range(5) for j in range(i)
                        if (parts[i]-parts[j]) % 5 in (1, 4)))


def test_all_budget_actions_and_independent_neighborhood_inequalities():
    table = profiles()
    cases = budget_rows()
    assert len(cases) == 14
    assert {canonical(p, a) for p, a, *_ in cases} == {
        key for key, row in table.items()
        if any(region['slope'] for region in row['regions'])}
    for parts, colors, m, actions, c, bound, target in cases:
        row = table[canonical(parts, colors)]
        assert row['minimum_size'] == m
        assert target == certified_profile(m, row)-m*m
        for ids, delta in actions:
            flipped = tuple(a ^ (i in ids) for i, a in enumerate(colors))
            regions = table[canonical(parts, flipped)]['regions']
            assert len(regions) == 1
            assert (regions[0]['slope'], regions[0]['constant']) == (0, delta)
        contributions = [sum((1 if colors[i] != y else -1)
                             for ids, _ in actions for i in ids if mask >> i & 1)
                         for mask in neighborhoods(parts) for y in (0, 1)]
        assert max(contributions) == c
        assert bound == (5*c+sum(delta for _, delta in actions)) // len(actions)
        assert bound <= target


def test_piecewise_profile_and_nested_optima_in_fixed_gluings():
    table = profiles()
    for parts, colors in (((0, 0, 1, 1, 3), (0, 0, 0, 0, 1)),
                          ((0, 1, 2, 3, 4), (0, 0, 0, 0, 0))):
        m = max(parts.count(j) for j in range(5))
        for t in range(m, 7):
            exact = direct_profile(t, parts, colors)
            assert exact == certified_profile(t, table[canonical(parts, colors)])
            expected = min(2*t, 8) if m == 2 else 2*t+2
            assert exact-t*t == expected

    for parts, _, m, *_ in budget_rows():
        allowed = neighborhoods(parts)
        fixtures = (
            (tuple(1 << i for i in range(5)),
             ((0, 1), (1, 2), (2, 3), (3, 4), (0, 4))),
            (tuple(allowed[-1-i % len(allowed)] for i in range(5)), ()),
        )
        for attachments, edges in fixtures:
            assert all(mask in allowed for mask in attachments)
            assert all(not attachments[u] & attachments[v] for u, v in edges)
            outside = {a: min(sum(y[u] == y[v] for u, v in edges)
                              +sum(a[i] == y[v] for v, mask in enumerate(attachments)
                                   for i in range(5) if mask >> i & 1)
                              for y in BITS) for a in BITS}
            direct = [{a: direct_profile(t, parts, a) for a in BITS}
                      for t in (m, m+1)]
            optima = [min(values[a]+outside[a] for a in BITS) for values in direct]
            flat = [a for a in BITS
                    if len(table[canonical(parts, a)]['regions']) == 1
                    and table[canonical(parts, a)]['regions'][0]['slope'] == 0]
            a = min(flat, key=lambda a: direct[0][a]+outside[a])
            delta = table[canonical(parts, a)]['regions'][0]['constant']
            assert optima == [t*t+delta+outside[a] for t in (m, m+1)]
            # Find a witness in original coordinates rather than transporting
            # the canonical certificate's bit string through symmetries.
            bits = next(b for b in BITS if coefficients(parts, a, b) == (1, 0, delta))
            r = [parts.count(j) for j in range(5)]
            z = [sum(p == j and c == 0 for p, c in zip(parts, a)) for j in range(5)]
            costs = [count_cost(t, [z[j]+bits[j]*(t-r[j]) for j in range(5)])
                     +outside[a] for t in (m, m+1)]
            assert costs == optima
            assert costs[0]-optima[0] == 0  # q=0
            assert costs[1]-costs[0] == 2*(m+1)-1
