from collections import Counter
import json
from pathlib import Path

import networkx as nx

from triangle_free import Graph, c5_blowup, exact_max_cut, is_triangle_free
from triangle_free.research import from_graph6, independent_max_cut, sha256, triangle_free_triples

ROOT = Path(__file__).resolve().parents[1]


def check_witness(record):
    graph = Graph(record['n'], record['edges'])
    assert graph == from_graph6(record['canonical_graph6'])
    assert triangle_free_triples(graph) and is_triangle_free(graph)
    cut = exact_max_cut(graph)
    assert cut.value == record['max_cut'] == independent_max_cut(graph)[0]
    side = set(record['cut_side'])
    assert sum((u in side) != (v in side) for u, v in graph.edges) == cut.value
    assert len(graph.edges) == record['m']
    assert record['d'] == len(graph.edges) - cut.value


def test_completed_k2_artifacts():
    directory = ROOT / 'results' / 'exhaustive_k2'
    result = json.loads((directory / 'result.json').read_text())
    audit = json.loads((directory / 'generation_audit.json').read_text())
    assert result['status'] == 'complete' and result['exhaustive']
    assert result['graphs_examined'] == audit['triangle_free_graphs'] == 12172
    assert audit['unrestricted_graphs'] == 12005168
    assert audit['canonical_sets_equal']
    assert audit['corpus_sha256'] == sha256(directory / 'graphs.g6') == result['identity']['corpus_sha256']
    lines = (directory / 'graphs.g6').read_text().splitlines()
    assert len(lines) == len(set(lines)) == 12172
    assert result['d_histogram'] == {'0': 5479, '1': 5270, '2': 1397, '3': 25, '4': 1}
    assert len(result['extremizers']) == 1
    record = result['extremizers'][0]
    check_witness(record)
    assert record['canonical_graph6'] in lines
    assert nx.is_isomorphic(nx.Graph(record['edges']), nx.Graph(c5_blowup(2).edges))
    assert not result['bound_violations']


def test_completed_k3_artifacts_and_log():
    directory = ROOT / 'results' / 'heuristic_k3'
    result = json.loads((directory / 'result.json').read_text())
    assert result['status'] == 'complete' and result['exhaustive'] is False
    assert result['evaluation_log_sha256'] == sha256(directory / 'evaluations.jsonl')
    histogram = Counter()
    count = 0
    with (directory / 'evaluations.jsonl').open() as stream:
        for index, line in enumerate(stream):
            record = json.loads(line)
            assert record['index'] == index
            assert record['d'] == record['m'] - record['max_cut']
            histogram[str(record['d'])] += 1
            count += 1
    assert dict(histogram) == result['d_histogram']
    assert count == result['evaluations']
    assert result['best_d'] == max(map(int, histogram))
    assert result['structured_coverage']['C5']['positive_weight_vectors'] == 1001
    for record in result['near_extremizers'] + result['best_witnesses']:
        check_witness(record)
    assert not result['bound_violations']


def test_rejected_structural_claim_witnesses():
    result = json.loads((ROOT / 'results' / 'structural_checks.json').read_text())
    records = result['examples']
    for record in records.values():
        check_witness(record)
    assert records['balanced_C5_minus_one_edge']['d'] == 8
    assert records['balanced_C5_minus_one_edge']['false_twin_class_sizes'] == [1, 1, 2, 2, 3, 3, 3]
    assert not records['balanced_C5_minus_one_edge']['is_C5_blowup']
    assert records['complete_bipartite_K7_8']['d'] == 0
    assert records['balanced_C5']['d'] == 9
