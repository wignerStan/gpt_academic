---
name: prompt-学术英中互译
description: Execute the '学术英中互译' prompt template. Use when the user wants to perform '学术英中互译' or apply this specific prompt pattern.
type: prompt
---

# 学术英中互译

## Quick start
Use this skill to wrap your input with the defined prompt template.

## Instructions
The system will apply the following prefix and suffix to the user input.

**Prefix**:
```text
<gpt_academic_string_mask><lang_english>你是经验丰富的翻译，请把以下学术文章段落翻译成中文，并同时充分考虑中文的语法、清晰、简洁和整体可读性，必要时，你可以修改整个句子的顺序以确保翻译后的段落符合中文的语言习惯。你需要翻译的文本如下：</lang_english><lang_chinese>I want you to act as a scientific English-Chinese translator, I will provide you with some paragraphs in one language and your task is to accurately and academically translate the paragraphs only into the other language. Do not repeat the original provided paragraphs after translation. You should use artificial intelligence tools, such as natural language processing, and rhetorical knowledge and experience about effective writing techniques to reply. I'll give you my paragraphs as follows, tell me what language it is written in, and then translate:</lang_chinese></gpt_academic_string_mask>


```

**Suffix**:
```text

```

## Examples
User: "Apply 学术英中互译 to this text: ..."
Agent: [Executes skill]

## Requirements
- None
