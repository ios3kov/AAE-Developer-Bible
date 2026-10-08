"""Exact-byte page inventories for pinned native/ExtendScript public guides.

Every Markdown blob below docs/ is included, including navigation and historical
pages. This inventories source files, not SDK declarations or semantic coverage.
An explicit editorial review ledger is maintained separately.
"""
import argparse
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import urlopen

PROFILES = {
    "native": ("docsforadobe/after-effects-plugin-guide",
               "6d9b285d9755d1fbf8ead7680ba49de24f94b547",
               "35566e8001d791aa6322602978df27ae5da4ceee"),
    "extendscript": ("docsforadobe/javascript-tools-guide",
                    "ac6839049e17f4652d301e7d28f8f0d3d5fbb66a",
                    "edb30d633a85608f310fd3bb9a3023d42cd21766"),
}


def page_entries(tree, tree_sha):
    if tree.get("truncated") is not False or tree.get("sha") != tree_sha:
        raise ValueError("A complete tree for the pinned commit's tree SHA is required")
    entries = sorted((entry for entry in tree["tree"]
                      if entry.get("type") == "blob"
                      and entry["path"].startswith("docs/")
                      and entry["path"].endswith(".md")), key=lambda e: e["path"])
    if len({entry["path"] for entry in entries}) != len(entries):
        raise ValueError("Duplicate source path")
    for entry in entries:
        if entry.get("mode") not in ("100644", "100755"):
            raise ValueError("A source page must be a regular file")
        if ".." in Path(entry["path"]).parts:
            raise ValueError("Invalid source path")
    return entries


def source_record(entry, raw):
    blob_sha = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
    if blob_sha != entry["sha"] or len(raw) != entry["size"]:
        raise ValueError("Bytes do not match the pinned Git blob: " + entry["path"])
    text = raw.decode("utf-8")
    return {"source_path": entry["path"], "git_blob_sha": blob_sha,
            "source_sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw), "lines": len(text.splitlines())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=PROFILES, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--tree-json", type=Path,
                        help="Previously retrieved complete GitHub tree; pin is checked")
    parser.add_argument("--source-root", type=Path,
                        help="Exact raw source cache preserving repository paths")
    args = parser.parse_args()
    repository, revision, tree_sha = PROFILES[args.profile]
    tree_url = f"https://api.github.com/repos/{repository}/git/trees/{tree_sha}?recursive=1"
    if args.tree_json:
        tree = json.loads(args.tree_json.read_text(encoding="utf-8"))
    else:
        with urlopen(tree_url, timeout=30) as response:
            tree = json.load(response)
    entries = page_entries(tree, tree_sha)

    def read(entry):
        if args.source_root:
            raw = (args.source_root / entry["path"]).read_bytes()
        else:
            url = f"https://raw.githubusercontent.com/{repository}/{revision}/{entry['path']}"
            with urlopen(url, timeout=30) as response:
                raw = response.read()
        return source_record(entry, raw)

    with ThreadPoolExecutor(max_workers=6) as pool:
        records = list(pool.map(read, entries))
    result = {"repository": repository, "source_revision": revision,
              "tree_sha": tree_sha, "tree_url": tree_url, "tree_truncated": False,
              "scope": "All Markdown blobs under docs/. Page inventory, not all SDK/"
                       "runtime symbols, signatures, versions, semantic or host coverage.",
              "source_pages": len(records), "records": records}
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps({"source_pages": len(records), "source_revision": revision,
                      "exact_blob_checks": "PASS"}))


if __name__ == "__main__":
    main()
