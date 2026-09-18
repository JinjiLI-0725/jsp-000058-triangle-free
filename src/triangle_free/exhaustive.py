"""Generate and independently evaluate every unlabeled triangle-free n=10 graph."""

import argparse
from collections import Counter
import json
from pathlib import Path
import platform
import re
import subprocess
import time

import networkx as nx
import numpy as np

from .core import exact_max_cut, is_triangle_free
from .research import atomic_json, canonicalize, from_graph6, independent_max_cut, sha256, triangle_free_triples, witness


def generate(n, geng, labelg, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    if (output / 'generator.json').exists():
        raise ValueError('generation already exists; use --resume or a fresh directory')
    command = [str(Path(geng).resolve()), '-t', str(n)]
    start = time.monotonic()
    process = subprocess.run(command, capture_output=True, text=True, check=True)
    match = re.search(r'>Z\s+(\d+) graphs generated', process.stderr)
    if not match:
        raise RuntimeError('missing geng completion count')
    lines = process.stdout.splitlines()
    if len(lines) != int(match[1]):
        raise RuntimeError('geng output count mismatch')
    canonical = canonicalize(lines, labelg)
    if len(set(canonical)) != len(lines):
        raise RuntimeError('duplicate isomorphism class after canonicalization')
    corpus = output / 'graphs.g6'
    corpus.write_text('\n'.join(canonical) + '\n', encoding='ascii')
    metadata = {'n': n, 'command': command, 'labelg_command': [str(Path(labelg).resolve()), '-q'],
                'generator_stderr': process.stderr, 'count': len(lines), 'corpus_sha256': sha256(corpus),
                'geng_sha256': sha256(geng), 'labelg_sha256': sha256(labelg),
                'generation_seconds': time.monotonic() - start,
                'coverage': 'All non-isomorphic simple triangle-free graphs, disconnected graphs and isolates included; no edge or degree restrictions'}
    atomic_json(output / 'generator.json', metadata)
    return metadata


def evaluate(output, *, checkpoint_every=1000, resume=False, stop_after=None):
    """Checkpoint after bounded batches. Resume binds to corpus AND evaluator source.

    `stop_after` is a test/controlled-interruption hook: it limits new evaluations,
    never marks a partial run complete. A crash may lose only the latest batch.
    """
    if checkpoint_every < 1 or (stop_after is not None and stop_after < 1):
        raise ValueError('checkpoint interval and stop_after must be positive')
    output = Path(output)
    metadata = json.loads((output / 'generator.json').read_text())
    corpus = output / 'graphs.g6'
    digest = sha256(corpus)
    if digest != metadata['corpus_sha256']:
        raise ValueError('corpus checksum mismatch')
    lines = corpus.read_text().splitlines()
    if len(lines) != metadata['count'] or len(set(lines)) != len(lines):
        raise ValueError('corpus count or uniqueness mismatch')
    source_hashes = {name: sha256(Path(__file__).with_name(name))
                     for name in ('core.py', 'research.py', 'exhaustive.py')}
    identity = {'corpus_sha256': digest, 'source_sha256': source_hashes, 'n': metadata['n'],
                'total_graphs': len(lines), 'python': platform.python_version(),
                'numpy': np.__version__, 'networkx': nx.__version__}
    checkpoint = output / 'checkpoint.json'
    if resume and checkpoint.exists():
        state = json.loads(checkpoint.read_text())
        if state['identity'] != identity:
            raise ValueError('checkpoint does not match input, code, or environment')
    else:
        if checkpoint.exists():
            raise ValueError('checkpoint already exists; explicitly request resume')
        state = {'identity': identity, 'status': 'in_progress', 'exhaustive': False,
                 'graphs_examined': 0, 'best_d': -1, 'd_histogram': {}, 'edge_histogram': {},
                 'extremizers': [], 'bound_violations': [], 'checkpoint_writes': 0}
    if not 0 <= state['graphs_examined'] <= len(lines) or sum(state['d_histogram'].values()) != state['graphs_examined']:
        raise ValueError('inconsistent checkpoint counts')
    histogram = Counter(state['d_histogram'])
    edge_histogram = Counter(state['edge_histogram'])
    processed = 0
    for index in range(state['graphs_examined'], len(lines)):
        graph = from_graph6(lines[index])
        if graph.n != metadata['n'] or not triangle_free_triples(graph) or not is_triangle_free(graph):
            raise RuntimeError(f'invalid graph at index {index}')
        cut = exact_max_cut(graph)
        reference, _ = independent_max_cut(graph)
        if cut.value != reference:
            raise RuntimeError(f'MaxCut disagreement at index {index}')
        d = len(graph.edges) - cut.value
        histogram[str(d)] += 1
        edge_histogram[str(len(graph.edges))] += 1
        if d > state['best_d']:
            state['best_d'], state['extremizers'] = d, []
        if d == state['best_d']:
            state['extremizers'].append(witness(graph, canonical_graph6=lines[index]))
        if d > (graph.n // 5) ** 2:
            state['bound_violations'].append(witness(graph, canonical_graph6=lines[index]))
        state['graphs_examined'] = index + 1
        processed += 1
        if (index + 1) % checkpoint_every == 0 or index + 1 == len(lines) or processed == stop_after:
            state.update(d_histogram=dict(histogram), edge_histogram=dict(edge_histogram))
            complete = index + 1 == len(lines)
            state.update(status='complete' if complete else 'in_progress', exhaustive=complete)
            state['checkpoint_writes'] += 1
            atomic_json(checkpoint, state)
            print(f"verified {index + 1}/{len(lines)}; best d={state['best_d']}", flush=True)
        if processed == stop_after:
            break
    if state['status'] == 'complete':
        atomic_json(output / 'result.json', state)
        (output / 'extremizers.g6').write_text(''.join(w['canonical_graph6'] + '\n' for w in state['extremizers']))
    return state


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--geng', type=Path)
    parser.add_argument('--labelg', type=Path)
    parser.add_argument('--output', type=Path, default=Path('results/exhaustive_k2'))
    parser.add_argument('--checkpoint-every', type=int, default=1000)
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    if not args.resume:
        if not args.geng or not args.labelg:
            parser.error('--geng and --labelg are required for generation')
        generate(10, args.geng, args.labelg, args.output)
    result = evaluate(args.output, checkpoint_every=args.checkpoint_every, resume=args.resume)
    return int(bool(result['bound_violations']))


if __name__ == '__main__':
    raise SystemExit(main())
