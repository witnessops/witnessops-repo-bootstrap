# Security

## Reporting

Use GitHub private vulnerability reporting when it is enabled. Otherwise,
contact the repository owner through a verified profile channel before sharing
sensitive details. Never put a vulnerability secret, credential, customer data,
or private evidence in a public issue.

Initial owner: `VaultSovereign`

## Security boundary

This repository is a template repository. It should not contain:

- Production secrets.
- Customer data.
- Customer evidence.
- Private keys.
- Cloud credentials.
- Access tokens.
- Runtime configuration with live credentials.

## Secret handling

This bootstrap defaults `allowed_secret_storage` to an empty list. Its required
validation workflow stores and reads no secrets. A seeded repository may name an
external secret store only after its actual runtime authority and credential
boundary are documented and approved for that repository.

The template permits only its canonical validation workflow. A downstream
repository that adds another workflow must separately review and document that
workflow's permissions, credentials, triggers, execution environment, and
authority.

Allowed references:

- Documentation that names approved secret stores.
- Placeholder examples that are clearly non-secret.
- Validation logic that detects secret-like strings.

Forbidden material:

- Real API keys.
- Real private keys.
- Real OAuth tokens.
- Real Azure credentials.
- Real GitHub tokens.
- Real customer data.

## Runtime secrets

Runtime secrets belong in the explicitly designated runtime authority and
external secret store for the relevant system.

They do not belong in this repository.

## Validation limitation

The bootstrap validation script is a basic guardrail. It is not a complete security scanner and is not proof that a repository is secure.
