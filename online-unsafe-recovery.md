---
title: Online Unsafe Recovery
summary: Learn how to use Online Unsafe Recovery.
---

# Online Unsafe Recovery

> **Warning:**
>
> Online Unsafe Recovery is a type of lossy recovery. If you use this feature, the integrity of data and data indexes cannot be guaranteed.

When permanently damaged replicas cause part of data on TiKV to be unreadable and unwritable, you can use the Online Unsafe Recovery feature to perform a lossy recovery operation.

## Feature description

In TiDB, the same data might be stored in multiple stores at the same time according to the replica rules defined by users. This guarantees that data is still readable and writable even if a single or a few stores are temporarily offline or damaged. However, when most or all replicas of a Region go offline during a short period of time, the Region becomes temporarily unavailable and cannot be read or written.

Suppose that multiple replicas of a data range encounter issues like permanent damage (such as disk damage), and these issues cause the stores to stay offline. In this case, this data range is temporarily unavailable. If you want the cluster back in use and also accept data rewind or data loss, in theory, you can re-form the majority of replicas by manually removing the failed replicas from the group. This allows application-layer services to read and write this data range (might be stale or empty) again.

In this case, if some stores with loss-tolerant data are permanently damaged, you can perform a lossy recovery operation by using Online Unsafe Recovery. When you use this feature, PD automatically pauses Region scheduling (including split and merge), collects the metadata of data shards from all stores, and then, under its global perspective, generates a real-time and complete recovery plan. Then, PD distributes the plan to all surviving stores to make them perform data recovery tasks. In addition, once the data recovery plan is distributed, PD periodically monitors the recovery progress and re-send the plan when necessary.

## User scenarios

The Online Unsafe Recovery feature is suitable for the following scenarios:

* The data for application services is unreadable and unwritable, because permanently damaged stores cause the stores to fail to restart.
* You can accept data loss and want the affected data to be readable and writable.
* You want to perform a one-stop online data recovery operation.

## Usage

### Prerequisites

Before using Online Unsafe Recovery, make sure that the following requirements are met:

* The offline stores indeed cause some pieces of data to be unavailable.
* The offline stores cannot be automatically recovered or restarted.

### Step 1. Specify the stores that cannot be recovered

