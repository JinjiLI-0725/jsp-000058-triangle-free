"""Separate, guarded I/O helpers for Candidate-A follow-up tools."""
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTECTED = ROOT / 'results/candidate_A_n20_large'


def safe_output(path, inputs=()):
    path = Path(path).resolve()
    if path == PROTECTED or PROTECTED in path.parents:
        raise ValueError('the active run directory is protected')
    for source in inputs:
        source = Path(source).resolve()
        if path == source or path in source.parents or source in path.parents:
            raise ValueError('output and input must be separate directories')
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_journal(path):
    """Only an unterminated final record may be discarded after a crash."""
    raw = Path(path).read_bytes()
    lines = raw.splitlines(keepends=True)
    rows = []
    for i, line in enumerate(lines):
        if not line.endswith(b'\n'):
            if i != len(lines) - 1:
                raise ValueError('unterminated interior record')
            break
        rows.append(json.loads(line))
    return rows, b''.join(lines[:len(rows)])


def fingerprint(paths):
    return {str(Path(p).resolve()): hashlib.sha256(Path(p).read_bytes()).hexdigest()
            for p in paths}


def durable(stream):
    stream.flush()
    os.fsync(stream.fileno())
