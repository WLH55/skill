---
name: "SDD: Fix"
description: "零 spec 快修：适用于纯机械性改动"
skill: sdd-riper-one
---

零 spec 快修通道。适用于纯机械性改动，跳过 spec 直接执行。

本命令属于 `sdd-riper-one` 技能。未加载技能时请先执行 `/sdd-riper-one`。

**Input**: `/sdd:fix <修改描述>`

**适用范围**

- typo 修复
- 日志添加
- 配置值变更
- import 整理
- 其他无决策性的单点修改

**Steps**

1. 快速判断复杂度
   - 如果确实是纯机械改动 → 直接执行
   - 如果发现涉及决策 → 立即升级到 `/sdd:ff`
2. 执行修改
3. 用一句话 summary 回写（不创建 spec 文件）

**Guardrails**

- 一旦发现复杂度超出预期，立即升级到 `/sdd:ff` 或 `/sdd:bootstrap`
- 不适用于：架构改动、跨文件逻辑变更、需求不明确的修改
- 每次只处理一个改动，不要批量
