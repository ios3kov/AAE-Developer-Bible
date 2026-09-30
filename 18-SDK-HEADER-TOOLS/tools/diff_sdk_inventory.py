#!/usr/bin/env python3
"""Compare indexed declarations, including field order; not a complete ABI diff."""
import argparse
import json
from pathlib import Path
import sys


def load(path):
    data = json.loads(Path(path).read_text("utf-8"))
    if data.get("unparsed_candidate_tables") or data.get("partial_candidate_tables"):
        raise ValueError(f"Incomplete inventory: {path}")
    tables = {}
    for table in data["tables"]:
        name = table["name"]
        if name in tables and tables[name] != table["functions"]:
            raise ValueError(f"Conflicting declarations for {name}")
        tables[name] = table["functions"]
    if not tables:
        raise ValueError("No tables to compare")
    return tables


def compare(old, new):
    lines = ["# SDK declaration diff", "", "> Textual declarations and function-field order only; not a complete ABI compatibility test.", ""]
    lines += ["## Contract tables", ""]
    for label, names in (("Added", new.keys() - old.keys()), ("Removed", old.keys() - new.keys())):
        lines.append(f"- {label}: " + (", ".join(f"`{n}`" for n in sorted(names)) or "none"))
    changes = bool(old.keys() ^ new.keys())
    for name in sorted(old.keys() & new.keys()):
        a, b = old[name], new[name]
        if a == b:
            continue
        changes = True
        lines += ["", f"## `{name}`", ""]
        a_order, b_order = [f["name"] for f in a], [f["name"] for f in b]
        if a_order != b_order:
            lines += ["Function field order/layout changed:", f"- old: `{a_order}`", f"- new: `{b_order}`"]
        am, bm = {f["name"]: f["signature"] for f in a}, {f["name"]: f["signature"] for f in b}
        for field in sorted(am.keys() | bm.keys()):
            if am.get(field) != bm.get(field):
                lines += [f"- `{field}`", f"  - old: `{am.get(field, 'absent')}`", f"  - new: `{bm.get(field, 'absent')}`"]
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
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(args.markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
