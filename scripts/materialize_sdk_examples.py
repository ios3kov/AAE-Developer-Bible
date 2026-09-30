#!/usr/bin/env python3
"""Materialize licensed Adobe sample shells outside the repository."""
from pathlib import Path
import argparse
import shutil

SAMPLES = {
    "aeio-import-export": "AEGP/IO", "artisan-renderer": "AEGP/Artie",
    "native-panel": "AEGP/Panelator", "gpu-effect": "Effect/SDK_Invert_ProcAmp",
    "pica-provider": "AEGP/Sweetie", "effect-aegp": "AEGP/Commando",
}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("examples", type=Path)
    ap.add_argument("--out", type=Path, default=Path(".build/sdk-examples"))
    ap.add_argument("--only", choices=sorted(SAMPLES), action="append")
    args = ap.parse_args(); examples = args.examples.resolve()
    if not (examples / "Headers/AE_GeneralPlug.h").exists(): ap.error("Expected SDK Examples directory")
    args.out.mkdir(parents=True, exist_ok=True)
    for name in args.only or list(SAMPLES):
        source = examples / SAMPLES[name]; target = args.out / name
        if not source.exists(): ap.error(f"Missing SDK sample: {source}")
        if target.exists(): shutil.rmtree(target)
        shutil.copytree(source, target)
        (target / "AAE-BIBLE-BASE.txt").write_text(f"Licensed SDK sample: {SAMPLES[name]}\n")
        print(f"{name}: {target}")
    print("SDK sources remain outside git and are not redistributed.")

if __name__ == "__main__": main()
