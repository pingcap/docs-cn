---
title: Changefeed 日志过滤器
summary: 了解 TiCDC 的表过滤器和事件过滤器使用方法。
---

# Changefeed 日志过滤器

TiCDC 支持基于表和事件两个维度的过滤功能，本文分别介绍两种过滤器的使用方法。

## Table Filter 表过滤器

TiCDC 支持基于库表名的过滤功能，你可以通过下列配置来选定或过滤掉指定的表：

```toml
[filter]
# 过滤器规则
rules = ['*.*', '!test.*']
```

常见的过滤器规则示例：

- `rules = ['*.*']`
    - 同步所有的表（不包含系统表）
- `rules = ['test1.*']`
    - 同步库 `test1` 下的所有表
- `rules = ['*.*', '!scm1.tbl2']`
    - 同步所有的表但排除表 `scm1.tbl2`
- `rules = ['scm1.tbl2', 'scm1.tbl3']`
    - 只同步表 `scm1.tbl2` 和 `scm1.tbl3`
- `rules = ['scm1.tidb_*']`
    - 同步库 `scm1` 下所有表名前缀为 `tidb_` 的表

更多用法说明参见：[库表过滤语法](/table-filter.md#表库过滤语法)

## Event Filter 事件过滤器 <span class="version-mark">从 v6.2.0 版本开始引入</span>

TiCDC 在 v6.2.0 中新增了事件过滤器功能，你可以通过配置该规则来过滤符合指定条件的 DML 和 DDL 事件。

以下是事件过滤器的配置规则示例：

```toml
[filter]
# 事件过滤器的规则应该写在 filter 配置项之下，可以同时配置多个事件过滤器。

[[filter.event-filters]]
matcher = ["test.worker"] # 该过滤规则只应用于 test 库中的 worker 表
ignore-event = ["insert"] # 过滤掉 insert 事件
ignore-sql = ["^drop", "add column"] # 过滤掉以 "drop" 开头或者包含 "add column" 的 DDL
ignore-delete-value-expr = "name = 'john'" # 过滤掉包含 name = 'john' 条件的 delete DML
ignore-insert-value-expr = "id >= 100" # 过滤掉包含 id >= 100 条件的 insert DML
ignore-update-old-value-expr = "age < 18 or name = 'lili'" # 过滤掉旧值 age < 18 或 name = 'lili' 的 update DML
ignore-update-new-value-expr = "gender = 'male' and age > 18" # 过滤掉新值 gender = 'male' 且 age > 18 的 update DML
```

配置参数说明：

- `matcher`：该事件过滤器所要匹配的数据库名和表名，其匹配规则和[表库过滤规则](/table-filter.md#表库过滤语法)相一致。
- `ignore-event`：要过滤掉的事件类型，它是一个字符串数组，可以配置多个事件类型。目前支持的类型如下表所示:

    | Event           | 分类 | 别名 |说明                    |
    | --------------- | ---- | -|--------------------------|
    | all dml         |      | |匹配所有 DML events         |
    | all ddl         |      | |匹配所有 DDL events         |
    | insert          | DML  | |匹配 insert DML event      |
    | update          | DML  | |匹配 update DML event      |
    | delete          | DML  | |匹配 delete DML event      |
    | create schema   | DDL  | create database |匹配 create database event |
    | drop schema     | DDL  | drop database  |匹配 drop database event |
    | create table    | DDL  | |匹配 create table event    |
    | drop table      | DDL  | |匹配 drop table event      |
    | rename table    | DDL  | |匹配 rename table event    |
    | truncate table  | DDL  | |匹配 truncate table event  |
    | alter table     | DDL  | |匹配 alter table event（包含 alter table 的所有子句和 create/drop index）     |
    | add table partition    | DDL  | |匹配 add table partition event     |
    | drop table partition    | DDL  | |匹配 drop table partition event     |
    | truncate table partition    | DDL  | |匹配 truncate table partition event     |
    | create view     | DDL  | |匹配 create view event     |
    | drop view     | DDL  | |匹配 drop view event     |
    | modify schema charset and collate | DDL  | |匹配 modify schema charset and collate event     |
    | recover table   | DDL  | |匹配 recover table event    |
    | rebase auto id    | DDL  | |匹配 rebase auto id event    |
    | modify table comment | DDL  | |匹配 modify table comment event    |
    | modify table charset and collate | DDL  | |匹配 modify table charset and collate event    |
    | exchange table partition | DDL  | |匹配 exchange table partition event    |
    | reorganize table partition | DDL  | |匹配 reorganize table partition event    |
    | alter table partitioning | DDL  | |匹配 alter table partitioning event    |
    | remove table partitioning | DDL  | |匹配 remove table partitioning event    |
    | add column | DDL  | |匹配 add column event    |
    | drop column | DDL  | |匹配 drop column event    |
    | modify column | DDL  | |匹配 modify column event    |
    | set default value | DDL  | |匹配 set default value event    |
    | add primary key | DDL  | |匹配 add primary key event    |
    | drop primary key | DDL  | |匹配 drop primary key event    |
    | rename index | DDL  | |匹配 rename index event    |
    | alter index visibility | DDL  | |匹配 alter index visibility event    |
    | alter ttl info | DDL  | |匹配 alter ttl info event    |
    | alter ttl remove| DDL  | |匹配清除一张表的所有 TTL 属性的 DDL event    |
    | multi schema change | DDL  | |匹配在同一条 DDL 语句内对一个表的多个属性进行更改的 DDL event  |

    > **注意：**
    >
    > TiDB 的 DDL 语句支持同时变更单个表的多个属性，例如 `ALTER TABLE t MODIFY COLUMN a INT, ADD COLUMN b INT, DROP COLUMN c;` 这种操作会被定义为 MultiSchemaChange。如果想过滤掉这种类型的 DDL，需要在 `ignore-event` 中配置 `"multi schema change"`。

- `ignore-sql`：要过滤掉的 DDL 语句的正则表达式。该参数接受一个字符串数组，数组中可以配置多条正则表达式。注意：该配置仅对 DDL 事件生效。
- `ignore-delete-value-expr`：配置一个遵循默认 SQL Mode 的 SQL 表达式，用于过滤掉带有指定值的 DELETE 类型的 DML 事件。
- `ignore-insert-value-expr`：配置一个遵循默认 SQL Mode 的 SQL 表达式，用于过滤掉带有指定值的 INSERT 类型的 DML 事件。
- `ignore-update-old-value-expr`：配置一个遵循默认 SQL Mode 的 SQL 表达式，用于过滤掉带有指定旧值的 UPDATE 类型的 DML 事件。
- `ignore-update-new-value-expr`：配置一个遵循默认 SQL Mode 的 SQL 表达式，用于过滤掉带有指定新值的 UPDATE 类型的 DML 事件。

> **注意：**
>
> - TiDB 在更新聚簇索引的列值时，会将一个 UPDATE 事件拆分成为 DELETE 和 INSERT 事件，TiCDC 无法将该类事件识别为 UPDATE 事件，因此无法正确地进行过滤。
>
> - 在配置 SQL 表达式时，请确保符合 matcher 规则的所有表均包含了对应 SQL 表达式中指明的所有列，否则同步任务将无法创建成功。此外，若在同步的过程中表的结构发生变化，不再包含 SQL 表达式中的列，那么同步任务将会进入无法自动恢复的错误状态，你需要手动修改配置并进行恢复操作。
