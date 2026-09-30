#!/usr/bin/env python3
"""Install a built plugin and optionally invoke aerender, fail-closed."""
import argparse, json, shutil, subprocess
from pathlib import Path

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("plugin", type=Path); ap.add_argument("--aerender", type=Path, required=True)
    ap.add_argument("--project", type=Path); ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--install-root", type=Path, required=True); a = ap.parse_args()
    if not a.plugin.is_dir() or a.plugin.suffix != ".plugin": ap.error("plugin must be a .plugin bundle")
    if not a.aerender.exists(): ap.error("aerender does not exist")
    a.install_root.mkdir(parents=True, exist_ok=True); installed=a.install_root/a.plugin.name
    if installed.exists(): shutil.rmtree(installed)
    shutil.copytree(a.plugin, installed)
    report={"build":"external","pipl":"bundle supplied","install":str(installed),"load":"pending","unload":"pending","stress_mfr":"pending"}
    if a.project:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        r=subprocess.run([str(a.aerender),"-project",str(a.project),"-output",str(a.output)],text=True,capture_output=True)
        report["execute_render"]={"returncode":r.returncode,"stdout":r.stdout[-4000:],"stderr":r.stderr[-4000:]}
    report["note"]="aerender evidence does not prove UI unload or MFR stress"
    p=a.output.with_suffix(a.output.suffix+".host-cycle.json"); p.write_text(json.dumps(report,indent=2)+"\n"); print(p)

if __name__ == "__main__": main()
