---
title: 使用 SQL 进行混合搜索
summary: 了解如何在 TiDB 中通过一条 SQL 查询结合全文搜索和向量搜索，并在插入时自动生成向量嵌入。
---

# 使用 SQL 进行混合搜索

混合搜索会在同一张表上同时执行全文搜索和向量搜索，并将两组结果列表合并。全文搜索用于查找精确关键字，例如错误码和产品名称。向量搜索则可以在用词不同的情况下，找到语义相近的文本。当一个查询同时包含精确术语和你想表达内容的描述时，合并这两组结果会很有帮助。

本文档介绍如何通过一条 SQL 查询实现混合搜索。TiDB 会在你插入文本时自动生成向量嵌入。若要使用 `pytidb` Python SDK 实现相同功能，请参阅[混合搜索](/ai/guides/vector-search-hybrid-search.md)。

## 前提条件 {#prerequisites}

全文搜索仍处于早期阶段，正在逐步向更多用户开放。目前，全文搜索仅在以下区域的 {{{ .starter }}} 上可用：

- AWS: `Oregon (us-west-2)`, `N. Virginia (us-east-1)`, `Tokyo (ap-northeast-1)`, `Frankfurt (eu-central-1)`, and `Singapore (ap-southeast-1)`

Auto Embedding 仅在部署于 AWS 上的 {{{ .starter }}} 实例中可用。

要完成本教程，请确保你拥有一个位于上述区域之一的 {{{ .starter }}} 实例，并已使用 MySQL 客户端连接到该实例。如果你还没有实例，请按照[创建 {{{ .starter }}} 实例](/develop/dev-guide-build-cluster-in-cloud.md)进行创建。

## 步骤 1. 创建表 {#step-1-create-a-table}

创建一张表，其中包含一个文本列、一个由 TiDB 根据文本填充的向量列、一个全文索引以及一个向量索引：

```sql
USE test;

CREATE TABLE docs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    content TEXT,
    content_vector VECTOR(1024) GENERATED ALWAYS AS (
        EMBED_TEXT("tidbcloud_free/amazon/titan-embed-text-v2", content)
    ) STORED,
    FULLTEXT INDEX ft_content (content) WITH PARSER STANDARD,
    VECTOR INDEX idx_vec ((VEC_COSINE_DISTANCE(content_vector)))
);
```

`EMBED_TEXT()` 会调用由 TiDB Cloud 托管的嵌入模型，因此在本示例中你不需要 API key。向量维度 `1024` 必须与该模型的输出大小一致。关于其他模型，请参阅[Auto Embedding 概述](/ai/integrations/vector-search-auto-embedding-overview.md)。

## 步骤 2. 插入文本 {#step-2-insert-text}

只需插入文本。TiDB 会在插入时为每一行自动生成向量嵌入：

```sql
INSERT INTO docs (content) VALUES
  ('TiDB error 8200 means a vector index cannot be added to a partitioned table.'),
  ('Store agent memory in one table with a vector index and transactions.'),
  ('Solar panels convert sunlight into renewable energy.'),
  ('Use EXPLAIN to check whether a query uses the vector index.'),
  ('Partitioning a table by tenant lets the optimizer prune partitions.'),
  ('A cat sat on the warm windowsill all afternoon.');
```

## 步骤 3. 按语义搜索 {#step-3-search-by-meaning}

将查询文本传给 `VEC_EMBED_COSINE_DISTANCE()`。TiDB 会使用相同的模型对查询进行向量化，并按距离对行进行排序：

```sql
SELECT id, content FROM docs
ORDER BY VEC_EMBED_COSINE_DISTANCE(content_vector, 'why does adding a vector index fail on my partitioned table')
LIMIT 3;
```

```
+----+------------------------------------------------------------------------------+
| id | content                                                                      |
+----+------------------------------------------------------------------------------+
|  1 | TiDB error 8200 means a vector index cannot be added to a partitioned table. |
|  4 | Use EXPLAIN to check whether a query uses the vector index.                  |
|  2 | Store agent memory in one table with a vector index and transactions.        |
+----+------------------------------------------------------------------------------+
```

## 步骤 4. 按关键字搜索 {#step-4-search-by-keyword}

使用 `fts_match_word()` 查找至少包含一个查询词项的行，并按相关性排序：

```sql
SELECT id, content FROM docs
WHERE fts_match_word('error 8200', content)
ORDER BY fts_match_word('error 8200', content) DESC
LIMIT 3;
```

```
+----+------------------------------------------------------------------------------+
| id | content                                                                      |
+----+------------------------------------------------------------------------------+
|  1 | TiDB error 8200 means a vector index cannot be added to a partitioned table. |
+----+------------------------------------------------------------------------------+
```

