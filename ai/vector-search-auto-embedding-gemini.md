---
title: Gemini Embeddings
summary: 了解如何在 TiDB Cloud 中使用 Google Gemini 嵌入模型。
---

# Gemini Embeddings <!-- Draft translated by AI -->

本文档介绍如何在 TiDB Cloud 中结合 [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) 使用 Gemini 嵌入模型，从文本查询中执行语义搜索。

> **Note:**
>
> [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) 仅在托管于 AWS 的 TiDB Cloud Starter 集群上可用。

## 可用模型

如果你自带 Gemini API 密钥（BYOK），则所有 Gemini 模型均可通过 `gemini/` 前缀使用。例如：

**gemini-embedding-001**

- 名称：`gemini/gemini-embedding-001`
- 维度：128–3072（默认：3072）
- 距离度量：Cosine，L2
- 最大输入文本 tokens 数：2,048
- 价格：由 Google 收费
- 由 TiDB Cloud 托管：❌
- 支持自带密钥：✅

完整的可用模型列表，请参见 [Gemini documentation](https://ai.google.dev/gemini-api/docs/embeddings)。

## SQL 使用示例

要使用 Gemini 模型，你必须按如下方式指定 [Gemini API key](https://ai.google.dev/gemini-api/docs/api-key)：

> **Note:**
>
> 请将 `'your-gemini-api-key-here'` 替换为你实际的 Gemini API 密钥。

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_GEMINI_API_KEY = 'your-gemini-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(3072) GENERATED ALWAYS AS (EMBED_TEXT(
                "gemini/gemini-embedding-001",
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

## 选项

所有 [Gemini options](https://ai.google.dev/gemini-api/docs/embeddings) 均可通过 `EMBED_TEXT()` 函数的 `additional_json_options` 参数进行设置。

**示例：指定任务类型以提升质量**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "gemini/gemini-embedding-001",
                `content`,
                '{"task_type": "SEMANTIC_SIMILARITY"}'
              )) STORED
);
```

**示例：使用不同的维度**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(768) GENERATED ALWAYS AS (EMBED_TEXT(
                "gemini/gemini-embedding-001",
                `content`,
                '{"output_dimensionality": 768}'
              )) STORED
);
```

所有可用选项请参见 [Gemini documentation](https://ai.google.dev/gemini-api/docs/embeddings)。

## Python 使用示例

参见 [PyTiDB Documentation](https://pingcap.github.io/ai/guides/auto-embedding/)。

## 参见

- [Auto Embedding Overview](/ai/vector-search-auto-embedding-overview.md)
- [Vector Search](/vector-search/vector-search-overview.md)
- [Vector Functions and Operators](/vector-search/vector-search-functions-and-operators.md)
- [Hybrid Search](/ai/vector-search-hybrid-search.md)
