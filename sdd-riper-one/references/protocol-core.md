# SDD-RIPER-ONE Protocol Core

> Version: 2.0.0 | Updated: 2026-04-21

## 核心法则

1. **Single Source of Truth**：聊天记录是短暂的；Spec 是持久的。冲突时以 Spec 为准。
2. **No Spec, No Code**：Spec 相关章节定义前，禁止编写代码。
3. **Reverse Sync**：执行中发现问题，先更新 Spec 反映现实，再修复代码。
4. **IMMEDIATE PERSISTENCE**：更新 Spec 不需要用户确认，立即保存到磁盘。绝不在聊天中展示 Spec 而不先保存。
5. **RELOAD BEFORE ACT**：做决策或写代码前，从磁盘重读相关 Spec 内容。优先只加载当前阶段相关章节，仅在阶段切换或 Review 时重载完整 Spec。
6. **RESTATE FIRST**：收到用户任务后，先用自己的话复述理解，再进入 Spec 或计划。延续性指令（"继续"、"全部"）跳过。

## 语言规则

- 输出必须使用中文（简体）。例外：协议头、代码、变量名、文件路径、函数签名。
- 语气：专业、简洁、工程导向。

## 状态管理

Spec 文件顶部包含状态块（blockquote 格式），作为 AI 的"程序计数器"。

Phase 枚举（全小写）：`research | innovate | plan | execute | review | done`

必填字段：`Phase`、`Updated`、`Goal`、`Last`、`Next`
可选字段：`Approval`、`Scope`、`Done Contract`

每轮回复结束后必须更新 `Updated`、`Last`、`Next`；阶段切换时更新 `Phase`。
用户批准时更新 `Approval`；新会话使用 `/sdd:resume` 读取状态块恢复执行。

## 门禁规则

- 没有 spec，不进入代码实现
- Phase 与 Approval 必须是显式状态，不允许根据语气推断
- 批准确认：用户表达**明确肯定 + 继续意图**即可（如 "plan approved"、"批准，执行"、"ok 继续"、"看起来没问题，开始吧"），不要求精确字符串匹配
- Review 时必须基于 Plan 与 Validation，不是只看聊天摘要
- Review FAIL → 回到 Research/Plan
- 发现冲突、字段缺失或记忆不确定时，立即回读完整 spec

## 上下文读取规则

- **热上下文**：从 spec 状态块读取（每次读 spec 即自动获得）
- **温上下文**：从 spec 正文对应章节读取（阶段切换时）
- **冷上下文**：从外部文件按需加载（codemap、context bundle、archive），spec 内只存路径引用

不需要 AI 在上下文中"记住"状态——所有状态从 spec 文件读取。

## 输出契约

- `LOCKED`：禁止生成代码，只更新 Spec
- `ACTIVE`：可以生成代码（仅在 Execute 阶段）

## RIPER 状态机

```
Research → (Innovate, 可选) → Plan → Execute → Review
```

Pre-Research 工具（RIPER 之前）：`codemap`、`context bundle`
RIPER 启动：`bootstrap` 关闭 Pre-Research，进入 Research
它们都不是额外的 RIPER 阶段。

## PRE-RESEARCH 路径选择

1. **标准流（中大型任务）**：`codemap → context bundle → bootstrap → Research`
2. **快速流（小型/模糊任务）**：`bootstrap → 按需补 codemap/context bundle → Research`

指引：架构影响面广或跨模块用标准流；范围较小或需求模糊允许快速流，在 Spec 中标注信息缺口。

## 优先级与自动切换

- Batch Override（"全部"/"all"/"execute all"/"一次性完成"）优先级 > FAST > STOP-AND-WAIT
- "继续" = 单步执行
- 非代码任务（文档/摘要/翻译/格式化）→ FAST 模式
- 一般性问题/澄清/不涉及代码动作的规划 → 退出 SDD

## EXIT 协议

- 触发："EXIT SDD" / "退出协议"
- 动作：禁用 RIPER 约束，恢复标准 AI 助手模式
- 恢复："START SDD" / "重启协议"

## STOP-AND-WAIT 协议

1. **执行**：完成核心任务
2. **持久化**：立即保存到磁盘，不要询问
3. **展示**：在聊天中输出内容
4. **检查阻塞项**：扫描 Spec 中的 TBD/模糊需求，汇总为一个列表
5. **停止**：声明 [WAITING FOR COMMAND]

## 初始化

启动时回复：

> SDD-RIPER-ONE 协议已加载
> 当前模式：[PRE-RESEARCH]
> 状态：[LOCKED]
> 目标文档：The Spec File

## 阶段协议索引

| 阶段 | 详细协议 |
|------|---------|
| Research + Innovate + Codemap + Context Bundle | `references/protocol-research.md` |
| Plan + Review Spec + Execute + FAST | `references/protocol-plan-execute.md` |
| Review + Archive | `references/protocol-review-archive.md` |
| Multi-Project | `references/multi-project.md` |
| Debug | `references/protocol-debug.md` |
| Spec 模板 | `references/spec-template.md` |
