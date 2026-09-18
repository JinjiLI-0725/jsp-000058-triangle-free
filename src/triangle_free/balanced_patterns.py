"""Exact cuts of B_t extensions with arbitrary per-vertex neighborhoods.

This is a small-instance reference implementation, not an exhaustive search.
See notes/BALANCED_EXTENSION_AUDIT.md for the cut identity and coverage gap.
"""

from itertools import product

from triangle_free.core import Graph


def _validate(edges, patterns):
    internal = Graph(5, tuple(edges)).edges
    if len(patterns) != 5 or not patterns[0]:
        raise ValueError("require five nonempty, equal-sized remainder parts")
    t = len(patterns[0])
    if any(len(part) != t for part in patterns):
        raise ValueError("remainder part sizes must agree")
    if any(type(mask) is not int or not 0 <= mask < 32
           for part in patterns for mask in part):
        raise ValueError("neighborhoods must be five-bit masks")
    return internal, t


def extension_graph(edges, patterns):
    """X has labels 0..4; each mask records one H vertex's neighbors in X."""
    internal, t = _validate(edges, patterns)
    out = list(internal)
    for j, part in enumerate(patterns):
        for r, mask in enumerate(part):
            v = 5 + j*t + r
            out.extend((x, v) for x in range(5) if mask >> x & 1)
            out.extend((v, 5 + ((j+1) % 5)*t + s) for s in range(t))
    return Graph(5+5*t, tuple(out))


def mixed_extension_distance(edges, patterns):
    """Exact sorted-unary-cost formula; O(16*(t+1)^5), for small t only.

    No triangle-free assumption is needed for this identity. In particular,
    vertices within one H part are allowed to receive different colors.
    """
    internal, t = _validate(edges, patterns)
    best = float("inf")
    # Fix the fifth X vertex to color zero, modulo global complementation.
    for color in range(16):
        x_cost = sum(((color >> u) ^ (color >> v)) & 1 == 0
                     for u, v in internal)
        unary = []
        for part in patterns:
            ones = [(mask & color).bit_count() for mask in part]
            zeros = [mask.bit_count()-one for mask, one in zip(part, ones)]
            values = [sum(zeros)]
            for delta in sorted(one-zero for one, zero in zip(ones, zeros)):
                values.append(values[-1]+delta)
            unary.append(values)
        for sizes in product(range(t+1), repeat=5):
            base = sum(sizes[j]*sizes[(j+1) % 5]
                       + (t-sizes[j])*(t-sizes[(j+1) % 5]) for j in range(5))
            value = x_cost + base + sum(unary[j][sizes[j]] for j in range(5))
            best = min(best, value)
    return int(best)
