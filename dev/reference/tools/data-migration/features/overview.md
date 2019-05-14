---
title: Data Synchronization Features
summary: Learn about the data synchronization features provided by the Data Migration tool.
category: reference
aliases: ['/docs/tools/dm/data-synchronization-features/']
---

# Data Synchronization Features

This document describes the data synchronization features provided by the Data Migration tool and explains the configuration of corresponding parameters.

## Table routing

The table routing feature enables DM to synchronize a certain table of the upstream MySQL or MariaDB instance to the specified table in the downstream.

> **Note:**
>
> - Configuring multiple different routing rules for a single table is not supported.
> - The match rule of schema needs to be configured separately, which is used to synchronize `create/drop schema xx`, as shown in `rule-2` of the [parameter configuration](#parameter-configuration).

### Parameter configuration

```yaml
routes:
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    target-schema: "test"
    target-table: "t"
  rule-2:
    schema-pattern: "test_*"
    target-schema: "test"
```

### Parameter explanation

DM synchronizes the upstream MySQL or MariaDB instance table that matches the [`schema-pattern`/`table-pattern` rule provided by Table selector](/tools/dm/table-selector.md) to the downstream `target-schema`/`target-table`.

### Usage examples

This sections shows the usage examples in different scenarios.

#### Merge sharded schemas and tables

Assuming in the scenario of sharded schemas and tables, you want to synchronize the `test_{1,2,3...}`.`t_{1,2,3...}` tables in two upstream MySQL instances to the `test`.`t` table in the downstream TiDB instance.

To synchronize the upstream instances to the downstream `test`.`t`, you must create two routing rules:

- `rule-1` is used to synchronize DML or DDL statements of the table that matches `schema-pattern: "test_*"` and `table-pattern: "t_*"` to the downstream `test`.`t`.
- `rule-2` is used to synchronize DDL statements of the schema that matches `schema-pattern: "test_*"`, such as `create/drop schema xx`.

> **Note:**
>
> - If the downstream `schema: test` already exists and will not be deleted, you can omit `rule-2`.
> - If the downstream `schema: test` does not exist and only `rule-1` is configured, then it reports the `schema test doesn't exist` error during synchronization.

```yaml
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    target-schema: "test"
    target-table: "t"
  rule-2:
    schema-pattern: "test_*"
    target-schema: "test"
```

#### Merge sharded schemas

Assuming in the scenario of sharded schemas, you want to synchronize the `test_{1,2,3...}`.`t_{1,2,3...}` tables in the two upstream MySQL instances to the `test`.`t_{1,2,3...}` tables in the downstream TiDB instance.

To synchronize the upstream schemas to the downstream `test`.`t_[1,2,3]`, you only need to create one routing rule.

```yaml
  rule-1:
    schema-pattern: "test_*"
    target-schema: "test"
```

#### Incorrect table routing

Assuming that the following two routing rules are configured and `test_1_bak`.`t_1_bak` matches both `rule-1` and `rule-2`, an error is reported because the table routing configuration violates the number limitation.

```yaml
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    target-schema: "test"
    target-table: "t"
  rule-2:
    schema-pattern: "test_1_bak"
    table-pattern: "t_1_bak"
    target-schema: "test"
    target-table: "t_bak"
```

## Black and white table lists

The black and white lists filtering rule of the upstream database instance tables is similar to MySQL replication-rules-db/tables, which can be used to filter or only synchronize all operations of some databases or some tables.

### Parameter configuration

```yaml
black-white-list:
  rule-1:
    do-dbs: ["~^test.*"]         # Starting with "~" indicates it is a regular expression.
​    ignore-dbs: ["mysql"]
    do-tables:
    - db-name: "~^test.*"
      tbl-name: "~^t.*"
    - db-name: "test"
      tbl-name: "t"
    ignore-tables:
    - db-name: "test"
      tbl-name: "log"
```

### Parameter explanation

- `do-dbs`: white lists of the schemas to be synchronized
- `ignore-dbs`: black lists of the schemas to be synchronized
- `do-tables`: white lists of the tables to be synchronized
- `ignore-tables`: black lists of the tables to be synchronized
- In black and white lists, starting with the "~" character indicates it is a [regular expression](https://golang.org/pkg/regexp/syntax/#hdr-Syntax).

### Filtering process

The filtering process is as follows:

1. Filter at the schema level:

    - If `do-dbs` is not empty, judge whether a matched schema exists in `do-dbs`.

        - If yes, continue to filter at the table level.
        - If not, filter `test`.`t`.

    - If `do-dbs` is empty and `ignore-dbs` is not empty, judge whether a matched schema exits in `ignore-dbs`.

        - If yes, filter `test`.`t`.
        - If not, continue to filter at the table level.

    - If both `do-dbs` and `ignore-dbs` are empty, continue to filter at the table level.

2. Filter at the table level:

    1. If `do-tables` is not empty, judge whether a matched table exists in `do-tables`.  

        - If yes, synchronize `test`.`t`.
        - If not, filter `test`.`t`.

    2. If `ignore-tables` is not empty, judge whether a matched table exists in `ignore-tables`.

        - If yes, filter `test`.`t`.
        - If not, synchronize `test`.`t`.

    3. If both `do-tables` and `ignore-tables` are empty, synchronize `test`.`t`.

> **Note:**
>
> To judge whether the schema `test` is filtered, you only need to filter at the schema level.

### Usage example

Assume that the upstream MySQL instances include the following tables:

```
`logs`.`messages_2016`
`logs`.`messages_2017`
`logs`.`messages_2018`
`forum`.`users`
`forum`.`messages`
`forum_backup_2016`.`messages`
`forum_backup_2017`.`messages`
`forum_backup_2018`.`messages`
```

The configuration is as follows:

```yaml
black-white-list:
  bw-rule:
    do-dbs: ["forum_backup_2018", "forum"]
    ignore-dbs: ["~^forum_backup_"]
    do-tables:
    - db-name: "logs"
      tbl-name: "~_2018$"
    - db-name: "~^forum.*"
​      tbl-name: "messages"
    ignore-tables:
    - db-name: "~.*"
​      tbl-name: "^messages.*"
```

After using the `bw-rule` rule:

| Table | Whether to filter | Why filter |
|:----|:----|:--------------|
| `logs`.`messages_2016` | Yes | The schema `logs` fails to match any `do-dbs`. |
| `logs`.`messages_2017` | Yes | The schema `logs` fails to match any `do-dbs`. |
| `logs`.`messages_2018` | Yes | The schema `logs` fails to match any `do-dbs`. |
| `forum_backup_2016`.`messages` | Yes | The schema `forum_backup_2016` fails to match any `do-dbs`. |
| `forum_backup_2017`.`messages` | Yes | The schema `forum_backup_2017` fails to match any `do-dbs`. |
| `forum`.`users` | Yes | 1. The schema `forum` matches `do-dbs` and continues to filter at the table level.<br> 2. The schema and table fail to match any of `do-tables` and `ignore-tables` and `do-tables` is not empty. |
| `forum`.`messages` | No | 1. The schema `forum` matches `do-dbs` and continues to filter at the table level.<br> 2. The table `messages` is in the `db-name: "~^forum.*",tbl-name: "messages"` of `do-tables`. |
| `forum_backup_2018`.`messages` | No | 1. The schema `forum_backup_2018` matches `do-dbs` and continues to filter at the table level.<br> 2. The schema and table match the `db-name: "~^forum.*",tbl-name: "messages"` of `do-tables`. |

## Binlog event filter

Binlog event filter is a more fine-grained filtering rule than the black and white lists filtering rule. You can use statements like `INSERT` or `TRUNCATE TABLE` to specify the binlog events of `schema/table` that you need to synchronize or filter out.

> **Note:**
>
> If a same table matches multiple rules, these rules are applied in order and the black list has priority over the white list. This means if both the `Ignore` and `Do` rules are applied to a single table, the `Ignore` rule takes effect.

### Parameter configuration

```yaml
filters:
  rule-1:
    schema-pattern: "test_*"
    ​table-pattern: "t_*"
    ​events: ["truncate table", "drop table"]
    sql-pattern: ["^DROP\\s+PROCEDURE", "^CREATE\\s+PROCEDURE"]
    ​action: Ignore
```

### Parameter explanation

- [`schema-pattern`/`table-pattern`](/tools/dm/table-selector.md): the binlog events or DDL SQL statements of upstream MySQL or MariaDB instance tables that match `schema-pattern`/`table-pattern` are filtered by the rules below.

- `events`: the binlog event array.

    | Events            | Type | Description                   |
    | ---------------   | ---- | ----------------------------- |
    | `all`             |      | Includes all the events below |
    | `all dml`         |      | Includes all DML events below |
    | `all ddl`         |      | Includes all DDL events below |
    | `none`            |      | Includes none of the events below |
    | `none ddl`        |      | Includes none of the DDL events below |
    | `none dml`        |      | Includes none of the DML events below |
    | `insert`          | DML  | The `INSERT` DML event              |
    | `update`          | DML  | The `UPDATE` DML event              |
    | `delete`          | DML  | The `DELETE` DML event              |
    | `create database` | DDL  | The `CREATE DATABASE` DDL event         |
    | `drop database`   | DDL  | The `DROP DATABASE` DDL event           |
    | `create table`    | DDL  | The `CREATE TABLE` DDL event      |
    | `create index`    | DDL  | The `CREATE INDEX` DDL event          |
    | `drop table`      | DDL  | The `DROP TABLE` DDL event              |
    | `truncate table`  | DDL  | The `TRUNCATE TABLE` DDL event          |
    | `rename table`    | DDL  | The `RENAME TABLE` DDL event            |
    | `drop index`      | DDL  | The `DROP INDEX` DDL event           |
    | `alter table`     | DDL  | The `ALTER TABLE` DDL event           |

- `sql-pattern`: it is used to filter specified DDL SQL statements. The matching rule supports using a regular expression. For example, `"^DROP\\s+PROCEDURE"`.

- `action`: the string (`Do`/`Ignore`). Based on the following rules, it judges whether to filter. If either of the two rules is satisfied, the binlog will be filtered; otherwise, the binlog will not be filtered.

    - `Do`: the white list. The binlog will be filtered in either of the following two conditions:
        - The type of the event is not in the `event` list of the rule.
        - The SQL statement of the event cannot be matched by `sql-pattern` of the rule.
    - `Ignore`: the black list. The binlog will be filtered in either of the following two conditions:
        - The type of the event is in the `event` list of the rule.
        - The SQL statement of the event can be matched by `sql-pattern` of the rule.

### Usage examples

This sections shows the usage examples in the scenario of sharding (sharded schemas and tables).

#### Filter all sharding deletion operations

To filter out all deletion operations, configure the following two filtering rules:

- `filter-table-rule` filters out the `truncate table`, `drop table` and `delete statement` operations of all tables that match the `test_*`.`t_*` pattern.
- `filter-schema-rule` filters out the `drop database` operation of all schemas that match the `test_*` pattern.

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

#### Only synchronize sharding DML statements

To only synchronize sharding DML statements, configure the following two filtering rules:

- `do-table-rule` only synchronizes the `create table`, `insert`, `update` and `delete` statements of all tables that match the `test_*`.`t_*` pattern.
- `do-schema-rule` only synchronizes the `create database` statement of all schemas that match the `test_*` pattern.

> **Note:**
>
> The reason why the `create database/table` statement is synchronized is that you can synchronize DML statements only after the schema and table are created.

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

#### Filter out the SQL statements that TiDB does not support

To filter out the `PROCEDURE` statements that TiDB does not support, configure the following `filter-procedure-rule`:

```yaml
filters:
  filter-procedure-rule:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    sql-pattern: ["^DROP\\s+PROCEDURE", "^CREATE\\s+PROCEDURE"]
    action: Ignore
```

`filter-procedure-rule`  filters out the `^CREATE\\s+PROCEDURE` and `^DROP\\s+PROCEDURE` statements of all tables that match the `test_*`.`t_*` pattern.

#### Filter out the SQL statements that the TiDB parser does not support

For the SQL statements that the TiDB parser does not support, DM cannot parse them and get the `schema`/`table` information. So you must use the global filtering rule: `schema-pattern: "*"`.

> **Note:**
>
> To avoid unexpectedly filtering out data that need to be replicated, you must configure the global filtering rule as strictly as possible.

To filter out the `PARTITION` statements that the TiDB parser does not support, configure the following filtering rule:

```yaml
filters:
  filter-partition-rule:
    schema-pattern: "*"
    sql-pattern: ["ALTER\\s+TABLE[\\s\\S]*ADD\\s+PARTITION", "ALTER\\s+TABLE[\\s\\S]*DROP\\s+PARTITION"]
    action: Ignore
```

## Column mapping

The column mapping feature supports modifying the value of table columns. You can execute different modification operations on the specified column according to different expressions. Currently, only the built-in expressions provided by DM are supported.

> **Note:**
>
> - It does not support modifying the column type and the table schema.
> - It does not support configuring multiple different column mapping rules for a same table.

### Parameter configuration

```yaml
column-mappings:
  rule-1:
​    schema-pattern: "test_*"
​    table-pattern: "t_*"
​    expression: "partition id"
​    source-column: "id"
​    target-column: "id"
​    arguments: ["1", "test_", "t_"]
  rule-2:
​    schema-pattern: "test_*"
​    table-pattern: "t_*"
​    expression: "partition id"
​    source-column: "id"
​    target-column: "id"
​    arguments: ["2", "test_", "t_"]
```

### Parameter explanation

- [`schema-pattern`/`table-pattern`](/tools/dm/table-selector.md): to execute column value modifying operations on the upstream MySQL or MariaDB instance tables that match the `schema-pattern`/`table-pattern` filtering rule.
- `source-column`, `target-column`: to modify the value of the `source-column` column according to specified `expression` and assign the new value to `target-column`.
- `expression`: the expression used to modify data. Currently, only the `partition id` built-in expression is supported.

#### The `partition id` expression

`partition id` is used to resolve the conflicts of auto-increment primary keys of sharded tables.

**`partition id` restrictions**

Note the following restrictions:

- The `partition id` expression only supports the bigint type of atuo-increment primary key.
- The schema name format must be `the schema prefix + number (the schema ID)`. For example, it supports `s_1`, but does not support `s_a`.
- The table name format must be `the table name + number (the table ID)`.
- Restrictions on sharding size:
    - It supports 16 MySQL or MariaDB instances at most (0 <= instance ID <= 15).
    - Each instance supports 128 schemas at most (0 <= schema ID  <= 127).
    - Each schema of each instance supports 256 tables at most (0 <= table ID <= 255).
    - The ID range of the auto-increment primary key is "0 <= ID <= 17592186044415".
    - The `{instance ID、schema ID、table ID}` group must be unique.
- Currently, the `partition id` expression is a customized feature. If you want to modify this feature, contact the corresponding developers.

**`partition id` arguments configuration**

Configure the following three arguments in order:

- `instance_id`: the ID of the upstream sharded MySQL or MariaDB instance (0 <= instance ID <= 15)
- The schema prefix: used to parse the schema name and get the `schema ID`
- The table prefix: used to parse the table name and get the `table ID`

**`partition id` expression rules**

`partition id` fills the beginning bit of the auto-increment primary key ID with the argument number, and computes an int64 (MySQL bigint) type of value. The specific rules are as follows:

- int64 bit indicates `[1:1 bit] [2:4 bits] [3：7 bits] [4:8 bits] [5: 44 bits]`.
- `1`: the sign bit, reserved
- `2`: the instance ID, 4 bits by default
- `3`: the schema ID, 7 bits by default
- `4`: the table ID, 8 bits by default
- `5`: the auto-increment primary key ID, 44 bits by default

### Usage example

Assuming in the sharding scenario where all tables have the auto-increment primary key, you want to synchronize two upstream MySQL instances `test_{1,2,3...}`.`t_{1,2,3...}` to the downstream TiDB instances `test`.`t`.

Configure the following two rules:

```yaml
column-mappings:
  rule-1:
​    schema-pattern: "test_*"
​    table-pattern: "t_*"
​    expression: "partition id"
​    source-column: "id"
​    target-column: "id"
​    arguments: ["1", "test_", "t_"]
  rule-2:
​    schema-pattern: "test_*"
​    table-pattern: "t_*"
​    expression: "partition id"
​    source-column: "id"
​    target-column: "id"
​    arguments: ["2", "test_", "t_"]
```

- The column ID of the MySQL instance 1 table `test_1`.`t_1` is converted from `1` to `1 << (64-1-4) | 1 << (64-1-4 -7) | 1 << 44 | 1 = 580981944116838401`.
- The row ID of the MySQL instance 2 table `test_1`.`t_2` is converted from `2` to `2 << (64-1-4) | 1 << (64-1-4 -7) | 2 << 44 | 2 = 1157460288606306306`.

## Synchronization delay monitoring

The heartbeat feature supports calculating the real-time synchronization delay between each synchronization task and MySQL or MariaDB based on real synchronization data.

> **Note:**
>
> - The estimation accuracy of the synchronization delay is at the second level.
> - The heartbeat related binlog will not be synchronized into the downstream, which is discarded after calculating the synchronization delay.

### System privileges

If the heartbeat feature is enabled, the upstream MySQL or MariaDB instances must provide the following privileges:

- SELECT
- INSERT
- CREATE (databases, tables)

### Parameter configuration

In the task configuration file, enable the heartbeat feature:

```
enable-heartbeat: true
```

### Principles introduction

- DM-worker creates the `dm_heartbeat` (currently unconfigurable) schema in the corresponding upstream MySQL or MariaDB.
- DM-worker creates the `heartbeat` (currently unconfigurable) table in the corresponding upstream MySQL or MariaDB.
- DM-worker uses `replace statement` to update the current `TS_master` timestamp every second (currently unconfigurable) in the corresponding upstream MySQL or MariaDB `dm_heartbeat`.`heartbeat` tables.
- DM-worker updates the `TS_slave_task` synchronization time after each synchronization task obtains the `dm_heartbeat`.`heartbeat` binlog.
- DM-worker queries the current `TS_master` timestamp in the corresponding upstream MySQL or MariaDB `dm_heartbeat`.`heartbeat` tables every 10 seconds, and calculates `task_lag` = `TS_master` - `TS_slave_task` for each task.

See the `replicate lag` in the [binlog replication](/dev/reference/tools/data-migration/monitor.md#binlog-replication) processing unit of DM monitoring metrics.
