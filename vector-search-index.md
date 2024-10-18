---
title: 向量搜索索引
summary: 了解如何在 TiDB 中构建并使用向量搜索索引加速 K 近邻 (K-Nearest Neighbors, KNN) 查询。
---

# 向量搜索索引

K 近邻（K-Nearest Neighbors，简称 KNN）搜索是一种在向量空间中找到距离给定向量最近的 K 个向量的查询。实现 K 近邻搜索最直接的方法是暴力搜索（即计算向量空间中所有点与给定向量之间的距离），这种方法可以达到最高的精确度，但在实际应用中其搜索速度往往过于缓慢。因此，K 近邻搜索通常会采用近似算法来提高搜索效率。

在 TiDB 中，你可以创建并利用向量搜索索引来对[向量数据类型](/vector-search-data-types.md)的列进行近似近邻（Approximate Nearest Neighbor，简称 ANN）搜索。通过使用向量搜索索引，整个查询可在几毫秒内完成。

> **警告：**
>
> 向量搜索索引目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

TiDB 目前支持 [HNSW (Hierarchical Navigable Small World)](https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world) 向量搜索索引算法。

## 使用限制

- 集群需要提前部署 TiFlash 节点。
- 向量搜索索引不能作为主键或者唯一索引。
- 向量搜索索引只能基于单一的向量列创建，不能与其他列（如整数列或字符串列）组合形成复合索引。
- 创建和使用搜索向量索引时需要指定距离函数。目前只支持余弦距离函数 `VEC_COSINE_DISTANCE()` 和 L2 距离函数 `VEC_L2_DISTANCE()`。
- 不支持在同一列上创建多个使用了相同距离函数的向量搜索索引。
- 不支持直接删除具有向量搜索索引的列。可以通过先删除列上的向量搜索索引，再删除列的方式完成删除。
- 不支持修改带有向量索引的列的类型。
- 不支持将向量搜索索引[设置为不可见](/sql-statements/sql-statement-alter-index.md)。
- 不支持在开启了[静态加密](/encryption-at-rest.md)的 TiFlash 节点上构建向量搜索索引。

## 创建 HNSW 向量搜索索引

[HNSW](https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world) 是当前最流行的向量搜索索引算法之一。它性能良好，而且准确率相对较高，特定情况下可达 98%。

在 TiDB 中，你可以通过以下任一种方式为[向量数据类型](/vector-search-data-types.md)的列创建 HNSW 索引。

- 在建表时，使用以下语法来指定为哪一个向量列创建 HNSW 索引：

    ```sql
    CREATE TABLE foo (
        id       INT PRIMARY KEY,
        embedding     VECTOR(5),
        VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding)))
    );
    ```

- 对于现有的表，如果该表已包含向量列，可以通过以下语法为向量列创建 HNSW 索引：

    ```sql
    CREATE VECTOR INDEX idx_embedding ON foo ((VEC_COSINE_DISTANCE(embedding)));
    ALTER TABLE foo ADD VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding)));

    -- 你也可以显式指定 "USING HNSW" 使用 HNSW 构建向量搜索索引
    CREATE VECTOR INDEX idx_embedding ON foo ((VEC_COSINE_DISTANCE(embedding))) USING HNSW;
    ALTER TABLE foo ADD VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding))) USING HNSW;
    ```

> **注意：**
>
> 向量搜索索引功能的实现需要基于表的 TiFlash 副本。
>
> - 在建表时如果定义了向量搜索索引，TiDB 将自动为该表创建一个 TiFlash 副本。
> - 如果建表时未定义向量搜索索引，并且该表当前没有 TiFlash 副本，那么为该表添加向量搜索索引时，你需要先手动为该表创建 TiFlash 副本，例如：`ALTER TABLE 'table_name' SET TIFLASH REPLICA 1;`。

在创建 HNSW 向量索引时，你需要指定向量的距离函数：

