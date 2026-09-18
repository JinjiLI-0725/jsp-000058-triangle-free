"""Bounded, reproducible k=3 experiments. NEVER exhaustive over all graphs."""

import argparse
from collections import Counter
from itertools import combinations
import json
import math
from pathlib import Path
import platform
import random

import networkx as nx
import numpy as np

from .core import Graph, c5_blowup, exact_max_cut, is_triangle_free, random_triangle_free
from .research import (atomic_json, canonicalize, from_graph6, graph6, independent_max_cut,
                       sha256, triangle_free_triples, witness)


def compositions(total, parts):
    """All ordered positive integer compositions, in lexicographic order."""
    if parts < 1 or total < parts:
        return
    if parts == 1:
        yield (total,)
    else:
        for first in range(1, total - parts + 2):
            for tail in compositions(total - first, parts - 1):
                yield (first,) + tail


def blowup(base, weights):
    if len(weights) != base.n or any(type(w) is not int or w < 1 for w in weights):
        raise ValueError('one positive integer weight per base vertex required')
    parts, offset = [], 0
    for size in weights:
        parts.append(range(offset, offset + size))
        offset += size
    return Graph(offset, tuple((u, v) for a, b in base.edges for u in parts[a] for v in parts[b]))


def andrasfai(index):
    if type(index) is not int or index < 1:
        raise ValueError('index must be positive')
    n = 3 * index - 1
    return Graph(n, tuple((u, v) for u, v in combinations(range(n), 2) if (v - u) % 3 == 1))


def structured_bases():
    for length in range(5, 16, 2):
        yield f'C{length}', Graph(length, tuple(nx.cycle_graph(length).edges()))
    for index in (3, 4, 5):
        yield f'Andrasfai_{index}', andrasfai(index)
    for name, graph in [('Petersen', nx.petersen_graph()), ('Mycielski_C5', nx.mycielskian(nx.cycle_graph(5)))]:
        yield name, Graph(len(graph), tuple(graph.edges()))


def fill_maximal(graph, rng):
    edges = set(graph.edges)
    adjacency = list(graph.adjacency_masks())
    pairs = list(combinations(range(graph.n), 2))
    rng.shuffle(pairs)
    for u, v in pairs:
        if (u, v) not in edges and not adjacency[u] & adjacency[v]:
            edges.add((u, v))
            adjacency[u] |= 1 << v
            adjacency[v] |= 1 << u
    return Graph(graph.n, tuple(sorted(edges)))


def mutate(graph, rng, operator):
    """Triangle-preserving kicks followed by randomized maximal completion."""
    if not is_triangle_free(graph):
        raise ValueError('mutation requires a triangle-free graph')
    edges = set(graph.edges)
    if operator == 'delete_refill':
        edges.difference_update(rng.sample(sorted(edges), min(len(edges), rng.randint(1, 6))))
    elif operator == 'rewire_vertex':
        v = rng.randrange(graph.n)
        edges = {edge for edge in edges if v not in edge}
    elif operator == 'force_nonedge':
        nonedges = sorted(set(combinations(range(graph.n), 2)) - edges)
        if nonedges:
            u, v = rng.choice(nonedges)
            adjacency = graph.adjacency_masks()
            common = adjacency[u] & adjacency[v]
            for w in range(graph.n):
                if common & (1 << w):
                    endpoint = rng.choice((u, v))
                    edges.remove(tuple(sorted((endpoint, w))))
            edges.add((u, v))
    else:
        raise ValueError('unknown mutation operator')
    return fill_maximal(Graph(graph.n, tuple(sorted(edges))), rng)


