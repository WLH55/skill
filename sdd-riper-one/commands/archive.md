---
name: "SDD: Archive"
description: "归档完成的 spec/codemap，沉淀为可复用知识"
skill: sdd-riper-one
---

本命令属于 `sdd-riper-one` 技能。未加载技能时请先执行 `/sdd-riper-one`。

对完成的 spec/codemap 做归档沉淀，将"中间产物"提炼为可复用知识。

**Input**: `/sdd:archive [targets]` 或 `/sdd:archive targets=<paths> kind=<spec|codemap|mixed> audience=<human|llm|both>`

- `targets`: 文件或目录路径（支持多个，默认当前活跃 spec）
- `kind`: `spec` / `codemap` / `mixed`（默认 `spec`）
- `audience`: `human` / `llm` / `both`（默认 `both`）
- `mode`: `snapshot`（单任务归档，默认）/ `thematic`（跨任务主题归档）
- `topic`: 归档主题名（可选，默认从 targets 推断）

**Steps**

1. 检查 spec 状态块，确认 `Phase` 不是 `execute`（未完成 Review 的 spec 禁止归档）
2. 读取 spec 内容，提炼关键知识
3. 生成归档文档：
   - `human`: 汇报视角
   - `llm`: 后续开发参考视角
4. 每个归档文档必须包含 `Trace to Sources`（结论 → 来源文件）避免失真
5. 更新状态块 `Phase: done`

**Output**

- `docs/archive/YYYY-MM-DD_HH-MM_<topic>_human.md`
- `docs/archive/YYYY-MM-DD_HH-MM_<topic>_llm.md`

**Guardrails**

- 有活跃执行中的 spec（Phase 为 execute）时，禁止归档该 spec
- 默认只归档不删除原文件；删除/移动需用户显式授权
