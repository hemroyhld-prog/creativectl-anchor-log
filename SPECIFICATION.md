# CreativeCTL Public Anchor Specification
Version: 1.0.0

## 1. Purpose

This specification defines the public anchoring protocol used by CreativeCTL
to provide external cryptographic verifiability of audit records.

The protocol guarantees:

- Tamper-evidence of audit history
- Deterministic Merkle root construction
- Public timestamp anchoring via Git commit history
- Independent third-party verification

---

## 2. Audit Record Model

Each audit record contains:

- previous_hash
- content
- hash
- signature

Records form a hash-linked chain.

---

## 3. Merkle Construction Rules

Merkle root is built using:

- SHA-256 hashing
- Pairwise concatenation (left + right)
- Duplicate last hash if odd number of leaves
- Deterministic ordering (record order preserved)

Root = build_merkle_root(hashes)

---

## 4. Proof Bundle Structure

Proof bundle contains:

- audit_records[]
- merkle_root
- merkle_signature
- public_key

---

## 5. Public Anchor Model

Each Merkle root is exported and saved as:

roots/YYYY-MM-DD_HH-MM-SS.txt

Git commit timestamp 
serves as independent public anchor.

---

## 6. Verification Procedure

Independent verifier must:

1. Rebuild Merkle root from audit records
2. Compare with bundle merkle_root
3. Compare with published root in repository
4. Confirm commit timestamp

---

## 7. Trust Model

- No private data is published
- Only hash roots are publicly stored
- Cryptographic integrity relies on SHA-256
- Public Git history provides external timestamp integrity

---

End of Specification.
