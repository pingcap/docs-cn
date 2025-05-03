---
title: 数值列倒排索引
summary: 了解如何在 TiDB 中构建并使用数值列倒排索引加速 OLAP 场景的查询。
---

# 数值列倒排索引

倒排索引是信息检索领域常用的索引技术。它将文本划分为单个词，并构建词->文档 ID 索引，以便快速搜索确定哪些文档包含特定的词。

对于数值列（整数、时间和日期类型），我们可以简化存储从数字到其在列中位置的映射（值 → rowid）。因此，使用倒排索引，可以快速查找包含特定值的行，从而加快 WHERE 子句的处理速度。

## 适用场景

数值列倒排索引在 TiFlash 中构建，支持数值、日期时间类型的 =, !=, >, >=, <, <=, in 快速过滤，在以下场景中数值列倒排索引有明显优势：

- 过滤条件过滤率高，但过滤后行数依然较多。TiFlash 批量读取性能可能优于 TiKV 索引回表。
- 查询条件涉及多列，每列单独过滤后都留存有大量数据，但组合所有列进行过滤后行数较少。此时可以使用倒排索引，在 TiFlash 本地进行索引组合过滤，降低查询延迟。
- 查询 WHERE 子句同时包含简单等值、范围过滤条件和复杂函数过滤条件。数值列倒排索引帮忙提前过滤掉不满足简单等值、范围过滤条件的行，从而减少复杂函数过滤条件的计算量。

## 创建数值列倒排索引

在 TiDB 中，你可以通过以下任一种方式为数值列创建倒排索引。

- 在建表时，使用以下语法来指定为哪一个列创建数值列倒排索引：

    ```sql
    CREATE TABLE foo (
        id          INT PRIMARY KEY,
        count       INT,
        create_date DATE,
        COLUMNAR INDEX idx_count (count) USING INVERTED,
        COLUMNAR INDEX idx_create_date (create_date) USING INVERTED
    );
    ```

- 对于现有的表，可以通过以下语法为数值列创建倒排索引：

    ```sql
    CREATE COLUMNAR INDEX idx_count ON foo (count) USING INVERTED;
    ALTER TABLE foo ADD COLUMNAR INDEX idx_count (count) USING INVERTED;
    ```

> **注意：**
>
> 数值列倒排索引功能的实现需要基于表的 TiFlash 副本。
>
> - 在建表时如果定义了数值列倒排索引，TiDB 将自动为该表创建一个 TiFlash 副本。
> - 如果建表时未定义数值列倒排索引，并且该表当前没有 TiFlash 副本，那么为该表添加数值列倒排索引时，你需要先手动为该表创建 TiFlash 副本，例如：`ALTER TABLE 'table_name' SET TIFLASH REPLICA 1;`。

## 使用数值列倒排索引

TiDB 优化器会自动选择使用倒排索引来加速查询，如下所示：

```sql
SELECT *
FROM foo
WHERE count > 10;
```

带有多个过滤条件的 WHERE 子句也可以使用数值列倒排索引：

```sql
SELECT *
FROM foo
WHERE count > 10 AND create_date = '2023-01-01';
```

## 查看索引构建进度

当插入大批量数据后，部分数据可能没有立即持久化到 TiFlash 中。对于已经持久化的数据，数值列倒排索引是通过同步的方式构建的；对于尚未未持久化的数据，数值列倒排索引会在数据持久化后才开始构建，但这并不会影响数据的准确性和一致性。你仍然可以随时进行查询，并获得完整的结果，但需要注意的是，查询性能只有在数值列倒排索引完全构建好之后才会达到最佳水平。

要查看索引构建进度，可以按如下方式查询 `INFORMATION_SCHEMA.TIFLASH_INDEXES` 表：

