# SDD-RIPER-ONE: Review

> 本文件是 `sdd-riper-one` 技能的阶段协议。核心规则见 `references/protocol-core.md`。

## REVIEW（审查者）

- 状态：`[LOCKED]`
- 触发：「代码评审」「实现复盘」「进入 review」

**动作（强制三轴审查）**：

1. **重载真相**：重读最新 Spec 章节（`§1 Requirements`、`§4 Plan`、`§5 Execute Log`、`§8 Change Log`、验收约束）+ 已变更的代码/文件

2. **Reverse Sync 审计**：检查 `§8 Change Log` 最新条目；若发现代码有未回写 spec 的实质变更，列为阻塞项（轴2 FAIL）

3. **轴1：Spec 质量与需求完成度**
   - Spec 是否清晰定义 Goal/In-Scope/Acceptance
   - 目标和需求完成是否可被证据证明
   - 需求模糊或不完整 → FAIL/PARTIAL 并列出阻塞项

4. **轴2：Spec-代码一致性**
   - 实现是否与 Plan（File Changes、Signatures、Checklist）匹配
   - 行为层面一致性（不仅是文件层面）
   - 未授权偏差记录在 `§7 Plan-Execution Diff`

5. **轴3：代码内在质量**
   - 正确性、鲁棒性、可维护性/可读性、测试充分性
   - 关键风险（安全/性能/回归）
   - 即使代码符合 Spec，也报告高风险缺陷

6. **外部证据要求**：Review 结论应有以下至少一项外部证据支撑：
   - 自动化测试输出
   - lint/build 输出
   - git diff 统计
   - 人工确认清单
   - 无外部证据的 Review 应标记为 `PARTIAL — 缺少外部验证`

7. **持久化审查报告到 Spec**：
   - 更新 `§6 Review Verdict`：Review Matrix（轴 / 关键检查 / PASS-FAIL-PARTIAL / 证据 + 外部证据）
   - Overall Verdict + Blocking Issues
   - 更新 `§7 Plan-Execution Diff`
   - 状态块 `Phase: review` → `done`

**决策门**：
- 轴1 或 轴2 = FAIL → Review FAIL，回到 Research 或 Plan
- 轴3 有高风险未解决 → Review FAIL，回到 Plan
- 阻塞项全部解决后才能关闭
