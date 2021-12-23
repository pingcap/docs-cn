---
title: Migration when There Are More Columns in the Downstream TiDB Table
summary: Learn how to use Data Migration (DM) to migrate tables when there are more columns in the downstream table schema.
---

# Migration when There Are More Columns in the Downstream TiDB Table

This document describes how to migrate tables using DM when there are more columns in the downstream TiDB table schema than the upstream table schema.

## The table shcema of the data source

This document uses the follwing data source example:

| Schema | Tables |
|:------|:------|
| user  | information, log |
| store | store_bj, store_tj |
| log   | messages |

## Migration requirements

Create a customized table `log.messages` in TiDB. Its schema contains not only all the columns in the `log.messages` table of the data source, but also additional columns. In this case, migrate the table `log.messages` of the data source to the table `log.messages` of the TiDB cluster.

> **Note:**
>
> * The columns that only exist in the downstream TiDB must be given a default value or allowed to be `NULL`.
> * For tables that are being migrated by DM, you can directly add new columns in the downstream TiDB that are given a default value or allowed to be `NULL`. Adding such new columns does not affect the data migration.

## Only migrate incremental data to TiDB and the downstream TiDB table has more columns

If your migration task contains full data migration, the task can operate normally. If you have already used other tools to do full data migration and this migration task only uses DM to replicate incremental data, refer to [Migrate Incremental Data to TiDB](/dm/usage-scenario-incremental-migration.md#create-a-replication-task) to create a data migration task. At the same time, you need to manually configure the table schema in DM for MySQL binlog parsing.

Otherwise, after creating the task, the following data migration errors occur when you execute the query-status` command:

```
"errors": [
    {
        "ErrCode": 36027,
        "ErrClass": "sync-unit",
        "ErrScope": "internal",
        "ErrLevel": "high",
        "Message": "startLocation: [position: (mysql-bin.000001, 2022), gtid-set:09bec856-ba95-11ea-850a-58f2b4af5188:1-9 ], endLocation: [position: (mysql-bin.000001, 2022), gtid-set: 09bec856-ba95-11ea-850a-58f2b4af5188:1-9]: gen insert sqls failed, schema: log, table: messages: Column count doesn't match value count: 3 (columns) vs 2 (values)",
        "RawCause": "",
        "Workaround": ""
    }
]
```

The reason for the above errors is that when DM migrates the binlog event, if DM has not maintained internally the table schema corresponding to that table, DM tries to use the current table schema in the downstream to parse the binlog event and generate the corresponding DML statement. If the number of columns in the binlog event is inconsistent with the number of columns in the downstream table schema, the above error might occur.

In such cases, you can execute the [`operate-schema`](/dm/dm-manage-schema.md) command to specify for the table a table schema that matches the binlog event. If you are migrating sharded tables, you need to configure the table schema in DM for parsing MySQL binlog for each sharded tables according to the following steps:

1. Specify the table schema for the table `log.messages` to be migrated in the data source. The table schema needs to correspond to the data of the binlog event to be replicated by DM. Then save the `CREATE TABLE` table schema statement in a file. For example, save the following table schema in the `log.messages.sql` file:

    ```sql
    CREATE TABLE `messages` (
      `id` int(11) NOT NULL,
      `message` varchar(255) DEFAULT NULL,
      PRIMARY KEY (`id`)
    )
    ```

2. Execute the [`operate-schema`](/dm/dm-manage-schema.md) command to set the table schema. At this time, the task should be in the `Paused` state because of the above error.

    {{< copyable "shell-regular" >}}

    ```bash
    tiup dmctl --master-addr <master-addr> operate-schema set -s mysql-01 task-test -d log -t message log.message.sql
    ```    

3. Execute the [`resume-task`](/dm/dm-resume-task.md) command to resume the `Paused` task.

4. Execute the [`query-status`](/dm/dm-query-status.md) command to check whether the data migration task is running normally.