- 余弦距离：`((VEC_COSINE_DISTANCE(embedding)))`
- L2 距离：`((VEC_L2_DISTANCE(embedding)))`

你只能为固定维度的向量列 (如定义为 `VECTOR(3)` 类型) 创建向量索引，不能为混合维度的向量列 (如定义为 `VECTOR` 类型) 创建向量索引，因为只有维度相同的向量之间才能计算向量距离。

有关向量搜索索引的约束和限制，请参阅[使用限制](#使用限制)。

## 使用向量搜索索引

在 K 近邻搜索查询中，可以通过 `ORDER BY ... LIMIT` 子句来使用向量搜索索引，如下所示：

```sql
SELECT *
FROM foo
ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3, 4, 5]')
LIMIT 10
```

要在向量搜索中使用索引，请确保 `ORDER BY ... LIMIT` 子句中使用的距离函数与创建向量索引时指定的距离函数相同。

## 使用带过滤条件的向量搜索索引

包含预过滤条件（使用 `WHERE` 子句）的查询无法使用向量搜索索引，因为这样的查询并没有严格按照 SQL 语义来查询 K 近邻。例如：

```sql
-- 对于以下查询，`WHERE` 过滤条件在 KNN 之前执行，因此不能使用向量搜索索引：

SELECT * FROM vec_table
WHERE category = "document"
ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]')
LIMIT 5;
```

如需使用带过滤条件的向量搜索索引，可以先通过向量搜索查询 K 个最近的邻居，再过滤掉不需要的结果：

```sql
-- 对于以下查询，过滤条件是在 KNN 之后执行的，因此可以使用向量索引：

SELECT * FROM
(
  SELECT * FROM vec_table
  ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]')
  LIMIT 5
) t
WHERE category = "document";

-- 请注意，如果过滤掉一些结果，此查询返回的结果可能少于 5 个。
```

## 查看索引构建进度

当插入大批量数据后，部分数据可能没有立即持久化到 TiFlash 中。对于已经持久化的向量数据，向量搜索索引是通过同步的方式构建的；对于尚未未持久化的数据，向量搜索索引会在数据持久化后才开始构建，但这并不会影响数据的准确性和一致性。你仍然可以随时进行向量搜索，并获得完整的结果，但需要注意的是，查询性能只有在向量搜索索引完全构建好之后才会达到最佳水平。

要查看索引构建进度，可以按如下方式查询 `INFORMATION_SCHEMA.TIFLASH_INDEXES` 表：

```sql
SELECT * FROM INFORMATION_SCHEMA.TIFLASH_INDEXES;
+---------------+------------+----------+-------------+---------------+-----------+----------+------------+---------------------+-------------------------+--------------------+------------------------+---------------+------------------+
| TIDB_DATABASE | TIDB_TABLE | TABLE_ID | COLUMN_NAME | INDEX_NAME    | COLUMN_ID | INDEX_ID | INDEX_KIND | ROWS_STABLE_INDEXED | ROWS_STABLE_NOT_INDEXED | ROWS_DELTA_INDEXED | ROWS_DELTA_NOT_INDEXED | ERROR_MESSAGE | TIFLASH_INSTANCE |
+---------------+------------+----------+-------------+---------------+-----------+----------+------------+---------------------+-------------------------+--------------------+------------------------+---------------+------------------+
| test          | tcff1d827  |      219 | col1fff     | 0a452311      |         7 |        1 | HNSW       |               29646 |                       0 |                  0 |                      0 |               | 127.0.0.1:3930   |
| test          | foo        |      717 | embedding   | idx_embedding |         2 |        1 | HNSW       |                   0 |                       0 |                  0 |                      3 |               | 127.0.0.1:3930   |
+---------------+------------+----------+-------------+---------------+-----------+----------+------------+---------------------+-------------------------+--------------------+------------------------+---------------+------------------+
```

- 可以通过 `ROWS_STABLE_INDEXED` 和 `ROWS_STABLE_NOT_INDEXED` 列查看索引构建进度。当 `ROWS_STABLE_NOT_INDEXED` 变为 0 时，表示索引构建完成。

    作为参考，对于一个 500 MiB 的向量数据集，构建索引的过程可能需要 20 分钟。索引构建器能够并行地在多个表中构建向量搜索索引。目前不支持调整索引构建器的优先级或速度。

- 可以通过 `ROWS_DELTA_NOT_INDEXED` 列查看 Delta 层中的行数。TiFlash 存储层的数据主要存放在 Delta 层和 Stable 层。Delta 层存储最近插入或更新的行，并根据写入工作量定期将这些行合并到 Stable 层。这个合并过程称为“压缩”。

    Delta 层本身是不包含索引的。为了达到最佳性能，你可以强制将 Delta 层合并到 Stable 层，以确保所有的数据都能够被索引：

    ```sql
    ALTER TABLE <TABLE_NAME> COMPACT;
    ```

    更多信息，请参阅 [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md)。

此外，你也可以通过 `ADMIN SHOW DDL JOBS;` 查看 DDL 任务的执行进度，观察其 `row count`。不过这种方式并不准确，`row count` 的值是从 `TIFLASH_INDEXES` 里的 `rows_stable_indexed` 获取的。你也可以使用此方式查看索引构建进度。

## 查看是否使用了向量搜索索引

你可以使用 [`EXPLAIN`](/sql-statements/sql-statement-explain.md) 或 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 语句查看一个查询是否使用了向量搜索索引。如果 `TableFullScan` 执行计划的 `operator info` 列中出现了 `annIndex:`，表示 TiDB 在扫描该表时使用了向量搜索索引。

**示例：使用了向量索引的查询**

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

**示例：由于未指定 Top K，导致未使用向量搜索索引的查询**

```sql
[tidb]> EXPLAIN SELECT * FROM vector_table_with_index
     -> ORDER BY Vec_Cosine_Distance(embedding, '[1, 2, 3]');
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

在某些情况下，如果无法使用向量搜索索引，TiDB 会生成警告信息，以帮助你了解背后的原因：

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

你可以执行 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 语句，然后查看输出中的 `execution info` 列了解向量索引使用情况的详细信息：

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
> 执行信息为 TiDB 内部信息。字段和格式如有更改，恕不另行通知。请勿依赖。

以下为一些重要字段的解释：

- `vector_index.load.total`：加载索引的总时长。该字段的值可能会超过查询实际耗时，因为 TiDB 可能会并行加载多个向量索引。
- `vector_index.load.from_s3`：从 S3 加载的索引数量。
- `vector_index.load.from_disk`：从磁盘加载的索引数量。这些索引之前已经从 S3 下载到磁盘上。
- `vector_index.load.from_cache`：从缓存中加载的索引数量。这些索引之前已经从 S3 下载并存储在缓存中。
- `vector_index.search.total`：在索引中搜索的总时长。如果该时间存在较大的延迟，通常意味着该索引为冷索引（以前从未被访问过，或很久以前被访问过），因此在索引中搜索时会产生较多的 I/O 操作。该字段的值可能会超过查询实际耗时，因为 TiDB 可能会并行搜索多个向量索引。
- `vector_index.search.discarded_nodes`：在搜索过程中已访问但被丢弃的向量行数。这些被丢弃的行不会包含在搜索结果中。如果该字段的值较大，通常表示表中有很多由于 `UPDATE` 或 `DELETE` 操作导致的数据过时的行。

关于执行信息输出的更多信息，请参阅 [`EXPLAIN`](/sql-statements/sql-statement-explain.md)、[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)，以及[使用 `EXPLAIN` 解读执行计划](/explain-walkthrough.md)。

## 另请参阅

- [优化向量搜索性能](/vector-search-improve-performance.md)
- [向量数据类型](/vector-search-data-types.md)