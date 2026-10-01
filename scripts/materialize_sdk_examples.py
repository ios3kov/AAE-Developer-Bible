#!/usr/bin/env python3
"""Materialize licensed Adobe sample shells outside the repository, fail-closed."""

from __future__ import annotations

import argparse
import shutil
import tempfile
from pathlib import Path

SAMPLES = {
    "aeio-import-export": ("AEGP/IO", "io"),
    "artisan-renderer": ("AEGP/Artie", "artie"),
    "native-panel": ("AEGP/Panelator", "panelator"),
    "gpu-effect": ("Effect/SDK_Invert_ProcAmp", "sdk_invert_procamp"),
    "pica-provider": ("AEGP/Sweetie", "sweetie"),
    "effect-aegp": ("AEGP/Commando", "commando"),
}


def _overlap(a: Path, b: Path) -> bool:
    a = a.resolve()
    b = b.resolve()
    return a == b or a in b.parents or b in a.parents


def _validate_sample(source: Path, expected_stem: str) -> None:
    if not source.is_dir():
        raise ValueError(f"Missing SDK sample directory: {source}")

    native_sources = [
        p
        for p in source.rglob("*")
        if p.is_file() and p.suffix.lower() in {".c", ".cc", ".cpp", ".cxx", ".m", ".mm"}
    ]
    if not native_sources:
        raise ValueError(f"SDK sample has no native source files: {source}")

    wanted = expected_stem.lower()
    if not any(wanted in p.stem.lower() for p in native_sources):
        raise ValueError(
            f"SDK sample looks incomplete or unexpected: no source matching "
            f"{expected_stem!r} under {source}"
        )


def _replace_tree_transactionally(source: Path, target: Path) -> None:
    if _overlap(source, target):
        raise ValueError(f"source and destination paths overlap: {source} -> {target}")

    target.parent.mkdir(parents=True, exist_ok=True)

    staging_root = Path(
        tempfile.mkdtemp(prefix=".aae-bible-stage-", dir=str(target.parent))
    )
    staging = staging_root / target.name

    backup_root: Path | None = None
    backup: Path | None = None

    if target.exists():
        backup_root = Path(
            tempfile.mkdtemp(prefix=".aae-bible-backup-", dir=str(target.parent))
        )
        backup = backup_root / target.name
        target.rename(backup)

    try:
        shutil.copytree(source, staging)
        staging.rename(target)
    except Exception:
        if staging_root.exists():
            shutil.rmtree(staging_root)
        if backup and backup.exists():
            backup.rename(target)
        if backup_root and backup_root.exists():
            shutil.rmtree(backup_root)
        raise

    if staging_root.exists():
        shutil.rmtree(staging_root)
    if backup_root and backup_root.exists():
        shutil.rmtree(backup_root)


def materialize(examples: Path, out: Path, names: list[str] | None = None) -> list[Path]:
    examples = examples.resolve()
    out = out.resolve()

    if not (examples / "Headers/AE_GeneralPlug.h").is_file():
        raise ValueError("Expected SDK Examples directory with Headers/AE_GeneralPlug.h")

    selected = names or list(SAMPLES)
    plan: list[tuple[str, Path, Path]] = []

    # Validate the complete plan before mutating any destination.
    for name in selected:
        rel, expected_stem = SAMPLES[name]
        source = (examples / rel).resolve()
        target = (out / name).resolve()

        _validate_sample(source, expected_stem)

        if _overlap(source, target):
            raise ValueError(f"source and destination paths overlap: {source} -> {target}")

        plan.append((name, source, target))

    written: list[Path] = []
    for name, source, target in plan:
        _replace_tree_transactionally(source, target)
        (target / "AAE-BIBLE-BASE.txt").write_text(
            f"Licensed SDK sample: {SAMPLES[name][0]}\n"
        )
        written.append(target)

    return written


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("examples", type=Path)
    ap.add_argument("--out", type=Path, default=Path(".build/sdk-examples"))
    ap.add_argument("--only", choices=sorted(SAMPLES), action="append")
    args = ap.parse_args(argv)

    try:
        written = materialize(args.examples, args.out, args.only)
    except ValueError as exc:
        ap.error(str(exc))

    for target in written:
        print(f"{target.name}: {target}")
    print("SDK sources remain outside git and are not redistributed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
