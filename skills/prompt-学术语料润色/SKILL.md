---
name: prompt-学术语料润色
description: Execute the '学术语料润色' prompt template. Use when the user wants to perform '学术语料润色' or apply this specific prompt pattern.
type: prompt
---

# 学术语料润色

## Quick start
Use this skill to wrap your input with the defined prompt template.

## Instructions
The system will apply the following prefix and suffix to the user input.

**Prefix**:
```text
<gpt_academic_string_mask><lang_english>Below is a paragraph from an academic paper. Polish the writing to meet the academic style, improve the spelling, grammar, clarity, concision and overall readability. When necessary, rewrite the whole sentence. Firstly, you should provide the polished paragraph (in English). Secondly, you should list all your modification and explain the reasons to do so in markdown table.</lang_english><lang_chinese>作为一名中文学术论文写作改进助理，你的任务是改进所提供文本的拼写、语法、清晰、简洁和整体可读性，同时分解长句，减少重复，并提供改进建议。请先提供文本的更正版本，然后在markdown表格中列出修改的内容，并给出修改的理由:</lang_chinese></gpt_academic_string_mask>


```

**Suffix**:
```text

```

## Examples
User: "Apply 学术语料润色 to this text: ..."
Agent: [Executes skill]

## Requirements
- None
