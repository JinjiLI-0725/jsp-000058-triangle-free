import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from triangle_free import Graph, exact_max_cut, is_triangle_free
from triangle_free.search import search


def test_exhaustive_k1():
    result = search(1)
    assert result['candidates_considered'] == 1024
    assert result['triangle_free_evaluations'] == 388
    assert result['unique_labeled_graphs_evaluated'] == 388
    assert result['d_histogram'] == {'0': 376, '1': 12}
    assert result['best_d'] == 1
    assert not result['bound_violations']


def test_seeded_search():
    result = search(2, seed=123, samples=80)
    assert result == search(2, seed=123, samples=80)
    assert result['triangle_free_evaluations'] == 81
    assert result['best_d'] == 4
    assert not result['bound_violations']
    for witness in result['best_witnesses']:
        graph = Graph(witness['n'], witness['edges'])
        assert is_triangle_free(graph)
        assert exact_max_cut(graph).value == witness['max_cut']
        assert len(graph.edges) - witness['max_cut'] == witness['d']


def test_search_validation():
    with pytest.raises(ValueError):
        search(3)
    with pytest.raises(ValueError):
        search(2, samples=-1)


def test_cli(tmp_path):
    process = subprocess.run([sys.executable, '-m', 'triangle_free.search', '--samples', '10',
                              '--output', str(tmp_path)], capture_output=True, text=True,
                             env={**os.environ, 'PYTHONPATH': str(Path(__file__).resolve().parents[1] / 'src')})
    assert process.returncode == 0, process.stderr
    assert json.loads((tmp_path / 'k1_seed58.json').read_text())['best_d'] == 1
    assert json.loads((tmp_path / 'k2_seed58.json').read_text())['best_d'] == 4


def test_saved_baseline_witnesses():
    paths = list((Path(__file__).resolve().parents[1] / 'results' / 'baseline').glob('*.json'))
    assert len(paths) == 2
    for path in paths:
        result = json.loads(path.read_text())
        for witness in result['best_witnesses'] + result['bound_violations']:
            graph = Graph(witness['n'], witness['edges'])
            assert graph.n == 5 * result['k']
            assert is_triangle_free(graph)
            assert len(graph.edges) == witness['m']
            assert exact_max_cut(graph).value == witness['max_cut']
            side = set(witness['cut_side'])
            assert sum((u in side) != (v in side) for u, v in graph.edges) == witness['max_cut']
            assert witness['d'] == witness['m'] - witness['max_cut']
