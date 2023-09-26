---
title: Best Practices of Data Migration in the Shard Merge Scenario
summary: Learn the best practices of data migration in the shard merge scenario.
aliases: ['/docs/tidb-data-migration/dev/shard-merge-best-practices/']
---

# Best Practices of Data Migration in the Shard Merge Scenario

This document describes the features and limitations of [TiDB Data Migration](https://github.com/pingcap/dm) (DM) in the shard merge scenario and provides a data migration best practice guide for your application (the default "pessimistic" mode is used).

## Use a separate data migration task

In the [Merge and Migrate Data from Sharded Tables](/dm/feature-shard-merge-pessimistic.md#principles) document, the definition of "sharding group" is given: A sharding group consists of all upstream tables that need to be merged and migrated into the same downstream table.

The current sharding DDL mechanism has some [usage restrictions](/dm/feature-shard-merge-pessimistic.md#restrictions) to coordinate the schema changes brought by DDL operations in different sharded tables. If these restrictions are violated due to unexpected reasons, you need to [handle sharding DDL locks manually in DM](/dm/manually-handling-sharding-ddl-locks.md), or even redo the entire data migration task.

To mitigate the impact on data migration when an exception occurs, it is recommended to merge and migrate each sharding group as a separate data migration task. **This might enable that only a small number of data migration tasks need to be handled manually while others remain unaffected.**

## Handle sharding DDL locks manually

You can easily conclude from [Merge and Migrate Data from Sharded Tables](/dm/feature-shard-merge-pessimistic.md#principles) that DM's sharding DDL lock is a mechanism for coordinating the execution of DDL operations to the downstream from multiple upstream sharded tables.

Therefore, when you find any sharding DDL lock on `DM-master` through `shard-ddl-lock` command, or any `unresolvedGroups` or `blockingDDLs` on some DM-workers through `query-status` command, do not rush to manually release the sharding DDL lock through `shard-ddl-lock unlock` commands.

Instead, you can:

- Follow the corresponding manual solution to handle the scenario if the failure of automatically releasing the sharding DDL lock is one of the [listed abnormal scenarios](/dm/manually-handling-sharding-ddl-locks.md#supported-scenarios).
- Redo the entire data migration task if it is an unsupported scenario: First, empty the data in the downstream database and the `dm_meta` information associated with the migration task; then, re-execute the full and incremental data replication.

## Handle conflicts between primary keys or unique indexes across multiple sharded tables

Data from multiple sharded tables might cause conflicts between the primary keys or unique indexes. You need to check each primary key or unique index based on the sharding logic of these sharded tables. The following are three cases related to primary keys or unique indexes:

- Shard key: Usually, the same shard key only exists in one sharded table, which means no data conflict is caused on shard key.
- Auto-increment primary key: The auto-increment primary key of each sharded tables counts separately, so their range might overlap. In this case, you need to refer to the next section [Handle conflicts of auto-increment primary key](/dm/shard-merge-best-practices.md#handle-conflicts-of-auto-increment-primary-key) to solve it.
- Other primary keys or unique indexes: you need to analyze them based on the business logic. If data conflict, you can also refer to the next section [Handle conflicts of auto-increment primary key](/dm/shard-merge-best-practices.md#handle-conflicts-of-auto-increment-primary-key) to solve it.

## Handle conflicts of auto-increment primary key

This section introduces two recommended solutions to handle conflicts of auto-increment primary key.

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

1. Before the full data migration, create a table in the downstream database for merging and migrating data, and modify the `PRIMARY KEY` attribute of the `auto_pk_c1` column to normal index.

    ```sql
    CREATE TABLE `tbl_no_pk_2` (
      `auto_pk_c1` bigint(20) NOT NULL,
      `uk_c2` bigint(20) NOT NULL,
      `content_c3` text,
      INDEX (`auto_pk_c1`),
      UNIQUE KEY `uk_c2` (`uk_c2`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1
    ```

2. Add the following configuration in `task.yaml` to skip the check of auto-increment primary key conflict:

    ```yaml
    ignore-checking-items: ["auto_increment_ID"]
    ```

3. Start the full and incremental data replication task.

4. Run `query-status` to verify whether the data migration task is successfully processed and whether the data from the upstream has already been merged and migrated to the downstream database.

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

1. Before the full data migration, create a table in the downstream database for merging and migrating data. Do not specify the `PRIMARY KEY` attribute for the `auto_pk_c1` column, but use the `auto_pk_c1` and `uuid_c2` columns to make up a composite primary key.

    ```sql
    CREATE TABLE `tbl_multi_pk_c2` (
      `auto_pk_c1` bigint(20) NOT NULL,
      `uuid_c2` bigint(20) NOT NULL,
      `content_c3` text,
      PRIMARY KEY (`auto_pk_c1`,`uuid_c2`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1
    ```

2. Start the full and incremental data migration task.

3. Run `query-status` to verify whether the data migration task is successfully processed and whether the data from upstream has already been merged and migrated to the downstream database.

## Special processing when the upstream RDS contains sharded tables

If the upstream data source is an RDS and it contains sharded tables, the table names in MySQL binlog might be invisible when connecting to a SQL client. For example, if the upstream is a UCloud distributed database, the table name in the binlog might have an extra prefix `_0001`. Therefore, you need to configure [table routing](/dm/dm-table-routing.md) based on the table names in binlog, instead of those in the SQL client.

## Create/drop tables in the upstream

In [Merge and Migrate Data from Sharded Tables](/dm/feature-shard-merge-pessimistic.md#principles), it is clear that the coordination of sharding DDL lock depends on whether the downstream database receives the DDL statements of all upstream sharded tables. In addition, DM currently **does not support** dynamically creating or dropping sharded tables in the upstream. Therefore, to create or drop sharded tables in the upstream, it is recommended to perform the following steps.

### Create sharded tables in the upstream

If you need to create a new sharded table in the upstream, perform the following steps:

1. Wait for the coordination of all executed sharding DDL in the upstream sharded tables to finish.

2. Run `stop-task` to stop the data migration task.

3. Create a new sharded table in the upstream.

4. Make sure that the configuration in the `task.yaml` file allows the newly added sharded table to be merged in one downstream table with other existing sharded tables.

5. Run `start-task` to start the task.

6. Run `query-status` to verify whether the data migration task is successfully processed and whether the data from upstream has already been merged and migrated to the downstream database.

### Drop sharded tables in the upstream

If you need to drop a sharded table in the upstream, perform the following steps:

1. Drop the sharded table, run [`SHOW BINLOG EVENTS`](https://dev.mysql.com/doc/refman/8.0/en/show-binlog-events.html) to fetch the `End_log_pos` corresponding to the `DROP TABLE` statement in the binlog events, and mark it as *Pos-M*.

2. Run `query-status` to fetch the position (`syncerBinlog`) corresponding to the binlog event that has been processed by DM, and mark it as *Pos-S*.

3. When *Pos-S* is greater than *Pos-M*, it means that DM has processed all of the `DROP TABLE` statements, and the data of the table before dropping has been migrated to the downstream, so the subsequent operation can be performed. Otherwise, wait for DM to finish migrating the data.

4. Run `stop-task` to stop the task.

5. Make sure that the configuration in the `task.yaml` file ignores the dropped sharded table in the upstream.

6. Run `start-task` to start the task.

7. Run `query-status` to verify whether the data migration task is successfully processed.

## Speed limits and traffic flow control

When data from multiple upstream MySQL or MariaDB instances is merged and migrated to the same TiDB cluster in the downstream, every DM-worker corresponding to each upstream instance executes full and incremental data replication concurrently. This means that the default degree of concurrency (`pool-size` in full data migration and `worker-count` in incremental data replication) accumulates as the number of DM-workers increases, which might overload the downstream database. In this case, you need to conduct a preliminary performance analysis based on TiDB and DM monitoring metrics and adjust the value of each concurrency parameter. In the future, DM is expected to support partially automated traffic flow control.