class Experiment:
    def __init__(self, output, labelg, checkpoint_every):
        self.output = Path(output)
        self.output.mkdir(parents=True, exist_ok=True)
        if (self.output / 'evaluations.jsonl').exists():
            raise ValueError('use a fresh output directory; heuristic resume is not implemented')
        if checkpoint_every < 1:
            raise ValueError('checkpoint interval must be positive')
        self.labelg = labelg
        self.interval = checkpoint_every
        self.cache = {}
        self.near = {}  # all distinct labeled graphs with d>=8
        self.best_graphs = {}
        self.family = {}
        self.requests = 0
        self.crosschecks = 0
        self.best = -1
        self.histogram = Counter()
        self.log = None

    def evaluate(self, graph, source):
        if graph.n != 15 or not is_triangle_free(graph) or not triangle_free_triples(graph):
            raise RuntimeError(f'invalid k=3 candidate from {source}')
        if graph.edges not in self.cache:
            cut, _ = independent_max_cut(graph)
            d = len(graph.edges) - cut
            # Every near-extremizer and a deterministic sample of lower values.
            if d >= 8 or len(self.cache) % 50 == 0:
                if exact_max_cut(graph).value != cut:
                    raise RuntimeError('independent exact solvers disagree')
                self.crosschecks += 1
            self.cache[graph.edges] = cut, d
        else:
            cut, d = self.cache[graph.edges]
        encoded = graph6(graph)
        if d > self.best:
            self.best, self.best_graphs = d, {}
        if d == self.best:
            self.best_graphs[encoded] = source
        if d >= 8:
            self.near[encoded] = source
        self.requests += 1
        self.histogram[str(d)] += 1
        group = source.split(':', 1)[0]
        stats = self.family.setdefault(group, {'evaluations': 0, 'best_d': -1, 'd_histogram': {}})
        stats['evaluations'] += 1
        stats['best_d'] = max(stats['best_d'], d)
        stats['d_histogram'][str(d)] = stats['d_histogram'].get(str(d), 0) + 1
        self.log.write(json.dumps({'index': self.requests - 1, 'source': source, 'graph6': encoded,
                                   'm': len(graph.edges), 'max_cut': cut, 'd': d}, sort_keys=True) + '\n')
        if self.requests % self.interval == 0:
            self.checkpoint()
        return d

    def checkpoint(self):
        self.log.flush()
        atomic_json(self.output / 'checkpoint.json', {
            'status': 'in_progress', 'exhaustive': False, 'resume_supported': False,
            'evaluations': self.requests, 'unique_labeled_graphs': len(self.cache),
            'best_d': self.best, 'd_histogram': dict(self.histogram),
            'best_labeled_graph6': sorted(self.best_graphs), 'families': self.family})
        print(f'k=3 evaluations={self.requests}; best d={self.best}', flush=True)

    def finish(self, parameters, structured_coverage, seed_summaries):
        self.log.flush()
        best_canonical = sorted(set(canonicalize(sorted(self.best_graphs), self.labelg)))
        near_canonical = sorted(set(canonicalize(sorted(self.near), self.labelg)))
        best = [witness(from_graph6(line), canonical_graph6=line) for line in best_canonical]
        near = [witness(from_graph6(line), canonical_graph6=line) for line in near_canonical]
        result = {'status': 'complete', 'exhaustive': False, 'k': 3, 'n': 15, 'target_bound': 9,
                  'best_d': self.best, 'evaluations': self.requests, 'unique_labeled_graphs': len(self.cache),
                  'independent_gray_crosschecks': self.crosschecks, 'd_histogram': dict(self.histogram),
                  'families': self.family, 'structured_coverage': structured_coverage,
                  'seed_summaries': seed_summaries, 'parameters': parameters,
                  'best_witnesses': best, 'near_extremizers': near,
                  'bound_violations': [w for w in near if w['d'] > 9],
                  'evaluation_log_sha256': sha256(self.output / 'evaluations.jsonl'),
                  'labelg_sha256': sha256(self.labelg), 'python': platform.python_version(),
                  'networkx': nx.__version__, 'numpy': np.__version__,
                  'source_sha256': {name: sha256(Path(__file__).with_name(name))
                                    for name in ('core.py', 'research.py', 'heuristic.py')},
                  'scope': 'Heuristic search of k=3; complete positive-weight enumeration ONLY within the named fixed-base blow-up families. Not exhaustive over triangle-free graphs.'}
        atomic_json(self.output / 'result.json', result)
        (self.output / 'extremizers.g6').write_text(''.join(line + '\n' for line in best_canonical))
        (self.output / 'near_extremizers.g6').write_text(''.join(line + '\n' for line in near_canonical))
        atomic_json(self.output / 'checkpoint.json', {
            'status': 'complete', 'exhaustive': False, 'resume_supported': False,
            'evaluations': self.requests, 'best_d': self.best,
            'result_sha256': sha256(self.output / 'result.json')})
        return result


