#!/usr/bin/env python3
"""Safely install a built macOS plug-in bundle and optionally run aerender."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class HostCycleError(RuntimeError):
    def __init__(self, message: str, report: dict[str, Any]):
        super().__init__(message)
        self.report = report


def _remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)


@dataclass
class InstallTransaction:
    installed: Path
    staging_root: Path
    backup_root: Path | None
    backup: Path | None

    def commit(self) -> None:
        _remove_path(self.staging_root)
        if self.backup_root:
            _remove_path(self.backup_root)

    def rollback(self) -> None:
        _remove_path(self.installed)
        if self.backup and self.backup.exists():
            self.backup.rename(self.installed)
        _remove_path(self.staging_root)
        if self.backup_root:
            _remove_path(self.backup_root)


def _install_transaction(plugin: Path, install_root: Path) -> InstallTransaction:
    source = plugin.resolve()
    install_root = install_root.resolve()
    installed = install_root / plugin.name

    if source == installed:
        raise ValueError("source plug-in and destination plug-in are the same path")

    install_root.mkdir(parents=True, exist_ok=True)

    staging_root = Path(
        tempfile.mkdtemp(prefix=".aae-bible-stage-", dir=str(install_root))
    )
    staging = staging_root / plugin.name

    backup_root: Path | None = None
    backup: Path | None = None

    if installed.exists():
        backup_root = Path(
            tempfile.mkdtemp(prefix=".aae-bible-backup-", dir=str(install_root))
        )
        backup = backup_root / plugin.name
        installed.rename(backup)

    try:
        shutil.copytree(source, staging)
        staging.rename(installed)
    except Exception:
        _remove_path(staging_root)
        if backup and backup.exists():
            backup.rename(installed)
        if backup_root:
            _remove_path(backup_root)
        raise

    return InstallTransaction(
        installed=installed,
        staging_root=staging_root,
        backup_root=backup_root,
        backup=backup,
    )


def _report_path(output: Path, explicit: Path | None) -> Path:
    if explicit:
        return explicit
    return output.with_suffix(output.suffix + ".host-cycle.json")


def write_report(report: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")


def run_cycle(
    plugin: Path,
    install_root: Path,
    output: Path,
    *,
    aerender: Path | None = None,
    project: Path | None = None,
    expected_output: Path | None = None,
    timeout_seconds: float = 300.0,
) -> dict[str, Any]:
    plugin = plugin.resolve()
    install_root = install_root.resolve()
    output = output.resolve()
    project = project.resolve() if project else None
    aerender = aerender.resolve() if aerender else None
    expected_output = (expected_output or output).resolve()

    report: dict[str, Any] = {
        "schema": 1,
        "build": {"status": "external", "artifact": str(plugin)},
        "install": {
            "status": "not_started",
            "source": str(plugin),
            "destination": str(install_root / plugin.name),
            "had_previous_install": False,
            "rolled_back": False,
        },
        "load": {
            "status": "not_proven",
            "note": "aerender execution does not by itself prove UI load/unload lifecycle",
        },
        "render": {"status": "not_run"},
        "stress_mfr": {"status": "not_run"},
    }

    if not plugin.is_dir() or plugin.suffix != ".plugin":
        raise HostCycleError("plugin must be an existing .plugin bundle", report)

    destination = (install_root / plugin.name).resolve()
    if plugin == destination:
        raise HostCycleError(
            "source plug-in and destination plug-in are the same path", report
        )

    if project and not project.is_file():
        raise HostCycleError("project does not exist", report)

    if project and (not aerender or not aerender.is_file()):
        raise HostCycleError("aerender must exist when --project is used", report)

    if timeout_seconds <= 0:
        raise HostCycleError("timeout must be greater than zero", report)

    report["install"]["had_previous_install"] = destination.exists()

    try:
        tx = _install_transaction(plugin, install_root)
    except Exception as exc:
        report["install"]["status"] = "failed"
        raise HostCycleError(f"install failed: {exc}", report) from exc

    report["install"]["status"] = "installed"

    try:
        if project:
            output.parent.mkdir(parents=True, exist_ok=True)
            expected_output.parent.mkdir(parents=True, exist_ok=True)

            command = [
                str(aerender),
                "-project",
                str(project),
                "-output",
                str(output),
            ]
            report["render"] = {
                "status": "running",
                "command": command,
                "timeout_seconds": timeout_seconds,
                "expected_output": str(expected_output),
            }

            try:
                result = subprocess.run(
                    command,
                    text=True,
                    capture_output=True,
                    timeout=timeout_seconds,
                    check=False,
                )
            except subprocess.TimeoutExpired as exc:
                report["render"].update(
                    {
                        "status": "timeout",
                        "stdout": (exc.stdout or "")[-4000:]
                        if isinstance(exc.stdout, str)
                        else "",
                        "stderr": (exc.stderr or "")[-4000:]
                        if isinstance(exc.stderr, str)
                        else "",
                    }
                )
                raise HostCycleError("aerender timed out", report) from exc

            report["render"].update(
                {
                    "returncode": result.returncode,
                    "stdout": result.stdout[-4000:],
                    "stderr": result.stderr[-4000:],
                    "output_exists": expected_output.exists(),
                }
            )

            if result.returncode != 0:
                report["render"]["status"] = "failed"
                raise HostCycleError(
                    f"aerender failed with exit code {result.returncode}", report
                )

            if not expected_output.exists():
                report["render"]["status"] = "missing_output"
                raise HostCycleError(
                    f"expected render output was not created: {expected_output}",
                    report,
                )

            report["render"]["status"] = "passed"

        tx.commit()
        report["install"]["status"] = "committed"
        return report

    except Exception:
        tx.rollback()
        report["install"]["status"] = "rolled_back"
        report["install"]["rolled_back"] = True
        raise


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("plugin", type=Path)
    ap.add_argument("--aerender", type=Path)
    ap.add_argument("--project", type=Path)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--expect-output", type=Path)
    ap.add_argument("--install-root", type=Path, required=True)
    ap.add_argument("--timeout", type=float, default=300.0)
    ap.add_argument("--report", type=Path)
    args = ap.parse_args(argv)

    report_path = _report_path(args.output, args.report)

    try:
        report = run_cycle(
            args.plugin,
            args.install_root,
            args.output,
            aerender=args.aerender,
            project=args.project,
            expected_output=args.expect_output,
            timeout_seconds=args.timeout,
        )
    except HostCycleError as exc:
        write_report(exc.report, report_path)
        print(f"host cycle failed: {exc}", file=sys.stderr)
        print(report_path)
        return 1

    write_report(report, report_path)
    print(report_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
