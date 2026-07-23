---
title: FLUSH STATS_DELTA
summary: TiDB 数据库中 FLUSH STATS_DELTA 的使用概况。
---

# FLUSH STATS_DELTA <span class="version-mark">从 v8.5.7 和 v9.0.0 开始引入</span>

通过 `FLUSH STATS_DELTA`，你可以将 TiDB 内存中缓存的待持久化的统计信息 delta 立即持久化到 [`mysql.stats_meta`](/mysql-schema/mysql-schema.md#statistics-system-tables) 系统表中。

当执行 `INSERT`、`UPDATE`、`DELETE` 等 DML 语句修改数据时，TiDB 会记录每张受影响的表中总行数和修改行数的变化，并将这些变化（即统计信息 delta）缓存在执行这些语句的 TiDB 节点的内存中。默认情况下，TiDB 每隔 20 * [`stats-lease`](/tidb-configuration-file.md#stats-lease)（默认 60 秒）会将这些 delta 持久化到 `mysql.stats_meta` 系统表中。详情参考[自动更新](/statistics.md#自动更新)。

由于[表的统计信息健康度](/sql-statements/sql-statement-show-stats-healthy.md)、[`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md) 的输出，以及统计信息自动收集的调度都依赖于已持久化的统计信息元数据，当你希望已持久化的统计信息元数据能立即反映最近的数据变更时（例如，在验证优化器行为的测试场景中），`FLUSH STATS_DELTA` 就会很有用。在你执行 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) 时，无需提前执行 `FLUSH STATS_DELTA`，因为 TiDB 会在收集某张表的统计信息之前，自动刷新该表待持久化的统计信息 delta。

## 语法概要

```ebnf+diagram
FlushStatsDeltaStmt ::=
    'FLUSH' 'STATS_DELTA' FlushTargetList ClusterOption?

FlushTargetList ::=
    FlushTarget (',' FlushTarget)*

FlushTarget ::=
    TableName
  | SchemaWildcard
  | GlobalWildcard

TableName ::=
    Identifier ('.' Identifier)?

SchemaWildcard ::=
    Identifier '.' '*'

GlobalWildcard ::=
    '*' '.' '*'

ClusterOption ::=
    'CLUSTER'
```

## 选项

- **Targets (`FlushTargetList`)**：指定要刷新统计信息 delta 的表。必须至少指定一个目标。
    - `table_name`：刷新当前数据库中指定表的统计信息 delta。如果你当前未选择数据库，TiDB 会返回 `No database selected` 错误。
    - `db_name.table_name`：刷新指定数据库中指定表的统计信息 delta。
    - `db_name.*`：刷新指定数据库中所有表的统计信息 delta。
    - `*.*`：刷新所有表的统计信息 delta。
- **`CLUSTER`**：在当前集群中的所有 TiDB 节点上执行该语句。每个 TiDB 节点都会缓存其自身执行的 DML 语句所产生的统计信息 delta。若不指定此选项，TiDB 只会持久化你当前连接的 TiDB 节点上缓存的统计信息 delta。

请注意以下行为：

- TiDB 会对要刷新的重复目标进行去重。例如，在 `FLUSH STATS_DELTA *.*, test.t` 中，`test.t` 会被忽略，因为 `*.*` 已涵盖所有表。类似地，在 `FLUSH STATS_DELTA test.*, test.t` 中，`test.t` 会被忽略，因为 `test.*` 已涵盖 `test` 数据库中的所有表。
- 对于分区表，TiDB 会持久化该表及其所有分区的统计信息 delta。
- 如果指定的数据库或表不存在，TiDB 会返回一条警告并跳过该目标。

## 示例

在数据变更后立即持久化单张表的统计信息 delta：

```sql
USE test;
CREATE TABLE t (a INT, b INT);
INSERT INTO t VALUES (1, 1), (2, 2), (3, 3);
FLUSH STATS_DELTA t;
```

```
Query OK, 0 rows affected (0.01 sec)
```

此时，TiDB 已将该表的行数变化持久化到 `mysql.stats_meta` 系统表。你可以使用 `SHOW STATS_META` 查看已持久化的值。注意，`SHOW STATS_META` 会从你当前连接的 TiDB 节点内存中读取统计信息。该 TiDB 节点会在 [`stats-lease`](/tidb-configuration-file.md#stats-lease)（默认 `3s`）周期内加载已持久化的值，因此刷新后的值可能会在短暂延迟后才显示在输出中：

```sql
SHOW STATS_META WHERE table_name = 't';
```

```
+---------+------------+----------------+---------------------+--------------+-----------+-------------------+
| Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count | Last_analyze_time |
+---------+------------+----------------+---------------------+--------------+-----------+-------------------+
| test    | t          |                | 2026-07-13 15:30:00 |            3 |         3 | NULL              |
+---------+------------+----------------+---------------------+--------------+-----------+-------------------+
1 row in set (0.01 sec)
```

持久化当前数据库中某张表以及 `sales` 数据库中所有表的统计信息 delta：

```sql
FLUSH STATS_DELTA t, sales.*;
```

持久化集群中每个 TiDB 节点上缓存的所有表的统计信息 delta：

```sql
FLUSH STATS_DELTA *.* CLUSTER;
```

## 权限

执行 `FLUSH STATS_DELTA` 时，需要对操作对象拥有 `SELECT` 权限：

- 对于 `table_name` 或 `db_name.table_name`，你需要具有目标表的 `SELECT` 权限；
- 对于 `db_name.*`，你需要具有目标数据库的 `SELECT` 权限；
- 对于 `*.*`，你需要具有全局 `SELECT` 权限。

与其他 `FLUSH` 语句不同，`FLUSH STATS_DELTA` 不需要 `RELOAD` 权限。

## MySQL 兼容性

`FLUSH STATS_DELTA` 是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

- [常规统计信息](/statistics.md)
- [`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md)
- [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)
- [`REFRESH STATS`](/sql-statements/sql-statement-refresh-stats.md)