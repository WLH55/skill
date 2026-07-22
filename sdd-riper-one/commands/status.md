---
name: "SDD: Status"
description: "查看所有活跃 spec 的状态概览"
skill: sdd-riper-one
---

查看所有 spec 文件的状态概览。

本命令属于 `sdd-riper-one` 技能。未加载技能时请先执行 `/sdd-riper-one`。

**Input**: `/sdd:status`（无参数）

**Steps**

1. 扫描 `docs/specs/` 目录下所有 `.md` 文件
2. 读取每个文件的顶部状态块（前 10 行即可）
3. 输出状态汇总表：

| Spec | Phase | Goal | Last | Next | Approval |
|------|-------|------|------|------|----------|
| ... | ... | ... | ... | ... | ... |

4. 标注异常状态：
   - Phase 为 execute 但无 Approval 的 spec
   - 长时间未更新的 spec（> 7 天）
   - Codemap 标记为 Stale 的 spec

**Output**

- 聊天中输出状态汇总表 + 异常提示
