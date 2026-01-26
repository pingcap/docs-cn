---
title: Amazon Titan Embeddings
summary: 了解如何在 TiDB Cloud 中使用 Amazon Titan 嵌入模型。
---

# Amazon Titan Embeddings <!-- Draft translated by AI -->

本文档介绍如何在 TiDB Cloud 中结合 [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) 使用 Amazon Titan 嵌入模型，从文本查询中执行语义搜索。

> **Note:**
>
> [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) 仅适用于托管在 AWS 上的 TiDB Cloud Starter 集群。

## 可用模型

TiDB Cloud 原生提供以下 [Amazon Titan 嵌入模型](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html)。无需 API 密钥。

**Amazon Titan Text Embedding V2 模型**

- 名称：`tidbcloud_free/amazon/titan-embed-text-v2`
- 维度：1024（默认）、512、256
- 距离度量：Cosine、L2
- 支持语言：英语（预览支持 100+ 种语言）
- 典型用例：RAG、文档检索、重排序、分类
- 最大输入文本 token 数：8,192
- 最大输入文本字符数：50,000
- 价格：免费
- 由 TiDB Cloud 托管：✅
- 支持自带密钥：❌

关于该模型的更多信息，请参见 [Amazon Bedrock 文档](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html)。

## SQL 使用示例

以下示例展示了如何结合 Auto Embedding 使用 Amazon Titan 嵌入模型。

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "tidbcloud_free/amazon/titan-embed-text-v2",
                `content`
              )) STORED
);


INSERT INTO sample
    (`id`, `content`)
VALUES
    (1, "Java: Object-oriented language for cross-platform development."),
    (2, "Java coffee: Bold Indonesian beans with low acidity."),
    (3, "Java island: Densely populated, home to Jakarta."),
    (4, "Java's syntax is used in Android apps."),
    (5, "Dark roast Java beans enhance espresso blends.");


SELECT `id`, `content` FROM sample
ORDER BY
  VEC_EMBED_COSINE_DISTANCE(
    embedding,
    "How to start learning Java programming?"
  )
LIMIT 2;
```

结果：

```
+------+----------------------------------------------------------------+
| id   | content                                                        |
+------+----------------------------------------------------------------+
|    1 | Java: Object-oriented language for cross-platform development. |
|    4 | Java's syntax is used in Android apps.                         |
+------+----------------------------------------------------------------+
```

## 可选参数

你可以通过 `EMBED_TEXT()` 函数的 `additional_json_options` 参数指定以下选项：

- `normalize`（可选）：是否对输出嵌入向量进行归一化。默认为 `true`。
- `dimensions`（可选）：输出嵌入向量的维度。支持的取值：`1024`（默认）、`512`、`256`。

**示例：使用其他维度**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(512) GENERATED ALWAYS AS (EMBED_TEXT(
                "tidbcloud_free/amazon/titan-embed-text-v2",
                `content`,
                '{"dimensions": 512}'
              )) STORED
);


INSERT INTO sample
    (`id`, `content`)
VALUES
    (1, "Java: Object-oriented language for cross-platform development."),
    (2, "Java coffee: Bold Indonesian beans with low acidity."),
    (3, "Java island: Densely populated, home to Jakarta."),
    (4, "Java's syntax is used in Android apps."),
    (5, "Dark roast Java beans enhance espresso blends.");


SELECT `id`, `content` FROM sample
ORDER BY
  VEC_EMBED_COSINE_DISTANCE(
    embedding,
    "How to start learning Java programming?"
  )
LIMIT 2;
```

结果：

```
+------+----------------------------------------------------------------+
| id   | content                                                        |
+------+----------------------------------------------------------------+
|    1 | Java: Object-oriented language for cross-platform development. |
|    4 | Java's syntax is used in Android apps.                         |
+------+----------------------------------------------------------------+
```

## Python 使用示例

参见 [PyTiDB 文档](https://pingcap.github.io/ai/guides/auto-embedding/)。

## 参见

- [Auto Embedding 概览](/ai/vector-search-auto-embedding-overview.md)
- [向量检索](/vector-search/vector-search-overview.md)
- [向量函数与操作符](/vector-search/vector-search-functions-and-operators.md)
- [混合检索](/ai/vector-search-hybrid-search.md)
