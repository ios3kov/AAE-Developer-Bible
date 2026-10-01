#!/usr/bin/env python3
"""Verify that an SDK inventory contains the Bible's required contract tables."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

INVENTORY_SCHEMA_VERSION = 1
MANIFEST_SCHEMA_VERSION = 1


def load_inventory(path: Path) -> dict:
    data = json.loads(path.read_text("utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != INVENTORY_SCHEMA_VERSION:
        raise ValueError("Unsupported or missing inventory schema_version")
    if data.get("unparsed_candidate_tables") or data.get("partial_candidate_tables"):
        raise ValueError("Inventory is incomplete; parser diagnostics are present")
    tables = data.get("tables")
    if not isinstance(tables, list) or not tables:
        raise ValueError("Inventory contains no contract tables")
    return data


def load_manifest(path: Path) -> dict:
    data = json.loads(path.read_text("utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != MANIFEST_SCHEMA_VERSION:
        raise ValueError("Unsupported or missing required-contract manifest schema_version")
    required = data.get("required_tables")
    if not isinstance(required, list) or not required:
        raise ValueError("Required-contract manifest contains no required_tables")
    for entry in required:
        if (
            not isinstance(entry, dict)
            or not isinstance(entry.get("name"), str)
            or not entry["name"]
            or not isinstance(entry.get("area"), str)
            or not entry["area"]
        ):
            raise ValueError("Malformed required_tables entry")
        functions = entry.get("required_functions", [])
        if (
            not isinstance(functions, list)
            or any(not isinstance(name, str) or not name for name in functions)
        ):
            raise ValueError(f"Malformed required_functions for {entry['name']}")
    return data


def verify_required(inventory: dict, manifest: dict):
    present = {}
    for table in inventory["tables"]:
        if not isinstance(table, dict) or not isinstance(table.get("name"), str):
            continue
        functions = table.get("functions")
        present[table["name"]] = {
            f.get("name")
            for f in functions
            if isinstance(f, dict) and isinstance(f.get("name"), str)
        }

    missing = []
    for entry in manifest["required_tables"]:
        if entry["name"] not in present:
            missing.append({**entry, "missing_functions": None})
            continue

        required_functions = entry.get("required_functions", [])
        absent = [name for name in required_functions if name not in present[entry["name"]]]
        if absent:
            missing.append({**entry, "missing_functions": absent})

    return len(manifest["required_tables"]), missing


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inventory_json", type=Path)
    parser.add_argument("manifest_json", type=Path)
    args = parser.parse_args(argv)

    try:
        inventory = load_inventory(args.inventory_json)
        manifest = load_manifest(args.manifest_json)
        required_count, missing = verify_required(inventory, manifest)
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(
        f"required_tables={required_count} missing={len(missing)} "
        f"target={manifest.get('target_sdk', 'unspecified')}"
    )
    for entry in missing:
        if entry.get("missing_functions") is None:
            print(f"MISSING_TABLE {entry['name']} [{entry['area']}]")
        else:
            names = ",".join(entry["missing_functions"])
            print(f"MISSING_FUNCTIONS {entry['name']} [{entry['area']}]: {names}")

    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
