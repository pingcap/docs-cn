---
title: Gemini 嵌入模型
summary: 了解如何在 TiDB Cloud 中使用 Google Gemini 嵌入模型。
---

# Gemini 嵌入模型

本文介绍如何在 TiDB Cloud 中通过 [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) 功能，使用 Gemini 嵌入模型对文本查询进行语义搜索。

> **注意：**
>
> 目前，仅 AWS 上的 TiDB Cloud Starter 集群支持 [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) 功能。

## 可用模型

如果你能提供自己的 Gemini API Key，可以通过在模型名称前指定 `gemini/` 前缀的方式使用任意 Gemini 模型。例如：

**gemini-embedding-001**

- 名称：`gemini/gemini-embedding-001`
- 维度：128–3072（默认：3072）
- 距离度量：Cosine，L2
- 最大输入文本 token 数：2,048
- 价格：由 Google 收费
- 由 TiDB Cloud 托管：❌
- Bring Your Own Key（BYOK，由用户自行提供 API key）：✅

完整的可用模型列表，请参见 [Gemini 文档](https://ai.google.dev/gemini-api/docs/embeddings)。

## SQL 使用示例

如需使用 Gemini 模型，请按照以下方式指定 [Gemini API key](https://ai.google.dev/gemini-api/docs/api-key)：

> **注意：**
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

输出结果：

```
+------+----------------------------------------------------------------+
| id   | content                                                        |
+------+----------------------------------------------------------------+
|    1 | Java: Object-oriented language for cross-platform development. |
|    4 | Java's syntax is used in Android apps.                         |
+------+----------------------------------------------------------------+
```

## 选项

所有 [Gemini 选项](https://ai.google.dev/gemini-api/docs/embeddings) 均可通过 `EMBED_TEXT()` 函数的 `additional_json_options` 参数进行设置。

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

所有可用选项请参见 [Gemini 文档](https://ai.google.dev/gemini-api/docs/embeddings)。

## Python 使用示例

参见 [PyTiDB 文档](https://pingcap.github.io/ai/guides/auto-embedding/)。

## 另请参阅

- [Auto Embedding 概览](/ai/vector-search-auto-embedding-overview.md)
- [向量搜索](/vector-search/vector-search-overview.md)
- [向量函数与操作符](/vector-search/vector-search-functions-and-operators.md)
- [混合搜索](/ai/vector-search-hybrid-search.md)
