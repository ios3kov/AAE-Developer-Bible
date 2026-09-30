#!/usr/bin/env python3
"""Deterministic auxiliary EXR inputs. Offline file checks, NOT an AE test runner.

This intentionally implements only uncompressed single-part scanline FLOAT/UINT.
The independent OpenEXR reference reader is mandatory in the fixture CI job.
No Adobe installation, preferences, projects or channel maps are modified.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.metadata
import json
import math
import re
import struct
from pathlib import Path

BUILD = 'ACX-INPUT-20260930-01'
WIDTH, HEIGHT = 64, 32
MAGIC = 20000630
MAX_FILE = 32 * 1024 * 1024
MAP_NAME = 'OpenEXR_channel_map.CANDIDATE.txt'
MAPPING = (
    ('Z', 'DPTH', 'FLT4'),
    ('objectID', 'OBID', 'UST2'),
    ('acxU|acxV', 'TEXR', 'FLT4'),
    ('acxNX|acxNY|acxNZ', 'NRML', 'FLT4'),
    ('acxCoverage', 'COVR', 'FLT4'),
    ('acxBgR|acxBgG|acxBgB', 'BKCR', 'UBT1'),
    ('materialID', 'MATR', 'UBT1'),
)
MAP_TEXT = '# CANDIDATE ONLY. Not installed or host-qualified. Do not overwrite a live map.\n' + \
    '# Pin and inspect the installed importer and existing map before any AE test.\n' + \
    '# UNCP deliberately omitted: external packed-byte/exponent contract unresolved.\n' + \
    ''.join('%s\t%s\t%s\n' % row for row in MAPPING)


def specifications() -> dict:
    """Deliberately synthetic inputs; palettes are source data, not AE outputs."""
    rgba = {
        'R': ('FLOAT', [0, .125, .25, .375, .5, .625, .75, 1]),
        'G': ('FLOAT', [1, .75, .5, .25, 0, .125, .375, .625]),
        'B': ('FLOAT', [.25, .5, .75, 1, .625, .375, .125, 0]),
        'A': ('FLOAT', [1] * 8),
    }
    aux = dict(rgba)
    aux.update({
        'Z': ('FLOAT', [-1000, 0, 250, 1000, 2000, 3500, 5000, 7500]),
        'objectID': ('UINT', [0, 1, 255, 256, 32767, 32768, 65534, 65535]),
        'materialID': ('UINT', [0, 1, 2, 127, 128, 253, 254, 255]),
        'acxU': ('FLOAT', [0, .125, .25, .375, .5, .625, .875, 1]),
        'acxV': ('FLOAT', [1, .75, .5, .25, 0, .125, .375, .625]),
        'acxNX': ('FLOAT', [1, 0, 0, -1, 0, 0, .6, -.6]),
        'acxNY': ('FLOAT', [0, 1, 0, 0, -1, 0, .8, -.8]),
        'acxNZ': ('FLOAT', [0, 0, 1, 0, 0, -1, 0, 0]),
        'acxCoverage': ('FLOAT', [0, .125, .25, .5, .75, .875, 1, .375]),
        'acxBgR': ('UINT', [0, 1, 17, 64, 127, 128, 254, 255]),
        'acxBgG': ('UINT', [255, 128, 64, 32, 16, 8, 1, 0]),
        'acxBgB': ('UINT', [3, 7, 11, 19, 31, 63, 95, 191]),
    })
    specials = dict(rgba)
    specials['Z'] = ('FLOAT', [-math.inf, -1, -0.0, 0.0, 1, math.inf, math.nan, 10000])
    alpha = [.0, .25, .5, .75, 1, .5, .25, 0]
    transparent = dict(rgba)
    transparent['A'] = ('FLOAT', alpha)
    for name in ('R', 'G', 'B'):
        transparent[name] = ('FLOAT', [v * a for v, a in zip(rgba[name][1], alpha)])
    transparent['Z'] = ('FLOAT', [250, 500, 1000, 1500, 2000, 3000, 4500, 6000])
    return {'aux_known.exr': aux, 'rgba_only.exr': rgba,
            'depth_specials.exr': specials, 'alpha_depth.exr': transparent}


def palette_index(x: int, y: int) -> int:
    return ((x // 8) + 3 * (y // 8)) % 8


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def plane_bytes(kind: str, palette: list, width: int = WIDTH, height: int = HEIGHT) -> bytes:
    if kind not in ('UINT', 'FLOAT') or len(palette) != 8:
        raise ValueError('Exactly eight values of UINT or FLOAT required')
    if kind == 'UINT' and any(type(v) is not int or not 0 <= v <= 0xffffffff for v in palette):
        raise ValueError('UINT value out of range or not an integer')
    fmt = '<I' if kind == 'UINT' else '<f'
    encoded = [struct.pack(fmt, v) for v in palette]
    return b''.join(encoded[palette_index(x, y)] for y in range(height) for x in range(width))


def attr(name: str, kind: str, value: bytes) -> bytes:
    return name.encode('ascii') + b'\0' + kind.encode('ascii') + b'\0' + struct.pack('<i', len(value)) + value


def encode_exr(channels: dict) -> bytes:
    if not 1 <= len(channels) <= 32:
        raise ValueError('Unsupported channel count')
    names = sorted(channels)
    for name in names:
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,30}', name):
            raise ValueError('Unsupported channel name')
    planes = {n: plane_bytes(*channels[n]) for n in names}
    chlist = b''.join(n.encode('ascii') + b'\0' + struct.pack('<iB3xii',
        0 if channels[n][0] == 'UINT' else 2, 0, 1, 1) for n in names) + b'\0'
    window = struct.pack('<4i', 0, 0, WIDTH - 1, HEIGHT - 1)
    header = struct.pack('<II', MAGIC, 2) + b''.join([
        attr('channels', 'chlist', chlist), attr('compression', 'compression', b'\0'),
        attr('dataWindow', 'box2i', window), attr('displayWindow', 'box2i', window),
        attr('lineOrder', 'lineOrder', b'\0'), attr('pixelAspectRatio', 'float', struct.pack('<f', 1)),
        attr('screenWindowCenter', 'v2f', struct.pack('<ff', 0, 0)),
        attr('screenWindowWidth', 'float', struct.pack('<f', 1)),
        attr('acxBuild', 'string', BUILD.encode('ascii'))]) + b'\0'
    row_size = WIDTH * 4 * len(names)
    offset = len(header) + 8 * HEIGHT
    offsets = b''.join(struct.pack('<Q', offset + y * (8 + row_size)) for y in range(HEIGHT))
    chunks = b''.join(struct.pack('<ii', y, row_size) +
        b''.join(planes[n][y * WIDTH * 4:(y + 1) * WIDTH * 4] for n in names) for y in range(HEIGHT))
    return header + offsets + chunks


def inspect_exr(raw: bytes) -> dict:
    """Bounded, strict decoder for this subset. It does not use encode_exr."""
    if len(raw) > MAX_FILE or len(raw) < 16 or struct.unpack_from('<II', raw) != (MAGIC, 2):
        raise ValueError('Invalid size, magic, version or unsupported EXR flags')
    pos = 8
    def text(limit=31):
        nonlocal pos
        end = raw.find(b'\0', pos, min(len(raw), pos + limit + 1))
        if end < 0:
            raise ValueError('Unterminated or overlong header string')
        s = raw[pos:end].decode('ascii'); pos = end + 1
        return s
    attributes = {}
    while True:
        name = text()
        if not name:
            break
        kind = text()
        if not kind or name in attributes or pos + 4 > len(raw):
            raise ValueError('Duplicate/malformed attribute')
        size = struct.unpack_from('<i', raw, pos)[0]; pos += 4
        if size < 0 or size > 65536 or pos + size > len(raw):
            raise ValueError('Attribute length out of bounds')
        attributes[name] = (kind, raw[pos:pos + size]); pos += size
    required = {'channels': 'chlist', 'compression': 'compression', 'dataWindow': 'box2i',
                'displayWindow': 'box2i', 'lineOrder': 'lineOrder', 'pixelAspectRatio': 'float',
                'screenWindowCenter': 'v2f', 'screenWindowWidth': 'float'}
    if any(n not in attributes or attributes[n][0] != k for n, k in required.items()):
        raise ValueError('Missing required attribute or wrong type')
    if attributes['compression'][1] != b'\0' or attributes['lineOrder'][1] != b'\0':
        raise ValueError('Only uncompressed increasing scanlines supported')
    dw = attributes['dataWindow'][1]
    if len(dw) != 16 or dw != attributes['displayWindow'][1]:
        raise ValueError('Invalid or unequal data/display windows')
    x0, y0, x1, y1 = struct.unpack('<4i', dw)
    w, h = x1 + 1, y1 + 1
    if (x0, y0) != (0, 0) or not 1 <= w <= 512 or not 1 <= h <= 512:
        raise ValueError('Unsupported data window')
    chlist = attributes['channels'][1]; p = 0; kinds = {}
    while True:
        end = chlist.find(b'\0', p, min(len(chlist), p + 32))
        if end < 0:
            raise ValueError('Bad channel name')
        name = chlist[p:end].decode('ascii'); p = end + 1
        if not name:
            break
        if name in kinds or len(kinds) >= 32 or p + 16 > len(chlist):
            raise ValueError('Bad channel descriptor/count')
        typ, linear, reserved, xs, ys = struct.unpack_from('<iB3sii', chlist, p); p += 16
        if typ not in (0, 2) or linear not in (0, 1) or reserved != b'\0' * 3 or (xs, ys) != (1, 1):
            raise ValueError('Unsupported channel type/sampling')
        kinds[name] = 'UINT' if typ == 0 else 'FLOAT'
    if p != len(chlist) or not kinds or list(kinds) != sorted(kinds):
        raise ValueError('Bad channel-list termination/order')
    if pos + 8 * h > len(raw):
        raise ValueError('Truncated offset table')
    offsets = struct.unpack_from('<' + 'Q' * h, raw, pos)
    cursor = pos + 8 * h; size = w * 4 * len(kinds)
    planes = {n: bytearray() for n in kinds}
    for y, offset in enumerate(offsets):
        if offset != cursor or offset + 8 + size > len(raw):
            raise ValueError('Overlapping, truncated or noncontiguous chunks')
        if struct.unpack_from('<ii', raw, offset) != (y, size):
            raise ValueError('Wrong row coordinate or chunk size')
        cursor = offset + 8
        for n in kinds:
            planes[n].extend(raw[cursor:cursor + w * 4]); cursor += w * 4
    if cursor != len(raw):
        raise ValueError('Unexpected trailing data')
    return {'width': w, 'height': h, 'kinds': kinds,
            'planes': {n: bytes(b) for n, b in planes.items()}}


def json_value(v):
    return ('NaN' if math.isnan(v) else '+Infinity' if v > 0 else '-Infinity') if isinstance(v, float) and not math.isfinite(v) else v


def build_package(destination: Path, source_commit: str = 'LOCAL_UNCOMMITTED') -> dict:
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False)  # Never replace original evidence.
    files = []
    for filename, channels in specifications().items():
        raw = encode_exr(channels)
        parsed = inspect_exr(raw)
        for n, desc in channels.items():
            if parsed['planes'][n] != plane_bytes(*desc):
                raise ValueError('Generated input failed round-trip')
        with (destination / filename).open('xb') as f:
            f.write(raw)
        files.append({'name': filename, 'bytes': len(raw), 'sha256': sha(raw),
            'width': WIDTH, 'height': HEIGHT, 'channels': {
                n: {'storage': kind, 'palette': [json_value(v) for v in values],
                    'plane_sha256': sha(plane_bytes(kind, values))}
                for n, (kind, values) in sorted(channels.items())}})
    with (destination / MAP_NAME).open('x', encoding='utf-8', newline='\n') as f:
        f.write(MAP_TEXT)
    manifest = {'schema': 1, 'build': BUILD, 'source_commit': source_commit,
        'generator_sha256': sha(Path(__file__).read_bytes()),
        'file_byte_check': 'PASS', 'reference_reader': 'NOT_RUN',
        'ae_importer_qualification': 'NOT_RUN', 'native_effect_acceptance': 'NOT_RUN',
        'pattern': 'palette[(x//8 + 3*(y//8)) % 8]; row-major, origin top-left',
        'files': files, 'candidate_map': {'name': MAP_NAME, 'sha256': sha(MAP_TEXT.encode()),
            'installed': False, 'entries': [list(x) for x in MAPPING]},
        'uncovered': ['UNCP packed input contract', 'DPAA input semantics',
            'native datatype mismatch', 'AE output conversion', 'ROI callbacks', 'GPU/MFR execution'],
        'warnings': ['Synthetic input data, not measured Adobe outputs.',
            'Channel names and EXR storage types do not prove AE semantic tags.',
            'Candidate map is NOT installed; do not overwrite an existing map.',
            'alpha_depth RGB is premultiplied by the stored alpha.',
            'depth_specials must stay separate from ordinary finite comparisons.']}
    with (destination / 'manifest.json').open('x', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, allow_nan=False); f.write('\n')
    return manifest


def verify_package(destination: Path, reference: bool = False) -> dict:
    destination = Path(destination)
    manifest = json.loads((destination / 'manifest.json').read_text())
    expected = specifications()
    if manifest['build'] != BUILD or {r['name'] for r in manifest['files']} != set(expected):
        raise ValueError('Wrong build or file set')
    if len(manifest['files']) != len(expected):
        raise ValueError('Duplicate manifest entry')
    if (destination / MAP_NAME).read_bytes() != MAP_TEXT.encode():
        raise ValueError('Candidate map changed')
    results = []
    for record in manifest['files']:
        path = destination / record['name']
        if path.is_symlink() or path.stat().st_size > MAX_FILE:
            raise ValueError('Unexpected file path/size')
        raw = path.read_bytes(); parsed = inspect_exr(raw)
        if sha(raw) != record['sha256'] or len(raw) != record['bytes']:
            raise ValueError('File identity mismatch')
        channels = expected[record['name']]
        if parsed['kinds'] != {n: d[0] for n, d in channels.items()} or (parsed['width'], parsed['height']) != (WIDTH, HEIGHT):
            raise ValueError('Wrong channel layout')
        for n, desc in channels.items():
            plane = plane_bytes(*desc)
            if parsed['planes'][n] != plane or record['channels'][n]['plane_sha256'] != sha(plane):
                raise ValueError('Unexpected channel values')
        if reference:
            import OpenEXR
            import numpy as np
            # Header bounds were checked before allocating through the reference library.
            with OpenEXR.File(str(path), separate_channels=True) as exr:
                if len(exr.parts) != 1 or set(exr.channels()) != set(channels):
                    raise ValueError('Reference channel/part inventory differs')
                for n, (kind, values) in channels.items():
                    pixels = exr.channels()[n].pixels
                    dtype = np.dtype('uint32' if kind == 'UINT' else 'float32')
                    if pixels.shape != (HEIGHT, WIDTH) or pixels.dtype != dtype:
                        raise ValueError('Reference dtype/shape mismatch: ' + n)
                    decoded = np.ascontiguousarray(pixels.astype(dtype.newbyteorder('<'))).tobytes()
                    if decoded != plane_bytes(kind, values):
                        raise ValueError('Reference full-plane bytes mismatch: ' + n)
        results.append({'name': record['name'], 'status': 'PASS', 'channels': len(channels),
            'scalar_values_checked': WIDTH * HEIGHT * len(channels), 'sha256': sha(raw)})
    return {'build': BUILD, 'status': 'PASS', 'scope': 'FILE_INPUTS_ONLY_NOT_AE',
        'reference': importlib.metadata.version('OpenEXR') if reference else 'NOT_RUN',
        'ae_importer_qualification': 'NOT_RUN', 'files': results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build', 'verify'])
    parser.add_argument('directory', type=Path)
    parser.add_argument('--source-commit', default='LOCAL_UNCOMMITTED')
    parser.add_argument('--reference', action='store_true', help='Require independent OpenEXR reader; missing dependency fails')
    args = parser.parse_args()
    if args.command == 'build':
        build_package(args.directory, args.source_commit)
    print(json.dumps(verify_package(args.directory, args.reference), indent=2, allow_nan=False))

if __name__ == '__main__':
    main()
