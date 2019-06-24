---
title: Data Migration Task Configuration Options
summary: This document introduces the configuration options that apply to Data Migration tasks.
category: tools
---

# Data Migration Task Configuration Options

This document introduces the configuration options that apply to Data Migration tasks. 

## `task-mode`

- String (`full`/`incremental`/`all`)
- The task mode of data migration to be executed 
- Default value: `all`

    - `full`: Only makes a full backup of the upstream database and then restores it to the downstream database.
    - `incremental`: Only replicates the incremental data of the upstream database to the downstream database using the binlog.
    - `all`: `full` + `incremental`. Makes a full backup of the upstream database, imports the full data to the downstream database, and then uses the binlog to make an incremental replication to the downstream database starting from the exported position during the full backup process (binlog position/GTID).

## Routing rule

```
# `schema-pattern`/`table-pattern` uses the wildcard matching rule
schema level:
    schema-pattern: "test_*"
    target-schema: "test"

table level:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    target-schema: "test"
    target-table: "t"
```

Description: Replicates the upstream table data that matches `schema-pattern`/`table-pattern` to the downstream `target-schema`/`target-table`. You can set the routing rule at the schema/table level. 

Taking the above code block as an example:

- Schema level: Replicates all the upstream tables that match the `test_*` schema to the downstream `test` schema.  

    For example, `schema: test_1 - tables [a, b, c]`  =>  `schema:test -  tables [a, b, c]`

- Table level: Replicates the `t_*` matched upstream tables with `test_*` matched schema to the downstream `schema:test table:t` table.

> **Notes:** 
>
> - The `table level` rule has a higher priority than the `schema level` rule.
> - You can set one routing rule at most at one level.


## Black and white lists filtering rule

```
instance:
    do-dbs: ["~^test.*", "do"]         # Starts with "~", indicating it is a regular expression
    ignore-dbs: ["mysql", "ignored"]
    do-tables:
    - db-name: "~^test.*"
      tbl-name: "~^t.*"
    - db-name: "do"
      tbl-name: "do"
    ignore-tables:
    - db-name: "do"
      tbl-name: "do"
```

The black and white lists filtering rule of the upstream database instances is similar to MySQL `replication-rules-db`/`replication-rules-table`.

The filter process is as follows:

1. Filter at the schema level:

    - If `do-dbs` is not empty, judge whether a matched schema exists in `do-dbs`. 
    
        - If yes, continue to filter at the table level.
        - If not, ignore it and exit.

    - If `do-dbs` is empty, and `ignore-dbs` is not empty, judge whether a matched schema exits in `ignore-dbs`. 
    
        - If yes, ignore it and exit.
        - If not, continue to filter at the table level.

    - If both `do-dbs` and `ignore-dbs` are empty, continue to filter at the table level.

2. Filter at the table level:
    
    1. If `do-tables` is not empty, judge whether a matched rule exists in `do-tables`.  
    
        - If yes, exit and execute the statement.
        - If not, continue to the next step.

    2. If `ignore tables` is not empty, judge whether a matched rule exists in `ignore-tables`.
    
        - If yes, ignore it and exit.
        - If not, continue to the next step.

    3. If `do-tables` is not empty, ignore it and exit. Otherwise, exit and execute the statement.

## Filtering rules of binlog events

```
# table level
user-filter-1:
    schema-pattern: "test_*"     # `schema-pattern`/`table-pattern` uses the wildcard matching rule.
    table-pattern: "t_*"
    events: ["truncate table", "drop table"]
    sql-pattern: ["^DROP\\s+PROCEDURE", "^CREATE\\s+PROCEDURE"]
    action: Ignore

# schema level
user-filter-2:
    schema-pattern: "test_*"
    events: ["All DML"]
    action: Do
```

Description: Configures the filtering rules for binlog events and DDL SQL statements of the upstream tables that match `schema-pattern`/`table-pattern`.

- `events`: the binlog event array

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

- `sql-pattern` 

    - Filters a specific DDL SQL statement. 
    - The matching rule supports using an regular expression, for example, `"^DROP\\s+PROCEDURE"`.
    
> **Note:**
>
> If `sql-pattern` is empty, no filtering operation is performed. For the filtering rules, see the `action` description.

- `action` 

    - String (`Do`/`Ignore`)
    - For rules that match `schema-pattern`/`table-pattern`, judge whether the DDL statement is in the events of the rule or `sql-pattern`. 
        
        - Black list: If `action = Ignore`, execute `Ignore`; otherwise execute `Do`.
        - White list: If `action = Ignore`, execute `Do`; otherwise execute `Ignore`.

## Column mapping rule

```
instance-1:
    schema-pattern: "test_*"    # `schema-pattern`/`table-pattern` uses the wildcard matching rule
    table-pattern: "t_*"
    expression: "partition id"
    source-column: "id"
    target-column: "id"
    arguments: ["1", "test_", "t_"]
instance-2:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    expression: "partition id"
    source-column: "id"
    target-column: "id"
    arguments: ["2", "test_", "t_"]
```

Description: the rules for mapping the columns of `schema-pattern`/`table-pattern` matched tables in upstream database instances. It is used to resolve the conflicts of auto-increment primary keys of sharded tables.

- `source-column`, `target-column`: Uses `expression` to compute the data of `source-column` as the data of `target-column`.

- `expression`: The expression used to convert the column data. Currently, only the following built-in expression is supported:
        
    - `partition id`
        
        - You need to set `arguments` to `[instance_id, prefix of schema, prefix of table]`.  
        
            - schema name = arguments[1] + schema ID（suffix of schema）; schema ID == suffix of schema
            - table name = argument[2] + table ID（suffix of table）; table ID == suffix of table
            - If argument[0] == "", the partition ID takes up 0 bit in the figure below; otherwise, it takes up 4 bits (by default)
            - If argument[1] == "", the schema ID takes up 0 bit in the figure below; otherwise, it takes up 7 bits (by default)
            - If argument[2] == "", the table ID takes up 0 bit in the figure below; otherwise, it takes up 8 bits (by default)
            - The origin ID is the value of the auto-increment ID column of a row in the table

            ![partition ID](../media/partition-id.png)

        - Restrictions:
        
            - It is only applicable to the bigint column.
            - The instance ID value should be (>= 0, <= 15) (4 bits by default)
            - The schema ID value should be (>= 0, <= 127) (7 bits by default)
            - The table ID value should be (>= 0, <= 255) (8 bits by default)
            - The origin ID value should be (>= 0, <= 17592186044415) (44 bits by default)
