---
title: 向量搜索集成概览
summary: 介绍 TiDB 向量搜索支持的 AI 框架、嵌入模型和 ORM 库。
---

# 向量搜索集成概览

本文档介绍了 TiDB 向量搜索支持的 AI 框架、嵌入模型和对象关系映射 (ORM) 库。

> **警告：**
>
> 向量搜索目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

## AI 框架

TiDB 目前支持以下 AI 框架。基于这些 AI 框架，你可以使用 TiDB 向量搜索轻松构建 AI 应用程序。

| AI 框架 | 教程                                                                                          |
|---------------|---------------------------------------------------------------------------------------------------|
| Langchain     | [在 LangChain 中使用 TiDB 向量搜索](/vector-search-integrate-with-langchain.md)   |
| LlamaIndex    | [在 LlamaIndex 中使用 TiDB 向量搜索](/vector-search-integrate-with-llamaindex.md) |

此外，你还可以使用 TiDB 完成多种其它需求，例如将 TiDB 用于 AI 应用程序的文档存储和知识图谱存储等。

## 嵌入模型和服务

TiDB 向量搜索支持存储高达 16383 维的向量，可适应大多数嵌入模型。

你可以使用自行部署的开源嵌入模型或第三方嵌入模型提供商的嵌入 API 来生成向量。

下表列出了部分主流嵌入模型服务提供商和相应的集成教程。

| 嵌入模型服务提供商 | 教程                                                                                                            |
|-----------------------------|---------------------------------------------------------------------------------------------------------------------|
| Jina AI                     | [结合 Jina AI 嵌入模型 API 使用 TiDB 向量搜索](/vector-search-integrate-with-jinaai-embedding.md) |

## 对象关系映射 (ORM) 库

你可以将 TiDB 向量搜索功能与 ORM 库结合使用，以便与 TiDB 数据库交互。

下表列出了支持的 ORM 库和相应的使用教程：

<table>
  <tr>
    <th>Language</th>
    <th>ORM/Client</th>
    <th>How to install</th>
    <th>Tutorial</th>
  </tr>
  <tr>
    <td rowspan="4">Python</td>
    <td>TiDB Vector Client</td>
    <td><code>pip install tidb-vector[client]</code></td>
    <td><a href="/vector-search-get-started-using-python.md">使用 Python 开始向量搜索</a></td>
  </tr>
  <tr>
    <td>SQLAlchemy</td>
    <td><code>pip install tidb-vector</code></td>
    <td><a href="/vector-search-integrate-with-sqlalchemy.md">在 SQLAlchemy 中使用 TiDB 向量搜索</a></td>
  </tr>
  <tr>
    <td>peewee</td>
    <td><code>pip install tidb-vector</code></td>
    <td><a href="/vector-search-integrate-with-peewee.md">在 peewee 中使用 TiDB 向量搜索</a></td>
  </tr>
  <tr>
    <td>Django</td>
    <td><code>pip install django-tidb[vector]</code></td>
    <td><a href="/vector-search-integrate-with-django-orm.md">在 Django 中使用 TiDB 向量搜索</a></td>
  </tr>
</table>