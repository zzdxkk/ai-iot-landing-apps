# 02 · 多智能体工作流（ReAct + DAG）

## 解决什么问题
单轮问答只能"答"，不能"办"。真实任务往往要拆成几步、调不同工具、按依赖顺序执行，中途失败还要重试。这个工程把这两件事拆开做：单个 Agent 的「规划—调工具—看结果」循环，和多任务之间的依赖编排。

## 怎么实现
- `src/agent.py`：简化 ReAct。`plan()` 决定用哪个工具，执行后把 observation 记入 history；工具以 `Tool(name, desc, fn)` 注册，新增工具不改核心
- `src/workflow.py`：DAG 调度。按依赖选出可执行任务，`ThreadPoolExecutor` 并行跑，失败按 `retries` 重试，检测到环或缺依赖直接报错

## 跑起来
```bash
python3 src/agent.py                        # 三句话触发三个工具
python3 src/workflow.py                     # 采集→清洗→(分析,告警检测)
python3 -m unittest discover -s tests -v    # 5 项
```

## 验证
5 项单元测试覆盖：工具选择、未知工具兜底、DAG 顺序、重试后成功、循环依赖报错。

## 边界
- `plan()` 是关键词规则，不是模型决策；换成真实 Agent 时替换这一个方法即可
- DAG 在内存中执行：没有持久化、超时取消和断点续跑，也不做跨进程调度
