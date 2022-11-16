---
title: Manage Table Schemas of Tables to Be Migrated Using TiDB Data Migration
summary: Learn how to manage the schema of the table to be migrated in DM.
---

# Manage Table Schemas of Tables to Be Migrated Using TiDB Data Migration

This document describes how to manage the schema of the table in DM during migration using [dmctl](/dm/dmctl-introduction.md).

When DM performs incremental replication, it first reads the upstream binlog, then creates SQL statements and executes them in the downstream. However, the upstream binlog does not contain the complete table schema. To generate the SQL statements, DM maintains internally the schema information of the table to be migrated. This is called the internal table schema.

To deal with some special occasions, or to handle migration interruptions caused by mismatch of the table schemas, DM provides the `binlog-schema` command to obtain, modify, and delete the internal table schema.

## Implementation principles

The internal table schema comes from the following sources:

- For full data migration (`task-mode=all`), the migration task goes through three stages: dump/load/sync, which means full export, full import, and incremental replication. In the dump stage, DM exports the table schema information along with the data and automatically creates the corresponding table in the downstream. In the sync stage, this table schema is used as the starting table scheme for incremental replication.
- In the sync stage, when DM handles DDL statements such as `ALTER TABLE`, it updates the internal table schema at the same time.
- If the task is an incremental migration (`task-mode=incremental`), in which the downstream has completed creating the table to be migrated, DM obtains the table schema information from the downstream database. This behavior varies with DM versions.

For incremental replication, schema maintenance is complicated. During the whole data replication, the following four table schemas are involved. These schemas might be the consistent or inconsistent with one another:

![schema](/media/dm/operate-schema.png)

* The upstream table schema at the current time, identified as `schema-U`.
* The table schema of the binlog event currently being consumed by DM, identified as `schema-B`. This schema corresponds to the upstream table schema at a historical time.
* The table schema currently maintained in DM (the schema tracker component), identified as `schema-I`.
* The table schema in the downstream TiDB cluster, identified as `schema-D`.

In most cases, the preceding four table schemas are consistent.

When the upstream database performs a DDL operation to change the table schema, `schema-U` is changed. By applying the DDL operation to the internal schema tracker component and the downstream TiDB cluster, DM updates `schema-I` and `schema-D` in an orderly manner to keep them consistent with `schema-U`. Therefore, DM can then normally consume the binlog event corresponding to the `schema-B` table schema. That is, after the DDL operation is successfully migrated, `schema-U`, `schema-B`, `schema-I`, and `schema-D` are still consistent.

Note the following situations that might cause inconsistency:

- During the migration with [optimistic mode sharding DDL support](/dm/feature-shard-merge-optimistic.md) enabled, the `schema-D` of the downstream table might be inconsistent with the `schema-B` and `schema-I` of some upstream sharded tables. In such cases, DM still keeps `schema-I` and `schema-B` consistent to ensure that the binlog event corresponding to DML can be parsed normally.

- When the downstream table has more columns than the upstream table, `schema-D` might be inconsistent with `schema-B` and `schema-I`. In the full data migration (`task-mode=all`), DM automatically handles inconsistency. In the incremental migration (`task-mode=incremental`), because the task is on a first start and there is no internal schema information yet, DM automatically reads the downstream schema (`schema-D`) and updates `schema-I` (this behavior varies with DM versions). After that, if DM uses `schema-I` to parse `schema-B`'s binlog, it will report `Column count doesn't match value count` error. For details, refer to [Migrate Data to a Downstream TiDB Table with More Columns](/migrate-with-more-columns-downstream.md).

You can run the `binlog-schema` command to obtain, modify, or delete the `schema-I` table schema maintained in DM.

> **Note:**
>
> The `binlog-schema` command is supported only in DM v6.0 or later versions. For earlier versions, you must use the `operate-schema` command.

## Command

{{< copyable "shell-regular" >}}

```bash
help binlog-schema
```

```
manage or show table schema in schema tracker

Usage:
  dmctl binlog-schema [command]

Available Commands:
  delete      delete table schema structure
  list        show table schema structure
  update      update tables schema structure

Flags:
  -h, --help   help for binlog-schema

Global Flags:
  -s, --source strings   MySQL Source ID.

Use "dmctl binlog-schema [command] --help" for more information about a command.
```

> **Note:**
>
> - Because a table schema might change during data migration, to obtain a predictable table schema, currently the `binlog-schema` command can be used only when the data migration task is in the `Paused` state.
> - To avoid data loss due to mishandling, it is **strongly recommended** to get and backup the table schema firstly before you modify the schema.

## Parameters

* `delete`: Deletes the table schema.
* `list`: Lists the table schema.
* `update`: Updates the table schema.
* `-s` or `--source`:
    - Required.
    - Specifies the MySQL source that the operation is applied to.

## Usage example

### Get the table schema

To get the table schema, run the `binlog-schema list` command:

```bash
help binlog-schema list
```

```
show table schema structure

Usage:
  dmctl binlog-schema list <task-name> <database> <table> [flags]

Flags:
  -h, --help   help for list

Global Flags:
  -s, --source strings   MySQL Source ID.
```

If you want to get the table schema of the ``` `db_single`.`t1` ``` table corresponding to the `mysql-replica-01` MySQL source in the `db_single` task, run the following command:

{{< copyable "shell-regular" >}}

```bash
binlog-schema list -s mysql-replica-01 task_single db_single t1
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

### Update the table schema

To update the table schema, run the `binlog-schema update` command:

{{< copyable "shell-regular" >}}

```bash
help binlog-schema update
```

```
update tables schema structure

Usage:
  dmctl binlog-schema update <task-name> <database> <table> [schema-file] [flags]

Flags:
      --flush         flush the table info and checkpoint immediately (default true)
      --from-source   use the schema from upstream database as the schema of the specified tables
      --from-target   use the schema from downstream database as the schema of the specified tables
  -h, --help          help for update
      --sync          sync the table info to master to resolve shard ddl lock, only for optimistic mode now (default true)

Global Flags:
  -s, --source strings   MySQL Source ID.
```

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

### Delete the table schema

To delete the table schema, run the `binlog-schema delete` command:

```bash
help binlog-schema delete
```

```
delete table schema structure

Usage:
  dmctl binlog-schema delete <task-name> <database> <table> [flags]

Flags:
  -h, --help   help for delete

Global Flags:
  -s, --source strings   MySQL Source ID.
```

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
binlog-schema delete -s mysql-replica-01 task_single db_single t1
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