## 步骤 5. 在一条查询中结合两种搜索 {#step-5-combine-both-searches-in-one-query}

以下查询会同时执行两种搜索，对每个结果列表分别排序，并先对向量搜索和全文搜索返回的 Top-K 候选 ID 执行 Reciprocal Rank Fusion (RRF)。然后，它会将融合后的热门结果重新与 `docs` 连接，以获取文档内容。每一行在其出现的每个列表中都会获得 `1 / (60 + rank)` 的分数，最后将这些分数相加。若某一行在两个列表中的排名都较高，它就会排到更前面。常数 `60` 是 RRF 中常用的取值；值越大，排名靠前的行相对于排名靠后的行优势就越小。

```sql
WITH
vec AS (
  SELECT id,
         ROW_NUMBER() OVER (ORDER BY distance, id) AS r
  FROM (
    SELECT /*+ READ_FROM_STORAGE(TIFLASH[docs]) */
           id,
           VEC_EMBED_COSINE_DISTANCE(
             content_vector,
             'vector index error 8200 partitioned table'
           ) AS distance
    FROM docs
    ORDER BY distance
    LIMIT 20
  ) v
),
fts AS (
  SELECT id,
         ROW_NUMBER() OVER (ORDER BY score DESC, id) AS r
  FROM (
    SELECT id,
           fts_match_word(
             'vector index error 8200 partitioned table',
             content
           ) AS score
    FROM docs
    WHERE fts_match_word(
      'vector index error 8200 partitioned table',
      content
    )
    ORDER BY score DESC
    LIMIT 20
  ) f
),
hits AS (
  SELECT id,
         1.0 / (60 + r) AS contribution,
         r AS vector_rank,
         NULL AS fulltext_rank
  FROM vec
  UNION ALL
  SELECT id,
         1.0 / (60 + r),
         NULL,
         r
  FROM fts
),
top_hits AS (
  SELECT id,
         SUM(contribution) AS rrf_score,
         MAX(vector_rank) AS vector_rank,
         MAX(fulltext_rank) AS fulltext_rank
  FROM hits
  GROUP BY id
  ORDER BY rrf_score DESC, id
  LIMIT 3
)
SELECT d.id, d.content,
       t.rrf_score,
       t.vector_rank,
       t.fulltext_rank
FROM top_hits t
JOIN docs d ON d.id = t.id
ORDER BY t.rrf_score DESC, t.id;
```

```
+----+------------------------------------------------------------------------------+-----------+-------------+---------------+
| id | content                                                                      | rrf_score | vector_rank | fulltext_rank |
+----+------------------------------------------------------------------------------+-----------+-------------+---------------+
|  1 | TiDB error 8200 means a vector index cannot be added to a partitioned table. |   0.03279 |           1 |             1 |
|  2 | Store agent memory in one table with a vector index and transactions.        |   0.03200 |           3 |             2 |
|  4 | Use EXPLAIN to check whether a query uses the vector index.                  |   0.03200 |           2 |             3 |
+----+------------------------------------------------------------------------------+-----------+-------------+---------------+
```

每种搜索在合并前都会先获取 20 个候选结果。如果合并结果中缺少相关行，可以适当增大该 `LIMIT`。

在 TiFlash 于后台重新组织新写入的行之后，全文相关性分数可能会发生变化，分数相近的行也可能因此交换位置。因此，在刚完成数据加载的表上，你输出中的 `fulltext_rank` 和 `rrf_score` 值可能与前面的示例不同。

`READ_FROM_STORAGE(TIFLASH[docs])` hint 会让向量搜索从 TiFlash 读取数据，因为向量索引位于 TiFlash 上。否则，在小表上，优化器可能会改为从 TiKV 读取并跳过向量索引。对于小表上的其他向量搜索，也可能发生同样的情况，例如步骤 3 中的查询；如果 `EXPLAIN` 没有显示 `annIndex:`，也可以在那里添加相同的 hint。要检查优化器是否选择了这两个索引，请对该查询执行 `EXPLAIN`：`operator info` 列会对向量搜索显示 `annIndex:`，对全文搜索显示 `textSearch:`。关于如何检查是否使用了向量索引的更多信息，请参阅[检查是否使用了向量索引](/ai/reference/vector-search-index.md#check-whether-the-vector-index-is-used)。

## 另请参阅 {#see-also}

- [混合搜索](/ai/guides/vector-search-hybrid-search.md)
- [使用 SQL 进行全文搜索](/ai/guides/vector-search-full-text-search-sql.md)
- [Auto Embedding 概述](/ai/integrations/vector-search-auto-embedding-overview.md)
- [向量搜索索引](/ai/reference/vector-search-index.md)