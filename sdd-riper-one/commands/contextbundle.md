---
name: "SDD: Context Bundle"
description: "构建需求上下文包，支持 Lite 和 Standard 两种粒度"
skill: sdd-riper-one
---

构建需求上下文包。从用户提供的目录或文件中提取需求事实和约束，整理为结构化 bundle。

本命令属于 `sdd-riper-one` 技能。未加载技能时请先执行 `/sdd-riper-one`。

**Input**: `/sdd:contextbundle <目录路径>` 或 `/sdd:contextbundle files=<文件列表>`

- 输入可以是目录路径、文件路径列表
- `level`: Lite（默认，小任务）/ Standard（中大型任务）

**Steps**

1. 读取目录/文件中的可用内容（文本/文档/图片等）
   - 使用尽力解析，无法解析的文件记录在 Unparsed Sources 列表
2. 提取需求事实和约束，附带来源引用
3. 根据复杂度选择输出级别：
   - **Lite**：Source Index + Requirement Snapshot + Open Questions + Next Actions
   - **Standard**：完整需求事实、业务规则、约束、冲突、待定问题
4. 持久化到 `docs/context/YYYY-MM-DD_HH-MM_<task>_context_bundle.md`
5. 信息模糊/不完整时明确标记并继续

**Output**

- `docs/context/YYYY-MM-DD_HH-MM_<task>_context_bundle.md`

**Guardrails**

- 需求较小/模糊时使用 Lite 级别
- 信息冲突时标记但不静默解决
- 输出是参考文档，不是 Spec；需要 `/sdd:bootstrap` 才能进入 RIPER 流程
