---
title: AI 功能
summary: 了解 TiDB Cloud 的 AI 功能。
---

# AI 功能

TiDB Cloud 中的 AI 功能使您能够充分利用先进技术进行数据探索、搜索和集成。从自然语言驱动的 SQL 查询生成到高性能向量搜索，TiDB 将数据库功能与现代 AI 功能相结合，为创新应用提供动力。通过支持流行的 AI 框架、嵌入模型以及与 ORM 库的无缝集成，TiDB 为语义搜索和 AI 驱动的分析等用例提供了一个多功能平台。

本文档重点介绍这些 AI 功能以及它们如何增强 TiDB 体验。

## Chat2Query（Beta）

Chat2Query 是集成在 SQL 编辑器中的 AI 驱动功能，可帮助用户使用自然语言指令生成、调试或重写 SQL 查询。更多信息，请参见[使用 AI 辅助的 SQL 编辑器探索数据](/tidb-cloud/explore-data-with-chat2query.md)。

此外，TiDB Cloud 为 TiDB Cloud Serverless 集群提供 Chat2Query API。启用后，TiDB Cloud 将自动在数据服务中创建一个名为 Chat2Query 的系统数据应用和一个 Chat2Data 端点。您可以调用此端点，通过提供指令让 AI 生成并执行 SQL 语句。更多信息，请参见[开始使用 Chat2Query API](/tidb-cloud/use-chat2query-api.md)。

## 向量搜索（Beta）

向量搜索是一种优先考虑数据含义以提供相关结果的搜索方法。

与依赖精确关键词匹配和词频的传统全文搜索不同，向量搜索将各种数据类型（如文本、图像或音频）转换为高维向量，并基于这些向量之间的相似度进行查询。这种搜索方法捕捉数据的语义含义和上下文信息，从而更准确地理解用户意图。

即使搜索词与数据库中的内容不完全匹配，向量搜索仍然可以通过分析数据的语义提供符合用户意图的结果。例如，对"会游泳的动物"进行全文搜索只会返回包含这些确切关键词的结果。相比之下，向量搜索可以返回其他会游泳的动物的结果，如鱼或鸭子，即使这些结果不包含确切的关键词。

更多信息，请参见[向量搜索（Beta）概述](/tidb-cloud/vector-search-overview.md)。

## AI 集成

### AI 框架

TiDB 官方支持多个流行的 AI 框架，使您能够轻松地将基于这些框架开发的 AI 应用程序与 TiDB 向量搜索集成。

有关支持的 AI 框架列表，请参见[向量搜索集成概述](/tidb-cloud/vector-search-integration-overview.md#ai-frameworks)。

### 嵌入模型和服务

向量嵌入（也称为嵌入）是一个数字序列，用于在高维空间中表示现实世界的对象。它捕捉非结构化数据（如文档、图像、音频和视频）的含义和上下文。

嵌入模型是将数据转换为[向量嵌入](/tidb-cloud/vector-search-overview.md#vector-embedding)的算法。选择合适的嵌入模型对于确保语义搜索结果的准确性和相关性至关重要。

TiDB 向量搜索支持存储最多 16383 维的向量，可以适应大多数嵌入模型。对于非结构化文本数据，您可以在 [Massive Text Embedding Benchmark (MTEB) 排行榜](https://huggingface.co/spaces/mteb/leaderboard)上找到性能最佳的文本嵌入模型。

### 对象关系映射（ORM）库

对象关系映射（ORM）库是一种工具，通过允许开发人员像处理编程语言中的对象一样处理数据库记录，从而促进应用程序和关系数据库之间的交互。

TiDB 允许您将向量搜索与 ORM 库集成，以便与传统关系数据一起管理向量数据。这种集成对于需要存储和查询 AI 模型生成的向量嵌入的应用程序特别有用。通过使用 ORM 库，开发人员可以无缝地与存储在 TiDB 中的向量数据交互，利用数据库的功能执行最近邻搜索等复杂的向量操作。

有关支持的 ORM 库列表，请参见[向量搜索集成概述](/tidb-cloud/vector-search-integration-overview.md#object-relational-mapping-orm-libraries)。
