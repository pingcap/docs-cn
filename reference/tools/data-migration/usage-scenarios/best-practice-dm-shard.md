---
title: Best Practices of Data Migration in the Shard Merge Scenario
summary: Learn the best practices of data migration in the shard merge scenario.
category: reference
---
# Best Practices of Data Migration in the Shard Merge Scenario

This document describes the features and limitations of [TiDB Data Migration](https://github.com/pingcap/dm) (DM) in the shard merge scenario and provides a data migration best practice guide for your application.

## Use a separate data migration task

In the [Merge and Replicate Data from Sharded Tables](/reference/tools/data-migration/features/shard-merge.md#principles) document, the definition of "sharding group" is given: A sharding group consists of all upstream tables that need to be merged and replicated into the same downstream table.

The current sharding DDL mechanism has some [usage restrictions](/reference/tools/data-migration/features/shard-merge.md#restrictions) to coordinate the schema changes brought by DDL operations in different sharded tables. If these restrictions are violated due to unexpected reasons, you need to [handle sharding DDL locks manually in DM](/reference/tools/data-migration/features/manually-handling-sharding-ddl-locks.md), or even redo the entire data migration task.

To mitigate the impact on data migration when an exception occurs, it is recommended to merge and replicate each sharding group as a separate data migration task. **This might enable that only a small number of data migration tasks need to be handled manually while others remain unaffected.**

## Handle sharding DDL locks manually

You can easily conclude from [Merge and Replicate Data from Sharded Tables](/reference/tools/data-migration/features/shard-merge.md#principles) that DM's sharding DDL lock is a mechanism for coordinating the execution of DDL operations to the downstream from multiple upstream sharded tables.

Therefore, when you find any sharding DDL lock on `DM-master` through `show-ddl-locks` command, or any `unresolvedGroups` or `blockingDDLs` on some DM-workers through `query-status` command, do not rush to manually release the sharding DDL lock through `unlock-ddl-lock` or `break-ddl-lock` commands.

Instead, you can:

- Follow the corresponding manual solution to handle the scenario if the failure of automatically releasing the sharding DDL lock is one of the [listed abnormal scenarios](/reference/tools/data-migration/features/manually-handling-sharding-ddl-locks.md#supported-scenarios).
- Redo the entire data migration task if it is an unsupported scenario: First, empty the data in the downstream database and the `dm_meta` information associated with the migration task; then, re-execute the full and incremental data migration.

## Handle conflicts of auto-increment primary key

DM offers the [column mapping](/reference/tools/data-migration/features/overview.md#column-mapping) feature to handle conflicts that might occur in merging the `bigint` type of auto-increment primary key. However, it is **strongly discouraged** to choose this approach. If it is acceptable in the production environment, the following two alternatives are recommended.

### Remove the `PRIMARY KEY` attribute from the column

Assume that the upstream schemas are as follows:

```sql
CREATE TABLE `tbl_no_pk` (
  `auto_pk_c1` bigint(20) NOT NULL,
  `uk_c2` bigint(20) NOT NULL,
  `content_c3` text,
  PRIMARY KEY (`auto_pk_c1`),
  UNIQUE KEY `uk_c2` (`uk_c2`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

If the following requirements are satisfied:

- The `auto_pk_c1` column has no impact on the application and does not depend on the column's `PRIMARY KEY` attribute.
- The `uk_c2` column has the `UNIQUE KEY` attribute, and it is globally unique in all upstream sharded tables.

Then you can perform the following steps to fix the `ERROR 1062 (23000): Duplicate entry '***' for key 'PRIMARY'` error that is possibly caused by the `auto_pk_c1` column when you merge sharded tables.

1. Before the full data migration, create a table in the downstream database for merging and replicating data, and modify the `PRIMARY KEY` attribute of the `auto_pk_c1` column to normal index.

    ```sql
    CREATE TABLE `tbl_no_pk_2` (
      `auto_pk_c1` bigint(20) NOT NULL,
      `uk_c2` bigint(20) NOT NULL,
      `content_c3` text,
      INDEX (`auto_pk_c1`),
      UNIQUE KEY `uk_c2` (`uk_c2`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1
    ```

2. Start the full and incremental data migration task.

3. Run `query-status` to verify whether the data migration task is successfully processed and whether the data from the upstream has already been merged and replicated to the downstream database.

### Use a composite primary key

Assume that the upstream schemas are as follows:

```sql
CREATE TABLE `tbl_multi_pk` (
  `auto_pk_c1` bigint(20) NOT NULL,
  `uuid_c2` bigint(20) NOT NULL,
  `content_c3` text,
  PRIMARY KEY (`auto_pk_c1`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

If the following requirements are satisfied:

* The application does not depend on the `PRIMARY KEY` attribute of the `auto_pk_c1` column.
* The composite primary key that consists of the `auto_pk_c1` and `uuid_c2` columns is globally unique.
* It is acceptable to use a composite primary key in the application.

Then you can perform the following steps to fix the `ERROR 1062 (23000): Duplicate entry '***' for key 'PRIMARY'` error that is possibly caused by the `auto_pk_c1` column when you merge sharded tables.

1. Before the full data migration, create a table in the downstream database for merging and replicating data. Do not specify the `PRIMARY KEY` attribute for the `auto_pk_c1` column, but use the `auto_pk_c1` and `uuid_c2` columns to make up a composite primary key.

    ```sql
    CREATE TABLE `tbl_multi_pk_c2` (
      `auto_pk_c1` bigint(20) NOT NULL,
      `uuid_c2` bigint(20) NOT NULL,
      `content_c3` text,
      PRIMARY KEY (`auto_pk_c1`,`uuid_c2`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1
    ```

2. Start the full and incremental data migration task.

3. Run `query-status` to verify whether the data migration task is successfully processed and whether the data from upstream has already been merged and replicated to the downstream database.

## Create/drop tables in the upstream

In [Merge and Replicate Data from Sharded Tables](/reference/tools/data-migration/features/shard-merge.md#principles), it is clear that the coordination of sharding DDL lock depends on whether the downstream database receives the DDL statements of all upstream sharded tables. In addition, DM currently **does not support** dynamically creating or dropping sharded tables in the upstream. Therefore, to create or drop sharded tables in the upstream, it is recommended to perform the following steps.

### Create sharded tables in the upstream

If you need to create a new sharded table in the upstream, perform the following steps:

1. Wait for the coordination of all executed sharding DDL in the upstream sharded tables to finish.

2. Run `stop-task` to stop the data migration task.

3. Create a new sharded table in the upstream.

4. Make sure that the configuration in the `task.yaml` file allows the newly added sharded table to be merged in one downstream table with other existing sharded tables.

5. Run `start-task` to start the task.

6. Run `query-status` to verify whether the data migration task is successfully processed and whether the data from upstream has already been merged and replicated to the downstream database.

### Drop sharded tables in the upstream

If you need to drop a sharded table in the upstream, perform the following steps:

1. Drop the sharded table, run [`SHOW BINLOG EVENTS`](https://dev.mysql.com/doc/refman/5.7/en/show-binlog-events.html) to fetch the `End_log_pos` corresponding to the `DROP TABLE` statement in the binlog events, and mark it as *Pos-M*.

2. Run `query-status` to fetch the position (`syncerBinlog`) corresponding to the binlog event that has been processed by DM, and mark it as *Pos-S*.

3. When *Pos-S* is greater than *Pos-M*, it means that DM has processed all of the `DROP TABLE` statements, and the data of the table before dropping has been replicated to the downstream, so the subsequent operation can be performed. Otherwise, wait for DM to finish replicating the data.

4. Run `stop-task` to stop the task.

5. Make sure that the configuration in the `task.yaml` file ignores the dropped sharded table in the upstream.

6. Run `start-task` to start the task.

7. Run `query-status` to verify whether the data migration task is successfully processed.

## Speed limits and traffic flow control

When data from multiple upstream MySQL or MariaDB instances is merged and replicated to the same TiDB cluster in the downstream, every DM-worker corresponding to each upstream instance executes full and incremental data migration concurrently. This means that the default degree of concurrency (`pool-size` in full data migration and `worker-count` in incremental data migration) accumulates as the number of DM-workers increases, which might overload the downstream database. In this case, you need to conduct a preliminary performance analysis based on TiDB and DM monitoring metrics and adjust the value of each concurrency parameter. In the future, DM is expected to support partially automated traffic flow control.
