import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SEEDER = ROOT / "scripts" / "seed_new_repo.py"

sys.path.insert(0, str(ROOT / "scripts"))
import validate_repo  # noqa: E402


class SeedNewRepoTests(unittest.TestCase):
    def run_seeder(self, *args: str):
        env = os.environ.copy()
        env.pop("GITHUB_REPOSITORY", None)
        env.pop("WITNESSOPS_EXPECTED_REPO_ID", None)
        return subprocess.run(
            [sys.executable, str(SEEDER), *args],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )

    def test_seed_produces_exact_inventory_and_passes_gate(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "new-witnessops-repository"
            result = self.run_seeder(
                str(target),
                "--repo-class",
                "docs",
                "--owner",
                "ExampleOwner",
                "--maintainer",
                "ExampleMaintainer",
                "--purpose",
                "Bounded documentation seed for regression tests.",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("repo bootstrap validation passed", result.stdout)
            self.assertIn("validation gate: passed", result.stdout)
            self.assertIn("Claims not made", result.stdout)

            seeded_files = {
                str(path.relative_to(target))
                for path in target.rglob("*")
                if path.is_file()
                and not {".git", "__pycache__"}
                & set(path.relative_to(target).parts)
            }
            self.assertEqual(seeded_files, set(validate_repo.REQUIRED_FILES))
            self.assertTrue((target / ".git").is_dir())

            manifest = json.loads(
                (target / "repo.manifest.json").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["repo_id"], "new-witnessops-repository")
            self.assertEqual(manifest["repo_class"], "docs")
            self.assertEqual(manifest["status"], "seeded")
            self.assertEqual(manifest["owners"]["primary"], "ExampleOwner")
            self.assertEqual(
                manifest["owners"]["maintainers"], ["ExampleMaintainer"]
            )
            self.assertEqual(
                manifest["created_for"],
                "Bounded documentation seed for regression tests.",
            )

            readme = (target / "README.md").read_text(encoding="utf-8")
            self.assertTrue(readme.startswith("# new-witnessops-repository\n"))
            contract = (target / "REPO_CONTRACT.md").read_text(encoding="utf-8")
            self.assertIn("Repo: `new-witnessops-repository`", contract)
            self.assertIn("Class: `docs`", contract)
            self.assertIn("Status: `seeded`", contract)
            governance = (target / "GOVERNANCE.md").read_text(encoding="utf-8")
            self.assertIn("Initial owner: `ExampleOwner`", governance)
            security = (target / "SECURITY.md").read_text(encoding="utf-8")
            self.assertIn("Initial owner: `ExampleOwner`", security)
            codeowners = (target / ".github/CODEOWNERS").read_text(
                encoding="utf-8"
            )
            self.assertIn("* @ExampleOwner", codeowners)
            decision = (
                target / "docs/decisions/0001-repo-created.md"
            ).read_text(encoding="utf-8")
            self.assertIn("Create `new-witnessops-repository`", decision)

    def test_no_git_skips_git_initialisation(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "seed-without-git"
            result = self.run_seeder(
                str(target),
                "--repo-class",
                "docs",
                "--owner",
                "ExampleOwner",
                "--purpose",
                "Bounded seed without git initialisation.",
                "--no-git",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((target / ".git").exists())

    def test_rejects_invalid_repo_id(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "Invalid_Name"
            result = self.run_seeder(
                str(target),
                "--repo-class",
                "docs",
                "--owner",
                "ExampleOwner",
                "--purpose",
                "Bounded purpose.",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("does not match required pattern", result.stderr)
            self.assertFalse(target.exists())

    def test_rejects_nonempty_target(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "occupied-target"
            target.mkdir()
            (target / "existing.txt").write_text("occupied\n", encoding="utf-8")
            result = self.run_seeder(
                str(target),
                "--repo-class",
                "docs",
                "--owner",
                "ExampleOwner",
                "--purpose",
                "Bounded purpose.",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("not empty", result.stderr)
            self.assertEqual(
                {path.name for path in target.iterdir()}, {"existing.txt"}
            )

    def test_rejects_multiline_purpose(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "multiline-purpose"
            result = self.run_seeder(
                str(target),
                "--repo-class",
                "docs",
                "--owner",
                "ExampleOwner",
                "--purpose",
                "line one\nline two",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("purpose must be a non-empty single line", result.stderr)
            self.assertFalse(target.exists())

    def test_rejects_unknown_repo_class(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "unknown-class"
            result = self.run_seeder(
                str(target),
                "--repo-class",
                "unreviewed-runtime",
                "--owner",
                "ExampleOwner",
                "--purpose",
                "Bounded purpose.",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("invalid choice", result.stderr)
            self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
