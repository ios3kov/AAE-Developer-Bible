#!/usr/bin/env python3
"""Changed-native CI gate. Missing licensed SDK is BLOCKED, never compiler PASS."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import tempfile
import urllib.request
from urllib.parse import urlsplit
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NATIVE_ROOTS = ('16-WORKING-TEMPLATES/', '17-NATIVE-SUITE-COOKBOOK/code/',
                '19-NATIVE-CODE-FOUNDATION/code/', '20-REFERENCE-IMPLEMENTATIONS/')
NATIVE_SUFFIXES = {'.c', '.cc', '.cpp', '.h', '.hpp', '.hh', '.r', '.rc'}
RUNNERS = {'scripts/check_native.py', '18-SDK-HEADER-TOOLS/run-macos.sh',
           '18-SDK-HEADER-TOOLS/run-windows.ps1'}


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], timeout=30)


def affected(paths):
    return sorted(p for p in paths if p in RUNNERS or
                  (p.startswith(NATIVE_ROOTS) and Path(p).suffix.lower() in NATIVE_SUFFIXES) or
                  (p.startswith('18-SDK-HEADER-TOOLS/') and Path(p).suffix.lower() in {'.py', '.json'}
                   and not p.startswith('18-SDK-HEADER-TOOLS/generated/')))


def changed_paths(root, base, head):
    if not re.fullmatch(r'[0-9a-f]{40}', head):
        raise ValueError('A full candidate Git SHA is required')
    if not base or base == '0' * 40:
        data = git(root, 'ls-tree', '-r', '--name-only', '-z', head)
    else:
        if not re.fullmatch(r'[0-9a-f]{40}', base):
            raise ValueError('A full base Git SHA is required')
        git(root, 'cat-file', '-e', base + '^{commit}')
        data = git(root, 'diff', '--no-renames', '--name-only', '-z', base, head, '--')
    return [p.decode('utf-8') for p in data.split(b'\0') if p]


def extract_sdk(archive, destination):
    """Extract only bounded regular ZIP members into a new private temporary directory."""
    destination = Path(destination).resolve()
    with zipfile.ZipFile(archive) as z:
        members = z.infolist()
        if not members or len(members) > 30000 or sum(i.file_size for i in members) > 2 * 1024**3:
            raise ValueError('SDK ZIP inventory exceeds supported bounds')
        seen = set()
        for info in members:
            p = PurePosixPath(info.filename)
            key = info.filename.rstrip('/').casefold()
            kind = stat.S_IFMT(info.external_attr >> 16)
            if (not key or key in seen or p.is_absolute() or '..' in p.parts or '\\' in info.filename
                    or ':' in info.filename or '\0' in info.filename
                    or kind not in {0, stat.S_IFREG, stat.S_IFDIR}
                    or (kind == stat.S_IFDIR) != info.is_dir() and kind != 0
                    or info.flag_bits & 1 or info.file_size > 512 * 1024**2):
                raise ValueError('Unsafe, duplicate or unsupported SDK ZIP member')
            seen.add(key)
        for info in members:
            out = destination.joinpath(*PurePosixPath(info.filename).parts)
            if info.is_dir():
                out.mkdir(parents=True, exist_ok=True)
            else:
                out.parent.mkdir(parents=True, exist_ok=True)
                with z.open(info) as src, out.open('xb') as dst:
                    while chunk := src.read(1024 * 1024):
                        dst.write(chunk)
    examples = [p.parent.parent for p in destination.rglob('AE_Effect.h') if p.parent.name == 'Headers']
    if len(examples) != 1:
        raise ValueError('SDK ZIP must contain exactly one Examples/Headers/AE_Effect.h')
    return examples[0]


def acquire_sdk(directory):
    url = os.environ.get('AE_SDK_ARCHIVE_URL', '')
    expected = os.environ.get('AE_SDK_ARCHIVE_SHA256', '')
    if not url or not re.fullmatch(r'[0-9a-f]{64}', expected):
        raise ValueError('Licensed SDK unavailable: configure AE_SDK_ARCHIVE_URL and its SHA-256')
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or not parsed.netloc or parsed.username or parsed.password:
        raise ValueError('SDK archive must use an owner-configured HTTPS URL without userinfo')
    archive = Path(directory) / 'sdk.zip'
    digest, size = hashlib.sha256(), 0
    try:
        with urllib.request.urlopen(url, timeout=60) as response, archive.open('xb') as out:
            if urlsplit(response.url).scheme != 'https':
                raise ValueError('SDK redirect must remain HTTPS')
            while chunk := response.read(1024 * 1024):
                size += len(chunk)
                if size > 1024**3:
                    raise ValueError('SDK download exceeds 1 GiB')
                digest.update(chunk)
                out.write(chunk)
    except Exception:
        # A signed URL may contain credentials; never print it in exception/log text.
        raise ValueError('SDK download failed or exceeded its supported bounds') from None
    if digest.hexdigest() != expected:
        raise ValueError('SDK archive SHA-256 mismatch')
    return extract_sdk(archive, Path(directory) / 'sdk')


def run_sdk(root, examples, expected_headers):
    from scripts.check_native import sdk_header_manifest
    if not re.fullmatch(r'[0-9a-f]{64}', expected_headers or ''):
        raise ValueError('AE_SDK_HEADERS_SHA256 must pin the complete Headers + Util identity')
    count, digest = sdk_header_manifest(Path(examples))
    if count == 0 or digest != expected_headers:
        raise ValueError('SDK header identity mismatch')
    if git(root, 'status', '--porcelain').strip():
        raise ValueError('Native gate requires a clean source checkout')
    command = ['bash', str(Path(root) / '18-SDK-HEADER-TOOLS/run-macos.sh'), str(examples)]
    result = subprocess.run(command, cwd=root, timeout=300, check=False)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', default=os.environ.get('NATIVE_BASE_SHA', ''))
    parser.add_argument('--force', action='store_true')
    parser.add_argument('--sdk', type=Path, help='Explicit already licensed local Examples path')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = {'status': 'BLOCKED', 'scope': 'native SDK contract/compiler only', 'host_runtime': 'NOT_RUN'}
    code = 2
    try:
        head = git(ROOT, 'rev-parse', 'HEAD').decode().strip()
        changes = affected(changed_paths(ROOT, args.base, head))
        report.update(source_git_sha=head, base_git_sha=args.base, affected_native_paths=changes)
        if not changes and not args.force:
            report.update(status='NOT_APPLICABLE', reason='No SDK consumer/driver/contract inputs changed')
            code = 0
        else:
            with tempfile.TemporaryDirectory(prefix='bible-sdk-') as temp:
                examples = args.sdk.resolve() if args.sdk else acquire_sdk(temp)
                code = run_sdk(ROOT, examples, os.environ.get('AE_SDK_HEADERS_SHA256', ''))
                report.update(status='PASS' if code == 0 else 'FAIL', runner_exit_code=code)
                code = 0 if code == 0 else 1
    except (OSError, ValueError, subprocess.SubprocessError, zipfile.BadZipFile) as error:
        report['reason'] = str(error)
    text = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    print(text)
    if args.report:
        args.report.write_text(text, encoding='utf-8')
    return code


if __name__ == '__main__':
    sys.path.insert(0, str(ROOT))
    raise SystemExit(main())