```sql
SELECT * FROM INFORMATION_SCHEMA.TIFLASH_INDEXES;
+---------------+------------+----------+-------------+-----------------+-----------+----------+------------+---------------------+-------------------------+--------------------+------------------------+---------------+------------------+
| TIDB_DATABASE | TIDB_TABLE | TABLE_ID | COLUMN_NAME | INDEX_NAME      | COLUMN_ID | INDEX_ID | INDEX_KIND | ROWS_STABLE_INDEXED | ROWS_STABLE_NOT_INDEXED | ROWS_DELTA_INDEXED | ROWS_DELTA_NOT_INDEXED | ERROR_MESSAGE | TIFLASH_INSTANCE |
+---------------+------------+----------+-------------+-----------------+-----------+----------+------------+---------------------+-------------------------+--------------------+------------------------+---------------+------------------+
| test          | foo        |      112 | count       | idx_count       |         2 |        1 | Inverted   |                   1 |                       0 |                  0 |                      0 |               | 127.0.0.1:3930   |
| test          | foo        |      112 | create_date | idx_create_date |         3 |        2 | Inverted   |                   1 |                       0 |                  0 |                      0 |               | 127.0.0.1:3930   |
+---------------+------------+----------+-------------+-----------------+-----------+----------+------------+---------------------+-------------------------+--------------------+------------------------+---------------+------------------+
```

- 可以通过 `ROWS_STABLE_INDEXED` 和 `ROWS_STABLE_NOT_INDEXED` 列查看索引构建进度。当 `ROWS_STABLE_NOT_INDEXED` 变为 0 时，表示索引构建完成。

- 可以通过 `ROWS_DELTA_NOT_INDEXED` 列查看 Delta 层中的行数。TiFlash 存储层的数据主要存放在 Delta 层和 Stable 层。Delta 层存储最近插入或更新的行，并根据写入工作量定期将这些行合并到 Stable 层。这个合并过程称为“压缩”。

    Delta 层可能仅有部分数据是包含索引的，为了达到最佳性能，你可以强制将 Delta 层合并到 Stable 层，以确保所有的数据都能够被索引：

    ```sql
    ALTER TABLE <TABLE_NAME> COMPACT;
    ```

    更多信息，请参阅 [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md)。

此外，你也可以通过 `ADMIN SHOW DDL JOBS;` 查看 DDL 任务的执行进度，观察其 `row count`。不过这种方式并不准确，`row count` 的值是从 `TIFLASH_INDEXES` 里的 `rows_stable_indexed` 获取的。你也可以使用此方式查看索引构建进度。

## 查看是否使用了数值列倒排索引

你可以使用 [`EXPLAIN`](/sql-statements/sql-statement-explain.md) 或 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 语句查看一个查询是否使用了数值列倒排索引。如果 `TableFullScan` 执行计划的 `operator info` 列中出现了 `invertedIndex:`，表示 TiDB 在扫描该表时使用了数值列倒排索引。

**示例：使用了数值列倒排索引的查询**

```sql
[tidb]> EXPLAIN SELECT * FROM foo WHERE count < 10;
+-----+-----------------------------------------------------------------------------------+
| ... | operator info                                                                     |
+-----+-----------------------------------------------------------------------------------+
| ... | MppVersion: 3, data:ExchangeSender_12                                             |
| ... | ExchangeType: PassThrough                                                         |
| ... | lt(test.foo.count, 10)                                                            |
| ... | pushed down filter:empty, keep order:false, stats:pseudo, invertedIndex:idx_count |
+-----+-----------------------------------------------------------------------------------+
4 rows in set (0.00 sec)
[tidb]> EXPLAIN SELECT * FROM foo WHERE create_date < DATE('2025-05-01');
+-----+-----------------------------------------------------------------------------------------+
| ... | operator info                                                                           |
+-----+-----------------------------------------------------------------------------------------+
| ... | MppVersion: 3, data:ExchangeSender_12                                                   |
| ... | ExchangeType: PassThrough                                                               |
| ... | lt(test.foo.create_date, 2025-05-01)                                                    |
| ... | pushed down filter:empty, keep order:false, stats:pseudo, invertedIndex:idx_create_date |
+-----+-----------------------------------------------------------------------------------------+
4 rows in set (0.00 sec)
```

**示例：由于过滤条件过滤效果不佳，优化器选择不使用数值列倒排索引的查询**

