"""Pinned public scripting member inventory; mentions are not reviewed coverage."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent.parent
REVISION = "7137a990db4bd8dc9f5869b8ca431c7dfed52bdc"
REPO = "docsforadobe/after-effects-scripting-guide"
DOM_FOLDERS = {"general", "item", "layer", "property", "text", "renderqueue", "other", "sources"}


def members(text):
    # Preserve overloads as one member; headings are an inventory, not signature parsing.
    return sorted(set(re.findall(r"^###\s+([A-Za-z][A-Za-z0-9_]*\.[A-Za-z][A-Za-z0-9_]*)(?:\(\))?:?\s*$",
                                 text, re.M)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    with urlopen(f"https://api.github.com/repos/{REPO}/git/trees/{REVISION}?recursive=1",
                 timeout=60) as response:
        tree = json.load(response)
    if tree.get("truncated"):
        raise RuntimeError("truncated source tree; refuse incomplete inventory")
    paths = sorted(entry["path"] for entry in tree["tree"]
                   if entry["type"] == "blob" and entry["path"].endswith(".md")
                   and entry["path"].split("/")[:1] == ["docs"]
                   and entry["path"].split("/")[1] in DOM_FOLDERS)
    # Exclude generated summaries: a token in MASTER is not an independent lesson.
    corpus = {}
    for folder in ("06-SCRIPTING", "16-WORKING-TEMPLATES"):
        for path in (ROOT / folder).rglob("*"):
            if path.suffix in {".md", ".jsx", ".js"}:
                corpus[path.relative_to(ROOT).as_posix()] = path.read_text(encoding="utf-8")
    records = []
    for path in paths:
        with urlopen(f"https://raw.githubusercontent.com/{REPO}/{REVISION}/{path}",
                     timeout=60) as response:
            raw = response.read()
        text = raw.decode("utf-8")
        headings = members(text)
        records.append({"source_path": path, "source_sha256": hashlib.sha256(raw).hexdigest(),
                        "members": [{"name": name,
                                     "literal_mentions": sorted(p for p, body in corpus.items()
                                                                if name in body),
                                     "review_status": "UNASSESSED"}
                                    for name in headings]})
    report = {"source_revision": REVISION, "scope": "DOM member headings; excludes expressions/matchnames",
              "warning": "Literal mentions do not establish practical or contract coverage. No auto-PASS.",
              "source_pages": len(records),
              "members": sum(len(r["members"]) for r in records), "records": records}
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("source_revision", "source_pages", "members")}))


if __name__ == "__main__":
    main()
