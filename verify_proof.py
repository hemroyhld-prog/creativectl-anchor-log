import json
import hashlib
import sys


def hash_data(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def build_merkle_root(hashes):
    if not hashes:
        return None

    level = hashes[:]

    while len(level) > 1:
        next_level = []

        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i + 1] if i + 1 < len(level) else left
            combined = hash_data(left + right)
            next_level.append(combined)

        level = next_level

    return level[0]


def verify_bundle(path):
    with open(path, "r") as f:
        bundle = json.load(f)

    audit_records = bundle["audit_records"]
    expected_root = bundle["merkle_root"]

    hashes = [record["hash"] for record in audit_records]
    calculated_root = build_merkle_root(hashes)

    print("Expected Root:  ", expected_root)
    print("Calculated Root:", calculated_root)

    if calculated_root == expected_root:
        print("\n✅ Merkle root VALID")
    else:
        print("\n❌ Merkle root INVALID")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python verify_proof.py proof_bundle.json")
        sys.exit(1)

    verify_bundle(sys.argv[1])
