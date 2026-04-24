#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
import json
import pathlib
import re
import sys

ROOT = pathlib.Path('.').resolve()

required_files = [
    'README.md',
    'REPO_CONTRACT.md',
    'GOVERNANCE.md',
    'SECURITY.md',
    'CHANGELOG.md',
    'LICENSE',
    'repo.manifest.json',
    'schemas/repo.manifest.schema.json',
    '.github/workflows/validate.yml',
    '.github/CODEOWNERS',
    '.github/pull_request_template.md',
    'docs/authority-boundary.md',
    'docs/operating-model.md',
    'docs/release-gates.md',
    'docs/decisions/0001-repo-created.md',
]

missing = [path for path in required_files if not (ROOT / path).is_file()]
if missing:
    print('missing required files:')
    for path in missing:
        print(f'  - {path}')
    sys.exit(1)

manifest_path = ROOT / 'repo.manifest.json'
schema_path = ROOT / 'schemas/repo.manifest.schema.json'

try:
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
except json.JSONDecodeError as exc:
    print(f'repo.manifest.json is invalid JSON: {exc}')
    sys.exit(1)

try:
    schema = json.loads(schema_path.read_text(encoding='utf-8'))
except json.JSONDecodeError as exc:
    print(f'repo.manifest.schema.json is invalid JSON: {exc}')
    sys.exit(1)

required_manifest_keys = schema.get('required', [])
missing_manifest_keys = [key for key in required_manifest_keys if key not in manifest]
if missing_manifest_keys:
    print('repo.manifest.json is missing required keys:')
    for key in missing_manifest_keys:
        print(f'  - {key}')
    sys.exit(1)

allowed_repo_classes = set(schema['properties']['repo_class']['enum'])
if manifest.get('repo_class') not in allowed_repo_classes:
    print(f"repo_class is not allowed: {manifest.get('repo_class')}")
    sys.exit(1)

allowed_statuses = set(schema['properties']['status']['enum'])
if manifest.get('status') not in allowed_statuses:
    print(f"status is not allowed: {manifest.get('status')}")
    sys.exit(1)

required_authority_keys = schema['properties']['authority']['required']
authority = manifest.get('authority', {})
missing_authority_keys = [key for key in required_authority_keys if key not in authority]
if missing_authority_keys:
    print('authority block is missing required keys:')
    for key in missing_authority_keys:
        print(f'  - {key}')
    sys.exit(1)

if not manifest.get('owners', {}).get('primary'):
    print('owners.primary is required')
    sys.exit(1)

secret_patterns = [
    re.compile(r'AKIA[0-9A-Z]{16}'),
    re.compile(r'gh[pousr]_[A-Za-z0-9_]{36,}'),
    re.compile(r'-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----'),
    re.compile(r'(?i)azure_client_secret\s*[=:]\s*[A-Za-z0-9_./+=-]{20,}'),
    re.compile(r'(?i)hubspot.*token\s*[=:]\s*[A-Za-z0-9_./+=-]{20,}'),
]

excluded_dirs = {'.git', 'node_modules', '.venv', 'dist', 'build', '.next'}
excluded_files = {
    pathlib.Path('scripts/validate-repo.sh'),
}

for path in ROOT.rglob('*'):
    rel = path.relative_to(ROOT)
    if any(part in excluded_dirs for part in rel.parts):
        continue
    if rel in excluded_files:
        continue
    if not path.is_file():
        continue
    try:
        text = path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    for pattern in secret_patterns:
        if pattern.search(text):
            print(f'possible secret-like material found in {rel}')
            sys.exit(1)

print('repo bootstrap validation passed')
PY
