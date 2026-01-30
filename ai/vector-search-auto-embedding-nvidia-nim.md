---
title: NVIDIA NIM 嵌入模型
summary: 了解如何在 TiDB Cloud 中使用 NVIDIA NIM 嵌入模型。
---

# NVIDIA NIM 嵌入模型

本文介绍如何在 TiDB Cloud 中通过 [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) 功能，使用 NVIDIA NIM 嵌入模型对文本查询进行语义搜索。

> **注意：**
>
> 目前，仅 AWS 上的 TiDB Cloud Starter 集群支持 [Auto Embedding](/ai/vector-search-auto-embedding-overview.md) 功能。

## 可用模型

如果你能提供自己的 [NVIDIA NIM API 密钥](https://build.nvidia.com/settings/api-keys)，可以通过在模型名称前指定 `nvidia_nim/` 前缀的方式使用任意 NVIDIA NIM 模型。

以下章节以一个比较流行的 NVIDIA NIM 模型为例，展示如何通过 Auto Embedding 功能使用 NVIDIA NIM 模型。完整可用模型列表请参见 [NVIDIA NIM Text-to-embedding Models](https://build.nvidia.com/models?filters=usecase%3Ausecase_text_to_embedding)。

## bge-m3

- 名称：`nvidia_nim/baai/bge-m3`
- 维度：1024
- 距离度量：Cosine，L2
- 最大输入文本 token 数：8,192
- 价格：由 NVIDIA 收费
- 由 TiDB Cloud 托管：❌
- Bring Your Own Key（BYOK，由用户自行提供 API 密钥）：✅
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

输出示例：

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

## 另请参阅

- [Auto Embedding 概览](/ai/vector-search-auto-embedding-overview.md)
- [向量搜索](/vector-search/vector-search-overview.md)
- [向量函数与操作符](/vector-search/vector-search-functions-and-operators.md)
- [混合搜索](/ai/vector-search-hybrid-search.md)