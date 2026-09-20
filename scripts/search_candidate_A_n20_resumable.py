"""Original search with crash-durable deterministic replay checkpoints.

Use the original CLI arguments plus --resume to continue this driver's output.
Replay reconstructs RNG, pool, current graph, cache and counters without max-cut
calls. It costs linear graph-generation time, and resumes at evaluation boundaries.
The legacy running process cannot acquire checkpoints retroactively.
"""
import io
import fcntl
import json
from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode = True

import search_candidate_A_n20 as original
from candidate_A_n20_support import safe_output, read_journal, durable, fingerprint
from triangle_free.research import atomic_json, graph6

RESUME = '--resume' in sys.argv
if RESUME:
    sys.argv.remove('--resume')


class ReplaySearch(original.Search):
    def __init__(self, output, **kwargs):
        output = safe_output(output)
        self.saved = []
        manifest_path = output / 'replay_manifest.json'
        dependencies = [Path(original.__file__), Path(__file__),
                        Path(__file__).with_name('candidate_A_n20_support.py'),
                        Path(original.__file__).with_name('libmaxcut_fast.so')]
        import triangle_free.core, triangle_free.heuristic, triangle_free.research
        import triangle_free.structural_analysis
        dependencies += [Path(m.__file__) for m in
                         (triangle_free.core, triangle_free.heuristic, triangle_free.research,
                          triangle_free.structural_analysis)]
        manifest = {'version': 1, 'argv': sys.argv[1:], 'python': sys.version,
                    'code_sha256': fingerprint(dependencies)}
        journal = output / 'evaluations.jsonl'
        if RESUME:
            self.lock = manifest_path.open('r')
            fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            if json.loads(manifest_path.read_text()) != manifest:
                raise ValueError('resume requires identical CLI, Python and source/library hashes')
            self.saved, committed = read_journal(journal)
            # Repair only our own interrupted final append.
            journal.write_bytes(committed)
        else:
            if any(output.iterdir()):
                raise ValueError('a fresh empty output directory is required')
            atomic_json(manifest_path, manifest)
            self.lock = manifest_path.open('r')
            fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        with tempfile.TemporaryDirectory(prefix='candidate-a-init-') as scratch:
            super().__init__(scratch, **kwargs)
            self.close()
        self.output = output
        self.log_path = journal
        self.log = journal.open('a')
        self.replay_record = None

    def evaluate_new(self, graph, source):
        if self.replay_record is None:
            return super().evaluate_new(graph, source)
        row = dict(self.replay_record)
        self.possible_failures += int(row['estimated_gap'] >= 8 and row['d'] >= 8)
        self.screen2_survivors += int('screen3_checked' in row)
        self.screen3_survivors += int('full_checked' in row)
        self.full_verifications += int('full_checked' in row)
        row.pop('index', None)
        return row

    def evaluate(self, graph, source):
        if self.requests < len(self.saved):
            row = self.saved[self.requests]
            if (row['index'] != self.requests or row['graph6'] != graph6(graph)
                    or row['source'] != source):
                raise ValueError('deterministic replay diverged; refusing continuation')
            self.replay_record = row
            real_log = self.log
            self.log = io.StringIO()
            try:
                result = super().evaluate(graph, source)
                if result != {k: v for k, v in row.items() if k != 'index'}:
                    # JSON turns tuples into lists; normalize before comparing.
                    if json.loads(json.dumps(result)) != {k: v for k, v in row.items() if k != 'index'}:
                        raise ValueError('replayed record mismatch')
                return result
            finally:
                self.log.close()
                self.log = real_log
                self.replay_record = None
        result = super().evaluate(graph, source)
        durable(self.log)
        atomic_json(self.output / 'checkpoint.json', {
            'version': 1, 'committed_evaluations': self.requests,
            'method': 'deterministic replay of durable evaluations.jsonl',
            'exhaustive_graph_search': False})
        return result


if __name__ == '__main__':
    original.Search = ReplaySearch
    original.main()
