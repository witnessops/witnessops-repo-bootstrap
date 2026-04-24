# Security

## Reporting

Report security concerns through the repository owner until a dedicated security intake is published.

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

Runtime secrets belong in the runtime authority for the relevant system, such as GitHub Actions secrets or Azure Key Vault.

They do not belong in this repository.

## Validation limitation

The bootstrap validation script is a basic guardrail. It is not a complete security scanner and is not proof that a repository is secure.
