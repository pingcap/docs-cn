---
title: AI Integrations for TiDB
summary: An overview of AI integrations for TiDB, including Auto Embedding providers, AI frameworks, ORM libraries, cloud services, and MCP server support.
aliases: ['/zh/tidb/stable/vector-search-integration-overview/','/zh/tidb/dev/vector-search-integration-overview/','/zh/tidbcloud/vector-search-integration-overview/']
---

# AI Integrations for TiDB

本文档概述了 TiDB 的 AI 集成，包括 Auto Embedding 提供方、AI 框架、对象关系映射（ORM）库、云服务和 MCP server 支持。

> **注意：**
>
> - 向量搜索功能目前为 beta 版本，可能会在未提前通知的情况下发生变更。如果你发现了 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。
> - 向量搜索功能适用于 [TiDB Self-Managed](/overview.md)、[TiDB Cloud Starter](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#starter)、[TiDB Cloud Essential](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#essential) 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#tidb-cloud-dedicated)。对于 TiDB Self-Managed 和 TiDB Cloud Dedicated，TiDB 版本需为 v8.4.0 或更高（推荐 v8.5.0 或更高）。

## Auto Embedding {#auto-embedding}

[Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) 功能让你可以直接使用纯文本执行向量搜索。TiDB 会在后台自动将文本转换为向量，因此你无需自行生成或管理嵌入。

TiDB 向量搜索支持存储最多 16383 维的向量，可满足大多数嵌入模型的需求。

你既可以使用自行部署的开源嵌入模型，也可以使用第三方嵌入 API 来生成向量。

下表列出了支持的嵌入提供方。有关如何配置各提供方的详细信息，请参见对应指南。

| Provider          | Guide                                                                                |
|-------------------|--------------------------------------------------------------------------------------|
| OpenAI            | [OpenAI](/ai/integrations/vector-search-auto-embedding-openai.md)                    |
| OpenAI Compatible | [OpenAI Compatible](/ai/integrations/embedding-openai-compatible.md)                 |
| Jina AI           | [Jina AI](/ai/integrations/vector-search-auto-embedding-jina-ai.md)                  |
| Cohere            | [Cohere](/ai/integrations/vector-search-auto-embedding-cohere.md)                    |
| Google Gemini     | [Google Gemini](/ai/integrations/vector-search-auto-embedding-gemini.md)             |
| Hugging Face      | [Hugging Face](/ai/integrations/vector-search-auto-embedding-huggingface.md)         |
| NVIDIA NIM        | [NVIDIA NIM](/ai/integrations/vector-search-auto-embedding-nvidia-nim.md)            |
| Amazon Titan      | [Amazon Titan](/ai/integrations/vector-search-auto-embedding-amazon-titan.md)        |

## ORM libraries {#orm-libraries}

你可以将 TiDB 向量搜索与 ORM 库集成，以便与 TiDB 数据库进行交互。

下表列出了支持的 ORM 库及其对应的集成教程：

| 语言 | ORM/客户端 | 安装说明 | 教程 |
|----------|--------------------|-----------------------------------|----------|
| Python   | SQLAlchemy         | `pip install tidb-vector`         | [集成 TiDB 向量搜索与 SQLAlchemy](/ai/integrations/vector-search-integrate-with-sqlalchemy.md) |
| Python   | peewee             | `pip install tidb-vector`         | [集成 TiDB 向量搜索与 peewee](/ai/integrations/vector-search-integrate-with-peewee.md) |
| Python   | Django             | `pip install django-tidb[vector]` | [集成 TiDB 向量搜索与 Django](/ai/integrations/vector-search-integrate-with-django-orm.md) |

## AI 框架

TiDB 官方支持以下 AI 框架，帮助你轻松将使用这些框架开发的 AI 应用集成到 TiDB 向量搜索中。

| AI framework | Tutorial                                                                                          |
|---------------|---------------------------------------------------------------------------------------------------|
| LangChain     | [Integrate Vector Search with LangChain](/ai/integrations/vector-search-integrate-with-langchain.md)   |
| LlamaIndex    | [Integrate Vector Search with LlamaIndex](/ai/integrations/vector-search-integrate-with-llamaindex.md) |

你还可以将 TiDB 用于 AI 应用的文档存储、知识图谱存储等多种场景。

## Cloud services

你可以使用第三方云嵌入服务生成向量并将其存储在 TiDB 中。

下表列出了支持的云服务及其对应的教程：

| Cloud service  | Tutorial                                                                                                                  |
|----------------|---------------------------------------------------------------------------------------------------------------------------|
| Jina AI        | [Integrate Vector Search with Jina AI Embeddings API](/ai/integrations/vector-search-integrate-with-jinaai-embedding.md)  |
| Amazon Bedrock | [Integrate TiDB Vector Search with Amazon Bedrock](/ai/integrations/vector-search-integrate-with-amazon-bedrock.md)       |

## MCP server

[TiDB MCP Server](/ai/integrations/tidb-mcp-server.md) 是一个开源工具，让你能够通过 Model Context Protocol (MCP) 使用自然语言指令与 TiDB 数据库进行交互。

下表列出了支持的 MCP 客户端及其对应的设置指南：

| MCP client     | Guide                                                                  |
|----------------|------------------------------------------------------------------------|
| Claude Code    | [Claude Code](/ai/integrations/tidb-mcp-claude-code.md)                |
| Claude Desktop | [Claude Desktop](/ai/integrations/tidb-mcp-claude-desktop.md)          |
| Cursor         | [Cursor](/ai/integrations/tidb-mcp-cursor.md)                          |
| VS Code        | [VS Code](/ai/integrations/tidb-mcp-vscode.md)                         |
| Windsurf       | [Windsurf](/ai/integrations/tidb-mcp-windsurf.md)                      |