```sql
[tidb]> EXPLAIN SELECT * FROM foo WHERE create_date != DATE('2025-05-01');
+-----+----------------------------------------------------------+
| ... | operator info                                            |
+-----+----------------------------------------------------------+
| ... | MppVersion: 3, data:ExchangeSender_12                    |
| ... | ExchangeType: PassThrough                                |
| ... | ne(test.foo.create_date, 2025-05-01)                     |
| ... | pushed down filter:empty, keep order:false, stats:pseudo |
+-----+----------------------------------------------------------+
4 rows in set (0.00 sec)
```

## 分析数值列倒排索引性能

你可以执行 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 语句，然后查看输出中的 `execution info` 列了解数值列倒排索引使用情况的详细信息：

```sql
[tidb]> EXPLAIN ANALYZE SELECT * FROM foo WHERE create_date > DATE('2025-05-01');
+-----+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----+
|     | execution info                                                                                                                                                                     |     |
+-----+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----+
| ... | time:9.47ms, open:1.2ms, close:8.47µs, loops:1, RU:1.00, cop_task: {num: 1, max: 0s, proc_keys: 0, copr_cache_hit_ratio: 0.00}                                                     | ... |
| ... | tiflash_task:{time:6.36ms, loops:0, threads:72}                                                                                                                                    | ... |
| ... | tiflash_task:{time:5.36ms, loops:0, threads:72}                                                                                                                                    | ... |
| ... | tiflash_task:{...}, inverted_idx:{load:{total:13ms,from_s3:0,from_disk:0,from_cache:864},search:{total:986ms,skipped_packs:29765,indexed_rows:600011622,selected_rows:845092}} ... | ... |
+-----+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----+
```

> **注意：**
>
> 执行信息为 TiDB 内部信息。字段和格式如有更改，恕不另行通知。请勿依赖。

以下为一些重要字段的解释：

- `inverted_idx.load.total`：加载索引的总时长。该字段的值可能会超过查询实际耗时，因为 TiDB 可能会并行加载多个数值列倒排索引。
- `inverted_idx.load.from_s3`：从 S3 加载的索引数量。
- `inverted_idx.load.from_disk`：从磁盘加载的索引数量。这些索引之前已经从 S3 下载到磁盘上。
- `inverted_idx.load.from_cache`：从缓存中加载的索引数量。这些索引之前已经从 S3 下载并存储在缓存中。
- `inverted_idx.search.total`：在索引中搜索的总时长。如果该时间存在较大的延迟，通常意味着该索引为冷索引（以前从未被访问过，或很久以前被访问过），因此在索引中搜索时会产生较多的 I/O 操作。该字段的值可能会超过查询实际耗时，因为 TiDB 可能会并行搜索多个数值列倒排索引。
- `inverted_idx.search.skipped_packs`：在搜索过程中跳过的 Pack 的数量。Pack 是 TiFlash 中存储数据的基本单位。TiFlash 会将数据分成多个 Pack 进行存储和索引。该字段的值越大，表示在搜索过程中跳过的 Pack 越多，减少的 I/O 操作越多。
- `inverted_idx.search.indexed_rows`：被索引的总行数。
- `inverted_idx.search.selected_rows`：在搜索过程中被选中的总行数。

关于执行信息输出的更多信息，请参阅 [`EXPLAIN`](/sql-statements/sql-statement-explain.md)、[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)，以及[使用 `EXPLAIN` 解读执行计划](/explain-walkthrough.md)。

## 使用限制

- 集群需要提前部署 TiFlash 节点。
- 数值列倒排索引不能作为主键或者唯一索引。
- 数值列倒排索引只能基于单一的数值列创建，不能与其他列组合形成复合索引。
- 不支持直接删除具有数值列倒排索引的列。可以通过先删除列上的数值列倒排索引，再删除列的方式完成删除。
- 不支持对带有数值列倒排索引的列进行 [Reorg 类型变更](/sql-statements/sql-statement-modify-column.md)。
- 不支持将数值列倒排索引[设置为不可见](/sql-statements/sql-statement-alter-index.md)。
- 不支持在开启了[静态加密](/encryption-at-rest.md)的 TiFlash 节点上构建数值列倒排索引。
