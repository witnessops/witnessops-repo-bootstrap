#!/usr/bin/env python3
"""Validate the bounded WitnessOps repository seed contract."""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import subprocess
import sys
from typing import Any


REQUIRED_FILES = [
    ".gitignore",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "README.md",
    "REPO_CONTRACT.md",
    "GOVERNANCE.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "LICENSE",
    "repo.manifest.json",
    "schemas/repo.manifest.schema.json",
    "scripts/validate-repo.sh",
    "scripts/validate_repo.py",
    "tests/test_validate_repo.py",
    ".github/workflows/validate.yml",
    ".github/CODEOWNERS",
    ".github/dependabot.yml",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/repository-standard-gap.yml",
    "docs/authority-boundary.md",
    "docs/customization-checklist.md",
    "docs/operating-model.md",
    "docs/release-gates.md",
    "docs/repository-settings.md",
    "docs/decisions/0001-repo-created.md",
    "docs/decisions/0002-self-contained-seed-validation.md",
]

MANIFEST_FIELDS = {
    "allowed_secret_storage",
    "authority",
    "created_for",
    "forbidden",
    "owners",
    "proof_surfaces",
    "repo_class",
    "repo_id",
    "status",
}
AUTHORITY_FIELDS = {
    "evidence_authority",
    "governance_authority",
    "proof_authority",
    "runtime_authority",
    "source_authority",
    "verification_authority",
}
OWNER_FIELDS = {"maintainers", "primary"}
REPO_CLASSES = {
    "catalogue",
    "docs",
    "integration-bridge",
    "operator-tool",
    "proof-component",
    "sample-cases",
    "schema-registry",
    "site",
    "template",
    "verifier",
}
REPO_STATUSES = {"active", "archived", "deprecated", "experimental", "seeded"}
REPO_ID_PATTERN = r"^[a-z0-9][a-z0-9._-]*$"
JSON_SCHEMA_DRAFT = "https://json-schema.org/draft/2020-12/schema"
MANIFEST_SCHEMA_ID = "https://witnessops.com/schemas/repo.manifest.schema.json"
MANIFEST_SCHEMA_TITLE = "WitnessOps Repo Manifest"
ROOT_SCHEMA_FIELDS = {
    "$id",
    "$schema",
    "additionalProperties",
    "properties",
    "required",
    "title",
    "type",
}
OBJECT_SCHEMA_FIELDS = {"additionalProperties", "properties", "required", "type"}

SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{36,}"),
    re.compile(r"-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    re.compile(r"(?i)azure_client_secret\s*[=:]\s*[A-Za-z0-9_./+=-]{20,}"),
    re.compile(r"(?i)hubspot.*token\s*[=:]\s*[A-Za-z0-9_./+=-]{20,}"),
]

EXCLUDED_DIRS = {
    ".git",
    ".next",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
}

CANONICAL_VALIDATION_WORKFLOW = """name: Validate repo bootstrap

on:
  pull_request:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: validate-repo-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  validate:
    name: Validate repository contract
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Checkout
        uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5
        with:
          persist-credentials: false

      - name: Validate repository contract
        shell: bash
        run: bash scripts/validate-repo.sh
"""


class DuplicateJSONKey(ValueError):
    """Raised when a JSON object contains the same key more than once."""


def _reject_duplicate_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJSONKey(key)
        result[key] = value
    return result


def _read_text(
    path: pathlib.Path, label: str, errors: list[str]
) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"unable to read {label}: {exc}")
        return None


