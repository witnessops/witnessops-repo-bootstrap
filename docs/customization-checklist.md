# Repository Customization Checklist

Use this checklist immediately after creating or copying a repository from this
bootstrap. The copied files describe the bootstrap repository until each item is
made specific to the new repository.

## Required identity changes

1. Set `repo.manifest.json.repo_id` to the exact GitHub repository name.
2. Select the real `repo_class` and current `status`.
3. Replace every authority value with the real authority or `none`.
4. Set the primary owner and current maintainers.
5. Keep `allowed_secret_storage` empty unless the repository actually uses a
   named external secret store.
6. Declare real proof surfaces only when they exist.
7. Replace `created_for` with the repository's bounded purpose.

## Required contract changes

- Make the identity lines in `REPO_CONTRACT.md` match the manifest.
- Make the first README heading match `repo_id`.
- Replace the repository identity and decision text in
  `docs/decisions/0001-repo-created.md`.
- Replace the purpose, owned authority, excluded authority, and release gates.
- Make the owner in `GOVERNANCE.md` match `owners.primary`.
- Make the owner in `SECURITY.md` match `owners.primary`.
- Make `.github/CODEOWNERS` name the same primary owner.
- Replace the README description and examples.
- Review `SECURITY.md` against the repository's actual data and runtime boundary.
- Review the inherited self-contained-validation decision and record any
  repository-specific exception under `docs/decisions/`.
- If the copied repository needs another workflow, first change its class from
  `template` and document that workflow's execution, permission, credential, and
  authority boundary. The bootstrap does not authorize it automatically.
- Apply and verify `docs/repository-settings.md` after the validation check exists.

## Validation

Run from the repository root:

```bash
bash scripts/validate-repo.sh
```

For a local copy without `GITHUB_REPOSITORY` or a configured Git remote, supply
the expected identity:

```bash
WITNESSOPS_EXPECTED_REPO_ID=my-repository bash scripts/validate-repo.sh
```

In GitHub Actions, `GITHUB_REPOSITORY` takes precedence over the local override.
Validation fails closed if none of those identity sources is available.
The validator checks the expected repository identity, exact manifest shape,
cross-file identity and effective ownership fields, regular required files,
the canonical baseline workflow, regression tests, and configured secret-like
patterns.

Do not call the repository structurally seeded until the command passes in the
customized repository and the same commit passes its GitHub validation workflow.
