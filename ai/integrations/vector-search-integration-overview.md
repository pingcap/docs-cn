---
title: 向量搜索集成概览
summary: TiDB 向量搜索集成的概览，包括支持的 AI 框架、嵌入模型和 ORM 库。
aliases: ['/zh/tidb/stable/vector-search-integration-overview/','/zh/tidb/dev/vector-search-integration-overview/','/zh/tidbcloud/vector-search-integration-overview/']
---

# 向量搜索集成概览

本文档概述了 TiDB 向量搜索的集成方式，包括支持的 AI 框架、嵌入模型和对象关系映射（ORM）库。

> **注意：**
>
> - 向量搜索功能目前为 beta 版本，可能会在未提前通知的情况下发生变更。如果你发现了 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。
> - 向量搜索功能适用于 [TiDB 自托管](/overview.md)、[TiDB Cloud Starter](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#starter)、[TiDB Cloud Essential](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#essential) 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#tidb-cloud-dedicated)。对于 TiDB 自托管和 TiDB Cloud Dedicated，TiDB 版本需为 v8.4.0 或更高（推荐 v8.5.0 或更高）。

## AI 框架

TiDB 官方支持以下 AI 框架，帮助你轻松将基于这些框架开发的 AI 应用与 TiDB 向量搜索集成。

| AI 框架      | 教程                                                                                          |
|--------------|----------------------------------------------------------------------------------------------|
| LangChain    | [与 LangChain 集成向量搜索](/ai/integrations/vector-search-integrate-with-langchain.md)       |
| LlamaIndex   | [与 LlamaIndex 集成向量搜索](/ai/integrations/vector-search-integrate-with-llamaindex.md)     |

你还可以将 TiDB 用于 AI 应用的文档存储、知识图谱存储等多种场景。

## 嵌入模型与服务

TiDB 向量搜索支持存储最多 16383 维的向量，能够满足大多数嵌入模型的需求。

你可以使用自部署的开源嵌入模型，或第三方嵌入 API 生成向量。

下表列出了一些主流嵌入服务提供商及其对应的集成教程。

| 嵌入服务提供商 | 教程                                                                                                         |
|----------------|-------------------------------------------------------------------------------------------------------------|
| Jina AI        | [与 Jina AI Embeddings API 集成向量搜索](/ai/integrations/vector-search-integrate-with-jinaai-embedding.md)  |

## 对象关系映射（ORM）库

你可以将 TiDB 向量搜索与 ORM 库集成，以便与 TiDB 数据库进行交互。

下表列出了支持的 ORM 库及其对应的集成教程：

<table>
  <tr>
    <th>语言</th>
    <th>ORM/客户端</th>
    <th>安装方式</th>
    <th>教程</th>
  </tr>
  <tr>
    <td rowspan="4">Python</td>
    <td>TiDB Vector Client</td>
    <td><code>pip install tidb-vector[client]</code></td>
    <td><a href="/ai/quickstart-via-python">使用 Python 快速开始向量搜索</a></td>
  </tr>
  <tr>
    <td>SQLAlchemy</td>
    <td><code>pip install tidb-vector</code></td>
    <td><a href="/ai/vector-search-integrate-with-sqlalchemy">与 SQLAlchemy 集成 TiDB 向量搜索</a></td>
  </tr>
  <tr>
    <td>peewee</td>
    <td><code>pip install tidb-vector</code></td>
    <td><a href="/ai/vector-search-integrate-with-peewee">与 peewee 集成 TiDB 向量搜索</a></td>
  </tr>
  <tr>
    <td>Django</td>
    <td><code>pip install django-tidb[vector]</code></td>
    <td><a href="/ai/vector-search-integrate-with-django-orm">与 Django 集成 TiDB 向量搜索</a></td>
  </tr>
</table>