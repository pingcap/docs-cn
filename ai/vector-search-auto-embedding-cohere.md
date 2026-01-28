---
title: Cohere 嵌入模型
summary: 了解如何在 TiDB Cloud 中使用 Cohere 嵌入模型。
---

# Cohere 嵌入模型

本文介绍如何在 TiDB Cloud 中通过 [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) 功能，使用 Cohere 嵌入模型对文本查询进行语义搜索。

> **注意：**
>
> 目前，仅 AWS 上的 TiDB Cloud Starter 集群支持 [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) 功能。

## 可用模型

TiDB Cloud 内置了以下 [Cohere](https://cohere.com/) 嵌入模型。使用时，无需提供 API 密钥。

**Cohere Embed v3 model**

- 名称：`tidbcloud_free/cohere/embed-english-v3`
- 维度：1024
- 距离度量：Cosine，L2
- 语言：英语
- 最大输入文本 token 数：512（约每个 token 4 个字符）
- 最大输入文本字符数：2,048
- 价格：免费
- 由 TiDB Cloud 托管：✅ `tidbcloud_free/cohere/embed-english-v3`
- Bring Your Own Key（BYOK，由用户自行提供 API key）：✅ `cohere/embed-english-v3.0`

**Cohere Multilingual Embed v3 model**

- 名称：`tidbcloud_free/cohere/embed-multilingual-v3`
- 维度：1024
- 距离度量：Cosine，L2
- 语言：100+ 种语言
- 最大输入文本 token 数：512（约每个 token 4 个字符）
- 最大输入文本字符数：2,048
- 价格：免费
- 由 TiDB Cloud 托管：✅ `tidbcloud_free/cohere/embed-multilingual-v3`
- Bring Your Own Key（BYOK，由用户自行提供 API key）：✅ `cohere/embed-multilingual-v3.0`

此外，如果你能提供自己的 Cohere API Key，可以通过在模型名称前指定 `cohere/` 前缀的方式使用任意 Cohere 模型。例如：

**Cohere Embed v4 model**

- 名称：`cohere/embed-v4.0`
- 维度：256、512、1024、1536（默认）
- 距离度量：Cosine，L2
- 最大输入文本 token 数：128,000
- 价格：由 Cohere 收费
- 由 TiDB Cloud 托管：❌
- Bring Your Own Key（BYOK，由用户自行提供 API key）：✅

完整的 Cohere 模型列表请参见 [Cohere 文档](https://docs.cohere.com/docs/cohere-embed)。

## SQL 使用示例（针对 TiDB Cloud 内置的嵌入模型）

以下示例展示了如何通过 Auto Embedding 功能使用 TiDB Cloud 内置的 Cohere 嵌入模型。

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "tidbcloud_free/cohere/embed-multilingual-v3",
                `content`,
                '{"input_type": "search_document", "input_type@search": "search_query"}'
              )) STORED
);
```

> **Note:**
>
> - 对于 Cohere 嵌入模型，在定义表时，你必须在 `EMBED_TEXT()` 函数中指定 `input_type`。例如，`'{"input_type": "search_document", "input_type@search": "search_query"}'` 表示插入数据时 `input_type` 为 `search_document`，向量搜索时自动应用 `search_query`。
> - `@search` 后缀表示该字段仅在向量搜索查询时生效，因此在查询时无需再次指定 `input_type`。

插入和查询数据：

```sql
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

## 选项（针对 TiDB Cloud 内置的嵌入模型）

**Embed v3** 和 **Multilingual Embed v3** 模型均支持以下选项，你可以通过 `EMBED_TEXT()` 函数的 `additional_json_options` 参数进行指定。

- `input_type`（必填）：在嵌入前添加特殊 token 以指示嵌入用途。你在为同一任务生成嵌入时必须始终使用相同的 `input type`，否则嵌入会被映射到不同的语义空间，导致不兼容。唯一的例外是语义搜索，文档使用 `search_document`，查询使用 `search_query`。

    - `search_document`：从文档生成嵌入，用于存储到向量数据库。
    - `search_query`：从查询生成嵌入，用于在向量数据库中检索已存储的嵌入。
    - `classification`：生成嵌入，作为文本分类器的输入。
    - `clustering`：生成嵌入，用于聚类任务。

- `truncate`（可选）：控制 API 如何处理超出最大 token 长度的输入。可选值如下：

    - `NONE`（默认）：当输入超过最大 token 长度时返回错误。
    - `START`：从开头截断文本，直到输入符合要求。
    - `END`：从结尾截断文本，直到输入符合要求。

## SQL 使用示例（BYOK）

如需使用 Bring Your Own Key (BYOK) 方式的 Cohere 模型，你必须按如下方式指定 Cohere API 密钥：

> **Note**
>
> 请将 `'your-cohere-api-key-here'` 替换为你的实际 Cohere API 密钥。你可以在 [Cohere Dashboard](https://dashboard.cohere.com/) 获取 API 密钥。

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_COHERE_API_KEY = 'your-cohere-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "cohere/embed-v4.0",
                `content`,
                '{"input_type": "search_document", "input_type@search": "search_query"}'
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

## 选项（BYOK）

所有 [Cohere 嵌入选项](https://docs.cohere.com/v2/reference/embed) 均可通过 `EMBED_TEXT()` 函数的 `additional_json_options` 参数进行设置。

**示例：为搜索和插入操作分别指定不同的 `input_type`**

使用 `@search` 后缀表示该字段仅在向量搜索查询时生效。

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "cohere/embed-v4.0",
                `content`,
                '{"input_type": "search_document", "input_type@search": "search_query"}'
              )) STORED
);
```

**示例：使用不同的维度**

```sql
CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(512) GENERATED ALWAYS AS (EMBED_TEXT(
                "cohere/embed-v4.0",
                `content`,
                '{"output_dimension": 512}'
              )) STORED
);
```

所有可用选项请参见 [Cohere Documentation](https://docs.cohere.com/v2/reference/embed)。

## Python 使用示例

参见 [PyTiDB Documentation](https://pingcap.github.io/ai/guides/auto-embedding/)。

## 另请参阅

- [Auto Embedding 概览](/ai/vector-search-auto-embedding-overview.md)
- [向量搜索](/vector-search/vector-search-overview.md)
- [向量函数与操作符](/vector-search/vector-search-functions-and-operators.md)
- [混合搜索](/ai/vector-search-hybrid-search.md)
