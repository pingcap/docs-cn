---
title: 向量搜索索引
summary: 了解如何构建和使用向量搜索索引来加速 TiDB 中的 K-最近邻（KNN）查询。
---

# 向量搜索索引

如[向量搜索](/tidb-cloud/vector-search-overview.md)文档所述，向量搜索通过计算给定向量与数据库中存储的所有向量之间的距离来识别给定向量的 K-最近邻（KNN）。虽然这种方法可以提供准确的结果，但当表包含大量向量时，由于需要进行全表扫描，速度可能会很慢。[^1]

为了提高搜索效率，你可以在 TiDB 中创建向量搜索索引以进行近似 KNN（ANN）搜索。使用向量索引进行向量搜索时，TiDB 可以大大提高查询性能，同时只会略微降低准确性，通常可以保持超过 90% 的搜索召回率。

目前，TiDB 支持 [HNSW（分层可导航小世界）](https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world)向量搜索索引算法。

## 创建 HNSW 向量索引

[HNSW](https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world) 是最流行的向量索引算法之一。HNSW 索引提供了良好的性能和相对较高的准确性，在特定情况下可达到 98%。

在 TiDB 中，你可以通过以下任一方式为具有[向量数据类型](/tidb-cloud/vector-search-data-types.md)的列创建 HNSW 索引：

- 创建表时，使用以下语法为向量列指定 HNSW 索引：

  ```sql
  CREATE TABLE foo (
      id       INT PRIMARY KEY,
      embedding     VECTOR(5),
      VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding)))
  );
  ```

- 对于已包含向量列的现有表，使用以下语法为向量列创建 HNSW 索引：

  ```sql
  CREATE VECTOR INDEX idx_embedding ON foo ((VEC_COSINE_DISTANCE(embedding)));
  ALTER TABLE foo ADD VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding)));

  -- 你也可以显式指定 "USING HNSW" 来构建向量搜索索引。
  CREATE VECTOR INDEX idx_embedding ON foo ((VEC_COSINE_DISTANCE(embedding))) USING HNSW;
  ALTER TABLE foo ADD VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding))) USING HNSW;
  ```

> **注意：**
>
> 向量搜索索引功能依赖于表的 TiFlash 副本。
>
> - 如果在创建表时定义了向量搜索索引，TiDB 会自动为该表创建 TiFlash 副本。
> - 如果在创建表时未定义向量搜索索引，且该表当前没有 TiFlash 副本，则需要在为表添加向量搜索索引之前手动创建 TiFlash 副本。例如：`ALTER TABLE 'table_name' SET TIFLASH REPLICA 1;`。

创建 HNSW 向量索引时，你需要指定向量的距离函数：

- 余弦距离：`((VEC_COSINE_DISTANCE(embedding)))`
- L2 距离：`((VEC_L2_DISTANCE(embedding)))`

向量索引只能为固定维度的向量列创建，例如定义为 `VECTOR(3)` 的列。它不能为非固定维度的向量列创建（例如定义为 `VECTOR` 的列），因为向量距离只能在具有相同维度的向量之间计算。

