# 原生命令动作详细参数

> 本文件是 `SKILL.md` 中「原生命令动作」段落的完整展开。默认不常驻上下文，仅在需要查看命令详细参数时按需加载。
> 本技能只维护 spec 一种产物，不生成 context bundle / archive / codemap 等派生文档。

## 1) `sdd_bootstrap`

- 用途：RIPER 启动命令（进入 Research 第一步，并产出第一版 spec）
- 输入：只要是「有意义且真实的需求」即可（口述/文档/聊天记录均可）
- 执行动作：
  - 汇总用户输入 + 代码事实 + 历史 spec
  - 冲突处理：先落首版 spec 标记冲突，再给 `Option A/B` 和推荐决策
  - 形成首版研究结论与下一步动作
- 输出：`mydocs/specs/YYYY-MM-DD_hh-mm_<TaskName>.md`，**必须使用 `references/spec-template.md` 骨架与状态块**
- 首版最小内容：状态块、`§1 Requirements`、`§1.1 Context Sources`、`§2 Research Findings`、`§2.1 Open Questions`、`§2.2 Next Actions`

## 2) `review_spec`

- 用途：在 `Plan` 完成后、`Execute` 前进行 spec 质量评审（建议性，不阻塞执行）
- 输入：
  - `spec`：spec 文件路径（可选，默认当前活跃 spec）
  - `scope`：`plan_only`（默认）或 `full`
- 评审重点：
  1. 目标/范围/验收标准是否清晰且可验证
  2. `Plan` 是否可执行（文件、签名、checklist 是否原子化）
  3. 风险、回滚、跨项目契约（如有）是否充分
  4. 结构是否符合 `references/spec-template.md` 骨架
- 分阶段原则：
  - 仅评审「当前阶段应当具备」的章节，不要求一次性覆盖全 spec
  - 对尚未到阶段的章节只做 `Reminder`，不计入 `NO-GO`
- 输出：
  - `Spec Review Matrix`（逐项 `PASS/FAIL/PARTIAL` + 证据）
  - `Readiness Verdict`：`GO/NO-GO`（**建议性结论**）
  - `Risks & Suggestions`（若继续执行需关注项）
  - `Phase Reminders`（按阶段待补齐项）
- 约束：
  - `NO-GO` 不构成硬阻塞；若用户坚持执行，允许继续
  - 用户选择继续时，必须在 spec 记录 `User Decision: Proceed despite NO-GO`

## 3) `review_execute`

- 用途：在 `Execute` 后执行结构化评审，输出可回写 spec 的审查结论
- 输入：
  - `spec`：spec 文件路径（可选，默认当前活跃 spec）
  - `scope`：`changed_only`（默认）或 `full`（全量评审）
- 评审三轴（必须全部输出）：
  1. **Spec 质量与目标达成**：spec 是否写清目标、范围、验收标准；需求是否完成
  2. **Spec-代码一致性**：代码是否忠实执行 `Plan`（文件、签名、checklist、行为）
  3. **代码自身质量**：脱离 spec 后，代码在正确性、鲁棒性、可维护性、测试、风险上的质量
- 输出：
  - `Review Matrix`（三轴逐项 `PASS/FAIL/PARTIAL` + 证据）
  - `Overall Verdict`（`PASS/FAIL`）与 `Blocking Issues`
  - `Plan-Execution Diff`（偏差与原因）
- 门禁：
  - 轴 1 或轴 2 任一 `FAIL` → `Review FAIL`，回到 `Research/Plan`
  - 轴 3 存在高风险问题 → `Review FAIL`，回到 `Plan`
