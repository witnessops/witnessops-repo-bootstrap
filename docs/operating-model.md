# Operating Model

This template establishes a bounded repository seed. It does not create runtime,
evidence, proof, receipt, verification-outcome, or production authority.

## Seed a repository

1. Create the repository from this bootstrap, either with
   `bash scripts/seed-new-repo.sh` or by copying the seeded inventory manually.
2. Complete `docs/customization-checklist.md` before feature work.
3. Run `bash scripts/validate-repo.sh` from the new repository root.
4. Open a pull request that states its change class and authority impact.
5. Confirm the named validation check passes on the exact commit.
6. Apply and verify `docs/repository-settings.md` after the check exists.
7. Call the repository `seeded` only after the source and settings gates pass.

## Change the standard

1. Make one reviewable change to this bootstrap.
2. Record durable authority, security, or workflow decisions under
   `docs/decisions/`.
3. Update the changelog and any copied guidance affected by the change.
4. Run the local gate and open a draft pull request for owner review.
5. Merge only after the governance requirements and required check pass.
6. Propagate an approved release deliberately; do not silently overwrite
   repository-specific authority, ownership, or security policy.
