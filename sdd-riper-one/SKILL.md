---
name: sdd-riper-one
description: 将 SDD-RIPER 方法论落地为严格可执行流程的技能。用于代码/架构任务中的 Spec 驱动研发与 RIPER 阶段门禁（Research→Plan→Execute→Review）及审批控制（Plan Approved），适用于 Claude/Codex/其他 CLI Agent 的多轮协作开发。触发词：sdd_bootstrap、SDD、RIPER、spec 驱动、Plan Approved、review_spec、review_execute、多项目、debug 排查。
---

# SDD-RIPER-ONE

> 单一协议来源：`references/protocol-core.md` + `references/protocol-*.md`（v4）。
> `SKILL.md` 只保留门禁、流程与索引；细节一律按路径回读，不在此复述。
> **本技能只维护 spec 一种产物**，不生成 codemap / context bundle / archive 等派生文档。

## 全局行为与安全底线 (Global Safeguards)

- **高危操作阻断**：永远不要静默或提议执行 `git clean`（包含任何参数，特别是 `-fdx`），防止用户未提交的工作区数据不可逆丢失。
- **研发纪律**：
  - `No Spec, No Code`：未形成并持久化 Spec 前，不进入代码实现。
  - `No Approval, No Execute`：未得到执行许可前，禁止进行环境修改或高风险变更。
  - `Spec is Truth`：任何聊天决议或最新改动必须回源到 Spec，Spec 是唯一真相源。

## 核心定位

- 总纲：`RIPER`，全程遵循 SDD 并持续维护 Spec。
- 三条底线：`No Spec, No Code`、`Spec is Truth`、`Reverse Sync`（实质变更必须回写 spec 并在 `§8 Change Log` 留痕）。
- RIPER 主流程：`Research -> (Innovate, 可选) -> Plan -> Execute -> Review`。
- **Spec 受众分层与上下文保护**：Spec 的第一受众是人类（持久化的任务上下文与组织记忆），第二受众才是模型。协议对模型的核心价值是四件事：**注意力聚焦**、**信息索引**（按路径回读而非全量常驻）、**防止上下文腐烂**（用落盘 Spec 对抗长对话遗忘与漂移）、**辅助 Review**（提供 Spec vs 代码的交叉验证基准）。协议绝不应导致上下文被塞满挤爆——RIPER 管流程，Spec 管记录，模型按需取用。
- 不要在每轮对话里重载整份 Skill / Spec；默认只回读当前阶段需要的小节。

## CANONICAL DEFINITIONS（唯一权威定义）

以下四项在**所有文件**中必须一致；发现不一致时以本节为准，并修正对方文件。

### 1) 路径与命名

- 唯一产物是 spec，落在 `mydocs/specs/`，统一时间前缀 `YYYY-MM-DD_hh-mm_`：
  - `mydocs/specs/YYYY-MM-DD_hh-mm_<TaskName>.md`
- 时间前缀不可省略，业务名不可擅改。

### 2) Spec 状态块（程序计数器）

每份 spec 顶部必须包含，字段名与顺序固定：

```markdown
> **Phase**: research
> **Approval**: None
> **Updated**: YYYY-MM-DD HH:mm
> **Spec**: mydocs/specs/<file>.md
> **Goal**: <一句话目标>
> **Scope**: <In-Scope 一句话>
> **Last**: <上一轮完成了什么>
> **Next**: <下一步动作>
```

- `Phase` 枚举（全小写）：`research` | `innovate` | `plan` | `execute` | `review` | `done`。
- `Approval` 枚举：`None` | `Plan Approved`。
- 每轮结束必须更新 `Updated` / `Last` / `Next`；阶段切换更新 `Phase`。
- 被取代时可选追加 `> **Superseded by**: mydocs/specs/<新 spec>.md`。

### 3) 批准确认

- 进入 `Execute` 的**唯一准入条件**是 spec 状态块中 `Approval: Plan Approved`。
- Agent 只能在用户做出**明确指向执行**的批准表态后写入该标记，例如「批准，执行」「Plan Approved」「可以，开始实现」。
- **单独出现「继续」「嗯」「可以」「看起来没问题」不构成 Plan Approved**；「继续」只表示按当前步骤单步推进。
- 禁止根据语气、倾向或不完整表述推断批准；无法确定时直接问。
- 批准时在 spec 记录原始语句：`Approval Note: <用户原话>`。
- 已批准后若修改 Plan，必须追加 `§8 Change Log` 并将 `Approval` 重置为 `None`（需重新批准）。

