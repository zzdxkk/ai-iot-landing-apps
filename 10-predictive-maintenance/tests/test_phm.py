import sys, os, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from phm import rms, peak, features, health_score, rul, monitor

class TestPHM(unittest.TestCase):
    def test_rms(self): self.assertAlmostEqual(rms([3,4]), 3.5355, places=3)
    def test_peak(self): self.assertEqual(peak([-5,2,3]), 5)
    def test_features(self):
        f = features([1,2,3,4]); self.assertIn("kurtosis", f)
    def test_health_monotonic(self):
        self.assertGreater(health_score({"rms":1.0}), health_score({"rms":3.0}))
    def test_rul(self): self.assertGreaterEqual(rul(80), rul(30))
    def test_monitor(self):
        r = monitor(steps=40, win=10); self.assertEqual(len(r), 31)

if __name__ == "__main__": unittest.main()
