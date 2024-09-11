---
title: 向量搜索索引
summary: 了解如何在 TiDB 中构建并使用向量搜索索引加速 K 近邻 (KNN) 查询
---

# 向量搜索索引

K 近邻 (KNN) 搜索是在向量空间中找到距离给定向量最近的 K 个向量的查询。要找到最近的 K 个向量，最直接的方法就是暴力搜索，即计算向量空间中所有点与给定向量之间的距离。这种方法拥有最好的精确度，但在实际的搜索中，往往搜索速度太慢。因此，近邻搜索问题通常采用近似算法来解决。

在 TiDB 中，你可以创建并利用向量搜索索引来对 [向量类型](/vector-search-data-types.md) 的列进行近似近邻 (ANN) 搜索。通过使用向量搜索索引，整个查询可在几毫秒内完成。

TiDB 目前支持以下向量搜索索引算法：

- HNSW


## 创建 HNSW 向量搜索索引

[HNSW](https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world) 是最流行的向量搜索索引算法。HNSW 索引的性能良好，且准确率相对较高 (特定情况下可达 98%),

要创建 HNSW 向量搜索索引，你可以在创建表格时，使用以下语法指定为哪一列的[向量数据类型](/vector-search-data-types.md)构建索引：

```sql
CREATE TABLE foo (
    id       INT PRIMARY KEY,
    data     VECTOR(5),
    data64   VECTOR64(10),
    VECTOR INDEX data USING HNSW ((VEC_COSINE_DISTANCE(data)))
);
```

如果已经创建了带有向量数据类型的表格，你可以通过 `ALTER TABLE` 的语法为向量数据创建索引，示例如下：

```sql
CREATE VECTOR INDEX idx ON t ((VEC_COSINE_DISTANCE(a))) USING HNSW;
CREATE VECTOR INDEX IF NOT EXISTS idx ON t ((VEC_COSINE_DISTANCE(a))) TYPE HNSW;
CREATE VECTOR INDEX ident ON db.t (ident, ident ASC ) TYPE HNSW;

ALTER TABLE t ADD VECTOR ((VEC_COSINE_DISTANCE(a))) USING HNSW COMMENT 'a';
ALTER TABLE t ADD VECTOR KEY ((VEC_COSINE_DISTANCE(a))) USING HNSW COMMENT 'a';
ALTER TABLE t ADD VECTOR INDEX ((VEC_COSINE_DISTANCE(a))) USING HNSW COMMENT 'a';
ALTER TABLE t ADD VECTOR INDEX IF NOT EXISTS ((VEC_COSINE_DISTANCE(a))) USING HNSW COMMENT 'a';
```

> **Note:**
>
> 创建向量索引的语法可能在今后的版本中发生变化。

创建向量索引时，需要通过 `distance=<metric>` 配置指定距离度量：

- 余弦距离: `COMMENT "hnsw(distance=cosine)"`
- L2 距离: `COMMENT "hnsw(distance=l2)"`

只能为固定维度的向量列 (如 `VECTOR(3)` ) 创建向量索引。它不能为混合维度的向量列 (如 `VECTOR` ) 创建，因为向量距离只能在具有相同维度的向量之间计算。

如果你使用的是编程语言 SDK 或 ORM，请参阅以下文档以创建向量索引：

