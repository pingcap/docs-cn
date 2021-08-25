---
title: TiCDC OpenAPI
summary: Learn how to use the OpenAPI interface to manage the cluster status and data replication.
---

# TiCDC OpenAPI

<!-- markdownlint-disable MD024 -->

> **Warning:**
>
> TiCDC OpenAPI is still an experimental feature. It is not recommended to use it in a production environment.

TiCDC provides the OpenAPI feature for querying and operating the TiCDC cluster, which is similar to the feature of [`cdc cli` tool](/ticdc/manage-ticdc.md#use-cdc-cli-to-manage-cluster-status-and-data-replication-task).

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
- [Manually trigger the load balancing of all tables in a replication task](#manually-trigger-the-load-balancing-of-all-tables-in-a-replication-task)
- [Manually schedule a table to another node](#manually-schedule-a-table-to-another-node)
- [Dynamically adjust the log level of the TiCDC server](#dynamically-adjust-the-log-level-of-the-ticdc-server)

The request body and returned value of all APIs are in JSON format. The following sections describe the specific usage of the APIs.

In the following examples, the listening IP address of the TiCDC server is `127.0.0.1` and the port is `8300`. You can bind a specified IP and port via `--addr=ip:port` when starting the TiCDC server.

## API error message template

After sending an API request, if an error occurs, the returned error message is in the following format:

```json
{
    "error_msg": "",
    "error_code": ""
}
```

From the above JSON output, `error_msg` describes the error message and `error_code` is the corresponding error code.

## Get the status information of a TiCDC node

This API is a synchronous interface. If the request is successful, the status information of the corresponding node is returned.

### Request URI

`GET /api/v1/status`

### Example

The following request gets the status information of the TiCDC node whose IP address is `127.0.0.1` and port number is `8300`.

{{< copyable "shell-regular" >}}

```shell
curl -X GET http://127.0.0.1:8300/api/v1/status
```

```json
{
    "version": "v5.2.0-master-dirty",
    "git_hash": "f191cd00c53fdf7a2b1c9308a355092f9bf8824e",
    "id": "c6a43c16-0717-45af-afd6-8b3e01e44f5d",
    "pid": 25432,
    "is_owner": true
}
```

The fields of the above output are described as follows:

- version: The current TiCDC version number.
- git_hash: The Git hash value.
- id: The capture ID of the node.
- pid: The capture process PID of the node.
- is_owner: Indicates whether the node is an owner.

## Check the health status of a TiCDC cluster

This API is a synchronous interface. If the cluster is healthy, `200 OK` is returned.

### Request URI

`GET /api/v1/health`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X GET http://127.0.0.1:8300/api/v1/health
```

## Create a replication task

This API is an asynchronous interface. If the request is successful, `202 Accepted` is returned. The returned result only means that the server agrees to run the command but does not guarantee that the command will be run successfully.

### Request URI

`POST /api/v1/changefeeds`

### Parameter description

Compared to the optional parameters for creating a replication task using the `cli` command, the optional parameters for creating such task using the API are not as complete. This API supports the following parameters.

#### Parameters for the request body

| Parameter name | Description |
| :------------------------ | :---------------------- ------------------------------- |
| `changefeed_id` | `STRING` type. The ID of the replication task. (Optional) |
| `start_ts` | `UINT64` type. Specifies the start TSO of the changefeed. (Optional) |
| `target_ts` | `UINT64` type. Specifies the target TSO of the changefeed. (Optional) |
| **`sink_uri`** | `STRING` type. The downstream address of the replication task. (**Required**) |
| `force_replicate` | `BOOLEAN` type. Determines whether to forcibly replicate the tables without unique indexes. (Optional) |
| `ignore_ineligible_table` | `BOOLEAN` type. Determines whether to ignore the tables that cannot be replicated. (Optional) |
| `filter_rules` | `STRING` type array. The rules for table schema filtering. (Optional) |
| `ignore_txn_start_ts` | `UINT64` type array. Ignores the transaction of a specified start_ts. (Optional) |
| `mounter_worker_num` | `INT` type. The mounter thread number. (Optional) |
| `sink_config` | The configuration parameters of sink. (Optional) |

The meaning and format of `changefeed_id`, `start_ts`, `target_ts`, and `sink_uri` are the same as those described in the [Use `cdc cli` to create a replication task](/ticdc/manage-ticdc.md#create-a-replication-task) document. For the detailed description of these parameters, see this document. Note that when you specify the certificate path in `sink_uri`, make sure you have uploaded the corresponding certificate to the corresponding TiCDC server.

Some other parameters in the above table are described further as follows.

`force_replicate`: This parameter defaults to `false`. When it is specified as `true`, TiCDC tries to forcibly replicate tables that do not have a unique index.

`ignore_ineligible_table`: This parameter defaults to `false`. When it is specified as `true`, TiCDC ignores tables that cannot be replicated.

`filter_rules`: The rules for table schema filtering, such as `filter_rules = ['foo*.*','bar*.*']`. For details, see the [Table Filter](/table-filter.md) document.

`ignore_txn_start_ts`: When this parameter is specified, the specified start_ts is ignored. For example, `ignore-txn-start-ts = [1, 2]`.

`mounter_worker_num`: The thread number of mounter. Mounter is used to decode the data output from TiKV. The default value is `16`.

The configuration parameters of sink are as follows:

```json
{
  "dispatchers":[
    {"matcher":["test1.*", "test2.*"], "dispatcher":"ts"},
    {"matcher":["test3.*", "test4.*"], "dispatcher":"rowid"},
  ],
  "protocal":"default",
}
```

`dispatchers`: For the sink of MQ type, you can use dispatchers to configure the event dispatcher. Four dispatchers are supported: `default`, `ts`, `rowid`, and `table`. The dispatcher rules are as follows:

- `default`: When multiple unique indexes (including the primary key) exist or the Old Value feature is enabled, events are dispatched in the `table` mode. When only one unique index (or the primary key) exists, events are dispatched in the `rowid` mode.
- `ts`: Uses the commitTs of the row change to create the hash value and dispatch events.
- `rowid`: Uses the name and value of the selected HandleKey column to create the hash value and dispatch events.
- `table`: Uses the schema name of the table and the table name to create the hash value and dispatch events.

`matcher`: The matching syntax of matcher is the same as the filter rule syntax.

`protocal`: For the sink of MQ type, you can specify the protocol format of the message. Currently four protocols are supported: `default`, `canal`, `avro`, and `maxwell`. The default protocol is the TiCDC Open Protocol.

### Example

The following request creates a replication task with an ID of `test5` and a `sink_uri` of `blackhome://`.

{{< copyable "shell-regular" >}}

```shell
curl -X POST -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v1/changefeeds -d '{"changefeed_id":"test5","sink_uri":"blackhole://"}'
```

If the request is successful, `202 Accepted` is returned. If the request fails, an error message and error code are returned.

## Remove a replication task

This API is an asynchronous interface. If the request is successful, `202 Accepted` is returned. The returned result only means that the server agrees to run the command but does not guarantee that the command will be run successfully.

### Request URI

`DELETE /api/v1/changefeeds/{changefeed_id}`

### Parameter description

#### Path parameters

| Parameter name | Description |
| :-------------- | :----------------------------------- |
| `changefeed_id` | The ID of the replication task (changefeed) to be removed. |

### Example

The following request removes the replication task with the ID `test1`.

{{< copyable "shell-regular" >}}

```shell
curl -X DELETE http://127.0.0.1:8300/api/v1/changefeeds/test1
```

If the request is successful, `202 Accepted` is returned. If the request fails, an error message and error code are returned.

## Update the replication configuration

This API is an asynchronous interface. If the request is successful, `202 Accepted` is returned. The returned result only means that the server agrees to run the command but does not guarantee that the command will be run successfully.

To modify the changefeed configuration, follow the steps of `pause the replication task -> modify the configuration -> resume the replication task`.

### Request URI

`PUT /api/v1/changefeeds/{changefeed_id}`

### Parameter description

#### Path parameters

| Parameter name | Description |
| :-------------- | :----------------------------------- |
| `changefeed_id` | The ID of the replication task (changefeed) to be updated. |

#### Parameters for the request body

Currently, only the following configuration can be modified via the API.

| Parameter name | Description |
| :-------------------- | :-------------------------- --------------------------- |
| `target_ts` | `UINT64` type. Specifies the target TSO of the changefeed. (Optional) |
| `sink_uri` | `STRING` type. The downstream address of the replication task. (Optional) |
| `filter_rules` | `STRING` type array. The rules for table schema filtering. (Optional) |
| `ignore_txn_start_ts` | `UINT64` type array. Ignores the transaction of a specified start_ts. (Optional) |
| `mounter_worker_num` | `INT` type. The mounter thread number. (Optional) |
| `sink_config` | The configuration parameters of sink. (Optional) |

The meanings of the above parameters are the same as those in the [Create a replication task](#create-a-replication-task) section. See that section for details.

### Example

The following request updates the `mounter_worker_num` of the replication task with the ID `test1` to `32`.

{{< copyable "shell-regular" >}}

```shell
 curl -X PUT -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v1/changefeeds/test1 -d '{"mounter_worker_num":32}'
```

If the request is successful, `202 Accepted` is returned. If the request fails, an error message and error code are returned.

## Query the replication task list

This API is a synchronous interface. If the request is successful, the basic information of all nodes in the TiCDC cluster is returned.

### Request URI

`GET /api/v1/changefeeds`

### Parameter description

#### Query parameters

| Parameter name | Description |
| :------ | :---------------------------------------- ----- |
| `state` | When this parameter is specified, the replication status information only of this state is returned.(Optional) |

The value options for `state` are `all`, `normal`, `stopped`, `error`, `failed`, and `finished`.

If this parameter is not specified, the basic information of replication tasks whose state is normal, stopped, or failed is returned by default.

### Example

The following request queries the basic information of all replication tasks whose state is `normal`.

{{< copyable "shell-regular" >}}

```shell
curl -X GET http://127.0.0.1:8300/api/v1/changefeeds?state=normal
```

```json
[
    {
        "id": "test1",
        "state": "normal",
        "checkpoint_tso": 426921294362574849,
        "checkpoint_time": "2021-08-10 14:04:54.242",
        "error": null
    },
    {
        "id": "test2",
        "state": "normal",
        "checkpoint_tso": 426921294362574849,
        "checkpoint_time": "2021-08-10 14:04:54.242",
        "error": null
    }
]
```

The fields in the returned result above are described as follows:

- id: The ID of the replication task.
- state: The current [state](/ticdc/manage-ticdc.md#state-transfer-of-replication-tasks) of the replication task.
- checkpoint_tso: The TSO representation of the current checkpoint of the replication task.
- checkpoint_tso: The formatted time representation of the current checkpoint of the replication task.
- error: The error information of the replication task.

## Query a specific replication task

This API is a synchronous interface. If the request is successful, the detailed information of the specified replication task is returned.

### Request URI

`GET /api/v1/changefeeds/{changefeed_id}`

### Parameter description

#### Path parameters

| Parameter name | Description |
| :-------------- | :----------------------------------- |
| `changefeed_id` | The ID of the replication task (changefeed) to be queried. |

### Example

The following request queries the detailed information of the replication task with the ID `test1`.

{{< copyable "shell-regular" >}}

```shell
curl -X GET http://127.0.0.1:8300/api/v1/changefeeds/test1
```

```json
{
    "id": "test1",
    "sink_uri": "blackhole://",
    "create_time": "2021-08-10 11:41:30.642",
    "start_ts": 426919038970232833,
    "target_ts": 0,
    "checkpoint_tso": 426921014615867393,
    "checkpoint_time": "2021-08-10 13:47:07.093",
    "sort_engine": "unified",
    "state": "normal",
    "error": null,
    "error_history": null,
    "creator_version": "",
    "task_status": [
        {
            "capture_id": "d8924259-f52f-4dfb-97a9-c48d26395945",
            "table_ids": [
                63,
                65,
            ],
            "table_operations": {}
        }
    ]
}
```

## Pause a replication task

This API is an asynchronous interface. If the request is successful, `202 Accepted` is returned. The returned result only means that the server agrees to run the command but does not guarantee that the command will be run successfully.

### Request URI

`POST /api/v1/changefeeds/{changefeed_id}/pause`

### Parameter description

#### Path parameters

| Parameter name | Description |
| :-------------- | :----------------------------------- |
| `changefeed_id` | The ID of the replication task (changefeed) to be paused. |

### Example

The following request pauses the replication task with the ID `test1`.

{{< copyable "shell-regular" >}}

```shell
curl -X POST http://127.0.0.1:8300/api/v1/changefeeds/test1/pause
```

If the request is successful, `202 Accepted` is returned. If the request fails, an error message and error code are returned.

## Resume a replication task

This API is an asynchronous interface. If the request is successful, `202 Accepted` is returned. The returned result only means that the server agrees to run the command but does not guarantee that the command will be run successfully.

### Request URI

`POST /api/v1/changefeeds/{changefeed_id}/resume`

### Parameter description

#### Path parameters

| Parameter name | Description |
| :-------------- | :----------------------------------- |
| `changefeed_id` | The ID of the replication task (changefeed) to be resumed. |

### Example

The following request resumes the replication task with the ID `test1`.

{{< copyable "shell-regular" >}}

```shell
curl -X POST http://127.0.0.1:8300/api/v1/changefeeds/test1/resume
```

If the request is successful, `202 Accepted` is returned. If the request fails, an error message and error code are returned.

## Query the replication subtask list

This API is a synchronous interface. If the request is successful, the basic information of all replication subtasks (`processor`) is returned.

### Request URI

`GET /api/v1/processors`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X GET http://127.0.0.1:8300/api/v1/processors
```

```json
[
    {
        "changefeed_id": "test1",
        "capture_id": "561c3784-77f0-4863-ad52-65a3436db6af"
    }
]
```

## Query a specific replication subtask

This API is a synchronous interface. If the request is successful, the detailed information of the specified replication subtask (`processor`) is returned.

### Request URI

`GET /api/v1/processors/{changefeed_id}/{capture_id}`

### Parameter description

#### Path parameters

| Parameter name | Description |
| :-------------- | :----------------------------------- |
| `changefeed_id` | The changefeed ID of the replication subtask to be queried. |
| `capture_id` | The capture ID of the replication subtask to be queried. |

### Example

The following request queries the detailed information of a subtask whose `changefeed_id` is `test` and `capture_id` is `561c3784-77f0-4863-ad52-65a3436db6af`. A subtask can be indentifed by `changefeed_id` and `capture_id`.

{{< copyable "shell-regular" >}}

```shell
curl -X GET http://127.0.0.1:8300/api/v1/processors/test1/561c3784-77f0-4863-ad52-65a3436db6af
```

```json
{
    "checkpoint_ts": 426919123303006208,
    "resolved_ts": 426919123369066496,
    "table_ids": [
        63,
        65,
    ],
    "error": null
}
```

## Query the TiCDC service process list

This API is a synchronous interface. If the request is successful, the basic information of all replication processes (`capture`) is returned.

### Request URI

`GET /api/v1/captures`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X GET http://127.0.0.1:8300/api/v1/captures
```

```json
[
    {
        "id": "561c3784-77f0-4863-ad52-65a3436db6af",
        "is_owner": true,
        "address": "127.0.0.1:8300"
    }
]
```

## Evict an owner node

This API is an asynchronous interface. If the request is successful, `202 Accepted` is returned. The returned result only means that the server agrees to run the command but does not guarantee that the command will be run successfully.

### Request URI

`POST /api/v1/owner/resign`

### Example

The following request evicts the current owner node of TiCDC and triggers a new round of elections to generate a new owner node.

{{< copyable "shell-regular" >}}

```shell
curl -X POST http://127.0.0.1:8300/api/v1/owner/resign
```

If the request is successful, `202 Accepted` is returned. If the request fails, an error message and error code are returned.

## Manually trigger the load balancing of all tables in a replication task

This API is an asynchronous interface. If the request is successful, `202 Accepted` is returned. The returned result only means that the server agrees to run the command but does not guarantee that the command will be run successfully.

### Request URI

`POST /api/v1/changefeeds/{changefeed_id}/tables/rebalance_table`

### Parameter description

#### Path parameters

| Parameter name | Description |
| :-------------- | :----------------------------------- |
| `changefeed_id` | The ID of the replication task (changefeed) to be scheduled. |

### Example

The following request triggers the load balancing of all tables in the changefeed with the ID `test1`.

{{< copyable "shell-regular" >}}

```shell
 curl -X POST http://127.0.0.1:8300/api/v1/changefeeds/test1/tables/rebalance_table
```

If the request is successful, `202 Accepted` is returned. If the request fails, an error message and error code are returned.

## Manually schedule a table to another node

This API is an asynchronous interface. If the request is successful, `202 Accepted` is returned. The returned result only means that the server agrees to run the command but does not guarantee that the command will be run successfully.

### Request URI

`POST /api/v1/changefeeds/{changefeed_id}/tables/move_table`

### Parameter description

#### Path parameters

| Parameter name | Description |
| :-------------- | :----------------------------------- |
| `changefeed_id` | The ID of the replication task (changefeed) to be scheduled. |

#### Parameters for the request body

| Parameter name | Description |
| :------------------ | :------------------ |
| `target_capture_id` | The ID of the target capture. |
| `table_id` | The ID of the table to be scheduled. |

### Example

The following request schedules the table with the ID `49` in the changefeed with the ID `test1` to the capture with the ID `6f19a6d9-0f8c-4dc9-b299-3ba7c0f216f5`.

{{< copyable "shell-regular" >}}

```shell
curl -X POST -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v1/changefeeds/changefeed-test1/tables/move_table -d '{"capture_id":"6f19a6d9-0f8c-4dc9-b299-3ba7c0f216f5","table_id":49}'

```

If the request is successful, `202 Accepted` is returned. If the request fails, an error message and error code are returned.

## Dynamically adjust the log level of the TiCDC server

This API is a synchronous interface. If the request is successful, `202 OK` is returned.

### Request URI

`POST /api/v1/log`

### Request parameters

#### Parameters for the request body

| Parameter name | Description |
| :---------- | :----------------- |
| `log_level` | The log level you want to set. |

`log_level` supports the [log levels provided by zap](https://godoc.org/go.uber.org/zap#UnmarshalText): "debug", "info", "warn", "error", "dpanic" , "panic", and "fatal".

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X POST -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v1/log -d '{"log_level":"debug"}'

```

If the request is successful, `202 OK` is returned. If the request fails, an error message and error code are returned.
