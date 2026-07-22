---
name: "SDD: Plan"
description: "进入 Plan 阶段，输出详细的实施计划（含可选 Innovate 方案设计）"
skill: sdd-riper-one
---

本命令属于 `sdd-riper-one` 技能。未加载技能时请先执行 `/sdd-riper-one`。

进入 Plan 阶段。输出详细实施计划，人类批准后才准动手。

**Input**: `/sdd:plan`（无参数，从 spec 状态块读取当前上下文）

**Steps**

1. 读取 spec 文件状态块，确认 `Phase` 为 `research`
2. 读取 spec `§2 Research Findings`（温上下文加载）
3. 如任务复杂，先进入 `§3 Innovate`，产出 2-3 个方案并推荐
4. 小任务可跳过 Innovate，但要写原因
5. 完成 `§4 Plan (Contract)`：
   - `4.1 File Changes`: 具体文件路径 + 变更说明
   - `4.2 Signatures`: 函数/类签名
   - `4.3 Implementation Checklist`: 原子化 checklist
6. 建议执行 `review_spec`（建议性预审）
7. 更新状态块 `Phase: plan`、`Approval: Pending`

**Output**

更新 spec 文件的 `§3`、`§4` 段和状态块。

**Guardrails**

- Plan 必须可执行：文件路径 + 签名 + 原子 checklist
- 未收到用户明确肯定 + 继续意图，禁止进入 Execute（不要求精确字符串 "Plan Approved"）
- `/sdd:reviewspec` 的 `NO-GO` 为建议项，不是强制门禁
