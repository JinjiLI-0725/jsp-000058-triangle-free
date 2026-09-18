"""Reproducible small counterexamples to overly strong research heuristics."""

import argparse
from pathlib import Path

from .core import Graph, c5_blowup
from .research import atomic_json, canonicalize, from_graph6, graph6, sha256, witness


def run(output, labelg):
    balanced = c5_blowup(3)
    examples = {
        'balanced_C5': balanced,
        'balanced_C5_minus_one_edge': Graph(15, balanced.edges[1:]),
        'complete_bipartite_K7_8': Graph(15, tuple((u, v) for u in range(7) for v in range(7, 15))),
    }
    canonical = canonicalize([graph6(graph) for graph in examples.values()], labelg)
    records = {name: witness(from_graph6(line), canonical_graph6=line)
               for name, line in zip(examples, canonical)}
    # Fail loudly if an assumed counterexample is not actually verified.
    assert records['balanced_C5']['d'] == 9
    assert records['balanced_C5_minus_one_edge']['d'] == 8
    assert not records['balanced_C5_minus_one_edge']['is_C5_blowup']
    assert records['complete_bipartite_K7_8']['d'] == 0
    assert records['complete_bipartite_K7_8']['m'] > records['balanced_C5']['m']
    assert all(records[name]['maximal_triangle_free'] for name in ('balanced_C5', 'complete_bipartite_K7_8'))
    result = {'exhaustive': False, 'examples': records, 'source_sha256': sha256(__file__),
              'labelg_sha256': sha256(labelg),
              'scope': 'Three explicitly specified examples; counterexamples to structural guesses, not to JSP-000058.'}
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--labelg', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=Path('results/structural_checks.json'))
    args = parser.parse_args()
    run(args.output, args.labelg)


if __name__ == '__main__':
    main()
