# SDD-RIPER-ONE: Research & Pre-Research

> 本文件是 `sdd-riper-one` 技能的阶段协议。核心规则见 `references/protocol-core.md`。

## RESEARCH（第一个 RIPER 阶段）

- 状态：`[LOCKED]`
- 动作：
  1. 分析用户输入/代码库
  2. 加载或生成 Codemap 索引（见下方 Codemap 协议）
  3. 加载或构建 Context Bundle（见下方 Context Bundle 协议）
  4. 识别未知项，检查模糊约束
  5. 立即在磁盘上创建/更新 Spec 文件
- 决策门：
  1. MAP ONLY → 留在 RESEARCH
  2. 复杂任务 → 进入 INNOVATE
  3. 标准/小型任务 → 进入 PLAN（跳过 INNOVATE，在 Spec §3 记录跳过原因）
- 暂停点：触发 STOP-AND-WAIT

## INNOVATE（可选 — 复杂场景）

- 状态：`[LOCKED]`
- 触发：仅在 RESEARCH 中明确需要时进入
- 动作：
  1. 分析权衡（利/弊），产出 2-3 个方案
  2. 更新 Spec → §3 Innovate
- 下一步：用户选择方案 → 进入 PLAN
- 暂停点：输出策略，停止并等待用户指令

## CODE MAP 协议

Codemap 是代码库的**索引和上下文切片**，将大型代码库压缩为按需加载的局部上下文。对于遗留/大型项目，建议按功能切片增量构建，形成可复用的长期资产。

**触发**："MAP"、"链路梳理"、"只看代码"

**动作**：
1. 进入/留在 RESEARCH 模式
2. 扫描与映射：
   - `feature` 模式：入口点、核心逻辑、数据模型、依赖
   - `project` 模式：架构分层、核心模块、跨模块流程、外部依赖、风险热区
3. 持久化到 `docs/codemap/YYYY-MM-DD_HH-MM_<name>功能.md`（feature）或 `docs/codemap/YYYY-MM-DD_HH-MM_<name>项目总图.md`（project）
4. project 模式建议包含 Mermaid 架构图 + 主流程图；受限时可用结构化文字替代
5. 更新 Spec §1.2 Codemap Used 的引用（简短引用，不完整复制）
6. 不要进入 PLAN，不要提出实现步骤

**输出格式**（推荐结构）：

```markdown
## Codemap: <scope>
### Entry Points
- ...
### Core Logic
- ...
### Data Models
- ...
### Dependencies
- ...
### Risk Hotspots
- ...
```

## CODEMAP STALENESS DETECTION

Codemap 是时间点索引。当 Execute 变更触及 codemap 中索引的文件/流程时，该 codemap 变为过期。

**过期状态**：

| 状态 | 含义 |
|------|------|
| Fresh | Codemap 与当前代码库一致 |
| Stale | Execute 变更触及了此 codemap 中索引的文件/流程 |
| Refreshed | 过期后已重新生成 |

**检测节点（强制）**：

1. **EXECUTE 逐项检测**：每完成一个 checklist 项，将变更文件与 Spec §1.2 Codemap Used 交叉比对。命中 → 标记 Stale。仅比较文件路径，不做完整内容 diff。
2. **REVIEW 前审计**：重读 §1.2 检查过期状态。Stale → 警告用户，在 §6 Review Verdict 中注明哪些证据来自直接代码阅读 vs 过期 codemap。
3. **FAST 执行后同步**：FAST 变更后同样运行逐项检测。
4. **Resume 恢复时**：发现 Stale codemap 警告用户。

**刷新规则**：
- Review 完成时如有 Stale codemap → 附加后续建议刷新
- 用户可随时运行 `/sdd:codemap` 重新生成
- 新文件替换过期文件，Spec §1.2 更新为 Refreshed 并指向新文件路径
- 归档时注明过期 codemap

**过期判定范围**：
- feature 模式：已索引的入口点、核心类、数据模型或依赖链变更触发
- project 模式：架构层变更、模块边界移动、跨模块流程修改触发
- 不相关文件变更不触发

Spec §1.2 新增字段：`Staleness: Fresh/Stale/Refreshed` + `Stale Reason`

## CONTEXT BUNDLE 协议

**触发**："整理上下文"、"汇总需求文档"、"读取这个目录做 bundle"

**动作**：
1. 读取目录中的可用文件（文本/文档/图片等），使用尽力解析。无法解析的文件记录在 Unparsed Sources 列表
2. 提取需求事实和约束，附带来源引用
3. 选择输出级别：
   - `Lite`：Source Index + Requirement Snapshot + Open Questions + Next Actions
   - `Standard`：完整需求事实、业务规则、约束、冲突、待定问题
4. 持久化到 `docs/context/YYYY-MM-DD_HH-MM_<task>_context_bundle.md`
5. 信息模糊/不完整时明确标记并继续
