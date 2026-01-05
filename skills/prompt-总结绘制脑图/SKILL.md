---
name: prompt-总结绘制脑图
description: Execute the '总结绘制脑图' prompt template. Use when the user wants to perform '总结绘制脑图' or apply this specific prompt pattern.
type: prompt
---

# 总结绘制脑图

## Quick start
Use this skill to wrap your input with the defined prompt template.

## Instructions
The system will apply the following prefix and suffix to the user input.

**Prefix**:
```text
"""


```

**Suffix**:
```text



"""

使用mermaid flowchart对以上文本进行总结，概括上述段落的内容以及内在逻辑关系，例如：

以下是对以上文本的总结，以mermaid flowchart的形式展示：
```mermaid
flowchart LR
    A["节点名1"] --> B("节点名2")
    B --> C{"节点名3"}
    C --> D["节点名4"]
    C --> |"箭头名1"| E["节点名5"]
    C --> |"箭头名2"| F["节点名6"]
```

注意：
（1）使用中文
（2）节点名字使用引号包裹，如["Laptop"]
（3）`|` 和 `"`之间不要存在空格
（4）根据情况选择flowchart LR（从左到右）或者flowchart TD（从上到下）

```

## Examples
User: "Apply 总结绘制脑图 to this text: ..."
Agent: [Executes skill]

## Requirements
- None
