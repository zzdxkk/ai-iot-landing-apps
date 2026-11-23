"""把 RAG 能力包成 HTTP 接口（标准库 http.server，无第三方依赖）。

启动：python3 src/server.py            # 默认 127.0.0.1:8080
      PORT=8099 python3 src/server.py  # 换端口
调用：curl -X POST http://127.0.0.1:8080/ask \
        -H 'Content-Type: application/json' \
        -d '{"question":"年假几天"}'
"""
import json, os
from http.server import BaseHTTPRequestHandler, HTTPServer
from rag import KnowledgeBase, answer

kb = KnowledgeBase()
kb.add("入职满一年享 5 天年假，满三年 10 天。社保公积金入职当月缴纳。", "员工手册.pdf")
kb.add("差旅住宿：一线城市 500 元/晚，其他 350 元/晚，需发票。", "财务制度.docx")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/health":
            self.send_error(404); return
        self._json({"ok": True, "docs": len(kb.docs)})

    def do_POST(self):
        if self.path != "/ask":
            self.send_error(404); return
        n = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(n) or b"{}")
        self._json(answer(kb, body.get("question", "")))

    def _json(self, obj):
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"listening on http://127.0.0.1:{port}", flush=True)
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()
