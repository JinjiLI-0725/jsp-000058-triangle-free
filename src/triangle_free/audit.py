"""Cross-check triangle-filtered generation against unrestricted geng + pickg."""

import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile
import time

from .research import atomic_json, canonicalize, sha256


def audit(output, geng, pickg, labelg):
    output = Path(output)
    metadata = json.loads((output / 'generator.json').read_text())
    corpus = output / 'graphs.g6'
    if sha256(corpus) != metadata['corpus_sha256']:
        raise ValueError('corpus checksum mismatch')
    commands = [[str(geng), str(metadata['n'])], [str(pickg), '-T0'], [str(labelg), '-q']]
    start = time.monotonic()
    # Stream the unrestricted corpus rather than holding millions of graphs in memory.
    with tempfile.TemporaryFile(mode='w+t') as error:
        generator = subprocess.Popen(commands[0], stdout=subprocess.PIPE, stderr=error, text=True)
        try:
            picker = subprocess.Popen(commands[1], stdin=generator.stdout, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE, text=True)
            generator.stdout.close()
            filtered, picker_error = picker.communicate()
            returncode = generator.wait()
            if returncode or picker.returncode:
                raise RuntimeError(f'geng/pickg failed: {returncode}/{picker.returncode}: {picker_error}')
        finally:
            if generator.poll() is None:
                generator.terminate()
                generator.wait()
        error.seek(0)
        generator_error = error.read()
    match = re.search(r'>Z\s+(\d+) graphs generated', generator_error)
    if not match:
        raise RuntimeError('missing unrestricted geng completion count')
    canonical = canonicalize(filtered.splitlines(), labelg)
    expected = corpus.read_text().splitlines()
    if len(canonical) != len(expected) or len(set(canonical)) != len(canonical) or set(canonical) != set(expected):
        raise RuntimeError('filtered unrestricted generation disagrees with triangle-free generation')
    result = {'status': 'complete', 'n': metadata['n'], 'commands': commands,
              'unrestricted_graphs': int(match[1]), 'triangle_free_graphs': len(canonical),
              'canonical_sets_equal': True, 'corpus_sha256': sha256(corpus),
              'generator_stderr': generator_error, 'picker_stderr': picker_error,
              'binary_sha256': {name: sha256(path) for name, path in [('geng', geng), ('pickg', pickg), ('labelg', labelg)]},
              'audit_source_sha256': sha256(__file__), 'elapsed_seconds': time.monotonic() - start,
              'limitation': 'Different generation/filtering paths, but both use the same nauty package; not fully independent software.'}
    atomic_json(output / 'generation_audit.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('results/exhaustive_k2'))
    parser.add_argument('--nauty-dir', type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.output, *(args.nauty_dir / name for name in ('geng', 'pickg', 'labelg')))
    print(f"Matched all {result['triangle_free_graphs']} classes after filtering {result['unrestricted_graphs']} unrestricted graphs.")


if __name__ == '__main__':
    main()
