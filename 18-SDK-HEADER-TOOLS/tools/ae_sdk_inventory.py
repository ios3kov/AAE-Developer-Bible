#!/usr/bin/env python3
"""Build a native After Effects SDK contract inventory from local C/C++ headers.

No Adobe headers are bundled. Point this tool at the SDK Include/Headers directory
that you are legally using on your machine. The output is a machine-readable JSON
plus a Markdown index of suite/function-table contracts found in that SDK version.

The parser intentionally targets C ABI function-pointer tables instead of trying to
be a full C++ parser. It handles named and anonymous typedef structs and normalizes
multiline function-pointer declarations. For unusual macro-heavy headers, inspect
`unparsed_candidate_tables` in the JSON and use the SDK headers as source of truth.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable, Sequence

TABLE_NAME_RE = re.compile(
    r"(?:Suite\d*|FunctionBlock\d*|EntryPoints\d*|EntryPoints|Callbacks\d*|Callbacks)$"
)
FUNC_PTR_RE = re.compile(
    r"(?P<ret>[A-Za-z_][\w\s*]*?)"
    r"\(\s*\*\s*(?P<name>[A-Za-z_][\w]*)\s*\)\s*"
    r"\((?P<args>.*?)\)\s*;",
    re.S,
)
TYPEDEF_FUNC_PTR_RE = re.compile(
    r"typedef\s+(?P<ret>[A-Za-z_][\w\s*]*?)"
    r"\(\s*\*\s*(?P<name>[A-Za-z_][\w]*)\s*\)\s*"
    r"\((?P<args>.*?)\)\s*;",
    re.S,
)
CALLBACK_FIELD_RE = re.compile(
    r"(?P<type>[A-Za-z_][\w]*)\s+(?P<name>[A-Za-z_][\w]*)\s*;"
)
NAMED_STRUCT_RE = re.compile(
    r"typedef\s+struct\s+(?P<tag>[A-Za-z_][\w]*)\s*\{(?P<body>.*?)\}\s*(?P<alias>[A-Za-z_][\w]*)\s*;",
    re.S,
)
ANON_STRUCT_RE = re.compile(
    r"typedef\s+struct\s*\{(?P<body>.*?)\}\s*(?P<alias>[A-Za-z_][\w]*)\s*;",
    re.S,
)
DEFINE_RE = re.compile(r"^\s*#\s*define\s+(?P<name>[A-Za-z_][\w]*)\s+(?P<value>.+?)\s*$", re.M)


@dataclass
class FunctionDecl:
    name: str
    return_type: str
    arguments: str
    signature: str


@dataclass
class ContractTable:
    name: str
    tag: str
    family: str
    source_file: str
    source_sha256: str
    functions: list[FunctionDecl] = field(default_factory=list)
    nearby_defines: dict[str, str] = field(default_factory=dict)


def strip_comments(text: str) -> str:
    # Preserve newlines so diagnostics remain roughly line-correlated.
    text = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    text = re.sub(r"//[^\n]*", "", text)
    return text


def normalize_ws(text: str) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    text = re.sub(r"\s*,\s*", ", ", text)
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)
    return text


def family_for(name: str) -> str:
    prefixes = (
        ("AEGP_", "AEGP"),
        ("PF_", "PF/Effect"),
        ("AEIO_", "AEIO"),
        ("PR_", "Artisan/PR"),
        ("DRAWBOT_", "Drawbot"),
        ("SP", "PICA/SP"),
    )
    for prefix, family in prefixes:
        if name.startswith(prefix):
            return family
    return "Other"


def iter_headers(inputs: Sequence[str]) -> list[Path]:
    out: set[Path] = set()
    for raw in inputs:
        p = Path(raw).expanduser().resolve()
        if not p.exists():
            raise FileNotFoundError(p)
        if p.is_file():
            out.add(p)
        else:
            for ext in ("*.h", "*.hpp", "*.hh"):
                out.update(x.resolve() for x in p.rglob(ext))
    return sorted(out)


def callback_typedefs(clean_text: str) -> dict[str, tuple[str, str]]:
    out: dict[str, tuple[str, str]] = {}
    for match in TYPEDEF_FUNC_PTR_RE.finditer(clean_text):
        out[match.group("name")] = (
            normalize_ws(match.group("ret")),
            normalize_ws(match.group("args")),
        )
    return out


def parse_functions(body: str, callback_types: dict[str, tuple[str, str]] | None = None) -> tuple[list[FunctionDecl], list[str]]:
    funcs: list[FunctionDecl] = []
    unresolved: list[str] = []
    callback_types = callback_types or {}
    # Adobe tables frequently prefix fields with SPAPI. Remove only the calling-convention token.
    body = re.sub(r"\bSPAPI\b", "", body)
    # Full-match individual declarations: bounded work on macro-heavy headers,
    # and no accidental match starting halfway through an unsupported field.
    for declaration in body.split(";"):
        declaration = declaration.strip()
        if not declaration:
            continue
        text = declaration + ";"
        m = FUNC_PTR_RE.fullmatch(text)
        if m:
            ret = normalize_ws(m.group("ret"))
            name = m.group("name")
            args = normalize_ws(m.group("args"))
            sig = f"{ret} (*{name})({args});"
            funcs.append(FunctionDecl(name=name, return_type=ret, arguments=args, signature=sig))
            continue

        field = CALLBACK_FIELD_RE.fullmatch(text)
        if field and field.group("type") in callback_types:
            ret, args = callback_types[field.group("type")]
            name = field.group("name")
            sig = f"{ret} (*{name})({args});"
            funcs.append(FunctionDecl(name=name, return_type=ret, arguments=args, signature=sig))
            continue

        unresolved.append(declaration)
    return funcs, unresolved


def nearby_defines(raw_text: str, start: int, table_name: str) -> dict[str, str]:
    window = raw_text[max(0, start - 2500):start]
    defs = {m.group("name"): normalize_ws(m.group("value")) for m in DEFINE_RE.finditer(window)}
    # Keep likely suite/table metadata plus any exact family stem versions.
    stem = re.sub(r"(?:Suite|FunctionBlock|EntryPoints|Callbacks)\d*$", "", table_name)
    selected = {}
    for k, v in defs.items():
        if (
            "Suite" in k
            or "Version" in k
            or "VERSION" in k
            or (stem and stem.replace("_", "").lower() in k.replace("_", "").lower())
        ):
            selected[k] = v
    return dict(sorted(selected.items()))


def parse_header(path: Path, base: Path | None = None, partial: dict | None = None) -> tuple[list[ContractTable], list[str]]:
    raw = path.read_text("utf-8", errors="replace")
    clean = strip_comments(raw)
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    rel = str(path.relative_to(base)) if base and path.is_relative_to(base) else str(path)
    found: list[ContractTable] = []
    seen_spans: set[tuple[int, int]] = set()
    callback_types = callback_typedefs(clean)

    for rx in (NAMED_STRUCT_RE, ANON_STRUCT_RE):
        for m in rx.finditer(clean):
            span = m.span()
            if span in seen_spans:
                continue
            seen_spans.add(span)
            alias = m.group("alias")
            tag = m.groupdict().get("tag") or alias
            if not TABLE_NAME_RE.search(alias):
                continue
            funcs, unresolved = parse_functions(m.group("body"), callback_types)
            # Keep non-function/data fields as diagnostics. Required-contract verification
            # decides whether a diagnostic blocks the acceptance lane.
            remainder = "; ".join(unresolved)
            if remainder and partial is not None:
                partial[f"{rel}:{alias}"] = normalize_ws(remainder)
            if not funcs:
                continue
            found.append(
                ContractTable(
                    name=alias,
                    tag=tag,
                    family=family_for(alias),
                    source_file=rel,
                    source_sha256=sha,
                    functions=funcs,
                    nearby_defines=nearby_defines(clean, m.start(), alias),
                )
            )

    # Candidate tables whose names look right but yielded no fields are useful diagnostics.
    candidate_names = set(re.findall(r"}\s*([A-Za-z_][\w]*(?:Suite\d*|FunctionBlock\d*|EntryPoints\d*|Callbacks\d*))\s*;", clean))
    parsed_names = {t.name for t in found}
    unparsed = sorted(candidate_names - parsed_names)
    return found, unparsed


def inventory(inputs: Sequence[str]) -> dict:
    headers = iter_headers(inputs)
    if not headers:
        raise RuntimeError("No .h/.hpp/.hh files found")
    common_base = Path(Path(*Path(headers[0]).parts[:1]))
    try:
        import os
        common_base = Path(os.path.commonpath([str(p.parent) for p in headers]))
    except Exception:
        common_base = None

    tables: list[ContractTable] = []
    unparsed: dict[str, list[str]] = {}
    partial: dict[str, str] = {}
    for h in headers:
        ts, bad = parse_header(h, common_base, partial)
        tables.extend(ts)
        if bad:
            unparsed[str(h)] = bad

    # A given table can appear in more than one header subtree. Prefer one unique contract per
    # table name+signature set, but preserve different generations (Suite6, Suite7, ...).
    dedup: dict[tuple[str, tuple[str, ...]], ContractTable] = {}
    for t in tables:
        key = (t.name, tuple(f.signature for f in t.functions))
        dedup.setdefault(key, t)
    tables = sorted(dedup.values(), key=lambda t: (t.family, t.name, t.source_file))

    return {
        "schema_version": 1,
        "header_count": len(headers),
        "table_count": len(tables),
        "function_count": sum(len(t.functions) for t in tables),
        "families": sorted({t.family for t in tables}),
        "tables": [asdict(t) for t in tables],
        "unparsed_candidate_tables": unparsed,
        "partial_candidate_tables": partial,
    }


def markdown(data: dict) -> str:
    lines = [
        "# Generated After Effects native SDK contract inventory",
        "",
        "> Generated from local SDK headers. Do not hand-edit. The headers used for your build remain the source of truth.",
        "",
        f"- Headers scanned: **{data['header_count']}**",
        f"- Contract tables: **{data['table_count']}**",
        f"- Function-pointer entries: **{data['function_count']}**",
        "",
    ]
    families: dict[str, list[dict]] = {}
    for t in data["tables"]:
        families.setdefault(t["family"], []).append(t)
    for family in sorted(families):
        lines += [f"## {family}", ""]
        for t in families[family]:
            lines += [f"### `{t['name']}`", "", f"Source: `{t['source_file']}`", ""]
            if t["nearby_defines"]:
                lines.append("Nearby SDK macros:")
                for k, v in t["nearby_defines"].items():
                    lines.append(f"- `{k}` = `{v}`")
                lines.append("")
            lines += ["| Function | Header signature |", "|---|---|"]
            for f in t["functions"]:
                sig = f["signature"].replace("|", "\\|")
                lines.append(f"| `{f['name']}` | `{sig}` |")
            lines.append("")
    if data.get("unparsed_candidate_tables"):
        lines += ["## Parser diagnostics", "", "The following table-like declarations matched by name but were not parsed. Inspect them manually:", ""]
        for src, names in sorted(data["unparsed_candidate_tables"].items()):
            lines.append(f"- `{src}`: " + ", ".join(f"`{n}`" for n in names))
        lines.append("")
    if data.get("partial_candidate_tables"):
        lines += ["## Partially parsed tables", "", "Unsupported declarations remain; this inventory is incomplete.", ""]
        for name, remainder in sorted(data["partial_candidate_tables"].items()):
            lines.append(f"- `{name}`: `{remainder}`")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+", help="SDK header file(s) or directories")
    ap.add_argument("--json", dest="json_path", default="ae-sdk-inventory.json")
    ap.add_argument("--markdown", dest="md_path", default="ae-sdk-inventory.md")
    ap.add_argument("--allow-incomplete", action="store_true", help="Write an exploratory index despite diagnostics (never a verification pass)")
    args = ap.parse_args(argv)
    try:
        data = inventory(args.inputs)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    for destination in (args.json_path, args.md_path):
        Path(destination).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", "utf-8")
    Path(args.md_path).write_text(markdown(data), "utf-8")
    print(f"headers={data['header_count']} tables={data['table_count']} functions={data['function_count']}")
    print(f"json={args.json_path}")
    print(f"markdown={args.md_path}")
    incomplete = not data["table_count"] or data["unparsed_candidate_tables"] or data["partial_candidate_tables"]
    if incomplete:
        print("Incomplete index: inspect parser diagnostics; no ABI or signature validation performed", file=sys.stderr)
        return 0 if args.allow_incomplete else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