### 4) Spec 章节骨架（硬门禁）

首版 spec 必须使用 `references/spec-template.md` 的单项目骨架（`§1`~`§8` 固定编号与顺序）；新增内容只可**追加**，不可重排或改名。状态块见第 2 条。

## 推荐流程（直接执行）

- 标准流（中大型任务）：
  - `sdd_bootstrap -> Research -> (Innovate, 可选) -> Plan -> Execute -> Review`
- 快速流（小任务/需求模糊）：
  - `sdd_bootstrap -> Research -> Plan -> Execute -> Review`
- 门禁：
  - 首版 spec 落盘前，不进入实现
  - 状态块无 `Approval: Plan Approved`，禁止进入 `Execute`
  - `Review` 不通过，回到 `Research/Plan` 修正

## 上下文装配规则

- `SDD` 是完整持久化上下文与记忆层：必须完整落盘、持续维护，但不要求每轮整份常驻输入。
- `RIPER` 是审批驱动状态机：必须在每轮保持当前 `phase`、当前 `Approval` 与下一步动作清晰可见。
- 裁剪目标是减少重复重放，不是减少约束或弱化门禁。

### 热上下文（每轮必带）

- 当前 `Phase`、`Approval`
- 当前 `Spec` 路径
- 当前 `Goal`、`In Scope / Out of Scope`
- 当前活跃 `Checklist`
- 当前 `Open Questions`
- 当前风险与 `Next Action`

热上下文只用于当前轮聚焦，不替代完整 spec；与 spec 冲突时，永远以 spec 为准。

### 温上下文（切阶段或高风险动作前加载）

- `Research -> Plan`：`Research Findings`、关键事实、方案结论
- `Plan -> Execute`：`File Changes`、`Signatures`、原子 `Checklist`
- `Execute -> Review`：`Execute Log`、实际改动摘要、偏差说明
- 执行 `review_spec` / `review_execute` 时，回读对应评审区块

### 冷上下文（默认不带，命中再加载）

- 全量 `Change Log`
- 历史 `Research` 细节
- `MULTI` / `DEBUG` 的完整扩展规则
- 长示例、长模板、长 quick reference

### 硬门禁（不可因裁剪而削弱）

- 没有 spec，不进入代码实现（唯一例外：用户显式调用 `/sdd:fix` 做纯机械改动，需声明 `Spec Waived: /sdd:fix`）
- `Phase` 与 `Approval` 必须是显式状态，不允许根据语气、倾向或不完整表述推断
- 状态块无 `Approval: Plan Approved`，不进入 `Execute`
- 首版 spec 结构必须符合 `references/spec-template.md` 骨架（见 CANONICAL DEFINITIONS 第 4 条）
- phase 切换前，必须回读对应 spec 区块；不能只靠热上下文跨阶段推进
- `Review` 时必须基于 Plan 与 Validation，而不是只看聊天摘要
- 发现冲突、字段缺失、摘要过期或记忆不确定时，立即回读完整 spec 或相关原文区块

### 回读触发规则

- **每轮必带**：`Phase`、`Approval`、`Spec` 路径、`Goal`、当前活跃 `Checklist`、`Next Action`
- **切阶段时**：回读目标阶段对应的 spec 区块（Research Findings / File Changes / Execute Log 等）
- **执行 review 时**：`review_spec` 回读 Plan 区块，`review_execute` 回读 Plan + Execute Log + Review 区块
- **触发全量回读**：阶段切换有争议、摘要与 spec 冲突、长对话出现遗忘迹象、高风险改动
- **禁止**：不能用热上下文替代 spec 原文跨阶段推进，不能根据模糊语气推断 `Plan Approved`

## 多项目协作（自动发现 + 作用域隔离）

- 目标：多项目场景下保持「局部理解 + 局部执行 + 显式边界」，**用户零额外配置**。
- 详细协议：`references/multi-project.md`

### 自动发现（Auto-Discovery）

