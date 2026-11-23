"""把评测结果渲染成 Markdown 报告，可直接贴进周报/PR。"""
def render(result, cmp=None):
    lines = ["# 模型应用评测报告", "", f"样本数：**{result['n']}**", "", "## 汇总", "", "| 指标 | 得分 |", "| --- | --- |"]
    for k, v in result["summary"].items(): lines.append(f"| {k} | {v} |")
    lines += ["", "## 逐条明细", "", "| 用例 | " + " | ".join(result["summary"].keys()) + " |",
              "| --- | " + " | ".join(["---"] * len(result["summary"])) + " |"]
    for row in result["per_case"]:
        lines.append("| " + str(row["id"]) + " | " + " | ".join(str(row[k]) for k in result["summary"]) + " |")
    if cmp:
        lines += ["", f"## 回归对比（{cmp['metric']}）", "",
                  f"- 基线：{cmp['baseline']}  ", f"- 当前：{cmp['candidate']}  ",
                  f"- 变化：{cmp['delta']}（{'提升' if cmp['improved'] else '未提升'}）"]
    return "\n".join(lines)

if __name__ == "__main__":
    from evaluator import evaluate, compare, Case
    a = evaluate([Case("1", "q", "5天", "5天")])
    print(render(a, compare(a, a)))
