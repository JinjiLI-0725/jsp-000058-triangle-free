"""Regression checks for isolated follow-up tools (no active-run access)."""
import json
from pathlib import Path
import sys

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import candidate_A_n20_support as support
import analyze_candidate_A_n20 as analysis
from triangle_free.core import Graph, c5_blowup, deletion_distance, random_triangle_free
from triangle_free.research import graph6, canonicalize


def test_protected_output(tmp_path):
    with pytest.raises(ValueError):
        support.safe_output(support.PROTECTED / 'never-create')
    link = tmp_path / 'alias'
    link.symlink_to(support.PROTECTED, target_is_directory=True)
    with pytest.raises(ValueError):
        support.safe_output(link / 'never-create')
    with pytest.raises(ValueError):
        support.safe_output(tmp_path, [tmp_path / 'input'])


def test_journal_torn_tail_and_corruption(tmp_path):
    p = tmp_path / 'log'
    p.write_bytes(b'{"index": 0}\n{"index":')
    assert support.read_journal(p) == ([{'index': 0}], b'{"index": 0}\n')
    p.write_bytes(b'bad\n')
    with pytest.raises(json.JSONDecodeError):
        support.read_journal(p)


def test_extract_includes_unsampled_and_duplicates():
    records = [dict(graph6='x', source='a', index=0, estimated_gap=7, d=7),
               dict(graph6='x', source='b', index=1, estimated_gap=7, d=7),
               dict(graph6='y', source='a', index=2, estimated_gap=8, d=10),
               dict(graph6='z', source='a', index=3, estimated_gap=6, d=10)]
    rows = analysis.extract(records)
    assert len(rows) == 2
    assert rows[0]['sources'] == ['a', 'b']
    assert rows[0]['indices'] == [0, 1]


def test_fast_oracle_against_reference():
    import random
    oracle = analysis.CutOracle()
    for n in (0, 1, 5, 9, 15):
        g = random_triangle_free(n, random.Random(n))
        assert oracle.distance(g) == deletion_distance(g)


def test_b4_structure_and_canonical_relabel():
    import random
    import shutil
    labelg = shutil.which('nauty-labelg') or shutil.which('labelg')
    if not labelg:
        pytest.skip('nauty not installed')
    g = c5_blowup(4)
    permutation = list(range(20))
    random.Random(123).shuffle(permutation)
    h = Graph(20, tuple((permutation[u], permutation[v]) for u, v in g.edges))
    assert graph6(g) != graph6(h)
    canon = canonicalize([graph6(g), graph6(h)], labelg)
    assert canon[0] == canon[1]
    info = analysis.structure(canon[0])
    assert info['is_B4'] and info['independence_number'] == 8
    assert info['degree_sequence'] == [8] * 20


def test_verify_full_deletion_domain_and_resume(tmp_path):
    # A synthetic oracle isolates enumeration/checkpoint mechanics; empty graph
    # also agrees with both real independent reference checks.
    class Zero:
        calls = 0
        def distance(self, graph):
            self.calls += 1
            return 0
    oracle = Zero()
    checkpoint = tmp_path / 'verify.json'
    result = analysis.verify(graph6(Graph(20)), oracle, checkpoint, batch=4000)
    assert result['checked'] == 15504
    assert result['Delta5'] == 0
    assert result['maximizer_count'] == 15504
    assert result['maximizer_vertex_incidence'] == [3876] * 20
    assert oracle.calls == 15505
    again = Zero()
    assert analysis.verify(graph6(Graph(20)), again, checkpoint) == result
    assert again.calls == 1


def test_search_resume_replays_identical_trajectory(tmp_path):
    import os
    import subprocess
    env = dict(os.environ, PYTHONPATH=str(SCRIPTS.parent / 'src'), PYTHONDONTWRITEBYTECODE='1')
    command = [sys.executable, str(SCRIPTS / 'search_candidate_A_n20_resumable.py'),
               '--output', str(tmp_path / 'search'), '--seeds', '801', '--samples', '0',
               '--steps', '2', '--screen1', '4', '--screen2', '8', '--screen3', '16']
    subprocess.run(command, env=env, check=True, capture_output=True)
    output = tmp_path / 'search'
    expected = (output / 'evaluations.jsonl').read_bytes()
    expected_summary = json.loads((output / 'result.json').read_text())
    lines = expected.splitlines(keepends=True)
    (output / 'evaluations.jsonl').write_bytes(b''.join(lines[:2]) + b'{"torn":')
    subprocess.run(command + ['--resume'], env=env, check=True, capture_output=True)
    assert (output / 'evaluations.jsonl').read_bytes() == expected
    assert json.loads((output / 'result.json').read_text()) == expected_summary
    subprocess.run(command + ['--resume'], env=env, check=True, capture_output=True)
    assert (output / 'evaluations.jsonl').read_bytes() == expected


def test_partial_exact_checkpoint_resume(tmp_path):
    class Interrupted:
        calls = 0
        def distance(self, graph):
            self.calls += 1
            if self.calls == 520:
                raise InterruptedError('simulated interruption')
            return 0
    class Zero:
        def distance(self, graph):
            return 0
    checkpoint = tmp_path / 'partial.json'
    with pytest.raises(InterruptedError):
        analysis.verify(graph6(Graph(20)), Interrupted(), checkpoint)
    assert json.loads(checkpoint.read_text())['checked'] == 512
    result = analysis.verify(graph6(Graph(20)), Zero(), checkpoint, batch=4000)
    assert result['checked'] == 15504
    assert result['core_d_histogram'] == {0: 15504}
    assert result['maximizer_vertex_incidence'] == [3876] * 20
