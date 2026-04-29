---
title: REFRESH STATS
summary: 了解如何为特定表或整个 TiDB 集群将统计信息重新加载到内存中。
---

# REFRESH STATS

`REFRESH STATS` 将持久化的优化器统计信息从 TiDB 系统表重新加载到内存中。该语句主要用于统计信息已通过外部方式恢复的场景（例如，通过 [BR](/br/br-use-overview.md)），或者当你需要在不重新运行 `ANALYZE` 的情况下协调内存中的统计信息时。

当你运行 `REFRESH STATS` 时，TiDB 会复用在启动时自动触发的统计信息初始化例程。你可以为单个表、所选数据库中的所有表或整个集群重新加载统计信息，并可选择执行轻量级（`LITE`）或完整（`FULL`）初始化。

> **Warning:**
>
> 该语句是为 BR 的内部恢复工作流设计的，BR 会在需要时自动运行它。 
> 
> - 除非你正在调试内存中的统计信息，否则**不要**手动执行该语句，并且绝不要将其作为例行操作的一部分在生产集群上运行。
> - **不要**在相同的表上并发执行该语句，因为这可能导致不可预期的行为。

## Synopsis

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

## Options

- **Targets (`RefreshTargetList`)**：
    - `table_name` 刷新当前数据库中的一个表。
    - `db_name.table_name` 刷新一个带完整限定名的表。
    - `db_name.*` 刷新指定数据库中的所有表。
    - `*.*` 刷新集群中的所有表。
- **`FULL`**：将完整统计信息（例如直方图、TopN 和 CMSketch）加载到内存中，等同于在本次操作中将 [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710) 设置为 `false`。当你需要立即获得完整统计信息时，请使用此选项。
- **`LITE`**：执行轻量级初始化，等同于 `lite-init-stats = true`，这会跳过加载直方图和其他较重的结构体，直到实际需要时再加载。
- **`CLUSTER`**：将刷新请求广播到每个 TiDB server。不带此选项时，只有接收该语句的 TiDB 节点会重新加载其内存中的统计信息。
- **Default mode**：如果既未指定 `FULL` 也未指定 `LITE`，TiDB 将使用当前的 [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710) 值。

## Examples

- 在已连接的 TiDB 节点上刷新单个表的统计信息：

  ```sql
  REFRESH STATS orders;
  ```

- 以轻量级初始化方式刷新 `sales` 中的所有表：

  ```sql
  REFRESH STATS sales.* LITE;
  ```

- 强制每个 TiDB 节点为整个集群加载完整统计信息：

  ```sql
  REFRESH STATS *.* FULL CLUSTER;
  ```

## Privileges

要执行 `REFRESH STATS`，你必须拥有 `RESTORE_ADMIN` 权限，或者拥有每个目标表上的 `SELECT` 权限。如果你的权限不足，TiDB 会返回错误并退出该语句的执行。

## MySQL compatibility

`REFRESH STATS` 是 TiDB 特有的扩展，不属于 MySQL 的一部分。

## See also

- [Statistics](/statistics.md)
- [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)
- [`LOCK STATS`](/sql-statements/sql-statement-lock-stats.md)