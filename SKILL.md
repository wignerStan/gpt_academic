# GPT Academic Skills

This document lists the core capabilities available to the agent.

## Core Functions
These are text processing functions usually applied to the current input.

### 学术语料润色

### 总结绘制脑图

### 查找语法错误

### 中译英

### 学术英中互译

### 英译中

### 找图片

### 解释代码

### 参考文献转Bib

## Crazy Functions (Plugins)
These are complex functions that can handle files, perform searches, etc.

### Group: 智能体
#### 多媒体智能体
- **Description**: 【仅测试】多媒体任务

#### 动态代码解释器（CodeInterpreter）
- **Description**: No description available.

### Group: 对话|编程|学术|智能体
#### 虚空终端
- **Description**: 使用自然语言实现您的想法

### Group: 编程
#### 解析整个Python项目
- **Description**: 解析一个Python项目的所有源文件(.py) | 输入参数为路径

#### 注释Python项目
- **Description**: 上传一系列python源文件(或者压缩包), 为这些代码添加docstring | 输入参数为路径

#### 解析整个Matlab项目
- **Description**: 解析一个Matlab项目的所有源文件(.m) | 输入参数为路径

#### 解析整个C++项目头文件
- **Description**: 解析一个C++项目的所有头文件(.h/.hpp) | 输入参数为路径

#### 解析整个C++项目（.cpp/.hpp/.c/.h）
- **Description**: 解析一个C++项目的所有源文件（.cpp/.hpp/.c/.h）| 输入参数为路径

#### 解析整个Go项目
- **Description**: 解析一个Go项目的所有源文件 | 输入参数为路径

#### 解析整个Rust项目
- **Description**: 解析一个Rust项目的所有源文件 | 输入参数为路径

#### 解析整个Java项目
- **Description**: 解析一个Java项目的所有源文件 | 输入参数为路径

#### 解析整个前端项目（js,ts,css等）
- **Description**: 解析一个前端项目的所有源文件（js,ts,css等） | 输入参数为路径

#### 解析整个Lua项目
- **Description**: 解析一个Lua项目的所有源文件 | 输入参数为路径

#### 解析整个CSharp项目
- **Description**: 解析一个CSharp项目的所有源文件 | 输入参数为路径

#### 解析Jupyter Notebook文件
- **Description**: 解析Jupyter Notebook文件 | 输入参数为路径
- **Advanced Arguments**: 若输入0，则不解析notebook中的Markdown块

#### 翻译README或MD
- **Description**: 将Markdown翻译为中文 | 输入参数为路径或URL

#### 翻译Markdown或README（支持Github链接）
- **Description**: 将Markdown或README翻译为中文 | 输入参数为路径或URL

#### 批量生成函数注释
- **Description**: 批量生成函数的注释 | 输入参数为路径

#### 批量Markdown中译英（输入路径或上传压缩包）
- **Description**: 批量将Markdown文件中文翻译为英文 | 输入参数为路径或上传压缩包

#### 解析项目源代码（手动指定和筛选源代码文件类型）
- **Description**: No description available.
- **Advanced Arguments**: 输入时用逗号隔开, *代表通配符, 加了^代表不匹配; 不输入代表全部匹配。例如: "*.c, ^*.cpp, config.toml, ^*.toml"

#### Markdown翻译（指定翻译成何种语言）
- **Description**: No description available.
- **Advanced Arguments**: 请输入要翻译成哪种语言，默认为Chinese。

### Group: 对话
#### 载入对话历史存档（先上传存档或输入路径）
- **Description**: 载入对话历史存档 | 输入参数为路径

#### 删除所有本地对话历史记录（谨慎操作）
- **Description**: 删除所有本地对话历史记录，谨慎操作 | 不需要输入参数

#### 清除所有缓存文件（谨慎操作）
- **Description**: 清除所有缓存文件，谨慎操作 | 不需要输入参数

#### 生成多种Mermaid图表(从当前对话或路径(.pdf/.md/.docx)中生产图表）
- **Description**: 基于当前对话或文件生成多种Mermaid图表,图表类型由模型判断

#### 保存当前的对话
- **Description**: 保存当前的对话 | 不需要输入参数

#### 查互联网后回答
- **Description**: No description available.

#### 历史上的今天
- **Description**: 查看历史上的今天事件 (这是一个面向开发者的插件Demo) | 不需要输入参数

#### 询问多个GPT模型
- **Description**: No description available.

#### 🎨图片生成（DALLE2/DALLE3, 使用前切换到GPT系列模型）
- **Description**: 使用 DALLE2/DALLE3 生成图片 | 输入参数字符串，提供图像的内容

#### 🎨图片修改_DALLE2 （使用前请切换模型到GPT系列）
- **Description**: No description available.

#### 询问多个GPT模型（手动指定询问哪些模型）
- **Description**: No description available.
- **Advanced Arguments**: 支持任意数量的llm接口，用&符号分隔。例如chatglm&gpt-3.5-turbo&gpt-4

