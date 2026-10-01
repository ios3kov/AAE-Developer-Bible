#!/usr/bin/env python3
"""Compile Bible native translation units against a local Adobe SDK.

This is a compiler/type check only. It does not link a plug-in or run After Effects.
The machine-readable report records SDK header identity, compiler identity, commands
and per-translation-unit results so a syntax PASS cannot be detached from its inputs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]


def compiler_style(compiler: str, requested: str) -> str:
    if requested != "auto":
        return requested
    name = Path(compiler).name.lower()
    return "msvc" if name in {"cl", "cl.exe"} else "clang"


def collect_sources(root: Path = ROOT) -> list[Path]:
    sources: list[Path] = []
    for directory in (
        "16-WORKING-TEMPLATES",
        "17-NATIVE-SUITE-COOKBOOK/code",
        "20-REFERENCE-IMPLEMENTATIONS",
    ):
        base = root / directory
        if base.exists():
            sources.extend(sorted(base.rglob("*.cpp")))
    if not sources:
        raise ValueError("No native C++ sources found")
    return sorted(set(p.resolve() for p in sources))


def sdk_include_roots(examples: Path) -> list[Path]:
    return [
        examples / "Headers",
        examples / "Headers" / "SP",
        examples / "Util",
    ]


def project_include_roots(root: Path = ROOT) -> list[Path]:
    return [
        root / "19-NATIVE-CODE-FOUNDATION" / "code",
        root / "17-NATIVE-SUITE-COOKBOOK" / "code",
    ]


def sdk_header_manifest(examples: Path) -> tuple[int, str]:
    files: list[Path] = []
    for base in (examples / "Headers", examples / "Util"):
        if not base.exists():
            continue
        files.extend(
            p for p in base.rglob("*")
            if p.is_file() and p.suffix.lower() in {".h", ".hpp", ".hh"}
        )
    files = sorted(set(p.resolve() for p in files))
    if not files:
        raise ValueError("No SDK headers found for identity manifest")

    aggregate = hashlib.sha256()
    for path in files:
        rel = path.relative_to(examples).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        aggregate.update(rel.encode("utf-8"))
        aggregate.update(b"\0")
        aggregate.update(digest.encode("ascii"))
        aggregate.update(b"\n")
    return len(files), aggregate.hexdigest()


def build_compile_command(
    style: str,
    compiler: str,
    sdk_includes: Iterable[Path],
    project_includes: Iterable[Path],
    source: Path,
) -> list[str]:
    if style == "clang":
        command = [
            compiler,
            "-std=c++17",
            "-fsyntax-only",
            "-Wall",
            "-Wextra",
            "-Werror",
            "-Wno-unused-parameter",
            "-Wno-deprecated-declarations",
        ]
        for include in sdk_includes:
            command += ["-isystem", str(include)]
        for include in project_includes:
            command += ["-I", str(include)]
        return command + [str(source)]

    if style == "msvc":
        command = [
            compiler,
            "/nologo",
            "/std:c++17",
            "/Zs",
            "/W4",
            "/WX",
            "/EHsc",
            "/permissive-",
            "/wd4100",  # unused parameter: callback signatures are host-defined
            "/wd4996",  # SDK/toolchain deprecation warnings are tracked separately
            "/external:W0",
        ]
        for include in sdk_includes:
            command.append("/external:I" + str(include))
        for include in project_includes:
            command.append("/I" + str(include))
        return command + [str(source)]

    raise ValueError(f"Unsupported compiler style: {style}")


def compiler_identity(compiler: str, style: str) -> str:
    command = [compiler] if style == "msvc" else [compiler, "--version"]
    try:
        result = subprocess.run(
            command,
            text=True,
            capture_output=True,
            timeout=15,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError(f"Unable to execute compiler {compiler!r}: {exc}") from exc

    text = (result.stdout + "\n" + result.stderr).strip()
    if not text:
        raise RuntimeError(f"Compiler {compiler!r} returned no identity text")
    return "\n".join(text.splitlines()[:8])


def _relative_source(path: Path, root: Path = ROOT) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def git_identity(root: Path) -> dict:
    try:
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            text=True,
            capture_output=True,
            timeout=10,
            check=False,
        )
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=root,
            text=True,
            capture_output=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return {"git_sha": None, "dirty": None}

    if head.returncode != 0:
        return {"git_sha": None, "dirty": None}

    return {
        "git_sha": head.stdout.strip() or None,
        "dirty": bool(status.stdout.strip()) if status.returncode == 0 else None,
    }


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_identity_error(source: dict) -> str | None:
    if not source.get("git_sha"):
        return "source Git SHA is unavailable"
    if source.get("dirty") is not False:
        return "source working tree is dirty or its state is unknown"
    return None


def run_checks(
    examples: Path,
    compiler: str,
    style: str,
    *,
    root: Path = ROOT,
) -> tuple[dict, int]:
    examples = examples.resolve()
    required = examples / "Headers" / "AE_Effect.h"
    if not required.is_file():
        raise ValueError("Expected SDK Examples/Headers/AE_Effect.h")

    sdk_includes = sdk_include_roots(examples)
    for include in sdk_includes:
        if not include.exists():
            raise ValueError(f"Missing SDK include root: {include}")

    project_includes = project_include_roots(root)
    for include in project_includes:
        if not include.exists():
            raise ValueError(f"Missing Bible include root: {include}")

    sources = collect_sources(root)
    header_count, header_manifest_sha256 = sdk_header_manifest(examples)
    identity = compiler_identity(compiler, style)

    report = {
        "schema_version": 1,
        "kind": "native-syntax-type-check",
        "verification_boundary": "compiler only; no link, PiPL load, host execution or runtime semantics",
        "sdk": {
            "examples_root": str(examples),
            "header_count": header_count,
            "header_manifest_sha256": header_manifest_sha256,
        },
        "source": {
            "root": str(root.resolve()),
            **git_identity(root),
        },
        "compiler": {
            "path": shutil.which(compiler) or compiler,
            "style": style,
            "identity": identity,
        },
        "results": [],
    }

    failures = 0
    with tempfile.TemporaryDirectory() as tmp:
        foundation = Path(tmp) / "foundation.cpp"
        foundation.write_text(
            '#include "AEConfig.h"\n'
            '#include "PicaSuiteRef.h"\n'
            '#include "AegpOwners.h"\n'
            '#include "UndoScope.h"\n'
            '#include "HostCallbackGuard.h"\n'
            '#include "BibleAegpCommon.h"\n',
            encoding="utf-8",
        )

        for source in sources + [foundation]:
            command = build_compile_command(
                style,
                compiler,
                sdk_includes,
                project_includes,
                source,
            )
            label = (
                "<generated>/foundation.cpp"
                if source == foundation
                else _relative_source(source, root)
            )
            print(f"CHECK {label}", flush=True)

            try:
                result = subprocess.run(
                    command,
                    cwd=root,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                returncode = result.returncode
                stdout = result.stdout[-8000:]
                stderr = result.stderr[-8000:]
            except OSError as exc:
                returncode = 127
                stdout = ""
                stderr = str(exc)

            if returncode != 0:
                failures += 1

            report["results"].append(
                {
                    "source": label,
                    "source_sha256": file_sha256(source),
                    "command": command,
                    "returncode": returncode,
                    "status": "PASS" if returncode == 0 else "FAIL",
                    "stdout_tail": stdout,
                    "stderr_tail": stderr,
                }
            )

    report["summary"] = {
        "translation_units": len(report["results"]),
        "failed": failures,
        "status": "PASS" if failures == 0 else "FAIL",
    }
    return report, failures


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("examples", type=Path, help="Adobe SDK Examples directory")
    parser.add_argument("--compiler", default=os.environ.get("CXX", "clang++"))
    parser.add_argument(
        "--compiler-style",
        choices=("auto", "clang", "msvc"),
        default="auto",
    )
    parser.add_argument("--report", type=Path)
    parser.add_argument(
        "--require-clean",
        action="store_true",
        help="Fail evidence acceptance unless the Bible source tree is a known clean Git commit",
    )
    args = parser.parse_args(argv)

    style = compiler_style(args.compiler, args.compiler_style)

    try:
        report, failures = run_checks(args.examples, args.compiler, style)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"error: {exc}")
        return 2

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"report={args.report}")

    if args.require_clean:
        identity_error = source_identity_error(report["source"])
        if identity_error:
            print(f"error: {identity_error}")
            return 2

    summary = report["summary"]
    print(
        "SDK syntax checks: "
        f"{summary['translation_units']}, failed: {summary['failed']}; "
        "host tests not run"
    )
    print(
        "SDK header identity: "
        f"{report['sdk']['header_count']} headers, "
        f"manifest={report['sdk']['header_manifest_sha256']}"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
