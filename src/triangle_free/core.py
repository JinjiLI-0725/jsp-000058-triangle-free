"""Small-graph reference algorithms; no floating point or solver tolerances."""

from dataclasses import dataclass
from itertools import combinations
import random


@dataclass(frozen=True)
class Graph:
    """Simple undirected graph with vertices 0,...,n-1, including isolates.

    Reversed edges are canonicalized; loops and repeated edges are rejected.
    """

    n: int
    edges: tuple[tuple[int, int], ...] = ()

    def __post_init__(self):
        if type(self.n) is not int or self.n < 0:
            raise ValueError("n must be a nonnegative integer")
        canonical = set()
        for u, v in self.edges:
            if type(u) is not int or type(v) is not int or not (0 <= u < self.n and 0 <= v < self.n):
                raise ValueError("edge endpoints must be integer vertex labels in range")
            if u == v:
                raise ValueError("loops are not allowed")
            edge = (min(u, v), max(u, v))
            if edge in canonical:
                raise ValueError("duplicate undirected edge")
            canonical.add(edge)
        object.__setattr__(self, "edges", tuple(sorted(canonical)))

    def adjacency_masks(self) -> tuple[int, ...]:
        masks = [0] * self.n
        for u, v in self.edges:
            masks[u] |= 1 << v
            masks[v] |= 1 << u
        return tuple(masks)


def is_triangle_free(graph: Graph) -> bool:
    adjacency = graph.adjacency_masks()
    return all(not (adjacency[u] & adjacency[v]) for u, v in graph.edges)


@dataclass(frozen=True)
class MaxCutResult:
    value: int
    side: tuple[int, ...]
    cuts_examined: int


def exact_max_cut(graph: Graph, *, max_vertices: int = 24) -> MaxCutResult:
    """Enumerate all cuts modulo complementation using Gray-code updates.

    Vertex 0 stays outside `side`. Complexity is O(n+m+2**(n-1)) time
    and O(n+m) space (integer bit operations). The explicit size guard avoids
    accidentally launching an infeasible exact computation; callers may raise it.
    """
    if graph.n > max_vertices:
        raise ValueError(f"exact MaxCut limited to {max_vertices} vertices")
    adjacency = graph.adjacency_masks()
    mask = score = best = best_mask = 0
    count = 1 << max(0, graph.n - 1)
    for index in range(1, count):
        vertex = (index & -index).bit_length()  # variable bits start at vertex 1
        inside = (adjacency[vertex] & mask).bit_count()
        delta = adjacency[vertex].bit_count() - 2 * inside
        score += -delta if mask & (1 << vertex) else delta
        mask ^= 1 << vertex
        if score > best:
            best, best_mask = score, mask
    return MaxCutResult(best, tuple(v for v in range(graph.n) if best_mask & (1 << v)), count)


def deletion_distance(graph: Graph, *, max_vertices: int = 24) -> int:
    """d(G)=|E|-MaxCut; valid for every simple graph, not just triangle-free ones."""
    return len(graph.edges) - exact_max_cut(graph, max_vertices=max_vertices).value


def random_triangle_free(n: int, rng: random.Random, *, edge_probability: float = 1.0) -> Graph:
    """Random greedy construction, NOT uniform over triangle-free graphs.

    Shuffle all pairs, propose each with the given probability, and insert it
    only if its endpoints have no common neighbor. At probability 1 the output
    is maximal triangle-free, but need not have maximum edge count or d(G).
    """
    Graph(n)  # validate before allocating
    if not 0 <= edge_probability <= 1:
        raise ValueError("edge_probability must lie in [0, 1]")
    pairs = list(combinations(range(n), 2))
    rng.shuffle(pairs)
    adjacency = [0] * n
    edges = []
    for u, v in pairs:
        if rng.random() < edge_probability and not adjacency[u] & adjacency[v]:
            edges.append((u, v))
            adjacency[u] |= 1 << v
            adjacency[v] |= 1 << u
    return Graph(n, tuple(edges))


def c5_blowup(k: int) -> Graph:
    """Replace each vertex of C5 by k independent vertices."""
    if type(k) is not int or k < 1:
        raise ValueError("k must be a positive integer")
    return Graph(5 * k, tuple((a, b) for a, b in combinations(range(5 * k), 2)
                             if (a // k - b // k) % 5 in (1, 4)))
