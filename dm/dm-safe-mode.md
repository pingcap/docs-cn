---
title: DM Safe Mode
summary: Introduces the DM safe mode, its purpose, working principles and how to use it.
---

# DM Safe Mode

Safe mode is a special operation mode for DM to perform incremental replication. In safe mode, when the DM incremental replication component replicates binlog events, DM forcibly rewrites all the `INSERT` and `UPDATE` statements before executing them in the downstream.

During safe mode, one binlog event can be replicated repeatedly to the downstream with idempotence guaranteed. Thus, the incremental replication is *safe*.

After resuming a data replication task from a checkpoint, DM might repeatedly replicate some binlog events, which leads to the following issues:

- During incremental replication, the operation of executing DML and the operation of writing checkpoints are not simultaneous. The operation of writing checkpoints and writing data into the downstream database is not atomic. Therefore, **when DM exits abnormally, checkpoints might only record the restoration point before the exit point**.
- When DM restarts a replication task and resumes incremental replication from a checkpoint, some data between the checkpoint and the exit point might already be processed before the abnormal exit. This causes **some SQL statements to be executed repeatedly**.
- If an `INSERT` statement is executed repeatedly, the primary key or the unique index might encounter a conflict, which leads to a replication failure. If an `UPDATE` statement is executed repeatedly, the filter condition might not be able to locate the previously updated records.

In safe mode, DM can rewrite SQL statements to resolve the preceding issues.

## Working principle

In safe mode, DM guarantees the idempotency of binlog events by rewriting SQL statements. Specifically, the following SQL statements are rewritten:

* `INSERT` statements are rewritten to `REPLACE` statements.
* `UPDATE` statements are analyzed to obtain the value of the primary key or the unique index of the row updated. `UPDATE` statements are then rewritten to `DELETE` + `REPLACE` statements in the following two steps: DM deletes the old record using the primary key or unique index, and inserts the new record using the `REPLACE` statement.

`REPLACE` is a MySQL-specific syntax for inserting data. When you insert data using `REPLACE`, and the new data and existing data have a primary key or unique constraint conflict, MySQL deletes all the conflicting records and executes the insert operation, which is equivalent to "force insert". For details, see [`REPLACE` statement](https://dev.mysql.com/doc/refman/8.0/en/replace.html) in MySQL documentation.

Assume that a `dummydb.dummytbl` table has a primary key `id`. Execute the following SQL statements repeatedly on this table:

```sql
INSERT INTO dummydb.dummytbl (id, int_value, str_value) VALUES (123, 999, 'abc');
UPDATE dummydb.dummytbl SET int_value = 888999 WHERE int_value = 999;   -- Suppose there is no other record with int_value = 999
UPDATE dummydb.dummytbl SET id = 999 WHERE id = 888;    -- Update the primary key
```

With safe mode enabled, when the preceding SQL statements are executed again in the downstream, they are rewritten as follows:

```sql
REPLACE INTO dummydb.dummytbl (id, int_value, str_value) VALUES (123, 999, 'abc');
DELETE FROM dummydb.dummytbl WHERE id = 123;
REPLACE INTO dummydb.dummytbl (id, int_value, str_value) VALUES (123, 888999, 'abc');
DELETE FROM dummydb.dummytbl WHERE id = 888;
REPLACE INTO dummydb.dummytbl (id, int_value, str_value) VALUES (999, 888888, 'abc888');
```

In the preceding statements, `UPDATE` is rewritten as `DELETE` + `REPLACE`, rather than `DELETE` + `INSERT`. If `INSERT` is used here, when you insert a duplicate record with `id = 999`, the database reports a primary key conflict. This is why `REPLACE` is used instead. The new record will replace the existing record.

By rewriting SQL statements, DM overwrites the existing row data using the new row data when performing duplicate insert or update operations. This guarantees that insert and update operations are executed repeatedly.

## Enable safe mode

You can enable safe mode either automatically or manually. This section describes the detailed steps.

### Automatically enable

When DM resumes an incremental replication task from a checkpoint (For example, DM worker restart or network reconnection), DM automatically enables safe mode for a period (60 seconds by default).

Whether to enable safe mode is related to `safemode_exit_point` in the checkpoint. When an incremental replication task is paused abnormally, DM tries to replicate all DML statements in the memory to the downstream and records the latest binlog position among the DML statements as `safemode_exit_point`, which is saved to the last checkpoint.

The detailed logic is as follows:

- If the checkpoint contains `safemode_exit_point`, the incremental replication task is paused abnormally. When DM resumes the task, the binlog position of the checkpoint to be resumed (**begin position**) is earlier than `safemode_exit_point`, which represents the binlog events between the begin position and the `safemode_exit_point` might have been processed in the downstream. So, during the resume process, some binlog events might be executed repeatedly. Therefore, enabling safe mode can make these binlog positions **safe**. After the binlog position exceeds the `safemode_exit_point`, DM automatically disables safe mode unless safe mode is enabled manually.

- If the checkpoint does not contain `safemode_exit_point`, there are two cases:

    1. This is a new task, or this task is paused as expected.
    2. This task is paused abnormally but DM fails to record `safemode_exit_point`, or the DM process exits abnormally.

    In the second case, DM does not know which binlog events after the checkpoint are executed in the downstream. To ensure that repeatedly executed binlog events do not cause any problems, DM automatically enables safe mode during the first two checkpoint intervals. The default interval between two checkpoints is 30 seconds, which means when a normal incremental replication task starts, safe mode is enforced for the first 60 seconds (2 * 30 seconds).

    Usually, it is not recommended to change the checkpoint interval to adjust the safe mode period at the beginning of the incremental replication task. However, if you do need a change, you can [manually enable safe mode](#manually-enable) (recommended) or change the `checkpoint-flush-interval` item in syncer configuration.

### Manually enable

You can set the `safe-mode` item in the syncer configuration to enable safe mode during the entire replication process. `safe-mode` is a bool type parameter and is `false` by default. If it is set to `true`, DM enables safe mode for the whole incremental replication process. 

The following is a task configuration example with safe mode enabled:

```
syncers:                              # The running configurations of the sync processing unit.
  global:                            # Configuration name.
    # Other configuration items are not provided in this example.
    safe-mode: true                  # Enables safe mode for the whole incremental replication process.
    # Other configuration items are not provided in this example.
# ----------- Instance configuration -----------
mysql-instances:
  -
    source-id: "mysql-replica-01"
    # Other configuration items are not provided in this example.
    syncer-config-name: "global"            # Name of the syncers configuration.
```

## Notes for safe mode

If you want to enable safe mode during the entire replication process for safety reasons, be aware of the following:

- **Incremental replication in safe mode consumes extra overhead.** Frequent `DELETE` + `REPLACE` operations result in frequent changes to primary keys or unique indexes, which creates a greater performance overhead than executing `UPDATE` statements only.
- **Safe mode forces the replacement of records with the same primary key, which might result in data loss in the downstream.** When you merge and migrate shards from the upstream to the downstream, incorrect configuration might lead to a large number of primary key or unique key conflicts. If safe mode is enabled in this situation, the downstream might lose lots of data without showing any exception, resulting in severe data inconsistency.
- **Safe mode relies on the primary key or unique index to detect conflicts.** If the downstream table has no primary key or unique index, DM cannot use `REPLACE` to replace and insert records. In this case, even if safe mode is enabled and DM rewrites `INSERT` to `REPLACE` statements, duplicate records are still inserted into the downstream.

In summary, if the upstream database has data with duplicate primary keys, and your application tolerates loss of duplicate records and performance overhead, you can enable safe mode to ignore data duplication.
