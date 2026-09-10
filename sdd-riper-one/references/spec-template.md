# SDD Spec Template（唯一骨架 · 硬门禁）

本模板是 spec 结构的**唯一权威**。`sdd_bootstrap` 产出的首版 spec 必须符合对应骨架；`review_spec` 会检查结构一致性。

规则：

- 章节编号与顺序固定，**只可追加，不可重排、改号或改名**。
- 未到阶段的章节可以留空或写 `TBD`，但**标题必须存在**。
- 不适用的小节标记 `Skipped + Reason`，而不是删除标题。
- 顶部状态块字段名与顺序固定，见下方。

本模板包含两个版本：**单项目模板**（默认）和**多项目模板**（`mode=multi_project` 时使用）。Agent 根据启动模式自动选择。

---

## 状态块（两个模板通用，必须放在标题下第一段）

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

- `Phase` 枚举（全小写）：`research` | `innovate` | `plan` | `execute` | `review` | `done`
- `Approval` 枚举：`None` | `Plan Approved`
- 每轮结束更新 `Updated` / `Last` / `Next`；阶段切换更新 `Phase`
- 批准时追加一行：`> **Approval Note**: <用户原话>`
- 被其他 spec 推翻时，追加一行（可选，唯一的第 9 行）：`> **Superseded by**: mydocs/specs/<新 spec>.md`

---

## 单项目模板（默认）

```markdown
# SDD Spec: <Task Name>

> **Phase**: research
> **Approval**: None
> **Updated**: YYYY-MM-DD HH:mm
> **Spec**: mydocs/specs/<file>.md
> **Goal**: ...
> **Scope**: ...
> **Last**: ...
> **Next**: ...

## 1. Requirements (Context)
- **Goal**: ...
- **In-Scope**: ...
- **Out-of-Scope**: ...
- **Acceptance Criteria**:
  - [ ] AC1 ...
  - [ ] AC2 ...

## 1.1 Context Sources
- Requirement Source: `...`
- Design Refs: `...`
- Chat/Business Refs: `...`
- Extra Context: `...`

## 2. Research Findings
- 事实与约束: ...
- 现状链路: ...
- 风险与不确定项: ...

## 2.1 Open Questions
- [ ] Q1 ...

## 2.2 Next Actions
- 下一步动作 1 ...
- 下一步动作 2 ...

## 3. Innovate (Optional: Options & Decision)
### Option A
- Pros: ...
- Cons: ...
### Option B
- Pros: ...
- Cons: ...
### Decision
- Selected: ...
- Why: ...
### Skip (for small/simple tasks)
- Skipped: true/false
- Reason: ...

## 4. Plan (Contract)
### 4.1 File Changes
- `path/to/file`: 变更说明

### 4.2 Signatures
- `fn/class signature`: ...

### 4.3 Implementation Checklist
- [ ] 1. ...
- [ ] 2. ...

### 4.4 Spec Review Notes (Optional Advisory, Pre-Execute)
- Spec Review Matrix:
| Check | Verdict | Evidence |
|---|---|---|
| Requirement clarity & acceptance | PASS/FAIL/PARTIAL | ... |
| Plan executability | PASS/FAIL/PARTIAL | ... |
| Risk / rollback readiness | PASS/FAIL/PARTIAL | ... |
| Structure conforms to template | PASS/FAIL/PARTIAL | ... |
- Readiness Verdict: GO/NO-GO (Advisory)
- Risks & Suggestions: ...
- Phase Reminders (for later sections): ...
- User Decision (if NO-GO): Proceed / Revise

## 5. Execute Log
- [ ] Step 1: ...
- [ ] Step 2: ...
- Validation（外部证据优先）: `test/lint/build/diff` 输出摘要

## 6. Review Verdict
- Review Matrix (Mandatory):
| Axis | Key Checks | Verdict | Evidence |
|---|---|---|---|
| Spec Quality & Requirement Completion | Goal/In-Scope/Acceptance 是否完整清晰；需求是否达成 | PASS/FAIL/PARTIAL | `spec section + test/log/人工验收` |
| Spec-Code Fidelity | 文件、签名、checklist、行为是否与 Plan 一致 | PASS/FAIL/PARTIAL | `diff + code refs + execute log` |
| Code Intrinsic Quality | 正确性、鲁棒性、可维护性、测试、关键风险 | PASS/FAIL/PARTIAL | `test/lint/review evidence` |
- Overall Verdict: PASS/FAIL
- Blocking Issues: ...
- Regression risk: Low/Medium/High
- Follow-ups: ...

## 7. Plan-Execution Diff
- Any deviation from plan: ...

## 8. Change Log
> Append-only：新条目插入本标题正下方（最新在上）；历史条目只读，不修改、不删除。
> 无实质变更时写 `- 无`。

### YYYY-MM-DD HH:mm · <相位变化，如 plan → execute>
- **改动**: <一句话：改了什么>
- **原因**: <用户决策 / 新发现 / 风险>
- **影响**: spec `<受影响章节>`；代码 `<受影响文件>`
- **批准**: `Plan Approved`（"用户原话"） / 不适用
- **取代**: 无 / `Supersedes <旧 spec 路径>`
```

