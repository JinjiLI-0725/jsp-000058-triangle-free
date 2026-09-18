#!/usr/bin/env bash
# Build locally without installing system files. Requires curl, tar, gcc and make.
set -euo pipefail
build_root="${1:-/tmp/jsp58-nauty}"
mkdir -p "$build_root"
cd "$build_root"
curl -fL --max-time 120 https://users.cecs.anu.edu.au/~bdm/nauty/nauty2_9_3.tar.gz -o nauty2_9_3.tar.gz
printf '%s\n' '9fc4edae04f88a0f5883985be3b39cf7f898fd6cc96e96b9ee25452743cc1b5b  nauty2_9_3.tar.gz' | sha256sum -c -
tar --no-same-owner -xzf nauty2_9_3.tar.gz
cd nauty2_9_3
./configure
make -j2 geng labelg countg pickg
