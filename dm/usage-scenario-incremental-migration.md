---
title: Incremental Data Migration Scenario
---

# Incremental Data Migration Scenario

This document describes how to use Data Migration (DM) to replicate the Binlog from a specified position in the source database to the downstream TiDB. The scenario is based on an example of migrating a data source MySQL instance to TiDB.

## Data source table

Assume the data source instance is:

| Schema | Tables |
|:------|:------|
| user  | information, log |
| store | store_bj, store_tj |
| log   | messages |

## Migration requirements

Only replicate the data change from a specified position in the source database `log` to the TiDB cluster.

## Incremental data migration operations

This section provides you data migration steps, which helps you use DM to replicate data changes from the `log` database to the TiDB cluster.

### Determines the start position of incremental replication

First you need to determine the replication position of the binlog where you start to migrate data. If you have determined the position of binlog, skip this step.

By following the steps below, you can obtain the position of binlog where you start migrating data in the source data:

- Use Dumpling/Mydumper for full data export. Then use other tools, such as TiDB Lightning, for full data import. After that, you can obtain the replication position by inspecting the [metadata files](/dumpling-overview.md#format-of-exported-files).

  ```file
  Started dump at: 2020-11-10 10:40:19
  SHOW MASTER STATUS:
        Log: mysql-bin.000001
        Pos: 2022
        GTID: 09bec856-ba95-11ea-850a-58f2b4af5188:1-9 
  Finished dump at: 2020-11-10 10:40:20
  ```

- Use `SHOW BINLOG EVENTS`, or use the `mysqlbinlog` tool to check binlog and select an appropriate position.
- If you want to start replicating binlog at the current time, use `SHOW MASTER STATUS` to check the current position:

  ```sql
  MySQL [log]> SHOW MASTER STATUS;
  +------------------+----------+--------------+------------------+------------------------------------------+
  | File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set                        |
  +------------------+----------+--------------+------------------+------------------------------------------+
  | mysql-bin.000001 |     2022 |              |                  | 09bec856-ba95-11ea-850a-58f2b4af5188:1-9 |
  +------------------+----------+--------------+------------------+------------------------------------------+
  1 row in set (0.000 sec)
  ```

This example starts replicating data changes from `binlog position=(mysql-bin.000001, 2022), gtid=09bec856-ba95-11ea-850a-58f2b4af5188:1-9`.

### Create tables manually downstream

Because the table SQL statements are created before replication starting point, this incremental replication task does not automatically create tables downstream. So you need to manually create a table schema at the corresponding starting point in the downstream TiDB. The detailed steps are as follows:

{{< copyable "sql" >}}

```sql
CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  `message` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
)
```

### Create a replication task

1. Create task configuration `task.yaml` to configure incremental replication mode and replication starting point for each data source. The complete task configuration example is as follows:

   {{< copyable "yaml" >}}

   ```yaml
   name: task-test # The name of the task. Should be globally unique.
   task-mode: incremental # The mode of the task. For "incremental", only incremental data is migrated.

   ## Configure the access information of TiDB database instance:
   target-database: # Downstream database instance configuration.
     host: "127.0.0.1"
     port: 4000
     user: "root"
     password: "" # If password is not empty, it is recommended to use dmctl encrypted password.

   ## Use block-allow-list to configure tables that require sync:
   block-allow-list: # The filter rule set of the matched table of the data source database instance. Use black-white-list if the DM version is earlier than or equal to v2.0.0-beta.2.
     bw-rule-1: # The name of the block and allow list rule.
       do-dbs: ["log"]# The databases to be migrated.

   ## (Optional) If incremental data migration needs to remigrate the data that has already been migrated during full data migration process, you need to enable safe mode to avoid incremental migration errors.
   ## This scenario usually happens when the full migrated data is not a consistent snapshot of the data source. You need to start migrating incremental data at a position before the full data migration starting point.
   syncers: # The configuration parameters of sync unit.
     global: # The name of the configuration.
       safe-mode: true # If you set `safe-mode` to `true`, `INSERT` from data sources is rewritten to `REPLACE` and `UPDATE` is rewritten to `DELETE` and `REPLACE`. This is to ensure that when primary keys or unique keys exist in table structure, you can re-import DML when migrating data.

   ## Configure the data source
   mysql-instances:
     - source-id: "mysql-01" # The ID of data source. You can obtain it from the configuration of the data source.
       block-allow-list: "bw-rule-1" # To import the block-allow-list configuration above.
       syncer-config-name: "global" # To import the incremental data migration configuration of syncers.
       meta: # If `task-mode` is `incremental` and the `checkpoint` in the downstream database does not exist, `meta` is the starting point of binlog; If `checkpoint` exists, base it on `checkpoint`.
         binlog-name: "mysql-bin. 00001"
         binlog-pos: 2022
         binlog-gtid: "09bec856-ba95-11ea-850a-58f2b4af5188:1-9"
   ```

2. Create a replication task using the `start-task` command:

   {{< copyable "shell-regular" >}}

   ```bash
   tiup dmctl --master-addr <master-addr> start-task task.yaml
   ```

   ```
   {
       "result": true,
       "msg": "",
       "sources": [
           {
               "result": true,
               "msg": "",
               "source": "mysql-01",
               "worker": "127.0.0.1:8262"
           }
       ]
   }
   ```

3. Check the replication task using the `query-status` command to ensure that no error message occurs:

   {{< copyable "shell-regular" >}}

   ```bash
   tiup dmctl --master-addr <master-addr> query-status test
   ```

   ```
   {
       "result": true,
       "msg": "",
       "sources": [
           {
               "result": true,
               "msg": "",
               "sourceStatus": {
                   "source": "mysql-01",
                   "worker": "127.0.0.1:8262",
                   "result": null,
                   "relayStatus": null
               },
               "subTaskStatus": [
                   {
                       "name": "task-test",
                       "stage": "Running",
                       "unit": "Sync",
                       "result": null,
                       "unresolvedDDLLockID": "",
                       "sync": {
                           "totalEvents": "0",
                           "totalTps": "0",
                           "recentTps": "0",
                           "masterBinlog": "(mysql-bin.000001, 2022)",
                           "masterBinlogGtid": "09bec856-ba95-11ea-850a-58f2b4af5188:1-9",
                           "syncerBinlog": "(mysql-bin.000001, 2022)",
                           "syncerBinlogGtid": "",
                           "blockingDDLs": [
                           ],
                           "unresolvedGroups": [
                           ],
                           "synced": true,
                           "binlogType": "remote"
                       }
                   }
               ]
           }
       ]
   }
   ```

## Test replication tasks

Insert new data in the source database:

{{< copyable "sql" >}}

```sql
MySQL [log]> INSERT INTO messages VALUES (4, 'msg4'), (5, 'msg5');
Query OK, 2 rows affected (0.010 sec)
Records: 2  Duplicates: 0  Warnings: 0
```

Currently, the source data is:

```sql
MySQL [log]> SELECT * FROM messages;
+----+---------+
| id | message |
+----+---------+
|  1 | msg1    |
|  2 | msg2    |
|  3 | msg3    |
|  4 | msg4    |
|  5 | msg5    |
+----+---------+
5 rows in set (0.001 sec)
```

If you query data in the downstream, you can find that the data after `(3, 'msg3')` is replicated successfully:

```sql
MySQL [log]> SELECT * FROM messages;
+----+---------+
| id | message |
+----+---------+
|  4 | msg4    |
|  5 | msg5    |
+----+---------+
2 rows in set (0.001 sec)
```
