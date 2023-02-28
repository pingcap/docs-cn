---
title: TiCDC OpenAPI V2
summary: 了解如何使用 OpenAPI V2 接口来管理集群状态和数据同步。
---

# TiCDC OpenAPI V2

TiCDC 提供 OpenAPI 功能，你可以通过 OpenAPI V2 对 TiCDC 集群进行查询和运维操作。OpenAPI 的功能是 [`cdc cli` 工具](/ticdc/ticdc-manage-changefeed.md)的一个子集。
注意： Open API v1 将在未来版本中被删除。

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

所有 API 的请求体与返回值统一使用 JSON 格式数据。本文档以下部分描述当前提供的 API 的具体使用方法。
在下文的示例描述中，假设 TiCDC server 的监听 IP 地址为 `127.0.0.1`，端口为 `8300`（在启动 TiCDC server 时可以通过 `--addr=ip:port` 指定绑定的 IP 和端口）。

## API 统一错误格式

对 API 发起的请求后，如发生错误，返回错误信息的格式如下所示：

```json
{
    "error_msg": "",
    "error_code": ""
}
```

如上所示，`error_msg` 描述错误信息，`error_code` 则是对应的错误码。

API List 统一返回格式
一个 API 请求如果是返回一个资源列表，比如说请求返回所有的 Captures， 侧 TiCDC 统一的返回格式如下，
```json
{
"total":1,
"items":[
{"id":"d2912e63-3349-447c-90ba-wwww","is_owner":true,"address":"127.0.0.1:8300","cluster_id":"default"},
{"id":"d2912e63-3349-447c-90ba-xxxx","is_owner":false,"address":"127.0.0.1:8302","cluster_id":"default"}
]
}
```
如上所示:
- `total`: 表示有一共有多少个资源
- `items`: 当次请求返回的资源在这个数组里

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
  "version": "v6.7.0-master-dirty",
  "git_hash": "10413bded1bdb2850aa6d7b94eb375102e9c44dc",
  "id": "d2912e63-3349-447c-90ba-72a4e04b5e9e",
  "cluster_id": "default",
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
- `cluster_id`: 当前 TiCDC 集群的集群 ID
- `liveness`: 该节点的 liveness 状态， 0 表示是正常的，1 表示正在 graceful shutdown 状态

## 检查 TiCDC 集群的健康状态

该接口是一个同步接口，在集群健康的时候会返回 `200 OK`。

### 请求 URI

`GET /api/v2/health`

### 使用样例

```shell
curl -X GET http://127.0.0.1:8300/api/v1/health
```
```json
{}
```

## 创建同步任务

该接口用于向 TiCDC 提交一个同步任务，请求成功会返回 `200 OK`。

### 请求 URI

`POST /api/v2/changefeeds`

### 参数说明

使用 API 创建同步任务可选的参数不如使用 `cli` 命令创建同步任务的参数完备，以下是该 API 支持的参数。

#### 请求体参数

| 参数名                       | 说明                                      |
|:--------------------------|:----------------------------------------|
| `changefeed_id`           | `STRING` 类型，同步任务的 ID。 （非必选）             |
| `start_ts`                | `UINT64` 类型，指定 changefeed 的开始 TSO。（非必选） |
| `target_ts`               | `UINT64` 类型，指定 changefeed 的目标 TSO。（非必选） |
| **`sink_uri`**            | `STRING` 类型，同步任务下游的地址。（**必选**）          |
| `force_replicate`         | `BOOLEAN` 类型，是否强制同步没有唯一索引的表。（非必选）       |
| `ignore_ineligible_table` | `BOOLEAN` 类型，是否忽略无法进行同步的表。（非必选）         |
| `filter_rules`            | `STRING` 类型数组，表库过滤的规则。（非必选）             |
| `ignore_txn_start_ts`     | `UINT64` 类型数组，忽略指定 start_ts 的事务。 （非必选）  |
| `mounter_worker_num`      | `INT` 类型，Mounter 线程数。（非必选）              |
| `sink_config`             | sink 的配置参数。（非必选）                        |

