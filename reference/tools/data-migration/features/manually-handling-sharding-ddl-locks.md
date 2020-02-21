---
title: Handle Sharding DDL Locks Manually in DM
summary: Learn how to handle sharding DDL locks manually in DM.
category: reference
---

# Handle Sharding DDL Locks Manually in DM

DM uses the sharding DDL lock to ensure operations are performed in the correct order. This locking mechanism resolves sharding DDL locks automatically in most cases, but you need to use the `unlock-ddl-lock` or `break-ddl-lock` command to manually handle the abnormal DDL locks in some abnormal scenarios.

> **Warning:**
>
> - Do not use `unlock-ddl-lock` or `break-ddl-lock` unless you are totally aware of the possible impacts brought by the command and you can accept them.
> - Before manually handling the abnormal DDL locks, make sure that you have already read the DM [shard merge principles](/reference/tools/data-migration/features/shard-merge.md#principles).

## Command

### `show-ddl-locks`

This command queries the current DDL lock information on `DM-master`.

#### Command usage

```bash
show-ddl-locks [--worker=127.0.0.1:8262] [task-name]
```

#### Arguments description

+ `worker`:

    - Flag; string; `--worker`; optional
    - It can be specified repeatedly multiple times.
    - If it is not specified, this command queries the lock information related to all DM-workers; if it is specified, this command queries the lock information related only to the specified DM-worker.

+ `task-name`:

    - Non-flag; string; optional
    - If it is not specified, this command queries the lock information related to all tasks; if it is specified, this command queries the lock information related only to the specified task.

#### Example of results

```bash
» show-ddl-locks test
{
    "result": true,                                        # The result of the query for the lock information.
    "msg": "",                                             # The additional message for the failure to query the lock information or other descriptive information (for example, the lock task does not exist).
    "locks": [                                             # The lock information list on DM-master.
        {
            "ID": "test-`shard_db`.`shard_table`",         # The lock ID, which is made up of the current task name and the schema/table information corresponding to the DDL.
            "task": "test",                                # The name of the task to which the lock belongs.
            "owner": "127.0.0.1:8262",                     # The owner of the lock.
            "DDLs": [                                      # The DDL list corresponding to the lock.
                "USE `shard_db`; ALTER TABLE `shard_db`.`shard_table` DROP COLUMN `c2`;"
            ],
            "synced": [                                    # The list of DM-workers that have received all sharding DDL events in the corresponding MySQL instance.
                "127.0.0.1:8262"
            ],
            "unsynced": [                                  # The list of DM-workers that have not yet received all sharding DDL events in the corresponding MySQL instance.
                "127.0.0.1:8263"
            ]
        }
    ]
}
```

### `unlock-ddl-lock`

This command actively requests `DM-master` to unlock the specified DDL lock, including requesting the owner to execute the DDL statement, requesting all other DM-workers that are not the owner to skip the DDL statement, and removing the lock information on `DM-master`.

#### Command usage

```bash
unlock-ddl-lock [--worker=127.0.0.1:8262] [--owner] [--force-remove] <lock-ID>
```

#### Arguments description

+ `worker`:

    - Flag; string; `--worker`; optional
    - It can be specified repeatedly multiple times.
    - If it is not specified, this command sends requests for all DM-workers (except for the owner) that are waiting for the lock to skip the DDL statement; if it is specified, this command sends requests only for the specified DM-worker to skip the DDL statement.

+ `owner`:

    - Flag; string; `--owner`; optional
    - If it is not specified, this command requests for the default owner (the owner in the result of `show-ddl-locks`) to execute the DDL statement; if it is specified, this command requests for the DM-worker (the alternative of the default owner) to execute the DDL statement.

+ `force-remove`:

    - Flag; boolean; `--force-remove`; optional
    - If it is not specified, this command removes the lock information only when the owner succeeds to execute the DDL statement; if it is specified, this command forcefully removes the lock information even though the owner fails to execute the DDL statement (after doing this you cannot query or operate on the lock again).

+ `lock-ID`:

    - Non-flag; string; required
    - It specifies the ID of the DDL lock that needs to be unlocked (the `ID` in the result of `show-ddl-locks`).

#### Example of results

```bash
» unlock-ddl-lock test-`shard_db`.`shard_table`
{
    "result": true,                                        # The result of the unlocking operation.
    "msg": "",                                             # The additional message for the failure to unlock the lock.
    "workers": [                                           # The result list of the executing or skipping DDL operation of each DM-worker.
        {
            "result": true,                                # The result of the executing or skipping DDL operation.
            "worker": "127.0.0.1:8262",                    # The DM-worker ID.
            "msg": ""                                      # The reasons why the DM-worker failed to execute or skip the DDL statement.
        }
    ]
}
```

### `break-ddl-lock`

This command actively asks the DM-worker to forcefully break the DDL lock that is to be unlocked, including asking the DM-worker to execute/skip the DDL and removing the DDL lock information on the DM-worker.

#### Command usage

```bash
break-ddl-lock <--worker=127.0.0.1:8262> [--remove-id] [--exec] [--skip] <task-name>
```

#### Arguments description

+ `worker`:

    - Flag; string; `--worker`; required
    - It specifies the DM-worker that needs to execute the breaking operation.

+ `remove-id`: deprecated.
+ `exec`:

    - Flag; boolean; `--exec`; optional
    - It cannot be specified simultaneously with the `--skip` parameter.
    - If it is specified, this command asks the DM-worker to execute the corresponding DDL statement of the lock.

+ `skip`:

    - flag; boolean; `--skip`; optional
    - It cannot be specified simultaneously with the `--exec` parameter.
    - If it is specified, this command asks the DM-worker to skip the corresponding DDL statement of the lock.

+ `task-name`:

    - Non-flag; string; required
    - It specifies the name of the task containing the lock that is going to execute the breaking operation (you can check whether a task contains the lock via [query-status](/reference/tools/data-migration/query-status.md)).

#### Example of results

```bash
» break-ddl-lock -w 127.0.0.1:8262 --exec test
{
    "result": true,                                        # The result of the lock breaking operation.
    "msg": "",                                             # The reason why the breaking lock operation failed.
    "workers": [                                           # The list of DM-workers which break the lock (currently the lock can be broken by only one DM-worker at a single operation).
        {
            "result": false,                               # The result of the lock breaking operation by the DM-worker.
            "worker": "127.0.0.1:8262",                    # The DM-worker ID.
            "msg": ""                                      # The reason why the DM-worker failed to break the lock.
        }
    ]
}
```

## Supported scenarios

Currently, the `unlock-ddl-lock` or `break-ddl-lock` command only supports handling sharding DDL locks in the following three abnormal scenarios.

### Scenario 1: Some DM-workers go offline

#### The reason for the abnormal lock

Before `DM-master` tries to automatically unlock the sharding DDL lock, all the DM-workers need to receive the sharding DDL events (for details, see [shard merge principles](/reference/tools/data-migration/features/shard-merge.md#principles)). If the sharding DDL event is already in the replication process, and some DM-workers have gone offline and are not to be restarted (these DM-workers have been removed according to the application demand), then the sharding DDL lock cannot be automatically replicated and unlocked because not all the DM-workers can receive the DDL event.

> **Note:**
>
> If you need to make some DM-workers offline when not in the process of replicating sharding DDL events, a better solution is to use `stop-task` to stop the running tasks first, make the DM-workers go offline, remove the corresponding configuration information from the task configuration file, and finally use `start-task` and the new task configuration to restart the replication task.

#### Manual solution

Suppose that there are two instances `MySQL-1` and `MySQL-2` in the upstream, and there are two tables `shard_db_1`.`shard_table_1` and `shard_db_1`.`shard_table_2` in `MySQL-1` and two tables `shard_db_2`.`shard_table_1` and `shard_db_2`.`shard_table_2` in `MySQL-2`. Now we need to merge the four tables and replicate them into the table `shard_db`.`shard_table` in the downstream TiDB.

The initial table structure is:

```sql
mysql> SHOW CREATE TABLE shard_db_1.shard_table_1;
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

1. The corresponding DDL operations are executed on the two sharded tables of `DM-worker-1` in `MySQL-1` to alter the table structures.

    ```sql
    ALTER TABLE shard_db_1.shard_table_1 ADD COLUMN c2 INT;
    ```

    ```sql
    ALTER TABLE shard_db_1.shard_table_2 ADD COLUMN c2 INT;
    ```

2. `DM-worker-1` sends the DDL information related to `MySQL-1` to `DM-master`, and `DM-master` creates the corresponding DDL lock.
3. Use `show-ddl-lock` to check the information of the current DDL lock.

    ```bash
    » show-ddl-locks test
    {
        "result": true,
        "msg": "",
        "locks": [
            {
                "ID": "test-`shard_db`.`shard_table`",
                "task": "test",
                "owner": "127.0.0.1:8262",
                "DDLs": [
                    "USE `shard_db`; ALTER TABLE `shard_db`.`shard_table` ADD COLUMN `c2` int(11);"
                ],
                "synced": [
                    "127.0.0.1:8262"
                ],
                "unsynced": [
                    "127.0.0.1:8263"
                ]
            }
        ]
    }
    ```

4. Due to the application demand, the `DM-worker-2` data in `MySQL-2` is no longer needed to be replicated to the downstream TiDB, and `DM-worker-2` is made offline.
5. The lock whose ID is ```test-`shard_db`.`shard_table` ``` on `DM-master` cannot receive the DDL information of `DM-worker-2`.

    - The returned result `unsynced` by `show-ddl-locks` has always included the information of `DM-worker-2` (`127.0.0.1:8263`).
6. Use `unlock-dll-lock` to ask `DM-master` to actively unlock the DDL lock.
    - If the owner of the DDL lock has gone offline, you can use the parameter `--owner` to specify another DM-worker as the new owner to execute the DDL.
    - If any DM-worker reports an error, `result` will be set to `false`, and at this point you should check carefully if the errors of each DM-worker is acceptable and within expectations.

        - DM-workers that have gone offline will return the error `rpc error: code = Unavailable`, which is within expectations and can be neglected; but if other online DM-workers return errors, then you should deal with them based on the scenario.

        ```bash
        » unlock-ddl-lock test-`shard_db`.`shard_table`
        {
            "result": false,
            "msg": "github.com/pingcap/tidb-enterprise-tools/dm/master/server.go:1472: DDL lock test-`shard_db`.`shard_table` owner ExecuteDDL successfully, so DDL lock removed. but some dm-workers ExecuteDDL fail, you should to handle dm-worker directly",
            "workers": [
                {
                    "result": true,
                    "worker": "127.0.0.1:8262",
                    "msg": ""
                },
                {
                    "result": false,
                    "worker": "127.0.0.1:8263",
                    "msg": "rpc error: code = Unavailable desc = all SubConns are in TransientFailure, latest connection error: connection error: desc = \"transport: Error while dialing dial tcp 127.0.0.1:8263: connect: connection refused\""
                }
            ]
        }
        ```

7. Use `show-ddl-locks` to confirm if the DDL lock is unlocked successfully.

    ```bash
    » show-ddl-locks test
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

9. Use `query-status` to confirm if the replication task is normal.

#### Impact

After you have manually unlocked the lock by using `unlock-ddl-lock`, if you don't deal with the offline DM-workers included in the task configuration information, the lock might still be unable to be replicated automatically when the next sharding DDL event is received.

Therefore, after you have manually unlocked the DDL lock, you should perform the following operations:

1. Use `stop-task` to stop the running tasks.
2. Update the task configuration file, and remove the related information of the offline DM-worker from the configuration file.
3. Use `start-task` and the new task configuration file to restart the task.

> **Note:**
>
> After you run `unlock-ddl-lock`, if the DM-worker that went offline becomes online again and tries to replicate the data of the sharded tables, a match error between the data and the downstream table structure might occur.

### Scenario 2: Some DM-workers restart during the DDL unlocking process

#### The reason for the abnormal lock

After `DM-master` receives the DDL events of all DM-workers, automatically running `unlock DDL lock` mainly include the following steps:

1. Ask the owner of the lock to execute the DDL and update the checkpoints of corresponding sharded tables.
2. Remove the DDL lock information stored on `DM-master` after the owner successfully executes the DDL.
3. Ask all other DM-workers to skip the DDL and update the checkpoints of corresponding sharded tables after the owner successfully executes the DDL.

Currently, the above unlocking process is not atomic. Therefore, after the owner successfully executes the DDL, if a DM-worker restarts during the period of asking other DM-workers to skip the DDL, then the DM-worker might fail to skip the DDL.

At this point, the lock information on `DM-master` has been removed and the restarted DM-worker will continue to replicate the DDL, but as other DM-workers (including the previous owner) has replicated the DDL and continued the replication process, this DM-worker will never see the DDL lock be unlocked automatically.

#### Manual solution

Suppose that now we have the same upstream and downstream table structures and the same demand for merging tables and replication as in the manual solution of [Some DM-workers go offline](#scenario-1-some-dm-workers-go-offline).

When `DM-master` automatically executes the unlocking process, the owner (`DM-worker-1`) successfully executes the DDL and continues the replication process, and the DDL lock information has been removed from `DM-master`. But at this point, if `DM-worker-2` restarts during the period of asking `DM-worker-2` to skip the DDL, then the skipping process might fail.

After `DM-worker-2` restarts, it will try to replicate the waiting DDL lock before it restarted. At this point, a new lock will be created on `DM-master`, and the DM-worker will become the owner of the lock (other DM-workers have executed/skipped the DDL by now and are continuing the replication process).

The operation processes are:

1. Use `show-ddl-locks` to confirm if the corresponding lock of the DDL exists on `DM-master`.

    Only the restarted DM-worker (`127.0.0.1:8263`) is at the `synced` state.

    ```bash
    » show-ddl-locks
    {
        "result": true,
        "msg": "",
        "locks": [
            {
                "ID": "test-`shard_db`.`shard_table`",
                "task": "test",
                "owner": "127.0.0.1:8263",
                "DDLs": [
                    "USE `shard_db`; ALTER TABLE `shard_db`.`shard_table` ADD COLUMN `c2` int(11);"
                ],
                "synced": [
                    "127.0.0.1:8263"
                ],
                "unsynced": [
                    "127.0.0.1:8262"
                ]
            }
        ]
    }
    ```

2. Use `unlock-ddl-lock` to ask `DM-master` to unlock the lock.

    - Use the parameter `--worker` to limit the operation to only target at the restarted DM-worker (`127.0.0.1:8263`).
    - The DM-worker will try to execute the DDL to the downstream again during the unlocking process (the owner before restarting has executed the DDL to the downstream), so as to make sure that the DDL can be executed multiple times.

        ```bash
        » unlock-ddl-lock --worker=127.0.0.1:8263 test-`shard_db`.`shard_table`
        {
            "result": true,
            "msg": "",
            "workers": [
                {
                    "result": true,
                    "worker": "127.0.0.1:8263",
                    "msg": ""
                }
            ]
        }
        ```

3. Use `show-ddl-locks` to confirm if the DDL lock has been successfully unlocked.
4. Use `query-status` to confirm if the replication task is normal.

#### Impact

After manually unlocking the lock, the following sharding DDL can be replicated automatically and normally.

### Scenario 3: Some DM-workers are temporarily unreachable during the DDL unlocking process

#### The reason for the abnormal lock

This scenario has the similar reason for the abnormal lock in [Scenario 3: Some DM-workers restart during the DDL unlocking process](#scenario-2-some-dm-workers-restart-during-the-ddl-unlocking-process). If the DM-worker is temporarily unreachable when you request the DM-worker to skip the DDL statement, this DM-worker might fail to skip the DDL statement. At this point, the lock information is removed from `DM-master`, but the DM-worker will continue to be waiting for a DDL lock which is no longer existing.

The difference between Scenario 3 and [Scenario 2: Some DM-workers restart during the DDL unlocking process](#scenario-2-some-dm-workers-restart-during-the-ddl-unlocking-process) is that the DM-master does not have a lock in Scenario 3, but the DM-master has a new lock in Scenario 2.

#### Manual solution

Suppose that now we have the same upstream and downstream table structures and the same demand for merging tables and replication as in the manual solution of [Some DM-workers go offline](#scenario-1-some-dm-workers-go-offline).

When `DM-master` automatically executes the unlocking operation, the owner (`DM-worker-1`) successfully executes the DDL and continues the replication process, and the DDL lock information has been removed from `DM-master`. But at this point, if `DM-worker-2` is temporarily unreachable due to the Internet failure during the period of asking `DM-worker-2` to skip the DDL, then the skipping process might fail.

The operation processes are:

1. Use `show-ddl-locks` to confirm if the corresponding lock of the DDL no longer exists on `DM-master`.
2. Use `query-status` to confirm if the DM-worker is still waiting for the lock to replicate.

    ```bash
    » query-status test
    {
        "result": true,
        "msg": "",
        "workers": [
            ...
            {
                ...
                "worker": "127.0.0.1:8263",
                "subTaskStatus": [
                    {
                        ...
                        "unresolvedDDLLockID": "test-`shard_db`.`shard_table`",
                        "sync": {
                            ...
                            "blockingDDLs": [
                                "USE `shard_db`; ALTER TABLE `shard_db`.`shard_table` ADD COLUMN `c2` int(11);"
                            ],
                            "unresolvedGroups": [
                                {
                                    "target": "`shard_db`.`shard_table`",
                                    "DDLs": [
                                        "USE `shard_db`; ALTER TABLE `shard_db`.`shard_table` ADD COLUMN `c2` int(11);"
                                    ],
                                    "firstPos": "(mysql-bin|000001.000003, 1752)",
                                    "synced": [
                                        "`shard_db_2`.`shard_table_1`",
                                        "`shard_db_2`.`shard_table_2`"
                                    ],
                                    "unsynced": [
                                    ]
                                }
                            ],
                            "synced": false
                        }
                    }
                ]
                ...
            }
        ]
    }
    ```

3. Use `break-ddl-lock` to compulsorily break the DDL lock which the DM-worker is waiting for.

    As the owner has executed the DDL to the downstream, you should use the parameter `--skip` to break the lock.

    ```bash
    » break-ddl-lock --worker=127.0.0.1:8263 --skip test
    {
        "result": true,
        "msg": "",
        "workers": [
            {
                "result": true,
                "worker": "127.0.0.1:8263",
                "msg": ""
            }
        ]
    }
    ```

4. Use `query-status` to confirm if the replication task is normal and no longer at the state of waiting for the lock.

#### Impact

After manually breaking the lock, the following sharding DDL can be replicated automatically and normally.