#### 批量总结音视频（输入路径或上传压缩包）
- **Description**: 批量总结音频或视频 | 输入参数为路径
- **Advanced Arguments**: 调用openai api 使用whisper-1模型, 目前支持的格式:mp4, m4a, wav, mpga, mpeg, mp3。此处可以输入解析提示，例如：解析为简体中文（默认）。

#### 数学动画生成（Manim）
- **Description**: 按照自然语言描述生成一个动画 | 输入参数是一段话

#### 构建知识库（先上传文件素材,再运行此插件）
- **Description**: No description available.
- **Advanced Arguments**: 此处待注入的知识库名称id, 默认为default。文件进入知识库后可长期保存。可以通过再次调用本插件的方式，向知识库追加更多文档。

#### 知识库文件注入（构建知识库后,再运行此插件）
- **Description**: No description available.
- **Advanced Arguments**: 待提取的知识库名称id, 默认为default, 您需要构建知识库后再运行此插件。

#### 交互功能模板Demo函数（查找wallhaven.cc的壁纸）
- **Description**: No description available.

#### Rag智能召回
- **Description**: 将问答数据记录到向量库中，作为长期参考。

#### 实时语音对话
- **Description**: 这是一个时刻聆听着的语音对话助手 | 没有输入参数

### Group: 学术
#### Arxiv论文翻译
- **Description**: ArXiv论文精细翻译 | 输入参数arxiv论文的ID，比如1812.10695

#### 批量总结Word文档
- **Description**: 批量总结word文档 | 输入参数为路径

#### 读Tex论文写摘要
- **Description**: 读取Tex论文并写摘要 | 输入参数为路径

#### PDF论文翻译
- **Description**: 精准翻译PDF论文为中文 | 输入参数为路径

#### 批量总结PDF文档
- **Description**: 批量总结PDF文档的内容 | 输入参数为路径

#### 谷歌学术检索助手（输入谷歌学术搜索页url）
- **Description**: 使用谷歌学术检索助手搜索指定URL的结果 | 输入参数为谷歌学术搜索页的URL

#### 理解PDF文档内容 （模仿ChatPDF）
- **Description**: 理解PDF文档的内容并进行回答 | 输入参数为路径

#### 英文Latex项目全文润色（输入路径或上传压缩包）
- **Description**: 对英文Latex项目全文进行润色处理 | 输入参数为路径或上传压缩包

#### 中文Latex项目全文润色（输入路径或上传压缩包）
- **Description**: 对中文Latex项目全文进行润色处理 | 输入参数为路径或上传压缩包

#### Latex英文纠错+高亮修正位置 [需Latex]
- **Description**: No description available.
- **Advanced Arguments**: 如果有必要, 请在此处追加更细致的矫错指令（使用英文）。

#### 📚Arxiv论文精细翻译（输入arxivID）[需Latex]
- **Description**: ArXiv论文精细翻译 | 输入参数arxiv论文的ID，比如1812.10695
- **Advanced Arguments**: 如果有必要, 请在此处给出自定义翻译命令, 解决部分词汇翻译不准确的问题。 例如当单词'agent'翻译不准确时, 请尝试把以下指令复制到高级参数区: If the term "agent" is used in this section, it should be translated to "智能体".

#### 📚本地Latex论文精细翻译（上传Latex项目）[需Latex]
- **Description**: 本地Latex论文精细翻译 | 输入参数是路径
- **Advanced Arguments**: 如果有必要, 请在此处给出自定义翻译命令, 解决部分词汇翻译不准确的问题。 例如当单词'agent'翻译不准确时, 请尝试把以下指令复制到高级参数区: If the term "agent" is used in this section, it should be translated to "智能体".

#### PDF翻译中文并重新编译PDF（上传PDF）[需Latex]
- **Description**: PDF翻译中文，并重新编译PDF | 输入参数为路径
- **Advanced Arguments**: 如果有必要, 请在此处给出自定义翻译命令, 解决部分词汇翻译不准确的问题。 例如当单词'agent'翻译不准确时, 请尝试把以下指令复制到高级参数区: If the term "agent" is used in this section, it should be translated to "智能体".

#### 批量文件询问 (支持自定义总结各种文件)
- **Description**: 先上传文件，点击此按钮，进行提问

#### 一键下载arxiv论文并翻译摘要（先在input输入编号，如1812.10695）
- **Description**: No description available.

#### 精准翻译PDF文档（NOUGAT）
- **Description**: No description available.

#### 速读论文
- **Description**: 上传一篇论文进行快速分析和解读 |  输入参数为论文路径或DOI/arXiv ID

### Group: 对话|编程
#### [多线程Demo]解析此项目本身（源码自译解）
- **Description**: 多线程解析并翻译此项目的源码 | 不需要输入参数
