#!/usr/bin/env python3
"""Offline comparison of a native auxiliary-channel readout against known EXRs.

This is NOT a native collector, installer, effect test, or evidence authenticator.
A self-reported capture is never independently authenticated by this program.
Only a separately pinned request can authorize a packet; legacy Mega JSON is refused.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import sys
import uuid
from pathlib import Path

import acx_fixture_candidate as fixture

BUILD = 'ACX-CHANNEL-GATE-20260930-01'
SCHEMA = 'ACX_NATIVE_CHANNEL_READOUT_V1'
MAX_JSON = 2 * 1024 * 1024
MAX_CHANNELS = 256
TAGS = tuple(row[1] for row in fixture.MAPPING)
FORMATS = {'FLT4': 'f', 'UST2': 'H', 'UBT1': 'B'}
UNTESTED = ['native_effect_output', 'DPAA', 'UNCP', 'datatype_mismatch_effect_behavior',
            'transparent_effect_output', 'ROI', 'CPU_GPU', 'MFR', 'cold_cache']


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha_ok(value) -> bool:
    return isinstance(value, str) and re.fullmatch(r'[0-9a-f]{64}', value) is not None


def exact_int(value, lo=0, hi=MAX_CHANNELS) -> bool:
    return type(value) is int and lo <= value <= hi


def text(value) -> bool:
    return isinstance(value, str) and 0 < len(value) <= 4096 and '\x00' not in value


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def read_json(path: Path) -> dict:
    require(not path.is_symlink(), 'Refuse symlink input')
    with path.open('rb') as f:
        raw = f.read(MAX_JSON + 1)
    require(len(raw) <= MAX_JSON, 'JSON exceeds bounded input size')
    def invalid_constant(value):
        raise ValueError('Nonstandard JSON constant: ' + value)
    obj = json.loads(raw.decode('utf-8-sig'), object_pairs_hook=_unique_object,
                     parse_constant=invalid_constant, parse_float=invalid_constant)
    require(isinstance(obj, dict), 'JSON root must be an object')
    return obj


def write_new(path: Path, value: dict) -> None:
    # Encode before opening; exclusive create never replaces input or previous evidence.
    raw = json.dumps(value, indent=2, allow_nan=False) + '\n'
    with path.open('x', encoding='utf-8', newline='\n') as f:
        f.write(raw)


def expected_assets() -> list[dict]:
    assets = []
    for name, planes in fixture.specifications().items():
        mappings = fixture.MAPPING if name in ('aux_known.exr', 'rgba_only.exr') else fixture.MAPPING[:1]
        assets.append({'name': name, 'sha256': digest(fixture.encode_exr(planes)),
                       'queries': [{'tag': tag, 'dtype': dtype, 'dimension': len(names.split('|')),
                                    'planes': names.split('|'), 'expect_present': name != 'rgba_only.exr'}
                                   for names, tag, dtype in mappings]})
    return assets


def make_request(collector_sha256: str, *, run_id: str | None = None,
                 synthetic: bool = False) -> dict:
    require(sha_ok(collector_sha256), 'Pin the built collector SHA-256 first')
    run_id = run_id or str(uuid.uuid4())
    require(isinstance(run_id, str) and re.fullmatch(r'[A-Za-z0-9_-]{8,96}', run_id), 'Invalid run ID')
    return {'schema': SCHEMA, 'gate_build': BUILD, 'run_id': run_id,
            'collector_sha256': collector_sha256, 'synthetic': synthetic,
            'target_host': {'ae_build': '25.6x101', 'architecture': 'arm64', 'os_family': 'macOS'},
            'fixture_build': fixture.BUILD,
            'fixture_generator_sha256': digest(Path(fixture.__file__).read_bytes()),
            'coordinate_contract': '64x32; top-left; row-major; full resolution; time 0/1',
            'assets': expected_assets()}


def expected_bytes(asset: dict, query: dict) -> bytes:
    planes = fixture.specifications()[asset['name']]
    fmt = '<' + FORMATS[query['dtype']] * query['dimension']
    palette = [struct.pack(fmt, *(planes[n][1][i] for n in query['planes'])) for i in range(8)]
    return b''.join(palette[fixture.palette_index(x, y)]
                    for y in range(fixture.HEIGHT) for x in range(fixture.WIDTH))


def check_descriptor(desc: dict) -> tuple:
    require(isinstance(desc, dict), 'Missing descriptor')
    for key in ('tag', 'dtype'):
        require(isinstance(desc.get(key), str) and re.fullmatch(r'[\x20-\x7e]{4}', desc[key]), 'Invalid FourCC')
    require(exact_int(desc.get('dimension'), 1, 32) and text(desc.get('name')), 'Bad descriptor dimension/name')
    return desc['tag'], desc['dtype'], desc['dimension'], desc['name']


def index_by(rows, key: str, limit: int) -> dict:
    require(isinstance(rows, list) and len(rows) <= limit, 'Invalid/oversized record list')
    result = {}
    for row in rows:
        require(isinstance(row, dict) and isinstance(row.get(key), (str, int)), 'Invalid record key')
        require(row[key] not in result, 'Duplicate record: ' + str(row[key]))
        result[row[key]] = row
    return result


def validate_chunk(chunk: dict, query: dict) -> bytes:
    require(isinstance(chunk, dict), 'Missing raw chunk')
    require(chunk.get('dtype') == query['dtype'] and
            type(chunk.get('dimension')) is int and chunk['dimension'] == query['dimension'],
            'Checkout datatype/dimension differs from descriptor request')
    require(type(chunk.get('width')) is int and type(chunk.get('height')) is int and
            (chunk['width'], chunk['height']) == (fixture.WIDTH, fixture.HEIGHT), 'Wrong chunk dimensions')
    require(chunk.get('encoding') == 'interleaved-le-hex-no-padding', 'Unrecognized canonical encoding')
    require(chunk.get('source_byte_order') == 'little', 'Only little-endian host readout covered')
    require(chunk.get('origin') == [0, 0] and chunk.get('scale') == [1, 1] and
            all(type(v) is int for v in chunk['origin'] + chunk['scale']), 'Wrong readout origin/scale')
    row_bytes = fixture.WIDTH * query['dimension'] * struct.calcsize(FORMATS[query['dtype']])
    require(exact_int(chunk.get('host_row_bytes'), row_bytes, 1024 * 1024), 'Invalid host row stride')
    raw_hex = chunk.get('data_hex')
    size = row_bytes * fixture.HEIGHT
    require(isinstance(raw_hex, str) and len(raw_hex) == size * 2 and
            re.fullmatch(r'[0-9a-f]+', raw_hex), 'Raw payload missing, wrong length or invalid hex')
    raw = bytes.fromhex(raw_hex)
    require(sha_ok(chunk.get('sha256')) and digest(raw) == chunk['sha256'], 'Raw chunk hash mismatch')
    return raw


def validate_query(asset: dict, wanted: dict, observed: dict, descriptors: list) -> dict:
    result = {'asset': asset['name'], 'tag': wanted['tag'], 'expected_present': wanted['expect_present']}
    require(exact_int(observed.get('query_error'), -2**31, 2**31 - 1), 'Missing query error code')
    # Lease cleanup is checked even for a blocked descriptor or a failed query.
    checkout = observed.get('checkout_error')
    if checkout is not None:
        require(exact_int(checkout, -2**31, 2**31 - 1), 'Invalid checkout result')
        if checkout == 0:
            require(type(observed.get('checkin_error')) is int and observed['checkin_error'] == 0,
                    'Successful checkout must have a successful checkin')
        else:
            require(observed.get('chunk') is None and observed.get('checkin_error') is None,
                    'Failed checkout must not claim data or a checkin')
    else:
        require(observed.get('chunk') is None and observed.get('checkin_error') is None,
                'Missing checkout result cannot carry data or a checkin')
    if observed['query_error'] != 0:
        return dict(result, status='BLOCKED', reason='Typed channel query returned an error')
    require(type(observed.get('found')) is bool, 'found must be a boolean, not a status or a number')
    matches = [d for d in descriptors if d['tag'] == wanted['tag']]
    if not observed['found']:
        require(not matches, 'Typed not-found contradicts indexed inventory')
        require(observed.get('descriptor') is None and observed.get('chunk') is None and
                observed.get('checkout_error') is None and observed.get('checkin_error') is None,
                'A not-found result must not claim a checkout or contain data')
        return dict(result, status='BLOCKED' if wanted['expect_present'] else 'MATCHED_ABSENCE',
                    reason='Semantic channel not exposed in this capture')
    require(len(matches) == 1, 'Missing or ambiguous semantic tag in indexed inventory')
    signature = check_descriptor(observed.get('descriptor'))
    require(signature == check_descriptor(matches[0]), 'Typed descriptor differs from indexed inventory')
    if not wanted['expect_present']:
        return dict(result, status='MISMATCH', reason='RGBA-only control exposes an unexpected semantic channel')
    if signature[:3] != (wanted['tag'], wanted['dtype'], wanted['dimension']):
        return dict(result, status='BLOCKED', reason='Importer descriptor is incompatible with planned channel contract',
                    actual_descriptor=observed['descriptor'])
    require(observed.get('requested_dtype') == wanted['dtype'], 'Do not coerce a different descriptor to make the test pass')
    require(exact_int(observed.get('checkout_error'), -2**31, 2**31 - 1), 'Missing checkout result')
    if observed['checkout_error'] != 0:
        return dict(result, status='BLOCKED', reason='Raw channel checkout failed')
    require(type(observed.get('checkin_error')) is int and observed['checkin_error'] == 0,
            'Successful checkout must have a successful checkin')
    raw = validate_chunk(observed.get('chunk'), wanted)
    expected = expected_bytes(asset, wanted)
    result.update(actual_sha256=digest(raw), expected_sha256=digest(expected), bytes_checked=len(raw))
    if raw == expected:
        return dict(result, status='MATCHED_BYTES')
    first = next(i for i, (a, b) in enumerate(zip(raw, expected)) if a != b)
    size = struct.calcsize(FORMATS[wanted['dtype']])
    pixel, component = divmod(first // size, wanted['dimension'])
    return dict(result, status='MISMATCH', reason='Canonical raw bytes differ; no effect behavior is inferred',
                first_difference={'x': pixel % fixture.WIDTH, 'y': pixel // fixture.WIDTH,
                                  'component': component, 'byte_offset': first})


def qualify(request: dict, capture: dict, *, allow_synthetic: bool = False) -> dict:
    """Validate content, not authenticity. Native-effect acceptance is always NOT_RUN."""
    require(request.get('schema') == SCHEMA and capture.get('schema') == SCHEMA, 'Wrong schema; old Mega is not a native readout')
    require(type(request.get('synthetic')) is bool, 'Missing evidence mode')
    synthetic = request['synthetic']
    require(not synthetic or allow_synthetic, 'Synthetic evidence is forbidden in host mode')
    require(request == make_request(request.get('collector_sha256'), run_id=request.get('run_id'), synthetic=synthetic),
            'Request is stale, incomplete or changed')
    for key in ('run_id', 'collector_sha256', 'fixture_build', 'fixture_generator_sha256'):
        require(capture.get(key) == request[key], 'Capture identity mismatch: ' + key)
    require(capture.get('evidence_origin') == ('SYNTHETIC_TEST' if synthetic else 'NATIVE_HOST_CAPTURE'), 'Wrong evidence origin')
    host = capture.get('host')
    require(isinstance(host, dict) and text(host.get('ae_build')) and text(host.get('os')) and
            host.get('architecture') in ('arm64', 'x86_64'), 'Missing host identity')
    require(all(host.get(k) == v for k, v in request['target_host'].items()), 'Wrong target AE build/architecture')
    importer = capture.get('importer')
    require(isinstance(importer, dict) and text(importer.get('loaded_module_path')) and
            text(importer.get('version')) and sha_ok(importer.get('sha256')), 'Missing loaded importer identity')
    mapping = importer.get('mapping')
    require(isinstance(mapping, dict) and mapping.get('state') in ('PRESENT', 'ABSENT'), 'Unknown mapping state')
    require(text(mapping.get('path')), 'Missing inspected map path')
    if mapping['state'] == 'PRESENT':
        require(isinstance(mapping.get('text'), str) and len(mapping['text']) <= 65536 and
                sha_ok(mapping.get('sha256')) and digest(mapping['text'].encode('utf-8')) == mapping['sha256'],
                'Map snapshot hash mismatch')
    else:
        require(mapping.get('text') is None and mapping.get('sha256') is None, 'Absent map cannot contain data')
    require(capture.get('cleanup_errors') == [] and type(capture.get('suite_release_error')) is int and
            capture['suite_release_error'] == 0, 'Incomplete native cleanup')
    assets = index_by(capture.get('assets'), 'name', 4)
    require(set(assets) == {x['name'] for x in request['assets']}, 'Incomplete/extra input suite')
    results = []
    for wanted in request['assets']:
        observed = assets[wanted['name']]
        require(observed.get('file_sha256_before') == wanted['sha256'] == observed.get('file_sha256_after'),
                'Wrong or changed input footage')
        require(observed.get('source_kind') == 'FOOTAGE' and observed.get('source_is_proxy') is False and
                observed.get('param_index') == 0 and type(observed.get('param_index')) is int,
                'Requires direct input footage, no precomp or proxy')
        tm = observed.get('time')
        require(isinstance(tm, dict) and tm == {'value': 0, 'scale': 1} and
                all(type(v) is int for v in tm.values()), 'Unexpected capture time')
        require(type(observed.get('channel_count_error')) is int and observed['channel_count_error'] == 0,
                'Channel enumeration failed')
        count = observed.get('channel_count')
        require(exact_int(count), 'Invalid channel count')
        indexed = index_by(observed.get('indexed'), 'index', MAX_CHANNELS)
        require(all(type(i) is int for i in indexed) and set(indexed) == set(range(count)), 'Incomplete indexed inventory')
        descriptors = []
        for i in range(count):
            row = indexed[i]
            require(type(row.get('error')) is int and row['error'] == 0 and row.get('found') is True,
                    'Indexed descriptor lookup failed')
            check_descriptor(row.get('descriptor'))
            descriptors.append(row['descriptor'])
        queries = index_by(observed.get('typed'), 'tag', 7)
        require(set(queries) == {q['tag'] for q in wanted['queries']}, 'Missing or extra typed queries')
        for query in wanted['queries']:
            results.append(validate_query(wanted, query, queries[query['tag']], descriptors))
    counts = {status: sum(r['status'] == status for r in results)
              for status in ('MATCHED_BYTES', 'MATCHED_ABSENCE', 'BLOCKED', 'MISMATCH')}
    status = 'MISMATCH' if counts['MISMATCH'] else 'PARTIAL' if counts['BLOCKED'] else 'MATCHED_CAPTURE_CONTENT'
    return {'build': BUILD, 'run_id': request['run_id'], 'status': status,
            'scope': 'SYNTHETIC_VALIDATOR_TEST' if synthetic else 'REPORTED_RAW_CHANNEL_CONTENT_ONLY',
            'authenticity': 'NOT_AUTHENTICATED', 'native_effect_acceptance': 'NOT_RUN',
            'host': host, 'importer': importer, 'collector_sha256': request['collector_sha256'],
            'untested': UNTESTED, 'counts': counts, 'results': results}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    plan = sub.add_parser('request', help='Write a NEW request only after a native collector binary is pinned')
    plan.add_argument('output', type=Path)
    plan.add_argument('--collector-sha256', required=True)
    check = sub.add_parser('verify', help='Verify a native capture; refuses synthetic evidence')
    check.add_argument('request', type=Path)
    check.add_argument('capture', type=Path)
    check.add_argument('output', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'request':
            write_new(args.output, make_request(args.collector_sha256))
            return 0
        result = qualify(read_json(args.request), read_json(args.capture))
        write_new(args.output, result)
        return 0 if result['status'] == 'MATCHED_CAPTURE_CONTENT' else 2
    except (ValueError, OSError, KeyError, TypeError, OverflowError, RecursionError) as exc:
        print('ACX channel gate ERROR: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
