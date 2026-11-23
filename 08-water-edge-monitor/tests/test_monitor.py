import sys, os, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from monitor import SensorSim, EWMA, LowPowerPolicy, report

class TestMonitor(unittest.TestCase):
    def test_sensor_range(self):
        s = SensorSim()
        self.assertTrue(all(20 < s.sample() < 40 for _ in range(20)))
    def test_ewma_detect(self):
        d = EWMA()
        for _ in range(10): d.update(25.0)
        self.assertTrue(d.update(60.0))
    def test_lowpower(self):
        self.assertAlmostEqual(LowPowerPolicy(600, 5).duty_cycle(), 5/600, places=5)
    def test_report(self):
        r = report("d", 25.5, False)
        self.assertFalse(r["alert"]); self.assertIn("payload_size", r)

if __name__ == "__main__": unittest.main()
