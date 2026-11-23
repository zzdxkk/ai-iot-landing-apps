import sys, os, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from pipeline import Task, render_prompt, moderate, run, mock_generate

class TestPipeline(unittest.TestCase):
    def test_template(self):
        self.assertEqual(render_prompt("hi {name}", name="Ada"), "hi Ada")
    def test_moderate_pass(self):
        self.assertTrue(moderate("正常文案")["pass"])
    def test_moderate_block(self):
        self.assertFalse(moderate("含诈骗内容")["pass"])
    def test_run(self):
        out = run([Task("1", "写一篇文案")])
        self.assertEqual(out[0]["task"]["status"], "passed")
    def test_generator(self):
        self.assertIn("生成内容", mock_generate("x"))

if __name__ == "__main__": unittest.main()
