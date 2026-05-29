---
title: Reranking
summary: 了解如何在你的应用中使用 reranking。
---

# Reranking

Reranking（重排序）是一种通过使用专用的重排序模型对搜索结果进行重新评估和排序，以提升结果相关性和准确性的技术。

搜索过程分为两个阶段：

1. **初始搜索**：向量搜索从集合中识别出最相似的前 `k` 个文档。
2. **重排序**：重排序模型根据查询与这些 `k` 个文档之间的相关性进行评估，并重新排序，生成最终的前 `n` 个结果（其中 `n` ≤ `k`）。

这种两阶段搜索方法能显著提升文档的相关性和准确性。

## 基本用法

[`pytidb`](https://github.com/pingcap/pytidb) 是 TiDB 官方的 Python SDK，旨在帮助开发者高效构建 AI 应用。

`pytidb` 提供了 `Reranker` 类，让你可以使用来自多个第三方提供商的重排序模型。

1. 创建一个重排序实例：

    ```python
    from pytidb.rerankers import Reranker

    reranker = Reranker(model_name="{provider}/{model_name}")
    ```

2. 通过 `.rerank()` 方法应用重排序：

    ```python
    table.search("{query}").rerank(reranker, "{field_to_rerank}").limit(3)
    ```

## 支持的提供商

以下示例展示了如何使用第三方提供商的重排序模型。

### Jina AI

要使用 Jina AI 的重排序器，请前往其 [官网](https://jina.ai/reranker) 创建 API 密钥。

例如：

```python
jinaai = Reranker(
    # 使用 `jina-reranker-m0` 模型
    model_name="jina_ai/jina-reranker-m0",
    api_key="{your-jinaai-api-key}"
)
```