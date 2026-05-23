---
title: REFRESH STATS
summary: 了解如何将指定表或整个 TiDB 集群的统计信息重新加载到内存中。
---

# REFRESH STATS

`REFRESH STATS` 用于将 TiDB 系统表中持久化的优化器统计信息重新加载到内存中。该语句主要适用于以下场景：统计信息已通过外部方式恢复（例如通过 [BR](/br/br-use-overview.md) 恢复），或者需要在不重新执行 `ANALYZE` 的情况下同步内存中的统计信息。

当你执行 `REFRESH STATS` 时，TiDB 会复用启动时自动触发的统计信息初始化流程。你可以重新加载单个表、指定数据库中的所有表，或者整个集群的统计信息，并可以选择执行轻量级（`LITE`）初始化或完整（`FULL`）初始化。

> **警告：**
>
> 该语句是为 BR 的内部恢复流程设计的，BR 会在需要时自动执行它。
>
> - 除非你正在排查内存中的统计信息问题，否则**请勿**手动执行该语句；同时，请不要在生产集群中将该语句作为常规操作执行。
> - **请勿**对同一张表并发执行该语句，否则可能导致非预期行为。

## 语法图

```ebnf+diagram
RefreshStatsStmt ::=
    'REFRESH' 'STATS' RefreshTargetList RefreshMode? ClusterOption?

RefreshTargetList ::=
    RefreshTarget (',' RefreshTarget)*

RefreshTarget ::=
    TableName
  | SchemaWildcard
  | GlobalWildcard

TableName ::=
    Identifier ('.' Identifier)?

SchemaWildcard ::=
    Identifier '.' '*'

GlobalWildcard ::=
    '*' '.' '*'

RefreshMode ::=
    'FULL'
  | 'LITE'

ClusterOption ::=
    'CLUSTER'
```

## 选项

- **刷新目标（`RefreshTargetList`）**：
    - `table_name`：刷新当前数据库中的指定表。
    - `db_name.table_name`：刷新指定数据库中的指定表。
    - `db_name.*`：刷新指定数据库中的所有表。
    - `*.*`：刷新集群中的所有表。
- **`FULL`**：将完整的统计信息（例如直方图、Top-N 和 Count-Min Sketch）加载到内存中，等同于针对本次操作将 [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-从-v710-版本开始引入) 设置为 `false`。当你需要立即获得完整统计信息时，可使用该选项。
- **`LITE`**：执行轻量级初始化，等同于设置 `lite-init-stats = true`。该模式会跳过直方图等较重数据结构的加载，直到真正需要时才加载。
- **`CLUSTER`**：将刷新请求发送到所有 TiDB 服务器。如果不指定该选项，则只有接收到该语句的 TiDB 节点会重新加载其内存中的统计信息。
- **默认模式**：如果既未指定 `FULL`，也未指定 `LITE`，TiDB 会使用 [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-从-v710-版本开始引入) 的当前值。

## 示例

- 刷新当前连接的 TiDB 节点上单个表的统计信息：

  ```sql
  REFRESH STATS orders;
  ```

- 以轻量级初始化方式刷新 `sales` 中的所有表：

  ```sql
  REFRESH STATS sales.* LITE;
  ```

- 强制所有 TiDB 节点加载整个集群的完整统计信息：

  ```sql
  REFRESH STATS *.* FULL CLUSTER;
  ```

## 权限

要执行 `REFRESH STATS`，你必须拥有 `RESTORE_ADMIN` 权限，或者拥有每个目标表上的 `SELECT` 权限。如果你的权限不足，TiDB 会返回错误并中止该语句的执行。

## MySQL 兼容性

`REFRESH STATS` 语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

- [统计信息](/statistics.md)
- [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)
- [`LOCK STATS`](/sql-statements/sql-statement-lock-stats.md)