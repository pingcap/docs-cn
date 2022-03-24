---
title: Handle Sharding DDL Locks Manually in DM
summary: Learn how to handle sharding DDL locks manually in DM.
aliases: ['/docs/tidb-data-migration/dev/feature-manually-handling-sharding-ddl-locks/']
---

# Handle Sharding DDL Locks Manually in DM

DM uses the sharding DDL lock to ensure operations are performed in the correct order. This locking mechanism resolves sharding DDL locks automatically in most cases, but you need to use the `shard-ddl-lock` command to manually handle the abnormal DDL locks in some abnormal scenarios.

> **Note:**
>
> - This document only applies to the processing of sharding DDL lock in pessimistic coordination mode.
> - The commands in the Command usage sections in this document are in interactive mode. In command-line mode, you need to add the escape characters to avoid an error report.
> - Do not use `shard-ddl-lock unlock` unless you are totally aware of the possible impacts brought by the command and you can accept them.
> - Before manually handling the abnormal DDL locks, make sure that you have already read the DM [shard merge principles](/dm/feature-shard-merge-pessimistic.md#principles).

## Command

### `shard-ddl-lock`

You can use this command to view the DDL lock and request DM-master to release the specified DDL lock. This command is only supported in DM v6.0 and later. For earlier versions, you must use the `show-ddl-locks` and `unlock-ddl-locks` commands.

```bash
shard-ddl-lock -h
```

```
maintain or show shard-ddl locks information
Usage:
  dmctl shard-ddl-lock [task] [flags]
  dmctl shard-ddl-lock [command]
Available Commands:
  unlock      Unlock un-resolved DDL locks forcely
Flags:
  -h, --help   help for shard-ddl-lock
Global Flags:
  -s, --source strings   MySQL Source ID.
Use "dmctl shard-ddl-lock [command] --help" for more information about a command.
```

#### Arguments description

* `shard-ddl-lock [task] [flags]`: view the DDL lock information on the current DM-master.

+ `shard-ddl-lock [command]`: request DM-master to release the specified DDL lock. `[command]` only accepts `unlock` as a value.

## Usage examples

### `shard-ddl-lock [task] [flags]`

You can use `shard-ddl-lock [task] [flags]` to view the DDL lock information on the current DM-master. For example:

```bash
shard-ddl-lock test
```

<details>
<summary>Expected output</summary>

```
{
    "result": true,                                        # The result of the query for the lock information.
    "msg": "",                                             # The additional message for the failure to query the lock information or other descriptive information (for example, the lock task does not exist).
    "locks": [                                             # The existing lock information list.
        {
            "ID": "test-`shard_db`.`shard_table`",         # The lock ID, which is made up of the current task name and the schema/table information corresponding to the DDL.
            "task": "test",                                # The name of the task to which the lock belongs.
            "mode": "pessimistic"                          # The shard DDL mode. Can be set to "pessimistic" or "optimistic".
            "owner": "mysql-replica-01",                   # The owner of the lock (the ID of the first source that encounters this DDL operation in the pessimistic mode), which is always empty in the optimistic mode.
            "DDLs": [                                      # The list of DDL operations corresponding to the lock in the pessimistic mode, which is always empty in the optimistic mode.
                "USE `shard_db`; ALTER TABLE `shard_db`.`shard_table` DROP COLUMN `c2`;"
            ],
            "synced": [                                    # The list of sources that have received all sharding DDL events in the corresponding MySQL instance.
                "mysql-replica-01"
            ],
            "unsynced": [                                  # The list of sources that have not yet received all sharding DDL events in the corresponding MySQL instance.
                "mysql-replica-02"
            ]
        }
    ]
}
```

</details>

### `shard-ddl-lock unlock`

This command actively requests `DM-master` to unlock the specified DDL lock, including requesting the owner to execute the DDL statement, requesting all other DM-workers that are not the owner to skip the DDL statement, and removing the lock information on `DM-master`.

> **Note:**
>
> Currently, `shard-ddl-lock unlock` takes effect only for the lock in the `pessimistic` mode.

```bash
shard-ddl-lock unlock -h
```

```
Unlock un-resolved DDL locks forcely

Usage:
  dmctl shard-ddl-lock unlock <lock-id> [flags]

Flags:
  -a, --action string     accept skip/exec values which means whether to skip or execute ddls (default "skip")
  -d, --database string   database name of the table
  -f, --force-remove      force to remove DDL lock
  -h, --help              help for unlock
  -o, --owner string      source to replace the default owner
  -t, --table string      table name

Global Flags:
  -s, --source strings   MySQL Source ID.
```

`shard-ddl-lock unlock` accepts the following arguments:

+ `-o, --owner`:

    - Flag; string; optional
    - If it is not specified, this command requests for the default owner (the owner in the result of `shard-ddl-lock`) to execute the DDL statement; if it is specified, this command requests for the MySQL source (the alternative of the default owner) to execute the DDL statement.
    - The new owner should not be specified unless the original owner is already removed from the cluster.

+ `-f, --force-remove`:

    - Flag; boolean; optional
    - If it is not specified, this command removes the lock information only when the owner succeeds to execute the DDL statement; if it is specified, this command forcefully removes the lock information even though the owner fails to execute the DDL statement (after doing this you cannot query or operate on the lock again).

+ `lock-id`:

    - Non-flag; string; required
    - It specifies the ID of the DDL lock that needs to be unlocked (the `ID` in the result of `shard-ddl-lock`).

The following is an example of the `shard-ddl-lock unlock` command:

{{< copyable "shell-regular" >}}

```bash
shard-ddl-lock unlock test-`shard_db`.`shard_table`
```

```
{
    "result": true,                                        # The result of the unlocking operation.
    "msg": "",                                             # The additional message for the failure to unlock the lock.
}
```

## Supported scenarios

Currently, the `shard-ddl-lock unlock` command only supports handling sharding DDL locks in the following two abnormal scenarios.

### Scenario 1: Some MySQL sources are removed

#### The reason for the abnormal lock

Before `DM-master` tries to automatically unlock the sharding DDL lock, all the MySQL sources need to receive the sharding DDL events (for details, see [shard merge principles](/dm/feature-shard-merge-pessimistic.md#principles)). If the sharding DDL event is already in the migration process, and some MySQL sources have been removed and are not to be reloaded (these MySQL sources have been removed according to the application demand), then the sharding DDL lock cannot be automatically migrated and unlocked because not all the DM-workers can receive the DDL event.

> **Note:**
>
> If you need to make some DM-workers offline when not in the process of migrating sharding DDL events, a better solution is to use `stop-task` to stop the running tasks first, make the DM-workers go offline, remove the corresponding configuration information from the task configuration file, and finally use `start-task` and the new task configuration to restart the migration task.

#### Manual solution

Suppose that there are two instances `MySQL-1` (`mysql-replica-01`) and `MySQL-2` (`mysql-replica-02`) in the upstream, and there are two tables `shard_db_1`.`shard_table_1` and `shard_db_1`.`shard_table_2` in `MySQL-1` and two tables `shard_db_2`.`shard_table_1` and `shard_db_2`.`shard_table_2` in `MySQL-2`. Now we need to merge the four tables and migrate them into the table `shard_db`.`shard_table` in the downstream TiDB.

The initial table structure is:

```sql
SHOW CREATE TABLE shard_db_1.shard_table_1;
+---------------+------------------------------------------+
| Table         | Create Table                             |
+---------------+------------------------------------------+
| shard_table_1 | CREATE TABLE `shard_table_1` (
  `c1` int(11) NOT NULL,
  PRIMARY KEY (`c1`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 |
+---------------+------------------------------------------+
```

The following DDL operation will be executed on the upstream sharded tables to alter the table structure:

```sql
ALTER TABLE shard_db_*.shard_table_* ADD COLUMN c2 INT;
```

The operation processes of MySQL and DM are as follows:

1. The corresponding DDL operations are executed on the two sharded tables of `mysql-replica-01` to alter the table structures.

    ```sql
    ALTER TABLE shard_db_1.shard_table_1 ADD COLUMN c2 INT;
    ```

    ```sql
    ALTER TABLE shard_db_1.shard_table_2 ADD COLUMN c2 INT;
    ```

2. DM-worker sends the received DDL information of the two sharded tables of `mysql-replica-01` to DM-master, and DM-master creates the corresponding DDL lock.
3. Use `shard-ddl-lock` to check the information of the current DDL lock.

    ```bash
    » shard-ddl-lock test
    {
        "result": true,
        "msg": "",
        "locks": [
            {
                "ID": "test-`shard_db`.`shard_table`",
                "task": "test",
                "mode": "pessimistic"
                "owner": "mysql-replica-01",
                "DDLs": [
                    "USE `shard_db`; ALTER TABLE `shard_db`.`shard_table` ADD COLUMN `c2` int(11);"
                ],
                "synced": [
                    "mysql-replica-01"
                ],
                "unsynced": [
                    "mysql-replica-02"
                ]
            }
        ]
    }
    ```

4. Due to the application demand, the data corresponding to `mysql-replica-02` is no longer needed to be migrated to the downstream TiDB, and `mysql-replica-02` is removed.
5. The lock whose ID is ```test-`shard_db`.`shard_table` ``` on `DM-master` cannot receive the DDL information of `mysql-replica-02`.

    - The returned result `unsynced` by `shard-ddl-lock` has always included the information of `mysql-replica-02`.

6. Use `shard-ddl-lock unlock` to request `DM-master` to actively unlock the DDL lock.

    - If the owner of the DDL lock has gone offline, you can use the parameter `--owner` to specify another DM-worker as the new owner to execute the DDL.
    - If any MySQL source reports an error, `result` will be set to `false`, and at this point you should check carefully if the errors of each MySQL source is acceptable and within expectations.

        {{< copyable "shell-regular" >}}

        ```bash
        shard-ddl-lock unlock test-`shard_db`.`shard_table`
        ```

        ```
        {
            "result": true,
            "msg": ""
        ```

7. Use `shard-ddl-lock` to confirm if the DDL lock is unlocked successfully.

    ```bash
    » shard-ddl-lock test
    {
        "result": true,
        "msg": "no DDL lock exists",
        "locks": [
        ]
    }
    ```

8. Check whether the table structure is altered successfully in the downstream TiDB.

    ```sql
    mysql> SHOW CREATE TABLE shard_db.shard_table;
    +-------------+--------------------------------------------------+
    | Table       | Create Table                                     |
    +-------------+--------------------------------------------------+
    | shard_table | CREATE TABLE `shard_table` (
      `c1` int(11) NOT NULL,
      `c2` int(11) DEFAULT NULL,
      PRIMARY KEY (`c1`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin |
    +-------------+--------------------------------------------------+
    ```

9. Use `query-status` to confirm if the migration task is normal.

#### Impact

After you have manually unlocked the lock by using `shard-ddl-lock unlock`, if you don't deal with the offline MySQL sources included in the task configuration information, the lock might still be unable to be migrated automatically when the next sharding DDL event is received.

Therefore, after you have manually unlocked the DDL lock, you should perform the following operations:

1. Use `stop-task` to stop the running tasks.
2. Update the task configuration file, and remove the related information of the offline MySQL source from the configuration file.
3. Use `start-task` and the new task configuration file to restart the task.

> **Note:**
>
> After you run `shard-ddl-lock unlock`, if the MySQL source that went offline is reloaded and the DM-worker tries to migrate the data of the sharded tables, a match error between the data and the downstream table structure might occur.

### Scenario 2: Some DM-workers stop abnormally or the network failure occurs during the DDL unlocking process

#### The reason for the abnormal lock

After `DM-master` receives the DDL events of all DM-workers, automatically running `unlock DDL lock` mainly include the following steps:

1. Ask the owner of the lock to execute the DDL and update the checkpoints of corresponding sharded tables.
2. Remove the DDL lock information stored on `DM-master` after the owner successfully executes the DDL.
3. Ask all other non-owners to skip the DDL and update the checkpoints of corresponding sharded tables after the owner successfully executes the DDL.
4. DM-master removes the corresponding DDL lock information after all the owners or non-owners' operations are successful.

Currently, the above unlocking process is not atomic. If the non-owner skips the DDL operation successfully, the DM-worker where the non-owner is located stops abnormally or a network anomaly occurs with the downstream TiDB, which can cause the checkpoint updating to fail.

When the MySQL source corresponding to the non-owner restores data migration, the non-owner tries to request the DM-master to re-coordinate the DDL operation that has been coordinated before the exception occurs and will never receives the corresponding DDL operation from other MySQL sources. This can cause the DDL operation to automatically unlock the corresponding lock.

#### Manual solution

Suppose that now we have the same upstream and downstream table structures and the same demand for merging tables and migration as in the manual solution of [Some MySQL sources are removed](#scenario-1-some-mysql-sources-are-removed).

When `DM-master` automatically executes the unlocking process, the owner (`mysql-replica-01`) successfully executes the DDL and continues the migration process. However, in the process of requesting the non-owner (`mysql-replica-02`) to skip the DDL operation, the checkpoint fails to update after the DM-worker skips the DDL operation because the corresponding DM-worker was restarted.

After the data migration subtask corresponding to `mysql-replica-02` restores, a new lock is created on the DM-master, but other MySQL sources have executed or skipped DDL operations and are performing subsequent migration.

The operation processes are:

1. Use `shard-ddl-lock` to confirm if the corresponding lock of the DDL exists on `DM-master`.

    Only `mysql-replica-02` is at the `synced` state.

    ```bash
    » shard-ddl-lock
    {
        "result": true,
        "msg": "",
        "locks": [
            {
                "ID": "test-`shard_db`.`shard_table`",
                "task": "test",
                "mode": "pessimistic"
                "owner": "mysql-replica-02",
                "DDLs": [
                    "USE `shard_db`; ALTER TABLE `shard_db`.`shard_table` ADD COLUMN `c2` int(11);"
                ],
                "synced": [
                    "mysql-replica-02"
                ],
                "unsynced": [
                    "mysql-replica-01"
                ]
            }
        ]
    }
    ```

2. Use `shard-ddl-lock` to ask `DM-master` to unlock the lock.

    - During the unlocking process, the owner tries to execute the DDL operation to the downstream again (the original owner before restarting has executed the DDL operation to the downstream once). Make sure that the DDL operation can be executed multiple times.

        ```bash
        shard-ddl-lock unlock test-`shard_db`.`shard_table`
        {
            "result": true,
            "msg": "",
        }
        ```

3. Use `shard-ddl-lock` to confirm if the DDL lock has been successfully unlocked.
4. Use `query-status` to confirm if the migration task is normal.

#### Impact

After manually unlocking the lock, the following sharding DDL can be migrated automatically and normally.
