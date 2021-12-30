---
title: Key Features
summary: Learn about the key features of DM and appropriate parameter configurations.
aliases: ['/docs/tidb-data-migration/dev/feature-overview/']
---

# Key Features

This document describes the data migration features provided by TiDB Data Migration (DM) and introduces appropriate parameter configurations.

For different DM versions, pay attention to the different match rules of schema or table names in the table routing, block & allow lists, and binlog event filter features:

+ For DM v1.0.5 or later versions, all the above features support the [wildcard match](https://en.wikipedia.org/wiki/Glob_(programming)#Syntax). For all versions of DM, note that there can be **only one** `*` in the wildcard expression, and `*` **must be placed at the end**.
+ For DM versions earlier than v1.0.5, table routing and binlog event filter support the wildcard but do not support the `[...]` and `[!...]` expressions. The block & allow lists only supports the regular expression.

It is recommended that you use the wildcard for matching in simple scenarios.

## Table routing

The table routing feature enables DM to migrate a certain table of the upstream MySQL or MariaDB instance to the specified table in the downstream.

> **Note:**
>
> - Configuring multiple different routing rules for a single table is not supported.
> - The match rule of schema needs to be configured separately, which is used to migrate `CREATE/DROP SCHEMA xx`, as shown in `rule-2` of the [parameter configuration](#parameter-configuration).

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

DM migrates the upstream MySQL or MariaDB instance table that matches the [`schema-pattern`/`table-pattern` rule provided by Table selector](/dm/table-selector.md) to the downstream `target-schema`/`target-table`.

### Usage examples

This section shows the usage examples in different scenarios.

#### Merge sharded schemas and tables

Assuming in the scenario of sharded schemas and tables, you want to migrate the `test_{1,2,3...}`.`t_{1,2,3...}` tables in two upstream MySQL instances to the `test`.`t` table in the downstream TiDB instance.

To migrate the upstream instances to the downstream `test`.`t`, you must create the following routing rules:

- `rule-1` is used to migrate DML or DDL statements of the table that matches `schema-pattern: "test_*"` and `table-pattern: "t_*"` to the downstream `test`.`t`.
- `rule-2` is used to migrate DDL statements of the schema that matches `schema-pattern: "test_*"`, such as `CREATE/DROP SCHEMA xx`.

> **Note:**
>
> - If the downstream `schema: test` already exists and is not to be deleted, you can omit `rule-2`.
> - If the downstream `schema: test` does not exist and only `rule-1` is configured, then it reports the `schema test doesn't exist` error during migration.

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

Assuming in the scenario of sharded schemas, you want to migrate the `test_{1,2,3...}`.`t_{1,2,3...}` tables in the two upstream MySQL instances to the `test`.`t_{1,2,3...}` tables in the downstream TiDB instance.

To migrate the upstream schemas to the downstream `test`.`t_[1,2,3]`, you only need to create one routing rule.

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

## Block and allow table lists

The block and allow lists filtering rule of the upstream database instance tables is similar to MySQL replication-rules-db/tables, which can be used to filter or only migrate all operations of some databases or some tables.

### Parameter configuration

```yaml
block-allow-list:             # Use black-white-list if the DM version is earlier than or equal to v2.0.0-beta.2.
  rule-1:
    do-dbs: ["test*"]         # Starting with characters other than "~" indicates that it is a wildcard;
                              # v1.0.5 or later versions support the regular expression rules.
    do-tables:
    - db-name: "test[123]"    # Matches test1, test2, and test3.
      tbl-name: "t[1-5]"      # Matches t1, t2, t3, t4, and t5.
    - db-name: "test"
      tbl-name: "t"
  rule-2:
    do-dbs: ["~^test.*"]      # Starting with "~" indicates that it is a regular expression.
    ignore-dbs: ["mysql"]
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

- `do-dbs`: allow lists of the schemas to be migrated, similar to [`replicate-do-db`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-do-db) in MySQL
- `ignore-dbs`: block lists of the schemas to be migrated, similar to [`replicate-ignore-db`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-ignore-db) in MySQL
- `do-tables`: allow lists of the tables to be migrated, similar to [`replicate-do-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-do-table) in MySQL. Both `db-name` and `tbl-name` must be specified
- `ignore-tables`: block lists of the tables to be migrated, similar to [`replicate-ignore-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-ignore-table) in MySQL. Both `db-name` and `tbl-name` must be specified

If a value of the above parameters starts with the `~` character, the subsequent characters of this value are treated as a [regular expression](https://golang.org/pkg/regexp/syntax/#hdr-syntax). You can use this parameter to match schema or table names.

### Filtering process

The filtering rules corresponding to `do-dbs` and `ignore-dbs` are similar to the [Evaluation of Database-Level Replication and Binary Logging Options](https://dev.mysql.com/doc/refman/5.7/en/replication-rules-db-options.html) in MySQL. The filtering rules corresponding to `do-tables` and `ignore-tables` are similar to the [Evaluation of Table-Level Replication Options](https://dev.mysql.com/doc/refman/5.7/en/replication-rules-table-options.html) in MySQL.

> **Note:**
>
> In DM and in MySQL, the allow and block lists filtering rules are different in the following ways:
>
> - In MySQL, [`replicate-wild-do-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-wild-do-table) and [`replicate-wild-ignore-table`](https://dev.mysql.com/doc/refman/5.7/en/replication-options-replica.html#option_mysqld_replicate-wild-ignore-table) support wildcard characters. In DM, some parameter values directly supports regular expressions that start with the `~` character.
> - DM currently only supports binlogs in the `ROW` format, and does not support those in the `STATEMENT` or `MIXED` format. Therefore, the filtering rules in DM correspond to those in the `ROW` format in MySQL.
> - MySQL determines a DDL statement only by the database name explicitly specified in the `USE` section of the statement. DM determines a statement first based on the database name section in the DDL statement. If the DDL statement does not contain such a section, DM determines the statement by the `USE` section. Suppose that the SQL statement to be determined is `USE test_db_2; CREATE TABLE test_db_1.test_table (c1 INT PRIMARY KEY)`; that `replicate-do-db=test_db_1` is configured in MySQL and `do-dbs: ["test_db_1"]` is configured in DM. Then this rule only applies to DM and not to MySQL.

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

        - If yes, migrate `test`.`t`.
        - If not, filter `test`.`t`.

    2. If `ignore-tables` is not empty, judge whether a matched table exists in `ignore-tables`.

        - If yes, filter `test`.`t`.
        - If not, migrate `test`.`t`.

    3. If both `do-tables` and `ignore-tables` are empty, migrate `test`.`t`.

> **Note:**
>
> To judge whether the schema `test` should be filtered, you only need to filter at the schema level.

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
block-allow-list:  # Use black-white-list if the DM version is earlier than or equal to v2.0.0-beta.2.
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
| `forum`.`users` | Yes | 1. The schema `forum` matches `do-dbs` and continues to filter at the table level.<br/> 2. The schema and table fail to match any of `do-tables` and `ignore-tables` and `do-tables` is not empty. |
| `forum`.`messages` | No | 1. The schema `forum` matches `do-dbs` and continues to filter at the table level.<br/> 2. The table `messages` is in the `db-name: "~^forum.*",tbl-name: "messages"` of `do-tables`. |
| `forum_backup_2018`.`messages` | No | 1. The schema `forum_backup_2018` matches `do-dbs` and continues to filter at the table level.<br/> 2. The schema and table match the `db-name: "~^forum.*",tbl-name: "messages"` of `do-tables`. |

## Binlog event filter

Binlog event filter is a more fine-grained filtering rule than the block and allow lists filtering rule. You can use statements like `INSERT` or `TRUNCATE TABLE` to specify the binlog events of `schema/table` that you need to migrate or filter out.

> **Note:**
>
> - If the same table matches multiple rules, these rules are applied in order and the block list has priority over the allow list. This means if both the `Ignore` and `Do` rules are applied to a table, the `Ignore` rule takes effect.
> - Starting from DM v2.0.2, you can configure binlog event filters in the source configuration file. For details, see [Upstream Database Configuration File](/dm/dm-source-configuration-file.md).

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

- [`schema-pattern`/`table-pattern`](/dm/table-selector.md): the binlog events or DDL SQL statements of upstream MySQL or MariaDB instance tables that match `schema-pattern`/`table-pattern` are filtered by the rules below.

- `events`: the binlog event array. You can only select one or more `Event`s from the following table:

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

- `action`: the string (`Do`/`Ignore`). Based on the following rules, it judges whether to filter. If either of the two rules is satisfied, the binlog is filtered; otherwise, the binlog is not filtered.

    - `Do`: the allow list. The binlog is filtered in either of the following two conditions:
        - The type of the event is not in the `event` list of the rule.
        - The SQL statement of the event cannot be matched by `sql-pattern` of the rule.
    - `Ignore`: the block list. The binlog is filtered in either of the following two conditions:
        - The type of the event is in the `event` list of the rule.
        - The SQL statement of the event can be matched by `sql-pattern` of the rule.

### Usage examples

This section shows the usage examples in the scenario of sharding (sharded schemas and tables).

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

#### Only migrate sharding DML statements

To only migrate sharding DML statements, configure the following two filtering rules:

- `do-table-rule` only migrates the `create table`, `insert`, `update` and `delete` statements of all tables that match the `test_*`.`t_*` pattern.
- `do-schema-rule` only migrates the `create database` statement of all schemas that match the `test_*` pattern.

> **Note:**
>
> The reason why the `create database/table` statement is migrated is that you can migrate DML statements only after the schema and table are created.

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

`filter-procedure-rule` filters out the `^CREATE\\s+PROCEDURE` and `^DROP\\s+PROCEDURE` statements of all tables that match the `test_*`.`t_*` pattern.

#### Filter out the SQL statements that the TiDB parser does not support

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

## Online DDL tools

In the MySQL ecosystem, tools such as gh-ost and pt-osc are widely used. DM provides supports for these tools to avoid migrating unnecessary intermediate data.

### Restrictions

- DM only supports gh-ost and pt-osc.
- When `online-ddl` is enabled, the checkpoint corresponding to incremental replication should not be in the process of online DDL execution. For example, if an upstream online DDL operation starts at `position-A` and ends at `position-B` of the binlog, the starting point of incremental replication should be earlier than `position-A` or later than `position-B`; otherwise, an error occurs. For details, refer to [FAQ](/dm/dm-faq.md#how-to-handle-the-error-returned-by-the-ddl-operation-related-to-the-gh-ost-table-after-online-ddl-scheme-gh-ost-is-set).

### Parameter configuration

<SimpleTab>
<div label="v2.0.5 and later">

In v2.0.5 and later versions, you need to use the `online-ddl` configuration item in the `task` configuration file.

- If the upstream MySQL/MariaDB (at the same time) uses the gh-ost or pt-osc tool, set `online-ddl` to `true` in the task configuration file:

```yml
online-ddl: true
```

> **Note:**
>
> Since v2.0.5, `online-ddl-scheme` has been deprecated, so you need to use `online-ddl` instead of `online-ddl-scheme`. That means that setting `online-ddl: true` overwrites `online-ddl-scheme`, and setting `online-ddl-scheme: "pt"` or `online-ddl-scheme: "gh-ost"` is converted to `online-ddl: true`.

</div>

<div label="earlier than v2.0.5">

Before v2.0.5 (not including v2.0.5), you need to use the `online-ddl-scheme` configuration item in the `task` configuration file.

- If the upstream MySQL/MariaDB uses the gh-ost tool, set it in the task configuration file:

```yml
online-ddl-scheme: "gh-ost"
```

- If the upstream MySQL/MariaDB uses the pt tool, set it in the task configuration file:

```yml
online-ddl-scheme: "pt"
```

</div>
</SimpleTab>

## Shard merge

DM supports merging the DML and DDL data in the upstream MySQL/MariaDB sharded tables and migrating the merged data to the downstream TiDB tables.

### Restrictions

Currently, the shard merge feature is supported only in limited scenarios. For details, refer to [Sharding DDL usage Restrictions in the pessimistic mode](/dm/feature-shard-merge-pessimistic.md#restrictions) and [Sharding DDL usage Restrictions in the optimistic mode](/dm/feature-shard-merge-optimistic.md#restrictions).

### Parameter configuration

Set `shard-mode` to `pessimistic` in the task configuration file:

```
shard-mode: "pessimistic" # The shard merge mode. Optional modes are ""/"pessimistic"/"optimistic". The "" mode is used by default which means sharding DDL merge is disabled. If the task is a shard merge task, set it to the "pessimistic" mode. After getting a deep understanding of the principles and restrictions of the "optimistic" mode, you can set it to the "optimistic" mode.
```

### Handle sharding DDL locks manually

In some abnormal scenarios, you need to [handle sharding DDL Locks manually](/dm/manually-handling-sharding-ddl-locks.md).
