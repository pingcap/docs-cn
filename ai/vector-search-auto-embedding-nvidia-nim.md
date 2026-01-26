---
title: NVIDIA NIM Embeddings
summary: 了解如何在 TiDB Cloud 中使用 NVIDIA NIM 嵌入模型。
---

# NVIDIA NIM Embeddings <!-- Draft translated by AI -->

本文档介绍如何在 TiDB Cloud 中结合 [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) 使用 NVIDIA NIM 嵌入模型，从文本查询中执行语义搜索。

> **Note:**
>
> [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) 仅适用于托管在 AWS 上的 TiDB Cloud Starter 集群。

## 可用模型

如果你自带 [NVIDIA NIM API key](https://build.nvidia.com/settings/api-keys)（BYOK），则可以使用以 `nvidia_nim/` 为前缀的 NVIDIA NIM 托管嵌入模型。

为方便起见，以下章节以一个流行模型为例，展示如何结合 Auto Embedding 使用该模型。完整可用模型列表请参见 [NVIDIA NIM Text-to-embedding Models](https://build.nvidia.com/models?filters=usecase%3Ausecase_text_to_embedding)。

## bge-m3

- 名称：`nvidia_nim/baai/bge-m3`
- 维度：1024
- 距离度量：Cosine，L2
- 最大输入文本 token 数：8,192
- 价格：由 NVIDIA 收费
- TiDB Cloud 托管：❌
- 支持自带密钥：✅
- 文档：<https://docs.api.nvidia.com/nim/reference/baai-bge-m3>

示例：

```sql
SET @@GLOBAL.TIDB_EXP_EMBED_NVIDIA_NIM_API_KEY = 'your-nvidia-nim-api-key-here';

CREATE TABLE sample (
  `id`        INT,
  `content`   TEXT,
  `embedding` VECTOR(1024) GENERATED ALWAYS AS (EMBED_TEXT(
                "nvidia_nim/baai/bge-m3",
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

## Python 使用示例

参见 [PyTiDB Documentation](https://pingcap.github.io/ai/guides/auto-embedding/)。

## 参见

- [Auto Embedding Overview](/ai/vector-search-auto-embedding-overview.md)
- [Vector Search](/vector-search/vector-search-overview.md)
- [Vector Functions and Operators](/vector-search/vector-search-functions-and-operators.md)
- [Hybrid Search](/ai/vector-search-hybrid-search.md)