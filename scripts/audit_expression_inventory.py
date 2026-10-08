"""Pinned expression headings; inventory is not semantic or host coverage."""
import argparse
import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import urlopen

REVISION = "a5c5c5066d0395239d524510ace060963f5c0d33"
REPO = "docsforadobe/after-effects-expression-reference"
FOLDERS = {"general", "layer", "objects", "text"}


def headings(text):
    # Keep overload headings separately; names aren't global unique identifiers.
    return re.findall(r"^###\s+(.+?)\s*$", text, re.M)


def source_record(path):
    with urlopen(f"https://raw.githubusercontent.com/{REPO}/{REVISION}/{path}",
                 timeout=60) as response:
        raw = response.read()
    return {"source_path": path, "source_sha256": hashlib.sha256(raw).hexdigest(),
            "headings": headings(raw.decode("utf-8"))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    with urlopen(f"https://api.github.com/repos/{REPO}/git/trees/{REVISION}?recursive=1",
                 timeout=60) as response:
        tree = json.load(response)
    if tree.get("truncated"):
        raise RuntimeError("truncated source tree")
    paths = sorted(r["path"] for r in tree["tree"] if r["type"] == "blob"
                   and r["path"].endswith(".md") and r["path"].split("/")[0] == "docs"
                   and r["path"].split("/")[1] in FOLDERS)
    with ThreadPoolExecutor(max_workers=6) as pool:
        records = list(pool.map(source_record, paths))
    result = {"source_revision": REVISION,
              "scope": "API-category third-level headings including overloads; not all signatures",
              "warning": "Unreviewed inventory; no mention-based or automatic PASS",
              "source_pages": len(records),
              "headings": sum(len(r["headings"]) for r in records), "records": records}
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("source_revision", "source_pages", "headings")}))


if __name__ == "__main__":
    main()