def run(output, labelg, *, seeds=(58, 59, 60, 61), samples=500, steps=2000,
        checkpoint_every=500, include_structured=True):
    if samples < 0 or steps < 0 or not seeds:
        raise ValueError('nonnegative counts and at least one seed required')
    experiment = Experiment(output, labelg, checkpoint_every)
    parameters = {'seeds': list(seeds), 'random_samples_per_seed': samples, 'local_steps_per_seed': steps,
                  'probability_schedule': [0.35, 0.6, 0.85, 1.0], 'restart_interval': 250,
                  'temperature': '1.2 - 1.1 * ((step % 250) / 249)',
                  'acceptance': 'accept ties/improvements; accept decrease with exp(delta/temperature)',
                  'operators': ['delete_refill', 'rewire_vertex', 'force_nonedge'],
                  'structured_enabled': include_structured, 'checkpoint_every': checkpoint_every}
    coverage, seed_summaries = {}, []
    anchors = [c5_blowup(3)]
    with (experiment.output / 'evaluations.jsonl').open('w') as log:
        experiment.log = log
        experiment.evaluate(anchors[0], 'benchmark:C5_3_3_3_3_3')
        if include_structured:
            for name, base in structured_bases():
                inputs = []
                for weights in compositions(15, base.n):
                    candidate = blowup(base, weights)
                    if not triangle_free_triples(candidate):
                        raise RuntimeError(f'non-triangle-free structured candidate: {name}')
                    inputs.append(graph6(candidate))
                canonical = sorted(set(canonicalize(inputs, labelg)))
                coverage[name] = {'positive_weight_vectors': len(inputs), 'canonical_graphs': len(canonical),
                                  'scope': 'All positive integer weights totaling 15 for this fixed base only'}
                family_best, family_anchor = -1, None
                for line in canonical:
                    graph = from_graph6(line)
                    d = experiment.evaluate(graph, f'{name}:positive_weight_blowup')
                    if d > family_best:
                        family_best, family_anchor = d, graph
                anchors.append(family_anchor)
            # Folded 4-cube (Clebsch) minus one vertex, then relabel to 0,...,14.
            folded = Graph(15, tuple((u - 1, v - 1) for u, v in combinations(range(1, 16), 2)
                                    if (u ^ v).bit_count() in (1, 4)))
            experiment.evaluate(folded, 'folded_4cube_minus_vertex:benchmark')
            anchors.append(folded)
            bipartite = Graph(15, tuple((u, v) for u in range(7) for v in range(7, 15)))
            experiment.evaluate(bipartite, 'K7_8:benchmark')
        for seed in seeds:
            rng = random.Random(seed)
            before = experiment.requests
            random_best = -1
            pool = list(anchors)
            for index in range(samples):
                graph = random_triangle_free(15, rng, edge_probability=parameters['probability_schedule'][index % 4])
                d = experiment.evaluate(graph, f'random_seed_{seed}:sample_{index}')
                random_best = max(random_best, d)
                if d >= 7 and len(pool) < 200:
                    pool.append(graph)
            current = anchors[0]
            current_d = experiment.evaluate(current, f'local_seed_{seed}:initial_extremizer')
            local_best = current_d
            accepted = 0
            for step in range(steps):
                if step and step % 250 == 0:
                    if rng.random() < 0.5:
                        # Includes newly discovered extremizers; list order is fixed.
                        current = from_graph6(rng.choice(sorted(experiment.best_graphs)))
                    else:
                        current = rng.choice(pool)
                    current_d = experiment.evaluate(current, f'local_seed_{seed}:restart_{step}')
                operator = parameters['operators'][step % 3]
                candidate = mutate(current, rng, operator)
                d = experiment.evaluate(candidate, f'local_seed_{seed}:{operator}_{step}')
                local_best = max(local_best, d)
                temperature = 1.2 - 1.1 * ((step % 250) / 249)
                if d >= current_d or rng.random() < math.exp((d - current_d) / temperature):
                    current, current_d = candidate, d
                    accepted += 1
            seed_summaries.append({'seed': seed, 'evaluations': experiment.requests - before,
                                   'random_best_d': random_best, 'local_best_d': local_best,
                                   'local_moves_accepted': accepted})
            experiment.checkpoint()
        return experiment.finish(parameters, coverage, seed_summaries)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--labelg', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=Path('results/heuristic_k3'))
    parser.add_argument('--seeds', type=int, nargs='+', default=[58, 59, 60, 61])
    parser.add_argument('--samples', type=int, default=500)
    parser.add_argument('--steps', type=int, default=2000)
    args = parser.parse_args()
    result = run(args.output, args.labelg, seeds=args.seeds, samples=args.samples, steps=args.steps)
    print(f"k=3 best d={result['best_d']}; {len(result['best_witnesses'])} maximizing classes observed; NOT exhaustive")
    return int(bool(result['bound_violations']))


if __name__ == '__main__':
    raise SystemExit(main())
