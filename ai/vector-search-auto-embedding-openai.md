---
title: OpenAI Embeddings
summary: 了解如何在 TiDB Cloud 中使用 OpenAI 嵌入模型。
---

# OpenAI Embeddings <!-- Draft translated by AI -->

本文档介绍如何在 TiDB Cloud 中结合 [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) 使用 OpenAI 嵌入模型，从文本查询中执行语义搜索。

> **注意：**
>
> [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) 仅适用于托管在 AWS 上的 TiDB Cloud Starter 集群。

## 可用模型

如果你自带 OpenAI API key（BYOK），所有 OpenAI 模型均可通过 `openai/` 前缀使用。例如：

**text-embedding-3-small**

- 名称：`openai/text-embedding-3-small`
- 维度：512-1536（默认：1536）
- 距离度量：Cosine，L2
- 价格：由 OpenAI 收费
- 由 TiDB Cloud 托管：❌
- 支持自带密钥：✅

**text-embedding-3-large**

- 名称：`openai/text-embedding-3-large`
- 维度：256-3072（默认：3072）
- 距离度量：Cosine，L2
- 价格：由 OpenAI 收费
- 由 TiDB Cloud 托管：❌
- 支持自带密钥：✅

完整可用模型列表请参见 [OpenAI Documentation](https://platform.openai.com/docs/guides/embeddings)。

## SQL 使用示例

要使用 OpenAI 模型，必须按如下方式指定 [OpenAI API key](https://platform.openai.com/api-keys)：

> **注意：**
>
> 请将 `'your-openai-api-key-here'` 替换为你实际的 OpenAI API key。

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_OPENAI_API_KEY = 'your-openai-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(3072) GENERATED ALWAYS AS (EMBED_TEXT(
                "openai/text-embedding-3-large",
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

## 使用 Azure OpenAI

如需在 Azure 上使用 OpenAI 嵌入模型，请将全局变量 `TIDB_EXP_EMBED_OPENAI_API_BASE` 设置为你的 Azure 资源的 URL。例如：

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_OPENAI_API_KEY = 'your-openai-api-key-here';
SET @@GLOBAL.TIDB_EXP_EMBED_OPENAI_API_BASE = 'https://<your-resource-name>.openai.azure.com/openai/v1';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(3072) GENERATED ALWAYS AS (EMBED_TEXT(
                "openai/text-embedding-3-large",
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

请注意，即使你的资源 URL 形式为 `https://<your-resource-name>.cognitiveservices.azure.com/`，也必须使用 `https://<your-resource-name>.openai.azure.com/openai/v1` 作为 API base，以确保 OpenAI 兼容的请求和响应格式。

如需从 Azure OpenAI 切换回直接使用 OpenAI，只需将 `TIDB_EXP_EMBED_OPENAI_API_BASE` 设置为空字符串：

```sql
SET @@GLOBAL.TIDB_EXP_EMED_OPENAI_API_BASE = '';
```

> **注意：**
>
> - 出于安全原因，你只能将 API base 设置为 Azure OpenAI URL 或 OpenAI URL。不允许设置为任意 base URL。
> - 如需使用其他 OpenAI 兼容的嵌入服务，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

## 选项

所有 [OpenAI embedding options](https://platform.openai.com/docs/api-reference/embeddings/create) 均可通过 `EMBED_TEXT()` 函数的 `additional_json_options` 参数进行设置。

**示例：为 text-embedding-3-large 使用其他维度**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "openai/text-embedding-3-large",
                `content`,
                '{"dimensions": 1024}'
              )) STORED
);
```

所有可用选项请参见 [OpenAI Documentation](https://platform.openai.com/docs/api-reference/embeddings/create)。

## Python 使用示例

参见 [PyTiDB Documentation](https://pingcap.github.io/ai/guides/auto-embedding/)。

## 另请参阅

- [Auto Embedding Overview](/ai/vector-search-auto-embedding-overview.md)
- [Vector Search](/vector-search/vector-search-overview.md)
- [Vector Functions and Operators](/vector-search/vector-search-functions-and-operators.md)
- [Hybrid Search](/ai/vector-search-hybrid-search.md)
