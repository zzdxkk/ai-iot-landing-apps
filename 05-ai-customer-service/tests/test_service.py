import sys, os, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from service import handle, intent, slots

class TestService(unittest.TestCase):
    def test_intent(self):
        self.assertEqual(intent("发票怎么开"), "发票")
    def test_slots(self):
        s = slots("订单号 ABC123456 电话 13800138000")
        self.assertEqual(s["phone"], "13800138000")
    def test_ticket_reply(self):
        t = handle("我要退款，订单号 ABC123456")
        self.assertIn("退款", t.reply)
        self.assertFalse(t.need_human)
    def test_transfer_human(self):
        self.assertTrue(handle("随便问问").need_human)

if __name__ == "__main__": unittest.main()
