#!/bin/bash

echo "Exporting proof bundle..."
creativectl export-proof

ROOT=$(jq -r '.merkle_root' ~/.creativectl/proof_bundle.json)

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
FILE="roots/${TIMESTAMP}.txt"

echo "Saving Merkle root to $FILE"
echo "$ROOT" > "$FILE"

git add "$FILE"
git commit -m "Anchor Merkle root $TIMESTAMP"
git push

echo "Anchor complete."
