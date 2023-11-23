---
title: Manage Changefeeds
summary: Learn how to manage TiCDC changefeeds.
aliases: ['/tidb/dev/manage-ticdc']
---

# Manage Changefeeds

This document describes how to create and manage TiCDC changefeeds by using the TiCDC command-line tool `cdc cli`. You can also manage changefeeds via the HTTP interface of TiCDC. For details, see [TiCDC OpenAPI](/ticdc/ticdc-open-api.md).

## Create a replication task

Run the following command to create a replication task:

```shell
cdc cli changefeed create --server=http://10.0.10.25:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task"
```

```shell
Create changefeed successfully!
ID: simple-replication-task
Info: {"upstream_id":7178706266519722477,"namespace":"default","id":"simple-replication-task","sink_uri":"mysql://root:xxxxx@127.0.0.1:4000/?time-zone=","create_time":"2023-11-28T15:05:46.679218+08:00","start_ts":438156275634929669,"engine":"unified","config":{"case_sensitive":false,"enable_old_value":true,"force_replicate":false,"ignore_ineligible_table":false,"check_gc_safe_point":true,"enable_sync_point":true,"bdr_mode":false,"sync_point_interval":30000000000,"sync_point_retention":3600000000000,"filter":{"rules":["test.*"],"event_filters":null},"mounter":{"worker_num":16},"sink":{"protocol":"","schema_registry":"","csv":{"delimiter":",","quote":"\"","null":"\\N","include_commit_ts":false},"column_selectors":null,"transaction_atomicity":"none","encoder_concurrency":16,"terminator":"\r\n","date_separator":"none","enable_partition_separator":false},"consistent":{"level":"none","max_log_size":64,"flush_interval":2000,"storage":""}},"state":"normal","creator_version":"v7.5.0"}
```

## Query the replication task list

Run the following command to query the replication task list:

```shell
cdc cli changefeed list --server=http://10.0.10.25:8300
```

```shell
[{
    "id": "simple-replication-task",
    "summary": {
      "state": "normal",
      "tso": 417886179132964865,
      "checkpoint": "2020-07-07 16:07:44.881",
      "error": null
    }
}]
```

- `checkpoint` indicates that TiCDC has already replicated data before this time point to the downstream.
- `state` indicates the state of the replication task.
    - `normal`: The replication task runs normally.
    - `stopped`: The replication task is stopped (manually paused).
    - `error`: The replication task is stopped (by an error).
    - `removed`: The replication task is removed. Tasks of this state are displayed only when you have specified the `--all` option. To see these tasks when this option is not specified, run the `changefeed query` command.
    - `finished`: The replication task is finished (data is replicated to the `target-ts`). Tasks of this state are displayed only when you have specified the `--all` option. To see these tasks when this option is not specified, run the `changefeed query` command.

## Query a specific replication task

To query a specific replication task, run the `changefeed query` command. The query result includes the task information and the task state. You can specify the `--simple` or `-s` argument to simplify the query result that will only include the basic replication state and the checkpoint information. If you do not specify this argument, detailed task configuration, replication states, and replication table information are output.

```shell
cdc cli changefeed query -s --server=http://10.0.10.25:8300 --changefeed-id=simple-replication-task
```

```shell
{
 "state": "normal",
 "tso": 419035700154597378,
 "checkpoint": "2020-08-27 10:12:19.579",
 "error": null
}
```

In the preceding command and result:

+ `state` is the replication state of the current changefeed. Each state must be consistent with the state in `changefeed list`.
+ `tso` represents the largest transaction TSO in the current changefeed that has been successfully replicated to the downstream.
+ `checkpoint` represents the corresponding time of the largest transaction TSO in the current changefeed that has been successfully replicated to the downstream.
+ `error` records whether an error has occurred in the current changefeed.

```shell
cdc cli changefeed query --server=http://10.0.10.25:8300 --changefeed-id=simple-replication-task
```

