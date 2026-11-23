import sys, os, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from modbus import crc16, build_rtu, parse_rtu, parse_tcp, RegisterMap

class TestModbus(unittest.TestCase):
    def test_crc_known(self):
        self.assertEqual(crc16(b"\x01\x03\x00\x00\x00\x02"), 0x0BC4)
        self.assertEqual(build_rtu(1, 3, 0, 2).hex(), "010300000002c40b")
    def test_build_parse(self):
        f = build_rtu(1, 3, 0, 2)
        p = parse_rtu(f)
        self.assertTrue(p["valid"]); self.assertEqual(p["slave"], 1)
    def test_corrupt(self):
        f = bytearray(build_rtu(1, 3, 0, 2)); f[-1] ^= 0xFF
        self.assertFalse(parse_rtu(bytes(f))["valid"])
    def test_tcp(self):
        frame = bytes.fromhex("00010006000301030000")
        self.assertEqual(parse_tcp(frame)["tx"], 1)
    def test_regmap(self):
        rm = RegisterMap({"t": (0, 0.1)})
        self.assertEqual(rm.decode({0: 250}), {"t": 25.0})

if __name__ == "__main__": unittest.main()