def _load_json(path: pathlib.Path, label: str, errors: list[str]) -> dict[str, Any]:
    text = _read_text(path, label, errors)
    if text is None:
        return {}
    try:
        payload = json.loads(text, object_pairs_hook=_reject_duplicate_json_keys)
    except DuplicateJSONKey as exc:
        errors.append(f"{label} contains duplicate key: {exc}")
        return {}
    except json.JSONDecodeError as exc:
        errors.append(f"{label} is invalid JSON: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"{label} must contain a JSON object")
        return {}
    return payload


def _check_exact_keys(
    value: dict[str, Any], expected: set[str], label: str, errors: list[str]
) -> None:
    missing = sorted(expected - set(value))
    unexpected = sorted(set(value) - expected)
    for key in missing:
        errors.append(f"{label} is missing required key: {key}")
    for key in unexpected:
        errors.append(f"{label} contains unsupported key: {key}")


def _check_nonempty_string(value: Any, label: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label} must be a non-empty string")


def _check_string_list(
    value: Any, label: str, errors: list[str], *, require_item: bool = False
) -> None:
    if not isinstance(value, list):
        errors.append(f"{label} must be an array")
        return
    if require_item and not value:
        errors.append(f"{label} must contain at least one item")
    invalid_entries = any(
        not isinstance(item, str) or not item.strip() for item in value
    )
    if invalid_entries:
        errors.append(f"{label} entries must be non-empty strings")
    elif len(value) != len(set(value)):
        errors.append(f"{label} entries must be unique")


def _string_set(value: Any, label: str, errors: list[str]) -> set[str] | None:
    if not isinstance(value, list) or any(
        not isinstance(item, str) for item in value
    ):
        errors.append(f"{label} must be an array of strings")
        return None
    if len(value) != len(set(value)):
        errors.append(f"{label} entries must be unique")
    return set(value)


def _object_schema(
    schema: Any,
    expected: set[str],
    label: str,
    errors: list[str],
    *,
    schema_fields: set[str] | None = None,
) -> dict[str, Any] | None:
    if not isinstance(schema, dict):
        errors.append(f"{label} must be an object schema")
        return None
    _check_exact_keys(schema, schema_fields or OBJECT_SCHEMA_FIELDS, label, errors)
    if schema.get("type") != "object":
        errors.append(f"{label}.type must be object")
    if schema.get("additionalProperties") is not False:
        errors.append(f"{label}.additionalProperties must be false")
    required = _string_set(schema.get("required"), f"{label}.required", errors)
    if required is not None and required != expected:
        errors.append(f"{label}.required does not match the bootstrap contract")
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        errors.append(f"{label}.properties must be an object")
        return None
    if set(properties) != expected:
        errors.append(f"{label}.properties does not match the bootstrap contract")
    return properties


def _check_string_schema(
    schema: Any,
    label: str,
    errors: list[str],
    *,
    extra_fields: set[str] | None = None,
) -> None:
    if not isinstance(schema, dict):
        errors.append(f"{label} must be a string schema")
        return
    expected_fields = {"minLength", "type"}
    if extra_fields:
        expected_fields.update(extra_fields)
    _check_exact_keys(schema, expected_fields, label, errors)
    if schema.get("type") != "string" or schema.get("minLength") != 1:
        errors.append(f"{label} must require a non-empty string")


def _check_string_array_schema(
    schema: Any, label: str, errors: list[str], *, require_item: bool = False
) -> None:
    if not isinstance(schema, dict):
        errors.append(f"{label} must be an array schema")
        return
    expected_fields = {"items", "type", "uniqueItems"}
    if require_item:
        expected_fields.add("minItems")
    _check_exact_keys(schema, expected_fields, label, errors)
    if schema.get("type") != "array":
        errors.append(f"{label}.type must be array")
    if schema.get("uniqueItems") is not True:
        errors.append(f"{label}.uniqueItems must be true")
    if require_item and schema.get("minItems") != 1:
        errors.append(f"{label}.minItems must be 1")
    _check_string_schema(schema.get("items"), f"{label}.items", errors)


def _validate_schema(schema: dict[str, Any], errors: list[str]) -> None:
    properties = _object_schema(
        schema,
        MANIFEST_FIELDS,
        "repo.manifest.schema.json",
        errors,
        schema_fields=ROOT_SCHEMA_FIELDS,
    )
    if properties is None:
        return
    if schema.get("$schema") != JSON_SCHEMA_DRAFT:
        errors.append("repo.manifest.schema.json.$schema does not match the contract")
    if schema.get("$id") != MANIFEST_SCHEMA_ID:
        errors.append("repo.manifest.schema.json.$id does not match the contract")
    if schema.get("title") != MANIFEST_SCHEMA_TITLE:
        errors.append("repo.manifest.schema.json.title does not match the contract")

    repo_id_schema = properties.get("repo_id")
    _check_string_schema(
        repo_id_schema,
        "schema.properties.repo_id",
        errors,
        extra_fields={"pattern"},
    )
    if (
        not isinstance(repo_id_schema, dict)
        or repo_id_schema.get("pattern") != REPO_ID_PATTERN
    ):
        errors.append("schema.properties.repo_id.pattern does not match the contract")

    for key, expected in (("repo_class", REPO_CLASSES), ("status", REPO_STATUSES)):
        item_schema = properties.get(key)
        _check_string_schema(
            item_schema,
            f"schema.properties.{key}",
            errors,
            extra_fields={"enum"},
        )
        if isinstance(item_schema, dict):
            enum = _string_set(
                item_schema.get("enum"), f"schema.properties.{key}.enum", errors
            )
            if enum is not None and enum != expected:
                errors.append(
                    f"schema.properties.{key}.enum does not match the contract"
                )

    authority_properties = _object_schema(
        properties.get("authority"),
        AUTHORITY_FIELDS,
        "schema.properties.authority",
        errors,
    )
    if authority_properties is not None:
        for key in AUTHORITY_FIELDS:
            _check_string_schema(
                authority_properties.get(key),
                f"schema.properties.authority.properties.{key}",
                errors,
            )

    owner_properties = _object_schema(
        properties.get("owners"), OWNER_FIELDS, "schema.properties.owners", errors
    )
    if owner_properties is not None:
        _check_string_schema(
            owner_properties.get("primary"),
            "schema.properties.owners.properties.primary",
            errors,
        )
        _check_string_array_schema(
            owner_properties.get("maintainers"),
            "schema.properties.owners.properties.maintainers",
            errors,
        )

    _check_string_array_schema(
        properties.get("allowed_secret_storage"),
        "schema.properties.allowed_secret_storage",
        errors,
    )
    _check_string_array_schema(
        properties.get("forbidden"),
        "schema.properties.forbidden",
        errors,
        require_item=True,
    )
    _check_string_array_schema(
        properties.get("proof_surfaces"),
        "schema.properties.proof_surfaces",
        errors,
    )
    _check_string_schema(
        properties.get("created_for"), "schema.properties.created_for", errors
    )


def _validate_manifest(manifest: dict[str, Any], errors: list[str]) -> None:
    _check_exact_keys(manifest, MANIFEST_FIELDS, "repo.manifest.json", errors)

    repo_id = manifest.get("repo_id")
    _check_nonempty_string(repo_id, "repo_id", errors)
    if isinstance(repo_id, str) and re.fullmatch(REPO_ID_PATTERN, repo_id) is None:
        errors.append(f"repo_id does not match required pattern: {REPO_ID_PATTERN}")

    for key, allowed in (("repo_class", REPO_CLASSES), ("status", REPO_STATUSES)):
        value = manifest.get(key)
        _check_nonempty_string(value, key, errors)
        if isinstance(value, str) and value not in allowed:
            errors.append(f"{key} is not allowed: {value}")

    authority = manifest.get("authority")
    if not isinstance(authority, dict):
        errors.append("authority must be an object")
    else:
        _check_exact_keys(authority, AUTHORITY_FIELDS, "authority", errors)
        for key in AUTHORITY_FIELDS:
            _check_nonempty_string(authority.get(key), f"authority.{key}", errors)

    owners = manifest.get("owners")
    if not isinstance(owners, dict):
        errors.append("owners must be an object")
    else:
        _check_exact_keys(owners, OWNER_FIELDS, "owners", errors)
        _check_nonempty_string(owners.get("primary"), "owners.primary", errors)
        _check_string_list(owners.get("maintainers"), "owners.maintainers", errors)

    _check_string_list(
        manifest.get("allowed_secret_storage"), "allowed_secret_storage", errors
    )
    _check_string_list(
        manifest.get("forbidden"), "forbidden", errors, require_item=True
    )
    _check_string_list(manifest.get("proof_surfaces"), "proof_surfaces", errors)
    _check_nonempty_string(manifest.get("created_for"), "created_for", errors)

    if manifest.get("repo_class") == "template":
        if manifest.get("allowed_secret_storage"):
            errors.append(
                "template repositories must default to no allowed secret storage"
            )
        if manifest.get("proof_surfaces"):
            errors.append("template repositories must default to no proof surfaces")


def _expected_repo_id(root: pathlib.Path) -> str | None:
    github_repository = os.environ.get("GITHUB_REPOSITORY", "").strip()
    if github_repository:
        return github_repository.rsplit("/", 1)[-1]

    explicit = os.environ.get("WITNESSOPS_EXPECTED_REPO_ID", "").strip()
    if explicit:
        return explicit

    try:
        completed = subprocess.run(
            ["git", "-C", str(root), "config", "--get", "remote.origin.url"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None
    remote = completed.stdout.strip()
    if not remote:
        return None
    remote = remote.rstrip("/").removesuffix(".git")
    return re.split(r"[/:]", remote)[-1] or None


def _check_cross_file_identity(
    root: pathlib.Path, manifest: dict[str, Any], errors: list[str]
) -> None:
    repo_id = manifest.get("repo_id")
    expected_repo_id = _expected_repo_id(root)
    if expected_repo_id is None:
        errors.append(
            "unable to determine repository identity; set "
            "WITNESSOPS_EXPECTED_REPO_ID for an unconfigured local copy"
        )
    elif repo_id != expected_repo_id:
        errors.append(
            f"repo_id {repo_id!r} does not match repository identity "
            f"{expected_repo_id!r}"
        )

    contract = _read_text(root / "REPO_CONTRACT.md", "REPO_CONTRACT.md", errors)
    if contract is not None:
        contract_fields = {
            "repo_id": re.search(
                r"^Repo:\s*`([^`]+)`[ \t]*$", contract, re.MULTILINE
            ),
            "repo_class": re.search(
                r"^Class:\s*`([^`]+)`[ \t]*$", contract, re.MULTILINE
            ),
            "status": re.search(
                r"^Status:\s*`([^`]+)`[ \t]*$", contract, re.MULTILINE
            ),
        }
        for key, match in contract_fields.items():
            if not match:
                errors.append(f"REPO_CONTRACT.md is missing its {key} identity line")
            elif match.group(1) != manifest.get(key):
                errors.append(
                    f"REPO_CONTRACT.md {key} does not match repo.manifest.json"
                )

    readme = _read_text(root / "README.md", "README.md", errors)
    if readme is not None:
        readme_title = re.search(r"^#\s+([^\n]+)$", readme, re.MULTILINE)
        if not readme_title:
            errors.append("README.md is missing its repository title")
        elif readme_title.group(1).strip() != repo_id:
            errors.append("README.md title does not match repo.manifest.json")

    creation_decision = _read_text(
        root / "docs/decisions/0001-repo-created.md",
        "docs/decisions/0001-repo-created.md",
        errors,
    )
    if creation_decision is not None:
        decision_repo = re.search(
            r"^Create\s+`([^`]+)`(?:[ \t]|$)", creation_decision, re.MULTILINE
        )
        if not decision_repo:
            errors.append("repository creation decision is missing its Create identity")
        elif decision_repo.group(1) != repo_id:
            errors.append(
                "repository creation decision does not match repo.manifest.json"
            )

    owners = manifest.get("owners")
    primary = owners.get("primary") if isinstance(owners, dict) else None
    governance = _read_text(root / "GOVERNANCE.md", "GOVERNANCE.md", errors)
    if governance is not None:
        governance_owner = re.search(
            r"^Initial owner:\s*`([^`]+)`[ \t]*$", governance, re.MULTILINE
        )
        if not governance_owner:
            errors.append("GOVERNANCE.md is missing the initial owner line")
        elif governance_owner.group(1) != primary:
            errors.append("GOVERNANCE.md owner does not match repo.manifest.json")

    security = _read_text(root / "SECURITY.md", "SECURITY.md", errors)
    if security is not None:
        security_owner = re.search(
            r"^Initial owner:\s*`([^`]+)`[ \t]*$", security, re.MULTILINE
        )
        if not security_owner:
            errors.append("SECURITY.md is missing the initial owner line")
        elif security_owner.group(1) != primary:
            errors.append("SECURITY.md owner does not match repo.manifest.json")

    codeowners = _read_text(root / ".github/CODEOWNERS", ".github/CODEOWNERS", errors)
    if codeowners is not None and isinstance(primary, str):
        catch_all_owner = f"@{primary}"
        has_primary_catch_all = False
        all_rules_include_primary = True
        for line in codeowners.splitlines():
            rule = line.split("#", 1)[0].strip()
            if not rule:
                continue
            parts = rule.split()
            if len(parts) < 2 or catch_all_owner not in parts[1:]:
                all_rules_include_primary = False
            if parts[0] == "*" and catch_all_owner in parts[1:]:
                has_primary_catch_all = True
        if not has_primary_catch_all:
            errors.append("CODEOWNERS must contain a catch-all rule for owners.primary")
        if not all_rules_include_primary:
            errors.append("every CODEOWNERS rule must include owners.primary")


def _check_documented_inventory(root: pathlib.Path, errors: list[str]) -> None:
    readme = _read_text(root / "README.md", "README.md", errors)
    if readme is None:
        return
    match = re.search(
        r"A new WitnessOps repo should begin with:[ \t]*\n+```text\n(.*?)\n```",
        readme,
        re.DOTALL,
    )
    if not match:
        errors.append("README.md is missing the seeded repository inventory")
        return

    documented = [line.strip() for line in match.group(1).splitlines() if line.strip()]
    if len(documented) != len(set(documented)):
        errors.append("README.md seeded repository inventory contains duplicates")
    missing = sorted(set(REQUIRED_FILES) - set(documented))
    unexpected = sorted(set(documented) - set(REQUIRED_FILES))
    for path in missing:
        errors.append(f"README.md seeded repository inventory is missing: {path}")
    for path in unexpected:
        errors.append(f"README.md seeded repository inventory is unsupported: {path}")


def _check_workflow_boundary(root: pathlib.Path, errors: list[str]) -> None:
    workflow = _read_text(
        root / ".github/workflows/validate.yml",
        ".github/workflows/validate.yml",
        errors,
    )
    if workflow is not None and workflow != CANONICAL_VALIDATION_WORKFLOW:
        errors.append(
            "validation workflow does not match the canonical self-contained baseline"
        )


def _check_template_workflow_inventory(
    root: pathlib.Path, manifest: dict[str, Any], errors: list[str]
) -> None:
    if manifest.get("repo_class") != "template":
        return
    workflows = root / ".github/workflows"
    try:
        actual = {
            path.name
            for path in workflows.iterdir()
            if path.is_file() and path.suffix in {".yml", ".yaml"}
        }
    except OSError as exc:
        errors.append(f"unable to inspect .github/workflows: {exc}")
        return
    expected = {"validate.yml"}
    if actual != expected:
        errors.append(
            "template workflow inventory must contain only "
            ".github/workflows/validate.yml"
        )


def _scan_secret_like_material(root: pathlib.Path, errors: list[str]) -> None:
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in EXCLUDED_DIRS for part in relative.parts):
            continue
        if path.is_symlink() or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        except OSError as exc:
            errors.append(f"unable to scan {relative}: {exc}")
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"possible secret-like material found in {relative}")
                break


def validate(root: pathlib.Path) -> list[str]:
    errors: list[str] = []
    symlinks = [path for path in REQUIRED_FILES if (root / path).is_symlink()]
    errors.extend(
        f"required file must not be a symbolic link: {path}" for path in symlinks
    )
    missing = [
        path
        for path in REQUIRED_FILES
        if not (root / path).is_file() and not (root / path).is_symlink()
    ]
    errors.extend(f"missing required file: {path}" for path in missing)
    if missing or symlinks:
        return errors

    manifest = _load_json(root / "repo.manifest.json", "repo.manifest.json", errors)
    schema = _load_json(
        root / "schemas/repo.manifest.schema.json",
        "repo.manifest.schema.json",
        errors,
    )
    if errors:
        return errors

    _validate_schema(schema, errors)
    _validate_manifest(manifest, errors)
    _check_documented_inventory(root, errors)
    _check_cross_file_identity(root, manifest, errors)
    _check_workflow_boundary(root, errors)
    _check_template_workflow_inventory(root, manifest, errors)
    _scan_secret_like_material(root, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=pathlib.Path, default=pathlib.Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("repo bootstrap validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
