---
title: Changefeed Log Filters
summary: Learn how to use the table filter and event filter of TiCDC.
---

# Changefeed Log Filters

TiCDC supports filtering data by tables and events. This document introduces how to use the two types of filters.

## Table filter

Table filter is a feature that allows you to keep or filter out specific databases and tables by specifying the following configurations:

```toml
[filter]
# Filter rules
rules = ['*.*', '!test.*']
```

Common filter rules:

- `rules = ['*.*']`
    - Replicate all tables (not including system tables)
- `rules = ['test1.*']`
    - Replicate all tables in the `test1` database
- `rules = ['*.*', '!scm1.tbl2']`
    - Replicate all tables except for the `scm1.tbl2` table
- `rules = ['scm1.tbl2', 'scm1.tbl3']`
    - Only replicate tables `scm1.tbl2` and `scm1.tbl3`
- `rules = ['scm1.tidb_*']`
    - Replicate all tables in the `scm1` database whose names start with `tidb_`

For more information, see [Table filter syntax](/table-filter.md#syntax).

## Event filter rules

Starting in v6.2.0, TiCDC supports event filter. You can configure event filter rules to filter out the DML and DDL events that meet the specified conditions.

The following is an example of event filter rules:

```toml
[filter]
# The event filter rules must be under the `[filter]` configuration. You can configure multiple event filters at the same time.

[[filter.event-filters]]
matcher = ["test.worker"] # matcher is an allow list, which means this rule only applies to the worker table in the test database.
ignore-event = ["insert"] # Ignore insert events.
ignore-sql = ["^drop", "add column"] # Ignore DDLs that start with "drop" or contain "add column".
ignore-delete-value-expr = "name = 'john'" # Ignore delete DMLs that contain the condition "name = 'john'".
ignore-insert-value-expr = "id >= 100" # Ignore insert DMLs that contain the condition "id >= 100".
ignore-update-old-value-expr = "age < 18 or name = 'lili'" # Ignore update DMLs whose old value contains "age < 18" or "name = 'lili'".
ignore-update-new-value-expr = "gender = 'male' and age > 18" # Ignore update DMLs whose new value contains "gender = 'male'" and "age > 18".
```

Description of configuration parameters:

- `matcher`: the database and table that this event filter rule applies to. The syntax is the same as [table filter](/table-filter.md).
- `ignore-event`: the event type to be ignored. This parameter accepts an array of strings. You can configure multiple event types. Currently, the following event types are supported:

| Event           | Type | Alias | Description         |
| --------------- | ---- | -|--------------------------|
| all dml         |      | |Matches all DML events       |
| all ddl         |      | |Matches all DDL events         |
| insert          | DML  | |Matches `insert` DML event      |
| update          | DML  | |Matches `update` DML event      |
| delete          | DML  | |Matches `delete` DML event      |
| create schema   | DDL  | create database |Matches `create database` event |
| drop schema     | DDL  | drop database  |Matches `drop database` event |
| create table    | DDL  | |Matches `create table` event    |
| drop table      | DDL  | |Matches `drop table` event      |
| rename table    | DDL  | |Matches `rename table` event    |
| truncate table  | DDL  | |Matches `truncate table` event  |
| alter table     | DDL  | |Matches `alter table` event, including all clauses of `alter table`, `create index` and `drop index`   |
| add table partition    | DDL  | |Matches `add table partition` event     |
| drop table partition    | DDL  | |Matches `drop table partition` event     |
| truncate table partition    | DDL  | |Matches `truncate table partition` event     |
| create view     | DDL  | |Matches `create view`event     |
| drop view     | DDL  | |Matches `drop view` event     |

- `ignore-sql`: the DDL statements to be ignored. This parameter accepts an array of strings, in which you can configure multiple regular expressions. This rule only applies to DDL events.
- `ignore-delete-value-expr`: this parameter accepts a SQL expression. This rule only applies to delete DML events with the specified value.
- `ignore-insert-value-expr`: this parameter accepts a SQL expression. This rule only applies to insert DML events with the specified value.
- `ignore-update-old-value-expr`: this parameter accepts a SQL expression. This rule only applies to update DML events whose old value contains the specified value.
- `ignore-update-new-value-expr`: this parameter accepts a SQL expression. This rule only applies to update DML events whose new value contains the specified value.

> **Note:**
>
> - When TiDB updates a value in the column of the clustered index, TiDB splits an `UPDATE` event into a `DELETE` event and an `INSERT` event. TiCDC does not identify such events as an `UPDATE` event and thus cannot correctly filter out such events.
> - When you configure a SQL expression, make sure all tables that matches `matcher` contain all the columns specified in the SQL expression. Otherwise, the replication task cannot be created. In addition, if the table schema changes during the replication, which results in a table no longer containing a required column, the replication task fails and cannot be resumed automatically. In such a situation, you must manually modify the configuration and resume the task.
