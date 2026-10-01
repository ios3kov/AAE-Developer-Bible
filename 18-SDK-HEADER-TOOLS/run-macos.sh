#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: $0 /path/to/AfterEffectsSDK/Examples" >&2
  exit 2
fi

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
SDK_EXAMPLES="$(cd "$1" && pwd)"
SDK_HEADERS="$SDK_EXAMPLES/Headers"
OUT="$HERE/generated/local-sdk"

if [[ ! -f "$SDK_HEADERS/AE_Effect.h" ]]; then
  echo "Expected SDK Examples/Headers/AE_Effect.h" >&2
  exit 2
fi

mkdir -p "$OUT"

python3 "$HERE/tools/ae_sdk_inventory.py" "$SDK_HEADERS" \
  --json "$OUT/ae-sdk-inventory.json" \
  --markdown "$OUT/ae-sdk-inventory.md"

python3 "$HERE/tools/verify_required_contracts.py" \
  "$OUT/ae-sdk-inventory.json" \
  "$HERE/sdk25.6-required-contracts.json"

python3 "$HERE/tools/verify_recipe_symbols.py" \
  "$OUT/ae-sdk-inventory.json" \
  "$HERE/../17-NATIVE-SUITE-COOKBOOK/code"

python3 "$ROOT/scripts/check_native.py" "$SDK_EXAMPLES" \
  --compiler "${CXX:-clang++}" \
  --compiler-style clang \
  --report "$OUT/native-compile-report.json" \
  --require-clean

echo "Gate-4 local SDK lane: inventory + symbol-name + compiler syntax/type checks PASS"
echo "No link, PiPL load, AE host execution or runtime semantics were tested."
