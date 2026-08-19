import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_repo.py"


class ValidateRepoTests(unittest.TestCase):
    def run_validator(
        self,
        root: Path,
        expected_repo_id: str | None,
        extra_env: dict[str, str] | None = None,
    ):
        env = os.environ.copy()
        env.pop("GITHUB_REPOSITORY", None)
        env.pop("WITNESSOPS_EXPECTED_REPO_ID", None)
        if expected_repo_id is not None:
            env["WITNESSOPS_EXPECTED_REPO_ID"] = expected_repo_id
        if extra_env:
            env.update(extra_env)
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "--root", str(root)],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )

    def copy_repository(self, destination: Path) -> Path:
        target = destination / "repository"
        shutil.copytree(
            ROOT,
            target,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", ".venv"),
        )
        return target

    def test_current_repository_passes(self):
        result = self.run_validator(ROOT, "witnessops-repo-bootstrap")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("repo bootstrap validation passed", result.stdout)

    def test_missing_required_file_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            target = self.copy_repository(Path(temp))
            (target / "SECURITY.md").unlink()
            result = self.run_validator(target, "witnessops-repo-bootstrap")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing required file: SECURITY.md", result.stderr)

    def test_documented_inventory_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            target = self.copy_repository(Path(temp))
            readme = target / "README.md"
            readme.write_text(
                readme.read_text(encoding="utf-8").replace("CONTRIBUTING.md\n", ""),
                encoding="utf-8",
            )
            result = self.run_validator(target, "witnessops-repo-bootstrap")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("inventory is missing: CONTRIBUTING.md", result.stderr)

    def test_unexpected_manifest_key_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            target = self.copy_repository(Path(temp))
            path = target / "repo.manifest.json"
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["unreviewed_authority"] = "runtime"
            path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            result = self.run_validator(target, "witnessops-repo-bootstrap")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("contains unsupported key: unreviewed_authority", result.stderr)

    def test_duplicate_manifest_key_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            target = self.copy_repository(Path(temp))
            path = target / "repo.manifest.json"
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    '  "repo_id": "witnessops-repo-bootstrap",',
                    '  "repo_id": "witnessops-repo-bootstrap",\n'
                    '  "repo_id": "shadow-repository",',
                    1,
                ),
                encoding="utf-8",
            )
            result = self.run_validator(target, "witnessops-repo-bootstrap")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("contains duplicate key: repo_id", result.stderr)

    def test_damaged_schema_fails_without_crashing(self):
        with tempfile.TemporaryDirectory() as temp:
            target = self.copy_repository(Path(temp))
            path = target / "schemas/repo.manifest.schema.json"
            schema = json.loads(path.read_text(encoding="utf-8"))
            schema["properties"]["repo_id"]["pattern"] = ".*"
            path.write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")
            result = self.run_validator(target, "witnessops-repo-bootstrap")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("repo_id.pattern does not match", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_unsupported_schema_keyword_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            target = self.copy_repository(Path(temp))
            path = target / "schemas/repo.manifest.schema.json"
            schema = json.loads(path.read_text(encoding="utf-8"))
            schema["properties"]["repo_id"]["default"] = "shadow-repository"
            path.write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")
            result = self.run_validator(target, "witnessops-repo-bootstrap")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("contains unsupported key: default", result.stderr)

    def test_stale_template_identity_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            target = self.copy_repository(Path(temp))
            result = self.run_validator(target, "new-witnessops-repository")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not match repository identity", result.stderr)

    def test_missing_repository_identity_source_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            target = self.copy_repository(Path(temp))
            result = self.run_validator(target, None)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unable to determine repository identity", result.stderr)

    def test_github_repository_identity_overrides_local_override(self):
        result = self.run_validator(
            ROOT,
            "untrusted-local-override",
            {"GITHUB_REPOSITORY": "witnessops/witnessops-repo-bootstrap"},
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_customized_repository_identity_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            target = self.copy_repository(Path(temp))
            manifest_path = target / "repo.manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["repo_id"] = "new-witnessops-repository"
            manifest_path.write_text(
                json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
            )

            replacements = {
                "REPO_CONTRACT.md": (
                    "Repo: `witnessops-repo-bootstrap`",
                    "Repo: `new-witnessops-repository`",
                ),
                "README.md": (
                    "# witnessops-repo-bootstrap",
                    "# new-witnessops-repository",
                ),
                "docs/decisions/0001-repo-created.md": (
                    "Create `witnessops-repo-bootstrap`",
                    "Create `new-witnessops-repository`",
                ),
            }
            for relative, (old, new) in replacements.items():
                path = target / relative
                path.write_text(
                    path.read_text(encoding="utf-8").replace(old, new),
                    encoding="utf-8",
                )

            result = self.run_validator(target, "new-witnessops-repository")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_invalid_manifest_type_fails_without_crashing(self):
        with tempfile.TemporaryDirectory() as temp:
            target = self.copy_repository(Path(temp))
            path = target / "repo.manifest.json"
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["repo_class"] = ["template"]
            path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            result = self.run_validator(target, "witnessops-repo-bootstrap")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("repo_class must be a non-empty string", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_contract_manifest_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            target = self.copy_repository(Path(temp))
            contract = target / "REPO_CONTRACT.md"
            contract.write_text(
                contract.read_text(encoding="utf-8").replace(
                    "Class: `template`", "Class: `site`"
                ),
                encoding="utf-8",
            )
            result = self.run_validator(target, "witnessops-repo-bootstrap")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("repo_class does not match", result.stderr)

    def test_owner_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            target = self.copy_repository(Path(temp))
            security = target / "SECURITY.md"
            security.write_text(
                security.read_text(encoding="utf-8").replace(
                    "Initial owner: `VaultSovereign`",
                    "Initial owner: `DifferentOwner`",
                ),
                encoding="utf-8",
            )
            result = self.run_validator(target, "witnessops-repo-bootstrap")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("SECURITY.md owner does not match", result.stderr)

    def test_codeowners_comment_only_reference_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            target = self.copy_repository(Path(temp))
            (target / ".github/CODEOWNERS").write_text(
                "# @VaultSovereign is not an effective ownership rule.\n",
                encoding="utf-8",
            )
            result = self.run_validator(target, "witnessops-repo-bootstrap")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must contain a catch-all rule", result.stderr)

    def test_codeowners_later_override_without_primary_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            target = self.copy_repository(Path(temp))
            (target / ".github/CODEOWNERS").write_text(
                "* @VaultSovereign\n.github/** @DifferentOwner\n",
                encoding="utf-8",
            )
            result = self.run_validator(target, "witnessops-repo-bootstrap")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("every CODEOWNERS rule must include", result.stderr)

    def test_required_file_symlink_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            target = self.copy_repository(Path(temp))
            security = target / "SECURITY.md"
            security.unlink()
            security.symlink_to("README.md")
            result = self.run_validator(target, "witnessops-repo-bootstrap")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "required file must not be a symbolic link: SECURITY.md",
            result.stderr,
        )

    def test_secret_like_material_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            target = self.copy_repository(Path(temp))
            (target / "leak.txt").write_text("AKIA" + "A" * 16 + "\n", encoding="utf-8")
            result = self.run_validator(target, "witnessops-repo-bootstrap")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("possible secret-like material found in leak.txt", result.stderr)

    def test_workflow_secret_dependency_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            target = self.copy_repository(Path(temp))
            workflow = target / ".github/workflows/validate.yml"
            workflow.write_text(
                workflow.read_text(encoding="utf-8")
                + "\n# forbidden regression: ${{ secrets.ORGANIZATION_TOKEN }}\n",
                encoding="utf-8",
            )
            result = self.run_validator(target, "witnessops-repo-bootstrap")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "does not match the canonical self-contained baseline", result.stderr
        )

    def test_workflow_unpinned_action_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            target = self.copy_repository(Path(temp))
            workflow = target / ".github/workflows/validate.yml"
            workflow.write_text(
                workflow.read_text(encoding="utf-8").replace(
                    "actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5",
                    "actions/checkout@v4",
                ),
                encoding="utf-8",
            )
            result = self.run_validator(target, "witnessops-repo-bootstrap")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "does not match the canonical self-contained baseline", result.stderr
        )

    def test_workflow_job_skip_override_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            target = self.copy_repository(Path(temp))
            workflow = target / ".github/workflows/validate.yml"
            workflow.write_text(
                workflow.read_text(encoding="utf-8").replace(
                    "    runs-on: ubuntu-latest",
                    "    if: false\n    runs-on: ubuntu-latest",
                    1,
                ),
                encoding="utf-8",
            )
            result = self.run_validator(target, "witnessops-repo-bootstrap")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "does not match the canonical self-contained baseline", result.stderr
        )

    def test_workflow_shorthand_step_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            target = self.copy_repository(Path(temp))
            workflow = target / ".github/workflows/validate.yml"
            workflow.write_text(
                workflow.read_text(encoding="utf-8").replace(
                    "        run: bash scripts/validate-repo.sh",
                    "        run: bash scripts/validate-repo.sh\n"
                    "      - run: echo unexpected",
                    1,
                ),
                encoding="utf-8",
            )
            result = self.run_validator(target, "witnessops-repo-bootstrap")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "does not match the canonical self-contained baseline", result.stderr
        )

    def test_template_additional_workflow_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            target = self.copy_repository(Path(temp))
            (target / ".github/workflows/extra.yml").write_text(
                "name: Extra\non: workflow_dispatch\njobs: {}\n",
                encoding="utf-8",
            )
            result = self.run_validator(target, "witnessops-repo-bootstrap")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("workflow inventory must contain only", result.stderr)


if __name__ == "__main__":
    unittest.main()
