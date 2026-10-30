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

配置 DM 的任务配置文件时，增加如下`filter`，具体配置示例如下图：

```yaml
filters:
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    events: ["truncate table", "drop table"]
    action: Ignore
```

- `schema-pattern`/`table-pattern`：对匹配上的 schema 或 table 进行过滤
- `events`：binlog events，支持的 Event 如下表所示:

| Event           | 分类 | 说明                       |
| --------------- | ---- | --------------------------|
| all             |      | 匹配所有 events            |
| all dml         |      | 匹配所有 DML events        |
| all ddl         |      | 匹配所有 DDL events        |
| none            |      | 不匹配任何 events          |
| none ddl        |      | 不包含任何 DDL events      |
| none dml        |      | 不包含任何 DML events      |
| insert          | DML  | 匹配 insert DML event      |
| update          | DML  | 匹配 update DML event      |
| delete          | DML  | 匹配 delete DML event      |
| create database | DDL  | 匹配 create database event |
| drop database   | DDL  | 匹配 drop database event   |
| create table    | DDL  | 匹配 create table event    |
| create index    | DDL  | 匹配 create index event    |
| drop table      | DDL  | 匹配 drop table event      |
| truncate table  | DDL  | 匹配 truncate table event  |
| rename table    | DDL  | 匹配 rename table event    |
| drop index      | DDL  | 匹配 drop index event      |
| alter table     | DDL  | 匹配 alter table event     |

- `sql-pattern`：匹配指定的 DDL SQL 语句，支持正则表达式匹配。
- `action`：可取值 Do 或 Ignore。
    - `Do`：白名单。binlog event 如果满足下面两个条件之一将会被同步：
        - 符合 events 条件；
        - sql-pattern 不为空，且对应的 SQL 可以匹配上 sql-pattern 中任意一项。
    - `Ignore`：黑名单。如果满足下面两个条件之一就会被过滤掉：
        - 符合 events 条件；
        - sql-pattern 不为空，且对应的 SQL 可以匹配上 sql-pattern 中任意一项

注意：如果同时配置 `Do/Ignore`，则 `Ignore` 优先级更高。`binlog event` 不匹配白名单或者匹配黑名单都将被直接过滤。

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