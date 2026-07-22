---
name: "SDD: Resume"
description: "从 spec 状态块恢复执行上下文，支持跨会话恢复"
skill: sdd-riper-one
---

本命令属于 `sdd-riper-one` 技能。未加载技能时请先执行 `/sdd-riper-one`。

从 spec 文件的状态块恢复执行上下文。新会话或中断后使用。

**Input**: `/sdd:resume [spec-path]` 或 `/sdd:resume`（自动发现活跃 spec）

**Steps**

1. 确定目标 spec 文件
   - 如果提供了路径，直接使用
   - 如果未提供，扫描 `docs/specs/` 目录，按修改时间找到最近更新的 spec
   - 如果找到多个，列出供用户选择
2. 读取 spec 文件，解析顶部状态块
3. 从状态块提取关键字段：
   - `Phase`: 当前处于哪个阶段
   - `Goal`: 核心目标
   - `Approval`: 是否已获批准（如有）
   - `Scope`: 范围（如有）
   - `Done Contract`: 完成定义（如有）
   - `Last`: 上次做了什么
   - `Next`: 下一步动作
4. 检查 §1.2 Codemap Used 的 Staleness 状态：
   - 如果任何 codemap 标记为 `Stale`，在恢复摘要中警告用户
   - 提示建议执行 `/sdd:codemap` 刷新过期索引后再继续
5. 输出恢复摘要
6. 用户确认后继续执行

**Output 示例**

```
## 恢复上下文

**Spec**: docs/specs/2026-04-19_14-30_用户登录.md
**Phase**: Plan
**Goal**: 实现完整登录流程
**Last**: 完成 Research，调研了 3 个方案
**Next**: 完成 Plan §4 的 File Changes 和 Checklist
**Approval**: Pending

继续吗？
```

**Guardrails**

- 如果 spec 文件没有状态块，提示用户先初始化（使用 `/sdd:bootstrap`）
- 如果状态块 `Phase` 为 `done`，提示已完成，建议 `/sdd:archive`
- 通过状态块字段自动适配不同任务复杂度
