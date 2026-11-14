---
title: 如何过滤 binlog 事件
summary: 介绍如何过滤 binlog 事件。
---

# 如何过滤 binlog 事件

本文档介绍使用 DM 持续增量数据同步时，如何过滤 binlog 事件。具体迁移操作可参考已有数据迁移场景：

- [从小数据量 MySQL 迁移数据到 TiDB](/migrate-small-mysql-to-tidb.md)
- [从大数据量 MySQL 迁移数据到 TiDB](/migrate-large-mysql-to-tidb.md)
- [从小数据量分库分表 MySQL 合并迁移数据到 TiDB](/migrate-small-mysql-shards-to-tidb.md)
- [从大数据量分库分表 MySQL 合并迁移数据到 TiDB](/migrate-large-mysql-shards-to-tidb.md)

## 配置方式

配置 DM 的任务配置文件时，增加如下 `filters`，具体配置示例如下：

```yaml
filters:
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    events: ["truncate table", "drop table"]
    action: Ignore
```

定义过滤规则后，还需要在对应的 `mysql-instances` 项下通过 `filter-rules` 引用该规则，否则 DM 不会将该规则应用到对应的数据源。

```yaml
mysql-instances:
  - source-id: "mysql-replica-01"
    filter-rules: ["rule-1"]
```

