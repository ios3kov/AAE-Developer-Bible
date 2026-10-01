#!/usr/bin/env python3
"""Check SDK call-site symbol names only. Real compilation validates types/suites."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

SCHEMA_VERSION = 1
CALL_RE = re.compile(r"(?:->|\.)\s*(?P<name>(?:AEGP|PF|AEIO|PR|DRAWBOT)_[A-Za-z0-9_]+)\s*\(")
COMMENT_OR_STRING = re.compile(
    r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'',
    re.S,
)


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
            files.update(
                p.resolve()
                for p in path.rglob("*")
                if p.is_file() and p.suffix in (".cpp", ".h", ".hpp", ".cc", ".c")
            )
    if not files:
        raise ValueError("No source files found")
    return sorted(files)


def validate_inventory(data):
    if not isinstance(data, dict):
        raise ValueError("Inventory root must be an object")
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(
            f"Unsupported inventory schema_version: {data.get('schema_version')!r}"
        )
    if data.get("unparsed_candidate_tables") or data.get("partial_candidate_tables"):
        raise ValueError("Inventory has parser diagnostics; resolve them before verification")

    tables = data.get("tables")
    if not isinstance(tables, list) or not tables:
        raise ValueError("Inventory contains no contract tables")

    seen = {}
    for table in tables:
        if not isinstance(table, dict) or not isinstance(table.get("name"), str):
            raise ValueError("Inventory contains malformed table entry")
        functions = table.get("functions")
        if not isinstance(functions, list) or not functions:
            raise ValueError(f"Inventory table {table['name']} contains no functions")

        normalized = []
        for function in functions:
            if (
                not isinstance(function, dict)
                or not isinstance(function.get("name"), str)
                or not function["name"]
                or not isinstance(function.get("signature"), str)
                or not function["signature"]
            ):
                raise ValueError(f"Inventory table {table['name']} has malformed function entry")
            normalized.append((function["name"], function["signature"]))

        previous = seen.get(table["name"])
        if previous is not None and previous != normalized:
            raise ValueError(f"Conflicting declarations for {table['name']}")
        seen[table["name"]] = normalized

    return tables


def verify(data, files):
    tables = validate_inventory(data)
    known = {f["name"] for table in tables for f in table["functions"]}

    unknown = []
    checked = 0
    for path in files:
        text = path.read_text("utf-8")
        text = COMMENT_OR_STRING.sub(lambda m: "\n" * m[0].count("\n") + " ", text)
        for match in CALL_RE.finditer(text):
            checked += 1
            if match["name"] not in known:
                unknown.append(
                    (
                        str(path),
                        text.count("\n", 0, match.start()) + 1,
                        match["name"],
                    )
                )

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
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(f"call_sites={checked} unknown={len(unknown)} (symbol names only)")
    for path, line, name in unknown:
        print(f"UNKNOWN {path}:{line}: {name}")
    return 1 if unknown else 0


if __name__ == "__main__":
    raise SystemExit(main())
