"""Offline fixture regression tests. No After Effects API or pixel algorithm is run."""
import hashlib
import json
import math
import struct
import tempfile
import unittest
from pathlib import Path
import acx_fixture_candidate as fx


class FixtureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dest = Path(self.tmp.name) / 'candidate'

    def test_four_files_and_thirty_planes(self):
        fx.build_package(self.dest)
        r = fx.verify_package(self.dest)
        self.assertEqual(r['status'], 'PASS')
        self.assertEqual(r['reference'], 'NOT_RUN')
        self.assertEqual(sum(x['channels'] for x in r['files']), 30)
        self.assertEqual(sum(x['scalar_values_checked'] for x in r['files']), 61440)

    def test_repeatable_byte_generation(self):
        for channels in fx.specifications().values():
            self.assertEqual(fx.encode_exr(channels), fx.encode_exr(channels))

    def test_exact_known_id_boundaries(self):
        obj = fx.inspect_exr(fx.encode_exr(fx.specifications()['aux_known.exr']))
        values = struct.unpack('<' + 'I' * (fx.WIDTH * fx.HEIGHT), obj['planes']['objectID'])
        self.assertEqual([values[x * 8 + 4] for x in range(8)], [0, 1, 255, 256, 32767, 32768, 65534, 65535])

    def test_rgba_only_has_identical_color_and_no_auxiliary(self):
        specs = fx.specifications()
        a = fx.inspect_exr(fx.encode_exr(specs['aux_known.exr']))
        b = fx.inspect_exr(fx.encode_exr(specs['rgba_only.exr']))
        self.assertEqual(set(b['planes']), set('RGBA'))
        for n in 'RGBA':
            self.assertEqual(a['planes'][n], b['planes'][n])

    def test_special_depth_bits_are_preserved(self):
        p = fx.inspect_exr(fx.encode_exr(fx.specifications()['depth_specials.exr']))['planes']['Z']
        v = struct.unpack('<' + 'f' * (fx.WIDTH * fx.HEIGHT), p)
        picked = [v[x * 8 + 4] for x in range(8)]
        self.assertEqual(picked[0], -math.inf)
        self.assertEqual(picked[5], math.inf)
        self.assertTrue(math.isnan(picked[6]))
        self.assertEqual(struct.pack('<f', picked[2]), b'\0\0\0\x80')
        self.assertEqual(struct.pack('<f', picked[3]), b'\0\0\0\0')

    def test_transparent_input_is_premultiplied(self):
        p = fx.inspect_exr(fx.encode_exr(fx.specifications()['alpha_depth.exr']))['planes']
        vals = {n: struct.unpack('<' + 'f' * (fx.WIDTH * fx.HEIGHT), b) for n, b in p.items()}
        self.assertTrue(any(0 < a < 1 for a in vals['A']))
        for i, a in enumerate(vals['A']):
            if a == 0:
                self.assertEqual([vals[n][i] for n in 'RGB'], [0, 0, 0])

    def test_orientation_is_asymmetric(self):
        p = fx.inspect_exr(fx.encode_exr(fx.specifications()['aux_known.exr']))['planes']['Z']
        v = struct.unpack('<' + 'f' * (fx.WIDTH * fx.HEIGHT), p)
        self.assertNotEqual(v[4 * fx.WIDTH + 4], v[12 * fx.WIDTH + 4])
        self.assertNotEqual(v[4], v[fx.WIDTH - 5])

    def test_reject_existing_destination_without_changing_anything(self):
        self.dest.mkdir()
        keep = self.dest / 'existing-user-data'; keep.write_bytes(b'unchanged')
        with self.assertRaises(FileExistsError):
            fx.build_package(self.dest)
        self.assertEqual(keep.read_bytes(), b'unchanged')
        self.assertEqual(len(list(self.dest.iterdir())), 1)

    def test_bad_magic_version_and_truncation_rejected(self):
        raw = fx.encode_exr(fx.specifications()['aux_known.exr'])
        for broken in [b'', b'WRONG' + raw[5:], raw[:4] + b'\x02\x10\0\0' + raw[8:], raw[:-1], raw[:100]]:
            with self.subTest(size=len(broken)):
                with self.assertRaises(ValueError):
                    fx.inspect_exr(broken)

    def test_trailing_data_rejected(self):
        with self.assertRaises(ValueError):
            fx.inspect_exr(fx.encode_exr(fx.specifications()['rgba_only.exr']) + b'JUNK')

    def test_malformed_channel_sampling_rejected(self):
        raw = fx.encode_exr(fx.specifications()['rgba_only.exr'])
        # A is first in alphabetic channel list; its 16-byte descriptor follows A NUL.
        p = raw.index(b'A\0', raw.index(b'chlist\0')) + 2
        broken = raw[:p + 8] + struct.pack('<i', 2) + raw[p + 12:]
        with self.assertRaises(ValueError):
            fx.inspect_exr(broken)

    def test_duplicate_channel_rejected(self):
        raw = fx.encode_exr(fx.specifications()['rgba_only.exr'])
        p = raw.index(b'B\0', raw.index(b'chlist\0'))
        with self.assertRaises(ValueError):
            fx.inspect_exr(raw[:p] + b'A' + raw[p + 1:])

    def test_corrupted_payload_fails_identity(self):
        fx.build_package(self.dest)
        p = self.dest / 'aux_known.exr'; raw = p.read_bytes()
        p.write_bytes(raw[:-1] + bytes([raw[-1] ^ 1]))
        with self.assertRaises(ValueError):
            fx.verify_package(self.dest)

    def test_updated_hash_cannot_hide_wrong_values(self):
        fx.build_package(self.dest)
        p = self.dest / 'aux_known.exr'; raw = p.read_bytes()
        raw = raw[:-4] + struct.pack('<I', 12345); p.write_bytes(raw)
        m = self.dest / 'manifest.json'; data = json.loads(m.read_text())
        data['files'][0]['sha256'] = hashlib.sha256(raw).hexdigest(); m.write_text(json.dumps(data))
        with self.assertRaises(ValueError):
            fx.verify_package(self.dest)

    def test_manifest_path_injection_rejected(self):
        fx.build_package(self.dest)
        m = self.dest / 'manifest.json'; data = json.loads(m.read_text())
        data['files'][0]['name'] = '../outside.exr'; m.write_text(json.dumps(data))
        with self.assertRaises(ValueError):
            fx.verify_package(self.dest)

    def test_map_not_installed_no_uncp_claim(self):
        m = fx.build_package(self.dest)
        self.assertFalse(m['candidate_map']['installed'])
        self.assertEqual(len(m['candidate_map']['entries']), 7)
        self.assertNotIn('UNCP', [x[1] for x in m['candidate_map']['entries']])
        self.assertFalse((self.dest / 'OpenEXR_channel_map.txt').exists())
        self.assertEqual(m['native_effect_acceptance'], 'NOT_RUN')
        self.assertEqual(m['ae_importer_qualification'], 'NOT_RUN')

    def test_candidate_map_tampering_rejected(self):
        fx.build_package(self.dest)
        (self.dest / fx.MAP_NAME).write_text('anything')
        with self.assertRaises(ValueError):
            fx.verify_package(self.dest)

    def test_invalid_uint_input_rejected(self):
        for bad in [-1, 2**32, 1.5, True]:
            with self.assertRaises(ValueError):
                fx.plane_bytes('UINT', [bad] * 8)

    def test_unsafe_channel_names_rejected(self):
        for bad in ['', '../data', 'x\0y', 'a' * 32]:
            with self.assertRaises(ValueError):
                fx.encode_exr({bad: ('FLOAT', [0] * 8)})

    def test_no_nonstandard_json_floats(self):
        fx.build_package(self.dest)
        text = (self.dest / 'manifest.json').read_text()
        data = json.loads(text, parse_constant=lambda v: self.fail('Non-standard JSON: ' + v))
        p = [r for r in data['files'] if r['name'] == 'depth_specials.exr'][0]['channels']['Z']['palette']
        self.assertEqual(p[0], '-Infinity')
        self.assertEqual(p[6], 'NaN')


if __name__ == '__main__':
    unittest.main(verbosity=2)