更多信息，请参阅[DM 任务配置指南](/dm/dm-task-configuration-guide.md#配置需要迁移的-binlog-events)。

- `schema-pattern`/`table-pattern`：对匹配上的 schema 或 table 进行过滤。
- `events`：binlog event。支持的 Event 如下表所示：

  | Event | 分类 | 说明 |
  | --- | --- | --- |
  | `all` |  | 匹配所有 event。 |
  | `all dml` |  | 匹配所有 DML event。 |
  | `all ddl` |  | 匹配所有 DDL event。 |
  | `incompatible ddl changes` |  | 匹配所有可能导致数据丢失的不兼容 DDL event。 |
  | `none` |  | 不匹配任何 event。 |
  | `none ddl` |  | 不包含任何 DDL event。 |
  | `none dml` |  | 不包含任何 DML event。 |
  | `insert` | DML | 匹配 `INSERT` DML event。 |
  | `update` | DML | 匹配 `UPDATE` DML event。 |
  | `delete` | DML | 匹配 `DELETE` DML event。 |
  | `create database` | DDL | 匹配 `CREATE DATABASE` DDL event。 |
  | `drop database` | 不兼容 DDL | 匹配 `DROP DATABASE` DDL event。 |
  | `create table` | DDL | 匹配 `CREATE TABLE` DDL event。 |
  | `create index` | DDL | 匹配 `CREATE INDEX` DDL event。 |
  | `drop table` | 不兼容 DDL | 匹配 `DROP TABLE` DDL event。 |
  | `truncate table` | 不兼容 DDL | 匹配 `TRUNCATE TABLE` DDL event。 |
  | `rename table` | 不兼容 DDL | 匹配 `RENAME TABLE` DDL event。 |
  | `drop index` | 不兼容 DDL | 匹配 `DROP INDEX` DDL event。 |
  | `alter table` | DDL | 匹配 `ALTER TABLE` DDL event。 |
  | `value range decrease` | 不兼容 DDL | 匹配缩小列值范围的 DDL。 |
  | `precision decrease` | 不兼容 DDL | 匹配降低列精度的 DDL。 |
  | `modify column` | 不兼容 DDL | 匹配修改列类型的 DDL。 |
  | `rename column` | 不兼容 DDL | 匹配修改列名的 DDL。 |
  | `rename index` | 不兼容 DDL | 匹配修改索引名的 DDL。 |
  | `drop column` | 不兼容 DDL | 匹配删除列的 DDL。 |
  | `truncate table partition` | 不兼容 DDL | 匹配清空指定分区数据的 DDL。 |
  | `drop primary key` | 不兼容 DDL | 匹配删除主键的 DDL。 |
  | `drop unique key` | 不兼容 DDL | 匹配删除唯一键的 DDL。 |
  | `modify default value` | 不兼容 DDL | 匹配修改列默认值的 DDL。 |
  | `modify constraint` | 不兼容 DDL | 匹配修改约束的 DDL。 |
  | `modify columns order` | 不兼容 DDL | 匹配修改列顺序的 DDL。 |
  | `modify charset` | 不兼容 DDL | 匹配修改列字符集的 DDL。 |
  | `modify collation` | 不兼容 DDL | 匹配修改列排序规则的 DDL。 |
  | `remove auto increment` | 不兼容 DDL | 匹配移除自增属性的 DDL。 |
  | `modify storage engine` | 不兼容 DDL | 匹配修改表存储引擎的 DDL。 |
  | `reorganize table partition` | 不兼容 DDL | 匹配重组表分区的 DDL。 |
  | `rebuild table partition` | 不兼容 DDL | 匹配重建表分区的 DDL。 |
  | `exchange table partition` | 不兼容 DDL | 匹配在两张表之间交换分区的 DDL。 |
  | `coalesce table partition` | 不兼容 DDL | 匹配减少表分区数量的 DDL。 |

- `sql-pattern`：匹配指定的 DDL SQL 语句，支持正则表达式匹配。
- `action`：可取值 `Do`、`Ignore` 或 `Error`。

    - `Do`：白名单。

        - 如果只配置 `events`，DM 只会同步事件类型匹配 `events` 的 binlog event。
        - 如果只配置 `sql-pattern`，DM 只会同步 SQL 文本匹配 `sql-pattern` 的 DDL 语句。
        - 如果同时为某个 DDL 语句配置 `events` 和 `sql-pattern`，只有当事件类型和 SQL 文本都匹配规则时，DM 才会同步该语句。

    - `Ignore`：黑名单。只要满足以下任一条件，DM 就会过滤掉该 binlog event：

        - 事件类型匹配 `events`。
        - 配置了 `sql-pattern`，且 SQL 语句匹配 `sql-pattern` 中的任意一项。

    - `Error`：报错列表。只要满足以下任一条件，DM 就会报错：

        - 事件类型匹配 `events`。
        - 配置了 `sql-pattern`，且 SQL 语句匹配 `sql-pattern` 中的任意一项。

    当同一张表同时命中多条规则时，`Ignore` 的优先级高于 `Error`，`Error` 的优先级高于 `Do`。

## 使用场景举例

### 过滤分库分表的所有删除操作

设置 `filter-table-rule` 和 `filter-schema-rule` 两个过滤规则，具体如下：

```
filters:
  filter-table-rule:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    events: ["truncate table", "drop table", "delete"]
    action: Ignore
  filter-schema-rule:
    schema-pattern: "test_*"
    events: ["drop database"]
    action: Ignore
```

### 只迁移分库分表的 DML 操作

设置两个 `Binlog event filter rule`：

```
filters:
  do-table-rule:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    events: ["create table", "all dml"]
    action: Do
  do-schema-rule:
    schema-pattern: "test_*"
    events: ["create database"]
    action: Do
```

### 处理 TiDB 不支持或 DM 无法解析的 SQL 语句

对于 `CREATE PROCEDURE`、`DROP PROCEDURE` 和 `ALTER PROCEDURE`，无需配置过滤规则。DM 会自动跳过这些语句。

在 MySQL 中添加或删除分区时，DM 通常会将变更同步到 TiDB。对于 DM 和 TiDB 都支持的分区操作，无需配置过滤规则。要查看 TiDB 支持分区类型的操作，请参阅[分区管理](/partitioned-table.md#分区管理)。

如果 DM 在处理使用 `ADD PARTITION` 或 `DROP PARTITION` 的 `ALTER TABLE` 语句时报解析错误，并且你不需要将该分区变更同步到 TiDB，则可以使用如下规则跳过该语句。DM 的解析错误并不一定意味着 TiDB 不支持该操作。

当 DM 无法解析某条语句时，它无法应用仅针对特定 schema 或 table 的过滤规则。此时，你需要使用 `schema-pattern: "*"` 且不设置 `table-pattern` 的全局过滤规则。该规则会对迁移任务中所有表的匹配语句生效。

> **警告：**
>
> 为避免过滤掉需要迁移的数据，请尽可能严格地配置该全局过滤规则。
>
> 以下正则表达式匹配 SQL 文本，包括字符串字面量，因此可能误过滤其他 DDL 语句。例如，如果 `ALTER TABLE ... ADD COLUMN` 语句的默认值中包含 `ADD PARTITION`，该语句也可能被跳过。使用此规则前，请确认这些正则表达式不会匹配任何需要同步的 DDL 语句。

```
filters:
  filter-partition-rule:
    schema-pattern: "*"
    sql-pattern: ["ALTER\\s+TABLE[\\s\\S]*ADD\\s+PARTITION", "ALTER\\s+TABLE[\\s\\S]*DROP\\s+PARTITION"]
    action: Ignore
```

## 探索更多

- [如何通过 SQL 表达式过滤 binlog](/filter-dml-event.md)