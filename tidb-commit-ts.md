---
title: _tidb_commit_ts
summary: 了解如何读取隐藏列 `_tidb_commit_ts`、在查询中使用该列，以及该列的只读限制和执行计划限制。
---

# _tidb_commit_ts

`_tidb_commit_ts` 是一个隐藏系统列，用于显示行在本地 TiDB 集群中的提交时间戳。TiDB 从事务的 MVCC 提交记录中获取此时间戳，并将其作为无符号的 `BIGINT` 值返回。使用 `SELECT *` 时不会显示此列，但你可以显式指定列名来引用它。

你可以使用该列比较行版本、检查行的提交顺序，或根据提交时间戳删除行。已提交的行通常具有大于 0 的时间戳。在 TiDB 内部，对于尚未提交的行版本，该值可能为 `NULL`。

## 读取 `_tidb_commit_ts`

你无需启用会话特性，即可从常规 TiDB 表中查询 `_tidb_commit_ts`：

```sql
CREATE TABLE t (
    id INT PRIMARY KEY,
    value VARCHAR(20)
);

INSERT INTO t VALUES (1, 'a'), (2, 'b');

SELECT id, _tidb_commit_ts > 0 AS has_commit_ts
FROM t
ORDER BY id;
```

```sql
+----+----------------+
| id | has_commit_ts  |
+----+----------------+
|  1 |              1 |
|  2 |              1 |
+----+----------------+
```

你可以在表达式和谓词中使用该列，包括在 JOIN 和集合操作中使用：

```sql
SELECT id
FROM t
WHERE _tidb_commit_ts > 0
ORDER BY id;

SELECT _tidb_commit_ts > 0 AS has_commit_ts FROM t
UNION ALL
SELECT _tidb_commit_ts > 0 FROM t;
```

读取 `_tidb_commit_ts` 不受 `tidb_mview_enable` 的值影响。

## 使用表扫描和索引扫描读取 `_tidb_commit_ts`

读取 `_tidb_commit_ts` 时，TiDB 会使用能够将提交时间戳和行数据一起返回的下推扫描。例如，按主键查询时，执行计划会使用表范围扫描：

```sql
EXPLAIN FORMAT = 'plan_tree'
SELECT _tidb_commit_ts FROM t WHERE id = 1;
```

执行计划包含 `TableReader`，其下包含 `TableRangeScan`。对于使用二级索引的谓词，TiDB 可以使用索引回表：

```sql
ALTER TABLE t ADD INDEX idx_value (value);

EXPLAIN FORMAT = 'plan_tree'
SELECT _tidb_commit_ts
FROM t USE INDEX (idx_value)
WHERE value = 'a';
```

执行计划包含 `IndexLookUp`，查询会返回匹配行的提交时间戳。由于 `Point_Get`、`Batch_Point_Get` 或单独的 `IndexReader` 无法提供 `_tidb_commit_ts`，TiDB 不会将这些查询转换为这些执行算子。

## 在 DML 表达式中使用 `_tidb_commit_ts`

你可以在 `UPDATE`、`INSERT ... SELECT` 和 `DELETE` 语句中读取该列，用于过滤或计算值。读取该列不会修改其值：

```sql
UPDATE t
SET value = CONCAT(value, '-updated')
WHERE _tidb_commit_ts > 0;

CREATE TABLE t_copy (id INT, commit_ts BIGINT UNSIGNED);

INSERT INTO t_copy
SELECT id, _tidb_commit_ts
FROM t
WHERE _tidb_commit_ts > 0;

DELETE FROM t
WHERE _tidb_commit_ts = 0;
```

如果没有提交时间戳为 0 的行，最后一条语句不会删除任何行。你可以使用 `_tidb_commit_ts > 0` 等范围谓词，根据提交时间戳条件删除行。

## 使用限制

- `_tidb_commit_ts` 是只读列。你不能在 `INSERT`、`REPLACE`、`UPDATE` 或 `INSERT ... ON DUPLICATE KEY UPDATE` 语句中为其赋值。尝试写入时会返回类似 `Usage of column name '_tidb_commit_ts' is not supported for now` 的错误。
- 不要将用户列命名为 `_tidb_commit_ts`。该名称由隐藏系统列保留。
- 读取 `_tidb_commit_ts` 的查询不能使用索引合并。如果强制使用索引合并执行计划，TiDB 会返回无法找到合适物理执行计划的错误。
- 通过表缓存读取表时不支持 `_tidb_commit_ts`。如果查询同时使用该列和表缓存，TiDB 会返回类似 `'_tidb_commit_ts' is unsupported on cache tables.` 的错误。
- 该时间戳是 MVCC 提交时间戳，而不是实际时间。要将其解释为时间，请使用适合你的 TiDB 部署的时间戳工具，不要将该数值直接视为 Unix 时间戳。

## 另请参阅

- [乐观事务](/optimistic-transaction.md)
- [悲观事务](/pessimistic-transaction.md)
- [TiCDC 协议](/ticdc/ticdc-avro-protocol.md)
