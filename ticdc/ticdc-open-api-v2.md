---
title: TiCDC OpenAPI v2
summary: 了解如何使用 OpenAPI v2 接口来管理集群状态和数据同步。
---

# TiCDC OpenAPI v2

TiCDC 提供 OpenAPI 功能，你可以通过 OpenAPI v2 对 TiCDC 集群进行查询和运维操作。OpenAPI 的功能是 [`cdc cli` 工具](/ticdc/ticdc-manage-changefeed.md)的一个子集。

> **注意：**
>
> TiCDC OpenAPI v1 将在未来版本中被删除。推荐使用 TiCDC OpenAPI v2。

你可以通过 OpenAPI 完成 TiCDC 集群的如下运维操作：

- [获取 TiCDC 节点状态信息](#获取-ticdc-节点状态信息)
- [检查 TiCDC 集群的健康状态](#检查-ticdc-集群的健康状态)
- [创建同步任务](#创建同步任务)
- [删除同步任务](#删除同步任务)
- [更新同步任务配置](#更新同步任务配置)
- [查询同步任务列表](#查询同步任务列表)
- [查询特定同步任务](#查询特定同步任务)
- [暂停同步任务](#暂停同步任务)
- [恢复同步任务](#恢复同步任务)
- [查询同步子任务列表](#查询同步子任务列表)
- [查询特定同步子任务](#查询特定同步子任务)
- [查询 TiCDC 服务进程列表](#查询-ticdc-服务进程列表)
- [驱逐 owner 节点](#驱逐-owner-节点)
- [动态调整 TiCDC Server 日志级别](#动态调整-ticdc-server-日志级别)

所有 API 的请求体与返回值统一使用 JSON 格式数据。请求如果成功，则统一返回 `200 OK`。本文档以下部分描述当前提供的 API 的具体使用方法。

在下文的示例描述中，假设 TiCDC server 的监听 IP 地址为 `127.0.0.1`，端口为 `8300`。在启动 TiCDC server 时，可以通过 `--addr=ip:port` 指定 TiCDC 绑定的 IP 地址和端口。

## API 统一错误格式

对 API 发起请求后，如发生错误，返回错误信息的格式如下所示：

```json
{
  "error_msg": "",
  "error_code": ""
}
```

如上所示，`error_msg` 描述错误信息，`error_code` 则是对应的错误码。

## API List 接口统一返回格式

一个 API 请求如果返回是一个资源列表（例如，返回所有的服务进程 `Captures`），TiCDC 统一的返回格式如下：

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

如上所示:

- `total`: 表示有一共有多少个资源。
- `items`: 当次请求返回的资源在这个数组里，数组所有的元素都是同种资源。

## 获取 TiCDC 节点状态信息

该接口是一个同步接口，请求成功会返回对应节点的状态信息。

### 请求 URI

`GET /api/v2/status`

### 使用样例

以下请求会获取 IP 地址为 `127.0.0.1`，端口号为 `8300` 的 TiCDC 节点的状态信息。

```shell
curl -X GET http://127.0.0.1:8300/api/v2/status
```

```json
{
  "version": "v8.5.1",
  "git_hash": "10413bded1bdb2850aa6d7b94eb375102e9c44dc",
  "id": "d2912e63-3349-447c-90ba-72a4e04b5e9e",
  "pid": 1447,
  "is_owner": true,
  "liveness": 0
}
```

以上返回信息的字段解释如下：

- `version`：当前 TiCDC 版本号。
- `git_hash`：Git 哈希值。
- `id`：该节点的 capture ID。
- `pid`：该节点 capture 进程的 PID。
- `is_owner`：表示该节点是否是 owner。
- `liveness`: 该节点是否在线。`0` 表示正常，`1` 表示处于 `graceful shutdown` 状态。

## 检查 TiCDC 集群的健康状态

该接口是一个同步接口，在集群健康的时候会返回 `200 OK`。

### 请求 URI

`GET /api/v2/health`

### 使用样例

```shell
curl -X GET http://127.0.0.1:8300/api/v2/health
```

如果集群健康，则返回 `200 OK` 和一个空的 json {}：

```json
{}
```

如果集群不健康，则返回错误信息。

## 创建同步任务

该接口用于向 TiCDC 提交一个同步任务，请求成功会返回 `200 OK`。该返回结果表示服务器收到了执行命令指示，并不代表命令被成功执行。

### 请求 URI

`POST /api/v2/changefeeds`

### 参数说明

```json
{
  "changefeed_id": "string",
  "replica_config": {
    "bdr_mode": true,
    "case_sensitive": false,
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

参数说明如下：

| 参数名              | 说明                                                                                  |
|:-----------------|:------------------------------------------------------------------------------------|
| `changefeed_id`  | `STRING` 类型，同步任务的 ID。（非必选）                                                          |
| `replica_config` | 同步任务的配置参数。（非必选）                                                                     |
| **`sink_uri`**   | `STRING` 类型，同步任务下游的地址。（**必选**）                                                      |
| `start_ts`       | `UINT64` 类型，指定 changefeed 的开始 TSO。TiCDC 集群将从这个 TSO 开始拉取数据。默认为当前时间。（非必选）             |
| `target_ts`      | `UINT64` 类型，指定 changefeed 的目标 TSO。达到这个 TSO 后，TiCDC 集群将停止拉取数据。默认为空，即 TiCDC 不会自动停止。（非必选） |

`changefeed_id`、`start_ts`、`target_ts`、`sink_uri` 的含义和格式与[使用 cli 创建同步任务](/ticdc/ticdc-manage-changefeed.md#创建同步任务)中所作的解释相同，具体解释请参见该文档。需要注意，当在 `sink_uri` 中指定证书的路径时，须确保已将对应证书上传到对应的 TiCDC server 上。

`replica_config` 参数说明如下：

| 参数名                       | 说明                                                                                                       |
|:--------------------------|:---------------------------------------------------------------------------------------------------------|
| `bdr_mode`                | `BOOLEAN` 类型，是否开启[双向同步复制](/ticdc/ticdc-bidirectional-replication.md)。默认值为 `false`。（非必选）                  |
| `case_sensitive`          | `BOOLEAN` 类型，过滤表名时大小写是否敏感。自 v6.5.6、v7.1.3 和 v7.5.0 起，默认值由 `true` 改为 `false`。（非必选）                        |
| `check_gc_safe_point`     | `BOOLEAN` 类型，是否检查同步任务的开始时间早于 GC 时间，默认值为 `true`。（非必选）                                                     |
| `consistent`              | Redo log 配置。（非必选）                                                                                        |
| `enable_sync_point`       | `BOOLEAN` 类型，是否开启 `sync point` 功能。（非必选）                                                                  |
| `filter`                  | filter 配置。（非必选）                                                                                          |
| `force_replicate`         | `BOOLEAN` 类型，该值默认为 `false`，当指定为 `true` 时，同步任务会尝试强制同步没有唯一索引的表。（非必选）                                       |
| `ignore_ineligible_table` | `BOOLEAN` 类型，该值默认为 `false`，当指定为 `true` 时，同步任务会忽略无法进行同步的表。（非必选）                                           |
| `memory_quota`            | `UINT64` 类型，同步任务的内存 quota。（非必选）                                                                          |
| `mounter`                 | 同步任务 `mounter` 配置。（非必选）                                                                                  |
| `sink`                    | 同步任务的`sink`配置。（非必选）                                                                                      |
| `sync_point_interval`     | `STRING` 类型，注意返回值为 `UINT64` 类型的纳秒级时间，`sync point` 功能开启时，对齐上下游 snapshot 的时间间隔。默认值为 `10m`，最小值为 `30s`。（非必选） |
| `sync_point_retention`    | `STRING` 类型，注意返回值为 `UINT64` 类型的纳秒级时间，`sync point` 功能开启时，在下游表中保存的数据的时长，超过这个时间的数据会被清理。默认值为 `24h`。（非必选）     |

`consistent` 参数说明如下：

| 参数名              | 说明                                     |
|:-----------------|:---------------------------------------|
| `flush_interval` | `UINT64` 类型，redo log 文件 flush 间隔。（非必选） |
| `level`          | `STRING` 类型，同步数据的一致性级别。（非必选）           |
| `max_log_size`   | `UINT64` 类型，redo log 的最大值。（非必选）        |
| `storage`        | `STRING` 类型，存储的目标地址。（非必选）              |
| `use_file_backend`        | `BOOL` 类型，是否将 redo log 存储到本地文件中。（非必选）              |
| `encoding_worker_num`        | `INT` 类型，redo 模块中编解码 worker 的数量。（非必选）|
|`flush_worker_num`        | `INT` 类型，redo 模块中上传文件 worker 的数量。（非必选）              |
| `compression`         | `STRING` 类型，redo 文件的压缩行为，可选值为 `""` 和 `"lz4"`。默认值为 `""`，表示不进行压缩。（非必选）        |
| `flush_concurrency`    | `INT` 类型，redo log 上传单个文件的并发数，默认值为 1，表示禁用并发。（非必选）                      |

`filter` 参数说明如下：

| 参数名                   | 说明                                                                                    |
|:----------------------|:--------------------------------------------------------------------------------------|
| `event_filters`       | event 过滤配置。（非必选）                                                                       |
| `ignore_txn_start_ts` | `UINT64 ARRAY` 类型，指定之后会忽略指定 `start_ts` 的事务，如 `[1, 2]`。（非必选）                             |
| `rules`               | `STRING ARRAY` 类型，表库过滤的规则，如 `['foo*.*', 'bar*.*']`。详情请参考[表库过滤](/table-filter.md)。（非必选） |

`filter.event_filters` 参数说明如下，可参考[日志过滤器](/ticdc/ticdc-filter.md)。

| 参数名                            | 说明                                                                                          |
|:-------------------------------|:--------------------------------------------------------------------------------------------|
| `ignore_delete_value_expr`     | `STRING ARRAY` 类型，如 `"name = 'john'"` 表示过滤掉包含 `name = 'john'` 条件的 DELETE DML。（非必选）            |
| `ignore_event`                 | `STRING ARRAY` 类型，如 `["insert"]` 表示过滤掉 INSERT 事件。（非必选）                                      |
| `ignore_insert_value_expr`     | `STRING ARRAY` 类型，如 `"id >= 100"` 表示过滤掉包含 `id >= 100` 条件的 INSERT DML。（非必选）                     |
| `ignore_sql`                   | `STRING ARRAY` 类型，如 `["^drop", "add column"]` 表示过滤掉以 `DROP` 开头或者包含 `ADD COLUMN` 的 DDL。（非必选） |
| `ignore_update_new_value_expr` | `STRING ARRAY` 类型，如 `"gender = 'male'"` 表示过滤掉新值 `gender = 'male'` 的 UPDATE DML。（非必选）          |
| `ignore_update_old_value_expr` | `STRING ARRAY` 类型，如 `"age < 18"` 表示过滤掉旧值 `age < 18` 的 UPDATE DML。（非必选）                        |
| `matcher`                      | `STRING ARRAY` 类型，是一个白名单，如 `["test.worker"]`，表示该过滤规则只应用于 `test` 库中的 `worker` 表。（非必选）             |

`mounter` 参数说明如下：

| 参数名          | 说明                                                         |
|:-------------|:-----------------------------------------------------------|
| `worker_num` | `INT` 类型。Mounter 线程数，Mounter 用于解码 TiKV 输出的数据，默认值为 `16`。（非必选） |

`sink` 参数说明如下：

| 参数名                           | 说明                                                                                                 |
|:------------------------------|:---------------------------------------------------------------------------------------------------|
| `column_selectors`            | column selector 配置。（非必选）                                                                           |
| `csv`                         | CSV 配置。（非必选）                                                                                       |
| `date_separator`              | `STRING` 类型，文件路径的日期分隔类型。可选类型有 `none`、`year`、`month` 和 `day`。默认值为 `none`，即不使用日期分隔。（非必选）             |
| `dispatchers`                 | 事件分发配置数组。（非必选）                                                                                     |
| `encoder_concurrency`         | `INT` 类型。MQ sink 中编码器的线程数。默认值为 `16`。（非必选）                                                          |
| `protocol`                    | `STRING` 类型，对于 MQ 类的 Sink，可以指定消息的协议格式。目前支持以下协议：`canal-json`、`open-protocol`、`avro`、`debezium` 和 `simple`。    |
| `schema_registry`             | `STRING` 类型，schema registry 地址。（非必选）                                                               |
| `terminator`                  | `STRING` 类型，换行符，用来分隔两个数据变更事件。默认值为空，表示使用 `"\r\n"` 作为换行符。（非必选）                                       |
| `transaction_atomicity`       | `STRING` 类型，事务一致性等级。（非必选）                                                                          |
| `only_output_updated_columns` | `BOOLEAN` 类型，对于 MQ 类型的 Sink 中的 `canal-json` 和 `open-protocol`，表示是否只向下游同步有内容更新的列。默认值为 `false`。（非必选） |
| `cloud_storage_config`        | storage sink 配置。（非必选）                                                                              |
| `open`                        | Open Protocol 配置。（非必选）                                                                             |
| `debezium`                    | Debezium Protocol 配置。（非必选）                                                                             |

`sink.column_selectors` 是一个数组，元素参数说明如下：

| 参数名       | 说明                                        |
|:----------|:------------------------------------------|
| `columns` | `STRING ARRAY` 类型，column 数组。                 |
| `matcher` | `STRING ARRAY` 类型，matcher 配置，匹配语法和过滤器规则的语法相同。 |

`sink.csv` 参数说明如下：

| 参数名                    | 说明                                              |
|:-------------------------|:------------------------------------------------|
| `delimiter`              | `STRING` 类型，字段之间的分隔符。必须为 ASCII 字符，默认值为 `,`。     |
| `include_commit_ts`      | `BOOLEAN` 类型，是否在 CSV 行中包含 commit-ts。默认值为 `false`。 |
| `null`                   | `STRING` 类型，如果这一列是 null，那这一列该如何表示。默认是用 `\N` 来表示。 |
| `quote`                  | `STRING` 类型，用于包裹字段的引号字符。空值代表不使用引号字符。默认值为 `"`。   |
| `binary_encoding_method` | `STRING` 类型，二进制类型数据的编码方式，可选 `"base64"` 或 `"hex"`。默认值为 `"base64"`。   |

`sink.dispatchers`：对于 MQ 类的 Sink，可以通过该参数配置 event 分发器，支持以下分发器：`default`、`ts`、`index-value`、`table` 。分发规则如下：

- `default`：按照 table 分发。
- `ts`：以行变更的 commitTs 做 Hash 计算并进行 event 分发。
- `index-value`：以所选的 HandleKey 列名和列值做 Hash 计算并进行 event 分发。
- `table`：以表的 schema 名和 table 名做 Hash 计算并进行 event 分发。

`sink.dispatchers` 是一个数组，元素参数说明如下：

| 参数名         | 说明                                |
|:------------|:----------------------------------|
| `matcher`   | `STRING ARRAY` 类型，匹配语法和过滤器规则的语法相同。 |
| `partition` | `STRING` 类型，事件分发的目标 partition。    |
| `topic`     | `STRING` 类型，事件分发的目标 topic。        |

`sink.cloud_storage_config` 参数说明如下：

| 参数名         | 说明                                |
|:------------|:----------------------------------|
| `worker_count`   | `INT` 类型，向下游存储服务保存数据变更记录的并发度。 |
| `flush_interval`   | `STRING` 类型，向下游存储服务保存数据变更记录的间隔。 |
| `file_size`   | `INT` 类型，单个数据变更文件的字节数超过 `file-size` 时将其保存至存储服务中。 |
| `file_expiration_days`   | `INT` 类型，文件保留的时长。|
| `file_cleanup_cron_spec`   | `STRING` 类型，定时清理任务的运行周期，与 crontab 配置兼容，格式为 `<Second> <Minute> <Hour> <Day of the month> <Month> <Day of the week (Optional)>`。|
| `flush_concurrency`   | `INT` 类型，上传单个文件的并发数。|
| `output_raw_change_event`   | `BOOLEAN` 类型，控制使用非 MySQL Sink 时是否输出原始的数据变更事件。|

`sink.open` 参数说明如下：

| 参数名                | 说明                                                            |
|:-------------------|:--------------------------------------------------------------|
| `output_old_value` | `BOOLEAN` 类型，是否输出行数据更改前的值。默认值为 `true`。关闭后，Update 事件不会输出 "p" 字段的数据。 |

`sink.debezium` 参数说明如下：

| 参数名                | 说明                                                                 |
|:-------------------|:-------------------------------------------------------------------|
| `output_old_value` | `BOOLEAN` 类型，是否输出行数据更改前的值。默认值为 `true`。关闭后，Update 事件不会输出 "before" 字段的数据。 |

### 使用样例

以下请求会创建一个 ID 为 `test5`，sink_uri 为 `blackhole://` 的同步任务。

```shell
curl -X POST -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v2/changefeeds -d '{"changefeed_id":"test5","sink_uri":"blackhole://"}'
```

如果请求成功，则返回 `200 OK`。如果请求失败，则返回错误信息和错误码。

### 响应体格式

```json
{
  "admin_job_type": 0,
  "checkpoint_time": "string",
  "checkpoint_ts": 0,
  "config": {
    "bdr_mode": true,
    "case_sensitive": false,
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

参数说明如下：

| 参数名               | 说明                                                             |
|:------------------|:---------------------------------------------------------------|
| `admin_job_type`  | `INTEGER` 类型，admin 事件类型                                       |
| `checkpoint_time` | `STRING` 类型，同步任务当前 checkpoint 的格式化时间表示                        |
| `checkpoint_ts`   | `STRING` 类型，同步任务当前 checkpoint 的 TSO 表示                        |
| `config`          | 同步任务配置，结构和含义与创建同步任务中的 `replica_config` 配置项相同                                              |
| `create_time`     | `STRING` 类型，同步任务创建的时间                                          |
| `creator_version` | `STRING` 类型，同步任务创建时 TiCDC 的版本                                  |
| `error`           | 同步任务错误                                                         |
| `id`              | `STRING` 类型，同步任务 ID                                            |
| `resolved_ts`     | `UINT64` 类型，同步任务 resolved ts                                   |
| `sink_uri`        | `STRING` 类型，同步任务的 sink uri                                     |
| `start_ts`        | `UINT64` 类型，同步任务 start ts                                      |
| `state`           | `STRING` 类型，同步任务状态，状态可分为 `normal`、`stopped`、`error`、`failed`、`finished` |
| `target_ts`       | `UINT64` 类型，同步任务的 target ts                                    |
| `task_status`     | 同步任务分发的详细状态                                                    |

`task_status` 参数说明如下：

| 参数名          | 说明                                          |
|:-------------|:--------------------------------------------|
| `capture_id` | `STRING` 类型，`Capture` ID                    |
| `table_ids`  | `UINT64 ARRAY` 类型，该 Capture 上正在同步的 table 的 ID |

`error` 参数说明如下：

| 参数名    | 说明                       |
|:-------|:-------------------------|
| `addr` | `STRING` 类型，`Capture` 地址 |
| `code` | `STRING` 类型，错误码          |
| `message` | `STRING` 类型，错误的详细信息      |

## 删除同步任务

该接口是幂等的（即其任意多次执行所产生的影响均与一次执行的影响相同），用于删除一个 changefeed 同步任务，请求成功会返回 `200 OK`。该返回结果表示服务器收到了执行命令指示，并不代表命令被成功执行。

### 请求 URI

`DELETE /api/v2/changefeeds/{changefeed_id}`

### 参数说明

#### 路径参数

| 参数名             | 说明                          |
|:----------------|:----------------------------|
| `changefeed_id` | 需要删除的同步任务 (changefeed) 的 ID |

### 使用样例

以下请求会删除 ID 为 `test1` 的同步任务。

```shell
curl -X DELETE http://127.0.0.1:8300/api/v2/changefeeds/test1
```

如果请求成功，则返回 `200 OK`。如果请求失败，则返回错误信息和错误码。

## 更新同步任务配置

该接口用于更新一个同步任务，请求成功会返回 `200 OK`。该返回结果表示服务器收到了执行命令指示，并不代表命令被成功执行。

修改 changefeed 配置需要按照`暂停任务 -> 修改配置 -> 恢复任务`的流程。

### 请求 URI

`PUT /api/v2/changefeeds/{changefeed_id}`

### 参数说明

#### 路径参数

| 参数名             | 说明                          |
|:----------------|:----------------------------|
| `changefeed_id` | 需要更新的同步任务 (changefeed) 的 ID |

#### 请求体参数

```json
{
  "replica_config": {
    "bdr_mode": true,
    "case_sensitive": false,
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

目前仅支持通过 API 修改同步任务的如下配置。

| 参数名              | 说明                                      |
|:-----------------|:----------------------------------------|
| `target_ts`      | `UINT64` 类型，指定 changefeed 的目标 TSO。（非必选） |
| `sink_uri`       | `STRING` 类型，同步任务下游的地址。（非必选)             |
| `replica_config` | sink 的配置参数, 必须是完整的配置。（非必选）              |

以上参数含义与[创建同步任务](#创建同步任务)中的参数相同，此处不再赘述。

### 使用样例

以下请求会更新 ID 为 `test1` 的同步任务的 `target_ts` 为 `32`。

```shell
 curl -X PUT -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v2/changefeeds/test1 -d '{"target_ts":32}'
```

若是请求成功，则返回 `200 OK`，若请求失败，则返回错误信息和错误码。响应的 JSON 格式以及字段含义与[创建同步任务](#创建同步任务)中的响应参数相同，此处不再赘述。

## 查询同步任务列表

该接口是一个同步接口，请求成功会返回 TiCDC 集群中所有同步任务 (changefeed) 的基本信息。

### 请求 URI

`GET /api/v2/changefeeds`

### 参数说明

#### 查询参数

| 参数名     | 说明                      |
|:--------|:------------------------|
| `state` | 非必选，指定后将会只返回该状态的同步任务的信息 |

`state` 可选值为 `all`、`normal`、`stopped`、`error`、`failed`、`finished`。

若不指定该参数，则默认返回处于 `normal`、`stopped`、`failed` 状态的同步任务基本信息。

### 使用样例

以下请求查询所有状态 (state) 为 `normal` 的同步任务的基本信息。

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

以上返回的信息的说明如下：

- `id`：同步任务的 ID。
- `state`：同步任务当前所处的[状态](/ticdc/ticdc-changefeed-overview.md#changefeed-状态流转)。
- `checkpoint_tso`：同步任务当前 checkpoint 的 TSO 表示。
- `checkpoint_time`：同步任务当前 checkpoint 的格式化时间表示。
- `error`：同步任务的错误信息。

## 查询特定同步任务

该接口是一个同步接口，请求成功会返回指定同步任务 (changefeed) 的详细信息。

### 请求 URI

`GET /api/v2/changefeeds/{changefeed_id}`

### 参数说明

#### 路径参数

| 参数名             | 说明                          |
|:----------------|:----------------------------|
| `changefeed_id` | 需要查询的同步任务 (changefeed) 的 ID |

### 使用样例

以下请求会查询 ID 为 `test1` 的同步任务的详细信息。

```shell
curl -X GET http://127.0.0.1:8300/api/v2/changefeeds/test1
```

响应的 JSON 格式以及字段含义与[创建同步任务](#创建同步任务)中的响应参数相同，此处不再赘述。

## 查询特定同步任务是否完成

该接口是一个同步接口，请求成功后会返回指定同步任务 (changefeed) 的同步完成情况，包括是否同步完成，以及一些更详细的信息。

### 请求 URI

`GET /api/v2/changefeed/{changefeed_id}/synced`

### 参数说明

#### 路径参数

| 参数名             | 说明                          |
|:----------------|:----------------------------|
| `changefeed_id` | 需要查询的同步任务 (changefeed) 的 ID |

### 使用样例

以下请求会查询 ID 为 `test1` 的同步任务的同步完成状态。

```shell
curl -X GET http://127.0.0.1:8300/api/v2/changefeed/test1/synced
```

**示例 1：同步已完成**

```json
{
  "synced": true,
  "sink_checkpoint_ts": "2023-11-30 15:14:11.015",
  "puller_resolved_ts": "2023-11-30 15:14:12.215",
  "last_synced_ts": "2023-11-30 15:08:35.510",
  "now_ts": "2023-11-30 15:14:11.511",
  "info": "Data syncing is finished"
}
```

以上返回的信息的说明如下：

- `synced`：该同步任务是否已完成。`true` 表示已完成；`false` 表示不一定完成，具体状态需要结合 `info` 字段以及其他字段进行判断。
- `sink_checkpoint_ts`：sink 模块的 checkpoint-ts 值，时间为 PD 时间。
- `puller_resolved_ts`：puller 模块的 resolved-ts 值，时间为 PD 时间。
- `last_synced_ts`：TiCDC 处理的最新一条数据的 commit-ts 值，时间为 PD 时间。
- `now_ts`：当前的 PD 时间。
- `info`：一些帮助判断同步状态的信息，特别是在 `synced` 为 `false` 时可以为你提供参考。

**示例 2：同步未完成**

```json
{
  "synced": false,
  "sink_checkpoint_ts": "2023-11-30 15:26:31.519",
  "puller_resolved_ts": "2023-11-30 15:26:23.525",
  "last_synced_ts": "2023-11-30 15:24:30.115",
  "now_ts": "2023-11-30 15:26:31.511",
  "info": "The data syncing is not finished, please wait"
}
```

此示例展示了当未完成同步任务时该接口返回的查询结果。你可以结合 `synced` 和 `info` 字段判断出数据目前还未完成同步，需要继续等待。

**示例 3：同步状态需要进一步判断**

```json
{
  "synced":false,
  "sink_checkpoint_ts":"2023-12-13 11:45:13.515",
  "puller_resolved_ts":"2023-12-13 11:45:13.525",
  "last_synced_ts":"2023-12-13 11:45:07.575",
  "now_ts":"2023-12-13 11:50:24.875",
  "info":"Please check whether PD is online and TiKV Regions are all available. If PD is offline or some TiKV regions are not available, it means that the data syncing process is complete. To check whether TiKV regions are all available, you can view 'TiKV-Details' > 'Resolved-Ts' > 'Max Leader Resolved TS gap' on Grafana. If the gap is large, such as a few minutes, it means that some regions in TiKV are unavailable. Otherwise, if the gap is small and PD is online, it means the data syncing is incomplete, so please wait"
}
```

本接口支持在上游集群遇到灾害时对同步状态进行查询判断。在部分情况下，你可能无法直接判定 TiCDC 目前的数据同步任务是否完成。此时，你可以查询该接口，并结合返回结果中的 `info` 字段以及目前上游集群的状态进行判断。

在此示例中，`sink_checkpoint_ts` 在时间上落后于 `now_ts`，这可能是因为 TiCDC 还在追数据，也可能是由于 PD 或者 TiKV 出现了故障。如果这是 TiCDC 还在追数据导致的，说明同步任务尚未完成。如果这是由于 PD 或者 TiKV 出现了故障导致的，说明同步任务已经完成。因此，你需要参考 `info` 中的信息对集群状态进行辅助判断。

**示例 4：查询报错**

```json
{
  "error_msg": "[CDC:ErrPDEtcdAPIError]etcd api call error: context deadline exceeded",
  "error_code": "CDC:ErrPDEtcdAPIError"
}
```

在上游集群的 PD 长时间故障后，查询该 API 接口时会返回类似如上的错误，无法提供进一步的判断信息。因为 PD 故障会直接影响 TiCDC 的数据同步，当遇到这类错误时，你可以认为 TiCDC 已经尽可能完成数据同步，但下游集群仍然可能存在因 PD 故障导致的数据丢失。

## 暂停同步任务

该接口暂停一个同步任务，请求成功会返回 `200 OK`。该返回结果表示服务器收到了执行命令指示，并不代表命令被成功执行。

### 请求 URI

`POST /api/v2/changefeeds/{changefeed_id}/pause`

### 参数说明

#### 路径参数

| 参数名             | 说明                          |
|:----------------|:----------------------------|
| `changefeed_id` | 需要暂停的同步任务 (changefeed) 的 ID |

### 使用样例

以下请求会暂停 ID 为 `test1` 的同步任务。

```shell
curl -X POST http://127.0.0.1:8300/api/v2/changefeeds/test1/pause
```

如果请求成功，则返回 `200 OK`。如果请求失败，则返回错误信息和错误码。

## 恢复同步任务

该接口恢复一个同步任务，请求成功会返回 `200 OK`。该返回结果表示服务器收到了执行命令指示，并不代表命令被成功执行。

### 请求 URI

`POST /api/v2/changefeeds/{changefeed_id}/resume`

### 参数说明

#### 路径参数

| 参数名             | 说明                          |
|:----------------|:----------------------------|
| `changefeed_id` | 需要恢复的同步任务 (changefeed) 的 ID |

#### 请求体参数

```json
{
  "overwrite_checkpoint_ts": 0
}
```

| 参数名                       | 说明                                                    |
|:--------------------------|:------------------------------------------------------|
| `overwrite_checkpoint_ts` | `UINT64` 类型，恢复同步任务 (changefeed) 时重新指定的 checkpoint TSO |

### 使用样例

以下请求会恢复 ID 为 `test1` 的同步任务。

```shell
curl -X POST http://127.0.0.1:8300/api/v2/changefeeds/test1/resume -d '{}'
```

如果请求成功，则返回 `200 OK`。如果请求失败，则返回错误信息和错误码。

## 查询同步子任务列表

该接口是一个同步接口，请求成功会返回当前 TiCDC 集群中的所有同步子任务 (`processor`) 的基本信息。

### 请求 URI

`GET /api/v2/processors`

### 使用样例

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

以上返回的信息的说明如下：

- `changefeed_id`：同步任务的 ID。
- `capture_id`：`Capture` 的 ID。

## 查询特定同步子任务

该接口是一个同步接口，请求成功会返回指定同步子任务 (`processor`) 的详细信息。

### 请求 URI

`GET /api/v2/processors/{changefeed_id}/{capture_id}`

### 参数说明

#### 路径参数

| 参数名             | 说明                      |
|:----------------|:------------------------|
| `changefeed_id` | 需要查询的子任务的 Changefeed ID |
| `capture_id`    | 需要查询的子任务的 Capture ID    |

### 使用样例

以下请求查询 `changefeed_id` 为 `test`、`capture_id` 为 `561c3784-77f0-4863-ad52-65a3436db6af` 的同步子任务。一个同步子任务通过 `changefeed_id` 和 `capture_id` 来标识。

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

以上返回的信息的说明如下：

- `table_ids`：在这个 capture 上同步的 table 的 ID。

## 查询 TiCDC 服务进程列表

该接口是一个同步接口，请求成功会返回当前 TiCDC 集群中的所有服务进程 (`capture`) 的基本信息。

### 请求 URI

`GET /api/v2/captures`

### 使用样例

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

以上返回的信息的说明如下：

- `id`：`capture` 的 ID。
- `is_owner`：该 `capture` 是否是 owner 。
- `address`：该 `capture` 的地址。

## 驱逐 owner 节点

该接口是一个异步的请求，请求成功会返回 `200 OK`。该返回结果表示服务器收到了执行命令指示，并不代表命令被成功执行。

### 请求 URI

`POST /api/v2/owner/resign`

### 使用样例

以下请求会驱逐 TiCDC 当前的 owner 节点，并会触发新一轮的选举，产生新的 owner 节点。

```shell
curl -X POST http://127.0.0.1:8300/api/v2/owner/resign
```

如果请求成功，则返回 `200 OK`。如果请求失败，则返回错误信息和错误码。

## 动态调整 TiCDC Server 日志级别

该接口是一个同步接口，请求成功会返回 `200 OK`。

### 请求 URI

`POST /api/v2/log`

### 请求参数

#### 请求体参数

| 参数名         | 说明        |
|:------------|:----------|
| `log_level` | 想要设置的日志等级 |

`log_level` 支持 [zap 提供的日志级别](https://godoc.org/go.uber.org/zap#UnmarshalText)："debug"、"info"、"warn"、"error"、"dpanic"、"panic"、"fatal"。

### 使用样例

```shell
curl -X POST -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v2/log -d '{"log_level":"debug"}'
```

如果请求成功，则返回 `200 OK`。如果请求失败，则返回错误信息和错误码。