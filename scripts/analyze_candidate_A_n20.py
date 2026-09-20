"""Snapshot, extract, exactly verify, canonically classify and analyze n=20 logs.

No claim of exhaustive graph coverage: exhaustive means all 15504 deletions
of each selected isomorphism class. Canonical equivalence transfers that result
to every listed labeled member. Run again with --resume after interruption.
"""
import argparse
from collections import Counter, defaultdict
import ctypes
import fcntl
from functools import lru_cache
import hashlib
from itertools import combinations
import json
from pathlib import Path
import shutil
import sys

sys.dont_write_bytecode = True

import networkx as nx

from candidate_A_n20_support import safe_output, read_journal, fingerprint
from triangle_free.core import is_triangle_free, exact_max_cut
from triangle_free.research import atomic_json, canonicalize, from_graph6, graph6
from triangle_free.structural_analysis import induced

TOTAL = 15504
VERSION = 1


class CutOracle:
    def __init__(self):
        path = Path(__file__).with_name('libmaxcut_fast.so').resolve()
        self.lib = ctypes.CDLL(str(path))
        self.lib.maxcut_exact.argtypes = [ctypes.c_int, ctypes.c_int,
                                         ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
        self.lib.maxcut_exact.restype = ctypes.c_int

    @lru_cache(maxsize=4096)
    def distance(self, graph):
        if graph.n < 2:
            return 0
        m = len(graph.edges)
        u = (ctypes.c_int * m)(*(a for a, b in graph.edges))
        v = (ctypes.c_int * m)(*(b for a, b in graph.edges))
        return m - self.lib.maxcut_exact(graph.n, m, u, v)


def verify(g6, oracle, checkpoint, batch=256):
    graph = from_graph6(g6)
    if graph.n != 20 or not is_triangle_free(graph):
        raise ValueError('verification requires a triangle-free n=20 graph')
    d = oracle.distance(graph)
    # Independent implementation check on the full graph.
    if d != len(graph.edges) - exact_max_cut(graph).value:
        raise RuntimeError('full graph cut oracle disagreement')
    state = {'version': VERSION, 'graph6': g6, 'd': d, 'checked': 0,
             'M15': -1, 'best_deleted': None, 'core_d_histogram': {},
             'maximizer_count': 0, 'maximizer_vertex_incidence': [0] * 20,
             'maximizer_deleted_edge_histogram': {}}
    if checkpoint.exists():
        state = json.loads(checkpoint.read_text())
        if (state['version'] != VERSION or state['graph6'] != g6 or state['d'] != d
                or not 0 <= state['checked'] <= TOTAL
                or sum(state['core_d_histogram'].values()) != state['checked']):
            raise ValueError('invalid verification checkpoint')
    hist = Counter({int(k): v for k, v in state['core_d_histogram'].items()})
    for index, deleted in enumerate(combinations(range(20), 5)):
        if index < state['checked']:
            continue
        deleted_set = set(deleted)
        core = induced(graph, tuple(v for v in range(20) if v not in deleted_set))
        dh = oracle.distance(core)
        # Cross-check first core with the independent full-partition NumPy oracle.
        if index == 0:
            from triangle_free.research import independent_max_cut
            if dh != len(core.edges) - independent_max_cut(core)[0]:
                raise RuntimeError('core cut oracle disagreement')
        hist[dh] += 1
        if dh > state['M15']:
            state.update(M15=dh, best_deleted=list(deleted), maximizer_count=0,
                         maximizer_vertex_incidence=[0] * 20,
                         maximizer_deleted_edge_histogram={})
        if dh == state['M15']:
            state['maximizer_count'] += 1
            for v in deleted:
                state['maximizer_vertex_incidence'][v] += 1
            e = str(sum(u in deleted_set and v in deleted_set for u, v in graph.edges))
            eh = state['maximizer_deleted_edge_histogram']
            eh[e] = eh.get(e, 0) + 1
        state['checked'] = index + 1
        if state['checked'] % batch == 0 or state['checked'] == TOTAL:
            state['core_d_histogram'] = dict(sorted(hist.items()))
            atomic_json(checkpoint, state)
    state['core_d_histogram'] = dict(sorted(hist.items()))
    state['Delta5'] = d - state['M15']
    state['all_deletions_verified'] = state['checked'] == TOTAL
    state['status'] = ('A_FAILURE' if state['Delta5'] >= 8 else
                       'exact_tight' if state['Delta5'] == 7 else 'not_tight')
    return state


def structure(g6):
    graph = from_graph6(g6)
    network = nx.Graph()
    network.add_nodes_from(range(20))
    network.add_edges_from(graph.edges)
    adj = graph.adjacency_masks()
    twins = defaultdict(list)
    for v, mask in enumerate(adj):
        twins[mask].append(v)
    groups = sorted(twins.values(), key=lambda x: x[0])
    quotient = nx.Graph()
    quotient.add_nodes_from(range(len(groups)))
    quotient.add_edges_from((i, j) for i in range(len(groups)) for j in range(i + 1, len(groups))
                           if network.has_edge(groups[i][0], groups[j][0]))
    is_c5 = len(groups) == 5 and nx.is_isomorphic(quotient, nx.cycle_graph(5))
    alpha = len(nx.algorithms.clique.max_weight_clique(nx.complement(network), weight=None)[0])
    cut = exact_max_cut(graph)
    return {'m': len(graph.edges), 'degree_sequence': sorted(dict(network.degree()).values()),
            'component_sizes': sorted(map(len, nx.connected_components(network))),
            'vertex_connectivity': nx.node_connectivity(network),
            'independence_number': alpha, 'bipartite': nx.is_bipartite(network),
            'maximal_triangle_free': all(adj[u] & adj[v] for u, v in nx.non_edges(network)),
            'false_twin_classes': groups, 'twin_quotient_edges': sorted(quotient.edges()),
            'twin_class_sizes': list(map(len, groups)), 'is_C5_blowup': is_c5,
            'is_B4': is_c5 and all(len(g) == 4 for g in groups),
            'maximum_cut_size': cut.value, 'maximum_cut_side': list(cut.side)}


def extract(rows):
    selected = {}
    for row in rows:
        # Include every estimated-gap-7 record, even d_too_small records whose
        # gap was set to d without sampling. Also audit any possible failures.
        if row['estimated_gap'] < 7:
            continue
        key = row['graph6']
        entry = selected.setdefault(key, {'graph6': key, 'sources': set(),
                                         'indices': [], 'estimated_gaps': set(), 'logged_d': set()})
        entry['sources'].add(row['source'])
        entry['indices'].append(row.get('index'))
        entry['estimated_gaps'].add(row['estimated_gap'])
        entry['logged_d'].add(row['d'])
    return [{k: sorted(v) if isinstance(v, set) else v for k, v in entry.items()}
            for _, entry in sorted(selected.items())]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True, help='source run directory, read only')
    parser.add_argument('--output', type=Path, required=True, help='separate fresh analysis directory')
    parser.add_argument('--labelg', default=shutil.which('nauty-labelg') or shutil.which('labelg'))
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    output = safe_output(args.output, [args.input])
    if not args.labelg:
        parser.error('nauty labelg is required for canonical labels; supply --labelg')
    labelg = Path(args.labelg).resolve()
    hashes = fingerprint([Path(__file__), Path(__file__).with_name('candidate_A_n20_support.py'),
                          Path(__file__).with_name('libmaxcut_fast.so'), labelg])
    import triangle_free.core, triangle_free.research, triangle_free.structural_analysis
    hashes.update(fingerprint([m.__file__ for m in (triangle_free.core, triangle_free.research,
                                                   triangle_free.structural_analysis)]))
    manifest_path = output / 'manifest.json'
    snapshot_path = output / 'input_snapshot.jsonl'
    if args.resume:
        lock = manifest_path.open('r')
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        manifest = json.loads(manifest_path.read_text())
        if manifest['code_sha256'] != hashes or manifest['source'] != str(args.input.resolve()):
            raise ValueError('resume source or toolchain differs')
        if hashlib.sha256(snapshot_path.read_bytes()).hexdigest() != manifest['snapshot_sha256']:
            raise ValueError('snapshot changed')
        rows, _ = read_journal(snapshot_path)
    else:
        if any(output.iterdir()):
            raise ValueError('fresh analysis requires an empty output directory')
        rows, committed = read_journal(args.input / 'evaluations.jsonl')
        snapshot_path.write_bytes(committed)
        manifest = {'version': VERSION, 'source': str(args.input.resolve()),
                    'code_sha256': hashes, 'snapshot_sha256': hashlib.sha256(committed).hexdigest(),
                    'records': len(rows), 'selection': 'estimated_gap >= 7',
                    'scope': 'Immutable committed-log snapshot; may be a prefix of a running search.'}
        atomic_json(manifest_path, manifest)
        lock = manifest_path.open('r')
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    selected = extract(rows)
    canonical = canonicalize([r['graph6'] for r in selected], labelg)
    groups = defaultdict(list)
    for row, canon in zip(selected, canonical):
        # Check the canonicalizer's output is genuinely isomorphic, including isolates.
        if not nx.is_isomorphic(nx.from_graph6_bytes(row['graph6'].encode()),
                                nx.from_graph6_bytes(canon.encode())):
            raise RuntimeError('canonicalization isomorphism check failed')
        row['canonical_graph6'] = canon
        groups[canon].append(row)
    atomic_json(output / 'extracted.json', selected)
    (output / 'estimated_gap7.g6').write_text(''.join(r['graph6'] + '\n' for r in selected
                                                  if 7 in r['estimated_gaps']))
    oracle = CutOracle()
    verified = []
    tight = []
    for index, (canon, members) in enumerate(sorted(groups.items()), 1):
        key = hashlib.sha256(canon.encode()).hexdigest()
        result = verify(canon, oracle, output / f'verify_{key}.json')
        for member in members:
            if member['logged_d'] != [result['d']]:
                raise RuntimeError('logged d disagrees with exact recomputation')
        result['members'] = members
        result['canonical_graph6'] = canon
        verified.append(result)
        if result['Delta5'] == 7:
            result['structure'] = structure(canon)
            tight.append(result)
        atomic_json(output / 'verified.json', verified)
        print(f'class {index}/{len(groups)}: d={result["d"]} M15={result["M15"]} '
              f'Delta5={result["Delta5"]} labeled={len(members)}', flush=True)
    atomic_json(output / 'tight_classes.json', tight)
    failures = [r for r in verified if r['Delta5'] >= 8 and r['checked'] == TOTAL]
    atomic_json(output / 'exact_failures.json', failures)
    summary = {'status': 'complete', 'snapshot_records': len(rows),
               'selected_labeled_graphs': len(selected), 'verified_isomorphism_classes': len(verified),
               'estimated_gap7_labeled_graphs': sum(7 in r['estimated_gaps'] for r in selected),
               'exact_tight_classes': len(tight),
               'exact_tight_labeled_graphs': sum(len(r['members']) for r in tight),
               'exact_failure_classes': len(failures), 'exhaustive_graph_search': False,
               'Delta5_class_histogram': dict(Counter(r['Delta5'] for r in verified)),
               'scope': 'All 15504 deletions per selected canonical graph; results transfer by '
                        'checked isomorphism to listed labeled members. Heuristic graph coverage '
                        'does not prove Candidate A.'}
    atomic_json(output / 'summary.json', summary)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
