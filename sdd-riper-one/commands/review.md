---
name: "SDD: Review"
description: "执行后三轴审查，输出 Review Verdict"
skill: sdd-riper-one
---

本命令属于 `sdd-riper-one` 技能。未加载技能时请先执行 `/sdd-riper-one`。

Execute 完成后执行结构化三轴审查。

**Input**: `/sdd:review`（无参数，从 spec 状态块读取）

**Steps**

1. 读取 spec 文件状态块，确认 `Phase` 为 `execute`
2. 读取 spec `§4 Plan` + `§5 Execute Log`（温上下文加载）
3. 执行三轴审查（必须全部输出）：
   - **轴 1 - Spec 质量与目标达成**：Goal/Scope/Acceptance 是否完整清晰；需求是否完成
   - **轴 2 - Spec-代码一致性**：代码是否忠实执行 Plan（文件、签名、checklist、行为）
   - **轴 3 - 代码自身质量**：正确性、鲁棒性、可维护性、测试、风险
4. 输出 `§6 Review Verdict`：Review Matrix + Overall Verdict + Blocking Issues
5. 输出 `§7 Plan-Execution Diff`：偏差与原因
6. 更新状态块 `Phase: review`

**Output**

更新 spec `§6`、`§7` 和状态块。

**门禁**

- 轴 1 或轴 2 任一 FAIL → Review FAIL，回到 Research/Plan
- 轴 3 存在高风险问题 → Review FAIL，回到 Plan
- Review PASS → 可执行 `/sdd:archive`
