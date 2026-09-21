#!/usr/bin/env python3
"""Reduced exact enumeration for the four abstract L11 core shapes.

Isolated core vertices are represented by multiplicities of the eleven
independent C5-neighbourhoods.  Orbit counts use Burnside's lemma; minima use
the additive isolated-vertex formula except for the one genuinely coupled
matching support case.  No labelled isolated assignments or graphs are
enumerated.
"""
from collections import Counter
from functools import lru_cache
import itertools
import json
from pathlib import Path


TYPES = (0,) + tuple(1 << i for i in range(5)) + tuple(
    (1 << i) | (1 << ((i + 2) % 5)) for i in range(5))
TYPE_INDEX = {mask: i for i, mask in enumerate(TYPES)}
SHAPES = {
    'zero': (),
    'one': ((0, 1),),
    'path': ((0, 1), (1, 2)),
    'matching': ((0, 1), (2, 3)),
}

ASSIGNMENTS = []
for bad in range(5):
    for eps in (0, 1):
        assignment = [0] * 5
        assignment[bad] = eps
        for offset in range(1, 5):
            assignment[(bad + offset) % 5] = eps ^ (offset & 1)
        ASSIGNMENTS.append(tuple(assignment))


def transform_type(type_index, vertex_permutation):
    mask = TYPES[type_index]
    transformed = sum(1 << vertex_permutation[i]
                      for i in range(5) if mask >> i & 1)
    return TYPE_INDEX[transformed]


D5 = []
for reflected in (False, True):
    for rotation in range(5):
        vertex_permutation = tuple(
            (rotation + (-i if reflected else i)) % 5 for i in range(5))
        D5.append(tuple(transform_type(i, vertex_permutation)
                        for i in range(len(TYPES))))


def shape_size(edges):
    return max((v for edge in edges for v in edge), default=-1) + 1


def shape_automorphisms(edges):
    n = shape_size(edges)
    if n == 0:
        return [()]
    target = {tuple(sorted(edge)) for edge in edges}
    return [permutation for permutation in itertools.permutations(range(n))
            if {tuple(sorted((permutation[u], permutation[v])))
                for u, v in edges} == target]


def endpoint_tuples(edges):
    n = shape_size(edges)
    for endpoint in itertools.product(range(len(TYPES)), repeat=n):
        if all(not (TYPES[endpoint[u]] & TYPES[endpoint[v]])
               for u, v in edges):
            yield endpoint


