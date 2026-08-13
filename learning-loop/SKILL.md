---
name: learning-loop
description: "Run a 10-step research-to-mastery learning loop with two modes: quick (output-first, ~2.5h) and standard (full depth, ~1 week). Pipeline: STORM multi-perspective research, contradiction map, brief, peer review, 5 curated resources, learning ladder, 2h core-20% hands-on, exam-style retrieval quiz, Feynman loop, 1-page cheatsheet. Output stages 7-10 are mandatory in both modes. Use when the user wants to seriously learn or master a topic instead of just getting an explanation (学习/学会/系统学/把X学透/分阶段学/快速学习/按阶段推进), wants to resume an ongoing learning session, or asks to apply the 多视角+矛盾+测试+压缩+反馈 closed loop."
---

# Learning Loop

10 步闭环把陌生主题学扎实。两种模式，共同底线：**输出必做**（核心 20% 动手练、考官自测、费曼复述、一页速查表），输入阶段（调研/矛盾/简报/评审/资源/阶梯）可压缩裁剪。

## 核心认知

- 学习要有结构，不是「问 AI 讲讲 X」。
- 真学习 = 多视角 + 矛盾 + 测试 + 压缩 + 反馈。
- 输入型学习伪造「懂了」，检索练习（考/讲）才长记忆。
- 资源在精不在多：5 个用完远胜 500 个收藏。
- 输出是学习的落点：AI 写的是教材，用户写/讲/答的才是用户的产出。

## 模式

- `quick` 快速（约 2.5 小时，一次会话）：storm(压缩) → brief(压缩) → core20(快剪) → quiz(迷你) → feynman(单轮) → cheatsheet
- `standard` 标准（一周，分 2-3 次会话）：完整 10 步 storm → conflict → brief → review → resources → ladder → core20 → quiz → feynman → cheatsheet
- 默认 standard；用户说「快速/没时间/先了解个大概」才用 quick。
- 压缩规则、时间盒、产物规格见 `references/modes.md`。绝不擅自砍掉 7-10 中的任何一步。

## 启动流程

1. 确认主题。用户未给出时先问。
2. 确认模式（默认 standard，向用户说明）。
3. 初始化会话：`python scripts/session.py init "<主题>" --mode <quick|standard>`
   会话目录默认 `<cwd>/learning-sessions/<主题>/`；用户指定路径时用 `--dir`。
4. 从 `current` 阶段开始执行。

## 状态与推进

- `session.json` 是唯一状态源；每阶段产物写入独立 markdown（`01-storm.md` … `10-cheatsheet.md`）。
- 每完成一个阶段：运行 `python scripts/session.py advance <stage>` 推进状态 → 向用户汇报 ≤3 条要点 → 问是否继续下一阶段。
- 用户说「继续/暂停/看进度」：运行 `python scripts/session.py status`，从 `current` 恢复，绝不重建已存在的会话。
- 存在多个会话时，先列出让用户选择主题。
- 快速模式想升级：运行 `python scripts/session.py upgrade`，再补跑缺失阶段（conflict/review/resources/ladder）。
- 若 python 不可用：按 `session.json` 格式（topic/mode/pipeline/completed/current）手动维护状态。

## 阶段执行规则

- 每阶段提示词在 `references/stage-prompts.md`，把 `{主题}`/`{概念}` 替换为真实主题后执行；7-10 按模式选「标准全量版」或「快速压缩版」。
- 阶段间上下文必须传递：后一阶段以前一阶段产物为输入（conflict 用 storm 的五视角，brief 用 storm+conflict，review 评审 brief），不得重开炉灶。
- 输出阶段（7-10）硬性要求：
  - core20：产物里必须有用户做练习/小项目的记录，不是只有计划。
  - quiz：一次只问一题，等用户回答；逐题打分、指差距、记入 `08-quiz-log.md`；绝不一次性输出全部题目。
  - feynman：让用户用自己的话讲，只补含糊/跳步/绕不过去的洞；讲清楚前不进入新内容；把用户复述原文记入 `09-feynman-log.md`。
  - cheatsheet：最终交付物，用短条目，不用长段落。
- 其余阶段为生成型，直接产出并保存。

## 完成

- 最后产出 `10-cheatsheet.md`，并用 3-5 句话总结：已掌握什么、薄弱点、下一步建议。
- 告知用户会话已归档，之后用 `$learning-loop` 配主题可随时重开或复习。
