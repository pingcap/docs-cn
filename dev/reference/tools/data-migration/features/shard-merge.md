---
title: Merge and Replicate Data from Sharded Tables
summary: Learn how DM merges and replicates data from sharded tables.
category: reference
aliases: ['/docs/tools/dm/shard-merge/']
---

# Merge and Replicate Data from Sharded Tables

This document introduces the sharding support feature provided by Data Migration (DM). This feature allows you to merge and replicate the data of tables with the same table schema in the upstream MySQL or MariaDB instances into one same table in the downstream TiDB. It supports not only replicating the upstream DML statements, but also coordinating to replicate the table schema change using DDL statements in multiple upstream sharded tables.

> **Note:**
>
> To merge and replicate data from the sharded tables, you must configure the `is-sharding: true` item in the task configuration file.

### Restrictions

DM has the following sharding DDL usage restrictions:

- In a logical **sharding group** (composed of all sharded tables that need to be merged and replicated into one same downstream table), the same DDL statements must be executed in the same order in all upstream sharded tables (the schema name and the table name can be different), and the next DDL statement cannot be executed unless the current DDL operation is completely finished.
    - For example, if you add `column A` to `table_1` before you add `column B`, then you cannot add `column B` to `table_2` before you add `column A`. Executing the DDL statements in a different order is not supported.
- For each sharding group, it is recommended to use one independent task to perform the replication.
    - If multiple sharding groups exist in a task, you cannot start to execute the DDL statements in other sharding groups until the DDL statements in one sharding group has been replicated successfully.
- In a sharding group, the corresponding DDL statements should be executed in all upstream sharded tables.
    - For example, if DDL statements are not executed on one or more upstream sharded tables corresponding to `DM-worker-2`, then other DM-workers that have executed the DDL statements pause their replication task and wait for `DM-worker-2` to receive the upstream DDL statements.
- The sharding group replication task does not support `DROP DATABASE`/`DROP TABLE`.
    - The Syncer unit in DM-worker automatically ignores the `DROP DATABASE`/`DROP TABLE` statement of upstream sharded tables.
- The sharding group replication task supports `RENAME TABLE`, but with the following limitations (Online DDL is supported in another solution):
    - A table can only be renamed to a new name that is not used by any other table.
    - A single `RENAME TABLE` statement can only involve a single `RENAME` operation.
