import sys, os, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ota import chunk_firmware, verify, version_gt, OTAJob, canary

class TestOTA(unittest.TestCase):
    def test_chunk(self):
        self.assertEqual(len(chunk_firmware(b"a"*500, 256)), 2)
    def test_verify(self):
        d = b"abc"*50
        job = OTAJob("v1", d)
        self.assertTrue(verify(d, job.checksums))
    def test_corrupt_rejected(self):
        d = b"abc"*50; job = OTAJob("v1", d)
        self.assertFalse(job.deliver(0, job.chunks[0], corrupt=True))
    def test_version(self):
        self.assertTrue(version_gt("v1.2.0", "v1.1.9"))
        self.assertFalse(version_gt("v1.0.0", "v1.0.1"))
    def test_resume(self):
        d = b"x"*600; job = OTAJob("v1", d)
        for i in range(2): job.deliver(i, job.chunks[i])
        self.assertAlmostEqual(job.progress(), 2/len(job.chunks), places=2)
    def test_canary(self):
        self.assertEqual(len(canary([str(i) for i in range(10)])), 2)

if __name__ == "__main__": unittest.main()
