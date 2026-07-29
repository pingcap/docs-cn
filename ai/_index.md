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

### TiDB Cloud CLI (tdc) (Preview)

| 文档 | 描述 |
| --- | --- |
| [tdc 概览](/ai/tdc/tdc-overview.md) | 了解 tdc 管理的资源，以及它如何使用随附的文件系统 companion。 |
| [快速开始使用 tdc](/ai/tdc/tdc-quick-start.md) | 安装并配置 tdc，然后完成第一次数据库或文件系统操作。 |

## 基础概念

了解 TiDB AI 搜索的基础概念。

| 文档 | 描述 |
| --- | --- |
| [向量搜索](/ai/concepts/vector-search-overview.md) | 向量搜索的全面概述，包括概念、工作原理和应用场景。 |
| [tdc 概念与架构 (Preview)](/ai/tdc/concepts/tdc-concepts-and-architecture.md) | 了解 profile、地域、凭证、SQL 角色、文件系统以及 Drive9 companion 边界。 |

## 使用指南

使用 TiDB Python SDK [`pytidb`](https://github.com/pingcap/pytidb) 或 SQL 构建 AI 应用的分步指南。

| 文档 | 描述 |
| --- | --- |
| [连接 TiDB](/ai/guides/connect.md) | 使用 `pytidb` 连接 TiDB Cloud 或 TiDB Self-Managed。 |
| [使用表](/ai/guides/tables.md) | 创建、查询和管理包含向量字段的表。 |
| [向量搜索](/ai/guides/vector-search.md) | 使用 `pytidb` 进行语义相似度搜索。 |
| [全文搜索](/ai/guides/vector-search-full-text-search-python.md) | 基于关键字的文本搜索，支持 BM25 排序。 |
| [混合搜索](/ai/guides/vector-search-hybrid-search.md) | 结合向量搜索与全文搜索，获得更优结果。 |
| [图片搜索](/ai/guides/image-search.md) | 利用多模态嵌入进行 image 搜索。 |
| [Auto Embedding（自动生成向量）](/ai/guides/auto-embedding.md) | 数据插入时自动生成嵌入向量。 |
| [过滤](/ai/guides/filtering.md) | 通过元信息条件过滤搜索结果。 |

### TiDB Cloud CLI (tdc) (Preview)

| 文档 | 描述 |
| --- | --- |
| [安装、配置和更新 tdc](/ai/tdc/guides/tdc-install-configure-update.md) | 安装发布版二进制文件、配置 profile、更新和卸载 tdc。 |
| [组织](/ai/tdc/guides/tdc-organization.md) | 列出项目并了解虚拟项目的选择方式。 |
| [Starter 数据库](/ai/tdc/guides/tdc-starter-database.md) | 管理集群、分支、SQL 用户、连接字符串以及 SQL 执行。 |
| [文件系统](/ai/tdc/guides/tdc-filesystem.md) | 管理文件系统资源、数据、layer、打包以及 FUSE 或 WebDAV 挂载。 |
| [文件系统 Git](/ai/tdc/guides/tdc-filesystem-git.md) | 克隆、hydrate 并管理关联的 Git worktree。 |
| [文件系统 Journal](/ai/tdc/guides/tdc-filesystem-journal.md) | 记录、搜索并验证仅追加的工作流事件。 |
| [文件系统 Vault](/ai/tdc/guides/tdc-filesystem-vault.md) | 存储密钥、委派访问、审计、注入并挂载只读 Vault。 |

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

### TiDB Cloud CLI (tdc) (Preview)

| 文档 | 描述 |
| --- | --- |
| [Agent 沙箱](/ai/tdc/examples/tdc-agent-sandbox-example.md) | 在不提供 TiDB Cloud API 密钥的情况下，让干净的沙箱访问文件系统。 |
| [日常工作流](/ai/tdc/examples/tdc-daily-workflow-example.md) | 按常规运维流程管理一个 Starter 集群和文件系统。 |
| [使用不同角色查询 SQL](/ai/tdc/examples/tdc-query-sql-with-roles-example.md) | 显式使用只读、读写和管理员 SQL 角色。 |
| [在多台机器间共享文件系统](/ai/tdc/examples/tdc-share-filesystem-across-machines-example.md) | 安全传递 owner token，并验证多台机器间的数据可见性。 |
| [为 Agent 准备 Git 工作区](/ai/tdc/examples/tdc-git-workspace-for-agents-example.md) | 准备已挂载的 Git 工作区和隔离的关联 worktree。 |
| [记录 Agent 工作流](/ai/tdc/examples/tdc-journal-agent-workflow-example.md) | 记录结构化事件并验证其哈希链。 |
| [向 Agent 委派 Vault 密钥](/ai/tdc/examples/tdc-vault-agent-secrets-example.md) | 向 Agent 临时授予一个密钥字段的访问权限。 |

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

### TiDB Cloud CLI (tdc) (Preview)

| 文档 | 描述 |
| --- | --- |
| [CLI 参考](/ai/tdc/reference/tdc-cli-reference.md) | 全局参数、输出、查询、dry run、帮助、错误和别名。 |
| [配置与凭证](/ai/tdc/reference/tdc-configuration-and-credentials.md) | Profile、优先级、本地状态、凭证、挂载定位文件和日志。 |
| [区域、安全与限制](/ai/tdc/reference/tdc-regions-security-and-limitations.md) | 部署区域、认证边界、平台、持久性和预览阶段限制。 |
| [故障排查](/ai/tdc/reference/tdc-troubleshooting.md) | 排查认证、配额、SQL、companion、文件系统选择和挂载故障。 |
