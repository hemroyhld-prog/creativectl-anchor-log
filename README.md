# CreativeCTL Anchor Log

This repository provides public cryptographic anchoring for CreativeCTL audit records.

## Purpose

To ensure:
- External verifiability
- Tamper evidence
- Timestamped Merkle root anchoring
- Public transparency

Each file inside `/roots/` represents a Merkle root exported from CreativeCTL at a specific timestamp.

## Verification Model

1. Export proof bundle from CreativeCTL:
   creativectl export-proof

2. Verify Merkle root locally.

3. Compare exported root with corresponding file inside `/roots/`.

4. Validate commit timestamp via Git history:
   git log

## Trust Model

- Cryptographic signatures are included inside proof bundles.
- Merkle root guarantees audit chain integrity.
- GitHub commit history provides independent timestamp anchoring.

This repository contains no private data.
Only hash roots are published.

Maintained by: Hemanta Roy
