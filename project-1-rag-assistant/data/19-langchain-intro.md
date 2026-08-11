# LangChain 入门

## 什么是 LangChain

LangChain 是构建 LLM 应用的框架，提供链式调用、工具集成、记忆管理等组件。作用是将 LLM 调用标准化、可组合化。

## 核心组件

Chain：将多个 LLM 调用串联，前一步输出作为后一步输入
Prompt Template：可复用的提示词模板，支持变量替换
Memory：对话历史管理，支持滑动窗口、摘要等策略
Tool：让 LLM 调用外部工具（搜索、计算器、API）

## RAG 中的 LangChain

LangChain 提供了完整的 RAG 工具链：Document Loaders 加载文档、Text Splitters 切分、Vector Stores 存储、Retrievers 检索。但学习阶段建议先手写理解原理，再迁移到框架。

## 注意事项

LangChain 版本迭代快，API 不稳定。生产项目越来越多选择轻量方案：直接调 OpenAI SDK + 自建 pipeline。理解底层原理后，框架只是提速工具而非必需品。
