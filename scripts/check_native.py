#!/usr/bin/env python3
"""Compile translation units against local Adobe SDK headers; no link/host test."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("examples", type=Path, help="Adobe SDK Examples directory")
    parser.add_argument("--compiler", default=os.environ.get("CXX", "clang++"))
    args = parser.parse_args()
    sdk = args.examples.resolve()
    if not (sdk / "Headers/AE_Effect.h").is_file():
        parser.error("Expected SDK Examples/Headers/AE_Effect.h")
    includes = [sdk / "Headers", sdk / "Headers/SP", sdk / "Util",
                ROOT / "19-NATIVE-CODE-FOUNDATION/code",
                ROOT / "17-NATIVE-SUITE-COOKBOOK/code"]
    sources = []
    for directory in ("16-WORKING-TEMPLATES", "17-NATIVE-SUITE-COOKBOOK/code",
                      "20-REFERENCE-IMPLEMENTATIONS"):
        sources.extend(sorted((ROOT / directory).rglob("*.cpp")))
    with tempfile.TemporaryDirectory() as tmp:
        foundation = Path(tmp) / "foundation.cpp"
        foundation.write_text('''#include "AEConfig.h"
#include "PicaSuiteRef.h"
#include "AegpOwners.h"
#include "UndoScope.h"
#include "HostCallbackGuard.h"
#include "BibleAegpCommon.h"
''')
        failures = 0
        for source in sources + [foundation]:
            print(f"CHECK {source.name}", flush=True)
            command = [args.compiler, "-std=c++17", "-fsyntax-only", "-Wall", "-Wextra",
                       "-Werror", "-Wno-unused-parameter", "-Wno-deprecated-declarations"]
            for include in includes:
                command += ["-isystem", str(include)]
            command += [str(source)]
            result = subprocess.run(command, cwd=ROOT)
            failures += result.returncode != 0
    print(f"SDK syntax checks: {len(sources) + 1}, failed: {failures}; host tests not run")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
