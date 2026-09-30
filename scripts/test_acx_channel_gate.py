"""Synthetic protocol tests, NOT native capture or Adobe effect evidence."""
import copy
import hashlib
import json
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import acx_channel_gate as gate


def synthetic_packet():
    request = gate.make_request('1' * 64, run_id='synthetic-test-01', synthetic=True)
    capture = {key: copy.deepcopy(request[key]) for key in
               ('schema', 'run_id', 'collector_sha256', 'fixture_build', 'fixture_generator_sha256')}
    capture.update(evidence_origin='SYNTHETIC_TEST',
                   host={'ae_build': '25.6x101', 'os': 'MOCK', 'architecture': 'arm64', 'os_family': 'macOS'},
                   importer={'loaded_module_path': '/mock/OpenEXR', 'version': 'MOCK', 'sha256': '2' * 64,
                             'mapping': {'state': 'ABSENT', 'path': '/mock/OpenEXR_channel_map.txt'}},
                   cleanup_errors=[], suite_release_error=0, assets=[])
    for asset in request['assets']:
        item = {'name': asset['name'], 'source_kind': 'FOOTAGE', 'source_is_proxy': False,
                'param_index': 0, 'time': {'value': 0, 'scale': 1}, 'channel_count_error': 0,
                'file_sha256_before': asset['sha256'], 'file_sha256_after': asset['sha256'],
                'channel_count': len(asset['queries']) if asset['name'] != 'rgba_only.exr' else 0,
                'indexed': [], 'typed': []}
        capture['assets'].append(item)
        for i, query in enumerate(asset['queries']):
            row = {'tag': query['tag'], 'query_error': 0, 'found': query['expect_present']}
            item['typed'].append(row)
            if not query['expect_present']:
                continue
            desc = {'tag': query['tag'], 'dtype': query['dtype'], 'dimension': query['dimension'],
                    'name': '|'.join(query['planes'])}
            item['indexed'].append({'index': i, 'error': 0, 'found': True, 'descriptor': desc})
            raw = gate.expected_bytes(asset, query)
            row.update(descriptor=copy.deepcopy(desc), requested_dtype=query['dtype'],
                       checkout_error=0, checkin_error=0,
                       chunk={'dtype': query['dtype'], 'dimension': query['dimension'],
                              'width': 64, 'height': 32, 'origin': [0, 0], 'scale': [1, 1],
                              'encoding': 'interleaved-le-hex-no-padding', 'source_byte_order': 'little',
                              'host_row_bytes': len(raw) // 32, 'data_hex': raw.hex(),
                              'sha256': hashlib.sha256(raw).hexdigest()})
    return request, capture


