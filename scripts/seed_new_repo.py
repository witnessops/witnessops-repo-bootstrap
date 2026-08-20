#!/usr/bin/env python3
"""Seed a new WitnessOps repository from this bootstrap template.

Copies exactly the documented seeded inventory, rewrites every identity field
the validator checks, and then runs the copied validation gate with the new
repository identity. Fails closed if any rewrite or the gate fails.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

import validate_repo

TEMPLATE_ROOT = pathlib.Path(__file__).resolve().parents[1]
OWNER_PATTERN = r"^[A-Za-z0-9][A-Za-z0-9-]*$"

REMAINING_MANUAL_STEPS = [
    "Replace the README description and examples for the new repository.",
    "Replace the purpose, owned authority, excluded authority, and "
    "release-gate text in REPO_CONTRACT.md.",
    "Replace manifest authority values when the repository holds more than "
    "the seeded floor of none.",
    "Review SECURITY.md against the repository's actual data and runtime "
    "boundary.",
    "Create the GitHub repository under the same name, push, and confirm the "
    "validation workflow passes on the pushed commit.",
    "Apply and verify docs/repository-settings.md after the check exists.",
]


class SeedError(Exception):
    """Raised when the seed cannot be produced exactly as specified."""


def _single_line(value: str, label: str) -> str:
    stripped = value.strip()
    if not stripped or "\n" in value or "\r" in value:
        raise SeedError(f"{label} must be a non-empty single line")
    return stripped


def _template_repo_id() -> str:
    manifest = json.loads(
        (TEMPLATE_ROOT / "repo.manifest.json").read_text(encoding="utf-8")
    )
    return manifest["repo_id"]


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Seed a new WitnessOps repository from this template."
    )
    parser.add_argument(
        "target",
        type=pathlib.Path,
        help="directory to create for the new repository",
    )
    parser.add_argument(
        "--repo-id",
        help="new repository name (default: the target directory name)",
    )
    parser.add_argument(
        "--repo-class",
        required=True,
        choices=sorted(validate_repo.REPO_CLASSES),
        help="repository class recorded in the manifest and contract",
    )
    parser.add_argument(
        "--owner",
        required=True,
        help="primary owner GitHub account for governance, security, and "
        "CODEOWNERS",
    )
    parser.add_argument(
        "--maintainer",
        action="append",
        default=[],
        dest="maintainers",
        help="additional maintainer GitHub account (repeatable)",
    )
    parser.add_argument(
        "--purpose",
        required=True,
        help="bounded purpose recorded in the manifest created_for field",
    )
    parser.add_argument(
        "--no-git",
        action="store_true",
        help="skip initialising a Git repository in the target",
    )
    return parser.parse_args(argv)


def _check_arguments(args: argparse.Namespace) -> None:
    if re.fullmatch(validate_repo.REPO_ID_PATTERN, args.repo_id) is None:
        raise SeedError(
            f"repo_id {args.repo_id!r} does not match required pattern: "
            f"{validate_repo.REPO_ID_PATTERN}"
        )
    args.owner = _single_line(args.owner, "owner")
    if re.fullmatch(OWNER_PATTERN, args.owner) is None:
        raise SeedError(f"owner {args.owner!r} is not a plausible GitHub account")
    args.maintainers = [
        _single_line(maintainer, "maintainer") for maintainer in args.maintainers
    ]
    for maintainer in args.maintainers:
        if re.fullmatch(OWNER_PATTERN, maintainer) is None:
            raise SeedError(
                f"maintainer {maintainer!r} is not a plausible GitHub account"
            )
    if len(args.maintainers) != len(set(args.maintainers)):
        raise SeedError("maintainers must be unique")
    args.purpose = _single_line(args.purpose, "purpose")


def _check_target(target: pathlib.Path) -> None:
    if target.exists():
        if not target.is_dir():
            raise SeedError(f"target exists and is not a directory: {target}")
        if any(target.iterdir()):
            raise SeedError(f"target directory is not empty: {target}")
    if target == TEMPLATE_ROOT or TEMPLATE_ROOT in target.parents:
        raise SeedError("target must be outside the template repository")


def _copy_seed_inventory(target: pathlib.Path) -> None:
    for relative in validate_repo.REQUIRED_FILES:
        source = TEMPLATE_ROOT / relative
        if source.is_symlink() or not source.is_file():
            raise SeedError(
                f"template is missing required regular file: {relative}"
            )
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def _write_manifest(
    target: pathlib.Path, args: argparse.Namespace
) -> dict[str, object]:
    manifest_path = target / "repo.manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["repo_id"] = args.repo_id
    manifest["repo_class"] = args.repo_class
    manifest["status"] = "seeded"
    manifest["owners"] = {"primary": args.owner, "maintainers": args.maintainers}
    manifest["created_for"] = args.purpose
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def _replace_once(
    path: pathlib.Path, pattern: str, replacement: str, label: str
) -> None:
    text = path.read_text(encoding="utf-8")
    new_text, count = re.subn(
        pattern, lambda _match: replacement, text, count=1, flags=re.MULTILINE
    )
    if count != 1:
        raise SeedError(f"unable to rewrite {label} in {path}")
    path.write_text(new_text, encoding="utf-8")


def _rewrite_identity(target: pathlib.Path, args: argparse.Namespace) -> None:
    _replace_once(
        target / "README.md",
        r"^#\s+[^\n]+$",
        f"# {args.repo_id}",
        "the repository title",
    )
    contract = target / "REPO_CONTRACT.md"
    _replace_once(
        contract,
        r"^Repo:\s*`[^`]+`[ \t]*$",
        f"Repo: `{args.repo_id}`  ",
        "the repo identity line",
    )
    _replace_once(
        contract,
        r"^Class:\s*`[^`]+`[ \t]*$",
        f"Class: `{args.repo_class}`  ",
        "the class identity line",
    )
    _replace_once(
        contract,
        r"^Status:\s*`[^`]+`[ \t]*$",
        "Status: `seeded`",
        "the status identity line",
    )
    decision = target / "docs/decisions/0001-repo-created.md"
    _replace_once(
        decision,
        r"^Date:\s*[^\n]*$",
        f"Date: {datetime.date.today().isoformat()}",
        "the creation decision date",
    )
    _replace_once(
        decision,
        r"^Create\s+`[^`]+`[^\n]*$",
        f"Create `{args.repo_id}` from the `{_template_repo_id()}` bootstrap "
        f"template for: {args.purpose}",
        "the creation decision identity",
    )
    _replace_once(
        target / "GOVERNANCE.md",
        r"^Initial owner:\s*`[^`]+`[ \t]*$",
        f"Initial owner: `{args.owner}`",
        "the governance owner line",
    )
    _replace_once(
        target / "SECURITY.md",
        r"^Initial owner:\s*`[^`]+`[ \t]*$",
        f"Initial owner: `{args.owner}`",
        "the security owner line",
    )
    (target / ".github/CODEOWNERS").write_text(
        "# Initial owner boundary for repository governance.\n"
        f"* @{args.owner}\n",
        encoding="utf-8",
    )


def _run_validation_gate(target: pathlib.Path, repo_id: str) -> None:
    env = os.environ.copy()
    env.pop("GITHUB_REPOSITORY", None)
    env["WITNESSOPS_EXPECTED_REPO_ID"] = repo_id
    try:
        completed = subprocess.run(
            ["bash", "scripts/validate-repo.sh"],
            cwd=target,
            env=env,
            check=False,
        )
    except OSError as exc:
        raise SeedError(f"unable to run the validation gate: {exc}") from exc
    if completed.returncode != 0:
        raise SeedError(
            "the validation gate failed in the new repository; "
            "do not call it seeded"
        )


def _initialise_git(target: pathlib.Path) -> None:
    try:
        subprocess.run(
            ["git", "init", "--quiet", "--initial-branch=main", str(target)],
            check=True,
        )
        subprocess.run(["git", "-C", str(target), "add", "--all"], check=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        raise SeedError(f"unable to initialise git in {target}: {exc}") from exc


def _print_summary(target: pathlib.Path, manifest: dict[str, object]) -> None:
    owners = manifest["owners"]
    assert isinstance(owners, dict)
    print()
    print(f"seeded repository created: {target}")
    print(f"repo_id: {manifest['repo_id']}")
    print(f"repo_class: {manifest['repo_class']}")
    print(f"status: {manifest['status']}")
    print(f"owners.primary: {owners['primary']}")
    print("validation gate: passed (bash scripts/validate-repo.sh)")
    print()
    print("Remaining manual steps before feature work:")
    for index, step in enumerate(REMAINING_MANUAL_STEPS, start=1):
        print(f"{index}. {step}")
    print()
    print("The GitHub repository name must match repo_id. Until a matching")
    print("origin remote or CI identity exists, run the local gate with")
    print(f"WITNESSOPS_EXPECTED_REPO_ID={manifest['repo_id']}.")
    print()
    print("Claims not made: this seed is structural only. It is not verified,")
    print("production-ready, compliant, or proof-producing.")


def seed(args: argparse.Namespace) -> None:
    if not args.repo_id:
        args.repo_id = args.target.name
    _check_arguments(args)
    target = args.target.resolve()
    _check_target(target)
    target.mkdir(parents=True, exist_ok=True)
    _copy_seed_inventory(target)
    manifest = _write_manifest(target, args)
    _rewrite_identity(target, args)
    _run_validation_gate(target, args.repo_id)
    if not args.no_git:
        _initialise_git(target)
    _print_summary(target, manifest)


def main() -> int:
    args = _parse_args()
    try:
        seed(args)
    except SeedError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
