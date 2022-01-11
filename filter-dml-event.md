---
title: 如何通过 SQL 表达式过滤 DML
summary: 介绍如何通过 SQL 表达式过滤 DML 事件
---

# 如何通过 SQL 表达式过滤 DML

本文档介绍使用 DM 持续增量数据同步时，如何更加精细的过滤 binlog 事件。具体迁移操作可参考已有数据迁移场景：

- [从小数据量 MySQL 迁移数据到 TiDB](/migrate-small-mysql-to-tidb.md)
- [从大数据量 MySQL 迁移数据到 TiDB](/migrate-large-mysql-to-tidb.md)
- [从小数据量分库分表 MySQL 合并迁移数据到 TiDB](/migrate-small-mysql-shards-to-tidb.md)
- [从大数据量分库分表 MySQL 合并迁移数据到 TiDB](/migrate-large-mysql-shards-to-tidb.md)

在进行增量数据迁移时，可以通过[如何过滤 binlog 事件](/filter-binlog-event.md)功能过滤某些类型的 binlog event，例如不向下游迁移 `DELETE` 事件以达到归档、审计等目的。但是 binlog event filter 无法以更细粒度判断某一行的 `DELETE` 事件是否要被过滤。

为了解决上述问题，从 v2.0.5 起，DM 支持在增量数据同步阶段使用`binlog value filter`过滤迁移数据。DM 支持的 `ROW` 格式的 binlog 中，binlog event 带有所有列的值。你可以基于这些值配置 SQL 表达式。如果该表达式对于某条行变更的计算结果是 `TRUE`，DM 就不会向下游迁移该条行变更。

与[如何过滤 binlog 事件](/filter-binlog-event.md)类似，表达式过滤需要在数据迁移任务配置文件里配置，详见下面配置样例。完整的配置及意义，可以参考 [DM 完整配置文件示例](/dm/task-configuration-file-full.md#完整配置文件示例)：

```yaml
name: test
task-mode: all

mysql-instances:
  - source-id: "mysql-replica-01"
    expression-filters: ["even_c"]

expression-filter:
  even_c:
    schema: "expr_filter"
    table: "tbl"
    insert-value-expr: "c % 2 = 0"
```

上面的示例配置了 `even_c` 规则，并让 source ID 为 `mysql-replica-01` 的数据源引用了该规则。`even_c` 规则的含义是：对于 `expr_filter` 库下的 `tbl` 表，当插入的 `c` 的值为偶数 (`c % 2 = 0`) 时，不将这条插入语句迁移到下游。下面展示该规则的使用效果。

在上游数据源增量插入以下数据：

```sql
INSERT INTO tbl(id, c) VALUES (1, 1), (2, 2), (3, 3), (4, 4);
```

随后在下游查询 `tbl` 表，可见只有 `c` 的值为单数的行迁移到了下游：

```
MySQL [test]> select * from tbl;

+------+------+
| id   | c    |
+------+------+
|    1 |    1 |
|    3 |    3 |
+------+------+

2 rows in set (0.001 sec)
```

## 配置参数及规则说明

- `schema`：要匹配的上游数据库库名，不支持通配符匹配或正则匹配。
- `table`: 要匹配的上游表名，不支持通配符匹配或正则匹配。
- `insert-value-expr`：配置一个表达式，对 INSERT 类型的 binlog event (WRITE_ROWS_EVENT) 带有的值生效。不能与 `update-old-value-expr`、`update-new-value-expr`、`delete-value-expr` 出现在一个配置项中。
- `update-old-value-expr`：配置一个表达式，对 UPDATE 类型的 binlog event (UPDATE_ROWS_EVENT) 更新对应的旧值生效。不能与 `insert-value-expr`、`delete-value-expr` 出现在一个配置项中。
- `update-new-value-expr`：配置一个表达式，对 UPDATE 类型的 binlog event (UPDATE_ROWS_EVENT) 更新对应的新值生效。不能与 `insert-value-expr`、`delete-value-expr` 出现在一个配置项中。
- `delete-value-expr`：配置一个表达式，对 DELETE 类型的 binlog event (DELETE_ROWS_EVENT) 带有的值生效。不能与 `insert-value-expr`、`update-old-value-expr`、`update-new-value-expr` 出现在一个配置项中。

> **注意：**
>
> - `update-old-value-expr` 可以与 `update-new-value-expr` 同时配置。
> - 当二者同时配置时，会将“更新+旧值“满足`update-old-value-expr` **且**”更新+新值“满足 `update-new-value-expr` 的行过滤掉。
> - 当只配置一者时，配置的这条表达式会决定是否过滤**整个行变更**，即旧值的删除和新值的插入会作为一个整体被过滤掉。

SQL 表达式可以涉及一列或多列，也可使用 TiDB 支持的 SQL 函数，例如 `c % 2 = 0`、`a*a + b*b = c*c`、`ts > NOW()`。

TIMESTAMP 类型的默认时区是任务配置文件中指定的时区，默认值是下游时区。可以使用 `c_timestamp = '2021-01-01 12:34:56.5678+08:00'` 的方式显式指定时区。

配置项 `expression-filter` 下可以定义多条过滤规则，上游数据源在其 `expression-filters` 配置项中引用需要的规则使其生效。当有多条规则生效时，匹配到**任意一条**规则即会导致某个行变更被过滤。

> **注意：**
>
> 为某张表设置过多的表达式过滤会增加 DM 的计算开销，可能导致数据迁移速度变慢。