#!/usr/bin/env bash
set -euo pipefail
if [[ $# -lt 1 ]]; then
  echo "usage: $0 /path/to/AE-SDK-Headers" >&2
  exit 2
fi
HERE="$(cd "$(dirname "$0")" && pwd)"
SDK_HEADERS="$1"
OUT="$HERE/generated/local-sdk"
mkdir -p "$OUT"
python3 "$HERE/tools/ae_sdk_inventory.py" "$SDK_HEADERS" \
  --json "$OUT/ae-sdk-inventory.json" \
  --markdown "$OUT/ae-sdk-inventory.md"
python3 "$HERE/tools/verify_recipe_symbols.py" \
  "$OUT/ae-sdk-inventory.json" \
  "$HERE/../17-NATIVE-SUITE-COOKBOOK/code"
echo "native SDK validation: PASS"