`changefeed_id`、`start_ts`、`target_ts`、`sink_uri` 的含义和格式与[使用 cli 创建同步任务](/ticdc/ticdc-manage-changefeed.md#创建同步任务)中所作的解释相同，具体解释请参见该文档。需要注意，当在 `sink_uri` 中指定证书的路径时，须确保已将对应证书上传到对应的 TiCDC server 上。

下面会对一些需要补充说明的参数进行进一步阐述。

`force_replicate`：该值默认为 false，当指定为 true 时，同步任务会尝试强制同步没有唯一索引的表。

`ignore_ineligible_table`：该值默认为 false，当指定为 true 时，同步任务会忽略无法进行同步的表。

`filter_rules`：表库过滤的规则，如 `filter_rules = ['foo*.*', 'bar*.*']` 详情参考[表库过滤](/table-filter.md)。

`ignore_txn_start_ts`：指定之后会忽略指定 start_ts 的事务，如 `ignore-txn-start-ts = [1, 2]`。

`mounter_worker_num`： Mounter 线程数，Mounter 用于解码 TiKV 输出的数据，默认值为 16。

`sink_config`：sink 的配置参数，如下

```json
{
  "dispatchers":[
    {"matcher":["test1.*", "test2.*"], "dispatcher":"ts"},
    {"matcher":["test3.*", "test4.*"], "dispatcher":"rowid"}
  ],
  "protocol":"canal-json"
}
```

`dispatchers`：对于 MQ 类的 Sink，可以通过 dispatchers 配置 event 分发器，支持 default、ts、rowid、table 四种分发器，分发规则如下：

- default：有多个唯一索引（包括主键）时按照 table 模式分发；只有一个唯一索引（或主键）按照 rowid 模式分发；如果开启了 old value 特性，按照 table 分发。
- ts：以行变更的 commitTs 做 Hash 计算并进行 event 分发。
- rowid：以所选的 HandleKey 列名和列值做 Hash 计算并进行 event 分发。
- table：以表的 schema 名和 table 名做 Hash 计算并进行 event 分发。

`matcher`：匹配语法和过滤器规则语法相同。

`protocol`：对于 MQ 类的 Sink，可以指定消息的协议格式。目前支持 `canal-json`、`open-protocol`、`canal`、`avro` 和 `maxwell` 五种协议。

### 使用样例

以下请求会创建一个 ID 为 `test5`，sink_uri 为 `blackhole://` 的同步任务。

```shell
curl -X POST -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v2/changefeeds -d '{"changefeed_id":"test5","sink_uri":"blackhole://"}'
```

若是请求成功，则返回 `200 OK`，若请求失败，则返回错误信息和错误码。

## 删除同步任务

该接口是幂等的，用于删除一个 changefeed 同步任务，请求成功会返回 `200 OK`。

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
curl -X DELETE http://127.0.0.1:8300/api/v1/changefeeds/test1
```

若是请求成功，则返回 `204 NoContent`，若请求失败，则返回错误信息和错误码。

## 更新同步任务配置

该接口用于更新一个同步任务，请求成功会返回 `200 OK`。

修改 changefeed 配置需要按照`暂停任务 -> 修改配置 -> 恢复任务`的流程。

### 请求 URI

`PUT /api/v2/changefeeds/{changefeed_id}`

### 参数说明

#### 路径参数

| 参数名             | 说明                          |
|:----------------|:----------------------------|
| `changefeed_id` | 需要更新的同步任务 (changefeed) 的 ID |

#### 请求体参数

目前仅支持通过 API 修改同步任务的如下配置。

| 参数名                   | 说明                                      |
|:----------------------|:----------------------------------------|
| `target_ts`           | `UINT64` 类型，指定 changefeed 的目标 TSO。（非必选） |
| `sink_uri`            | `STRING` 类型，同步任务下游的地址。（非必选)             |
| `filter_rules`        | `STRING` 类型数组，表库过滤的规则。（非必选）             |
| `ignore_txn_start_ts` | `UINT64` 类型数组，忽略指定 start_ts 的事务。 （非必选）  |
| `mounter_worker_num`  | `INT` 类型，mounter 线程数。（非必选）              |
| `sink_config`         | sink 的配置参数。（非必选）                        |

以上参数含义与[创建同步任务](#创建同步任务)中的参数相同，此处不再赘述。

### 使用样例

以下请求会更新 ID 为 `test1` 的同步任务的 `mounter_worker_num` 为 `32`。

```shell
 curl -X PUT -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v2/changefeeds/test1 -d '{"mounter_worker_num":32}'
```

若是请求成功，则返回 `200 OK`，若请求失败，则返回错误信息和错误码。

## 查询同步任务列表

该接口是一个同步接口，请求成功会返回 TiCDC 集群中所有同步任务 (changefeed) 的基本信息。

### 请求 URI

`GET /api/v2/changefeeds`

### 参数说明

#### 查询参数

| 参数名     | 说明                      |
|:--------|:------------------------|
| `state` | 非必选，指定后将会只返回该状态的同步任务的信息 |

`state` 可选值为 all、normal、stopped、error、failed、finished。

若不指定该参数，则默认返回处于 normal、stopped、failed 状态的同步任务基本信息。

### 使用样例

以下请求查询所有状态 (state) 为 normal 的同步任务的基本信息。

```shell
curl -X GET http://127.0.0.1:8300/api/v2/changefeeds?state=normal
```

```json
{
  "total":2,
  "items":[
    {"upstream_id":7204854053024313036,"namespace":"default","id":"test","state":"normal","checkpoint_tso":439749918821711874,"checkpoint_time":"2023-02-27 23:46:52.888","error":null},
    {"upstream_id":7204854053024313036,"namespace":"default","id":"test2","state":"normal","checkpoint_tso":439749918821711874,"checkpoint_time":"2023-02-27 23:46:52.888","error":null}
  ]
}
```

此处对以上返回的信息做进一步阐述：

- `id`：同步任务的 ID
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
curl -X GET http://127.0.0.1:8300/api/v1/changefeeds/test1
```

```json
{
  "upstream_id":7204854053024313036,
  "namespace":"default",
  "id":"test2",
  "sink_uri":"blackhole:",
  "create_time":"2023-02-27 23:46:41.728",
  "start_ts":439749915859484676,
  "engine":"unified",
  "config":{
    "memory_quota":1073741824,
    "case_sensitive":true,
    "enable_old_value":true,
    "force_replicate":false,
    "ignore_ineligible_table":false,
    "check_gc_safe_point":true,
    "enable_sync_point":false,
    "bdr_mode":false,
    "sync_point_interval":"10m0s",
    "sync_point_retention":"24h0m0s",
    "filter":{
      "rules":["*.*"],
      "event_filters":null
    },
    "mounter":{
      "worker_num":16
    },
    "sink":{
      "protocol":"",
      "schema_registry":"",
      "csv":{
        "delimiter":",",
        "quote":"\"",
        "null":"\\N",
        "include_commit_ts":false
      },
      "column_selectors":null,
      "transaction_atomicity":"",
      "encoder_concurrency":16,
      "terminator":"\r\n",
      "date_separator":"none",
      "enable_partition_separator":false
    },
    "consistent":{"level":"none","max_log_size":64,"flush_interval":2000,"storage":""},"scheduler":{"enable_split_span":false,"region_per_span":100000}},"state":"normal","creator_version":"v6.7.0-master-dirty","resolved_ts":439749939268419588,"checkpoint_ts":439749939268419588,
  "checkpoint_time":"2023-02-27 23:48:10.886",
  "task_status":[{"capture_id":"d2912e63-3349-447c-90ba-72a4e04b5e9e","table_ids":[],"table_operations":null}]}
```

## 暂停同步任务

该接口暂停一个同步任务，请求成功会返回 `200 OK`。

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
curl -X POST http://127.0.0.1:8300/api/v1/changefeeds/test1/pause
```
```json
{}
```

若是请求成功，则返回 `200 OK`，若请求失败，则返回错误信息和错误码。

## 恢复同步任务

该接恢复一个同步任务，请求成功会返回 `202 OK`。

### 请求 URI

`POST /api/v2/changefeeds/{changefeed_id}/resume`

### 参数说明

#### 路径参数

| 参数名             | 说明                          |
|:----------------|:----------------------------|
| `changefeed_id` | 需要恢复的同步任务 (changefeed) 的 ID |

#### 请求体参数

| 参数名                        | 说明                                       |
|:---------------------------|:-----------------------------------------|
| `overwrite_checkpoint_ts`  | 恢复同步任务 (changefeed) 时重新指定的 checkpoint ts |


### 使用样例

以下请求会恢复 ID 为 `test1` 的同步任务。

```shell
curl -X POST http://127.0.0.1:8300/api/v2/changefeeds/test1/resume -d '{}'
```

若是请求成功，则返回 `200 OK`，若请求失败，则返回错误信息和错误码。

## 查询同步子任务列表

该接口是一个同步接口，请求成功会返回当前 TiCDC 集群中的所有同步子任务 (`processor`) 的基本信息。

### 请求 URI

`GET /api/v2/processors`

### 使用样例

```shell
curl -X GET http://127.0.0.1:8300/api/v1/processors
```

```json
{"total":3,
  "items":[
    {"namespace":"default","changefeed_id":"test2","capture_id":"d2912e63-3349-447c-90ba-72a4e04b5e9e"}, 
    {"namespace":"default","changefeed_id":"test1","capture_id":"d2912e63-3349-447c-90ba-72a4e04b5e9e"}, 
    {"namespace":"default","changefeed_id":"test","capture_id":"d2912e63-3349-447c-90ba-72a4e04b5e9e"}
  ]
}
```

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
curl -X GET http://127.0.0.1:8300/api/v2/processors/test1/561c3784-77f0-4863-ad52-65a3436db6af

```

```json
{"table_ids":[80]}
```

## 查询 TiCDC 服务进程列表

该接口是一个同步接口，请求成功会返回当前 TiCDC 集群中的所有服务进程 (`capture`) 的基本信息。

### 请求 URI

`GET /api/v2/captures`

### 使用样例

```shell
curl -X GET http://127.0.0.1:8300/api/v2/captures
```

```json
{"total":1,
  "items":[
    {"id":"d2912e63-3349-447c-90ba-72a4e04b5e9e","is_owner":true,"address":"127.0.0.1:8300","cluster_id":"default"}
  ]
}
```

## 驱逐 owner 节点

该接口是一个异步的请求，请求成功会返回 `200 OK`，它只代表服务器答应执行该命令，不保证命令会被成功的执行。

### 请求 URI

`POST /api/v2/owner/resign`

### 使用样例

以下请求会驱逐 TiCDC 当前的 owner 节点，并会触发新一轮的选举，产生新的 owner 节点。

```shell
curl -X POST http://127.0.0.1:8300/api/v2/owner/resign
```

若是请求成功，则返回 `200 OK`，若请求失败，则返回错误信息和错误码。

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
curl -X POST -H "'Content-type':'application/json'" http://127.0.0.1:8300/api/v1/log -d '{"log_level":"debug"}'
```
```json
{}
```

若是请求成功，则返回 `200 OK`，若请求失败，则返回错误信息和错误码。
