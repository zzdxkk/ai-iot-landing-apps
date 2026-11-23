import sys, os, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from evaluator import Case, evaluate, compare, token_f1
from report import render

class TestEval(unittest.TestCase):
    def test_exact(self):
        r = evaluate([Case("1", "q", "5天", "5天")])
        self.assertEqual(r["summary"]["exact"], 1.0)
    def test_f1_range(self):
        s = token_f1(Case("1", "q", "abcdef", "abc"))
        self.assertTrue(0 < s <= 1)
    def test_compare(self):
        a = evaluate([Case("1", "q", "5天", "错误")])
        b = evaluate([Case("1", "q", "5天", "5天")])
        c = compare(a, b, "exact")
        self.assertTrue(c["improved"]); self.assertEqual(c["delta"], 1.0)
    def test_report(self):
        r = evaluate([Case("1", "q", "5天", "5天")])
        self.assertIn("评测报告", render(r))

if __name__ == "__main__": unittest.main()
