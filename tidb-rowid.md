---
title: _tidb_rowid
summary: 了解 `_tidb_rowid` 是什么，何时可用，以及如何安全地使用它。
---

# _tidb_rowid

`_tidb_rowid` 是一个 TiDB 使用的隐藏系统列，作为不使用聚集索引的表的行句柄。你不需要在表模式中声明此列，但当表使用 `_tidb_rowid` 作为其句柄时，你可以在 SQL 中引用它。

在当前实现中，`_tidb_rowid` 是一个由 TiDB 管理的额外的 `BIGINT NOT NULL` 句柄列。

> **警告：**
>
> - 在所有情况下，不要假定 `_tidb_rowid` 是全局唯一的。对于不使用聚集索引的分区表，执行 `ALTER TABLE ... EXCHANGE PARTITION` 可能会导致不同分区具有相同的 `_tidb_rowid` 值。
> - 如果你需要一个稳定的唯一标识符，请定义并使用显式主键，而不是依赖 `_tidb_rowid`。

## `_tidb_rowid` 何时可用

`_tidb_rowid` 可用于其行句柄不是聚集主键的表。实际上，这意味着以下表类型会使用 `_tidb_rowid`：

- 没有主键的表
- 主键显式定义为 `NONCLUSTERED` 的表

`_tidb_rowid` 不适用于使用聚集索引的表，包括以下情况：

- 主键为整数且作为聚集行句柄的表
- 在复合主键上具有聚集索引的表

以下示例显示了区别：

```sql
CREATE TABLE t1 (a INT, b VARCHAR(20));
CREATE TABLE t2 (id BIGINT PRIMARY KEY NONCLUSTERED, a INT);
CREATE TABLE t3 (id BIGINT PRIMARY KEY CLUSTERED, a INT);
```

对于 `t1` 和 `t2`，你可以查询 `_tidb_rowid`：

```sql
SELECT _tidb_rowid, a, b FROM t1;
SELECT _tidb_rowid, id, a FROM t2;
```

对于 `t3`，`_tidb_rowid` 不可用，因为聚集主键已经是行句柄：

```sql
SELECT _tidb_rowid, id, a FROM t3;
```

```sql
ERROR 1054 (42S22): Unknown column '_tidb_rowid' in 'field list'
```

## 读取 `_tidb_rowid`

对于支持的表，你可以在 `SELECT` 语句中使用 `_tidb_rowid`。这对于分页、故障排除和批量处理等任务非常有用。

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

要检查 TiDB 将要分配的下一个行 ID 值，请使用 `SHOW TABLE ... NEXT_ROW_ID`：

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

默认情况下，TiDB 不允许 `INSERT`、`REPLACE` 或 `UPDATE` 语句直接写入 `_tidb_rowid`。

```sql
INSERT INTO t(_tidb_rowid, a, b) VALUES (101, 4, 'w');
```

```sql
ERROR 1105 (HY000): insert, update and replace statements for _tidb_rowid are not supported
```

如果你需要在数据导入或迁移期间保留行 ID，请先启用系统变量 [`tidb_opt_write_row_id`](/system-variables.md#tidb_opt_write_row_id)：

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
- `_tidb_rowid` 是一个内部行句柄。不要将其视为长期业务键。
- 在分区的非聚集表上，`_tidb_rowid` 的值不保证在分区之间是唯一的。执行 `EXCHANGE PARTITION` 后，不同分区可能包含具有相同 `_tidb_rowid` 值的行。
- `_tidb_rowid` 是否存在取决于表布局。如果表使用聚集索引，请改用主键。

## 关于热点的考虑

对于使用 `_tidb_rowid` 的表，TiDB 默认按递增顺序分配行 ID。在写密集型工作负载下，这可能会导致写热点。

要缓解此问题（针对依赖隐式行 ID 的表），请考虑使用 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)，并在需要时使用 [`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions)。

示例：

```sql
CREATE TABLE t (
    id BIGINT PRIMARY KEY NONCLUSTERED,
    c INT
) SHARD_ROW_ID_BITS = 4;
```

`SHARD_ROW_ID_BITS` 仅适用于使用隐式行 ID 路径的表。它不适用于聚集索引表。

## 相关语句和变量

- [`SHOW TABLE NEXT_ROW_ID`](/sql-statements/sql-statement-show-table-next-rowid.md)：显示 TiDB 将要分配的下一个行 ID
- [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)：分片隐式行 ID 以减少热点
- [`Clustered Indexes`](/clustered-indexes.md)：解释了何时表使用主键而不是 `_tidb_rowid`
- [`tidb_opt_write_row_id`](/system-variables.md#tidb_opt_write_row_id)：控制是否允许写入 `_tidb_rowid`

## 另请参阅

- [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)
- [`AUTO_INCREMENT`](/auto-increment.md)
- [Non-transactional DML](/non-transactional-dml.md)