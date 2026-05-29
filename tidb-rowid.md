---
title: _tidb_rowid
summary: 了解 `_tidb_rowid` 是什么，何时可用，以及如何安全地使用它。
---

# _tidb_rowid

`_tidb_rowid` 是 TiDB 自动生成的一个隐藏系统列，在没有使用聚簇索引的表中作为表的内部行 ID。你无法在表结构中定义或修改此列，但当表使用 `_tidb_rowid` 作为其内部行 ID 时，可以在 SQL 语句中引用它。

在当前实现中，`_tidb_rowid` 是一个由 TiDB 自动维护的 `BIGINT NOT NULL` 列。

> **警告：**
>
> - 不要假设 `_tidb_rowid` 在所有情况下都是全局唯一的。对于不使用聚簇索引的分区表，执行 `ALTER TABLE ... EXCHANGE PARTITION` 后，不同分区之间可能出现相同的 `_tidb_rowid`。
> - 如果你需要一个稳定的唯一标识符，请定义并使用显式主键，而不是依赖 `_tidb_rowid`。

## `_tidb_rowid` 何时可用

当表没有使用聚簇主键作为行的唯一标识时，TiDB 会使用 `_tidb_rowid` 来标识每一行。实际上，这意味着以下表类型会使用 `_tidb_rowid`：

- 没有主键的表
- 主键显式定义为 `NONCLUSTERED` 的表

`_tidb_rowid` 不适用于使用聚簇索引的表，即主键定义为 `CLUSTERED` 的表（无论是单列主键还是复合主键）。

以下示例显示了区别：

```sql
CREATE TABLE t1 (a INT, b VARCHAR(20));
CREATE TABLE t2 (id BIGINT PRIMARY KEY NONCLUSTERED, a INT);
CREATE TABLE t3 (id BIGINT PRIMARY KEY CLUSTERED, a INT);
```

对于 `t1` 和 `t2`，你可以查询 `_tidb_rowid`，因为这两个表没有使用聚簇索引作为行标识：

```sql
SELECT _tidb_rowid, a, b FROM t1;
SELECT _tidb_rowid, id, a FROM t2;
```

对于 `t3`，`_tidb_rowid` 不可用，因为该表使用了聚簇索引作为行标识，：

```sql
SELECT _tidb_rowid, id, a FROM t3;
```

```sql
ERROR 1054 (42S22): Unknown column '_tidb_rowid' in 'field list'
```

## 读取 `_tidb_rowid`

对于使用了 `_tidb_rowid` 的表，你可以在 `SELECT` 语句中查询 `_tidb_rowid`。这对于分页查询、故障排除和批量处理等任务非常有用。

示例：

```sql
CREATE TABLE t (a INT, b VARCHAR(20));
INSERT INTO t VALUES (1, 'x'), (2, 'y');

SELECT _tidb_rowid, a, b FROM t ORDER BY _tidb_rowid;
```

```sql
+-------------+---+---+
| _tidb_rowid | a | b |
+-------------+---+---+
|           1 | 1 | x |
|           2 | 2 | y |
+-------------+---+---+
```

要查看 TiDB 将要分配的下一个行 ID 值，请使用 `SHOW TABLE ... NEXT_ROW_ID`：

```sql
SHOW TABLE t NEXT_ROW_ID;
```

```sql
+-----------------------+------------+-------------+--------------------+-------------+
| DB_NAME               | TABLE_NAME | COLUMN_NAME | NEXT_GLOBAL_ROW_ID | ID_TYPE     |
+-----------------------+------------+-------------+--------------------+-------------+
| update_doc_rowid_test | t          | _tidb_rowid |              30001 | _TIDB_ROWID |
+-----------------------+------------+-------------+--------------------+-------------+
```

## 写入 `_tidb_rowid`

默认情况下，TiDB 不允许通过 `INSERT`、`REPLACE` 或 `UPDATE` 语句中直接写入 `_tidb_rowid`。

```sql
INSERT INTO t(_tidb_rowid, a, b) VALUES (101, 4, 'w');
```

```sql
ERROR 1105 (HY000): insert, update and replace statements for _tidb_rowid are not supported
```

在数据导入或迁移场景中，如需保留原始行 ID，请先启用系统变量 [`tidb_opt_write_row_id`](/system-variables.md#tidb_opt_write_row_id)：

```sql
SET @@tidb_opt_write_row_id = ON;
INSERT INTO t(_tidb_rowid, a, b) VALUES (100, 3, 'z');
SET @@tidb_opt_write_row_id = OFF;

SELECT _tidb_rowid, a, b FROM t WHERE _tidb_rowid = 100;
```

```sql
+-------------+---+---+
| _tidb_rowid | a | b |
+-------------+---+---+
|         100 | 3 | z |
+-------------+---+---+
```

> **警告：**
>
> `tidb_opt_write_row_id` 仅用于导入和迁移场景。不推荐用于常规应用程序写入。

## 限制

- 不能创建名为 `_tidb_rowid` 的用户列。
- 不能将现有用户列重命名为 `_tidb_rowid`。
- `_tidb_rowid` 是 TiDB 内部列，不适合作为业务主键或长期标识。
- 在分区的非聚簇表上，`_tidb_rowid` 的值不保证在分区之间是唯一的。执行 `EXCHANGE PARTITION` 后，不同分区可能包含具有相同 `_tidb_rowid` 值的行。
- `_tidb_rowid` 是否存在取决于表结构。对于使用聚簇索引的表，应使用主键作为行标识。

## 解决热点问题

对于使用 `_tidb_rowid` 的表，TiDB 默认按递增顺序分配行 ID。在写密集型工作负载下，这可能会导致写热点。

要缓解此问题（针对依赖 `_tidb_rowid` 作为行 ID 的表），请考虑使用 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)将行 ID 打散分布，并在需要时使用 [`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions) 提前分裂 Region。

示例：

```sql
CREATE TABLE t (
    id BIGINT PRIMARY KEY NONCLUSTERED,
    c INT
) SHARD_ROW_ID_BITS = 4;
```

`SHARD_ROW_ID_BITS` 仅适用于使用 `_tidb_rowid` 的表，不适用于聚簇索引表。

## 相关语句和变量

- [`SHOW TABLE NEXT_ROW_ID`](/sql-statements/sql-statement-show-table-next-rowid.md)：显示 TiDB 将要分配的下一个行 ID
- [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)：分片隐式行 ID 以减少热点
- [`Clustered Indexes`](/clustered-indexes.md)：解释了何时表使用主键而不是 `_tidb_rowid`
- [`tidb_opt_write_row_id`](/system-variables.md#tidb_opt_write_row_id)：控制是否允许写入 `_tidb_rowid`

## 另请参阅

- [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)
- [`AUTO_INCREMENT`](/auto-increment.md)
- [非事务 DML 语句](/non-transactional-dml.md)