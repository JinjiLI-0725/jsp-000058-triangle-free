from itertools import combinations
import json
import os
from pathlib import Path
import random

import networkx as nx
import pytest

from triangle_free import Graph, c5_blowup, exact_max_cut, is_triangle_free
from triangle_free.exhaustive import evaluate, generate
from triangle_free.research import (atomic_json, canonicalize, from_graph6, graph6,
                                    independent_max_cut, sha256, triangle_free_triples, witness)
from triangle_free.search import all_labeled_graphs


@pytest.mark.parametrize('n', range(6))
def test_independent_oracles_and_graph6(n):
    for graph in all_labeled_graphs(n):
        assert from_graph6(graph6(graph)) == graph
        assert triangle_free_triples(graph) == is_triangle_free(graph)
        value, side = independent_max_cut(graph)
        assert value == exact_max_cut(graph).value
        assert value == sum((u in side) != (v in side) for u, v in graph.edges)


def test_large_oracle_and_structure():
    rng = random.Random(5802)
    for n in (10, 15):
        for _ in range(8):
            graph = Graph(n, tuple(e for e in combinations(range(n), 2) if rng.random() < .4))
            assert exact_max_cut(graph).value == independent_max_cut(graph)[0]
    for k in (1, 2, 3):
        result = witness(c5_blowup(k))
        assert result['is_C5_blowup']
        assert result['false_twin_class_sizes'] == [k] * 5
        assert result['d'] == k * k
    assert not witness(Graph(10))['is_C5_blowup']


def corpus_fixture(path):
    path.mkdir()
    graphs = [Graph(5), Graph(5, ((0, 1),)), c5_blowup(1)]
    corpus = path / 'graphs.g6'
    corpus.write_text(''.join(graph6(graph) + '\n' for graph in graphs))
    atomic_json(path / 'generator.json', {'n': 5, 'count': len(graphs), 'corpus_sha256': sha256(corpus)})
    return graphs


def test_checkpoint_resume(tmp_path):
    corpus_fixture(tmp_path / 'resumed')
    corpus_fixture(tmp_path / 'fresh')
    partial = evaluate(tmp_path / 'resumed', checkpoint_every=2, stop_after=1)
    assert partial['graphs_examined'] == 1
    assert not partial['exhaustive']
    assert not (tmp_path / 'resumed' / 'result.json').exists()
    resumed = evaluate(tmp_path / 'resumed', resume=True, checkpoint_every=2)
    fresh = evaluate(tmp_path / 'fresh', checkpoint_every=2)
    assert resumed['status'] == 'complete'
    for key in ('identity', 'best_d', 'extremizers', 'graphs_examined', 'd_histogram', 'bound_violations'):
        assert resumed[key] == fresh[key]
    assert evaluate(tmp_path / 'resumed', resume=True) == resumed
    with pytest.raises(ValueError, match='already exists'):
        evaluate(tmp_path / 'resumed')


def test_reject_corrupt_or_mismatched_checkpoint(tmp_path):
    corpus_fixture(tmp_path / 'run')
    evaluate(tmp_path / 'run', stop_after=1)
    path = tmp_path / 'run' / 'checkpoint.json'
    data = json.loads(path.read_text())
    data['identity']['source_sha256']['core.py'] = 'wrong'
    atomic_json(path, data)
    with pytest.raises(ValueError, match='does not match'):
        evaluate(tmp_path / 'run', resume=True)
    with (tmp_path / 'run' / 'graphs.g6').open('a') as stream:
        stream.write('D??\n')
    with pytest.raises(ValueError, match='checksum'):
        evaluate(tmp_path / 'run', resume=True)


def test_reject_triangle_in_corpus(tmp_path):
    corpus_fixture(tmp_path / 'run')
    path = tmp_path / 'run' / 'graphs.g6'
    path.write_text(graph6(Graph(5, ((0, 1), (0, 2), (1, 2)))) + '\n')
    atomic_json(tmp_path / 'run' / 'generator.json', {'n': 5, 'count': 1, 'corpus_sha256': sha256(path)})
    with pytest.raises(RuntimeError, match='invalid graph'):
        evaluate(tmp_path / 'run')


def nauty_tools():
    root = Path(os.environ.get('NAUTY_DIR', '/tmp/nauty2_9_3'))
    if not all((root / name).exists() for name in ('geng', 'labelg')):
        pytest.skip('set NAUTY_DIR to run nauty integration checks')
    return root / 'geng', root / 'labelg'


def test_nauty_small_corpus_against_networkx_atlas(tmp_path):
    geng, labelg = nauty_tools()
    metadata = generate(5, geng, labelg, tmp_path)
    assert metadata['count'] == 14
    expected = []
    for network in nx.graph_atlas_g():
        if len(network) == 5:
            graph = Graph(5, tuple(network.edges()))
            if triangle_free_triples(graph):
                expected.append(graph6(graph))
    assert set(canonicalize(expected, labelg)) == set((tmp_path / 'graphs.g6').read_text().splitlines())
    assert evaluate(tmp_path)['best_d'] == 1
    with pytest.raises(ValueError, match='already exists'):
        generate(5, geng, labelg, tmp_path)


def test_canonical_labeling_invariant_under_relabeling():
    _, labelg = nauty_tools()
    graph = c5_blowup(2)
    rng = random.Random(123)
    inputs = [graph6(graph)]
    for _ in range(12):
        permutation = list(range(10))
        rng.shuffle(permutation)
        inputs.append(graph6(Graph(10, tuple((permutation[u], permutation[v]) for u, v in graph.edges))))
    assert len(set(canonicalize(inputs, labelg))) == 1


def test_unrestricted_generation_audit(tmp_path):
    from triangle_free.audit import audit
    geng, labelg = nauty_tools()
    pickg = geng.with_name('pickg')
    if not pickg.exists():
        pytest.skip('pickg is needed for generation audit')
    generate(5, geng, labelg, tmp_path)
    result = audit(tmp_path, geng, pickg, labelg)
    assert result['unrestricted_graphs'] == 34
    assert result['triangle_free_graphs'] == 14
    assert result['canonical_sets_equal']
