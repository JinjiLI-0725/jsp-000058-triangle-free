"""Finite falsification tests for notes/structural_analysis.md; no broad search."""

from collections import Counter
from itertools import combinations
import json
from pathlib import Path

import numpy as np

from .core import Graph, c5_blowup, deletion_distance, is_triangle_free
from .research import atomic_json, from_graph6, graph6, sha256, witness


def induced(graph, vertices):
    labels = {v: i for i, v in enumerate(vertices)}
    return Graph(len(vertices), tuple((labels[u], labels[v]) for u, v in graph.edges
                                     if u in labels and v in labels))


def balanced(graph):
    adjacency = graph.adjacency_masks()
    classes = Counter(adjacency)
    if len(classes) != 5 or set(classes.values()) != {graph.n // 5}:
        return False
    reps = [adjacency.index(a) for a in classes]
    quotient = induced(graph, reps)
    return len(quotient.edges) == 5 and all(a.bit_count() == 2 for a in quotient.adjacency_masks())


def vertex_patterns(k):
    original = c5_blowup(k)
    core = induced(original, range(1, original.n))
    masks = np.arange(1 << core.n, dtype=np.uint32)
    costs = np.zeros(len(masks), dtype=np.int16)
    for u, v in core.edges:
        costs += (1 - (((masks >> u) ^ (masks >> v)) & 1)).astype(np.int16)
    adjacency = core.adjacency_masks()
    hist = Counter()
    equality = []
    representatives = {}
    for neighborhood in range(1 << core.n):
        vertices = [v for v in range(core.n) if neighborhood >> v & 1]
        if any(adjacency[v] & neighborhood for v in vertices):
            continue
        counts = np.zeros(len(masks), dtype=np.int16)
        for v in vertices:
            counts += ((masks >> v) & 1).astype(np.int16)
        d = int((costs + np.minimum(counts, len(vertices) - counts)).min())
        graph = Graph(core.n + 1, core.edges + tuple((v, core.n) for v in vertices))
        hist[d] += 1
        representatives.setdefault(d, graph)
        if d >= k*k:
            equality.append(witness(graph))
    # Independent Gray-code/full-graph evaluation for each attained value,
    # and both existing exact oracles for every potential equality witness.
    for d, graph in representatives.items():
        assert is_triangle_free(graph) and deletion_distance(graph) == d
    return {'k': k, 'patterns': sum(hist.values()), 'histogram': dict(hist),
            'equality_or_better': equality,
            'non_C5_equality': sum(not w['is_C5_blowup'] and w['d'] == k*k for w in equality)}


def reduction_test(records):
    result = {'graphs': len(records), 'A_failures': [], 'B_failures': [],
              'automatic_A': 0, 'automatic_B': 0, 'cores_evaluated': 0}
    for graph, d in records:
        k = graph.n // 5
        need_a = d - (2*k - 1)
        need_b = d - (2*k - 2) if not balanced(graph) else need_a
        result['automatic_A'] += need_a <= 0
        result['automatic_B'] += need_b <= 0
        if need_b <= 0:
            continue
        best = -1
        best_vertices = None
        for vertices in combinations(range(graph.n), graph.n - 5):
            value = deletion_distance(induced(graph, vertices))
            result['cores_evaluated'] += 1
            if value > best:
                best, best_vertices = value, vertices
            if best >= need_b:
                break
        for label, need in [('A', need_a), ('B', need_b)]:
            if best < need:
                result[label + '_failures'].append({'graph6': graph6(graph), 'd': d,
                    'maximum_core_d': best, 'core_vertices': best_vertices})
    return result


def main():
    inputs = ['results/exhaustive_k2/graphs.g6', 'results/heuristic_k3/evaluations.jsonl']
    small = [from_graph6(s) for s in Path(inputs[0]).read_text().splitlines()]
    small_records = [(g, deletion_distance(g)) for g in small]
    saved = {}
    for line in Path(inputs[1]).read_text().splitlines():
        row = json.loads(line)
        saved[row['graph6']] = row['d']
    large_records = [(from_graph6(s), d) for s, d in saved.items()]
    base = c5_blowup(3)
    large_records.append((Graph(15, base.edges[1:]), 8))
    print('Testing all one-vertex neighborhoods for k=1,2,3', flush=True)
    patterns = [vertex_patterns(k) for k in (1, 2, 3)]
    print('Testing reduction lemmas on the n=10 corpus', flush=True)
    small_result = reduction_test(small_records)
    print('Testing reduction lemmas on the saved n=15 corpus', flush=True)
    large_result = reduction_test(large_records)
    result = {'scope': 'Exhaustive one-vertex neighborhoods; exhaustive n=10 corpus; saved bounded n=15 corpus only.',
              'source_sha256': sha256(__file__), 'input_sha256': {p: sha256(p) for p in inputs},
              'vertex_patterns': patterns, 'reduction_n10': small_result,
              'reduction_n15': large_result}
    atomic_json('results/structural_analysis.json', result)
    print(json.dumps({key: value for key, value in result.items() if key != 'vertex_patterns'}, indent=2), flush=True)
    print([(p['k'], p['patterns'], p['histogram'], p['non_C5_equality']) for p in patterns], flush=True)


if __name__ == '__main__':
    main()
