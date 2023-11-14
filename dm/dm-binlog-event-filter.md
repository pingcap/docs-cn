---
title: TiDB Data Migration Binlog Event Filter
summary: Learn how to use the binlog event filter feature of DM.
---

# TiDB Data Migration Binlog Event Filter

TiDB Data Migration (DM) provides the binlog event filter feature to filter out, block and report errors, or only receive specified types of binlog events for some schemas or tables. For example, you can filter out all `TRUNCATE TABLE` or `INSERT` events. The binlog event filter feature is more fine-grained than the [block and allow lists](/dm/dm-block-allow-table-lists.md) feature.

## Configure the binlog event filter

In the task configuration file, add the following configuration:

```yaml
filters:
  rule-1:
    schema-pattern: "test_*"
    ​table-pattern: "t_*"
    ​events: ["truncate table", "drop table"]
    sql-pattern: ["^DROP\\s+PROCEDURE", "^CREATE\\s+PROCEDURE"]
    ​action: Ignore
```

Starting from DM v2.0.2, you can configure the binlog event filter in the source configuration file. For details, see [Upstream Database Configuration File](/dm/dm-source-configuration-file.md).

When you use the wildcard for matching schemas and tables, note the following:

- `schema-pattern` and `table-pattern` only support wildcards, including `*`, `?`, and `[]`. There can only be one `*` symbol in a wildcard match, and it must be at the end. For example, in `table-pattern: "t_*"`, `"t_*"` indicates all tables starting with `t_`. See [wildcard matching](https://en.wikipedia.org/wiki/Glob_(programming)#Syntax) for details.

- `sql-pattern` only supports regular expressions.

## Parameter descriptions

- [`schema-pattern`/`table-pattern`](/dm/table-selector.md): the binlog events or DDL SQL statements of upstream MySQL or MariaDB instance tables that match `schema-pattern`/`table-pattern` are filtered by the rules below.

- `events`: the binlog event array. You can only select one or more `Event`s from the following table:

    | Events            | Type | Description                   |
    | ---------------   | ---- | ----------------------------- |
    | `all`             |      | Includes all the events below |
    | `all dml`         |      | Includes all DML events below |
    | `all ddl`         |      | Includes all DDL events below |
    | `incompatible ddl changes` |      | Includes all incompatible DDL events, where "incompatible DDL" means DDL operations that might cause data loss   |
    | `none`            |      | Includes none of the events below |
    | `none ddl`        |      | Includes none of the DDL events below |
    | `none dml`        |      | Includes none of the DML events below |
    | `insert`          | DML  | The `INSERT` DML event              |
    | `update`          | DML  | The `UPDATE` DML event              |
    | `delete`          | DML  | The `DELETE` DML event              |
    | `create database` | DDL  | The `CREATE DATABASE` DDL event         |
    | `drop database`   | incompatible DDL  | The `DROP DATABASE` DDL event           |
    | `create table`    | DDL  | The `CREATE TABLE` DDL event      |
    | `create index`    | DDL  | The `CREATE INDEX` DDL event          |
    | `drop table`      | incompatible DDL  | The `DROP TABLE` DDL event              |
    | `truncate table`  | incompatible DDL  | The `TRUNCATE TABLE` DDL event          |
    | `rename table`    | incompatible DDL  | The `RENAME TABLE` DDL event            |
    | `drop index`      | incompatible DDL  | The `DROP INDEX` DDL event           |
    | `alter table`     | DDL  | The `ALTER TABLE` DDL event           |
    | `value range decrease` | incompatible DDL  | A DDL statement that decreases the value range of a column field, such as the `ALTER TABLE MODIFY COLUMN` statement that changes `VARCHAR(20)` to `VARCHAR(10)`  |
    | `precision decrease` | incompatible DDL  | A DDL statement that decreases the precision of a column field, such as the `ALTER TABLE MODIFY COLUMN` statement that changes `Decimal(10, 2)` to `Decimal(10, 1)`  |
    | `modify column` | incompatible DDL  | A DDL statement that changes the type of a column field, such as the `ALTER TABLE MODIFY COLUMN` statement that changes `INT` to `VARCHAR` |
    | `rename column` | incompatible DDL  | A DDL statement that changes the name of a column, such as the `ALTER TABLE RENAME COLUMN` statement |
    | `rename index` | incompatible DDL  | A DDL statement that changes the index name, such as the `ALTER TABLE RENAME INDEX` statement |
    | `drop column` | incompatible DDL  | A DDL statement that drops a column from a table, such as the `ALTER TABLE DROP COLUMN` statement |
    | `drop index` | incompatible DDL  | A DDL statement that drops an index in a table, such as the `ALTER TABLE DROP INDEX` statement |
    | `truncate table partition` | incompatible DDL  | A DDL statement that removes all data from a specified partition, such as the `ALTER TABLE TRUNCATE PARTITION` statement |
    | `drop primary key` | incompatible DDL  | A DDL statement that drops the primary key, such as the `ALTER TABLE DROP PRIMARY KEY` statement |
    | `drop unique key` | incompatible DDL  | A DDL statement that drops a unique key, such as the `ALTER TABLE DROP UNIQUE KEY` statement |
    | `modify default value` | incompatible DDL  | A DDL statement that modifies a column's default value, such as the `ALTER TABLE CHANGE DEFAULT` statement |
    | `modify constraint` | incompatible DDL  | A DDL statement that modifies the constraint, such as the `ALTER TABLE ADD CONSTRAINT` statement |
    | `modify columns order` | incompatible DDL  | A DDL statement that modifies the order of the columns, such as the `ALTER TABLE CHANGE AFTER` statement |
    | `modify charset` | incompatible DDL  | A DDL statement that modifies the charset of a column, such as the `ALTER TABLE MODIFY CHARSET` statement |
    | `modify collation` | incompatible DDL  | A DDL statement that modifies a column collation, such as the `ALTER TABLE MODIFY COLLATE` statement |
    | `remove auto increment` | incompatible DDL  | A DDL statement that removes an auto-incremental key |
    | `modify storage engine` | incompatible DDL  | A DDL statement that modifies the table storage engine, such as the `ALTER TABLE ENGINE = MyISAM` statement |
    | `reorganize table partition` | incompatible DDL  | A DDL statement that reorganizes partitions in a table, such as the `ALTER TABLE REORGANIZE PARTITION` statement |
    | `rebuild table partition` | incompatible DDL  | A DDL statement that rebuilds the table partition, such as the `ALTER TABLE REBUILD PARTITION` statement |
    | `exchange table partition` | incompatible DDL  | A DDL statement that exchanges a partition between two tables, such as the `ALTER TABLE EXCHANGE PARTITION` statement |
    | `coalesce table partition` | incompatible DDL  | A DDL statement that decreases the number of partitions in a table, such as the `ALTER COALESCE PARTITION` statement |

- `sql-pattern`: it is used to filter specified DDL SQL statements. The matching rule supports using a regular expression. For example, `"^DROP\\s+PROCEDURE"`.

- `action`: the string (`Do`/`Ignore`/`Error`). Based on the rules, it judges as follows:

    - `Do`: the allow list. The binlog is filtered in either of the following two conditions:
        - The type of the event is not in the `event` list of the rule.
        - The SQL statement of the event cannot be matched by `sql-pattern` of the rule.
    - `Ignore`: the block list. The binlog is filtered in either of the following two conditions:
        - The type of the event is in the `event` list of the rule.
        - The SQL statement of the event can be matched by `sql-pattern` of the rule.
    - `Error`: the error list. The binlog reports an error in either of the following two conditions:
        - The type of the event is in the `event` list of the rule.
        - The SQL statement of the event can be matched by `sql-pattern` of the rule.
    - When multiple rules match the same table, the rules are applied sequentially. The block list has a higher priority than the error list, and the error list has a higher priority than the allow list. For example:
        - If both the `Ignore` and `Error` rules are applied to the same table, the `Ignore` rule takes effect.
        - If both the `Error` and `Do` rules are applied to the same table, the `Error` rule takes effect.

## Usage examples

This section shows the usage examples in the scenario of sharding (sharded schemas and tables).

### Filter all sharding deletion operations

To filter out all deletion operations, configure the following two filtering rules:

- `filter-table-rule` filters out the `TRUNCATE TABLE`, `DROP TABLE` and `DELETE STATEMENT` operations of all tables that match the `test_*`.`t_*` pattern.
- `filter-schema-rule` filters out the `DROP DATABASE` operation of all schemas that match the `test_*` pattern.

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

### Only migrate sharding DML statements

To only migrate sharding DML statements, configure the following two filtering rules:

- `do-table-rule` only migrates the `CREATE TABLE`, `INSERT`, `UPDATE` and `DELETE` statements of all tables that match the `test_*`.`t_*` pattern.
- `do-schema-rule` only migrates the `CREATE DATABASE` statement of all schemas that match the `test_*` pattern.

> **Note:**
>
> The reason why the `CREATE DATABASE/TABLE` statement is migrated is that you can migrate DML statements only after the schema and table are created.

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

### Filter out the SQL statements that TiDB does not support

To filter out the `PROCEDURE` statements that TiDB does not support, configure the following `filter-procedure-rule`:

```yaml
filters:
  filter-procedure-rule:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    sql-pattern: ["^DROP\\s+PROCEDURE", "^CREATE\\s+PROCEDURE"]
    action: Ignore
```

`filter-procedure-rule` filters out the `^CREATE\\s+PROCEDURE` and `^DROP\\s+PROCEDURE` statements of all tables that match the `test_*`.`t_*` pattern.

### Filter out the SQL statements that the TiDB parser does not support

For the SQL statements that the TiDB parser does not support, DM cannot parse them and get the `schema`/`table` information. So you must use the global filtering rule: `schema-pattern: "*"`.

> **Note:**
>
> To avoid filtering out data that need to be migrated, you must configure the global filtering rule as strictly as possible.

To filter out the `PARTITION` statements that the TiDB parser (of some version) does not support, configure the following filtering rule:

```yaml
filters:
  filter-partition-rule:
    schema-pattern: "*"
    sql-pattern: ["ALTER\\s+TABLE[\\s\\S]*ADD\\s+PARTITION", "ALTER\\s+TABLE[\\s\\S]*DROP\\s+PARTITION"]
    action: Ignore
```

### Report errors on some DDL statements

If you need to block and report errors on DDL statements generated by some upstream operations before DM replicates them to TiDB, you can use the following settings:

```yaml
filters:
  filter-procedure-rule:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    events: ["truncate table", "truncate table partition"]
    action: Error
```