#!/usr/bin/env python3
"""Bounded documentation regressions; not a technical or host certification."""
import json
from pathlib import Path
import re
import subprocess
import yaml

ROOT = Path(__file__).resolve().parents[1]
CEP_PAGES = ["07-PANELS/01-CEP.md", "15-COMMUNICATION/06-CEP-TO-EXTENDSCRIPT.md",
             "12-RECIPES/05-HYBRID-PANEL-NATIVE.md",
             "16-WORKING-TEMPLATES/cep-panel-bridge/README.md"]


def validate_envelope(value):
    if not isinstance(value, dict) or type(value.get("protocol")) is not int or value['protocol'] != 1:
        raise ValueError("protocol must be integer 1")
    if not isinstance(value.get('requestId'), str) or not value['requestId']:
        raise ValueError("correlation id missing in canonical example")
    if 'command' in value:
        if value['command'] != 'renameSelected' or set(value) != {'protocol', 'requestId', 'command', 'payload'}:
            raise ValueError("canonical rename request fields/command")
        if not isinstance(value['payload'], dict) or set(value['payload']) != {'prefix'} or not isinstance(value['payload']['prefix'], str):
            raise ValueError("canonical payload.prefix must be string")
    elif type(value.get('ok')) is not bool:
        raise ValueError("response ok must be boolean")
    elif value['ok']:
        if set(value) != {'protocol', 'requestId', 'ok', 'result'}:
            raise ValueError("exclusive success envelope")
        if not isinstance(value.get('result'), dict):
            raise ValueError('result must be object')
        changed = value['result'].get('changed')
        if type(changed) is not int or changed < 0:
            raise ValueError("changed must be nonnegative integer")
    else:
        if set(value) != {'protocol', 'requestId', 'ok', 'error'}:
            raise ValueError("exclusive error envelope")
        e = value['error']
        if not isinstance(e, dict) or not isinstance(e.get('code'), str) or not e['code'] or not isinstance(e.get('message'), str) or e.get('outcome') not in {'notApplied', 'mayHaveApplied'}:
            raise ValueError("invalid error contract")


def cep_errors(texts):
    errors = []
    for path in CEP_PAGES:
        kinds = set()
        # Existing chapters use both json and javascript fences for JSON examples.
        for _, block in re.findall(r'(```|~~~)(?:json|javascript)\s*\n(.*?)\n\1', texts[path], re.S):
            try:
                value = json.loads(block)
            except json.JSONDecodeError:
                continue  # Executable JS snippets are not envelopes.
            if isinstance(value, dict) and 'protocol' in value:
                try:
                    validate_envelope(value)
                    kinds.add('request' if 'command' in value else 'success' if value['ok'] else 'error')
                except ValueError as e:
                    errors.append(f'{path}: {e}')
        if kinds != {'request', 'success', 'error'}:
            errors.append(f'{path}: missing canonical request/success/error examples')
    return errors


def menu_paths(nav):
    for entry in nav:
        for value in entry.values():
            if isinstance(value, list):
                yield from menu_paths(value)
            else:
                yield value


def core_paths(text):
    rows = []
    for line in text.splitlines():
        if line.startswith('| [') and len(line.split('|')) == 9:
            rows.append(re.search(r'\]\(([^)#]+\.md)\)', line).group(1))
    return rows


def navigation_errors(texts):
    errors = []
    core = core_paths(texts['CHAPTER-COMPLETION-TRACKER.md'])
    if len(core) != 129 or len(set(core)) != 129:
        errors.append('core baseline must contain 129 unique tracked rows; changes require review')
    menu = set(menu_paths(yaml.safe_load(texts['mkdocs.yml'])['nav']))
    catalogue = {p.split('#')[0] for p in re.findall(r'\]\(([^)]+)\)', texts['NAVIGATION.md'])}
    for path in sorted(set(core) - menu):
        errors.append(f'core page disappeared from menu: {path}')
    for path in sorted(menu - catalogue):
        errors.append(f'menu page absent from NAVIGATION: {path}')
    return errors


def evidence_errors(texts, registry):
    """Check declared current boundaries; historical PASS records remain untouched."""
    errors = []
    for path, boundary in registry['required_boundaries'].items():
        if boundary not in texts[path]:
            errors.append(f'{path}: declared current boundary missing: {boundary}')
    for path, text in texts.items():
        if re.search(r'^\s*(?:\*\*)?CURRENT-(?:COMPILE|RUNTIME|HOST):\s*PASS\b', text, re.M):
            errors.append(f'{path}: current positive evidence requires reviewed identity-bound registry entry')
    return errors


def check(root=ROOT):
    paths = subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=root).split(b'\0')
    texts = {p: (root / p).read_text(encoding='utf-8') for p in sorted({x.decode() for x in paths if x})
             if p.endswith('.md') and p != 'MASTER-AE-DEVELOPER-BIBLE.md'}
    texts['mkdocs.yml'] = (root / 'mkdocs.yml').read_text()
    registry = json.loads((root / 'tests/consistency/evidence-boundaries.json').read_text())
    exclusions = {'11-DISTRIBUTION/05-PLATFORM-SOURCE-REVIEW-2026-10-01.md',
                  '17-NATIVE-SUITE-COOKBOOK/VERIFICATION.md'}
    prefixes = tuple(f'{i:02d}-' for i in list(range(16)) + [17,19])
    inventory = {p for p in texts if len(Path(p).parts) == 2 and Path(p).parts[0].startswith(prefixes)} - exclusions
    declared = set(core_paths(texts['CHAPTER-COMPLETION-TRACKER.md']))
    errors = [f'core inventory/tracker mismatch: {p}' for p in sorted(inventory ^ declared)]
    return errors + cep_errors(texts) + navigation_errors(texts) + evidence_errors(texts, registry)


def main():
    errors = check()
    sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    print(json.dumps({'git_sha': sha, 'scope': 'CEP examples / 129 core menu entries / declared evidence boundaries',
                      'dirty':bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip()),
                      'errors': errors, 'status': 'FAIL' if errors else 'PASS'}, indent=2))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
