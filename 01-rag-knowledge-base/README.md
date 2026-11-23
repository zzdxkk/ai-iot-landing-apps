# 01 · 企业知识库问答（RAG）

## 解决什么问题
公司制度、手册、FAQ 散在 PDF/Word 里，员工问一句话要翻半天，或者只能问行政。直接让大模型答又容易编，答完没人敢用——因为不知道依据在哪。

这个工程把文档切块入库，提问时先检索、再从原文里给出答案，并把出处一起返回，人能自己核对。

## 怎么实现
1. 切分：160 字滑窗、重叠 40 字，避免一句话被边界切断
2. 向量化：64 维哈希向量（词袋），余弦相似度取 top-3
3. 回答：从召回片段里按与问题的词重合度挑一句（抽取式），附 `source` 与分数
4. 服务化：`src/server.py` 用标准库 `http.server` 提供 `POST /ask`、`GET /health`

## 跑起来
```bash
python3 src/rag.py                          # 三个问题，看答案与引用
python3 -m unittest discover -s tests -v    # 4 项
python3 src/server.py                       # 默认 127.0.0.1:8080，可用 PORT 覆盖
curl -s -X POST localhost:8080/ask \
  -H 'Content-Type: application/json' \
  -d '{"question":"年假几天"}'
```

## 验证
4 项单元测试覆盖：切分产生重叠、向量归一化、检索能召回相关片段、回答带引用。
演示输出里三个问题都能给出答案和出处，例如「年假几天」→ 命中《员工手册.pdf》。

## 边界
- 向量是哈希词袋，不是语义模型：换个说法（"休假天数"）不一定召回；接 bge/OpenAI 只需换掉 `HashEmbedder`
- 回答是抽句，不是生成；没有 PDF/Word 解析、没有增量索引、没有权限控制
