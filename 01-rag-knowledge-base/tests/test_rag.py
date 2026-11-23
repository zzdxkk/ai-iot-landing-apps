import sys, os, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from rag import KnowledgeBase, answer, chunk, HashEmbedder

class TestRAG(unittest.TestCase):
    def setUp(self):
        self.kb = KnowledgeBase()
        self.kb.add("年假规则：入职满一年 5 天，满三年 10 天。", "手册.pdf")
        self.kb.add("报销需要发票，住宿标准 500 元。", "财务.pdf")
    def test_chunk_overlap(self):
        chunks = chunk("甲" * 100 + "乙" * 100, size=80, overlap=20)
        self.assertGreater(len(chunks), 2)
    def test_embed_normalized(self):
        v = HashEmbedder().embed("测试文本")
        self.assertAlmostEqual(sum(x*x for x in v), 1.0, places=5)
    def test_retrieve_relevant(self):
        hits = self.kb.retrieve("年假天数", top_k=2)
        self.assertEqual(len(hits), 2)
        self.assertTrue(any("年假" in t for _, t, _ in hits))
    def test_answer_has_citation(self):
        r = answer(self.kb, "年假几天")
        self.assertTrue(r["citations"])
        self.assertIn("source", r["citations"][0])

if __name__ == "__main__": unittest.main()
