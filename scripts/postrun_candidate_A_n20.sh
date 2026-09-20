#!/usr/bin/env bash
# Read-only input; default output is separate from the active search.
set -euo pipefail
repo=$(cd "$(dirname "$0")/.." && pwd)
cd "$repo"
export PYTHONPATH="$repo/src${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONDONTWRITEBYTECODE=1
exec nice -n 15 "$repo/.venv/bin/python" scripts/analyze_candidate_A_n20.py \
  --input "${1:-results/candidate_A_n20_large}" \
  --output "${2:-results/candidate_A_n20_postrun}" "${@:3}"
