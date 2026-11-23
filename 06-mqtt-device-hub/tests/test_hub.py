import sys, os, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from hub import ThingModel, DeviceHub, RuleEngine

class TestHub(unittest.TestCase):
    def setUp(self):
        self.hub = DeviceHub(ThingModel("t", ["temp", "battery"]),
                             [("temp", ">", 30, "high")])
    def test_valid(self):
        self.assertTrue(self.hub.ingest("d1", {"temp": 20})["ok"])
    def test_invalid_field(self):
        r = self.hub.ingest("d1", {"oops": 1})
        self.assertFalse(r["ok"]); self.assertEqual(r["invalid"], ["oops"])
    def test_shadow(self):
        self.hub.ingest("d1", {"temp": 20}); self.hub.ingest("d1", {"battery": 88})
        self.assertEqual(self.hub.shadow.state["d1"], {"temp": 20, "battery": 88})
    def test_alert(self):
        r = self.hub.ingest("d1", {"temp": 40})
        self.assertEqual(r["record"]["alerts"][0]["level"], "high")

if __name__ == "__main__": unittest.main()
