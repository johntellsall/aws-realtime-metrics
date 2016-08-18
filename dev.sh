#!/usr/bin/env bash

set -euo pipefail # Bash strict mode
set -x # verbose mode

while true; do
    pip install -qr ./requirements.txt
    python $1 || true
    sleep 15
done
