# 03 · 大模型应用评测

## 解决什么问题
改了提示词、换了模型，效果到底变好还是变差？没有可复现的评测，就只能凭感觉，改坏了也发现不了。这个工程把评测做成一条固定流程：用例集 → 多指标打分 → 与基线对比 → 出 Markdown 报告。

## 怎么实现
- `src/evaluator.py`：`Case`（问题/参考答案/模型答案），三个指标 `exact`、`contains`、`token_f1`，`evaluate()` 出汇总与逐条明细，`compare()` 算基线到当前的 delta
- `src/report.py`：把结果渲染成 Markdown 表格，可直接贴进 PR 或周报

## 跑起来
```bash
python3 src/evaluator.py                    # 基线 vs 改进版对比
python3 src/report.py                       # 输出 Markdown 报告
python3 -m unittest discover -s tests -v    # 4 项
```

## 验证
4 项单元测试覆盖：三个指标的边界（完全相同/包含/部分重合）、汇总值、A/B delta 的方向。

## 边界
- 三个指标都是字面匹配，不做语义等价判断；需要语义或人工标准时得接更强评测器
- 用例集是示例规模（3 条）；没有并发调用、缓存、成本统计和 CI 集成
