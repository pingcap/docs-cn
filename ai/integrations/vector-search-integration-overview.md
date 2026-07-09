---
title: TiDB 支持的 AI 集成
summary: TiDB 支持的 AI 集成概览，包括 Auto Embedding 提供商、AI 框架、对象关系映射库、云服务和 MCP server。
aliases: ['/zh/tidb/stable/vector-search-integration-overview/','/zh/tidb/dev/vector-search-integration-overview/','/zh/tidbcloud/vector-search-integration-overview/']
---

# TiDB 支持的 AI 集成

本文档概述了 TiDB 支持的 AI 集成，包括 Auto Embedding 提供商、AI 框架、对象关系映射（ORM）库、云服务以及 MCP server。

> **注意：**
>
> - 向量搜索功能目前处于 beta 阶段，可能会在不事先通知的情况下发生变更。如果你发现 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。
> - 向量搜索功能适用于 [TiDB Self-Managed](/overview.md) 和 [{{{ .starter }}}](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#starter)。对于 TiDB Self-Managed，TiDB 版本需为 v8.4.0 或更高（推荐 v8.5.0 及以上）。

## Auto Embedding {#auto-embedding}

[Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) 功能使你能够直接使用纯文本执行向量搜索。TiDB 会在后台自动将文本转换为向量，因此你无需自行生成或管理 embedding。

TiDB 向量搜索支持存储最多 16383 维的向量，能够满足大多数 embedding 模型的需求。

你既可以使用自行部署的开源 embedding 模型，也可以使用第三方 embedding API 来生成向量。

下表列出了支持的 embedding 提供商。有关如何配置各提供商的详细信息，请参见对应的指南。

| 提供商          | 指南                                                                                |
|-------------------|--------------------------------------------------------------------------------------|
| OpenAI            | [OpenAI](/ai/integrations/vector-search-auto-embedding-openai.md)                    |
| OpenAI Compatible | [OpenAI Compatible](/ai/integrations/embedding-openai-compatible.md)                 |
| Jina AI           | [Jina AI](/ai/integrations/vector-search-auto-embedding-jina-ai.md)                  |
| Cohere            | [Cohere](/ai/integrations/vector-search-auto-embedding-cohere.md)                    |
| Google Gemini     | [Google Gemini](/ai/integrations/vector-search-auto-embedding-gemini.md)             |
| Hugging Face      | [Hugging Face](/ai/integrations/vector-search-auto-embedding-huggingface.md)         |
| NVIDIA NIM        | [NVIDIA NIM](/ai/integrations/vector-search-auto-embedding-nvidia-nim.md)            |
| Amazon Titan      | [Amazon Titan](/ai/integrations/vector-search-auto-embedding-amazon-titan.md)        |

## AI 框架 {#ai-frameworks}

TiDB 为以下 AI 框架提供官方支持，使你能够轻松将基于这些框架开发的 AI 应用集成到 TiDB 向量搜索中。

| AI 框架 | 教程                                                                                          |
|---------------|---------------------------------------------------------------------------------------------------|
| LangChain     | [Integrate Vector Search with LangChain](/ai/integrations/vector-search-integrate-with-langchain.md)   |
| LlamaIndex    | [Integrate Vector Search with LlamaIndex](/ai/integrations/vector-search-integrate-with-llamaindex.md) |

你还可以将 TiDB 用于 AI 应用中的多种任务，例如文档存储和知识图谱存储。

## ORM 库 {#orm-libraries}

你可以将 TiDB 向量搜索与你的 ORM 库集成，以便与 TiDB 数据库交互。

下表列出了支持的 ORM 库及其对应的集成教程：

| 语言 | ORM/Client         | 如何安装                    | 教程 |
|----------|--------------------|-----------------------------------|----------|
| Python   | SQLAlchemy         | `pip install tidb-vector`         | [Integrate TiDB Vector Search with SQLAlchemy](/ai/integrations/vector-search-integrate-with-sqlalchemy.md) |
| Python   | peewee             | `pip install tidb-vector`         | [Integrate TiDB Vector Search with peewee](/ai/integrations/vector-search-integrate-with-peewee.md) |
| Python   | Django             | `pip install django-tidb[vector]` | [Integrate TiDB Vector Search with Django](/ai/integrations/vector-search-integrate-with-django-orm.md) |

## 云服务 {#cloud-services}

你可以使用第三方云 embedding 服务生成向量，并将其存储到 TiDB 中。

下表列出了支持的云服务及其对应的教程：

| 云服务  | 教程                                                                                                                  |
|----------------|---------------------------------------------------------------------------------------------------------------------------|
| Jina AI        | [Integrate Vector Search with Jina AI Embeddings API](/ai/integrations/vector-search-integrate-with-jinaai-embedding.md)  |
| Amazon Bedrock | [Integrate TiDB Vector Search with Amazon Bedrock](/ai/integrations/vector-search-integrate-with-amazon-bedrock.md)       |

## MCP server {#mcp-server}

[TiDB MCP Server](/ai/integrations/tidb-mcp-server.md) 是一个开源工具，可让你通过 Model Context Protocol (MCP) 使用自然语言指令与 TiDB 数据库进行交互。

下表列出了支持的 MCP 客户端及其对应的设置指南：

| MCP client     | 指南                                                                  |
|----------------|------------------------------------------------------------------------|
| Claude Code    | [Claude Code](/ai/integrations/tidb-mcp-claude-code.md)                |
| Claude Desktop | [Claude Desktop](/ai/integrations/tidb-mcp-claude-desktop.md)          |
| Cursor         | [Cursor](/ai/integrations/tidb-mcp-cursor.md)                          |
| VS Code        | [VS Code](/ai/integrations/tidb-mcp-vscode.md)                         |
| Windsurf       | [Windsurf](/ai/integrations/tidb-mcp-windsurf.md)                      |