---

## 多项目模板（`mode=multi_project` 时使用）

与单项目模板的差异：新增 `§0.1` / `§0.2`，`§4` 按项目分组并新增 `§4.4 Contract Interfaces`（Spec Review Notes 顺延为 `§4.5`），新增 `§6.1 Touched Projects`。

```markdown
# SDD Spec: <Task Name>

> **Phase**: research
> **Approval**: None
> **Updated**: YYYY-MM-DD HH:mm
> **Spec**: mydocs/specs/<file>.md
> **Goal**: ...
> **Scope**: ...
> **Last**: ...
> **Next**: ...

## 0.1 Project Registry
| project_id | project_path | project_type | marker_file |
|---|---|---|---|
| web-console | ./web-console | typescript | package.json |
| api-service | ./api-service | java | pom.xml |

## 0.2 Multi-Project Config
- **workdir**: `./`
- **active_project**: `web-console`
- **active_workdir**: `./web-console`
- **change_scope**: `local`
- **related_projects**: `api-service`

## 1. Requirements (Context)
- **Goal**: ...
- **In-Scope**: ...
- **Out-of-Scope**: ...
- **Acceptance Criteria**:
  - [ ] AC1 ...

## 1.1 Context Sources
- Requirement Source: `...`
- Design Refs: `...`
- Chat/Business Refs: `...`
- Extra Context: `...`

## 2. Research Findings
- 事实与约束: ...
- 风险与不确定项: ...
- 跨项目依赖关系: ...

## 2.1 Open Questions
- [ ] Q1 ...

## 2.2 Next Actions
- 下一步动作 1 ...

## 3. Innovate (Optional: Options & Decision)
### Option A
- Pros: ...
- Cons: ...
### Option B
- Pros: ...
- Cons: ...
### Decision
- Selected: ...
- Why: ...
### Skip (for small/simple tasks)
- Skipped: true/false
- Reason: ...

## 4. Plan (Contract)
### 4.1 File Changes (grouped by project)
#### [web-console]
- `src/pages/release.tsx`: 变更说明

#### [api-service]
- `src/main/java/.../ReleaseController.java`: 变更说明

### 4.2 Signatures (grouped by project)
#### [web-console]
- `function triggerRelease(config: ReleaseConfig): Promise<Result>`: ...

#### [api-service]
- `public ResponseEntity<Result> release(ReleaseRequest req)`: ...

### 4.3 Implementation Checklist (grouped by project, dependency order)
#### [api-service] (provider first)
- [ ] 1. ...

#### [web-console] (consumer second)
- [ ] 2. ...

### 4.4 Contract Interfaces (cross-project only)
| Provider | Interface / API | Consumer(s) | Breaking Change? | Migration Plan |
|---|---|---|---|---|
| api-service | `POST /api/release` | web-console | No | N/A |

### 4.5 Spec Review Notes (Optional Advisory, Pre-Execute)
- Spec Review Matrix:
| Check | Verdict | Evidence |
|---|---|---|
| Requirement clarity & acceptance | PASS/FAIL/PARTIAL | ... |
| Plan executability | PASS/FAIL/PARTIAL | ... |
| Risk / rollback readiness | PASS/FAIL/PARTIAL | ... |
| Cross-project contract completeness | PASS/FAIL/PARTIAL | ... |
| Structure conforms to template | PASS/FAIL/PARTIAL | ... |
- Readiness Verdict: GO/NO-GO (Advisory)
- Risks & Suggestions: ...
- Phase Reminders (for later sections): ...
- User Decision (if NO-GO): Proceed / Revise

## 5. Execute Log (grouped by project)
#### [api-service]
- [ ] Step 1: ...

#### [web-console]
- [ ] Step 2: ...

- Validation（外部证据优先）: `test/lint/build/diff` 输出摘要

## 6. Review Verdict
- Review Matrix (Mandatory):
| Axis | Key Checks | Verdict | Evidence |
|---|---|---|---|
| Spec Quality & Requirement Completion | Goal/In-Scope/Acceptance 是否完整清晰；需求是否达成 | PASS/FAIL/PARTIAL | `spec section + test/log/人工验收` |
| Spec-Code Fidelity | 文件、签名、checklist、行为是否与 Plan 一致 | PASS/FAIL/PARTIAL | `diff + code refs + execute log` |
| Code Intrinsic Quality | 正确性、鲁棒性、可维护性、测试、关键风险 | PASS/FAIL/PARTIAL | `test/lint/review evidence` |
- Overall Verdict: PASS/FAIL
- Blocking Issues: ...
- Regression risk (per project):
  - web-console: Low/Medium/High
  - api-service: Low/Medium/High
- Cross-project consistency: PASS/FAIL
- Follow-ups: ...

## 6.1 Touched Projects
| project_id | Files Changed | Reason |
|---|---|---|
| api-service | `ReleaseController.java` | 新增发布接口 |
| web-console | `release.tsx` | 对接发布接口 |

## 7. Plan-Execution Diff
- Any deviation from plan: ...
- Orphan changes (files outside registered projects): None

## 8. Change Log
> Append-only：新条目插入本标题正下方（最新在上）；历史条目只读，不修改、不删除。
> 无实质变更时写 `- 无`。

### YYYY-MM-DD HH:mm · <相位变化，如 plan → execute>
- **改动**: <一句话：改了什么>
- **原因**: <用户决策 / 新发现 / 风险>
- **影响**: spec `<受影响章节>`；代码 `<受影响文件>`
- **批准**: `Plan Approved`（"用户原话"） / 不适用
- **取代**: 无 / `Supersedes <旧 spec 路径>`
```

