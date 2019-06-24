---
title: Troubleshooting Sharding DDL Locks
summary: Learn how to troubleshoot sharding DDL locks in different abnormal conditions.
category: tools
---

# Troubleshooting Sharding DDL Locks

The Data Migration tool uses a sharding DDL lock to ensure operations are applied in the correct order. This locking mechanism works automatically, but in some abnormal conditions you might need to perform manual operations such as force-releasing the lock.

This document shows how to troubleshoot sharding DDL locks in different abnormal conditions.

The possible causes of an abnormal condition include:

- Some DM-workers go offline
- A DM-worker restarts (or is unreachable temporarily)
- DM-master restarts

> **Warning:**
>
> Do not use `unlock-ddl-lock`/`break-ddl-lock` unless you are definitely clear about the possible impacts brought by this command and you can accept the impacts.

## Condition one: some DM-workers go offline

Before the DM-master tries to automatically unlock the sharding DDL lock, all the DM-workers need to receive the sharding DDL event. If the sharding DDL operation is already in the replication process, and some DM-workers have gone offline and are not to be restarted, then the sharding DDL lock cannot be automatically replicated and unlocked because not all the DM-workers can receive the DDL event.

If you do not need to make some DM-workers offline in the process of replicating sharding DDL statements, a better solution is using `stop-task` to stop the running task first, then make the DM-workers offline, and finally use `start-task` and the **new task configuration** that does not contain the already offline DM-workers to restart the task.

If the owner goes offline when the owner has finished executing the DDL statement but other DM-workers have not skipped this DDL statement. For the solution, see [Condition two: a DM-worker restarts](#condition-two-a-dm-worker-restarts-or-is-unreachable-temporarily).

### Manual solution

1. Run `show-ddl-locks` to obtain the information of the sharding DDL lock that is currently pending replication. 

2. Run the `unlock-ddl-lock` command to specify the information of the lock to be unlocked manually.

    - If the owner of this lock is offline, you can configure the `--owner` parameter to specify another DM-worker as the new owner to execute the DDL statement.

3. Run `show-ddl-locks` to check whether this lock has been successfully unlocked.

### Impact

After you have manually unlocked the lock, it still might exist that the lock cannot be automatically replicated when the next sharding DDL event is received, because the offline DM-workers are included in the task configuration information.

Therefore, after you have manually unlocked the DM-workers, you need to use `stop-task`/`start-task` and the updated task configuration that does not include offline DM-workers to restart the task.

> **Note:**
>
> If the DM-workers that went offline become online again after you run `unlock-ddl-lock`, it means: These DM-workers will replicate the unlocked DDL operation again. (Other DM-workers that were not offline have replicated the DDL statement.) The DDL operation of these DM-workers will try to match the subsequent replicated DDL statements of other DM-workers. A match error of replicating sharding DDL statements of different DM-workers might occur.

## Condition two: a DM-worker restarts (or is unreachable temporarily)

Currently, the DDL unlocking process is not atomic, during which the DM-master schedules multiple DM-workers to execute or skip the sharding DDL statement and updates the checkpoint. Therefore, it might exist that after the owner finishes executing the DDL statement, a non-owner restarts before it skips this DDL statement and updates the checkpoint. At this time, the lock information on the DM-master has been removed but the restarted DM-worker has failed to skip this DDL statement and update the checkpoint.

After the DM-worker restarts and runs `start-task`, it retries to replicate the sharding DDL statement. But as other DM-workers have finished replicating this DDL statement, the restarted DM-worker cannot replicate or skip this DDL statement.

### Manual solution

1. Run `query-status` to check the information of the sharding DDL statement that the restarted DM-worker is currently blocking. 

2. Run `break-ddl-lock` to specify the DM-worker that is to break the lock forcefully.
    
    - Specify `skip` to skip the sharding DDL statement.

3. Run `query-status` to check whether the lock has been successfully broken.

### Impact

No bad impact. After you have manually broken the lock, the subsequent sharding DDL statements can be automatically replicated normally.

## Condition three: DM-master restarts

After a DM-worker sends the sharding DDL information to DM-master, this DM-worker will hang up, wait for the message from DM-master, and then decide whether to execute or skip this DDL statement.

Because the state of DM-master is not persistent, the lock information that a DM-worker sends to DM-master will be lost if DM-master restarts.

Therefore, DM-master cannot schedule the DM-worker to execute or skip the DDL statement after DM-master restarts due to lock information loss.

### Manual solution

1. Run `show-ddl-locks` to verify whether the sharding DDL lock information is lost.
2. Run `query-status` to verify whether the DM-worker is blocked as it is waiting for replication of the sharding DDL lock.
3. Run `pause-task` to pause the blocked task.
4. Run `resume-task` to resume the blocked task and restart replicating the sharding DDL lock.

### Impact

No bad impact. After you have manually paused and resumed the task, the DM-worker resumes replicating the sharding DDL lock and sends the lost lock information to DM-master. The subsequent sharding DDL statements can be replicated normally.

## Parameter description of sharding DDL lock commands

### `show-ddl-locks`

- `task-name`: 
    
    - Non-flag parameter, string, optional
    - If it is not set, no specific task is queried; if it is set, only this task is queried.

- `worker`:
    
    - Flag parameter, string array, `--worker`, optional
    - Can be specified repeatedly multiple times.
    - If it is set, only the DDL lock information related to these DM-workers is to be queried.

#### `unlock-ddl-lock`

- `lock-ID`: 

    - Non-flag parameter, string, required
    - Specifies the ID of the DDL lock that to be unlocked (this ID can be obtained by `show-ddl-locks`)

- `owner`: 
    
    - Flag parameter, string, `--owner`, optional
    - If it is set, this value should correspond to a DM-worker that substitutes for the default owner to execute the DDL statement of the lock.

- `force-remove`: 
    
    - Flag parameter, boolean, `--force-remove`, optional
    - If it is set, the lock information is removed even though the owner fails to execute the DDL statement. The owner cannot retry or perform other operations on this DDL statement.

- `worker`: 
    
    - Flag parameter, string array, `--worker`, optional
    - Can be specified repeatedly multiple times.
    - If it is not set, all the DM-workers to receive the lock event execute or skip the DDL statement. If it is set, only the specified DM-workers execute or skip the DDL statement.

#### `break-ddl-lock`

- `task-name`: 
    
    - Non-flag parameter, string, required
    - Specifies the name of the task where the lock to be broken is located.

- `worker`: 

    - Flag parameter, string, `--worker`, required
    - You must specify one and can only specify one.
    - Specifies the DM-worker that is to break the lock.

- `remove-id`: 

    - Flag parameter, string, `--remove-id`, optional
    - If it is set, the value should be the ID of a DDL lock. Then the information about the DDL lock recorded in the DM-worker is removed.
    
- `exec`: 

    - Flag parameter, boolean, `--exec`, optional
    - If it is set, a specific DM-worker executes the DDL statement corresponding to the lock.
    - You cannot specify `exec` and `skip` at the same time.

- `skip`: 
    
    - Flag parameter, boolean, `--skip`, optional
    - If it is set, a specific DM-worker skips the DDL operation of the lock.
    - You cannot specify `exec` and `skip` at the same time.
