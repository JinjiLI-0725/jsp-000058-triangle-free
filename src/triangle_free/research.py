"""Shared research validation, serialization, and independent exact cut oracle."""

from functools import lru_cache
from itertools import combinations
import hashlib
import json
import os
from pathlib import Path
import subprocess

import networkx as nx
import numpy as np

from .core import Graph, exact_max_cut


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def atomic_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    with temporary.open('w') as stream:
        json.dump(data, stream, indent=2, sort_keys=True)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)


def graph6(graph):
    network = nx.Graph()
    network.add_nodes_from(range(graph.n))
    network.add_edges_from(graph.edges)
    return nx.to_graph6_bytes(network, header=False).decode('ascii').strip()


def from_graph6(line):
    network = nx.from_graph6_bytes(line.encode('ascii'))
    return Graph(len(network), tuple(network.edges()))


def triangle_free_triples(graph):
    """Independent of both geng and the core common-neighbor implementation."""
    edges = set(graph.edges)
    return not any((u, v) in edges and (u, w) in edges and (v, w) in edges
                   for u, v, w in combinations(range(graph.n), 3))


@lru_cache(maxsize=3)
def _crossings(n):
    if not 0 <= n <= 16:
        raise ValueError('independent full-partition oracle limited to 16 vertices')
    masks = np.arange(1 << n, dtype=np.uint32)
    pairs = tuple(combinations(range(n), 2))
    rows = np.array([((masks >> u) ^ (masks >> v)) & 1 for u, v in pairs], dtype=np.uint8)
    rows.flags.writeable = False
    return {edge: i for i, edge in enumerate(pairs)}, rows


def independent_max_cut(graph):
    """Sum edge crossings for ALL masks; no Gray-code recurrence or symmetry fix."""
    lookup, rows = _crossings(graph.n)
    if not graph.edges:
        return 0, ()
    scores = rows[[lookup[edge] for edge in graph.edges]].sum(axis=0, dtype=np.int16)
    best_mask = int(scores.argmax())
    return int(scores[best_mask]), tuple(v for v in range(graph.n) if best_mask & (1 << v))


def canonicalize(lines, labelg):
    if not lines:
        return []
    process = subprocess.run([str(labelg), '-q'], input='\n'.join(lines) + '\n',
                             text=True, capture_output=True, check=True)
    output = process.stdout.splitlines()
    if len(output) != len(lines):
        raise RuntimeError('labelg changed the number of input graphs')
    return output


def witness(graph, *, canonical_graph6=None):
    cut = exact_max_cut(graph)
    other, _ = independent_max_cut(graph)
    if cut.value != other or not triangle_free_triples(graph):
        raise RuntimeError('independent witness validation failed')
    network = nx.Graph()
    network.add_nodes_from(range(graph.n))
    network.add_edges_from(graph.edges)
    neighborhoods = {}
    for v in network:
        neighborhoods.setdefault(tuple(sorted(network[v])), []).append(v)
    classes = list(neighborhoods.values())
    quotient = nx.Graph()
    quotient.add_nodes_from(range(len(classes)))
    quotient.add_edges_from((i, j) for i, j in combinations(range(len(classes)), 2)
                            if network.has_edge(classes[i][0], classes[j][0]))
    is_c5 = len(classes) == 5 and nx.is_connected(quotient) and all(d == 2 for _, d in quotient.degree())
    return {'n': graph.n, 'm': len(graph.edges), 'edges': [list(e) for e in graph.edges],
            'graph6': graph6(graph), 'canonical_graph6': canonical_graph6,
            'max_cut': cut.value, 'd': len(graph.edges) - cut.value, 'cut_side': list(cut.side),
            'degree_sequence': sorted(dict(network.degree()).values()),
            'components': nx.number_connected_components(network),
            'false_twin_class_sizes': sorted(map(len, classes)), 'is_C5_blowup': is_c5,
            'maximal_triangle_free': all(set(network[u]) & set(network[v])
                for u, v in combinations(range(graph.n), 2) if not network.has_edge(u, v))}
