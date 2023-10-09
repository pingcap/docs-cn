---
title: TiCDC OpenAPI v2
summary: Learn how to use the OpenAPI v2 interface to manage the cluster status and data replication.
---

# TiCDC OpenAPI v2

<!-- markdownlint-disable MD024 -->

TiCDC provides the OpenAPI feature for querying and operating the TiCDC cluster. The OpenAPI feature is a subset of the [`cdc cli` tool](/ticdc/ticdc-manage-changefeed.md).

> **Note:**
>
> TiCDC OpenAPI v1 will be removed in the future. It is recommended to use TiCDC OpenAPI v2.

You can use the APIs to perform the following maintenance operations on the TiCDC cluster:

- [Get the status information of a TiCDC node](#get-the-status-information-of-a-ticdc-node)
- [Check the health status of a TiCDC cluster](#check-the-health-status-of-a-ticdc-cluster)
- [Create a replication task](#create-a-replication-task)
- [Remove a replication task](#remove-a-replication-task)
- [Update the replication configuration](#update-the-replication-configuration)
- [Query the replication task list](#query-the-replication-task-list)
- [Query a specific replication task](#query-a-specific-replication-task)
- [Pause a replication task](#pause-a-replication-task)
- [Resume a replication task](#resume-a-replication-task)
- [Query the replication subtask list](#query-the-replication-subtask-list)
- [Query a specific replication subtask](#query-a-specific-replication-subtask)
- [Query the TiCDC service process list](#query-the-ticdc-service-process-list)
- [Evict an owner node](#evict-an-owner-node)
- [Dynamically adjust the log level of the TiCDC server](#dynamically-adjust-the-log-level-of-the-ticdc-server)

The request body and returned values of all APIs are in JSON format. A successful request returns a `200 OK` message. The following sections describe the specific usage of the APIs.

In the following examples, the listening IP address of the TiCDC server is `127.0.0.1` and the port is `8300`. You can specify the IP address and port bound to TiCDC via `--addr=ip:port` when starting the TiCDC server.

## API error message template

After an API request is sent, if an error occurs, the returned error message is in the following format:

```json
{
    "error_msg": "",
    "error_code": ""
}
```

In the above JSON output, `error_msg` describes the error message and `error_code` is the corresponding error code.

## Return format of the API List interface

If an API request returns a list of resources (for example, a list of all `Captures`), the TiCDC return format is as follows:

```json
{
  "total": 2,
  "items": [
    {
      "id": "d2912e63-3349-447c-90ba-wwww",
      "is_owner": true,
      "address": "127.0.0.1:8300"
    },
    {
      "id": "d2912e63-3349-447c-90ba-xxxx",
      "is_owner": false,
      "address": "127.0.0.1:8302"
    }
  ]
}
```

In the above example:

- `total`: indicates the total number of resources.
- `items`: an array that contains all the resources returned by this request. All elements of the array are of the same resource.

## Get the status information of a TiCDC node

This API is a synchronous interface. If the request is successful, the status information of the corresponding node is returned.

### Request URI

`GET /api/v2/status`

### Example

The following request gets the status information of the TiCDC node whose IP address is `127.0.0.1` and port number is `8300`.

```shell
curl -X GET http://127.0.0.1:8300/api/v2/status
```

```json
{
  "version": "v7.3.0",
  "git_hash": "10413bded1bdb2850aa6d7b94eb375102e9c44dc",
  "id": "d2912e63-3349-447c-90ba-72a4e04b5e9e",
  "pid": 1447,
  "is_owner": true,
  "liveness": 0
}
```

The parameters of the above output are described as follows:

- `version`: the current version number of TiCDC.
- `git_hash`: the Git hash value.
- `id`: the capture ID of the node.
- `pid`: the capture process ID (PID) of the node.
- `is_owner`: indicates whether the node is an owner.
- `liveness`: whether this node is live. `0` means normal. `1` means that the node is in the `graceful shutdown` state.

## Check the health status of a TiCDC cluster

This API is a synchronous interface. If the cluster is healthy, `200 OK` is returned.

### Request URI

`GET /api/v2/health`

### Example

```shell
curl -X GET http://127.0.0.1:8300/api/v2/health
```

If the cluster is healthy, the response is `200 OK` and an empty JSON object:

```json
{}
```

If the cluster is not healthy, the response is a JSON object containing the error message.

## Create a replication task

This interface is used to submit a replication task to TiCDC. If the request is successful, `200 OK` is returned. The returned result only means that the server agrees to run the command but does not guarantee that the command will be run successfully.

### Request URI

`POST /api/v2/changefeeds`

### Parameter descriptions

```json
{
  "changefeed_id": "string",
  "replica_config": {
    "bdr_mode": true,
    "case_sensitive": true,
    "check_gc_safe_point": true,
    "consistent": {
      "flush_interval": 0,
      "level": "string",
      "max_log_size": 0,
      "storage": "string"
    },
    "enable_old_value": true,
    "enable_sync_point": true,
    "filter": {
      "do_dbs": [
        "string"
      ],
      "do_tables": [
        {
          "database_name": "string",
          "table_name": "string"
        }
      ],
      "event_filters": [
        {
          "ignore_delete_value_expr": "string",
          "ignore_event": [
            "string"
          ],
          "ignore_insert_value_expr": "string",
          "ignore_sql": [
            "string"
          ],
          "ignore_update_new_value_expr": "string",
          "ignore_update_old_value_expr": "string",
          "matcher": [
            "string"
          ]
        }
      ],
      "ignore_dbs": [
        "string"
      ],
      "ignore_tables": [
        {
          "database_name": "string",
          "table_name": "string"
        }
      ],
      "ignore_txn_start_ts": [
        0
      ],
      "rules": [
        "string"
      ]
    },
    "force_replicate": true,
    "ignore_ineligible_table": true,
    "memory_quota": 0,
    "mounter": {
      "worker_num": 0
    },
    "sink": {
      "column_selectors": [
        {
          "columns": [
            "string"
          ],
          "matcher": [
            "string"
          ]
        }
      ],
      "csv": {
        "delimiter": "string",
        "include_commit_ts": true,
        "null": "string",
        "quote": "string"
      },
      "date_separator": "string",
      "dispatchers": [
        {
          "matcher": [
            "string"
          ],
          "partition": "string",
          "topic": "string"
        }
      ],
      "enable_partition_separator": true,
      "encoder_concurrency": 0,
      "protocol": "string",
      "schema_registry": "string",
      "terminator": "string",
      "transaction_atomicity": "string"
    },
    "sync_point_interval": "string",
    "sync_point_retention": "string"
  },
  "sink_uri": "string",
  "start_ts": 0,
  "target_ts": 0
}
```

The parameters are described as follows:

| Parameter name | Description |
| :------------------------ | :----------------------------------------------------- |
| `changefeed_id` | `STRING` type. The ID of the replication task. (Optional) |
| `replica_config` | Configuration parameters for the replication task. (Optional) |
| **`sink_uri`** | `STRING` type. The downstream address of the replication task. (**Required**) |
| `start_ts` | `UINT64` type. Specifies the start TSO of the changefeed. The TiCDC cluster will start pulling data from this TSO. The default value is the current time. (Optional) |
| `target_ts` | `UINT64` type. Specifies the target TSO of the changefeed. The TiCDC cluster stops pulling data when reaching this TSO. The default value is empty, meaning TiCDC does not stop automatically. (Optional) |

The meaning and format of `changefeed_id`, `start_ts`, `target_ts`, and `sink_uri` are the same as those described in the [Use `cdc cli` to create a replication task](/ticdc/ticdc-manage-changefeed.md#create-a-replication-task) document. For the detailed description of these parameters, see that document. Note that when you specify the certificate path in `sink_uri`, make sure you have uploaded the corresponding certificate to the corresponding TiCDC server.

The descriptions of the `replica_config` parameters are as follows.

| Parameter name | Description |
| :------------------------ | :----------------------------------------------------- |
| `bdr_mode`                | `BOOLEAN` type. Determines whether to enable [bidirectional replication](/ticdc/ticdc-bidirectional-replication.md). The default value is `false`. (Optional)               |
| `case_sensitive`          | `BOOLEAN` type. Determines whether to be case-sensitive when filtering table names. The default value is `true`. (Optional)   |
| `check_gc_safe_point`     | `BOOLEAN` type. Determines whether to check that the start time of the replication task is earlier than the GC time. The default value is `true`. (Optional)                                  |
| `consistent`              | The configuration parameters of redo log. (Optional) |
| `enable_sync_point`       | `BOOLEAN` type. Determines whether to enable `sync point`. (Optional)         |
| `filter`                  | The configuration parameters of `filter`. (Optional)           |
| `force_replicate`         | `BOOLEAN` type. The default value is `false`. When you set it to `true`, the replication task forcibly replicates the tables without unique indexes. (Optional)                |
| `ignore_ineligible_table` | `BOOLEAN` type. The default value is `false`. When you set it to `true`, the replication task ignores the tables that cannot be replicated. (Optional)                     |
| `memory_quota`            | `UINT64` type. The memory quota for the replication task. (Optional)           |
| `mounter`                 | The  configuration parameters of `mounter`. (Optional)               |
| `sink`                    | The configuration parameters of `sink`. (Optional)                         |
| `sync_point_interval`     | `STRING` type. Note that the returned value is a time in nanosecond of the `UINT64` type. When the `sync point` feature is enabled, this parameter specifies the interval at which Syncpoint aligns the upstream and downstream snapshots. The default value is `10m` and the minimum value is `30s`. (Optional) |
| `sync_point_retention`    | `STRING` type. Note that the returned value is a time in nanosecond of the `UINT64` type. When the `sync point` feature is enabled, this parameter specifies how long the data is retained by Syncpoint in the downstream table. When this duration is exceeded, the data is cleaned up. The default value is `24h`. (Optional) |

The `consistent` parameters are described as follows:

| Parameter name | Description |
|:-----------------|:---------------------------------------|
| `flush_interval` | `UINT64` type. The interval to flush redo log files. (Optional) |
| `level`          | `STRING` type. The consistency level of the replicated data. (Optional)    |
| `max_log_size`   | `UINT64` type. The maximum value of redo log. (Optional)      |
| `storage`        | `STRING` type. The destination address of the storage. (Optional)            |

The `filter` parameters are described as follows:

| Parameter name | Description |
|:-----------------|:---------------------------------------|
| `do_dbs`              | `STRING ARRAY` type. The databases to be replicated. (Optional)                                       |
| `do_tables`           | The tables to be replicated. (Optional)                                                     |
| `ignore_dbs`          | `STRING ARRAY` type. The databases to be ignored. (Optional)            |
| `ignore_tables`       | The tables to be ignored. (Optional)        |
| `event_filters`       | The configuration to filter events. (Optional)  |
| `ignore_txn_start_ts` | `UINT64 ARRAY` type. Specifying this will ignore transactions that specify `start_ts`, such as `[1, 2]`. (Optional)   |
| `rules`               | `STRING ARRAY` type. The rules for table schema filtering, such as `['foo*.*', 'bar*.*']`. For more information, see [Table Filter](/table-filter.md). (Optional)  |

The `filter.event_filters` parameters are described as follows. For more information, see [Changefeed Log Filters](/ticdc/ticdc-filter.md).

| Parameter name | Description |
|:-----------------|:---------------------------------------|
| `ignore_delete_value_expr`     | `STRING ARRAY` type. For example, `"name = 'john'"` means to filter out DELETE DML statements containing the `name = 'john'` condition. (Optional)            |
| `ignore_event`                 | `STRING ARRAY` type. For example, `["insert"]` indicates that the INSERT events are filtered out. (Optional)     |
| `ignore_insert_value_expr`     | `STRING ARRAY` type. For example, `"id >= 100"` means to filter out INSERT DML statements that match the `id >= 100` condition. (Optional)                |
| `ignore_sql`                   | `STRING ARRAY` type. For example, `["^drop", "add column"]` means to filter out DDL statements that start with `DROP` or contain `ADD COLUMN`. (Optional)  |
| `ignore_update_new_value_expr` | `STRING ARRAY` type. For example, `"gender = 'male'"` means to filter out the UPDATE DML statements with the new value `gender = 'male'`. (Optional)          |
| `ignore_update_old_value_expr` | `STRING ARRAY` type. For example, `"age < 18"` means to filter out the UPDATE DML statements with the old value `age < 18`. (Optional)                  |
| `matcher`                      | `STRING ARRAY` type. It works as an allowlist. For example, `["test.worker"]` means that the filter rule applies only to the `worker` table in the `test` database. (Optional)          |

The `mounter` parameter is described as follows:

| Parameter name | Description |
|:-----------------|:---------------------------------------|
| `worker_num` | `INT` type. The number of Mounter threads. Mounter is used to decode the data output from TiKV. The default value is `16`. (Optional)   |

The `sink` parameters are described as follows:

| Parameter name | Description |
|:-----------------|:---------------------------------------|
| `column_selectors`      | The column selector configuration. (Optional)                                              |
| `csv`                   | The CSV configuration. (Optional)                                         |
| `date_separator`        | `STRING` type. Indicates the date separator type of the file directory. Value options are `none`, `year`, `month`, and `day`. `none` is the default value and means that the date is not separated. (Optional)      |
| `dispatchers`           | An configuration array for event dispatching. (Optional)                                                     |
| `encoder_concurrency`   | `INT` type. The number of encoder threads in the MQ sink. The default value is `16`. (Optional)               |
| `protocol`              | `STRING` type. For MQ sinks, you can specify the protocol format of the message. The following protocols are currently supported: `canal-json`, `open-protocol`, `canal`, `avro`, and `maxwell`. |
| `schema_registry`       | `STRING` type. The schema registry address. (Optional)                                                  |
| `terminator`            | `STRING` type. The terminator is used to separate two data change events. The default value is null, which means `"\r\n"` is used as the terminator. (Optional)                |
| `transaction_atomicity` | `STRING` type. The atomicity level of the transaction. (Optional)  |

`sink.column_selectors` is an array. The parameters are described as follows:

| Parameter name | Description |
|:-----------------|:---------------------------------------|
| `columns` | `STRING ARRAY` type. The column array.                 |
| `matcher` | `STRING ARRAY` type. The matcher configuration. It has the same matching syntax as the filter rule does.  |

The `sink.csv` parameters are described as follows:

| Parameter name | Description |
|:-----------------|:---------------------------------------|
| `delimiter`         | `STRING` type. The character used to separate fields in the CSV file. The value must be an ASCII character and defaults to `,`.     |
| `include_commit_ts` | `BOOLEAN` type. Whether to include commit-ts in CSV rows. The default value is `false`. |
| `null`              | `STRING` type. The character that is displayed when a CSV column is null. The default value is `\N`. |
| `quote`             | `STRING` type. The quotation character used to surround fields in the CSV file. If the value is empty, no quotation is used. The default value is `"`. |

`sink.dispatchers`: for the sink of MQ type, you can use this parameter to configure the event dispatcher. The following dispatchers are supported: `default`, `ts`, `rowid`, and `table`. The dispatcher rules are as follows:

- `default`: dispatches events in the `table` mode.
- `ts`: uses the commitTs of the row change to create the hash value and dispatch events.
- `rowid`: uses the name and value of the selected HandleKey column to create the hash value and dispatch events.
- `table`: uses the schema name of the table and the table name to create the hash value and dispatch events.

`sink.dispatchers` is an array. The parameters are described as follows:

| Parameter name | Description |
|:-----------------|:---------------------------------------|
| `matcher`   | `STRING ARRAY` type. It has the same matching syntax as the filter rule does. |
| `partition` | `STRING` type. The target partition for dispatching events.    |
| `topic`     | `STRING` type. The target topic for dispatching events.        |

### Example

The following request creates a replication task with an ID of `test5` and `sink_uri` of `blackhome://`.

```shell
curl -X POST -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v2/changefeeds -d '{"changefeed_id":"test5","sink_uri":"blackhole://"}'
```

If the request is successful, `200 OK` is returned. If the request fails, an error message and error code are returned.

### Response body format

```json
{
  "admin_job_type": 0,
  "checkpoint_time": "string",
  "checkpoint_ts": 0,
  "config": {
    "bdr_mode": true,
    "case_sensitive": true,
    "check_gc_safe_point": true,
    "consistent": {
      "flush_interval": 0,
      "level": "string",
      "max_log_size": 0,
      "storage": "string"
    },
    "enable_old_value": true,
    "enable_sync_point": true,
    "filter": {
      "do_dbs": [
        "string"
      ],
      "do_tables": [
        {
          "database_name": "string",
          "table_name": "string"
        }
      ],
      "event_filters": [
        {
          "ignore_delete_value_expr": "string",
          "ignore_event": [
            "string"
          ],
          "ignore_insert_value_expr": "string",
          "ignore_sql": [
            "string"
          ],
          "ignore_update_new_value_expr": "string",
          "ignore_update_old_value_expr": "string",
          "matcher": [
            "string"
          ]
        }
      ],
      "ignore_dbs": [
        "string"
      ],
      "ignore_tables": [
        {
          "database_name": "string",
          "table_name": "string"
        }
      ],
      "ignore_txn_start_ts": [
        0
      ],
      "rules": [
        "string"
      ]
    },
    "force_replicate": true,
    "ignore_ineligible_table": true,
    "memory_quota": 0,
    "mounter": {
      "worker_num": 0
    },
    "sink": {
      "column_selectors": [
        {
          "columns": [
            "string"
          ],
          "matcher": [
            "string"
          ]
        }
      ],
      "csv": {
        "delimiter": "string",
        "include_commit_ts": true,
        "null": "string",
        "quote": "string"
      },
      "date_separator": "string",
      "dispatchers": [
        {
          "matcher": [
            "string"
          ],
          "partition": "string",
          "topic": "string"
        }
      ],
      "enable_partition_separator": true,
      "encoder_concurrency": 0,
      "protocol": "string",
      "schema_registry": "string",
      "terminator": "string",
      "transaction_atomicity": "string"
    },
    "sync_point_interval": "string",
    "sync_point_retention": "string"
  },
  "create_time": "string",
  "creator_version": "string",
  "error": {
    "addr": "string",
    "code": "string",
    "message": "string"
  },
  "id": "string",
  "resolved_ts": 0,
  "sink_uri": "string",
  "start_ts": 0,
  "state": "string",
  "target_ts": 0,
  "task_status": [
    {
      "capture_id": "string",
      "table_ids": [
        0
      ]
    }
  ]
}
```

The parameters are described as follows:

| Parameter name | Description |
|:-----------------|:---------------------------------------|
| `admin_job_type`  | `INTEGER` type. The admin job type.                 |
| `checkpoint_time` | `STRING` type. The formatted time of the current checkpoint for the replication task.                  |
| `checkpoint_ts`   | `STRING` type. The TSO of the current checkpoint for the replication task.    |
| `config`          | The replication task configuration. The structure and meaning are the same as that of the `replica_config` configuration in creating the replication task.       |
| `create_time`     | `STRING` type. The time when the replication task is created.                          |
| `creator_version` | `STRING` type. The TiCDC version when the replication task is created.         |
| `error`           | The replication task error.                      |
| `id`              | `STRING` type. The replication task ID.                |
| `resolved_ts`     | `UINT64` type. The replication task resolved ts.    |
| `sink_uri`        | `STRING` type. The replication task sink URI.                                     |
| `start_ts`        | `UINT64` type. The replication task start ts.                                      |
| `state`           | `STRING` type. The replication task status. It can be `normal`, `stopped`, `error`, `failed`, or `finished`. |
| `target_ts`       | `UINT64` type. The replication task target ts.                                    |
| `task_status`     | The detailed status of dispatching the replication task. |

The `task_status` parameters are described as follows:

| Parameter name | Description |
|:-----------------|:---------------------------------------|
| `capture_id` | `STRING` type. The capture ID.                    |
| `table_ids`  | `UINT64 ARRAY` type. The ID of the table being replicated on this capture. |

The `error` parameters are described as follows:

| Parameter name | Description |
|:-----------------|:---------------------------------------|
| `addr` | `STRING` type. The capture address. |
| `code` | `STRING` type. The error code.          |
| `message` | `STRING` type. The details of the error.      |

## Remove a replication task

This API is an idempotent interface (that is, it can be applied multiple times without changing the result beyond the initial application) for removing a replication task. If the request is successful, `200 OK` is returned. The returned result only means that the server agrees to run the command but does not guarantee that the command will be run successfully.

### Request URI

`DELETE /api/v2/changefeeds/{changefeed_id}`

### Parameter descriptions

#### Path parameters

| Parameter name | Description |
| :-------------- | :----------------------------------- |
| `changefeed_id` | The ID of the replication task (changefeed) to be removed. |

### Example

The following request removes the replication task with the ID `test1`.

```shell
curl -X DELETE http://127.0.0.1:8300/api/v2/changefeeds/test1
```

If the request is successful, `200 OK` is returned. If the request fails, an error message and error code are returned.

## Update the replication configuration

This API is used for updating a replication task. If the request is successful, `200 OK` is returned. The returned result only means that the server agrees to run the command but does not guarantee that the command will be run successfully.

To modify the changefeed configuration, follow the steps of `pause the replication task -> modify the configuration -> resume the replication task`.

### Request URI

`PUT /api/v2/changefeeds/{changefeed_id}`

### Parameter descriptions

#### Path parameters

| Parameter name | Description |
| :-------------- | :----------------------------------- |
| `changefeed_id` | The ID of the replication task (changefeed) to be updated. |

#### Parameters for the request body

```json
{
  "replica_config": {
    "bdr_mode": true,
    "case_sensitive": true,
    "check_gc_safe_point": true,
    "consistent": {
      "flush_interval": 0,
      "level": "string",
      "max_log_size": 0,
      "storage": "string"
    },
    "enable_old_value": true,
    "enable_sync_point": true,
    "filter": {
      "do_dbs": [
        "string"
      ],
      "do_tables": [
        {
          "database_name": "string",
          "table_name": "string"
        }
      ],
      "event_filters": [
        {
          "ignore_delete_value_expr": "string",
          "ignore_event": [
            "string"
          ],
          "ignore_insert_value_expr": "string",
          "ignore_sql": [
            "string"
          ],
          "ignore_update_new_value_expr": "string",
          "ignore_update_old_value_expr": "string",
          "matcher": [
            "string"
          ]
        }
      ],
      "ignore_dbs": [
        "string"
      ],
      "ignore_tables": [
        {
          "database_name": "string",
          "table_name": "string"
        }
      ],
      "ignore_txn_start_ts": [
        0
      ],
      "rules": [
        "string"
      ]
    },
    "force_replicate": true,
    "ignore_ineligible_table": true,
    "memory_quota": 0,
    "mounter": {
      "worker_num": 0
    },
    "sink": {
      "column_selectors": [
        {
          "columns": [
            "string"
          ],
          "matcher": [
            "string"
          ]
        }
      ],
      "csv": {
        "delimiter": "string",
        "include_commit_ts": true,
        "null": "string",
        "quote": "string"
      },
      "date_separator": "string",
      "dispatchers": [
        {
          "matcher": [
            "string"
          ],
          "partition": "string",
          "topic": "string"
        }
      ],
      "enable_partition_separator": true,
      "encoder_concurrency": 0,
      "protocol": "string",
      "schema_registry": "string",
      "terminator": "string",
      "transaction_atomicity": "string"
    },
    "sync_point_interval": "string",
    "sync_point_retention": "string"
  },
  "sink_uri": "string",
  "target_ts": 0
}
```

Currently, only the following configurations can be modified via the API.

| Parameter name | Description |
| :-------------------- | :----------------------------------------------------- |
| `target_ts` | `UINT64` type. Specifies the target TSO of the changefeed. (Optional) |
| `sink_uri` | `STRING` type. The downstream address of the replication task. (Optional) |
| `replica_config` | The configuration parameters of sink. It must be complete. (Optional) |

The meanings of the above parameters are the same as those in the [Create a replication task](#create-a-replication-task) section. See that section for details.

### Example

The following request updates the `target_ts` of the replication task with the ID `test1` to `32`.

```shell
 curl -X PUT -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v2/changefeeds/test1 -d '{"target_ts":32}'
```

If the request is successful, `200 OK` is returned. If the request fails, an error message and error code are returned. The meanings of the JSON response body are the same as those in the [Create a replication task](#create-a-replication-task) section. See that section for details.

## Query the replication task list

This API is a synchronous interface. If the request is successful, the basic information of all replication tasks (changefeed) in the TiCDC cluster is returned.

### Request URI

`GET /api/v2/changefeeds`

### Parameter descriptions

#### Query parameter

| Parameter name | Description |
| :------ | :--------------------------------------------- |
| `state` | When this parameter is specified, the information of replication tasks in this specified state is returned. (Optional) |

The value options for `state` are `all`, `normal`, `stopped`, `error`, `failed`, and `finished`.

If this parameter is not specified, the basic information of replication tasks in the `normal`, `stopped`, or `failed` state is returned by default.

### Example

The following request queries the basic information of all replication tasks in the `normal` state.

```shell
curl -X GET http://127.0.0.1:8300/api/v2/changefeeds?state=normal
```

```json
{
  "total": 2,
  "items": [
    {
      "id": "test",
      "state": "normal",
      "checkpoint_tso": 439749918821711874,
      "checkpoint_time": "2023-02-27 23:46:52.888",
      "error": null
    },
    {
      "id": "test2",
      "state": "normal",
      "checkpoint_tso": 439749918821711874,
      "checkpoint_time": "2023-02-27 23:46:52.888",
      "error": null
    }
  ]
}
```

The parameters in the returned result above are described as follows:

- `id`: the ID of the replication task.
- `state`: the current [state](/ticdc/ticdc-changefeed-overview.md#changefeed-state-transfer) of the replication task.
- `checkpoint_tso`: the TSO of the current checkpoint of the replication task.
- `checkpoint_time`: the formatted time of the current checkpoint of the replication task.
- `error`: the error information of the replication task.

## Query a specific replication task

This API is a synchronous interface. If the request is successful, the detailed information of the specified replication task (changefeed) is returned.

### Request URI

`GET /api/v2/changefeeds/{changefeed_id}`

### Parameter description

#### Path parameter

| Parameter name | Description |
| :-------------- | :----------------------------------- |
| `changefeed_id` | The ID of the replication task (changefeed) to be queried. |

### Example

The following request queries the detailed information of the replication task with the ID `test1`.

```shell
curl -X GET http://127.0.0.1:8300/api/v2/changefeeds/test1
```

The meanings of the JSON response body are the same as those in the [Create a replication task](#create-a-replication-task) section. See that section for details.

## Pause a replication task

This API pauses a replication task. If the request is successful, `200 OK` is returned. The returned result only means that the server agrees to run the command but does not guarantee that the command will be run successfully.

### Request URI

`POST /api/v2/changefeeds/{changefeed_id}/pause`

### Parameter description

#### Path parameter

| Parameter name | Description |
| :-------------- | :----------------------------------- |
| `changefeed_id` | The ID of the replication task (changefeed) to be paused. |

### Example

The following request pauses the replication task with the ID `test1`.

```shell
curl -X POST http://127.0.0.1:8300/api/v2/changefeeds/test1/pause
```

If the request is successful, `200 OK` is returned. If the request fails, an error message and error code are returned.

## Resume a replication task

This API resumes a replication task. If the request is successful, `200 OK` is returned. The returned result only means that the server agrees to run the command but does not guarantee that the command will be run successfully.

### Request URI

`POST /api/v2/changefeeds/{changefeed_id}/resume`

### Parameter description

#### Path parameter

| Parameter name | Description |
| :-------------- | :----------------------------------- |
| `changefeed_id` | The ID of the replication task (changefeed) to be resumed. |

#### Parameters for the request body

```json
{
  "overwrite_checkpoint_ts": 0
}
```

| Parameter name | Description |
| :-------------- | :----------------------------------- |
| `overwrite_checkpoint_ts` | `UINT64` type. Reassign a checkpoint TSO when resuming a replication task (changefeed). |

### Example

The following request resumes the replication task with the ID `test1`.

```shell
curl -X POST http://127.0.0.1:8300/api/v2/changefeeds/test1/resume -d '{}'
```

If the request is successful, `200 OK` is returned. If the request fails, an error message and error code are returned.

## Query the replication subtask list

This API is a synchronous interface. If the request is successful, the basic information of all replication subtasks (`processor`) is returned.

### Request URI

`GET /api/v2/processors`

### Example

```shell
curl -X GET http://127.0.0.1:8300/api/v2/processors
```

```json
{
  "total": 3,
  "items": [
    {
      "changefeed_id": "test2",
      "capture_id": "d2912e63-3349-447c-90ba-72a4e04b5e9e"
    },
    {
      "changefeed_id": "test1",
      "capture_id": "d2912e63-3349-447c-90ba-72a4e04b5e9e"
    },
    {
      "changefeed_id": "test",
      "capture_id": "d2912e63-3349-447c-90ba-72a4e04b5e9e"
    }
  ]
}
```

The parameters are described as follows:

- `changefeed_id`: the changefeed ID.
- `capture_id`: the capture ID.

## Query a specific replication subtask

This API is a synchronous interface. If the request is successful, the detailed information of the specified replication subtask (`processor`) is returned.

### Request URI

`GET /api/v2/processors/{changefeed_id}/{capture_id}`

### Parameter descriptions

#### Path parameters

| Parameter name | Description |
| :-------------- | :----------------------------------- |
| `changefeed_id` | The changefeed ID of the replication subtask to be queried. |
| `capture_id` | The capture ID of the replication subtask to be queried. |

### Example

The following request queries the detailed information of a subtask whose `changefeed_id` is `test` and `capture_id` is `561c3784-77f0-4863-ad52-65a3436db6af`. A subtask can be identified by `changefeed_id` and `capture_id`.

```shell
curl -X GET http://127.0.0.1:8300/api/v2/processors/test/561c3784-77f0-4863-ad52-65a3436db6af
```

```json
{
  "table_ids": [
    80
  ]
}
```

The parameter is described as follows:

- `table_ids`: The table ID to be replicated on this capture.

## Query the TiCDC service process list

This API is a synchronous interface. If the request is successful, the basic information of all replication processes (`capture`) is returned.

### Request URI

`GET /api/v2/captures`

### Example

```shell
curl -X GET http://127.0.0.1:8300/api/v2/captures
```

```json
{
  "total": 1,
  "items": [
    {
      "id": "d2912e63-3349-447c-90ba-72a4e04b5e9e",
      "is_owner": true,
      "address": "127.0.0.1:8300"
    }
  ]
}
```

The parameters are described as follows:

- `id`: the capture ID.
- `is_owner`: whether the capture is the owner.
- `address`: the address of the capture.

## Evict an owner node

This API is an asynchronous interface. If the request is successful, `200 OK` is returned. The returned result only means that the server agrees to run the command but does not guarantee that the command will be run successfully.

### Request URI

`POST /api/v2/owner/resign`

### Example

The following request evicts the current owner node of TiCDC and triggers a new round of elections to generate a new owner node.

```shell
curl -X POST http://127.0.0.1:8300/api/v2/owner/resign
```

If the request is successful, `200 OK` is returned. If the request fails, an error message and error code are returned.

## Dynamically adjust the log level of the TiCDC server

This API is a synchronous interface. If the request is successful, `200 OK` is returned.

### Request URI

`POST /api/v2/log`

### Request parameter

#### Parameter for the request body

| Parameter name | Description |
| :---------- | :----------------- |
| `log_level` | The log level you want to set. |

`log_level` supports the [log levels provided by zap](https://godoc.org/go.uber.org/zap#UnmarshalText): "debug", "info", "warn", "error", "dpanic" , "panic", and "fatal".

### Example

```shell
curl -X POST -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v2/log -d '{"log_level":"debug"}'
```

If the request is successful, `200 OK` is returned. If the request fails, an error message and error code are returned.
