# SDD-RIPER Workflow Quick Reference

总纲：`RIPER`，全程按 SDD 维护 Spec。**本技能只维护 spec 一种产物。**

## 启动顺序

1. 标准流（中大型任务）：`sdd_bootstrap（启动 Research）`
2. 快速流（小任务/模糊需求）：`sdd_bootstrap（启动 Research）`
3. RIPER：`Research -> (Innovate, 可选) -> Plan -> Execute -> Review`

## 三个动作的定位

- `sdd_bootstrap`：RIPER 启动命令（进入 Research 第一步并产出首版 spec）
- `review_spec`：Plan 后的建议性预审动作，按当前阶段评审并输出 `Spec Review Matrix + Readiness Verdict(GO/NO-GO)`（不阻塞执行）
- `review_execute`：Execute 后质量门禁动作，按三轴输出 `Review Matrix + Overall Verdict + Plan-Execution Diff`

## sdd_bootstrap 输入容错与提问准则

- 容错输入：只要需求有意义，就可启动。
- 自动补全：优先自己找信息（代码/历史 spec）。
- 提问策略：鼓励多问，但每个问题必须服务于 research 决策。
- 无效提问定义：重复问、与任务无关、为问而问。

## 产物命名规则（统一时间前缀）

- `sdd_bootstrap`：`mydocs/specs/YYYY-MM-DD_hh-mm_<TaskName>.md`
- 规则：时间前缀不可省略，业务名不可擅改。

## 阶段完成标准（DoD）

- **RESEARCH DoD**：明确需求边界、现状链路、已知风险，并写入 spec。
- **INNOVATE（可选）DoD**：若执行则完成方案对比与取舍；若跳过需写明跳过原因。
- **PLAN DoD**：产出文件改动清单、签名变化、原子 checklist。
- **EXECUTE DoD**：代码改动与 plan 对齐，执行日志与 Validation 回写 spec。
- **REVIEW DoD**：三轴评审完整（Spec质量与达成 / Spec-代码一致性 / 代码自身质量），并给出 `Overall Verdict` 与偏差清单。

## Spec 产物策略

- 首版 Spec 只要求完成 Research 最小章节；Plan/Execute/Review 内容按阶段补齐。
- 章节骨架固定，只可追加不可重排：见 `references/spec-template.md`。
- `§8 Change Log` 记录实质变更（含 Reverse Sync 与推翻旧 spec）；全量属冷上下文，回读只看最新 1-2 条。

## 阶段门禁

- RESEARCH 门禁：优先引用 `Requirement Source`；小任务允许最小化输入，但需在 spec 标注信息缺口。
- INNOVATE 门禁：复杂任务默认 2-3 方案；小任务可跳过但需在 spec 标注原因。
- PLAN 门禁：必须包含 `File Changes + Signatures + Checklist`。
- PLAN 后建议：执行 `review_spec`；其 `NO-GO` 为建议项，用户可选择继续执行并记录决策。
- `review_spec` 采用分阶段检查：未到阶段的章节只提醒，不作为阻塞依据。
- EXECUTE 门禁：状态块必须为 `Approval: Plan Approved`。
- REVIEW 门禁：必须输出 `Review Matrix + Overall Verdict + Plan-Execution Diff`；任一高风险阻塞项未解决不得收口。

## 关键约束

- No Spec, No Code
- Spec is Truth
- Reverse Sync（变更必须回写 spec 并在 `§8` 留痕）
- Review FAIL -> 回到 Research/Plan

## 多项目协作（自动发现 + 作用域隔离）

### 启动方式

- `sdd_bootstrap: mode=multi_project, task=..., goal=..., requirement=...`
- 无需手动列项目；Agent 自动扫描 workdir 识别子项目（通过 `package.json`/`pom.xml`/`go.mod` 等标志文件）
- 也可显式提供 `projects=[...]` 跳过自动发现
- 智能降级：仅 1 个子项目 → 单项目模式；0 个子项目 → workdir 本身作为单项目

### 多项目 DoD（阶段完成标准）

- **RESEARCH DoD**：Project Registry 已确认，跨项目依赖已识别
- **PLAN DoD**：File Changes / Signatures / Checklist 按项目分组；跨项目改动有 Contract Interfaces
- **EXECUTE DoD**：按依赖顺序执行（Provider → Consumer）；Touched Projects 已记录
- **REVIEW DoD**：per-project regression risk + cross-project consistency 检查通过

### 多项目门禁

- 每轮必须声明 `active_project` + `active_workdir`
- 默认 `change_scope=local`，仅改当前项目
- `change_scope=cross` 需显式触发，且必须：检查目标 Spec 冲突 → 记录 Contract Interfaces → 记录 Touched Projects

### 多项目触发词

- `MULTI / 多项目`：进入多项目模式，运行自动发现
- `CROSS / 跨项目`：当前轮 `change_scope=cross`
- `SWITCH <project_id> / 切换 <project_id>`：切换 active_project
- `REGISTRY / 项目列表`：显示当前 Project Registry
- `SCOPE LOCAL / 回到本地`：重置为 `change_scope=local`

## 常用触发词（汇总）

- `sdd_bootstrap: task=..., goal=..., requirement=...`
- `FAST / 快速 / >>`：小改极速通道（事后同步 spec）
- `REVIEW SPEC / 评审规格 / 计划评审`：执行 `review_spec`（建议性预审）
- `REVIEW EXECUTE / 代码评审 / 实现复盘`：执行 `review_execute` 三轴审查
- `DEBUG / 排查 / 日志分析`：Debug 排查模式（日志 + Spec + 代码三角定位）
- `验证功能`：Debug 验证模式（全链路日志 vs Spec 逐条比对）
- `MULTI / 多项目`：多项目模式（自动发现 + 作用域隔离）
- `CROSS / 跨项目`：允许跨项目改动
- `SWITCH <id> / 切换 <id>`：切换活跃项目
- `REGISTRY / 项目列表`：查看项目注册表
- `SCOPE LOCAL / 回到本地`：回到本地作用域
