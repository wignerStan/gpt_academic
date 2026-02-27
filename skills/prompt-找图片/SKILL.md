---
name: prompt-找图片
description: Execute the '找图片' prompt template. Use when the user wants to perform '找图片' or apply this specific prompt pattern.
type: prompt
---

# 找图片

## Quick start
Use this skill to wrap your input with the defined prompt template.

## Instructions
The system will apply the following prefix and suffix to the user input.

**Prefix**:
```text
我需要你找一张网络图片。使用Unsplash API(https://source.unsplash.com/960x640/?<英语关键词>)获取图片URL，然后请使用Markdown格式封装，并且不要有反斜线，不要用代码块。现在，请按以下描述给我发送图片：


```

**Suffix**:
```text

```

## Examples
User: "Apply 找图片 to this text: ..."
Agent: [Executes skill]

## Requirements
- None
