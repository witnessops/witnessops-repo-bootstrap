#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

python3 "${SCRIPT_DIR}/validate_repo.py" --root "${REPO_ROOT}"
python3 -m unittest discover \
  -s "${REPO_ROOT}/tests" \
  -p 'test_*.py' \
  -v