- The table schema of each sharded table must be the same at the starting point of the incremental replication task, so as to make sure the DML statements of different sharded tables can be replicated into the downstream with a definite table schema, and the subsequent sharding DDL statements can be correctly matched and replicated.
- If you need to change the [table routing](/tools/dm/data-synchronization-features.md#table-routing) rule, you have to wait for the replication of all sharding DDL statements to complete.
    - During the replication of sharding DDL statements, an error is reported if you use `dmctl` to change `router-rules`.
- If you need to `CREATE` a new table to a sharding group where DDL statements are being executed, you have to make sure that the table schema is the same as the newly modified table schema.
    - For example, both the original `table_1` and `table_2` have two columns (a, b) initially, and have three columns (a, b, c) after the sharding DDL operation, so after the replication the newly created table should also have three columns (a, b, c).
- Because the DM-worker that has received the DDL statements will pause the task to wait for other DM-workers to receive their DDL statements, the delay of data replication will be increased.

### Background

Currently, DM uses the binlog in the `ROW` format to perform the replication task. The binlog does not contain the table schema information. When you use the `ROW` binlog to replicate data, if you have not replicated multiple upstream tables into the same downstream table, then there only exist DDL operations of one upstream table that can update the table schema of the downstream table. The `ROW` binlog can be considered to have the nature of self-description. During the replication process, the DML statements can be constructed accordingly with the column values and the downstream table schema.  

However, in the process of merging and replicating sharded tables, if DDL statements are executed on the upstream tables to modify the table schema, then you need to perform extra operations to replicate the DDL statements so as to avoid the inconsistency between the DML statements produced by the column values and the actual downstream table schema.

Here is a simple example:

![shard-ddl-example-1](/media/shard-ddl-example-1.png)

In the above example, the merging process is simplified, where only two MySQL instances exist in the upstream and each instance has only one table. When the replication begins, the table schema version of two sharded tables is marked as `schema V1`, and the table schema version after executing DDL statements is marked as `schema V2`.

Now assume that in the replication process, the binlog data received from the two upstream sharded tables has the following time sequence:

1. When the replication begins, the Syncer unit in DM-worker receives the DML events of `schema V1` from the two sharded tables.
2. At `t1`, the sharding DDL events from instance 1 are received.
3. From `t2` on, the Syncer unit receives the DML events of `schema V2` from instance 1; but from instance 2, it still receives the DML events of `schema V1`.
4. At `t3`, the sharding DDL events from instance 2 are received.
5. From `t4` on, the Syncer unit receives the DML events of `schema V2` from instance 2 as well.

Assume that the DDL statements of sharded tables are not processed during the replication process. After DDL statements of instance 1 are replicated to the downstream, the downstream table schema is changed to `schema V2`. But for instance 2, the Syncer unit in DM-worker is still receiving DML events of `schema V1` from `t2` to `t3`. Therefore, when the DML statements of `schema V1` are replicated to the downstream, the inconsistency between the DML statements and the table schema can cause errors and the data cannot be replicated successfully.

### Principles

This section shows how DM replicates DDL statements in the process of merging sharded tables based on the above example in the [background](#background) section.

![shard-ddl-flow](/media/shard-ddl-flow.png)

In this example, `DM-worker-1` replicates the data from MySQL instance 1 and `DM-worker-2` replicates the data from MySQL instance 2. `DM-master` coordinates the DDL replication among multiple DM-workers. Starting from `DM-worker-1` receiving the DDL statements, the DDL replication process is simplified as follows:

1. `DM-worker-1` receives the DDL statement from MySQL instance 1 at `t1`, pauses the data replication of the corresponding DDL and DML statements, and sends the DDL information to `DM-master`.
2. `DM-master` decides that the replication of this DDL statement needs to be coordinated based on the received DDL information, creates a lock for this DDL statement, sends the DDL lock information back to `DM-worker-1` and marks `DM-worker-1` as the owner of this lock at the same time.
3. `DM-worker-2` continues replicating the DML statement until it receives the DDL statement from MySQL instance 2 at `t3`, pauses the data replication of this DDL statement, and sends the DDL information to `DM-master`.
4. `DM-master` decides that the lock of this DDL statement already exists based on the received DDL information, and sends the lock information directly to `DM-worker-2`.
5. Based on the configuration information when the task is started, the sharded table information in the upstream MySQL instances, and the deployment topology information, `DM-master` decides that it has received this DDL statement of all upstream sharded tables to be merged, and requests the owner of the DDL lock (`DM-worker-1`) to replicate this DDL statement to the downstream.
6. `DM-worker-1` verifies the DDL statement execution request based on the DDL lock information received at Step #2, replicates this DDL statement to the downstream, and sends the results to `DM-master`. If this operation is successful, `DM-worker-1` continues replicating the subsequent (starting from the binlog at `t2`) DML statements.
7. `DM-master` receives the response from the lock owner that the DDL is successfully executed, and requests all other DM-workers (`DM-worker-2`) that are waiting for the DDL lock to ignore this DDL statement and then continue to replicate the subsequent (starting from the binlog at `t4`) DML statements.

The characteristics of DM handling the sharding DDL replication among multiple DM-workers can be concluded as follows:

- Based on the task configuration and DM cluster deployment topology information, a logical sharding group is built in `DM-master` to coordinate DDL replication. The group members are DM-workers that handle each sub-task divided from the replication task).
- After receiving the DDL statement from the binlog event, each DM-worker sends the DDL information to `DM-master`.
- `DM-master` creates or updates the DDL lock based on the DDL information received from each DM-worker and the sharding group information.
- If all members of the sharding group receive a same specific DDL statement, this indicates that all DML statements before the DDL execution on the upstream sharded tables have been completely replicated, and this DDL statement can be executed. Then DM can continue to replicate the subsequent DML statements.
- After being converted by the [table router](/tools/dm/data-synchronization-features.md#table-routing), the DDL statement of the upstream sharded tables must be consistent with the DDL statement to be executed in the downstream. Therefore, this DDL statement only needs to be executed once by the DDL owner and all other DM-workers can ignore this DDL statement.

In the above example, only one sharded table needs to be merged in the upstream MySQL instance corresponding to each DM-worker. But in actual scenarios, there might be multiple sharded tables in multiple sharded schemas to be merged in one MySQL instance. And when this happens, it becomes more complex to coordinate the sharding DDL replication.

Assume that there are two sharded tables, namely `table_1` and `table_2`, to be merged in one MySQL instance:

![shard-ddl-example-2](/media/shard-ddl-example-2.png)

Because data comes from the same MySQL instance, all the data is obtained from the same binlog stream. In this case, the time sequence is as follows:

1. The Syncer unit in DM-worker receives the DML statements of `schema V1` from both sharded tables when the replication begins.
2. At `t1`, the Syncer unit in DM-worker receives the DDL statements of `table_1`.
3. From `t2` to `t3`, the received data includes the DML statements of `schema V2` from `table_1` and the DML statements of `schema V1` from `table_2`.
4. At `t3`, the Syncer unit in DM-worker receives the DDL statements of `table_2`.
5. From `t4` on, the Syncer unit in DM-worker receives the DML statements of `schema V2` from both tables.

If the DDL statements are not processed particularly during the data replication, when the DDL statement of `table_1` is replicated to the downstream and changes the downstream table schema, the DML statement of `schema V1` from `table_2` cannot be replicated successfully. Therefore, within a single DM-worker, a logical sharding group similar to that within `DM-master` is created, except that members of this group are different sharded tables in the same upstream MySQL instance.

But when a DM-worker coordinates the replication of the sharding group within itself, it is not totally the same as that performed by `DM-master`. The reasons are as follows:

- When the DM-worker receives the DDL statement of `table_1`, it cannot pause the replication and needs to continue parsing the binlog to get the subsequent DDL statements of `table_2`. This means it needs to continue parsing between `t2` and `t3`.
- During the binlog parsing process between `t2` and `t3`, the DML statements of `schema V2` from `table_1` cannot be replicated to the downstream until the sharding DDL statement is replicated and successfully executed.

In DM, the simplified replication process of sharding DDL statements within the DM worker is as follows:

1. When receiving the DDL statement of `table_1` at `t1`, the DM-worker records the DDL information and the current position of the binlog.
2. DM-worker continues parsing the binlog between `t2` and `t3`.
3. DM-worker ignores the DML statement with the `schema V2` schema that belongs to `table_1`, and replicates the DML statement with the `schema V1` schema that belongs to `table_2` to the downstream.
4. When receiving the DDL statement of `table_2` at `t3`, the DM-worker records the DDL information and the current position of the binlog.
5. Based on the information of the replication task configuration and the upstream schemas and tables, the DM-worker decides that the DDL statements of all sharded tables in the MySQL instance have been received and replicates them to the downstream to modify the downstream table schema.
6. DM-worker sets the starting point of parsing the new binlog stream to be the position saved at Step #1.
7. DM-worker resumes parsing the binlog between `t2` and `t3`.
8. DM-worker replicates the DML statement with the `schema V2` schema that belongs to `table_1` to the downstream, and ignores the DML statement with the `schema V1` schema that belongs to `table_2`.
9. After parsing the binlog position saved at Step #4, the DM-worker decides that all DML statements that have been ignored in Step #3 have been replicated to the downstream again.
10. DM-worker resumes the replication starting from the binlog position at `t4`.

You can conclude from the above analysis that DM mainly uses two-level sharding groups for coordination and control when handling replication of the sharding DDL. Here is the simplified process:

1. Each DM-worker independently coordinates the DDL statements replication for the corresponding sharding group composed of multiple sharded tables within the upstream MySQL instance.
2. After the DM-worker receives the DDL statements of all sharded tables, it sends the DDL information to `DM-master`.
3. `DM-master` coordinates the DDL replication of the sharding group composed of the DM-workers based on the received DDL information.
4. After receiving the DDL information from all DM-workers, `DM-master` requests the DDL lock owner (a specific DM-worker) to execute the DDL statement.
5. The DDL lock owner executes the DDL statement and returns the result to `DM-master`. Then the owner restarts the replication of the previously ignored DML statements during the internal coordination of DDL replication.
6. After `DM-master` confirms that the owner has successfully executed the DDL statement, it asks all other DM-workers to continue the replication.
7. All other DM-workers separately restart the replication of the previously ignored DML statements during the internal coordination of DDL replication.
8. After finishing replicating the ignored DML statements again, all DM-workers resume the normal replication process.
