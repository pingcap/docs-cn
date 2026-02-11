---
title: 向量搜索索引
summary: 了解如何在 TiDB 中构建和使用向量搜索索引，以加速 K-最近邻（KNN）查询。
aliases: ['/zh/tidb/stable/vector-search-index/','/zh/tidb/dev/vector-search-index/','/zh/tidbcloud/vector-search-index/']
---

# 向量搜索索引

如 [向量搜索](/ai/concepts/vector-search-overview.md) 文档所述，向量搜索通过计算给定向量与数据库中所有向量之间的距离，找出 Top K-最近邻（KNN）。这种方式能够提供准确的结果，但当表中包含大量向量时，查询速度较慢，因为需要进行全表扫描。[^1]

为了提升搜索效率，你可以在 TiDB 中为近似 KNN（ANN）搜索创建向量搜索索引。使用向量索引进行向量搜索时，TiDB 可以大幅提升查询性能，准确性仅有轻微下降，通常搜索召回率可保持在 90% 以上。

> **注意：**
>
> - 向量搜索功能目前为 beta 版本，可能会在未提前通知的情况下发生变更。如果你发现 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。
> - 向量搜索功能适用于 [TiDB 自托管](/overview.md)、[TiDB Cloud Starter](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#starter)、[TiDB Cloud Essential](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#essential) 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#tidb-cloud-dedicated)。对于 TiDB 自托管和 TiDB Cloud Dedicated，TiDB 版本需为 v8.4.0 及以上（推荐 v8.5.0 及以上）。

目前，TiDB 支持 [HNSW（Hierarchical Navigable Small World）](https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world) 向量搜索索引算法。

## 限制 {#restrictions}

- 你的集群中必须提前部署 TiFlash 节点。
- 向量搜索索引不能作为主键或唯一索引使用。
- 向量搜索索引只能创建在单个向量列上，不能与其他列（如整数型或字符串）组合为组合索引。
- 创建和使用向量搜索索引时，必须指定距离函数。目前仅支持余弦距离 `VEC_COSINE_DISTANCE()` 和 L2 距离 `VEC_L2_DISTANCE()` 函数。
- 对于同一列，不支持使用相同距离函数创建多个向量搜索索引。
- 不支持直接删除带有向量搜索索引的列。你可以先删除该列上的向量搜索索引，再删除该列。
- 不支持修改带有向量索引的列的类型。
- 不支持将向量搜索索引设置为 [不可见](/sql-statements/sql-statement-alter-index.md)。
- 不支持在启用 [静态加密](/encryption-at-rest.md) 的 TiFlash 节点上构建向量搜索索引。

## 创建 HNSW 向量索引

[HNSW](https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world) 是最流行的向量索引算法之一。HNSW 索引在保持较高准确性的同时，能够提供良好的性能，在特定场景下准确率可达 98%。

在 TiDB 中，你可以通过以下任一方式为具有 [向量数据类型](/ai/reference/vector-search-data-types.md) 的列创建 HNSW 索引：

- 创建表时，使用如下语法为向量列指定 HNSW 索引：

    ```sql
    CREATE TABLE foo (
        id       INT PRIMARY KEY,
        embedding     VECTOR(5),
        VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding)))
    );
    ```

- 对于已存在且包含向量列的表，使用如下语法为该向量列创建 HNSW 索引：

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
> - 如果在创建表时未定义向量搜索索引，且当前表没有 TiFlash 副本，则需要在为表添加向量搜索索引前，手动创建 TiFlash 副本。例如：`ALTER TABLE 'table_name' SET TIFLASH REPLICA 1;`。

创建 HNSW 向量索引时，你需要为向量指定距离函数：

- 余弦距离：`((VEC_COSINE_DISTANCE(embedding)))`
- L2 距离：`((VEC_L2_DISTANCE(embedding)))`

向量索引只能创建在定长向量列上，例如定义为 `VECTOR(3)` 的列。不能为非定长向量列（如定义为 `VECTOR` 的列）创建索引，因为只有维度相同的向量之间才能计算距离。

关于向量搜索索引的限制，详见 [限制](#restrictions)。

## 使用向量索引

在 K-最近邻搜索查询中，可以通过如下 `ORDER BY ... LIMIT` 语句使用向量搜索索引：

```sql
SELECT *
FROM foo
ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3, 4, 5]')
LIMIT 10
```

要在向量搜索中使用索引，确保 `ORDER BY ... LIMIT` 子句使用的距离函数与创建向量索引时指定的距离函数一致。

## 向量索引与过滤条件联合使用

包含预过滤（使用 `WHERE` 子句）的查询无法利用向量索引，因为根据 SQL 语义，这类查询并非在全表范围内查找 K-最近邻。例如：

```sql
-- 对于以下查询，`WHERE` 过滤在 KNN 之前执行，因此无法使用向量索引：

SELECT * FROM vec_table
WHERE category = "document"
ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]')
LIMIT 5;
```

要在带有过滤条件的场景下使用向量索引，应先通过向量搜索查询 K-最近邻，再对结果进行过滤：

```sql
-- 对于以下查询，`WHERE` 过滤在 KNN 之后执行，因此可以使用向量索引：

SELECT * FROM
(
  SELECT * FROM vec_table
  ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]')
  LIMIT 5
) t
WHERE category = "document";

-- 注意，如果部分结果被过滤，最终返回的结果可能少于 5 条。
```

## 查看索引构建进度 {#view-index-build-progress}

在你插入大量数据后，部分数据可能不会立即持久化到 TiFlash。对于已持久化的向量数据，向量搜索索引会同步构建；对于尚未持久化的数据，索引会在数据持久化后再构建。此过程不会影响数据的准确性和一致性，你可以随时进行向量搜索并获得完整结果。但在向量索引完全构建前，性能会低于最佳状态。

你可以通过查询 `INFORMATION_SCHEMA.TIFLASH_INDEXES` 表来查看索引构建进度：

```sql
SELECT * FROM INFORMATION_SCHEMA.TIFLASH_INDEXES;
+---------------+------------+----------+-------------+---------------+-----------+----------+------------+---------------------+-------------------------+--------------------+------------------------+---------------+------------------+
| TIDB_DATABASE | TIDB_TABLE | TABLE_ID | COLUMN_NAME | INDEX_NAME    | COLUMN_ID | INDEX_ID | INDEX_KIND | ROWS_STABLE_INDEXED | ROWS_STABLE_NOT_INDEXED | ROWS_DELTA_INDEXED | ROWS_DELTA_NOT_INDEXED | ERROR_MESSAGE | TIFLASH_INSTANCE |
+---------------+------------+----------+-------------+---------------+-----------+----------+------------+---------------------+-------------------------+--------------------+------------------------+---------------+------------------+
| test          | tcff1d827  |      219 | col1fff     | 0a452311      |         7 |        1 | HNSW       |               29646 |                       0 |                  0 |                      0 |               | 127.0.0.1:3930   |
| test          | foo        |      717 | embedding   | idx_embedding |         2 |        1 | HNSW       |                   0 |                       0 |                  0 |                      3 |               | 127.0.0.1:3930   |
+---------------+------------+----------+-------------+---------------+-----------+----------+------------+---------------------+-------------------------+--------------------+------------------------+---------------+------------------+
```

- 你可以通过 `ROWS_STABLE_INDEXED` 和 `ROWS_STABLE_NOT_INDEXED` 列查看索引构建进度。当 `ROWS_STABLE_NOT_INDEXED` 为 0 时，索引构建完成。

    作为参考，对 500 MiB、768 维的向量数据集进行索引，可能需要长达 20 分钟。索引器可并行为多个表构建索引。目前不支持调整索引器优先级或速度。

- 你可以通过 `ROWS_DELTA_NOT_INDEXED` 列查看 Delta 层中的行数。TiFlash 存储层的数据分为 Delta 层和 Stable 层。Delta 层存储最近插入或更新的行，并会根据写入负载定期合并到 Stable 层。该合并过程称为 Compaction。

    Delta 层始终不会被索引。为获得最佳性能，你可以强制将 Delta 层合并到 Stable 层，使所有数据都能被索引：

    ```sql
    ALTER TABLE <TABLE_NAME> COMPACT;
    ```

    详细信息参见 [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md)。

此外，你还可以通过执行 `ADMIN SHOW DDL JOBS;` 并查看 `row count`，监控 DDL 任务的执行进度。但该方法并不完全准确，因为 `row count` 的值来自 `TIFLASH_INDEXES` 中的 `rows_stable_indexed` 字段。你可以将此方法作为索引进度的参考。

## 检查是否使用了向量索引

使用 [`EXPLAIN`](/sql-statements/sql-statement-explain.md) 或 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 语句，可以检查查询是否使用了向量索引。当 `TableFullScan` 执行器的 `operator info` 列中出现 `annIndex:` 时，表示该表扫描正在利用向量索引。

**示例：已使用向量索引**

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

**示例：未指定 Top K，未使用向量索引**

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

当无法使用向量索引时，部分场景下会出现 warning，帮助你了解原因：

```sql
-- 使用了错误的距离函数：
[tidb]> EXPLAIN SELECT * FROM vector_table_with_index
ORDER BY VEC_L2_DISTANCE(embedding, '[1, 2, 3]')
LIMIT 10;

[tidb]> SHOW WARNINGS;
ANN index not used: not ordering by COSINE distance

-- 使用了错误的排序方式：
[tidb]> EXPLAIN SELECT * FROM vector_table_with_index
ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]') DESC
LIMIT 10;

[tidb]> SHOW WARNINGS;
ANN index not used: index can be used only when ordering by vec_cosine_distance() in ASC order
```

## 分析向量搜索性能

要了解向量索引的详细使用信息，可以执行 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 语句，并查看输出中的 `execution info` 列：

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
> 执行信息为内部信息，字段及格式可能随时变更，恕不另行通知。请勿依赖这些信息。

部分重要字段说明：

- `vector_index.load.total`：索引加载总耗时。该值可能大于实际查询时间，因为可能有多个向量索引并行加载。
- `vector_index.load.from_s3`：从 S3 加载的索引数量。
- `vector_index.load.from_disk`：从磁盘加载的索引数量。该索引此前已从 S3 下载到本地磁盘。
- `vector_index.load.from_cache`：从缓存加载的索引数量。该索引此前已从 S3 下载到缓存。
- `vector_index.search.total`：在索引中搜索的总耗时。较大的延时通常意味着索引为冷数据（从未访问或长时间未访问），导致搜索时有大量 I/O 操作。该值可能大于实际查询时间，因为可能有多个向量索引并行搜索。
- `vector_index.search.discarded_nodes`：搜索过程中访问但被丢弃的向量行数。这些被丢弃的向量不会计入搜索结果。该值较大通常说明存在大量因 `UPDATE` 或 `DELETE` 语句产生的陈旧行。

关于输出的解读，参见 [`EXPLAIN`](/sql-statements/sql-statement-explain.md)、[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 及 [EXPLAIN 使用指南](/explain-walkthrough.md)。

## 另请参阅

- [提升向量搜索性能](/ai/reference/vector-search-improve-performance.md)
- [向量数据类型](/ai/reference/vector-search-data-types.md)

[^1]: KNN 搜索的解释改编自 ClickHouse 文档中 [Approximate Nearest Neighbor Search Indexes](https://github.com/ClickHouse/ClickHouse/pull/50661/files#diff-7ebd9e71df96e74230c9a7e604fa7cb443be69ba5e23bf733fcecd4cc51b7576) 一文，作者为 [rschu1ze](https://github.com/rschu1ze)，遵循 Apache License 2.0 许可协议。