```shell
{
  "info": {
    "sink-uri": "mysql://127.0.0.1:3306/?max-txn-row=20\u0026worker-number=4",
    "opts": {},
    "create-time": "2020-08-27T10:33:41.687983832+08:00",
    "start-ts": 419036036249681921,
    "target-ts": 0,
    "admin-job-type": 0,
    "sort-engine": "unified",
    "sort-dir": ".",
    "config": {
      "case-sensitive": false,
      "filter": {
        "rules": [
          "*.*"
        ],
        "ignore-txn-start-ts": null,
        "ddl-allow-list": null
      },
      "mounter": {
        "worker-num": 16
      },
      "sink": {
        "dispatchers": null,
      },
      "scheduler": {
        "type": "table-number",
        "polling-time": -1
      }
    },
    "state": "normal",
    "history": null,
    "error": null
  },
  "status": {
    "resolved-ts": 419036036249681921,
    "checkpoint-ts": 419036036249681921,
    "admin-job-type": 0
  },
  "count": 0,
  "task-status": [
    {
      "capture-id": "97173367-75dc-490c-ae2d-4e990f90da0f",
      "status": {
        "tables": {
          "47": {
            "start-ts": 419036036249681921
          }
        },
        "operation": null,
        "admin-job-type": 0
      }
    }
  ]
}
```

In the  preceding command and result:

- `info` is the replication configuration of the queried changefeed.
- `status` is the replication state of the queried changefeed.
    - `resolved-ts`: The largest transaction `TS` in the current changefeed. Note that this `TS` has been successfully sent from TiKV to TiCDC.
    - `checkpoint-ts`: The largest transaction `TS` in the current `changefeed`. Note that this `TS` has been successfully written to the downstream.
    - `admin-job-type`: The status of a changefeed:
        - `0`: The state is normal.
        - `1`: The task is paused. When the task is paused, all replicated `processor`s exit. The configuration and the replication status of the task are retained, so you can resume the task from `checkpiont-ts`.
        - `2`: The task is resumed. The replication task resumes from `checkpoint-ts`.
        - `3`: The task is removed. When the task is removed, all replicated `processor`s are ended, and the configuration information of the replication task is cleared up. Only the replication status is retained for later queries.
- `task-status` indicates the state of each replication sub-task in the queried changefeed.

## Pause a replication task

Run the following command to pause a replication task:

```shell
cdc cli changefeed pause --server=http://10.0.10.25:8300 --changefeed-id simple-replication-task
```

In the preceding command:

- `--changefeed-id=uuid` represents the ID of the changefeed that corresponds to the replication task you want to pause.

## Resume a replication task

Run the following command to resume a paused replication task:

```shell
cdc cli changefeed resume --server=http://10.0.10.25:8300 --changefeed-id simple-replication-task
```

- `--changefeed-id=uuid` represents the ID of the changefeed that corresponds to the replication task you want to resume.
- `--overwrite-checkpoint-ts`: starting from v6.2.0, you can specify the starting TSO of resuming the replication task. TiCDC starts pulling data from the specified TSO. The argument accepts `now` or a specific TSO (such as 434873584621453313). The specified TSO must be in the range of (GC safe point, CurrentTSO]. If this argument is not specified, TiCDC replicates data from the current `checkpoint-ts` by default.
- `--no-confirm`: when the replication is resumed, you do not need to confirm the related information. Defaults to `false`.

> **Note:**
>
> - If the TSO specified in `--overwrite-checkpoint-ts` (`t2`) is larger than the current checkpoint TSO in the changefeed (`t1`), data between `t1` and `t2` will not be replicated to the downstream. This causes data loss. You can obtain `t1` by running `cdc cli changefeed query`.
> - If the TSO specified in `--overwrite-checkpoint-ts` (`t2`) is smaller than the current checkpoint TSO in the changefeed (`t1`), TiCDC pulls data from an old time point (`t2`), which might cause data duplication (for example, if the downstream is MQ sink).

## Remove a replication task

Run the following command to remove a replication task:

```shell
cdc cli changefeed remove --server=http://10.0.10.25:8300 --changefeed-id simple-replication-task
```

In the preceding command:

- `--changefeed-id=uuid` represents the ID of the changefeed that corresponds to the replication task you want to remove.

## Update task configuration

TiCDC supports modifying the configuration of the replication task (not dynamically). To modify the changefeed configuration, pause the task, modify the configuration, and then resume the task.

```shell
cdc cli changefeed pause -c test-cf --server=http://10.0.10.25:8300
cdc cli changefeed update -c test-cf --server=http://10.0.10.25:8300 --sink-uri="mysql://127.0.0.1:3306/?max-txn-row=20&worker-number=8" --config=changefeed.toml
cdc cli changefeed resume -c test-cf --server=http://10.0.10.25:8300
```

