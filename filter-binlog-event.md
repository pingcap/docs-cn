---
title: Filter Binlog Events
summary: Learn how to filter binlog events when migrating data.
---

# Filter Binlog Events

This document describes how to filter binlog events when you use DM to perform continuous incremental data replication. For the detailed replication instructions, refer to the following documents by scenarios:

- [Migrate Small Datasets from MySQL to TiDB](/migrate-small-mysql-to-tidb.md)
- [Migrate Large Datasets from MySQL to TiDB](/migrate-large-mysql-to-tidb.md)
- [Migrate and Merge MySQL Shards of Small Datasets to TiDB](/migrate-small-mysql-shards-to-tidb.md)
- [Migrate and Merge MySQL Shards of Large Datasets to TiDB](/migrate-large-mysql-shards-to-tidb.md)

## Configuration

To use binlog event filter, add a `filter` to the task configuration file of DM, as shown below:

```yaml
filters:
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    events: ["truncate table", "drop table"]
    sql-pattern: ["^DROP\\s+PROCEDURE", "^CREATE\\s+PROCEDURE"]
    action: Ignore
```

- `schema-pattern`/`table-pattern`: Filters matching schemas or tables
- `events`: Filters binlog events. Supported events are listed in the table below:

  | Event           | Category | Description                       |
  | --------------- | ---- | --------------------------|
  | all             |      | Includes all events            |
  | all dml         |      | Includes all DML events        |
  | all ddl         |      | Includes all DDL events        |
  | none            |      | Includes no event          |
  | none ddl        |      | Excludes all DDL events      |
  | none dml        |      | Excludes all DML events      |
  | insert          | DML  | Insert DML event      |
  | update          | DML  | Update DML event      |
  | delete          | DML  | Delete DML event      |
  | create database | DDL  | Create database event |
  | drop database   | DDL  | Drop database event   |
  | create table    | DDL  | Create table event    |
  | create index    | DDL  | Create index event    |
  | drop table      | DDL  | Drop table event      |
  | truncate table  | DDL  | Truncate table event  |
  | rename table    | DDL  | Rename table event    |
  | drop index      | DDL  | Drop index event      |
  | alter table     | DDL  | Alter table event     |

- `sql-pattern`: Filters specified DDL SQL statements. The matching rule supports using a regular expression.
- `action`: `Do` or `Ignore`

    - `Do`: the allow list. A binlog event is replicated if meeting either of the following two conditions:

        - The event matches the rule setting.
        - sql-pattern has been specified and the SQL statement of the event matches any of the sql-pattern options.

    - `Ignore`: the block list. A binlog event is filtered out if meeting either of the following two conditions:

        - The event matches the rule setting.
        - sql-pattern has been specified and the SQL statement of the event matches any of the sql-pattern options.

    If both `Do` and `Ignore` are configured, `Ignore` has higher priority over `Do`. That is, an event satisfying both `Ignore` and `Do` conditions will be filtered out.

## Application scenarios

This section describes the application scenarios of binlog event filter.

### Filter out all sharding deletion operations

To filter out all deletion operations, configure a `filter-table-rule` and a `filter-schema-rule`, as shown below:

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

### Migrate only DML operations of sharded schemas and tables

To replicate only DML statements, configure two `Binlog event filter rule`, as shown below:

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

### Filter out SQL statements not supported by TiDB

To filter out SQL statements not supported by TiDB, configure a `filter-procedure-rule`, as shown below:

```
filters:
  filter-procedure-rule:
    schema-pattern: "*"
    sql-pattern: [".*\\s+DROP\\s+PROCEDURE", ".*\\s+CREATE\\s+PROCEDURE", "ALTER\\s+TABLE[\\s\\S]*ADD\\s+PARTITION", "ALTER\\s+TABLE[\\s\\S]*DROP\\s+PARTITION"]
    action: Ignore
```

> **Warning:**
>
> To avoid filtering out data that needs to be migrated, configure the global filtering rule as strictly as possible.

## See also

[Filter Binlog Events Using SQL Expressions](/filter-dml-event.md)
