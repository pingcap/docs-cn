---
title: 向量搜索集成概述
summary: TiDB 向量搜索集成的概述，包括支持的 AI 框架、嵌入模型和 ORM 库。
---

# 向量搜索集成概述

本文提供 TiDB 向量搜索集成的概述，包括支持的 AI 框架、嵌入模型和对象关系映射（ORM）库。

> **注意**
>
> TiDB 向量搜索仅适用于 TiDB Self-Managed（TiDB >= v8.4）和 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)。它不适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)。

## AI 框架

TiDB 官方支持以下 AI 框架，使你能够轻松地将基于这些框架开发的 AI 应用程序与 TiDB 向量搜索集成。

| AI 框架 | 教程 |
| ------------- | ------------------------------------------------------------------------------------------------- |
| Langchain | [将向量搜索与 LangChain 集成](/tidb-cloud/vector-search-integrate-with-langchain.md) |
| LlamaIndex | [将向量搜索与 LlamaIndex 集成](/tidb-cloud/vector-search-integrate-with-llamaindex.md) |

此外，你还可以将 TiDB 用于各种用途，例如 AI 应用程序的文档存储和知识图谱存储。

## AI 服务

TiDB 向量搜索支持与以下 AI 服务集成，使你能够轻松构建基于检索增强生成（RAG）的应用程序。

- [Amazon Bedrock](/tidb-cloud/vector-search-integrate-with-amazon-bedrock.md)

## 嵌入模型和服务

TiDB 向量搜索支持存储最多 16383 维的向量，可以容纳大多数嵌入模型。

你可以使用自部署的开源嵌入模型或第三方嵌入提供商提供的第三方嵌入 API 来生成向量。

下表列出了一些主流嵌入服务提供商及其相应的集成教程。

| 嵌入服务提供商 | 教程 |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Jina AI | [将向量搜索与 Jina AI Embeddings API 集成](/tidb-cloud/vector-search-integrate-with-jinaai-embedding.md) |

## 对象关系映射（ORM）库

你可以将 TiDB 向量搜索与你的 ORM 库集成，以与 TiDB 数据库交互。

下表列出了支持的 ORM 库及其相应的集成教程：

<table>
  <tr>
    <th>语言</th>
    <th>ORM/客户端</th>
    <th>如何安装</th>
    <th>教程</th>
  </tr>
  <tr>
    <td rowspan="4">Python</td>
    <td>TiDB Vector Client</td>
    <td><code>pip install tidb-vector[client]</code></td>
    <td><a href="/tidbcloud/vector-search-get-started-using-python">使用 Python 开始使用向量搜索</a></td>
  </tr>
  <tr>
    <td>SQLAlchemy</td>
    <td><code>pip install tidb-vector</code></td>
    <td><a href="/tidbcloud/vector-search-integrate-with-sqlalchemy">将 TiDB 向量搜索与 SQLAlchemy 集成</a></td>
  </tr>
  <tr>
    <td>peewee</td>
    <td><code>pip install tidb-vector</code></td>
    <td><a href="/tidbcloud/vector-search-integrate-with-peewee">将 TiDB 向量搜索与 peewee 集成</a></td>
  </tr>
  <tr>
    <td>Django</td>
    <td><code>pip install django-tidb[vector]</code></td>
    <td><a href="/tidbcloud/vector-search-integrate-with-django-orm">将 TiDB 向量搜索与 Django 集成</a></td>
  </tr>
</table>
