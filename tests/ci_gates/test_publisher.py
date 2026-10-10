import io
import sys
from pathlib import Path
import tarfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.publish_ci_patch import verified_jobs, verify_archive


class PublisherTests(unittest.TestCase):
    def test_missing_duplicate_skipped_or_failed_job_is_not_success(self):
        required = {'portable-checks', 'macos-path-regression'}
        jobs = [{'name': n, 'status': 'completed', 'conclusion': 'success'} for n in required]
        verified_jobs(jobs, required)
        for bad in [jobs[:-1], jobs + [jobs[0]]]:
            with self.assertRaises(RuntimeError):
                verified_jobs(bad, required)
        for value in ['failure', 'skipped', 'cancelled', None]:
            with self.assertRaises(RuntimeError):
                verified_jobs([{**j, 'conclusion': value} for j in jobs], required)

    def test_modified_archive_or_mode_is_rejected(self):
        expected = {'README.md': (b'checked', 0o644)}
        for content, mode, good in [(b'checked', 0o644, True), (b'changed', 0o644, False), (b'checked', 0o755, False)]:
            out = io.BytesIO()
            with zipfile.ZipFile(out, 'w') as z:
                info = zipfile.ZipInfo('src/README.md')
                info.external_attr = mode << 16
                z.writestr(info, content)
            if good:
                verify_archive(out.getvalue(), 'zip', expected, 'src/')
            else:
                with self.assertRaises(RuntimeError):
                    verify_archive(out.getvalue(), 'zip', expected, 'src/')

    def test_tar_link_is_not_a_source_file(self):
        out = io.BytesIO()
        with tarfile.open(fileobj=out, mode='w:gz') as tar:
            info = tarfile.TarInfo('src/README.md')
            info.type, info.linkname = tarfile.SYMTYPE, '../README.md'
            tar.addfile(info)
        with self.assertRaises(RuntimeError):
            verify_archive(out.getvalue(), 'tar', {'README.md': (b'checked', 0o644)}, 'src/')


if __name__ == '__main__':
    unittest.main()