To trigger automatic recovery, use PD Control to execute [`unsafe remove-failed-stores <store_id>[,<store_id>,...]`](/pd-control.md#unsafe-remove-failed-stores-store-ids--show) and specify **all** the TiKV nodes that cannot be recovered, seperated by commas.

{{< copyable "shell-regular" >}}

```bash
pd-ctl -u <pd_addr> unsafe remove-failed-stores <store_id1,store_id2,...>
```

If the command returns `Success`, PD Control has successfully registered the task to PD. This only means that the request has been accepted, not that the recovery has been successfully performed. The recovery task is performed in the background. To see the recovery progress, use [`show`](#step-2-check-the-recovery-progress-and-wait-for-the-completion).

If the command returns `Failed`, PD Control has failed to register the task to PD. The possible errors are as follows:

- `unsafe recovery is running`: There is already an ongoing recovery task.
- `invalid input store x doesn't exist`: The specified store ID does not exist.
- `invalid input store x is up and connected`: The specified store with the ID is still healthy and should not be recovered.

To specify the longest allowable duration of a recovery task, use the `--timeout <seconds>` option. If this option is not specified, the longest duration is 5 minutes by default. When the timeout occurs, the recovery is interrupted and returns an error.

> **Note:**
>
> - Because this command needs to collect information from all peers, it might cause an increase in memory usage (100,000 peers are estimated to use 500 MiB of memory).
> - If PD restarts when the command is running, the recovery is interrupted and you need to trigger the task again.
> - Once the command is running, the specified stores will be set to the Tombstone status, and you cannot restart these stores.
> - When the command is running, all scheduling tasks and split/merge are paused and will be resumed automatically after the recovery is successful or fails.

### Step 2. Check the recovery progress and wait for the completion

When the above store removal command runs successfully, you can use PD Control to check the removal progress by running [`unsafe remove-failed-stores show`](/pd-control.md#config-show--set-option-value--placement-rules).

{{< copyable "shell-regular" >}}

```bash
pd-ctl -u <pd_addr> unsafe remove-failed-stores show
```

The recovery process has multiple possible stages:

- `collect report`: The initial stage in which PD collects reports from TiKV and gets global information.
- `tombstone tiflash learner`: Among the unhealthy Regions, delete the TiFlash learners that are newer than other healthy peers, to prevent such an extreme situation and the possible panic.
- `force leader for commit merge`: A special stage. When there is an uncompleted commit merge, `force leader` is first performed on the Regions with commit merge, in case of extreme situations.
- `force leader`: Forces unhealthy Regions to assign a Raft leader among the remaining healthy peers.
- `demote failed voter`: Demotes the Region's failed voters to learners, and then the Regions can select a Raft leader as normal.
- `create empty region`: Creates an empty Region to fill in the space in the key range. This is to resolve the case that the stores with all replicas of some Regions have been damaged.

Each of the above stages is output in the JSON format, including information, time, and a detailed recovery plan. For example:

```json
[
    {
        "info": "Unsafe recovery enters collect report stage: failed stores 4, 5, 6",
        "time": "......"
    },
    {
        "info": "Unsafe recovery enters force leader stage",
        "time": "......",
        "actions": {
            "store 1": [
                "force leader on regions: 1001, 1002"
            ],
            "store 2": [
                "force leader on regions: 1003"
            ]
        }
    },
    {
        "info": "Unsafe recovery enters demote failed voter stage",
        "time": "......",
        "actions": {
            "store 1": [
                "region 1001 demotes peers { id:101 store_id:4 }, { id:102 store_id:5 }",
                "region 1002 demotes peers { id:103 store_id:5 }, { id:104 store_id:6 }",
            ],
            "store 2": [
                "region 1003 demotes peers { id:105 store_id:4 }, { id:106 store_id:6 }",
            ]
        }
    },
    {
        "info": "Collecting reports from alive stores(1/3)",
        "time": "......",
        "details": [
            "Stores that have not dispatched plan: ",
            "Stores that have reported to PD: 4",
            "Stores that have not reported to PD: 5, 6",
        ]
    }
]
```

After PD has successfully dispatched the recovery plan, it waits for TiKV to report the execution results. As you can see in `Collecting reports from alive stores`, the last stage of the above output, this part of the output shows the detailed statuses of PD dispatching recovery plan and receiving reports from TiKV.

The whole recovery process takes multiple stages and one stage might be retried multiple times. Usually, the estimated duration is 3 to 10 periods of store heartbeat (one period of store heartbeat is 10 seconds by default). After the recovery is completed, the last stage in the command output shows `"Unsafe recovery finished"`, the table IDs to which the affected Regions belong (if there is none or RawKV is used, the output does not show the table IDs), and the affected SQL meta Regions. For example:

```json
{
    "info": "Unsafe recovery finished",
    "time": "......",
    "details": [
        "Affected table ids: 64, 27",
        "Affected meta regions: 1001",
    ]
}
```

After you get the affected table IDs, you can query `INFORMATION_SCHEMA.TABLES` to view the affected table names.

```sql
SELECT TABLE_SCHEMA, TABLE_NAME, TIDB_TABLE_ID FROM INFORMATION_SCHEMA.TABLES WHERE TIDB_TABLE_ID IN (64, 27);
```

> **Note:**
>
> - The recovery operation has turned some failed voters to failed learners. Then PD scheduling needs some time to remove these failed learners.
> - It is recommended to add new stores in time.

If an error occurs during the task, the last stage in the output shows `"Unsafe recovery failed"` and the error message. For example:

```json
{
    "info": "Unsafe recovery failed: <error>",
    "time": "......"
}
```

### Step 3. Check the consistency of data and index (not required for RawKV)

> **Note:**
>
> Although the data can be read and written, it does not mean that there is no data loss.

After the recovery is completed, the data and index might be inconsistent. Use the SQL command [`ADMIN CHECK`](/sql-statements/sql-statement-admin-check-table-index.md) to check the data and index consistency of the affected tables

```sql
ADMIN CHECK TABLE table_name;
```

If there are inconsistent indexes, you can fix the index inconsistency by renaming the old index, creating a new index, and then droping the old index.

1. Rename the old index:

    ```sql
    ALTER TABLE table_name RENAME INDEX index_name TO index_name_lame_duck;
    ```

2. Create a new index:

    ```sql
    ALTER TABLE table_name ADD INDEX index_name (column_name);
    ```

3. Drop the old index:

    ```sql
    ALTER TABLE table_name DROP INDEX index_name_lame_duck;
    ```

### Step 4: Remove unrecoverable stores (optional)

<SimpleTab>
<div label="Stores deployed using TiUP">

1. Remove the unrecoverable nodes:

    ```bash
    tiup cluster scale-in <cluster-name> -N <host> --force
    ```

2. Clean up Tombstone nodes:

    ```bash
    tiup cluster prune <cluster-name>
    ```

</div>
<div label="Stores deployed using TiDB Operator">

1. Delete the `PersistentVolumeClaim`.

    {{< copyable "shell-regular" >}}

    ```bash
    kubectl delete -n ${namespace} pvc ${pvc_name} --wait=false
    ```

2. Delete the TiKV Pod and wait for newly created TiKV Pods to join the cluster.

    {{< copyable "shell-regular" >}}

    ```bash
    kubectl delete -n ${namespace} pod ${pod_name}
    ```

</div>
</SimpleTab>
