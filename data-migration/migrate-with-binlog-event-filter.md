---
title: 如何过滤 binlog 事件
summary: 介绍如何过滤 binlog 事件。
---

# 如何过滤 binlog 事件

本文档介绍使用 DM 持续增量数据同步时，如何过滤 binlog 事件。具体迁移操作可参考已有数据迁移场景：

- [从 TB 级以下 MySQL 迁移数据到 TiDB](/data-migration/migrate-mysql-tidb-less-tb.md)
- [从 TB 级以上 MySQL 迁移数据到 TiDB](/data-migration/migrate-mysql-tidb-above-tb.md)
- [TB 级以下分库分表 MySQL 合并迁移数据到 TiDB](/data-migration/migrate-shared-mysql-tidb-less-tb.md)
- [TB 级以上分库分表 MySQL 合并迁移数据到 TiDB](/data-migration/migrate-shared-mysql-tidb-above-tb.md)

## 配置方式

配置 DM 的任务配置文件时，增加如下`filter`，具体配置示例如下图：

```yaml
filters:
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    events: ["truncate table", "drop table"]
    sql-pattern: ["^DROP\\s+PROCEDURE", "^CREATE\\s+PROCEDURE"]
    action: Ignore
```

- `schema-pattern`/`table-pattern`：对匹配上的 schema 或 table 进行过滤
- `events`：binlog events，支持的 Event 如下表所示:

| Event           | 分类 | 说明                       |
| --------------- | ---- | --------------------------|
| all             |      | 过滤所有 events            |
| all dml         |      | 过滤所有 DML events        |
| all ddl         |      | 过滤所有 DDL events        |
| none            |      | 不过滤任何 events          |
| none ddl        |      | 不包含任何 DDL events      |
| none dml        |      | 不包含任何 DML events      |
| insert          | DML  | 过滤 insert DML event      |
| update          | DML  | 过滤 update DML event      |
| delete          | DML  | 过滤 delete DML event      |
| create database | DDL  | 过滤 create database event |
| drop database   | DDL  | 过滤 drop database event   |
| create table    | DDL  | 过滤 create table event    |
| create index    | DDL  | 过滤 create index event    |
| drop table      | DDL  | 过滤 drop table event      |
| truncate table  | DDL  | 过滤 truncate table event  |
| rename table    | DDL  | 过滤 rename table event    |
| drop index      | DDL  | 过滤 drop index event      |
| alter table     | DDL  | 过滤 alter table event     |

- `sql-pattern`：过滤指定的 DDL SQL 语句，支持正则表达式匹配。
- `action`：可取值 Do 或 Ignore。
    - `Do`：白名单。binlog event 如果满足下面两个条件之一就会被过滤掉：
        - 不在该 rule 的 events 中。
        - sql-pattern 不为空，且对应的 SQL 没有匹配上 sql-pattern 中任意一项。
    - `Ignore`：黑名单。如果满足下面两个条件之一就会被过滤掉：
        - 在该 rule 的 events 中。
        - sql-pattern 不为空，且对应的 SQL 可以匹配上 sql-pattern 中任意一项

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

### 过滤 TiDB 不支持的 SQL 语句

```
filters:
  filter-procedure-rule:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    sql-pattern: ["^DROP\\s+PROCEDURE", "^CREATE\\s+PROCEDURE"]
    action: Ignore
```

### 过滤 TiDB parser 不支持的 SQL 语句

使用全局过滤规则 `schema-pattern: "*"`来过滤 TiDB parser 不支持的 SQL 语句：

```
filters:
  filter-partition-rule:
    schema-pattern: "*"
    sql-pattern: ["ALTER\\s+TABLE[\\s\\S]*ADD\\s+PARTITION", "ALTER\\s+TABLE[\\s\\S]*DROP\\s+PARTITION"]
    action: Ignore
```

> **注意：**
>
> 全局过滤规则的设置必须尽可能严格，以避免过滤掉需要迁移的数据。

## 探索更多

- [如何通过 SQL 表达式过滤 binlog](/data-migration/migrate-with-binlog-sql-expression-filter.md)