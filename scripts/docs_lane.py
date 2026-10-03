#!/usr/bin/env python3
"""Select source staging or frozen-output validation before any regeneration."""
import argparse
import json
import os
from pathlib import Path
import subprocess
from build_docs import ROOT, GENERATED, source_digest, tracked_files


def classify(changed):
    return 'frozen' if changed and set(changed) <= GENERATED else 'source'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lane', choices=['auto','source','frozen'], default='auto')
    parser.add_argument('--github-output', type=Path)
    args = parser.parse_args()
    sha = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    changed = []
    if args.lane == 'auto' and os.environ.get('GITHUB_EVENT_NAME') == 'push':
        parent = subprocess.run(['git','rev-parse','--verify','HEAD^'],cwd=ROOT,capture_output=True,text=True)
        if parent.returncode == 0:
            changed = subprocess.check_output(['git','diff','--name-only',parent.stdout.strip(),sha],cwd=ROOT,text=True).splitlines()
    lane = classify(changed) if args.lane == 'auto' else args.lane
    report = {'lane':lane, 'checked_out_git_sha':sha, 'trigger_git_sha':os.environ.get('GITHUB_SHA'),
              'pull_request_head_sha':os.environ.get('PR_HEAD_SHA'), 'source_content_sha256':source_digest(tracked_files()),
              'changed_paths':changed,
              'dirty':bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip())}
    print(json.dumps(report,indent=2))
    if args.github_output:
        with args.github_output.open('a') as f: f.write('lane='+lane+'\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
