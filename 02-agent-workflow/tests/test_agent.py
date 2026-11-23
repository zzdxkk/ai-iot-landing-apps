import sys, os, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from agent import Agent, Tool, calculator
from workflow import Workflow, Task

class TestAgent(unittest.TestCase):
    def setUp(self):
        self.agent = Agent("测试", [Tool("weather", "", lambda c: f"{c}晴"),
                                    Tool("calculator", "", calculator)])
    def test_tool_dispatch(self):
        r = self.agent.run("南京天气")
        self.assertEqual(r["tool"], "weather")
        self.assertIn("晴", r["observation"])
    def test_calculator(self):
        self.assertEqual(calculator("计算 1 + 2"), "3.0")
    def test_history(self):
        self.agent.run("南京天气"); self.agent.run("南京天气")
        self.assertEqual(len(self.agent.history), 2)

class TestWorkflow(unittest.TestCase):
    def test_dag_order(self):
        wf = Workflow()
        wf.add(Task("a", lambda c: 1))
        wf.add(Task("b", lambda c: c["a"] + 1, deps=["a"]))
        out = wf.execute()
        self.assertEqual(out, {"a": 1, "b": 2})
    def test_retry(self):
        calls = {"n": 0}
        def flaky(c):
            calls["n"] += 1
            if calls["n"] < 2: raise ValueError("flaky")
            return "ok"
        wf = Workflow().add(Task("x", flaky, retries=2))
        self.assertEqual(wf.execute()["x"], "ok")

if __name__ == "__main__": unittest.main()
