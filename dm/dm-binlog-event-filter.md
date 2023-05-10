---
title: TiDB Data Migration Binlog 事件过滤
summary: 了解 DM 的关键特性 binlog 事件过滤 (Binlog event filter) 的使用方法和注意事项。
---

## TiDB Data Migration Binlog 事件过滤

TiDB Data Migration (DM) 的 Binlog 事件过滤 (Binlog event filter) 是比迁移表[黑白名单](/dm/dm-block-allow-table-lists.md)更加细粒度的过滤规则，可以指定只迁移或者过滤掉某些 `schema / table` 的指定类型 binlog，比如 `INSERT`、`TRUNCATE TABLE`。

## 配置 Binlog 事件过滤

在迁移任务配置文件中，添加如下配置：

```yaml
filters:
  rule-1:
    schema-pattern: "test_*"
    ​table-pattern: "t_*"
    ​events: ["truncate table", "drop table"]
    sql-pattern: ["^DROP\\s+PROCEDURE", "^CREATE\\s+PROCEDURE"]
    ​action: Ignore
```

从 DM v2.0.2 开始，你也可以在上游数据库配置文件中配置 Binlog 事件过滤。见[上游数据库配置文件介绍](/dm/dm-source-configuration-file.md)。

在简单任务场景下，推荐使用通配符匹配库表名，但需注意以下版本差异：

+ 对于 v1.0.5 版及后续版本，Binlog 事件过滤支持[通配符匹配](https://en.wikipedia.org/wiki/Glob_(programming)#Syntax)。但注意所有版本中通配符匹配中的 `*` 符号 **只能有一个，且必须在末尾**。
+ 对于 v1.0.5 以前的版本，Binlog Event Filter 支持通配符，但不支持 `[...]` 与 `[!...]` 表达式。

## 参数解释

- [`schema-pattern`/`table-pattern`](/dm/table-selector.md)：对匹配上的上游 MySQL/MariaDB 实例的表的 binlog events 或者 DDL SQL 语句通过以下规则进行过滤。

- `events`：binlog events 数组，仅支持从以下 `Event` 中选择一项或多项。

    | Event           | 分类 | 解释                           |
    | --------------- | ---- | ----------------------------- |
    | all             |      | 代表包含下面所有的 events        |
    | all dml         |      | 代表包含下面所有 DML events     |
    | all ddl         |      | 代表包含下面所有 DDL events     |
    | none            |      | 代表不包含下面所有 events        |
    | none ddl        |      | 代表不包含下面所有 DDL events    |
    | none dml        |      | 代表不包含下面所有 DML events    |
    | insert          | DML  | insert DML event              |
    | update          | DML  | update DML event              |
    | delete          | DML  | delete DML event              |
    | create database | DDL  | create database event         |
    | drop database   | DDL  | drop database event           |
    | create table    | DDL  | create table event            |
    | create index    | DDL  | create index event            |
    | drop table      | DDL  | drop table event              |
    | truncate table  | DDL  | truncate table event          |
    | rename table    | DDL  | rename table event            |
    | drop index      | DDL  | drop index event              |
    | alter table     | DDL  | alter table event             |

- `sql-pattern`：用于过滤指定的 DDL SQL 语句，支持正则表达式匹配，例如上面示例中的 `"^DROP\\s+PROCEDURE"`。

- `action`：string (`Do` / `Ignore`)；进行下面规则判断，满足其中之一则过滤，否则不过滤。

    - `Do`：白名单。binlog event 如果满足下面两个条件之一就会被过滤掉：
        - 不在该 rule 的 `events` 中。
        - 如果规则的 `sql-pattern` 不为空的话，对应的 SQL 没有匹配上 `sql-pattern` 中任意一项。
    - `Ignore`：黑名单。如果满足下面两个条件之一就会被过滤掉：
        - 在该 rule 的 `events` 中。
        - 如果规则的 `sql-pattern` 不为空的话，对应的 SQL 可以匹配上 `sql-pattern` 中任意一项。
    - 同一个表匹配上多个规则时，将会顺序应用这些规则，并且黑名单的优先级高于白名单，即如果同时存在规则 `Ignore` 和 `Do` 应用在某个表上，那么 `Ignore` 生效。

## 使用示例

### 过滤分库分表的所有删除操作

需要设置下面两个 `Binlog event filter rule` 来过滤掉所有的删除操作：

- `filter-table-rule` 过滤掉所有匹配到 pattern `test_*`.`t_*` 的 table 的 `turncate table`、`drop table`、`delete statement` 操作。
- `filter-schema-rule` 过滤掉所有匹配到 pattern `test_*` 的 schema 的 `drop database` 操作。

```yaml
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

需要设置下面两个 `Binlog event filter rule` 只迁移 DML 操作：

- `do-table-rule` 只迁移所有匹配到 pattern `test_*`.`t_*` 的 table 的 `create table`、`insert`、`update`、`delete` 操作。
- `do-schema-rule` 只迁移所有匹配到 pattern `test_*` 的 schema 的 `create database` 操作。

> **注意：**
>
> 迁移 `create database/table` 的原因是创建库和表后才能迁移 `DML`。

```yaml
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

可设置如下规则过滤 TiDB 不支持的 `PROCEDURE` 语句：

```yaml
filters:
  filter-procedure-rule:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    sql-pattern: ["^DROP\\s+PROCEDURE", "^CREATE\\s+PROCEDURE"]
    action: Ignore
```

### 过滤 TiDB parser 不支持的 SQL 语句

对于 TiDB parser 不支持的 SQL 语句，DM 无法解析获得 `schema`/`table` 信息，因此需要使用全局过滤规则：`schema-pattern: "*"`。

> **注意：**
>
> 全局过滤规则的设置必须尽可能严格，以避免过滤掉需要迁移的数据。

可设置如下规则过滤某些版本的 TiDB parser 不支持的 `PARTITION` 语句：

```yaml
filters:
  filter-partition-rule:
    schema-pattern: "*"
    sql-pattern: ["ALTER\\s+TABLE[\\s\\S]*ADD\\s+PARTITION", "ALTER\\s+TABLE[\\s\\S]*DROP\\s+PARTITION"]
    action: Ignore
```
