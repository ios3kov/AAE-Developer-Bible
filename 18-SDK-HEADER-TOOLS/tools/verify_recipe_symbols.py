#!/usr/bin/env python3
"""Check symbol names only. Compile with the SDK to validate types and suites."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys

CALL_RE = re.compile(r"(?:->|\.)\s*(?P<name>(?:AEGP|PF|AEIO|PR|DRAWBOT)_[A-Za-z0-9_]+)\s*\(")
COMMENT_OR_STRING = re.compile(r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', re.S)


def source_files(paths):
    files = set()
    for raw in paths:
        path = Path(raw)
        if not path.exists():
            raise ValueError(f"Source path does not exist: {path}")
        if path.is_file():
            if path.suffix not in (".cpp", ".h", ".hpp", ".cc", ".c"):
                raise ValueError(f"Unsupported source file: {path}")
            files.add(path.resolve())
        else:
            files.update(p.resolve() for p in path.rglob("*")
                         if p.is_file() and p.suffix in (".cpp", ".h", ".hpp", ".cc", ".c"))
    if not files:
        raise ValueError("No source files found")
    return sorted(files)


def verify(data, files):
    if data.get("unparsed_candidate_tables") or data.get("partial_candidate_tables"):
        raise ValueError("Inventory has parser diagnostics; resolve them before verification")
    known = {f["name"] for t in data["tables"] for f in t["functions"]}
    if not known:
        raise ValueError("Inventory contains no function names")
    unknown = []
    checked = 0
    for path in files:
        text = path.read_text("utf-8")
        text = COMMENT_OR_STRING.sub(lambda m: "\n" * m[0].count("\n") + " ", text)
        for match in CALL_RE.finditer(text):
            checked += 1
            if match["name"] not in known:
                unknown.append((str(path), text.count("\n", 0, match.start()) + 1, match["name"]))
    if not checked:
        raise ValueError("No supported call sites found; nothing was verified")
    return checked, unknown


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inventory_json")
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args(argv)
    try:
        data = json.loads(Path(args.inventory_json).read_text("utf-8"))
        checked, unknown = verify(data, source_files(args.paths))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"call_sites={checked} unknown={len(unknown)} (symbol names only)")
    for path, line, name in unknown:
        print(f"UNKNOWN {path}:{line}: {name}")
    return 1 if unknown else 0


if __name__ == "__main__":
    raise SystemExit(main())