- 触发：`sdd_bootstrap: mode=multi_project` 或触发词 `MULTI / 多项目`
- Agent 自动扫描 `workdir` 下子目录，通过标志文件识别子项目：
  - JS/TS: `package.json` | Java/Kotlin: `pom.xml`, `build.gradle` | Go: `go.mod` | Python: `pyproject.toml`, `setup.py` | Rust: `Cargo.toml` | 通用: `.git`
  - Monorepo: 额外检查 `workspaces`、`settings.gradle`、`pnpm-workspace.yaml`
- 产出 `Project Registry`（`§0.1`），报告给用户确认后继续
- 用户也可显式提供 `projects=[...]` 跳过自动发现
- 智能降级：仅 1 个子项目 → 自动降级为单项目模式；0 个子项目 → workdir 本身作为单项目

### 作用域隔离规则（必须）

- 每轮先声明 `active_project` 与 `active_workdir`
- 默认 `change_scope=local`，只允许修改 `active_project` 下的文件
- 仅在显式 `change_scope=cross`（或触发词 `CROSS / 跨项目`）时允许跨项目改动
- 跨项目执行后，在 spec `§6.1 Touched Projects` 记录改动项目、文件、原因

### 跨项目依赖与契约

- 跨项目改动时，必须在 spec `§4.4 Contract Interfaces` 记录：Provider → Interface → Consumer → 是否 Breaking Change → 迁移方案
- 跨项目 Plan 的 checklist 按项目分组，Provider 优先于 Consumer 执行
- 修改前检查目标项目是否有活跃 Spec，有冲突则 STOP 等待用户决策

### 多项目 Review（扩展）

- 校验跨项目契约一致性（Provider 与 Consumer 接口匹配）
- 校验 Touched Projects 完整性
- 校验无孤立改动（所有改动文件都在已注册项目内）
- 按项目分别评估回归风险

### 触发词

- `MULTI / 多项目` → 进入多项目模式，运行自动发现
- `CROSS / 跨项目` → 当前轮 `change_scope=cross`
- `SWITCH <project_id> / 切换 <project_id>` → 切换 `active_project`
- `REGISTRY / 项目列表` → 显示当前 Project Registry
- `SCOPE LOCAL / 回到本地` → 重置为 `change_scope=local`

## 原生命令动作（可直接输入）

### 1) `sdd_bootstrap`

- 用途：RIPER 启动命令（进入 Research 第一步，并产出第一版 spec）
- 输入：只要是「有意义且真实的需求」即可（口述/文档/聊天记录均可）
- 执行动作：
  - 汇总用户输入 + 代码事实 + 历史 spec
  - 冲突处理：先落首版 spec 标记冲突，再给 `Option A/B` 和推荐决策
  - 形成首版研究结论与下一步动作
- 输出：`mydocs/specs/YYYY-MM-DD_hh-mm_<TaskName>.md`，**必须使用 `references/spec-template.md` 骨架**
- 首版最小内容：状态块（见 CANONICAL 第 2 条）、`§1 Requirements`、`§1.1 Context Sources`、`§2 Research Findings`、`§2.1 Open Questions`、`§2.2 Next Actions`

### 2) `review_spec`

- 用途：在 `Plan` 完成后、`Execute` 前进行 spec 质量评审（建议性，不阻塞执行）
- 输入：`spec`（可选，默认当前活跃 spec）、`scope`（`plan_only` 默认 / `full`）
- 评审重点：
  1. 目标/范围/验收标准是否清晰且可验证
  2. `Plan` 是否可执行（文件、签名、checklist 是否原子化）
  3. 风险、回滚、跨项目契约（如有）是否充分
  4. **结构是否符合 `references/spec-template.md` 骨架**
- 分阶段原则：仅评审「当前阶段应当具备」的章节；未到阶段的章节只做 `Reminder`，不计入 `NO-GO`
- 输出：`Spec Review Matrix`（逐项 `PASS/FAIL/PARTIAL` + 证据）、`Readiness Verdict`（`GO/NO-GO`，建议性）、`Risks & Suggestions`、`Phase Reminders`
- 约束：`NO-GO` 不构成硬阻塞；若用户坚持执行，必须在 spec 记录 `User Decision: Proceed despite NO-GO`

### 3) `review_execute`

