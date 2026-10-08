"""Pinned official AE UXP property rows and method headings; no coverage inference."""
import argparse
import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import urlopen

REVISION = "7d1cd01b4c69a9e02b77d48b3f919a6145a90841"
REPO = "AdobeDocs/uxp-after-effects"
PREFIX = "src/pages/after-effects-api/"


def members(text):
    section = ""
    result = []
    for line in text.splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        elif section == "Properties" and line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) == 5 and re.fullmatch(r"[A-Za-z]\w*", cells[0]) and cells[0] != "Name":
                result.append({"kind": "property", "name": cells[0], "type": cells[1],
                               "access": cells[2], "min_version": cells[3]})
        elif line.startswith("### ") and "Methods" in section:
            result.append({"kind": section, "name": line[4:].strip()})
    return result


def source_record(path):
    with urlopen(f"https://raw.githubusercontent.com/{REPO}/{REVISION}/{path}", timeout=60) as response:
        raw = response.read()
    return {"source_path": path, "source_sha256": hashlib.sha256(raw).hexdigest(),
            "members": members(raw.decode("utf-8"))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    with urlopen(f"https://api.github.com/repos/{REPO}/git/trees/{REVISION}?recursive=1", timeout=60) as response:
        tree = json.load(response)
    if tree.get("truncated"):
        raise RuntimeError("truncated tree")
    paths = sorted(r["path"] for r in tree["tree"] if r["type"] == "blob"
                   and r["path"].startswith(PREFIX) and r["path"].endswith(".md"))
    with ThreadPoolExecutor(max_workers=6) as pool:
        records = list(pool.map(source_record, paths))
    result = {"source_revision": REVISION, "repository": REPO,
              "scope": "Property-table rows and method headings, not all overloads/inherited contracts",
              "warning": "Inventory NOT semantic review, installed availability or host PASS",
              "source_pages": len(records), "members": sum(len(r["members"]) for r in records),
              "records": records}
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("source_revision", "source_pages", "members")}))


if __name__ == "__main__":
    main()
