---
name: "SDD: Review Spec"
description: "Plan 后建议性预审，输出 Spec Review Matrix + Readiness Verdict"
skill: sdd-riper-one
---

Plan 完成后、执行前的建议性预审。评估 Spec 质量和 Plan 可执行性，输出 GO/NO-GO 建议（不阻塞执行）。

本命令属于 `sdd-riper-one` 技能。未加载技能时请先执行 `/sdd-riper-one`。

**Input**: `/sdd:reviewspec`（无参数，从 spec 状态块读取）

**前置条件**

- spec 状态块 `Phase` 为 `Plan`
- spec `§4 Plan` 已填写

**Steps**

1. 读取 spec 文件，聚焦当前阶段相关章节（阶段感知，不要求所有章节完整）
2. 评估以下维度：
   - **需求清晰度与验收可验证性**：Goal/In-Scope/Acceptance 是否完整清晰
   - **Plan 可执行性**：File Changes、Signatures、Checklist 是否足够明确
   - **风险与回滚覆盖度**：是否有回滚方案、风险是否已识别
   - **跨项目契约完整性**（如适用）：Contract Interfaces 是否完整
3. 输出 Spec Review Matrix：

| 检查项 | 裁决 | 证据 |
|--------|------|------|
| 需求清晰度与验收 | PASS/FAIL/PARTIAL | ... |
| Plan 可执行性 | PASS/FAIL/PARTIAL | ... |
| 风险/回滚覆盖度 | PASS/FAIL/PARTIAL | ... |
| 跨项目契约完整性 | PASS/FAIL/PARTIAL | ... |

4. 输出 Readiness Verdict：`GO` / `NO-GO`（**仅作建议，不阻塞执行**）
5. 输出 Risks & Suggestions
6. 输出 Phase Reminders（属于后续阶段但当前缺失的内容）
7. 持久化审查报告到 spec `§4.4 Spec Review Notes`

**阶段感知规则**

- 不要求所有 Spec 章节一次性完成
- 属于未来阶段的内容列为 Reminder，不作为阻塞依据

**建议性规则（非阻塞）**

- `NO-GO` 不硬性阻塞执行
- 如果用户仍希望执行，继续并记录：`User Decision: Proceed despite NO-GO`

**Output**

- 更新 spec `§4.4 Spec Review Notes`
- 聊天中输出 Review Matrix + Verdict + Suggestions
