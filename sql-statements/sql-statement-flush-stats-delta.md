---
title: FLUSH STATS_DELTA
summary: TiDB 数据库中 FLUSH STATS_DELTA 用法概述。
---

# FLUSH STATS_DELTA <span class="version-mark">于 v8.5.7 和 v9.0.0 新增</span>

`FLUSH STATS_DELTA` 会立即将 TiDB 内存中缓冲的待持久化统计信息 delta 持久化到 [`mysql.stats_meta`](/mysql-schema/mysql-schema.md#statistics-system-tables) 系统表中。

当你使用 DML 语句（例如 `INSERT`、`UPDATE` 和 `DELETE`）修改数据时，TiDB 会记录每个受影响表的总行数和已修改行数的变化，将这些变化（称为 statistics delta）缓存在执行这些语句的 TiDB 节点内存中，并每隔 20 * [`stats-lease`](/tidb-configuration-file.md#stats-lease)（默认 60 秒）将其持久化到 `mysql.stats_meta` 系统表中。更多信息，参见[自动修改](/statistics.md#automatic-update)。

由于[表的健康状态](/sql-statements/sql-statement-show-stats-healthy.md)、[`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md) 的输出以及自动统计信息收集的调度都依赖已持久化的统计信息元信息，因此当你需要让已持久化的统计信息元信息立即反映最近的数据变更时，`FLUSH STATS_DELTA` 会很有用，例如在验证优化器行为的测试场景中。你无需在 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) 之前执行此语句，因为 TiDB 会在收集某个表的统计信息之前，自动刷新该表待持久化的 statistics delta。

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

- **Targets (`FlushTargetList`)**：指定要刷新的统计信息 delta 所属表。你必须至少指定一个目标。
    - `table_name`：刷新当前数据库中某个表的统计信息 delta。如果你未选择数据库，TiDB 会返回 `No database selected` 错误。
    - `db_name.table_name`：刷新指定数据库中某个表的统计信息 delta。
    - `db_name.*`：刷新指定数据库中所有表的统计信息 delta。
    - `*.*`：刷新所有表的统计信息 delta。
- **`CLUSTER`**：将该语句广播到集群中的所有 TiDB 节点。每个 TiDB 节点都会缓存在其上执行的 DML 语句所产生的统计信息 delta。如果不指定此选项，TiDB 只会持久化你当前连接的 TiDB 节点上缓冲的 delta。

请注意以下行为：

- TiDB 会对重叠的目标进行去重。例如，在 `FLUSH STATS_DELTA *.*, test.t` 中，`test.t` 目标会被忽略，因为 `*.*` 已经包含所有表。类似地，在 `FLUSH STATS_DELTA test.*, test.t` 中，`test.t` 目标会被忽略，因为 `test.*` 已经包含 `test` 数据库中的所有表。
- 对于分区表，TiDB 会持久化该表及其所有分区的统计信息 delta。
- 如果指定的数据库或表不存在，TiDB 会返回一条警告并跳过该目标。

## 示例

在数据变更后立即持久化单个表的统计信息 delta：

```sql
USE test;
CREATE TABLE t (a INT, b INT);
INSERT INTO t VALUES (1, 1), (2, 2), (3, 3);
FLUSH STATS_DELTA t;
```

```
Query OK, 0 rows affected (0.01 sec)
```

此时，TiDB 已将该表的行数变化持久化到 `mysql.stats_meta` 系统表中。你可以使用 `SHOW STATS_META` 查看已持久化的值。注意，`SHOW STATS_META` 会从你当前连接的 TiDB 节点内存中读取统计信息。由于该 TiDB 节点会在 [`stats-lease`](/tidb-configuration-file.md#stats-lease)（默认 `3s`）内加载已持久化的值，因此刷新后的值可能会在短暂延迟后出现在输出中：

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

持久化当前数据库中某个表以及 `sales` 数据库中所有表的统计信息 delta：

```sql
FLUSH STATS_DELTA t, sales.*;
```

持久化集群中每个 TiDB 节点上缓冲的所有表的统计信息 delta：

```sql
FLUSH STATS_DELTA *.* CLUSTER;
```

## 权限

要执行 `FLUSH STATS_DELTA`，你必须对目标对象具有 `SELECT` 权限：对于 `table_name` 或 `db_name.table_name` 目标，需要具有目标表的 `SELECT` 权限；对于 `db_name.*` 目标，需要具有目标数据库的 `SELECT` 权限；对于 `*.*` 目标，需要具有全局 `SELECT` 权限。与其他 `FLUSH` 语句不同，`FLUSH STATS_DELTA` 不需要 `RELOAD` 权限。

## MySQL 兼容性

`FLUSH STATS_DELTA` 是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

- [Statistics](/statistics.md)
- [`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md)
- [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)
- [`REFRESH STATS`](/sql-statements/sql-statement-refresh-stats.md)