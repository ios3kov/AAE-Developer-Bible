#!/usr/bin/env python3
"""Check native recipe call-sites against an inventory generated from local SDK headers."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

CALL_RE = re.compile(r"(?:->|\.)\s*(?P<name>(?:AEGP|PF|AEIO|PR|DRAWBOT)_[A-Za-z0-9_]+)\s*\(")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("inventory_json")
    ap.add_argument("paths", nargs="+", help="Recipe source files/directories")
    args = ap.parse_args()
    data = json.loads(Path(args.inventory_json).read_text("utf-8"))
    known = {f["name"] for t in data["tables"] for f in t["functions"]}
    files=[]
    for raw in args.paths:
        p=Path(raw)
        files.extend([p] if p.is_file() else sorted(p.rglob("*.cpp"))+sorted(p.rglob("*.h"))+sorted(p.rglob("*.hpp")))
    unknown=[]; checked=0
    for p in files:
        text=p.read_text("utf-8",errors="replace")
        for m in CALL_RE.finditer(text):
            checked += 1
            name=m.group("name")
            if name not in known:
                line=text.count("\n",0,m.start())+1
                unknown.append((str(p),line,name))
    print(f"call_sites={checked} unknown={len(unknown)}")
    for p,line,name in unknown:
        print(f"UNKNOWN {p}:{line}: {name}")
    return 1 if unknown else 0

if __name__ == "__main__":
    raise SystemExit(main())