Currently, you can modify the following configuration items:

- `sink-uri` of the changefeed.
- The changefeed configuration file and all configuration items in the file.
- The `target-ts` of the changefeed.

## Manage processing units of replication sub-tasks (`processor`)

- Query the `processor` list:

    ```shell
    cdc cli processor list --server=http://10.0.10.25:8300
    ```

    ```shell
    [
            {
                    "id": "9f84ff74-abf9-407f-a6e2-56aa35b33888",
                    "capture-id": "b293999a-4168-4988-a4f4-35d9589b226b",
                    "changefeed-id": "simple-replication-task"
            }
    ]
    ```

- Query a specific changefeed which corresponds to the status of a specific replication task:

    ```shell
    cdc cli processor query --server=http://10.0.10.25:8300 --changefeed-id=simple-replication-task --capture-id=b293999a-4168-4988-a4f4-35d9589b226b
    ```

    ```shell
    {
      "status": {
        "tables": {
          "56": {    # 56 ID of the replication table, corresponding to tidb_table_id of a table in TiDB
            "start-ts": 417474117955485702
          }
        },
        "operation": null,
        "admin-job-type": 0
      },
      "position": {
        "checkpoint-ts": 417474143881789441,
        "resolved-ts": 417474143881789441,
        "count": 0
      }
    }
    ```

    In the preceding command:

    - `status.tables`: Each key number represents the ID of the replication table, corresponding to `tidb_table_id` of a table in TiDB.
    - `resolved-ts`: The largest TSO among the sorted data in the current processor.
    - `checkpoint-ts`: The largest TSO that has been successfully written to the downstream in the current processor.

## Replicate tables with the new framework for collations enabled

Starting from v4.0.15, v5.0.4, v5.1.1 and v5.2.0, TiCDC supports tables that have enabled [new framework for collations](/character-set-and-collation.md#new-framework-for-collations).

## Replicate tables without a valid index

Since v4.0.8, TiCDC supports replicating tables that have no valid index by modifying the task configuration. To enable this feature, configure in the changefeed configuration file as follows:

```toml
force-replicate = true
```

> **Warning:**
>
> When `force-replicate` is set to `true`, data consistency is not guaranteed. For tables without a valid index, operations such as `INSERT` and `REPLACE` are not reentrant, so there is a risk of data redundancy. TiCDC guarantees that data is distributed only at least once during the replication process. Therefore, enabling this feature to replicate tables without a valid index will definitely cause data redundancy. If you do not accept data redundancy, it is recommended to add an effective index, such as adding a primary key column with the `AUTO RANDOM` attribute.

## Unified Sorter

> **Note:**
>
> Starting from v6.0.0, TiCDC uses the DB Sorter engine by default, and no longer uses the Unified Sorter. It is recommended that you do not configure the `sort engine` item.

Unified sorter is the sorting engine in TiCDC. It can mitigate OOM problems caused by the following scenarios:

+ The data replication task in TiCDC is paused for a long time, during which a large amount of incremental data is accumulated and needs to be replicated.
+ The data replication task is started from an early timestamp so it becomes necessary to replicate a large amount of incremental data.

For the changefeeds created using `cdc cli` after v4.0.13, Unified Sorter is enabled by default; for the changefeeds that have existed before v4.0.13, the previous configuration is used.

To check whether or not the Unified Sorter feature is enabled on a changefeed, you can run the following example command (assuming the IP address of the PD instance is `http://10.0.10.25:2379`):

```shell
cdc cli --server="http://10.0.10.25:8300" changefeed query --changefeed-id=simple-replication-task | grep 'sort-engine'
```

In the output of the above command, if the value of `sort-engine` is "unified", it means that Unified Sorter is enabled on the changefeed.

> **Note:**
>
> + If your servers use mechanical hard drives or other storage devices that have high latency or limited bandwidth, the performance of Unified Sorter will be affected significantly.
> + By default, Unified Sorter uses `data_dir` to store temporary files. It is recommended to ensure that the free disk space is greater than or equal to 500 GiB. For production environments, it is recommended to ensure that the free disk space on each node is greater than (the maximum `checkpoint-ts` delay allowed by the business) * (upstream write traffic at business peak hours). In addition, if you plan to replicate a large amount of historical data after `changefeed` is created, make sure that the free space on each node is greater than the amount of the replicated data.
