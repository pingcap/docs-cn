---
title: TiDB for AI
summary: 利用 TiDB 集成的向量检索、全文检索和无缝 Python SDK 构建现代 AI 应用。
---

# TiDB for AI

TiDB 是为现代 AI 应用设计的分布式 SQL 数据库，提供集成的向量检索、全文检索和混合检索能力。本文档概述了使用 TiDB 构建 AI 驱动应用可用的 AI 特性和工具。

## 快速开始

快速体验 TiDB 的 AI 能力。

| 文档 | 描述 |
| --- | --- |
| [Get Started with Python](/ai/quickstart-via-python.md) | 使用 Python 在几分钟内构建你的第一个基于 TiDB 的 AI 应用。 |
| [Get Started with SQL](/ai/quickstart-via-sql.md) | 使用 SQL 快速开始向量检索。 |

## 概念

了解 TiDB AI 检索的基础概念。

| 文档 | 描述 |
| --- | --- |
| [Vector Search](/ai/concepts/vector-search-overview.md) | 向量检索的全面概述，包括概念、工作原理和应用场景。 |

## 指南

使用 [`pytidb`](https://github.com/pingcap/pytidb) SDK 或 SQL 构建 AI 应用的分步指南。

| 文档 | 描述 |
| --- | --- |
| [Connect to TiDB](/ai/guides/connect.md) | 使用 `pytidb` 连接 TiDB Cloud 或自建集群。 |
| [Working with Tables](/ai/guides/tables.md) | 创建、查询和管理包含向量字段的表。 |
| [Vector Search](/ai/guides/vector-search.md) | 使用 `pytidb` 进行语义相似度检索。 |
| [Full-Text Search](/ai/guides/vector-search-full-text-search-python.md) | 基于关键字的文本检索，支持 BM25 排序。 |
| [Hybrid Search](/ai/guides/vector-search-hybrid-search.md) | 结合向量检索与全文检索，获得更优结果。 |
| [Image Search](/ai/guides/image-search.md) | 利用多模态嵌入进行 image 检索。 |
| [Auto Embedding](/ai/guides/auto-embedding.md) | 数据插入时自动生成嵌入向量。 |
| [Filtering](/ai/guides/filtering.md) | 通过元信息条件过滤检索结果。 |

## 示例

完整代码示例和演示，展示 TiDB 的 AI 能力。

| 文档 | 描述 |
| --- | --- |
| [Basic CRUD Operations](/ai/examples/basic-with-pytidb.md) | 使用 `pytidb` 进行基础表操作。 |
| [Vector Search](/ai/examples/vector-search-with-pytidb.md) | 语义相似度检索示例。 |
| [RAG Application](/ai/examples/rag-with-pytidb.md) | 构建检索增强生成（RAG）应用。 |
| [Image Search](/ai/examples/image-search-with-pytidb.md) | 基于 Jina AI 嵌入的多模态 image 检索。 |
| [Conversational Memory](/ai/examples/memory-with-pytidb.md) | 为 AI agent 和聊天机器人提供持久 memory。 |
| [Text-to-SQL](/ai/examples/text2sql-with-pytidb.md) | 将自然语言转换为 SQL 查询。 |

## 集成

将 TiDB 集成到主流 AI framework、嵌入提供商和开发工具中。

| 文档 | 描述 |
| --- | --- |
| [Integration Overview](/ai/integrations/vector-search-integration-overview.md) | 所有可用集成的概览。 |
| [Embedding Providers](/ai/integrations/vector-search-auto-embedding-overview.md#available-text-embedding-models) | 为 OpenAI、Cohere、Jina AI 等提供统一接口。 |
| [LangChain](/ai/integrations/vector-search-integrate-with-langchain.md) | 将 TiDB 作为 LangChain 的向量存储。 |
| [LlamaIndex](/ai/integrations/vector-search-integrate-with-llamaindex.md) | 将 TiDB 作为 LlamaIndex 的向量存储。 |
| [MCP Server](/ai/integrations/tidb-mcp-server.md) | 将 TiDB 连接到 Claude Code、Cursor 及其他 AI 驱动的 IDE。 |

## 参考

TiDB AI 与向量检索特性的技术参考文档。

| 文档 | 描述 |
| --- | --- |
| [Vector Data Types](/ai/reference/vector-search-data-types.md) | 向量列类型及其用法。 |
| [Functions and Operators](/ai/reference/vector-search-functions-and-operators.md) | 距离函数与向量运算符。 |
| [Vector Search Index](/ai/reference/vector-search-index.md) | 创建和管理向量索引以提升性能。 |
| [Performance Tuning](/ai/reference/vector-search-improve-performance.md) | 优化向量检索性能。 |
| [Limitations](/ai/reference/vector-search-limitations.md) | 当前的限制与约束。 |