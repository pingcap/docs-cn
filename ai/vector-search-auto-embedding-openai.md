---
title: OpenAI 嵌入模型
summary: 了解如何在 TiDB Cloud 中使用 OpenAI 嵌入模型。
---

# OpenAI 嵌入模型

本文介绍如何在 TiDB Cloud 中通过 [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) 功能，使用 OpenAI 嵌入模型对文本查询进行语义搜索。

> **注意：**
>
> [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) 仅适用于托管在 AWS 上的 TiDB Cloud Starter 集群。

## 可用模型

如果你能提供自己的 OpenAI API 密钥，可以通过在模型名称前指定 `openai/` 前缀的方式使用任意 OpenAI 模型。例如：

**text-embedding-3-small**

- 名称：`openai/text-embedding-3-small`
- 维度：512-1536（默认：1536）
- 距离度量：Cosine、L2
- 价格：由 OpenAI 收费
- 由 TiDB Cloud 托管：❌
- Bring Your Own Key（BYOK，由用户自行提供 API 密钥）：✅

**text-embedding-3-large**

- 名称：`openai/text-embedding-3-large`
- 维度：256-3072（默认：3072）
- 距离度量：Cosine、L2
- 价格：由 OpenAI 收费
- 由 TiDB Cloud 托管：❌
- Bring Your Own Key（BYOK，由用户自行提供 API 密钥）：✅

完整可用模型列表请参见 [OpenAI 文档](https://platform.openai.com/docs/guides/embeddings)。

## SQL 使用示例

如需使用 OpenAI 模型，请按照以下方式指定 [OpenAI API 密钥](https://platform.openai.com/api-keys)：

> **注意：**
>
> 请将 `'your-openai-api-key-here'` 替换为你实际的 OpenAI API 密钥。

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

输出结果：

```
+------+----------------------------------------------------------------+
| id   | content                                                        |
+------+----------------------------------------------------------------+
|    1 | Java: Object-oriented language for cross-platform development. |
|    4 | Java's syntax is used in Android apps.                         |
+------+----------------------------------------------------------------+
```

## 使用 Azure OpenAI

如需使用 Azure 上提供的 OpenAI 嵌入模型，请将全局变量 `TIDB_EXP_EMBED_OPENAI_API_BASE` 设置为你的 Azure 资源的 URL。例如：

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

请注意，即使你的资源 URL 为 `https://<your-resource-name>.cognitiveservices.azure.com/`，配置 `TIDB_EXP_EMBED_OPENAI_API_BASE` 时也必须使用 `https://<your-resource-name>.openai.azure.com/openai/v1` 格式，以确保请求和响应格式与 OpenAI 兼容。

如需从 Azure OpenAI 切换回直接使用 OpenAI，将 `TIDB_EXP_EMBED_OPENAI_API_BASE` 设置为空字符串即可：

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_OPENAI_API_BASE = '';
```

> **注意：**
>
> - 出于安全原因，`API_BASE` 只能设置为 Azure OpenAI URL 或 OpenAI URL，不允许设置为任意 base URL。
> - 如需使用其他 OpenAI 兼容的嵌入服务，请联系 [TiDB Cloud 支持](https://docs.pingcap.com/zh/tidbcloud/tidb-cloud-support/)。

## 选项

所有 [OpenAI Embedding 选项](https://platform.openai.com/docs/api-reference/embeddings/create)均可通过 `EMBED_TEXT()` 函数的 `additional_json_options` 参数进行设置。

**示例：设置 text-embedding-3-large 的维度**

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

所有可用选项请参见 [OpenAI Embedding 文档](https://platform.openai.com/docs/api-reference/embeddings/create)。

## Python 使用示例

参见 [PyTiDB 文档](https://pingcap.github.io/ai/guides/auto-embedding/)。

## 另请参阅

- [Auto Embedding Overview](/ai/vector-search-auto-embedding-overview.md)
- [向量搜索](/vector-search/vector-search-overview.md)
- [向量函数与操作符](/vector-search/vector-search-functions-and-operators.md)
- [混合搜索](/ai/vector-search-hybrid-search.md)
