"""AI 客服工单助手：意图识别 -> 槽位抽取 -> 知识匹配 -> 自动建单/转人工。"""
import json, re
from dataclasses import dataclass, asdict

KB = {
    "退款": "退款申请可在订单页提交，7-15 个工作日到账。",
    "发票": "电子发票在订单详情申请，1 个工作日内开出。",
    "物流": "物流信息在『我的订单-查看物流』查询。",
}

def intent(q):
    for k in KB:
        if k in q: return k
    return "其他"

def slots(q):
    phone = re.search(r"1\d{10}", q)
    order = re.search(r"订单号?\s*(\w{6,})", q)
    return {"phone": phone.group() if phone else None,
            "order": order.group(1) if order else None}

@dataclass
class Ticket:
    id: str
    intent: str
    info: dict
    reply: str
    need_human: bool

_seq = [0]
def handle(question):
    it = intent(question); info = slots(question)
    _seq[0] += 1
    if it in KB:
        need_human = info["order"] is None and it == "退款"
        return Ticket(f"T{_seq[0]:04d}", it, info, KB[it], need_human)
    return Ticket(f"T{_seq[0]:04d}", "其他", info, "抱歉，我将转接人工客服为您服务。", True)

if __name__ == "__main__":
    for q in ["我要退款，订单号 ABC123456", "发票怎么开", "随便问问"]:
        print(json.dumps(asdict(handle(q)), ensure_ascii=False))
