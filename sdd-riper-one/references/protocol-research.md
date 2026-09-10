# SDD-RIPER-ONE: Research & Innovate

> 本文件是 `sdd-riper-one` 技能的阶段协议。核心规则见 `references/protocol-core.md`。

## RESEARCH（第一个 RIPER 阶段）

- 状态：`[LOCKED]`
- 动作：
  1. 分析用户输入/代码库（用 `read`/`grep` 直接读取相关文件，以当前代码为准）
  2. 识别未知项，检查模糊约束，写入 `§2.1 Open Questions`
  3. 立即在磁盘上创建/更新 Spec 文件，**使用 `references/spec-template.md` 骨架与状态块**
- 决策门：
  1. 仅调研 → 留在 RESEARCH
  2. 复杂任务 → 进入 INNOVATE
  3. 标准/小型任务 → 进入 PLAN（跳过 INNOVATE，在 Spec `§3` 记录跳过原因）
- 暂停点：触发 STOP-AND-WAIT

## INNOVATE（可选 — 复杂场景）

- 状态：`[LOCKED]`
- 触发：仅在 RESEARCH 中明确需要时进入
- 动作：
  1. 分析权衡（利/弊），产出 2-3 个方案
  2. 更新 Spec → `§3 Innovate`
- 下一步：用户选择方案 → 进入 PLAN
- 暂停点：输出策略，停止并等待用户指令

## 关于代码索引（原 CodeMap，已移除）

原 `create_codemap` 与 Codemap Staleness 机制已移除，原因：代码更新频繁时索引文件快速过期，维护成本高于收益，且容易让模型基于过期索引做判断。

做法：需要理解代码时**直接 `read`/`grep` 相关文件**，以当前代码为准；代码结构结论直接写进 spec 的 `§2 Research Findings`，并标注「快照时间 + 可能已过期」。不得以任何索引文件替代真实代码作为事实依据。
