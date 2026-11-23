"""AIGC 内容管线：模板 -> 批量任务队列 -> 生成(可插拔后端) -> 审核规则 -> 导出。"""
import json, re
from dataclasses import dataclass, asdict

@dataclass
class Task:
    id: str
    prompt: str
    platform: str = "xiaohongshu"
    status: str = "pending"
    output: str = ""

Banned = ["赌", "诈骗", "虚假宣传"]

def render_prompt(template, **kw):
    for k, v in kw.items(): template = template.replace("{" + k + "}", str(v))
    return template

def mock_generate(prompt):
    """演示用生成器；生产替换为 文生图/文生视频 API 调用即可。"""
    return f"[生成内容] {prompt[:40]}"

def moderate(text):
    hits = [b for b in Banned if b in text]
    return {"pass": not hits, "hits": hits}

def run(tasks):
    out = []
    for t in tasks:
        content = mock_generate(t.prompt)
        m = moderate(content)
        t.status = "passed" if m["pass"] else "blocked"
        t.output = content
        out.append({"task": asdict(t), "moderation": m})
    return out

if __name__ == "__main__":
    tpl = "写一篇关于{product}的{platform}文案，突出{selling}"
    tasks = [Task("1", render_prompt(tpl, product="保温杯", platform="小红书", selling="24小时保温")),
             Task("2", render_prompt(tpl, product="课程", platform="抖音", selling="限时优惠"))]
    print(json.dumps(run(tasks), ensure_ascii=False, indent=1))
