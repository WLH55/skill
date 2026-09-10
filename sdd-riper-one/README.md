# sdd-riper-one

SDD-RIPER ONE Skill（标准控盘协议）。

该 Skill 是比 `sdd-riper-one-light` 更重、更显式的入口，用于约束大模型严格按以下流程执行研发任务：

`Research -> (Innovate, 可选) -> Plan -> (Plan Approved) -> Execute -> Review`

> **只维护 spec 一种产物。** 本技能不生成 CodeMap、Context Bundle、Archive 等派生文档——它们会在源头变更后过期，成为误导模型的第二副本。

## 工作方式优先

这个仓库更推荐把 `sdd-riper-one` 当成一种**标准控盘工作方式**来使用，而不是当成一组必须死记硬背的显式命令。

它不是被 `sdd-riper-one-light` 淘汰的旧方案，而是给需要更强显式流程的人使用：团队训练、复杂任务、低模型能力环境、严格审计、跨人交接，都适合从这里进入。

最重要的不是先记住 `sdd_bootstrap` 这个名字，而是先形成下面这套默认习惯：

- `No Spec, No Code`
- `No Approval, No Execute`
- `Spec is Truth`
- 先形成最小 spec / summary / checkpoint，再进入执行
- 复杂任务走完整阶段门禁，小任务也不能裸改

显式命令是能力接口，不是唯一入口。真正该让团队先学会的，是**先收敛任务，再批准执行**。

## TL;DR（30 秒上手）

- 总纲：`RIPER`，全程遵循 SDD 并维护 Spec。
- 先记住三句话：`No Spec, No Code`、`No Approval, No Execute`、`Spec is Truth`。
- 不要一开始就要求直接改代码；先让模型形成最小 spec。
- 中大型任务默认走完整阶段门禁；小任务也先收敛目标、范围、约束与验证方式。
- 你给口述需求、文档、聊天记录都可以启动。
- 进入 Execute 的唯一准入是 spec 状态块 `Approval: Plan Approved`（详见下文）。

## 使用策略（团队标准）

- **稳态入口**：`sdd-riper-one` Skill（建议与 `sdd-riper-one-light` 同时安装）。
- **Prompt**：可选增强（有则更稳，无也可用）。
- **MCP**：可选提效，不是必需依赖。
- **底线**：`No Spec, No Code` + 未获批准前不得改代码。

### 推荐的最小启动方式

给 agent 任务时，优先说明：

- `目标`
- `范围`
- `约束`
- `验证方式`

然后要求它：

- 先收敛任务理解
- 先建立最小 spec
- 先给下一步计划与风险
- 等你批准后再进入执行

## 批准确认规则（重要，唯一权威）

- 进入 `Execute` 的唯一准入条件：Spec 状态块中 `Approval: Plan Approved`。
- 你只需表达**明确指向执行**的批准（如「批准，执行」「Plan Approved」「可以，开始实现」），模型即可写入该标记。
- **单独一句「继续」「嗯」「可以」不算批准**；「继续」只表示按当前步骤单步推进。
- 批准时模型需在 spec 记录 `Approval Note: <你的原话>`。
- 已批准后若修改 Plan，`Approval` 会被重置为 `None`，需要重新批准。

## 推荐流程

- 标准流（中大型任务）：
  - `sdd_bootstrap -> Research -> (Innovate, 可选) -> Plan -> Execute -> Review`
- 快速流（小任务/需求模糊）：
  - `sdd_bootstrap -> Research -> Plan -> Execute -> Review`
- 关键门禁：
  - 首版 spec 落盘前，不进入后续实现阶段。
  - 状态块无 `Approval: Plan Approved`，禁止进入 `Execute`。
  - `Review` 不通过，必须回到 `Research/Plan` 闭环修正。

## Spec 结构（硬门禁）

- 每份 spec 顶部必须有固定状态块（`Phase` / `Approval` / `Updated` / `Spec` / `Goal` / `Scope` / `Last` / `Next`）。
- 章节骨架固定（`§1`~`§8`），只可追加，不可重排或改名；详见 `references/spec-template.md`。
- `§8 Change Log` 是 append-only 的改动历史；任何实质变更（含 Reverse Sync、被其他 spec 取代）都必须留痕。
- 历史 spec 若为旧结构，不回填；恢复执行时在顶部补状态块即可。

## Multi-Project Collaboration（自动发现 + 作用域隔离）

**用户零配置**：只需 `mode=multi_project`，Agent 自动完成项目发现与作用域隔离。

### 核心能力

- **自动发现**：Agent 扫描 workdir，通过标志文件（`package.json`/`pom.xml`/`go.mod`/`Cargo.toml` 等）自动识别子项目，输出 Project Registry 供用户确认。
- **作用域隔离**：默认 `change_scope=local` 只改当前项目；`CROSS / 跨项目` 显式触发跨项目改动。
- **跨项目契约**：跨项目改动自动要求填写 Contract Interfaces（Provider → Consumer → Breaking Change?）。
- **智能降级**：仅 1 个子项目自动降级为单项目模式；0 个子项目则 workdir 本身作为单项目。

### 多项目触发词

| 触发词 | 作用 |
|---|---|
| `MULTI / 多项目` | 进入多项目模式，运行自动发现 |
| `CROSS / 跨项目` | 当前轮允许跨项目改动 |
| `SWITCH <id> / 切换 <id>` | 切换活跃项目 |
| `REGISTRY / 项目列表` | 查看当前 Project Registry |
| `SCOPE LOCAL / 回到本地` | 重置为本地作用域 |

