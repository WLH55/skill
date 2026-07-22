---
name: "SDD: Fast Forward"
description: "一键快进：任务描述 → micro-spec → checkpoint → 实现 → 回写"
skill: sdd-riper-one
---

一键快进模式。适用于小任务、需求明确的快速开发。跳过完整 RIPER 状态机，用最小流程完成任务。

本命令属于 `sdd-riper-one` 技能。未加载技能时请先执行 `/sdd-riper-one`。

**Input**: `/sdd:ff <任务描述>`

- 可以是自然语言描述，也可以是具体的任务指令

**适用范围**

- 单文件或少量文件的明确改动
- 需求清晰、无需深入调研的任务
- UI 微调、配置变更、简单逻辑修改

**Steps**

1. **复述理解**：用自己的话复述任务，确认核心目标
2. **写 micro-spec**（1-3 句）：
   - 目标
   - 涉及文件
   - 主要风险
   - 验证方式
   - Done Contract（什么算完成、由什么证明）
3. **落盘 spec**：写入 `docs/specs/YYYY-MM-DD_HH-MM_<TaskName>.md`，包含顶部状态块
4. **给 checkpoint**：
   - 当前理解
   - 核心目标
   - 下一步 1-3 个动作
   - 风险
   - 验证方式
5. **等待用户批准**
6. **实现**：按 checkpoint 执行代码变更
7. **回写验证**：
   - 更新 spec Change Log
   - 更新 Validation（外部证据优先）
   - 更新状态块 `Phase: done`
8. **复杂度升级**：如果执行中发现复杂度超出预期（架构改动、跨模块、需求模糊），立即暂停，建议升级到标准版的 `/sdd:bootstrap` 流程

**状态块格式**

```markdown
> **Phase**: <plan|execute|review|done> | **Updated**: YYYY-MM-DD HH:MM
> **Goal**: <核心目标>
> **Done Contract**: <完成定义>
> **Last**: <上次完成什么> | **Next**: <下一步>
```

使用标准 Phase 枚举（plan → execute → review → done），与标准版保持一致。

**Guardrails**

- 必须有最小 spec，不能裸改代码
- 必须等用户批准后再执行
- 完成由证据证明，不是模型自行宣布
- 执行后必须回写 spec
- 复杂度上升时立即升级到 `/sdd:bootstrap`
