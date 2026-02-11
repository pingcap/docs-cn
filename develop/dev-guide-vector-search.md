---
title: 向量搜索
summary: 为应用开发者介绍 TiDB 中的向量搜索功能，包括相关概念、教程、集成方式以及参考文档。
---

# 向量搜索

[向量搜索](/ai/concepts/vector-search-overview.md) 支持在文档、图像、音频和视频等多种数据类型上进行语义相似性搜索。熟悉 MySQL 的开发人员可以基于该功能轻松构建人工智能 (AI) 应用。

## 快速开始

要开始使用 TiDB 向量搜索，请参考以下文档：

- [使用 SQL 开始向量搜索](/ai/quickstart-via-sql.md)
- [使用 Python 开始向量搜索](/ai/quickstart-via-python.md)

## 自动嵌入（Auto Embedding）

自动嵌入功能允许你直接使用纯文本进行向量搜索，而无需自行生成或提供向量。通过该功能，你可以直接插入文本数据，并使用文本查询进行语义搜索，TiDB 会在后台自动将文本转换为向量。

目前，TiDB 支持多种嵌入模型，例如 Amazon Titan、Cohere、Jina AI、OpenAI、Gemini、Hugging Face 以及 NVIDIA NIM。你可以根据需求选择合适的模型。更多信息，请参阅[自动嵌入概述](/ai/integrations/vector-search-auto-embedding-overview.md)。

## 集成

为提高开发效率，你可以将 TiDB 向量搜索与主流 AI 框架（如 LlamaIndex 和 LangChain）、嵌入服务（如 Jina AI）以及 ORM 库（如 SQLAlchemy、Peewee 和 Django ORM）进行集成。你可以根据自己的使用场景选择最合适的集成方式。

更多信息，请参阅[向量搜索集成概述](/ai/integrations/vector-search-integration-overview.md)。

## 文本搜索

与侧重语义相似性的向量搜索不同，全文搜索主要基于精确关键词进行文档检索。

在 RAG 场景中，为了提升检索质量，你可以将向量搜索与全文搜索结合使用。

| 场景 | 文档 |
|---------------|-------------|
| 使用 SQL 进行基于关键词的搜索 | [使用 SQL 进行全文搜索](/ai/guides/vector-search-full-text-search-sql.md) |
| 在 Python 应用中进行全文搜索 | [使用 Python 进行全文搜索](/ai/guides/vector-search-full-text-search-python.md) |
| 结合向量搜索与全文搜索以获得更优结果 | [混合搜索](/ai/guides/vector-search-hybrid-search.md) |

## 性能优化

为了优化向量搜索查询的性能，你可以遵循一系列最佳实践，例如添加向量索引、监控索引构建进度、降低向量维度、排除向量列以及对索引进行预热。

关于这些最佳实践的详细说明，请参阅[提升向量搜索性能](/ai/reference/vector-search-improve-performance.md)。

## 限制

在实现向量搜索之前，请注意以下限制：

- 单个向量的最大维度为 16383
- 向量列不能作为主键、唯一索引或分区键
- 向量类型与其他数据类型之间不支持直接类型转换（可使用字符串作为中间类型）

完整限制列表，请参阅[向量搜索限制](/ai/reference/vector-search-limitations.md)。

## 参考

- [向量数据类型](/ai/reference/vector-search-data-types.md)
- [向量函数与运算符](/ai/reference/vector-search-functions-and-operators.md)
- [向量索引](/ai/reference/vector-search-index.md)