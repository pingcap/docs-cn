---
title: TiDB for AI
summary: 使用 SQL、集成搜索、TiDB Cloud Starter 和持久化共享文件系统，通过 TiDB 构建 AI 应用和 agent 工作流。
---

# TiDB for AI

TiDB 提供数据和工作空间能力，用于构建 AI 应用和运行 AI agent 工作流。

- 对于应用开发，你可以使用 SQL 或 [TiDB AI 的 Python SDK (`pytidb`)](https://github.com/pingcap/pytidb)，结合结构化数据、向量搜索、全文搜索、混合搜索和 AI 驱动的检索来开发。
- 对于 AI agent 和自动化，你可以使用 [TiDB Cloud CLI (`ti`)](https://github.com/tidbcloud/ti-cli) 管理 TiDB Cloud Starter 实例和 SQL 工作流，并使用 [TiDB Cloud Filesystem](/tidb-cloud-filesystem/_index.md) 作为跨本地机器、CI 作业和临时 agent 沙箱的持久化共享存储。TiDB Cloud Filesystem 还提供挂载工作空间、Git 工作流、日志（Journal）和委托 Secrets。

## 快速开始 {#get-started}

快速体验 TiDB 的 AI 能力。

| 目标 | 从这里开始 |
| --- | --- |
| 使用向量搜索构建 AI 应用 | [通过 Python 快速上手向量搜索](/ai/quickstart-via-python.md) 或 [通过 SQL 快速上手向量搜索](/ai/quickstart-via-sql.md) |
| 使用 TiDB Cloud 构建 agent 和自动化工作流 | [快速上手 TiDB Cloud CLI](/ai/ti/ti-quick-start.md) |

## 使用 TiDB 构建 AI 应用 {#build-ai-applications-with-tidb}

使用 [`pytidb`](https://github.com/pingcap/pytidb) SDK 或 SQL 连接到 TiDB，搜索和检索数据，并构建 AI 驱动的应用。

### 连接到 TiDB {#connect-to-tidb}

| 文档 | 描述 |
| --- | --- |
| [通过 Python 连接到 TiDB](/ai/guides/connect.md) | 使用 `pytidb` 连接到 TiDB Cloud 或 TiDB Self-Managed。 |

### 搜索与检索 {#search-retrieval}

#### 向量搜索 {#vector-search}

| 文档 | 描述 |
| --- | --- |
| [向量搜索概述](/ai/guides/vector-search-overview.md) | 全面介绍向量搜索，包括概念、工作原理和使用场景。 |
| [向量搜索指南](/ai/guides/vector-search.md) | 使用 `pytidb` 执行语义相似性搜索。 |
| [向量搜索示例](/ai/guides/vector-search-with-pytidb.md) | 使用 `pytidb` 的语义相似性搜索示例。 |

#### 全文搜索 {#full-text-search}

| 文档 | 描述 |
| --- | --- |
| [通过 Python 进行全文搜索](/ai/guides/vector-search-full-text-search-python.md) | 使用 `pytidb` 进行基于关键字并采用 BM25 排名的文本搜索。 |
| [通过 SQL 进行全文搜索](/ai/guides/vector-search-full-text-search-sql.md) | 使用 SQL 进行基于关键字并采用 BM25 排名的文本搜索。 |
| [全文搜索示例](/ai/guides/fulltext-search-with-pytidb.md) | 使用 `pytidb` 的全文搜索示例。 |

#### 混合搜索 {#hybrid-search}

| 文档 | 描述 |
| --- | --- |
| [混合搜索指南](/ai/guides/vector-search-hybrid-search.md) | 结合向量搜索和全文搜索以获得更好的结果。 |
| [混合搜索示例](/ai/guides/hybrid-search-with-pytidb.md) | 使用 `pytidb` 的混合搜索示例。 |

#### Auto embedding {#auto-embeddings}

| 文档 | 描述 |
| --- | --- |
| [Auto Embedding 指南](/ai/guides/auto-embedding.md) | 在插入数据时自动生成向量嵌入。 |
| [Auto Embedding 示例](/ai/guides/auto-embedding-with-pytidb.md) | 使用 `pytidb` 的 auto embedding 示例。 |

#### 图片搜索 {#image-search}

| 文档 | 描述 |
| --- | --- |
| [图片搜索指南](/ai/guides/image-search.md) | 使用多模态向量嵌入搜索图片。 |
| [图片搜索示例](/ai/guides/image-search-with-pytidb.md) | 使用 Jina AI 向量嵌入的多模态图片搜索示例。 |

#### 重排序 {#reranking}

| 文档 | 描述 |
| --- | --- |
| [重排序](/ai/guides/reranking.md) | 对搜索结果进行重排序以提升相关性。 |

### 处理数据 {#work-with-data}

| 文档 | 描述 |
| --- | --- |
| [使用表](/ai/guides/tables.md) | 创建、查询和管理包含向量字段的表。 |
| [过滤](/ai/guides/filtering.md) | 使用元信息条件过滤搜索结果。 |
| [Join 查询](/ai/guides/join-queries.md) | 跨表执行 Join 查询。 |
| [原始 SQL 查询](/ai/guides/raw-queries.md) | 直接执行原始 SQL 查询。 |
| [事务](/ai/guides/transactions.md) | 使用事务保证数据一致性。 |

### 应用示例 {#application-examples}

| 文档 | 描述 |
| --- | --- |
| [RAG 示例](/ai/guides/rag-with-pytidb.md) | 构建检索增强生成应用。 |
| [对话记忆示例](/ai/guides/memory-with-pytidb.md) | 为 AI agent 和聊天机器人提供持久化记忆。 |
| [Text-to-SQL 示例](/ai/guides/text2sql-with-pytidb.md) | 将自然语言转换为 SQL 查询。 |

## 使用 TiDB Cloud CLI 构建 agent 和自动化工作流 {#build-agent-and-automation-workflows-with-tidb-cloud-cli}

TiDB Cloud CLI (`ti`) 让用户、脚本、CI 作业和 AI agent 能够通过终端管理 TiDB Cloud。你可以使用它自动化 TiDB Cloud Starter 和 SQL 操作，或让文件和工作区独立于使用它们的机器和沙箱而持续可用。

| 你想做什么 | 从这里开始 |
| --- | --- |
| 了解 `ti` 管理什么以及何时使用它 | [TiDB Cloud CLI 概览](/ai/ti/ti-overview.md) |
| 安装并配置 `ti`，然后完成第一个工作流 | [TiDB Cloud CLI 快速上手指南](/ai/ti/ti-quick-start.md) |
| 自动化 TiDB Cloud Starter 实例、分支和 SQL 操作 | [管理 TiDB Cloud Starter 实例](/ai/ti/guides/manage-starter-instances.md) |
| 在机器、CI 作业和沙箱之间持久化并共享文件 | [通过 TiDB Cloud CLI 使用 TiDB Cloud Filesystem](/ai/ti/guides/manage-filesystems-via-cli.md) |
| 使用挂载工作区、Git 工作区、日志（Journal）或委托 Secret | [挂载文件系统](/tidb-cloud-filesystem/filesystem-mount.md)、[管理 Git 工作区](/tidb-cloud-filesystem/manage-git-workspaces.md)、[在文件系统中使用日志（Journal）](/tidb-cloud-filesystem/use-filesystem-journals.md) 和 [管理文件系统的 Vault Secret](/tidb-cloud-filesystem/manage-filesystem-vault-secrets.md) |
| 查看端到端自动化或 agent 示例 | [运行每日 TiDB Cloud CLI 工作流](/ai/ti/guides/ti-daily-workflow-example.md) 或 [在 Agent Sandbox 中使用 TiDB Cloud Filesystem](/ai/ti/guides/ti-agent-sandbox-example.md) |
| 查询命令、全局选项、输出行为和错误 | [TiDB Cloud CLI 命令参考](/ai/ti/reference/ti-cli-reference.md) |

## 集成指南

将 TiDB 连接到嵌入提供商、AI 框架、应用程序库、云服务和 AI 开发工具。

| 集成领域 | 从这里开始 |
| --- | --- |
| 所有集成 | [AI Integrations for TiDB](/ai/integrations/vector-search-integration-overview.md) |
| Auto Embedding 提供商 | [Auto Embedding Overview](/ai/integrations/vector-search-auto-embedding-overview.md) |
| AI 框架 | [LlamaIndex](/ai/integrations/vector-search-integrate-with-llamaindex.md) |
| ORM 库 | [SQLAlchemy](/ai/integrations/vector-search-integrate-with-sqlalchemy.md), [Django ORM](/ai/integrations/vector-search-integrate-with-django-orm.md), and [Peewee](/ai/integrations/vector-search-integrate-with-peewee.md) |
| 云嵌入服务 | [Jina AI Embedding](/ai/integrations/vector-search-integrate-with-jinaai-embedding.md) and [Amazon Bedrock](/ai/integrations/vector-search-integrate-with-amazon-bedrock.md) |
| MCP 客户端和 AI 开发工具 | [TiDB MCP Server](/ai/integrations/tidb-mcp-server.md) |

## 参考指南

TiDB AI 与向量搜索特性的技术参考文档。

| 文档 | 描述 |
| --- | --- |
| [向量数据类型](/ai/reference/vector-search-data-types.md) | 向量列类型及其用法。 |
| [向量函数和运算符](/ai/reference/vector-search-functions-and-operators.md) | 距离函数与向量运算符。 |
| [向量搜索索引](/ai/reference/vector-search-index.md) | 创建和管理向量索引以提升性能。 |
| [向量搜索性能调优](/ai/reference/vector-search-improve-performance.md) | 优化向量搜索性能。 |
| [向量搜索限制](/ai/reference/vector-search-limitations.md) | 当前的限制与约束。 |