有关其他限制，请参见[向量索引限制](/tidb-cloud/vector-search-limitations.md#向量索引限制)。

## 使用向量索引

向量搜索索引可以在 K-最近邻搜索查询中使用，方法是使用 `ORDER BY ... LIMIT` 子句，如下所示：

```sql
SELECT *
FROM foo
ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3, 4, 5]')
LIMIT 10
```

要在向量搜索中使用索引，请确保 `ORDER BY ... LIMIT` 子句使用的距离函数与创建向量索引时指定的距离函数相同。

## 使用带过滤条件的向量索引

包含预过滤条件（使用 `WHERE` 子句）的查询无法利用向量索引，因为根据 SQL 语义，它们不是在查询 K-最近邻。例如：

```sql
-- 对于以下查询，`WHERE` 过滤在 KNN 之前执行，所以无法使用向量索引：

SELECT * FROM vec_table
WHERE category = "document"
ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]')
LIMIT 5;
```

要使用带过滤条件的向量索引，请先使用向量搜索查询 K-最近邻，然后过滤掉不需要的结果：

```sql
-- 对于以下查询，`WHERE` 过滤在 KNN 之后执行，所以可以使用向量索引：

SELECT * FROM
(
  SELECT * FROM vec_table
  ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]')
  LIMIT 5
) t
WHERE category = "document";

-- 注意，如果某些结果被过滤掉，此查询可能返回少于 5 个结果。
```

## 查看索引构建进度

在插入大量数据后，其中一些数据可能不会立即持久化到 TiFlash。对于已经持久化的向量数据，向量搜索索引会同步构建。对于尚未持久化的数据，索引将在数据持久化后构建。此过程不会影响数据的准确性和一致性。你仍然可以随时执行向量搜索并获得完整的结果。但是，在向量索引完全构建之前，性能将不会达到最佳。

要查看索引构建进度，你可以查询 `INFORMATION_SCHEMA.TIFLASH_INDEXES` 表，如下所示：

```sql
SELECT * FROM INFORMATION_SCHEMA.TIFLASH_INDEXES;
+---------------+------------+----------+-------------+---------------+-----------+----------+------------+---------------------+-------------------------+--------------------+------------------------+---------------+------------------+
| TIDB_DATABASE | TIDB_TABLE | TABLE_ID | COLUMN_NAME | INDEX_NAME    | COLUMN_ID | INDEX_ID | INDEX_KIND | ROWS_STABLE_INDEXED | ROWS_STABLE_NOT_INDEXED | ROWS_DELTA_INDEXED | ROWS_DELTA_NOT_INDEXED | ERROR_MESSAGE | TIFLASH_INSTANCE |
+---------------+------------+----------+-------------+---------------+-----------+----------+------------+---------------------+-------------------------+--------------------+------------------------+---------------+------------------+
| test          | tcff1d827  |      219 | col1fff     | 0a452311      |         7 |        1 | HNSW       |               29646 |                       0 |                  0 |                      0 |               | 127.0.0.1:3930   |
| test          | foo        |      717 | embedding   | idx_embedding |         2 |        1 | HNSW       |                   0 |                       0 |                  0 |                      3 |               | 127.0.0.1:3930   |
+---------------+------------+----------+-------------+---------------+-----------+----------+------------+---------------------+-------------------------+--------------------+------------------------+---------------+------------------+
```

- 你可以查看 `ROWS_STABLE_INDEXED` 和 `ROWS_STABLE_NOT_INDEXED` 列来了解索引构建进度。当 `ROWS_STABLE_NOT_INDEXED` 变为 0 时，索引构建完成。

  作为参考，为一个 500 MiB、768 维的向量数据集建立索引可能需要长达 20 分钟。索引器可以为多个表并行运行。目前不支持调整索引器的优先级或速度。

- 你可以查看 `ROWS_DELTA_NOT_INDEXED` 列来了解 Delta 层中的行数。TiFlash 存储层中的数据存储在两个层中：Delta 层和 Stable 层。Delta 层存储最近插入或更新的行，并根据写入工作负载定期合并到 Stable 层中。这个合并过程称为 Compaction。

  Delta 层始终不会被索引。为了获得最佳性能，你可以强制将 Delta 层合并到 Stable 层，以便所有数据都可以被索引：

  ```sql
  ALTER TABLE <TABLE_NAME> COMPACT;
  ```

  更多信息，请参见 [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md)。

此外，你可以通过执行 `ADMIN SHOW DDL JOBS;` 并检查 `row count` 来监控 DDL 作业的执行进度。但是，这种方法并不完全准确，因为 `row count` 值是从 `TIFLASH_INDEXES` 中的 `rows_stable_indexed` 字段获取的。你可以将此方法作为跟踪索引进度的参考。

## 检查是否使用了向量索引

使用 [`EXPLAIN`](/sql-statements/sql-statement-explain.md) 或 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 语句来检查查询是否使用了向量索引。当 `TableFullScan` 执行器的 `operator info` 列中出现 `annIndex:` 时，表示此表扫描正在使用向量索引。

**示例：使用了向量索引**

```sql
[tidb]> EXPLAIN SELECT * FROM vector_table_with_index
ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]')
LIMIT 10;
+-----+-------------------------------------------------------------------------------------+
| ... | operator info                                                                       |
+-----+-------------------------------------------------------------------------------------+
| ... | ...                                                                                 |
| ... | Column#5, offset:0, count:10                                                        |
| ... | ..., vec_cosine_distance(test.vector_table_with_index.embedding, [1,2,3])->Column#5 |
| ... | MppVersion: 1, data:ExchangeSender_16                                               |
| ... | ExchangeType: PassThrough                                                           |
| ... | ...                                                                                 |
| ... | Column#4, offset:0, count:10                                                        |
| ... | ..., vec_cosine_distance(test.vector_table_with_index.embedding, [1,2,3])->Column#4 |
| ... | annIndex:COSINE(test.vector_table_with_index.embedding..[1,2,3], limit:10), ...     |
+-----+-------------------------------------------------------------------------------------+
9 rows in set (0.01 sec)
```

**示例：由于未指定 Top K，未使用向量索引**

```sql
[tidb]> EXPLAIN SELECT * FROM vector_table_with_index
     -> ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]');
+--------------------------------+-----+--------------------------------------------------+
| id                             | ... | operator info                                    |
+--------------------------------+-----+--------------------------------------------------+
| Projection_15                  | ... | ...                                              |
| └─Sort_4                       | ... | Column#4                                         |
|   └─Projection_16              | ... | ..., vec_cosine_distance(..., [1,2,3])->Column#4 |
|     └─TableReader_14           | ... | MppVersion: 1, data:ExchangeSender_13            |
|       └─ExchangeSender_13      | ... | ExchangeType: PassThrough                        |
|         └─TableFullScan_12     | ... | keep order:false, stats:pseudo                   |
+--------------------------------+-----+--------------------------------------------------+
6 rows in set, 1 warning (0.01 sec)
```

当无法使用向量索引时，在某些情况下会出现警告以帮助你了解原因：

```sql
-- 使用了错误的距离函数：
[tidb]> EXPLAIN SELECT * FROM vector_table_with_index
ORDER BY VEC_L2_DISTANCE(embedding, '[1, 2, 3]')
LIMIT 10;

[tidb]> SHOW WARNINGS;
ANN index not used: not ordering by COSINE distance

-- 使用了错误的排序顺序：
[tidb]> EXPLAIN SELECT * FROM vector_table_with_index
ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]') DESC
LIMIT 10;

[tidb]> SHOW WARNINGS;
ANN index not used: index can be used only when ordering by vec_cosine_distance() in ASC order
```

## 分析向量搜索性能

要了解向量索引使用的详细信息，你可以执行 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 语句并检查输出中的 `execution info` 列：

```sql
[tidb]> EXPLAIN ANALYZE SELECT * FROM vector_table_with_index
ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]')
LIMIT 10;
+-----+--------------------------------------------------------+-----+
|     | execution info                                         |     |
+-----+--------------------------------------------------------+-----+
| ... | time:339.1ms, loops:2, RU:0.000000, Concurrency:OFF    | ... |
| ... | time:339ms, loops:2                                    | ... |
| ... | time:339ms, loops:3, Concurrency:OFF                   | ... |
| ... | time:339ms, loops:3, cop_task: {...}                   | ... |
| ... | tiflash_task:{time:327.5ms, loops:1, threads:4}        | ... |
| ... | tiflash_task:{time:327.5ms, loops:1, threads:4}        | ... |
| ... | tiflash_task:{time:327.5ms, loops:1, threads:4}        | ... |
| ... | tiflash_task:{time:327.5ms, loops:1, threads:4}        | ... |
| ... | tiflash_task:{...}, vector_idx:{                       | ... |
|     |   load:{total:68ms,from_s3:1,from_disk:0,from_cache:0},|     |
|     |   search:{total:0ms,visited_nodes:2,discarded_nodes:0},|     |
|     |   read:{vec_total:0ms,others_total:0ms}},...}          |     |
+-----+--------------------------------------------------------+-----+
```

> **注意：**
>
> 执行信息是内部信息。字段和格式可能会在没有任何通知的情况下发生更改。请不要依赖它们。

一些重要字段的解释：

- `vector_index.load.total`：加载索引的总持续时间。此字段可能大于实际查询时间，因为多个向量索引可能会并行加载。
- `vector_index.load.from_s3`：从 S3 加载的索引数量。
- `vector_index.load.from_disk`：从磁盘加载的索引数量。索引之前已从 S3 下载。
- `vector_index.load.from_cache`：从缓存加载的索引数量。索引之前已从 S3 下载。
- `vector_index.search.total`：在索引中搜索的总持续时间。较大的延迟通常意味着索引是冷的（以前从未访问过，或者很久以前访问过），因此在搜索索引时会有大量 I/O 操作。此字段可能大于实际查询时间，因为多个向量索引可能会并行搜索。
- `vector_index.search.discarded_nodes`：搜索过程中访问但被丢弃的向量行数。这些被丢弃的向量不会被考虑在搜索结果中。较大的值通常表示由于 `UPDATE` 或 `DELETE` 语句导致存在许多过时的行。

有关解释输出的信息，请参见 [`EXPLAIN`](/sql-statements/sql-statement-explain.md)、[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 和 [EXPLAIN 详解](/explain-walkthrough.md)。

## 限制

请参见[向量索引限制](/tidb-cloud/vector-search-limitations.md#向量索引限制)。

## 另请参阅

- [提高向量搜索性能](/tidb-cloud/vector-search-improve-performance.md)
- [向量数据类型](/tidb-cloud/vector-search-data-types.md)

[^1]: KNN 搜索的解释改编自 ClickHouse 文档中由 [rschu1ze](https://github.com/rschu1ze) 撰写的 [Approximate Nearest Neighbor Search Indexes](https://github.com/ClickHouse/ClickHouse/pull/50661/files#diff-7ebd9e71df96e74230c9a7e604fa7cb443be69ba5e23bf733fcecd4cc51b7576) 文档，根据 Apache License 2.0 许可。
