---
name: prompt-查找语法错误
description: Execute the '查找语法错误' prompt template. Use when the user wants to perform '查找语法错误' or apply this specific prompt pattern.
type: prompt
---

# 查找语法错误

## Quick start
Use this skill to wrap your input with the defined prompt template.

## Instructions
The system will apply the following prefix and suffix to the user input.

**Prefix**:
```text
Help me ensure that the grammar and the spelling is correct. Do not try to polish the text, if no mistake is found, tell me that this paragraph is good. If you find grammar or spelling mistakes, please list mistakes you find in a two-column markdown table, put the original text the first column, put the corrected text in the second column and highlight the key words you fixed. Finally, please provide the proofreaded text.

Example:
Paragraph: How is you? Do you knows what is it?
| Original sentence | Corrected sentence |
| :--- | :--- |
| How **is** you? | How **are** you? |
| Do you **knows** what **is** **it**? | Do you **know** what **it** **is** ? |

Below is a paragraph from an academic paper. You need to report all grammar and spelling mistakes as the example before.


```

**Suffix**:
```text

```

## Examples
User: "Apply 查找语法错误 to this text: ..."
Agent: [Executes skill]

## Requirements
- None
