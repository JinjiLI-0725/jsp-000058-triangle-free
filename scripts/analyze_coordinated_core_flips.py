"""Structural audit of the four saved cutoff counterexamples only."""
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import networkx as nx
from triangle_free.research import atomic_json, from_graph6, sha256

ROOT = Path(__file__).resolve().parents[1]


def mono(edges, mask):
    return sum(((mask >> u) & 1) == ((mask >> v) & 1) for u,v in edges)


def vertices(mask, domain):
    return [v for v in domain if mask & (1 << v)]


def analyze(record):
    graph = from_graph6(record['graph6'])
    X = record['X']
    H = [v for v in range(graph.n) if v not in X]
    hmask = sum(1 << v for v in H)
    xmask = sum(1 << v for v in X)
    hedges = [(u,v) for u,v in graph.edges if u in H and v in H]
    touch = [(u,v) for u,v in graph.edges if u in X or v in X]
    xedges = [(u,v) for u,v in graph.edges if u in X and v in X]
    boundary = [(u,v) if u in H else (v,u) for u,v in graph.edges if (u in H) != (v in H)]
    assignments = [sum(((bits >> j) & 1) << v for j,v in enumerate(X)) for bits in range(32)]
    rows = []
    for bits in range(1 << (len(H)-1)):
        core = sum(((bits >> j) & 1) << v for j,v in enumerate(H[1:]))
        costs = [(mono(touch, core | a), a) for a in assignments]
        e = min(cost for cost,a in costs)
        rows.append({'core': core, 'b': mono(hedges, core), 'e': e,
                     'a': [a for cost,a in costs if cost == e]})
    dH = min(r['b'] for r in rows)
    q = min(r['b']-dH+r['e'] for r in rows)
    assert dH == record['dH'] and q == record['q']
    profile = {t: min(r['e'] for r in rows if r['b']-dH == t)
               for t in sorted({r['b']-dH for r in rows})}
    assert {str(t):e for t,e in profile.items()} == record['F']
    bases = [r for r in rows if r['b'] == dH]
    targets = [r for r in rows if r['b']-dH+r['e'] == q]
    network = nx.Graph()
    network.add_nodes_from(H)
    network.add_edges_from(hedges)

    def witness(base, target, core):
        S = vertices(base['core'] ^ core, H)
        a = min(target['a'])
        if core != target['core']:
            a ^= xmask
        delta = [(u,v) for u,v in hedges if (u in S) != (v in S)]
        delta_mono = [(u,v) for u,v in delta if ((base['core'] >> u)&1) == ((base['core'] >> v)&1)]
        weights = {v: sum(1 if ((base['core'] >> v)&1) == ((a >> x)&1) else -1
                          for u,x in boundary if u == v) for v in H}
        penalty = len(delta)-2*len(delta_mono)
        fixed_base_extension = mono(touch, base['core'] | a)
        fixed_gain = sum(weights[v] for v in S)
        assert penalty == target['b']-dH
        assert fixed_base_extension-fixed_gain == target['e']
        # Validate the flip identity for EVERY core subset for this assignment.
        for subset in range(1 << len(H)):
            subset_vertices = [v for j,v in enumerate(H) if subset & (1<<j)]
            smask = sum(1<<v for v in subset_vertices)
            bd = [(u,v) for u,v in hedges if (u in subset_vertices) != (v in subset_vertices)]
            signed = sum(1 if ((base['core']>>u)&1) != ((base['core']>>v)&1) else -1 for u,v in bd)
            direct = mono(graph.edges, (base['core'] ^ smask) | a)-dH
            predicted = fixed_base_extension+signed-sum(weights[v] for v in subset_vertices)
            assert direct == predicted
        return {'base_side1': vertices(base['core'],H), 'base_side0': vertices(hmask^base['core'],H),
                'target_side1': vertices(core,H), 'target_side0': vertices(hmask^core,H),
                'S': S, 'S_size': len(S), 'S_edges': sorted(network.subgraph(S).edges()),
                'S_components': sorted(sorted(c) for c in nx.connected_components(network.subgraph(S))),
                'core_boundary_edges': delta, 'base_monochromatic_boundary_edges': delta_mono,
                't': penalty, 'base_optimized_extension': base['e'],
                'target_optimized_extension': target['e'], 'extension_saved': base['e']-target['e'],
                'net_objective_improvement': base['e']-q,
                'target_X_side1': vertices(a,X), 'base_optimal_X_sides1': [vertices(b,X) for b in base['a']],
                'base_extension_using_target_X': fixed_base_extension,
                'fixed_assignment_saving': fixed_gain, 'boundary_weights': weights,
                'S_boundary_weights': {v:weights[v] for v in S},
                'S_to_X_edges': [(u,x) for u,x in boundary if u in S]}

    by_t = []
    for t in sorted({r['b']-dH for r in targets}):
        pairs = []
        for target in targets:
            if target['b']-dH != t:
                continue
            for base in bases:
                for core in (target['core'], target['core'] ^ hmask):
                    S = tuple(vertices(base['core'] ^ core,H))
                    pairs.append((len(S), S, base['e'], base['core'], core, base, target))
        pairs.sort(key=lambda p:p[:5])
        chosen = pairs[0]
        best_F0 = min((p for p in pairs if p[2] == profile[0]), key=lambda p:p[:5])
        by_t.append({'t': t, 'number_of_optimal_core_cuts_mod_reversal': sum(r['b']-dH == t for r in targets),
                     'minimum_flip_size': chosen[0],
                     'all_minimum_flip_sets': sorted({p[1] for p in pairs if p[0] == chosen[0]}),
                     'minimum_flip_size_from_F0_base': best_F0[0],
                     'witness': witness(chosen[-2],chosen[-1],chosen[4])})

    mincut_values = []
    if dH == 0:
        base = bases[0]['core']
        for a in assignments:
            flow = nx.DiGraph()
            flow.add_nodes_from(['source','sink',*H])
            # source side = unchanged, sink side = flipped.
            for v in H:
                unflipped = sum(((base >> v)&1) == ((a >> x)&1) for u,x in boundary if u == v)
                flipped = sum(((base >> v)&1) != ((a >> x)&1) for u,x in boundary if u == v)
                flow.add_edge('source',v,capacity=flipped)
                flow.add_edge(v,'sink',capacity=unflipped)
            for u,v in hedges:
                flow.add_edge(u,v,capacity=1)
                flow.add_edge(v,u,capacity=1)
            val,_ = nx.minimum_cut(flow,'source','sink')
            exact = min(mono(graph.edges,core|a) for r in rows for core in (r['core'],r['core']^hmask))
            assert val+mono(xedges,a) == exact
            mincut_values.append(int(exact))
        assert min(mincut_values) == q
    return {'T': record.get('T',1), 'graph6': record['graph6'], 'X': X, 'H_vertices': H,
            'H_edges': hedges, 'X_edges': xedges, 'boundary_edges': boundary,
            'H_components': sorted(sorted(c) for c in nx.connected_components(network)),
            'H_bipartite': nx.is_bipartite(network), 'dH': dH, 'dG': dH+q, 'q': q, 'F': profile,
            'optimal_core_cuts_mod_global_reversal': [
                {'side1': vertices(r['core'],H), 'side0': vertices(hmask^r['core'],H),
                 'extension': r['e'], 'monochromatic_edges': [(u,v) for u,v in hedges if ((r['core']>>u)&1) == ((r['core']>>v)&1)]}
                for r in bases],
            'minimum_flip_size_for_global_optimum': min(row['minimum_flip_size'] for row in by_t),
            'by_minimizing_t': by_t, 'mincut_values_for_32_X_assignments': mincut_values,
            'signed_flip_identity_verified': True}


def main():
    first = ROOT/'results/existential_core_band_n15/result.json'
    rest = ROOT/'results/uniform_core_cutoff_n15/summary.json'
    records = [json.loads(first.read_text())['last_result']]
    records += [row['counterexample'] for row in json.loads(rest.read_text())['audits']]
    output = ROOT/'results/coordinated_core_flips_n15'
    output.mkdir(exist_ok=False)
    atomic_json(output/'manifest.json', {'scope': 'four previously saved counterexamples only',
                'input_sha256': {str(p.relative_to(ROOT)): sha256(p) for p in (first,rest)},
                'source_sha256': sha256(__file__)})
    results = []
    for record in records:
        row = analyze(record)
        results.append(row)
        atomic_json(output/f'T{row["T"]}.json',row)
        print(json.dumps({'T':row['T'], 'dH':row['dH'],
              'base_cuts': row['optimal_core_cuts_mod_global_reversal'],
              'min_flip_size': row['minimum_flip_size_for_global_optimum'],
              'witnesses': [r['witness'] for r in row['by_minimizing_t']]}),flush=True)
    atomic_json(output/'summary.json',results)


if __name__ == '__main__':
    main()