## 原生命令动作（Skill 内置）

- `sdd_bootstrap`：RIPER 启动命令（进入 Research 第一步并产出第一版 spec）。
- `review_spec`：Execute 前的建议性评审命令，按当前阶段检查 spec/plan 并输出 `GO/NO-GO` 建议（不强制阻塞执行）。
- `review_execute`：Execute 后评审命令，按三轴输出 `Review Matrix`（Spec质量与达成 / Spec-代码一致性 / 代码自身质量）并给出 `Overall Verdict`。
- `debug`：日志驱动的排查与功能验证——指定日志路径 + 问题描述进行 Bug 三角定位，或指定日志 + Spec 逐条验证功能是否正常。

## 关于已移除的派生产物

早期版本提供 `create_codemap`（代码索引）、`build_context_bundle`（需求上下文包）、`archive`（归档沉淀）。三者均已移除，原因是同一条：

> **派生产物 = 负债。** 只有「源材料机器读不了（图片/OCR）」或「需要跨越 N 份文档做聚合」时，派生才有价值；否则它只是一个会在源头变更后悄悄过期的第二副本，而且没人知道该信哪个。

替代做法：

- 需要理解代码 → 直接 `read`/`grep` 当前代码；结构结论写进 spec `§2 Research Findings`。
- 需要记录需求来源 → 写进 spec `§1.1 Context Sources`。
- 需要跨任务沉淀知识 → 写进新 spec 的 `§2 Research Findings`，或综合历史 spec 直接阅读。

## 最小启动示例（示意，不是唯一入口）

如果你需要给团队一个最小示例，建议给这种「工作方式模板」，而不是让大家先背整套动作名：

```text
请使用 sdd-riper-one 先收敛任务，不要直接改代码。
先给我：
- 你对任务的理解
- 最小 spec
- 下一步计划
- 风险
- 验证方式
我批准后再执行。
```

在会话中可直接输入：

```text
请启用 $sdd-riper-one，并执行 sdd_bootstrap：
- task=资源访问审批与时效控制
- goal=支持审批授权与时效控制
- requirement=docs/prd/sample_approval.md
```

多项目场景（自动发现，无需手动列项目）：

```text
请启用 $sdd-riper-one，并执行 sdd_bootstrap：
- mode=multi_project
- task=前后端联动发布
- goal=并行推进 web-console 与 api-service 的发布功能
- requirement=docs/prd/release.md
```

也可显式指定项目列表（跳过自动发现）：

```text
请启用 $sdd-riper-one，并执行 sdd_bootstrap：
- mode=multi_project
- task=前后端联动发布
- goal=并行推进 web-console 与 api-service
- requirement=docs/prd/release.md
- projects=[{id:web-console,path:./web-console},{id:api-service,path:./api-service}]
```

## Bootstrap 后续步骤（辅导版）

1. **Research**：补背景、补约束、补链路，持续修正首版 spec。
2. **Innovate（可选）**：复杂任务输出 2-3 方案并对比；小任务可跳过并记录原因。
3. **Plan**：给文件级改动、签名、原子 checklist，等待你确认。
4. **Review Spec（可选）**：执行 `review_spec` 做执行前建议性预审（分阶段检查）；若 `NO-GO` 你仍可选择继续执行。
5. **Execute**：仅在你的批准写入状态块 `Approval: Plan Approved` 后改代码。
6. **Review / review_execute**：按三轴输出评审矩阵与总体结论；不通过则回到 Research/Plan。

补充：首版 spec 只需覆盖 Research 最小章节，Plan/Execute/Review 章节按阶段补齐。

## sdd_bootstrap 输入与提问策略

- 输入不强制格式：口述、文档、聊天记录都可直接启动。
- 输入越完整，启动越快；但不完整也可先进入 research。
- 模型应主动补全项目内信息（代码/历史 spec）。
- 提问鼓励「多问且问透」，但必须有价值（不是凑问题）。

## 新手常见误区

- 误区 1：还没 plan 就要求直接改代码。
- 误区 2：改完代码不回写 spec。
- 误区 3：把失效的派生文档（旧 codemap / 归档摘要）当成事实依据。

## 可选增强（有 MCP 时）

若已接入 MCP，可调用同名动作进行自动化落盘提效；未接入时，模型按 Skill 规则手工完成同等产物。

## 文件命名规则（统一时间前缀）

产物统一使用 `YYYY-MM-DD_hh-mm_` 前缀：

- `sdd_bootstrap`（spec）：`mydocs/specs/YYYY-MM-DD_hh-mm_<TaskName>.md`

未经用户明确允许，不得省略时间前缀，不得擅自改写业务名。

## 文件结构

- `SKILL.md`：门禁、流程、CANONICAL DEFINITIONS（唯一权威定义）
- `references/protocol-core.md` + `protocol-*.md`：协议细节
- `references/spec-template.md`：Spec 骨架（硬门禁）
- `references/commands.md` / `workflow-quickref.md` / `usage-examples.md`：参数、速查、示例
- `references/multi-project.md` / `protocol-debug.md`
- `commands/`：斜杠命令（供支持的宿主使用）

## 发布前检查

1. `SKILL.md`、`agents/openai.yaml`、`references/*.md` 是否齐全。
2. 全局一致性：路径统一 `mydocs/specs/`、批准规则统一、spec 骨架统一、无已移除产物（codemap/context/archive）残留。
3. 安装验证：`your-skill-host install /path/to/sdd-riper-one`。
4. 提交并推送到远端主分支。
