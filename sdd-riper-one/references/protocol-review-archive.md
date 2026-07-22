# SDD-RIPER-ONE: Review & Archive

> 本文件是 `sdd-riper-one` 技能的阶段协议。核心规则见 `references/protocol-core.md`。

## REVIEW（审查者）

- 状态：`[LOCKED]`
- 触发："代码评审"、"实现复盘"、"进入 review"

**动作（强制三轴审查）**：

1. **重载真相**：重读最新 Spec 章节（需求、Plan、Execute Log、验收约束）+ 已变更的代码/文件

2. **Codemap 过期审计**：检查 Spec §1.2 是否有 Stale 状态的 codemap。Stale → 警告用户，在 §6 Review Verdict 中注明哪些证据来自直接代码阅读 vs 过期 codemap。附加刷新过期 codemap 的后续建议。

3. **轴1：Spec 质量与需求完成度**
   - Spec 是否清晰定义 Goal/In-Scope/Acceptance
   - 目标和需求完成是否可被证据证明
   - 需求模糊或不完整 → FAIL/PARTIAL 并列出阻塞项

4. **轴2：Spec-代码一致性**
   - 实现是否与 Plan（File Changes、Signatures、Checklist）匹配
   - 行为层面一致性（不仅是文件层面）
   - 未授权偏差记录在 §7 Plan-Execution Diff

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
   - 更新 §6 Review Verdict：Review Matrix（轴 / 关键检查 / PASS-FAIL-PARTIAL / 证据 + 外部证据）
   - Overall Verdict + Blocking Issues
   - 更新 §7 Plan-Execution Diff

**决策门**：
- 轴1 或 轴2 = FAIL → Review FAIL，回到 Research 或 Plan
- 轴3 有高风险未解决 → Review FAIL，回到 Plan
- 阻塞项全部解决后才能关闭

## ARCHIVE（知识蒸馏）

**设计目标**：将中间产物（Spec/Codemap）转化为可复用知识资产。

**触发**："归档"、"沉淀"、"archive"

**输入**：
- `targets`（必填）：要归档的文件/目录
- `kind`：spec / codemap / mixed（默认 mixed）
- `audience`：human / llm / both（默认 both）
- `mode`：snapshot（单任务，默认）/ thematic（跨任务）
- `topic`：归档主题标题（可选，从 targets 推断）

**动作**：
1. 读取源文件，保持源列表明确（Source Index）
2. 整合事实：合并重复，标记冲突，不静默解决矛盾
3. 生成面向特定受众的输出：
   - `human`：目标、范围、决策、结果、风险、可汇报叙述
   - `llm`：约束、接口/契约、代码接触点、已接受模式、反模式、下一步钩子
4. 附加 Trace to Sources（结论 → 源文件/章节）
5. 持久化：
   - `docs/archive/YYYY-MM-DD_HH-MM_<topic>_human.md`
   - `docs/archive/YYYY-MM-DD_HH-MM_<topic>_llm.md`
   - audience=human 或 llm 时仅生成请求的输出

**约束**：
- 默认仅归档（不删除/移动原始产物）
- 活跃 Spec 未完成 Review → 警告并要求确认
- 归档是知识衍生品，不是活跃执行的真相源
