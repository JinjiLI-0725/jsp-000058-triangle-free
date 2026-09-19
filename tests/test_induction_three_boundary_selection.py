"""Independent cut checks and exact polynomial certificates for three roots."""
from itertools import combinations, product

from triangle_free.core import Graph, c5_blowup, deletion_distance, is_triangle_free
from triangle_free.structural_analysis import induced

BITS = tuple(product(range(2), repeat=5))


def cost(s, parts, colors, bits):
    r = [parts.count(i) for i in range(5)]
    z = [sum(p == i and c == 0 for p, c in zip(parts, colors)) for i in range(5)]
    x = [z[i] + bits[i] * (s-r[i]) for i in range(5)]
    return sum(x[i]*x[(i+1) % 5] + (s-x[i])*(s-x[(i+1) % 5]) for i in range(5))


def test_symbolic_profiles_all_boundary_orbits():
    # Costs are quadratic; three exact evaluations recover their coefficients.
    for parts in ((0,0,0), (0,0,1), (0,0,2), (0,1,2), (0,1,3)):
        m = max(parts.count(i) for i in range(5))
        for tail in product(range(2), repeat=2):
            colors = (0,) + tail
            delta = 2 * ((parts == (0,1,2) and colors == (0,0,0)) or
                         (parts == (0,1,3) and colors == (0,0,1)))
            coefficients = set()
            for bits in BITS:
                vals = [cost(s, parts, colors, bits)-s*s-delta for s in range(m,m+3)]
                a = (vals[2]-2*vals[1]+vals[0]) // 2
                b = vals[1]-vals[0]-a
                coefficients.add((a,b,vals[0]))
            assert (0,0,0) in coefficients
            assert all(min(c) >= 0 for c in coefficients)


def test_full_cuts_all_small_triples():
    for s in (1,2):
        graph = c5_blowup(s)
        triples = tuple(combinations(range(graph.n), 3))
        profiles = {roots: [len(graph.edges)+1]*8 for roots in triples}
        for mask in range(1 << graph.n):
            count = sum(((mask >> u) & 1) == ((mask >> v) & 1) for u,v in graph.edges)
            for roots in triples:
                state = sum(((mask >> v) & 1) << j for j,v in enumerate(roots))
                profiles[roots][state] = min(profiles[roots][state], count)
        for roots, values in profiles.items():
            parts = tuple(v // s for v in roots)
            for state, value in enumerate(values):
                colors = tuple((state >> j) & 1 for j in range(3))
                assert value == min(cost(s, parts, colors, bits) for bits in BITS)
                assert value-s*s in (0,2)


def test_nonflat_gluing_and_nested_optimum():
    graph = c5_blowup(2)
    roots = (0,2,4)
    edges = graph.edges + tuple(e for j,r in enumerate(roots)
                                for e in ((r,10+j),(10+j,13)))
    graph = Graph(15, edges)  # Vertex 14 is an isolate.
    assert is_triangle_free(graph)
    assert deletion_distance(graph) == 5
    x = {1,3,5,6,8}
    keep = tuple(v for v in range(graph.n) if v not in x)
    assert deletion_distance(induced(graph, keep)) == 2
    # Construct nested optima with boundary 001 and table witness 01010.
    colors = (0,0,1)
    bits = (0,1,0,1,0)
    coloring = {v: 1-bits[v//2] for v in range(10)}
    coloring.update(zip(roots, colors))
    coloring[13] = coloring[14] = 0
    coloring.update({10+j: 1-colors[j] for j in range(3)})
    full = sum(coloring[u] == coloring[v] for u,v in graph.edges)
    remainder = sum(coloring[u] == coloring[v] for u,v in graph.edges if u not in x and v not in x)
    assert (full, remainder, full-remainder) == (5,2,3)
