---
name: "SDD: Bootstrap"
description: "启动 SDD 任务，进入 Research 阶段，产出第一版 spec"
skill: sdd-riper-one
---

本命令属于 `sdd-riper-one` 技能。未加载技能时请先执行 `/sdd-riper-one`。

启动 SDD 任务（RIPER 的 Research 第一步）。

**Input**: `/sdd:bootstrap task=<任务名> goal=<目标> requirement=<需求文档或描述>`

- 输入只要是"有意义且真实的需求"即可（口述/文档/聊天记录均可）

**Steps**

1. 汇总用户输入 + 代码事实 + 历史资产（context/spec）
2. 冲突处理：先落首版 spec 标记冲突，再给 `Option A/B` 和推荐决策
3. 形成首版研究结论与下一步动作
4. 写入 spec 文件，更新状态块 `Phase: research`

**Output**

- `mydocs/specs/YYYY-MM-DD_hh-mm_<TaskName>.md`
- 首版最小内容：状态块（`Phase`/`Approval`/`Updated`/`Spec`/`Goal`/`Scope`/`Last`/`Next`）、`§1 Requirements`、`§1.1 Context Sources`、`§2 Research Findings`、`§2.1 Open Questions`、`§2.2 Next Actions`
- 章节骨架必须符合 `references/spec-template.md`（只可追加，不可重排）

**Guardrails**

- 首版 spec 落盘前，不进入代码实现
- 如果有 `mode=multi_project` 或触发词 `MULTI / 多项目`，执行多项目自动发现（详见 `references/multi-project.md`）