- Python: [TiDB Vector SDK for Python](https://github.com/pingcap/tidb-vector-python)
- Python: [SQLAlchemy](/vector-search-integrate-with-sqlalchemy.md)
- Python: [Peewee](/vector-search-integrate-with-peewee.md)
- Python: [Django](/vector-search-integrate-with-django-orm.md)

创建向量索引时请注意以下限制。这些限制可能会在今后的版本中取消：

- 向量索引暂不支持 L1 距离和内积。

- 只有在创建表时才能定义和创建矢量索引。创建表后，不能使用 DDL 语句创建矢量索引。也不能使用 DDL 语句删除矢量索引。


## 使用向量搜索索引

在 K 近邻搜索查询中，可以使用 `ORDER BY ... LIMIT` 形式来使用向量搜索索引，如下所示：

```sql
SELECT *
FROM vector_table_with_index
ORDER BY Vec_Cosine_Distance(embedding, '[1, 2, 3]')
LIMIT 10
```

如果要在向量搜索中使用索引，则必须使用与创建向量索引时所定义的相同的距离度量。

## 使用带过滤器的向量搜索索引

包含预过滤 (使用 `WHERE` 子句) 的查询不能使用向量搜索索引，因为它们不是根据 SQL 语义查询的 K 近邻。例如

```sql
-- 过滤器在 kNN 之前执行，因此不能使用向量搜索索引：

SELECT * FROM vec_table
WHERE category = "document"
ORDER BY Vec_Cosine_distance(embedding, '[1, 2, 3]')
LIMIT 5;
```

以下是几种变通方法：

**向量搜索后的后置过滤器:** 首先查询 K 个最近的邻居，然后过滤掉不需要的结果：

```sql
-- 对于这些查询，过滤器是在 kNN 之后执行的，因此可以使用向量索引：

SELECT * FROM
(
  SELECT * FROM vec_table
  ORDER BY Vec_Cosine_distance(embedding, '[1, 2, 3]')
  LIMIT 5
) t
WHERE category = "document";

-- 请注意，如果过滤掉一些结果，此查询返回的结果可能少于 5 个。
```

**使用表格分区**: [表分区](/partitioned-table.md)内的查询可以充分利用向量索引。如果要执行相等条件的过滤器，这将非常有效，因为相等条件的过滤器可以转化为访问指定分区。

举例说明： 假设您想查找与特定产品版本最接近的文档。

```sql
-- 过滤器在 kNN 之前执行，因此不能使用向量索引：
SELECT * FROM docs
WHERE ver = "v2.0"
ORDER BY Vec_Cosine_distance(embedding, '[1, 2, 3]')
LIMIT 5;
```

与其使用 `WHERE` 子句编写查询，不如对表进行分区，然后使用 [`PARTITION` 关键字](/partitioned-table.md#partition-selection) 在分区内进行查询：

```sql
CREATE TABLE docs (
    id INT,
    ver VARCHAR(10),
    doc TEXT,
    embedding VECTOR(3) COMMENT "hnsw(distance=cosine)"
) PARTITION BY LIST COLUMNS (ver) (
    PARTITION p_v1_0 VALUES IN ('v1.0'),
    PARTITION p_v1_1 VALUES IN ('v1.1'),
    PARTITION p_v1_2 VALUES IN ('v1.2'),
    PARTITION p_v2_0 VALUES IN ('v2.0')
);

SELECT * FROM docs
PARTITION (p_v2_0)
ORDER BY Vec_Cosine_distance(embedding, '[1, 2, 3]')
LIMIT 5;
```

更多信息，请参阅 [表分区](/partitioned-table.md)。

## 查看索引构建进度

与其他索引不同，向量搜索索引是异步建立的。因此，在批量数据插入后，向量索引可能无法立即使用。这不会影响数据的正确性或一致性，你可以随时执行向量搜索并获得完整的结果。不过，在向量搜索索引完全建立之前，性能将不会达到最佳。

要查看索引构建进度，可以按如下方式查询 `INFORMATION_SCHEMA.TIFLASH_INDEXES` 表：

```sql
SELECT * FROM INFORMATION_SCHEMA.TIFLASH_INDEXES;
+---------------+------------+----------------+----------+--------------------+-------------+-----------+------------+---------------------+-------------------------+--------------------+------------------------+------------------+
| TIDB_DATABASE | TIDB_TABLE | TIDB_PARTITION | TABLE_ID | BELONGING_TABLE_ID | COLUMN_NAME | COLUMN_ID | INDEX_KIND | ROWS_STABLE_INDEXED | ROWS_STABLE_NOT_INDEXED | ROWS_DELTA_INDEXED | ROWS_DELTA_NOT_INDEXED | TIFLASH_INSTANCE |
+---------------+------------+----------------+----------+--------------------+-------------+-----------+------------+---------------------+-------------------------+--------------------+------------------------+------------------+
| test          | sample     | NULL           |      106 |                 -1 | vec         |         2 | HNSW       |                   0 |                   13000 |                  0 |                   2000 | store-6ba728d2   |
| test          | sample     | NULL           |      106 |                 -1 | vec         |         2 | HNSW       |               10500 |                       0 |                  0 |                   4500 | store-7000164f   |
+---------------+------------+----------------+----------+--------------------+-------------+-----------+------------+---------------------+-------------------------+--------------------+------------------------+------------------+
```

- `ROWS_STABLE_INDEXED` 和 `ROWS_STABLE_NOT_INDEXED` 列显示索引构建进度。当 `ROWS_STABLE_NOT_INDEXED` 变为 0 时，索引构建完成。

    作为参考，500 MiB 的向量数据集构建索引的过程可能需要 20 分钟。索引构建器可以在多个表中并行构建向量搜索索引。目前不支持调整索引构建器的优先级或速度。

- `ROWS_DELTA_NOT_INDEXED` 列显示 Delta 层中的行数。Delta 层存储 _最近_ 插入或更新的行，并根据写入工作量定期合并到稳定层。这个合并过程称为 “压缩”。

    Delta 层始终没有索引。为了达到最佳性能，可以强制将 Delta 层合并到稳定层，这样所有数据都能被索引：

    ```sql
    ALTER TABLE <TABLE_NAME> COMPACT;
    ```

    更多信息，请参阅 [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md)。

## 检查是否使用了向量搜索索引

使用 [`EXPLAIN`](/sql-statements/sql-statement-explain.md) 或 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 语句检查该查询是否使用了向量搜索索引。当 `annIndex:` 出现在 `TableFullScan` 执行计划的 `operator info` 列中时，表示该表扫描使用了向量搜索索引。

**示例：使用向量索引**

```sql
[tidb]> EXPLAIN SELECT * FROM vector_table_with_index
ORDER BY Vec_Cosine_Distance(embedding, '[1, 2, 3]')
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

**示例：由于未指定 Top K，因此未使用向量搜索索引**

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

当无法使用向量搜索索引时，在某些情况下会出现警告，以帮助你了解原因：

```sql
-- 使用了错误的距离度量：
[tidb]> EXPLAIN SELECT * FROM vector_table_with_index
ORDER BY Vec_l2_Distance(embedding, '[1, 2, 3]')
LIMIT 10;

[tidb]> SHOW WARNINGS;
ANN index not used: not ordering by COSINE distance

-- 使用错误的顺序：
[tidb]> EXPLAIN SELECT * FROM vector_table_with_index
ORDER BY Vec_Cosine_Distance(embedding, '[1, 2, 3]') DESC
LIMIT 10;

[tidb]> SHOW WARNINGS;
ANN index not used: index can be used only when ordering by vec_cosine_distance() in ASC order
```

## 分析向量搜索性能

[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 语句包含关于如何在 `execution info` 列中使用向量索引的详细信息：

```sql
[tidb]> EXPLAIN ANALYZE SELECT * FROM vector_table_with_index
ORDER BY Vec_Cosine_Distance(embedding, '[1, 2, 3]')
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

> **Note:**
>
> 执行信息为内部信息。字段和格式如有更改，恕不另行通知。请勿依赖。

一些重要字段的解释：

- `vector_index.load.total`: 加载索引的总持续时间。该字段可能大于实际查询时间，因为可能会并行加载多个矢量索引。
- `vector_index.load.from_s3`: 从 S3 加载的索引数量。
- `vector_index.load.from_disk`: 从磁盘加载的索引数量。索引之前已从 S3 下载。
- `vector_index.load.from_cache`: 从缓存中加载的索引数量。索引之前已从 S3 下载。
- `vector_index.search.total`: 在索引中搜索的总持续时间。延迟大通常意味着索引是冷索引（以前从未被访问过，或很久以前被访问过），因此在索引中搜索时会产生大量 IO。这个字段可能大于实际查询时间，因为可能会并行搜索多个矢量索引。
- `vector_index.search.discarded_nodes`: 在搜索过程中已访问但被丢弃的向量行数。搜索结果不会考虑这些被丢弃的向量。如果数值较大，通常表示有很多由 UPDATE 或 DELETE 语句引起的陈旧行。

请参阅 [`EXPLAIN`](/sql-statements/sql-statement-explain.md)、[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)，以及 [EXPLAIN Walkthrough](/explain-walkthrough.md) 来解释输出结果。

## 向量搜索索引的约束

- TiDB 集群需要创建 TiFlash 的副本
- 不能是主键索引
- 不能是复合索引
- 不可以为同一列创建多个向量索引
- 向量索引需要指定距离函数（目前只支持 `余弦距离` 和 `L2 距离`）
- 不支持删除具有向量索引的列，也不支持同时创建多个索引。

## See also

- [优化向量搜索性能](/vector-search-improve-performance.md)
- [向量数据类型](/vector-search-data-types.md)