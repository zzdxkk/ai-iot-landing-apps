"""最小可用的 RAG 知识库：切分 -> 向量化(纯 python 哈希向量) -> 检索 -> 带引用回答。
不依赖任何第三方库和外部 API，可直接运行；真实项目中把 embed/llm 换成模型调用即可。"""
import re, math, hashlib
from collections import Counter

def _tokens(text):
    text = text.lower()
    toks = re.findall(r"[\u4e00-\u9fff]|[a-z0-9]+", text)
    return toks or [""]

class HashEmbedder:
    """把文本映射成 64 维稀疏向量，演示用；生产可替换为 bge / openai embeddings。"""
    DIM = 64
    def embed(self, text):
        v = [0.0] * self.DIM
        for t in _tokens(text):
            h = int(hashlib.md5(t.encode("utf-8")).hexdigest(), 16)
            v[h % self.DIM] += 1.0
        norm = math.sqrt(sum(x * x for x in v)) or 1.0
        return [x / norm for x in v]

def chunk(text, size=160, overlap=40):
    """按字符滑窗切分，保留重叠，避免语义被切断。"""
    text = re.sub(r"\s+", " ", text).strip()
    out, start = [], 0
    while start < len(text):
        out.append(text[start:start + size])
        if start + size >= len(text):
            break
        start += size - overlap
    return out

def cosine(a, b):
    return sum(x * y for x, y in zip(a, b))

class KnowledgeBase:
    def __init__(self):
        self.embedder = HashEmbedder()
        self.docs = []      # list of (text, source, vector)
    def add(self, text, source):
        for c in chunk(text):
            self.docs.append((c, source, self.embedder.embed(c)))
    def retrieve(self, query, top_k=3):
        qv = self.embedder.embed(query)
        scored = [(cosine(qv, v), t, s) for t, s, v in self.docs]
        scored.sort(key=lambda x: -x[0])
        return scored[:top_k]

def answer(kb, question, top_k=3):
    """抽取式回答：从召回片段中挑与问题最相关的句子，附引用。"""
    hits = kb.retrieve(question, top_k)
    qtok = set(_tokens(question))
    best, best_score, best_src = "", -1.0, ""
    for _, text, src in hits:
        for sent in re.split(r"[。！？.!?]", text):
            s = set(_tokens(sent))
            if not s:
                continue
            score = len(qtok & s) / math.sqrt(len(s))
            if score > best_score:
                best, best_score, best_src = sent.strip(), score, src
    return {"question": question, "answer": best or "知识库中暂无相关信息。",
            "citations": [{"source": s, "score": round(sc, 4)} for sc, _, s in hits]}

if __name__ == "__main__":
    kb = KnowledgeBase()
    kb.add("入职满一年可享 5 天年假，满三年 10 天。社保公积金入职当月缴纳。", "员工手册.pdf")
    kb.add("差旅住宿标准：一线城市每晚 500 元，其他城市 350 元，需提供发票。", "财务制度.docx")
    kb.add("远程办公需提前在 OA 申请，每周不超过 2 天，部门经理审批。", "考勤制度.pdf")
    for q in ["年假有几天？", "出差住宿能报多少？", "可以居家办公吗？"]:
        r = answer(kb, q)
        print(f"Q: {r['question']}\nA: {r['answer']}\n引用: {r['citations'][0]['source']}\n")
