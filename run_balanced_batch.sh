#!/usr/bin/env bash

set -u

for t in $(seq 6 25); do
  echo "===== t=$t ====="

  if [ -f "results/balanced_extension/t${t}.json" ]; then
    echo "t=$t already complete, skipping"
    continue
  fi

  if [ -f "results/balanced_extension/t${t}.checkpoint.json" ]; then
    /tmp/check_ext_fast "$t" --resume
  else
    /tmp/check_ext_fast "$t"
  fi

  rc=$?
  if [ $rc -ne 0 ]; then
    echo "FAILED at t=$t with exit code $rc"
    exit $rc
  fi
done
