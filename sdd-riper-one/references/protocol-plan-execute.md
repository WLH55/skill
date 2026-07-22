# SDD-RIPER-ONE: Plan & Execute

> 本文件是 `sdd-riper-one` 技能的阶段协议。核心规则见 `references/protocol-core.md`。

## PLAN（契约 — 严格）

- 状态：`[LOCKED]`
- 目标：创建可审查的蓝图。人类审查点。
- 动作：
  1. 更新 Spec → §4 Plan
  2. 必须内容：
     - **File Changes**：精确文件路径 + 变更说明
     - **Signatures**：精确函数/类名、参数、返回类型
     - **Implementation Checklist**：原子化执行步骤
  3. 约束：不包含实际代码实现，只有规格说明。禁止模糊。
- 下一步：用户批准 → 进入 EXECUTE
- 暂停点：触发 STOP-AND-WAIT

## REVIEW_SPEC（建议性预审）

- 状态：`[LOCKED]`
- 触发：Plan 完成后，用户希望执行前质量检查
- 动作：
  1. 重读当前阶段相关的 Spec 章节（阶段感知）
  2. 评估：
     - 需求清晰度和验收可验证性
     - Plan 可执行性（File Changes、Signatures、Checklist）
     - 风险/回滚覆盖度
     - 跨项目契约完整性（如有）
  3. 持久化到 Spec §4.4 Spec Review Notes：
     - Spec Review Matrix（PASS/FAIL/PARTIAL + 证据）
     - Readiness Verdict：GO/NO-GO（建议性）
     - Risks & Suggestions
     - Phase Reminders（属于后续阶段但当前缺失的内容）
- 阶段感知规则：
  - 不要求所有 Spec 章节一次完成
  - 属于未来阶段的内容列为 Reminder，不作为阻塞依据
- 建议性规则（非阻塞）：
  - NO-GO 不硬性阻塞执行
  - 用户继续执行需记录：`User Decision: Proceed despite NO-GO`

## EXECUTE（构建者）

- 状态：`[ACTIVE]`
- 执行策略：
  - **默认（逐步执行）**：实现一个 checklist 项 → 触发 STOP-AND-WAIT（最适合调试/关键路径）
  - **Batch Override**：触发词 "全部"/"all"/"execute all"/"一次性完成" → 按顺序实现所有剩余 checklist 项
    - 即使批量模式，每个逻辑文件完成后仍必须保存
    - 遇到逻辑冲突或缺失 spec 细节 → 立即停止
- 动作：
  1. 读取 Spec §4 Checklist
  2. 执行实现（根据命令执行单项或全量）
  3. 验证代码与 Spec 签名匹配
  4. Codemap Staleness Check：每次逻辑文件变更后，与 Spec §1.2 交叉比对
- 约束：零偏差。Plan 是契约。
- 错误处理：bug 需要逻辑变更 → 停止 → 报告 → 返回 PLAN

## FAST（极速通道）

- 状态：`[ACTIVE]`（写穿缓存策略）
- 触发：用户明确声明具体、孤立的变更，或非代码任务（文档/摘要/翻译/格式化）
- 工作流（压缩）：
  1. 绕过 RESEARCH 和 PLAN
  2. 立即实现
  3. 编码后必须静默更新 Spec 匹配新现实
- 允许：UI 微调、配置、单文件逻辑、typo、日志
- 升级：任务涉及 >2 个核心文件或架构 → 暂停，请求切换到 PLAN
