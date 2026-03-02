# Security Policy

## Supported Versions

Version 1.0.0 is currently supported.

## Reporting a Vulnerability

If you discover a security vulnerability in the CreativeCTL Anchor Protocol:

- Do NOT open a public issue.
- Report privately via email to the maintainer.
- Include reproduction steps and impact analysis.

## Security Model

- Cryptographic integrity relies on SHA-256.
- Merkle root construction is deterministic.
- Git commit history provides public timestamp anchoring.
- Only hash roots are publicly published.
- No private audit data is exposed.

## Threat Model

This system protects against:

- Record tampering
- Retroactive audit modification
- Undetected historical changes

This system does NOT protect against:

- Compromised signing keys
- Compromised GitHub accounts
- SHA-256 cryptographic break (currently infeasible)