class ChannelGateTests(unittest.TestCase):
    def setUp(self):
        self.request, self.capture = synthetic_packet()
        self.asset = self.capture['assets'][0]
        self.row = self.asset['typed'][0]

    def verify(self):
        return gate.qualify(self.request, self.capture, allow_synthetic=True)

    def rejected(self):
        with self.assertRaises((ValueError, TypeError, KeyError)):
            self.verify()

    def test_full_packet_matches_only_synthetic_content(self):
        result = self.verify()
        self.assertEqual(result['status'], 'MATCHED_CAPTURE_CONTENT')
        self.assertEqual(result['scope'], 'SYNTHETIC_VALIDATOR_TEST')
        self.assertEqual(result['authenticity'], 'NOT_AUTHENTICATED')
        self.assertEqual(result['native_effect_acceptance'], 'NOT_RUN')
        self.assertEqual(result['counts'], {'MATCHED_BYTES': 9, 'MATCHED_ABSENCE': 7, 'BLOCKED': 0, 'MISMATCH': 0})
        self.assertNotIn('"PASS"', json.dumps(result))

    def test_synthetic_rejected_by_normal_api(self):
        with self.assertRaisesRegex(ValueError, 'Synthetic'):
            gate.qualify(self.request, self.capture)

    def test_explicit_synthetic_origin_not_accepted_as_native(self):
        self.request['synthetic'] = False
        self.rejected()

    def test_legacy_mega_collected_rejected(self):
        with self.assertRaisesRegex(ValueError, 'schema'):
            gate.qualify(self.request, {'schema': 3, 'status': 'COLLECTED'}, allow_synthetic=True)

    def test_fresh_run_and_binary_and_fixture_binding(self):
        for key in ('run_id', 'collector_sha256', 'fixture_build', 'fixture_generator_sha256'):
            with self.subTest(key=key):
                request, capture = synthetic_packet()
                capture[key] = 'wrong'
                with self.assertRaises(ValueError):
                    gate.qualify(request, capture, allow_synthetic=True)

    def test_request_cannot_drop_suite_or_change_expected_value(self):
        for key in ('assets', 'coordinate_contract', 'gate_build'):
            with self.subTest(key=key):
                request, capture = synthetic_packet()
                request[key] = [] if key == 'assets' else 'changed'
                with self.assertRaises(ValueError):
                    gate.qualify(request, capture, allow_synthetic=True)

    def test_exact_original_input_hashes(self):
        expected = {'aux_known.exr': '73936b5abfc437d1a4572c39adf218cc7778c0de0b428b7052f84310fb3cd882',
                    'rgba_only.exr': 'be6952b719b42699ad1b74d1f821bb4b2f6bb4043b7adf2fe76698a225ad5627',
                    'depth_specials.exr': 'ca9544c448fbb88ad704c07238050ea888df8e3d3730f338bc9b7ac33208230c',
                    'alpha_depth.exr': '807f53cc78fb1f251fedb96118c02185dbe0fcbe1100a1fe41fa18515e7ad7f2'}
        self.assertEqual({a['name']: a['sha256'] for a in self.request['assets']}, expected)

    def test_wrong_changed_or_proxy_precomp_input_rejected(self):
        for key, value in [('file_sha256_before', '0' * 64), ('file_sha256_after', '0' * 64),
                           ('source_is_proxy', True), ('source_kind', 'PRECOMP'), ('param_index', 1)]:
            with self.subTest(key=key):
                original = self.asset[key]; self.asset[key] = value
                self.rejected(); self.asset[key] = original

    def test_missing_host_or_loaded_importer_identity_rejected(self):
        for root, key in [('host', 'ae_build'), ('host', 'architecture'), ('importer', 'sha256'), ('importer', 'loaded_module_path')]:
            with self.subTest(key=key):
                value = self.capture[root].pop(key); self.rejected(); self.capture[root][key] = value

    def test_map_snapshot_hash_checked_and_absence_distinct(self):
        raw = '# synthetic mapping\nZ DPTH FLT4\n'
        mapping = self.capture['importer']['mapping']
        mapping.update(state='PRESENT', text=raw, sha256=gate.digest(raw.encode()))
        self.assertEqual(self.verify()['status'], 'MATCHED_CAPTURE_CONTENT')
        mapping['text'] += 'changed'; self.rejected()
        mapping['state'] = 'ABSENT'; self.rejected()

    def test_missing_input_or_duplicate_suite_rejected(self):
        self.capture['assets'].pop(); self.rejected()
        self.capture['assets'].append(self.capture['assets'][0]); self.rejected()

    def test_duplicate_or_missing_queries_rejected(self):
        self.asset['typed'][1] = self.asset['typed'][0]; self.rejected()
        self.asset['typed'].pop(); self.rejected()

    def test_incomplete_indexed_inventory_rejected(self):
        self.asset['indexed'].pop(); self.rejected()

    def test_enumeration_error_not_treated_as_missing(self):
        self.asset['channel_count_error'] = 17; self.rejected()

    def test_indexed_error_or_not_found_rejected(self):
        self.asset['indexed'][0]['error'] = 3; self.rejected()
        self.asset['indexed'][0]['error'] = 0; self.asset['indexed'][0]['found'] = False; self.rejected()

    def test_not_found_does_not_establish_error_behavior(self):
        self.row.clear(); self.row.update(tag='DPTH', query_error=0, found=False)
        self.asset['indexed'][0]['descriptor']['tag'] = 'UNKN'
        result = self.verify()
        self.assertEqual(result['status'], 'PARTIAL')
        self.assertEqual(result['results'][0]['status'], 'BLOCKED')
        self.assertEqual(result['native_effect_acceptance'], 'NOT_RUN')

    def test_not_found_with_inventory_or_payload_contradiction_rejected(self):
        self.row['found'] = False; self.rejected()
        self.asset['indexed'][0]['descriptor']['tag'] = 'UNKN'; self.rejected()

    def test_typing_readback_not_enough_without_raw_chunk(self):
        self.row.pop('chunk'); self.rejected()

    def test_wrong_descriptor_type_blocks_without_coercion(self):
        for desc in (self.row['descriptor'], self.asset['indexed'][0]['descriptor']):
            desc['dtype'] = 'UST2'
        result = self.verify()
        self.assertEqual(result['status'], 'PARTIAL')
        self.assertEqual(result['results'][0]['status'], 'BLOCKED')

    def test_wrong_descriptor_dimensions_block(self):
        for desc in (self.row['descriptor'], self.asset['indexed'][0]['descriptor']):
            desc['dimension'] = 2
        self.assertEqual(self.verify()['results'][0]['status'], 'BLOCKED')

    def test_typed_descriptor_must_match_complete_index(self):
        self.row['descriptor']['name'] = 'different-channel'; self.rejected()

    def test_duplicate_semantic_tags_rejected(self):
        self.asset['indexed'][1]['descriptor'] = copy.deepcopy(self.row['descriptor']); self.rejected()

    def test_query_and_checkout_errors_block_not_pass(self):
        for key in ('query_error', 'checkout_error'):
            original = copy.deepcopy(self.row); self.row[key] = 8
            if key == 'checkout_error':
                self.row.pop('chunk'); self.row.pop('checkin_error')
            self.assertEqual(self.verify()['results'][0]['status'], 'BLOCKED')
            self.row.clear(); self.row.update(original)

    def test_checkin_and_suite_release_required(self):
        self.row['checkin_error'] = None; self.rejected()
        self.row['checkin_error'] = 0; self.capture['suite_release_error'] = 9; self.rejected()

    def test_cleanup_failure_rejects_packet(self):
        self.capture['cleanup_errors'] = ['native lease']; self.rejected()

    def test_wrong_byte_order_stride_dimensions_and_encoding_rejected(self):
        for key, value in [('source_byte_order', 'big'), ('host_row_bytes', 1), ('width', 63),
                           ('height', 31), ('scale', [2, 2]), ('origin', [1, 0]),
                           ('encoding', 'sampleImage'), ('dtype', 'UBT1'), ('dimension', 2)]:
            with self.subTest(key=key):
                original = self.row['chunk'][key]; self.row['chunk'][key] = value
                self.rejected(); self.row['chunk'][key] = original

    def test_host_padding_allowed_canonical_bytes_unchanged(self):
        self.row['chunk']['host_row_bytes'] += 64
        self.assertEqual(self.verify()['status'], 'MATCHED_CAPTURE_CONTENT')

    def test_short_invalid_or_wrong_hash_payload_rejected(self):
        for key, value in [('data_hex', '00'), ('data_hex', 'zz' * 8192), ('sha256', '0' * 64)]:
            original = self.row['chunk'][key]; self.row['chunk'][key] = value
            self.rejected(); self.row['chunk'][key] = original

    def test_altered_pixels_with_updated_hash_still_mismatch(self):
        chunk = self.row['chunk']; raw = bytearray.fromhex(chunk['data_hex']); raw[4] ^= 1
        chunk.update(data_hex=raw.hex(), sha256=gate.digest(raw))
        result = self.verify()
        self.assertEqual(result['status'], 'MISMATCH')
        self.assertEqual(result['results'][0]['first_difference'], {'x': 1, 'y': 0, 'component': 0, 'byte_offset': 4})

    def test_nonconstant_id_boundaries_independent_sentinels(self):
        raw = bytes.fromhex(self.asset['typed'][1]['chunk']['data_hex'])
        self.assertEqual([struct.unpack_from('<H', raw, x * 8 * 2)[0] for x in range(8)],
                         [0, 1, 255, 256, 32767, 32768, 65534, 65535])

    def test_uv_components_order_is_discriminating(self):
        chunk = self.asset['typed'][2]['chunk']; raw = bytearray.fromhex(chunk['data_hex'])
        for offset in range(0, len(raw), 8):
            raw[offset:offset+8] = raw[offset+4:offset+8] + raw[offset:offset+4]
        chunk.update(data_hex=raw.hex(), sha256=gate.digest(raw))
        self.assertEqual(self.verify()['results'][2]['status'], 'MISMATCH')

    def test_special_float_bits_preserved_not_silently_normalized(self):
        row = self.capture['assets'][2]['typed'][0]; chunk = row['chunk']; raw = bytearray.fromhex(chunk['data_hex'])
        self.assertEqual(struct.unpack_from('<I', raw, 16 * 4)[0], 0x80000000)
        self.assertEqual(struct.unpack_from('<I', raw, 24 * 4)[0], 0)
        raw[16*4:16*4+4] = b'\0' * 4
        chunk.update(data_hex=raw.hex(), sha256=gate.digest(raw))
        self.assertEqual(self.verify()['results'][-2]['status'], 'MISMATCH')

    def test_uncovered_families_always_remain_open(self):
        result = self.verify()
        for key in ('UNCP', 'DPAA', 'MFR', 'ROI', 'native_effect_output'):
            self.assertIn(key, result['untested'])

    def test_exclusive_output_preserves_existing_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'report.json'; path.write_text('ORIGINAL')
            with self.assertRaises(FileExistsError): gate.write_new(path, self.verify())
            self.assertEqual(path.read_text(), 'ORIGINAL')

    def test_bounded_json_duplicate_keys_nan_and_symlinks(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'input.json'
            for raw in ('{"a":1,"a":2}', '{"a":NaN}', '{"a":1e999}', '[' + '0,' * (gate.MAX_JSON // 2) + '0]'):
                path.write_text(raw)
                with self.assertRaises(ValueError): gate.read_json(path)
            link = Path(tmp) / 'link'; link.symlink_to(path)
            with self.assertRaises(ValueError): gate.read_json(link)

    def test_cli_refuses_synthetic_no_output_created(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); r = root / 'request.json'; c = root / 'capture.json'; out = root / 'result.json'
            gate.write_new(r, self.request); gate.write_new(c, self.capture)
            proc = subprocess.run([sys.executable, gate.__file__, 'verify', str(r), str(c), str(out)],
                                  capture_output=True, text=True, timeout=10)
            self.assertEqual(proc.returncode, 1); self.assertFalse(out.exists())
            self.assertIn('Synthetic', proc.stderr)

    def test_wrong_host_target_rejected(self):
        self.capture['host']['ae_build'] = 'OTHER'; self.rejected()

    def test_boolean_time_and_coordinates_rejected(self):
        self.asset['time']['value'] = False; self.rejected()
        self.asset['time']['value'] = 0
        self.row['chunk']['origin'] = [False, 0]; self.rejected()

    def test_cleanup_not_hidden_behind_incompatible_descriptor(self):
        for desc in (self.row['descriptor'], self.asset['indexed'][0]['descriptor']):
            desc['dtype'] = 'UBT1'
        self.row['checkin_error'] = 17; self.rejected()

    def test_failed_checkout_cannot_claim_payload(self):
        self.row['checkout_error'] = 1; self.rejected()

    def test_request_needs_digest_and_nonce(self):
        for value in ('', 'bad', 'z' * 64):
            with self.assertRaises(ValueError): gate.make_request(value)
        with self.assertRaises(ValueError): gate.make_request('1' * 64, run_id='x')
        self.assertNotEqual(gate.make_request('1' * 64)['run_id'], gate.make_request('1' * 64)['run_id'])


if __name__ == '__main__':
    unittest.main()