---

## 结构校验清单（`sdd_bootstrap` 落盘前自检，`review_spec` 复查）

- [ ] 标题下第一段是状态块，8 个字段齐全且顺序正确
- [ ] `Phase` 值是 6 个枚举之一（全小写）
- [ ] `Approval` 值是 `None` 或 `Plan Approved`
- [ ] 使用对应模式（单项目 / 多项目）的章节骨架，编号与顺序一致
- [ ] 未到阶段的章节标题存在（内容可为 `TBD`），而非缺失
- [ ] `§1 Requirements` 含 `Acceptance Criteria` 且可验证
- [ ] `§4.3 Implementation Checklist` 为原子步骤
- [ ] `§8 Change Log` 存在，且最新条目在最上方；实质变更均已留痕

## 使用要求

### 通用

- 首版 Spec 允许先完成 Research 最小章节，后续章节按 RIPER 阶段逐步补齐。
- 进入 Execute 的唯一准入是状态块 `Approval: Plan Approved`（见 `SKILL.md` CANONICAL DEFINITIONS）。
- `review_spec` 为建议性预审：`NO-GO` 不强制阻塞执行；若继续执行需记录用户决策。
- Review 未通过则返回 Research/Plan 重新闭环。
- 历史 spec 若使用旧结构（如 `## Phase`、`## RIPER Status`、无编号章节），**不回填**；恢复执行时按需在文件顶部补状态块即可。

### 变更记录（§8 Change Log）

- **何时必须记**：任何对已落盘 spec 的**实质内容**变更——Goal / Scope / Acceptance Criteria / Plan / 口径 / 行为约束 / 被其他 spec 取代。
- **何时可不记**：纯排版、错别字、链接修复。
- **Reverse Sync 必须留痕**：执行中发现现实与 spec 不符，先改 spec 再改代码，并在 `§8` 记录原因与影响。
- **推翻旧 spec**：新 spec 首条记录 `Supersedes <旧 spec 路径>`；同时去旧 spec 状态块补 `> **Superseded by**: <新 spec 路径>`，避免后人误读过期 spec。
- **只读历史**：历史条目不得修改或删除；更正错误的方式是追加一条新条目。
- **上下文策略**：全量 Change Log 属冷上下文，默认不加载；回读时只看最新 1-2 条。

### 多项目专属

- `§0.1 Project Registry` 和 `§0.2 Multi-Project Config` 在 bootstrap 时由 Agent 自动生成（Auto-Discovery 或用户提供的 projects 列表）。
- `§4 Plan` 的 File Changes、Signatures、Checklist 必须按项目分组，Provider 优先于 Consumer。
- `§4.4 Contract Interfaces` 仅在 `change_scope=cross` 时必填。
- `§6.1 Touched Projects` 在任何跨项目改动后必填。
- `§6 Review Verdict` 必须包含 per-project regression risk 和 cross-project consistency 检查。
