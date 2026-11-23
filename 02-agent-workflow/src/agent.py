"""轻量多智能体工作流：ReAct 风格的 规划-执行-观察-反思 循环，工具可插拔。"""
import json, re
from dataclasses import dataclass, field

@dataclass
class Step:
    thought: str
    action: str
    action_input: str
    observation: str = ""

class Tool:
    def __init__(self, name, desc, fn):
        self.name, self.desc, self.fn = name, desc, fn

class Agent:
    def __init__(self, name, tools=None):
        self.name = name
        self.tools = {t.name: t for t in (tools or [])}
        self.history = []
    def plan(self, task):
        if "天气" in task: return ("查询天气", "weather", "南京")
        if "计算" in task or "+" in task: return ("需要计算", "calculator", task)
        return ("直接回答", "echo", task)
    def run(self, task, max_steps=5):
        thought, action, inp = self.plan(task)
        tool = self.tools.get(action)
        obs = tool.fn(inp) if tool else f"无工具 {action}"
        step = Step(thought, action, inp, obs)
        self.history.append(step)
        result = {"task": task, "thought": thought, "tool": action,
                  "observation": obs, "steps": len(self.history)}
        return result

def calculator(expr):
    m = re.search(r"([\d\.]+)\s*\+\s*([\d\.]+)", expr)
    return str(float(m.group(1)) + float(m.group(2))) if m else "无法解析"

if __name__ == "__main__":
    tools = [Tool("weather", "查天气", lambda c: f"{c}：晴，26℃"),
             Tool("calculator", "计算", calculator), Tool("echo", "回显", lambda s: s)]
    agent = Agent("助手", tools)
    for t in ["南京天气怎么样？", "帮我计算 12 + 30", "你好"]:
        print(json.dumps(agent.run(t), ensure_ascii=False))
