<!-- markdownlint-disable MD007 -->
<!-- markdownlint-disable MD041 -->

# 目录

## 快速开始

- [使用 Python 快速上手](/ai/quickstart-via-python.md)
- [使用 SQL 快速上手](/ai/quickstart-via-sql.md)
- TiDB Cloud CLI (tdc) (Preview)
  - [概览](/ai/tdc/tdc-overview.md)
  - [快速开始](/ai/tdc/tdc-quick-start.md)

## 基础概念

- [向量搜索](/ai/concepts/vector-search-overview.md)
- TiDB Cloud CLI (tdc) (Preview)
  - [概念与架构](/ai/tdc/concepts/tdc-concepts-and-architecture.md)

## 使用指南

- [连接 TiDB](/ai/guides/connect.md)
- [使用表](/ai/guides/tables.md)
- 搜索功能
  - [向量搜索](/ai/guides/vector-search.md)
  - 全文搜索
    - [使用 Python 进行全文搜索](/ai/guides/vector-search-full-text-search-python.md)
    - [使用 SQL 进行全文搜索](/ai/guides/vector-search-full-text-search-sql.md)
  - [混合搜索](/ai/guides/vector-search-hybrid-search.md)
  - [图片搜索](/ai/guides/image-search.md)
- 高级功能
  - [自动生成向量](/ai/guides/auto-embedding.md)
  - [过滤](/ai/guides/filtering.md)
  - [重排序](/ai/guides/reranking.md)
  - [Join 查询](/ai/guides/join-queries.md)
  - [Raw SQL 查询](/ai/guides/raw-queries.md)
  - [事务](/ai/guides/transactions.md)
- TiDB Cloud CLI (tdc) (Preview)
  - [安装、配置和更新 tdc](/ai/tdc/guides/tdc-install-configure-update.md)
  - [组织](/ai/tdc/guides/tdc-organization.md)
  - [Starter 数据库](/ai/tdc/guides/tdc-starter-database.md)
  - [文件系统](/ai/tdc/guides/tdc-filesystem.md)
  - [文件系统 Git](/ai/tdc/guides/tdc-filesystem-git.md)
  - [文件系统 Journal](/ai/tdc/guides/tdc-filesystem-journal.md)
  - [文件系统 Vault](/ai/tdc/guides/tdc-filesystem-vault.md)

## 代码示例

- [增删改查](/ai/examples/basic-with-pytidb.md)
- [自动生成向量](/ai/examples/auto-embedding-with-pytidb.md)
- 搜索与检索
  - [向量搜索](/ai/examples/vector-search-with-pytidb.md)
  - [全文搜索](/ai/examples/fulltext-search-with-pytidb.md)
  - [混合搜索](/ai/examples/hybrid-search-with-pytidb.md)
  - [图片搜索](/ai/examples/image-search-with-pytidb.md)
- AI 应用
  - [RAG 应用](/ai/examples/rag-with-pytidb.md)
  - [对话记忆](/ai/examples/memory-with-pytidb.md)
  - [文本转 SQL](/ai/examples/text2sql-with-pytidb.md)
- TiDB Cloud CLI (tdc) (Preview)
  - [Agent 沙箱](/ai/tdc/examples/tdc-agent-sandbox-example.md)
  - [日常工作流](/ai/tdc/examples/tdc-daily-workflow-example.md)
  - [使用不同角色查询 SQL](/ai/tdc/examples/tdc-query-sql-with-roles-example.md)
  - [在多台机器间共享文件系统](/ai/tdc/examples/tdc-share-filesystem-across-machines-example.md)
  - [为 Agent 准备 Git 工作区](/ai/tdc/examples/tdc-git-workspace-for-agents-example.md)
  - [记录 Agent 工作流](/ai/tdc/examples/tdc-journal-agent-workflow-example.md)
  - [向 Agent 委派 Vault 密钥](/ai/tdc/examples/tdc-vault-agent-secrets-example.md)

## 集成指南

- [集成概览](/ai/integrations/vector-search-integration-overview.md)
- 自动生成向量
  - [概览](/ai/integrations/vector-search-auto-embedding-overview.md)
  - [OpenAI](/ai/integrations/vector-search-auto-embedding-openai.md)
  - [OpenAI 兼容](/ai/integrations/embedding-openai-compatible.md)
  - [Jina AI](/ai/integrations/vector-search-auto-embedding-jina-ai.md)
  - [Cohere](/ai/integrations/vector-search-auto-embedding-cohere.md)
  - [Google Gemini](/ai/integrations/vector-search-auto-embedding-gemini.md)
  - [Hugging Face](/ai/integrations/vector-search-auto-embedding-huggingface.md)
  - [NVIDIA NIM](/ai/integrations/vector-search-auto-embedding-nvidia-nim.md)
  - [Amazon Titan](/ai/integrations/vector-search-auto-embedding-amazon-titan.md)
- AI 框架
  - [LangChain](/ai/integrations/vector-search-integrate-with-langchain.md)
  - [LlamaIndex](/ai/integrations/vector-search-integrate-with-llamaindex.md)
- ORM 库
  - [SQLAlchemy](/ai/integrations/vector-search-integrate-with-sqlalchemy.md)
  - [Django ORM](/ai/integrations/vector-search-integrate-with-django-orm.md)
  - [Peewee](/ai/integrations/vector-search-integrate-with-peewee.md)
- 云服务
  - [Jina AI Embedding](/ai/integrations/vector-search-integrate-with-jinaai-embedding.md)
  - [Amazon Bedrock](/ai/integrations/vector-search-integrate-with-amazon-bedrock.md)
- MCP Server
  - [概览](/ai/integrations/tidb-mcp-server.md)
  - [Claude Code](/ai/integrations/tidb-mcp-claude-code.md)
  - [Claude Desktop](/ai/integrations/tidb-mcp-claude-desktop.md)
  - [Cursor](/ai/integrations/tidb-mcp-cursor.md)
  - [VS Code](/ai/integrations/tidb-mcp-vscode.md)
  - [Windsurf](/ai/integrations/tidb-mcp-windsurf.md)

## 参考指南

- [向量数据类型](/ai/reference/vector-search-data-types.md)
- [函数和运算符](/ai/reference/vector-search-functions-and-operators.md)
- [向量搜索索引](/ai/reference/vector-search-index.md)
- [性能调优](/ai/reference/vector-search-improve-performance.md)
- [限制](/ai/reference/vector-search-limitations.md)
- [更新记录](/ai/reference/vector-search-changelogs.md)
- TiDB Cloud CLI (tdc) (Preview)
  - [CLI 参考](/ai/tdc/reference/tdc-cli-reference.md)
  - [配置与凭证](/ai/tdc/reference/tdc-configuration-and-credentials.md)
  - [区域、安全与限制](/ai/tdc/reference/tdc-regions-security-and-limitations.md)
  - [故障排查](/ai/tdc/reference/tdc-troubleshooting.md)