- 用途：在 `Execute` 后执行结构化评审，输出可回写 spec 的审查结论
- 输入：`spec`（可选，默认当前活跃 spec）、`scope`（`changed_only` 默认 / `full`）
- 评审三轴（必须全部输出）：
  1. **Spec 质量与目标达成**：spec 是否写清目标、范围、验收标准；需求是否完成
  2. **Spec-代码一致性**：代码是否忠实执行 `Plan`（文件、签名、checklist、行为）
  3. **代码自身质量**：脱离 spec 后，代码在正确性、鲁棒性、可维护性、测试、风险上的质量
- 输出：`Review Matrix`（三轴逐项 `PASS/FAIL/PARTIAL` + 证据）、`Overall Verdict`（`PASS/FAIL`）与 `Blocking Issues`、`Plan-Execution Diff`（偏差与原因）
- 门禁：
  - 轴 1 或轴 2 任一 `FAIL` → `Review FAIL`，回到 `Research/Plan`
  - 轴 3 存在高风险问题 → `Review FAIL`，回到 `Plan`

## 阶段约束（最小集合）

- 每轮先同步 spec 再推进阶段
- 默认不在每轮对话中重载整份 spec；优先回读当前阶段区块、活跃 checklist、`Open Questions`、最近一次 `Change Log / Validation`
- 仅在切换阶段、执行 `review_spec/review_execute`、发现冲突或明显遗忘时，全量回读 spec
- `Innovate` 可选：复杂任务建议 2-3 方案；小任务可跳过但要写原因
- `Plan` 必须可执行：文件路径 + 签名 + 原子 checklist
- `Plan` 后建议执行 `review_spec`；其 `NO-GO` 为建议项，不是强制门禁
- `Review` 必须按三轴评审并回写结论：`Review Matrix`、`Overall Verdict`、`Plan-Execution Diff`
- 实质变更必须回写 `§8 Change Log`

## Debug 模式（日志驱动排查与功能验证）

- 用途：基于日志 + Spec + 代码三角定位 Bug，或用全链路日志验证功能是否正常
- 触发词：`DEBUG / 排查 / 日志分析 / 验证功能`
- 输入：`log_path`（必须）、`issue`（可选，排查时建议提供）、`spec`（可选，验证时建议提供）
- 两种子模式：
  - **排查模式**（默认）：结合 Spec 和代码定位可能的 Bug 根因
  - **验证模式**：逐条比对 Spec 预期行为与日志实际行为
- 工作流：读日志 → 建立「预期 vs 实际」对照 → 定位可疑代码 → 输出结论 → 如需修复则进入 RIPER
- 约束：
  - Debug 模式本身不直接改代码，只做分析和定位
  - 需要改代码时，必须走 RIPER 流程（或 FAST 通道处理小修复）
  - 分析结论回写到 Spec 的 `Debug Log` 段（如有活跃 Spec）

## 触发词

- `BOOTSTRAP / sdd_bootstrap` → `sdd_bootstrap(task, goal, requirement)`
- `MULTI / 多项目` → 多项目轻量模式（父目录 workdir + 局部执行）
- `CROSS / 跨项目` → 允许跨项目改动（强制记录 `Touched Projects`）
- `FAST / 快速 / >>` → 小改快速通道（改后同步 spec）
- `REVIEW SPEC / 评审规格 / 计划评审` → 执行 `review_spec`（建议性预审）
- `REVIEW EXECUTE / 代码评审 / 实现复盘` → 执行 `review_execute`（三轴审查）
- `DEBUG / 排查 / 日志分析 / 验证功能` → Debug 模式（日志驱动排查与功能验证）
- `EXIT SDD / 退出协议` → 退出状态机

## 命名规则（统一时间前缀）

- 时间前缀：`YYYY-MM-DD_hh-mm_`
- `sdd_bootstrap`：`mydocs/specs/YYYY-MM-DD_hh-mm_<TaskName>.md`

## 参考

- `references/protocol-core.md`（核心法则、状态机、门禁）
- `references/protocol-research.md`（Research + Innovate）
- `references/protocol-plan-execute.md`（Plan + Review Spec + Execute + FAST）
- `references/protocol-review.md`（Review）
- `references/protocol-debug.md`（Debug 模式）
- `references/spec-template.md`（**唯一 Spec 骨架，硬门禁**）
- `references/multi-project.md`（多项目协作详细规则）
- `references/commands.md`（原生命令动作详细参数）
- `references/workflow-quickref.md`（速查）
- `references/usage-examples.md`（示例）
