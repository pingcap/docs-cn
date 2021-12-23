---
title: Manage Table Schemas of Tables to be Migrated
summary: Learn how to manage the schema of the table to be migrated in DM.
aliases: ['/tidb-data-migration/dev/manage-schema/']
---

# Manage Table Schemas of Tables to be Migrated

This document describes how to manage the schema of the table in DM during migration using [dmctl](/dm/dmctl-introduction.md).

## Implementation principles

When you migrate tables using DM, DM performs the following operations on the table schema:

- For full export and import, DM directly exports the upstream table schema of the current time to SQL files and applies the table schema to the downstream.

- For incremental replication, the whole data link contains the following table schemas, which might be the same or different:

    ![schema](/media/dm/operate-schema.png)

    * The upstream table schema at the current time, identified as `schema-U`.
    * The table schema of the binlog event currently being consumed by DM, identified as `schema-B`. This schema corresponds to the upstream table schema at a historical time.
    * The table schema currently maintained in DM (the schema tracker component), identified as `schema-I`.
    * The table schema in the downstream TiDB cluster, identified as `schema-D`.

    In most cases, the four table schemas above are the same.

When the upstream database performs a DDL operation to change the table schema, `schema-U` is changed. By applying the DDL operation to the internal schema tracker component and the downstream TiDB cluster, DM updates `schema-I` and `schema-D` in an orderly manner to keep them consistent with `schema-U`. Therefore, DM can then normally consume the binlog event corresponding to the `schema-B` table schema. That is, after the DDL operation is successfully migrated, `schema-U`, `schema-B`, `schema-I`, and `schema-D` are still consistent.

However, during the migration with [optimistic mode sharding DDL support](/dm/feature-shard-merge-optimistic.md) enabled, the `schema-D` of the downstream table might be inconsistent with the `schema-B` and `schema-I` of some upstream sharded tables. In such cases, DM still keeps `schema-I` and `schema-B` consistent to ensure that the binlog event corresponding to DML can be parsed normally.

In addition, in some scenarios (such as when the downstream table has more columns than the upstream table), `schema-D` might be inconsistent with `schema-B` and `schema-I`.

To support the scenarios mentioned above and handle other migration interruptions caused by schema inconsistency, DM provides the `operate-schema` command to obtain, modify, and delete the `schema-I` table schema maintained in DM.

## Command

{{< copyable "shell-regular" >}}

```bash
help operate-schema
```

```
`get`/`set`/`remove` the schema for an upstream table.

Usage:
  dmctl operate-schema <operate-type> <-s source ...> <task-name | task-file> <-d database> <-t table> [schema-file] [--flush] [--sync] [flags]

Flags:
  -d, --database string   database name of the table
      --flush             flush the table info and checkpoint immediately
  -h, --help              help for operate-schema
      --sync              sync the table info to master to resolve shard ddl lock, only for optimistic mode now
  -t, --table string      table name

Global Flags:
  -s, --source strings   MySQL Source ID.
```

> **Note:**
>
> - Because a table schema might change during data migration, to obtain a predictable table schema, currently the `operate-schema` command can be used only when the data migration task is in the `Paused` state.
> - To avoid data loss due to mishandling, it is **strongly recommended** to get and backup the table schema firstly before you modify the schema.

## Parameters

* `operate-type`:
    - Required.
    - Specifies the type of operation on the schema. The optional values are `get`, `set`, and `remove`.
* `-s`:
    - Required.
    - Specifies the MySQL source that the operation is applied to.
* `task-name | task-file`:
    - Required.
    - Specifies the task name or task file path.
* `-d`:
    - Required.
    - Specifies the name of the upstream database the table belongs to.
* `-t`:
    - Required.
    - Specifies the name of the upstream table corresponding to the table.
* `schema-file`:
    - Required when the operation type is `set`. Optional for other operation types.
    - The table schema file to be set. The file content should be a valid `CREATE TABLE` statement.
* `--flush`:
    - Optional.
    - Writes the schema to the checkpoint so that DM can load it after restarting the task.
    - The default value is `true`.
* `--sync`:
    - Optional. Only used when an error occurs in the optimistic sharding DDL mode.
    - Updates the optimistic sharding metadata with this schema.

## Usage example

### Get the table schema

If you want to get the table schema of the ``` `db_single`.`t1` ``` table corresponding to the `mysql-replica-01` MySQL source in the `db_single` task, run the following command:

{{< copyable "shell-regular" >}}

```bash
operate-schema get -s mysql-replica-01 task_single -d db_single -t t1
```

```
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "CREATE TABLE `t1` ( `c1` int(11) NOT NULL, `c2` int(11) DEFAULT NULL, PRIMARY KEY (`c1`)) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin",
            "source": "mysql-replica-01",
            "worker": "127.0.0.1:8262"
        }
    ]
}
```

### Set the table schema

If you want to set the table schema of the ``` `db_single`.`t1` ``` table corresponding to the `mysql-replica-01` MySQL source in the `db_single` task as follows:

```sql
CREATE TABLE `t1` (
    `c1` int(11) NOT NULL,
    `c2` bigint(11) DEFAULT NULL,
    PRIMARY KEY (`c1`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin
```

Save the `CREATE TABLE` statement above as a file (for example, `db_single.t1-schema.sql`), and run the following command:

{{< copyable "shell-regular" >}}

```bash
operate-schema set -s mysql-replica-01 task_single -d db_single -t t1 db_single.t1-schema.sql
```

```
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "mysql-replica-01",
            "worker": "127.0.0.1:8262"
        }
    ]
}
```

### Delete table schema

> **Note:**
>
> After the table schema maintained in DM is deleted, if a DDL/DML statement related to this table needs to be migrated to the downstream, DM will try to get the table schema from the following three sources in an orderly manner:
>
> * The `table_info` field in the checkpoint table
> * The meta information in the optimistic sharding DDL
> * The corresponding table in the downstream TiDB

If you want to delete the table schema of the ``` `db_single`.`t1` ``` table corresponding to the `mysql-replica-01` MySQL source in the `db_single` task, run the following command:

{{< copyable "shell-regular" >}}

```bash
operate-schema remove -s mysql-replica-01 task_single -d db_single -t t1
```

```
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "mysql-replica-01",
            "worker": "127.0.0.1:8262"
        }
    ]
}
```
