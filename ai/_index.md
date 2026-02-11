---
title: TiDB for AI
summary: 利用 TiDB 的向量搜索、全文搜索和 Python SDK 构建现代 AI 应用。
---

# TiDB for AI

TiDB 是面向 AI 应用的分布式 SQL 数据库，支持向量搜索、全文搜索及混合搜索功能。本文介绍利用 TiDB 开发 AI 应用时可用的 AI 功能与工具。

## 快速开始

快速体验 TiDB 的 AI 能力。

| 文档 | 描述 |
| --- | --- |
| [使用 Python 快速上手](/ai/quickstart-via-python.md) | 使用 Python 在几分钟内构建你的第一个基于 TiDB 的 AI 应用。 |
| [使用 SQL 快速上手](/ai/quickstart-via-sql.md) | 使用 SQL 快速开始向量搜索。 |

## 基础概念

了解 TiDB AI 搜索的基础概念。

| 文档 | 描述 |
| --- | --- |
| [向量搜索](/ai/concepts/vector-search-overview.md) | 向量搜索的全面概述，包括概念、工作原理和应用场景。 |

## 使用指南

使用 TiDB Python SDK [`pytidb`](https://github.com/pingcap/pytidb) 或 SQL 构建 AI 应用的分步指南。

| 文档 | 描述 |
| --- | --- |
| [连接 TiDB](/ai/guides/connect.md) | 使用 `pytidb` 连接 TiDB Cloud 或自建集群。 |
| [使用表](/ai/guides/tables.md) | 创建、查询和管理包含向量字段的表。 |
| [向量搜索](/ai/guides/vector-search.md) | 使用 `pytidb` 进行语义相似度搜索。 |
| [全文搜索](/ai/guides/vector-search-full-text-search-python.md) | 基于关键字的文本搜索，支持 BM25 排序。 |
| [混合搜索](/ai/guides/vector-search-hybrid-search.md) | 结合向量搜索与全文搜索，获得更优结果。 |
| [图片搜索](/ai/guides/image-search.md) | 利用多模态嵌入进行 image 搜索。 |
| [Auto Embedding（自动生成向量）](/ai/guides/auto-embedding.md) | 数据插入时自动生成嵌入向量。 |
| [过滤](/ai/guides/filtering.md) | 通过元信息条件过滤搜索结果。 |

## 代码示例

完整代码示例和演示，展示 TiDB 的 AI 能力。

| 文档 | 描述 |
| --- | --- |
| [基本 CRUD 操作](/ai/examples/basic-with-pytidb.md) | 使用 `pytidb` 进行基础表操作。 |
| [向量搜索](/ai/examples/vector-search-with-pytidb.md) | 语义相似度搜索示例。 |
| [RAG 应用](/ai/examples/rag-with-pytidb.md) | 构建检索增强生成（RAG）应用。 |
| [图片搜索](/ai/examples/image-search-with-pytidb.md) | 基于 Jina AI 嵌入的多模态 image 搜索。 |
| [对话记忆](/ai/examples/memory-with-pytidb.md) | 为 AI agent 和聊天机器人提供持久 memory。 |
| [文本转 SQL](/ai/examples/text2sql-with-pytidb.md) | 将自然语言转换为 SQL 查询。 |

## 集成指南

将 TiDB 集成到主流 AI framework、嵌入提供商和开发工具中。

| 文档 | 描述 |
| --- | --- |
| [集成概览](/ai/integrations/vector-search-integration-overview.md) | 所有可用集成的概览。 |
| [Embedding Providers](/ai/integrations/vector-search-auto-embedding-overview.md#available-text-embedding-models) | 为 OpenAI、Cohere、Jina AI 等提供统一接口。 |
| [LangChain](/ai/integrations/vector-search-integrate-with-langchain.md) | 将 TiDB 作为 LangChain 的向量存储。 |
| [LlamaIndex](/ai/integrations/vector-search-integrate-with-llamaindex.md) | 将 TiDB 作为 LlamaIndex 的向量存储。 |
| [MCP Server](/ai/integrations/tidb-mcp-server.md) | 将 TiDB 连接到 Claude Code、Cursor 及其他 AI 驱动的 IDE。 |

## 参考指南

TiDB AI 与向量搜索特性的技术参考文档。

| 文档 | 描述 |
| --- | --- |
| [向量数据类型](/ai/reference/vector-search-data-types.md) | 向量列类型及其用法。 |
| [函数和运算符](/ai/reference/vector-search-functions-and-operators.md) | 距离函数与向量运算符。 |
| [向量搜索索引](/ai/reference/vector-search-index.md) | 创建和管理向量索引以提升性能。 |
| [性能调优](/ai/reference/vector-search-improve-performance.md) | 优化向量搜索性能。 |
| [限制](/ai/reference/vector-search-limitations.md) | 当前的限制与约束。 |