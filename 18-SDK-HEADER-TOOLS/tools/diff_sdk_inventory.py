#!/usr/bin/env python3
"""Compare indexed declarations/field order; this is not a complete ABI diff."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SCHEMA_VERSION = 1


def load(path):
    data = json.loads(Path(path).read_text("utf-8"))

    if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(
            f"Unsupported inventory schema_version in {path}: "
            f"{data.get('schema_version') if isinstance(data, dict) else None!r}"
        )
    if data.get("unparsed_candidate_tables") or data.get("partial_candidate_tables"):
        raise ValueError(f"Incomplete inventory: {path}")

    raw_tables = data.get("tables")
    if not isinstance(raw_tables, list) or not raw_tables:
        raise ValueError("No tables to compare")

    tables = {}
    for table in raw_tables:
        if not isinstance(table, dict) or not isinstance(table.get("name"), str):
            raise ValueError(f"Malformed table in {path}")
        functions = table.get("functions")
        if not isinstance(functions, list) or not functions:
            raise ValueError(f"Malformed/empty function table {table['name']} in {path}")

        for function in functions:
            if (
                not isinstance(function, dict)
                or not isinstance(function.get("name"), str)
                or not function["name"]
                or not isinstance(function.get("signature"), str)
                or not function["signature"]
            ):
                raise ValueError(
                    f"Malformed function declaration in {table['name']} from {path}"
                )

        name = table["name"]
        if name in tables and tables[name] != functions:
            raise ValueError(f"Conflicting declarations for {name}")
        tables[name] = functions

    return tables


def compare(old, new):
    lines = [
        "# SDK declaration diff",
        "",
        "> Textual declarations and function-field order only; not a complete ABI compatibility test.",
        "",
        "## Contract tables",
        "",
    ]

    changes = False
    for label, names in (
        ("Added", new.keys() - old.keys()),
        ("Removed", old.keys() - new.keys()),
    ):
        if names:
            changes = True
        lines.append(f"- {label}: " + (", ".join(f"`{n}`" for n in sorted(names)) or "none"))

    for name in sorted(old.keys() & new.keys()):
        a, b = old[name], new[name]
        if a == b:
            continue

        changes = True
        lines += ["", f"## `{name}`", ""]

        a_order = [f["name"] for f in a]
        b_order = [f["name"] for f in b]
        if a_order != b_order:
            lines += [
                "Function field order/layout changed:",
                f"- old: `{a_order}`",
                f"- new: `{b_order}`",
            ]

        am = {f["name"]: f["signature"] for f in a}
        bm = {f["name"]: f["signature"] for f in b}
        for field in sorted(am.keys() | bm.keys()):
            if am.get(field) != bm.get(field):
                lines += [
                    f"- `{field}`",
                    f"  - old: `{am.get(field, 'absent')}`",
                    f"  - new: `{bm.get(field, 'absent')}`",
                ]

    if not changes:
        lines += ["", "No indexed declaration or function-field order changes detected."]

    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("old")
    parser.add_argument("new")
    parser.add_argument("--markdown", default="sdk-diff.md")
    args = parser.parse_args(argv)

    try:
        output = compare(load(args.old), load(args.new))
        Path(args.markdown).write_text(output, "utf-8")
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(args.markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