def fixed_multiplicity_weight_distribution(type_permutation, slots):
    """DP for multiplicity vectors fixed by one D5 element."""
    unseen = set(range(len(TYPES)))
    cycles = []
    while unseen:
        start = min(unseen)
        cycle = []
        q = start
        while q in unseen:
            unseen.remove(q)
            cycle.append(q)
            q = type_permutation[q]
        cycles.append(cycle)

    dp = {(0, 0): 1}
    for cycle in cycles:
        length = len(cycle)
        weight = TYPES[cycle[0]].bit_count()
        nxt = Counter()
        for (used, boundary), count in dp.items():
            for multiplicity in range((slots - used) // length + 1):
                nxt[(used + length * multiplicity,
                     boundary + length * weight * multiplicity)] += count
        dp = nxt
    return Counter({boundary: count for (used, boundary), count in dp.items()
                    if used == slots})


def fixed_endpoint_weight_distribution(edges, type_permutation,
                                       shape_permutation):
    out = Counter()
    for endpoint in endpoint_tuples(edges):
        fixed = all(endpoint[shape_permutation[i]] ==
                    type_permutation[endpoint[i]]
                    for i in range(len(endpoint)))
        if fixed:
            out[sum(TYPES[t].bit_count() for t in endpoint)] += 1
    return out


def feasible_state_count(endpoint_weights, multiplicity_weights):
    return sum(endpoint_count * multiplicity_count
               for endpoint_weight, endpoint_count in endpoint_weights.items()
               for multiplicity_weight, multiplicity_count
               in multiplicity_weights.items()
               if endpoint_weight + multiplicity_weight >= 9)


def state_and_orbit_counts(edges):
    n = shape_size(edges)
    slots = 10 - n
    automorphisms = shape_automorphisms(edges)
    burnside_sum = 0
    raw = None
    identity_type = tuple(range(len(TYPES)))
    identity_shape = tuple(range(n))
    multiplicity_cache = {}
    for type_permutation in D5:
        key = (type_permutation, slots)
        multiplicity_cache.setdefault(
            key, fixed_multiplicity_weight_distribution(type_permutation, slots))
        for shape_permutation in automorphisms:
            endpoint_weights = fixed_endpoint_weight_distribution(
                edges, type_permutation, shape_permutation)
            fixed = feasible_state_count(endpoint_weights,
                                         multiplicity_cache[key])
            burnside_sum += fixed
            if (type_permutation == identity_type and
                    shape_permutation == identity_shape):
                raw = fixed
    group_size = len(D5) * len(automorphisms)
    assert raw is not None and burnside_sum % group_size == 0
    return raw, burnside_sum // group_size


def independent(mask, edges):
    return all(not (mask >> u & 1 and mask >> v & 1) for u, v in edges)


def biclique(mask, edges, n):
    vertices = [v for v in range(n) if mask >> v & 1]
    if len(vertices) < 2:
        return False
    edge_set = {tuple(sorted(edge)) for edge in edges}
    for side_mask in range(1, (1 << len(vertices)) - 1):
        left = [vertices[i] for i in range(len(vertices))
                if side_mask >> i & 1]
        right = [v for v in vertices if v not in left]
        induced = {edge for edge in edge_set
                   if edge[0] in vertices and edge[1] in vertices}
        expected = {tuple(sorted((u, v))) for u in left for v in right}
        if induced == expected:
            return True
    return False


@lru_cache(maxsize=None)
def support_masks(edges):
    n = shape_size(edges)
    full = (1 << n) - 1
    flexible = tuple(mask for mask in range(1 << n)
                     if independent(mask, edges) or
                     independent(full ^ mask, edges))
    bics = tuple(mask for mask in range(1 << n) if biclique(mask, edges, n))
    return full, flexible, bics


def endpoint_profiles(edges, endpoint):
    """Return the three endpoint maxima used by the multiplicity DP."""
    n = len(endpoint)
    full, flexible, bics = support_masks(edges)
    sigma = [0] * n
    for u, v in edges:
        sigma[u] += 1
        sigma[v] += 1
    colours = [v & 1 for v in range(n)]
    profiles = []
    gains = []
    for assignment_index, assignment in enumerate(ASSIGNMENTS):
        w = [TYPE_W_BY_COLOUR[colours[v]][endpoint[v]][assignment_index]
             for v in range(n)]

        if edges == SHAPES['matching']:
            # The only endpoint masks not covered by an independent set or
            # its complement are exactly one whole matching edge.
            independent_parts = [max(0, w[u] - 1, w[v] - 1)
                                 for u, v in edges]
            coindependent_parts = [max(w[u] - 1, w[v] - 1, w[u] + w[v])
                                   for u, v in edges]
            edge_values = [w[u] + w[v] for u, v in edges]
            a_value = max(sum(independent_parts),
                          sum(coindependent_parts))
            b_value = max(edge_values)
            profiles.append((a_value, b_value, b_value))
            gains.append(a_value)
            continue

        def base(mask):
            selected_edges = sum(bool(mask >> u & 1 and mask >> v & 1)
                                 for u, v in edges)
            return (sum(w[v] - sigma[v] for v in range(n)
                        if mask >> v & 1) + 2 * selected_edges)

        a_value = max(base(mask) for mask in flexible)
        b_value = max((base(mask) for mask in bics), default=-100)
        c_value = max((base(full ^ mask) for mask in bics), default=-100)
        profiles.append((a_value, b_value, c_value))
        gains.append(a_value)
    return tuple(profiles), tuple(gains)


TYPE_W_BY_COLOUR = []
for colour in (0, 1):
    colour_rows = []
    for neighbourhood in TYPES:
        colour_rows.append(tuple(
            sum(1 if assignment[x] == colour else -1
                for x in range(5) if neighbourhood >> x & 1)
            for assignment in ASSIGNMENTS))
    TYPE_W_BY_COLOUR.append(tuple(colour_rows))
TYPE_W = TYPE_W_BY_COLOUR[0]


def isolated_summary(multiplicities):
    positive = tuple(sum(multiplicities[t] * max(0, TYPE_W[t][a])
                         for t in range(len(TYPES))) for a in range(10))
    total = tuple(sum(multiplicities[t] * TYPE_W[t][a]
                      for t in range(len(TYPES))) for a in range(10))
    return positive, total


def assignment_gains(profiles, multiplicities):
    positive, total = isolated_summary(multiplicities)
    return tuple(max(a_value + positive[a], b_value,
                     c_value + total[a])
                 for a, (a_value, b_value, c_value) in enumerate(profiles))


def size_multiplicity_options(slots, required_boundary):
    for singles in range(slots + 1):
        for diagonals in range(slots - singles + 1):
            if singles + 2 * diagonals >= required_boundary:
                yield singles, diagonals, 5 * singles + 6 * diagonals


def canonical_size_witness(slots, singles, diagonals):
    multiplicities = [0] * len(TYPES)
    multiplicities[0] = slots - singles - diagonals
    multiplicities[1] = singles
    multiplicities[6] = diagonals
    return tuple(multiplicities)


def matching_multiplicity_vectors(slots):
    """All 11-type multiplicity vectors, generated without vertex labels."""
    counts = [0] * len(TYPES)
    out = []

    def rec(type_index, left, boundary, baseline):
        if type_index == len(TYPES) - 1:
            counts[type_index] = left
            final_boundary = boundary + 2 * left
            final_baseline = baseline + 6 * left
            multiplicities = tuple(counts)
            positive, total = isolated_summary(multiplicities)
            out.append((final_baseline, final_boundary, multiplicities,
                        positive, total))
            return
        weight = TYPES[type_index].bit_count()
        coefficient = 0 if weight == 0 else 5 if weight == 1 else 6
        for value in range(left + 1):
            counts[type_index] = value
            rec(type_index + 1, left - value,
                boundary + weight * value,
                baseline + coefficient * value)

    rec(0, slots, 0, 0)
    out.sort(key=lambda row: (row[0], row[1], row[2]))
    return out


def minimize_shape(name, edges):
    n = shape_size(edges)
    slots = 10 - n
    endpoints = []
    for endpoint in endpoint_tuples(edges):
        profiles, additive_gains = endpoint_profiles(edges, endpoint)
        endpoint_boundary = sum(TYPES[t].bit_count() for t in endpoint)
        endpoints.append((endpoint, endpoint_boundary, profiles,
                          sum(additive_gains)))

    best = None
    vectors_examined = 0
    monotone_pruned = 0
    if name != 'matching':
        for endpoint, endpoint_boundary, profiles, endpoint_gain in endpoints:
            required = max(0, 9 - endpoint_boundary)
            for singles, diagonals, isolated_gain in size_multiplicity_options(
                    slots, required):
                total_gain = endpoint_gain + isolated_gain
                if best is None or total_gain < best[0]:
                    multiplicities = canonical_size_witness(
                        slots, singles, diagonals)
                    gains = assignment_gains(profiles, multiplicities)
                    assert sum(gains) == total_gain
                    best = (total_gain, endpoint, endpoint_boundary,
                            multiplicities, gains)
    else:
        vectors = matching_multiplicity_vectors(slots)
        endpoint_tuple_count = len(endpoints)
        grouped = {}
        for endpoint, endpoint_boundary, profiles, endpoint_gain in endpoints:
            grouped.setdefault((endpoint_boundary, profiles, endpoint_gain), endpoint)
        endpoints = [(endpoint, endpoint_boundary, profiles, endpoint_gain)
                     for (endpoint_boundary, profiles, endpoint_gain), endpoint
                     in grouped.items()]
        # Find a good incumbent from one canonical orientation of each size
        # profile.  This is only an upper bound; the exact pass below still
        # considers every orientation that can beat it.  The least additive
        # profile is enough to seed the incumbent.
        for endpoint, endpoint_boundary, profiles, endpoint_gain in endpoints:
            required = max(0, 9 - endpoint_boundary)
            singles, diagonals, _ = min(
                size_multiplicity_options(slots, required),
                key=lambda option: (option[2], option[0] + option[1]))
            multiplicities = canonical_size_witness(
                slots, singles, diagonals)
            gains = assignment_gains(profiles, multiplicities)
            total_gain = sum(gains)
            if best is None or total_gain < best[0]:
                best = (total_gain, endpoint, endpoint_boundary,
                        multiplicities, gains)

        # Use the additive independent-flip contribution as a monotone lower
        # bound.  Vectors are sorted by that bound, so one failed bound prunes
        # the entire remaining suffix for this endpoint tuple.
        endpoints.sort(key=lambda row: (-row[1], row[3], row[0]))
        for endpoint, endpoint_boundary, profiles, endpoint_gain in endpoints:
            for vector_index, (baseline, boundary, multiplicities, positive,
                               total) in enumerate(vectors):
                lower_bound = endpoint_gain + baseline
                if lower_bound >= best[0]:
                    monotone_pruned += len(vectors) - vector_index
                    break
                if endpoint_boundary + boundary < 9:
                    continue
                gains = tuple(max(a_value + positive[a], b_value,
                                  c_value + total[a])
                              for a, (a_value, b_value, c_value)
                              in enumerate(profiles))
                vectors_examined += 1
                total_gain = sum(gains)
                if best is None or total_gain < best[0]:
                    best = (total_gain, endpoint, endpoint_boundary,
                            multiplicities, gains)

    assert best is not None
    total_gain, endpoint, endpoint_boundary, multiplicities, gains = best
    isolated_boundary = sum(multiplicities[t] * TYPES[t].bit_count()
                            for t in range(len(TYPES)))
    return {
        'endpoint_tuples': (endpoint_tuple_count if name == 'matching'
                            else len(endpoints)),
        'distinct_endpoint_profiles': (len(endpoints) if name == 'matching'
                                       else len(endpoints)),
        'exact_min_total_gain': total_gain,
        'witness': {
            'endpoint_neighbourhoods': [
                [i for i in range(5) if TYPES[t] >> i & 1] for t in endpoint],
            'isolated_multiplicities': list(multiplicities),
            'isolated_type_order': [
                [i for i in range(5) if mask >> i & 1] for mask in TYPES],
            'endpoint_boundary': endpoint_boundary,
            'isolated_boundary': isolated_boundary,
            'total_boundary': endpoint_boundary + isolated_boundary,
            'assignment_gains': list(gains),
            'total_gain': total_gain,
        },
        'matching_vectors_examined': vectors_examined,
        'matching_vectors_pruned_by_monotone_bound': monotone_pruned,
    }


def main():
    result = {
        'schema_version': 1,
        'method': ('multiplicity vectors over the 11 independent C5 subsets; '
                   'Burnside orbit count; additive minimization with a '
                   'matching-only profile DP'),
        'type_order': [[i for i in range(5) if mask >> i & 1]
                       for mask in TYPES],
        'isolated_ten_assignment_contribution_by_size': {'0': 0, '1': 5, '2': 6},
        'shapes': {},
    }
    for name, edges in SHAPES.items():
        raw, orbits = state_and_orbit_counts(edges)
        summary = minimize_shape(name, edges)
        summary['reduced_states_before_symmetry'] = raw
        summary['reduced_states_after_symmetry'] = orbits
        result['shapes'][name] = summary
        print(name, raw, orbits, summary['exact_min_total_gain'], flush=True)

    minimum = min(row['exact_min_total_gain']
                  for row in result['shapes'].values())
    result['global_min_total_gain'] = minimum
    result['status'] = ('counterexample' if minimum <= 6
                        else 'finite_certificate_minimum_at_least_7')
    output = Path('results/hard_regime_L_n15/L11_reduced_orbits.json')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + '\n')
    print('global', minimum, result['status'])


if __name__ == '__main__':
    main()
