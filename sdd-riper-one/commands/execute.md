---
name: "SDD: Execute"
description: "进入 Execute 阶段，按 Plan 无脑执行"
skill: sdd-riper-one
---

本命令属于 `sdd-riper-one` 技能。未加载技能时请先执行 `/sdd-riper-one`。

进入 Execute 阶段。按 Plan 逐项实施。

**Input**: `/sdd:execute`（无参数，从 spec 状态块读取）

**前置条件**

- spec 状态块 `Phase` 为 `plan`
- spec 状态块 `Approval` 为 `Plan Approved`（用户已做出明确指向执行的批准；单独「继续」不算）

**Steps**

1. 读取 spec 文件状态块，确认 Phase 和 Approval
2. 读取 spec `§4 Plan` 的 File Changes、Signatures、Checklist（温上下文加载）
3. 按 checklist 逐项执行
4. 每完成一项，更新 spec `§5 Execute Log`，勾选 checklist
5. 更新状态块 `Phase: execute`
6. 有实质偏差时：先追加 `§8 Change Log`，再向用户报告

**Output**

- 代码变更
- 更新 spec `§5 Execute Log` 和状态块

**Guardrails**

- 如果 Approval 不是 `Plan Approved`，STOP 并提示用户批准
- 实现偏差时，先暂停说明，更新 Plan 与 `§8 Change Log` 后重新请求批准
- 保持变更最小化和聚焦
