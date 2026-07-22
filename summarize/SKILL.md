---
name: summarize
description: Summarize learning materials, book chapters, docs, URLs, PDFs, transcripts, notes, or local files into concise, reusable notes for Codex workflows. Use when the user asks to summarize, compress, extract key points, make chapter notes, produce a teach-back summary, or create review notes after reading.
---

# Summarize

Turn source material into compact notes the user can remember, retell, and reuse.

## Workflow

1. Identify the source type: pasted text, local file, URL, PDF, transcript, notes, or a chapter range.
2. Gather only the needed content:
   - For local files, read the relevant file or section.
   - For URLs or current online content, browse and cite sources.
   - For PDFs/documents, use available document/PDF tooling when direct text read is not enough.
3. Produce a concise summary by default; ask only if the target format or scope is genuinely ambiguous.
4. Preserve uncertainty: mark unclear claims as `待确认` rather than inventing details.
5. If the source is long, chunk internally, summarize each chunk, then merge into a final synthesis.

## Default Output

For learning chapters, use:

```markdown
### 一句话
[用一句话说明本章解决什么问题]

### 核心概念
- [概念 1：一句解释]
- [概念 2：一句解释]
- [概念 3：一句解释]

### 可复述笔记
[3-6 句话，像讲给别人听一样]

### 易混点
- [容易误解/混淆的点]

### 复习问题
1. [检查理解的问题]
2. [检查迁移应用的问题]
```

For technical docs or APIs, prefer:

```markdown
### TL;DR
[2-4 句]

### What Matters
- [关键点]
- [限制/坑]
- [实践建议]

### Apply It
[如何用到当前任务/代码/学习计划]
```

## Style

- Keep it short unless the user asks for detail.
- Favor concrete terms over motivational prose.
- Do not copy long passages from copyrighted sources.
- Include links/citations when browsing or summarizing online sources.
- When summarizing for the user's study system, make the result easy to paste into `journal/` or chapter notes, but do not write files unless the user explicitly asks.
