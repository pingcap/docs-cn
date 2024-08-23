---
title: 管理 Changefeed
summary: 了解 Changefeed 相关的各种管理手段。
---

# 管理 Changefeed

本文介绍 Changefeed 相关的各种管理方法，其中大部分功能是通过 TiCDC 的命令行工具来完成的。如果你需要，也可以通过 TiCDC 暴露的 HTTP 接口实现类似功能，详细信息参考 [TiCDC OpenAPI](/ticdc/ticdc-open-api.md)。

## 创建同步任务

使用以下命令来创建同步任务：

```shell
cdc cli changefeed create --server=http://10.0.10.25:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task"
```

```shell
Create changefeed successfully!
ID: simple-replication-task
Info: {"upstream_id":7178706266519722477,"namespace":"default","id":"simple-replication-task","sink_uri":"mysql://root:xxxxx@127.0.0.1:4000/?time-zone=","create_time":"2024-08-27T15:05:46.679218+08:00","start_ts":438156275634929669,"engine":"unified","config":{"case_sensitive":false,"enable_old_value":true,"force_replicate":false,"ignore_ineligible_table":false,"check_gc_safe_point":true,"enable_sync_point":true,"bdr_mode":false,"sync_point_interval":30000000000,"sync_point_retention":3600000000000,"filter":{"rules":["test.*"],"event_filters":null},"mounter":{"worker_num":16},"sink":{"protocol":"","schema_registry":"","csv":{"delimiter":",","quote":"\"","null":"\\N","include_commit_ts":false},"column_selectors":null,"transaction_atomicity":"none","encoder_concurrency":16,"terminator":"\r\n","date_separator":"none","enable_partition_separator":false},"consistent":{"level":"none","max_log_size":64,"flush_interval":2000,"storage":""}},"state":"normal","creator_version":"v8.1.1"}
```

## 查询同步任务列表

使用以下命令来查询同步任务列表：

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

- `checkpoint` 即为 TiCDC 已经将该时间点前的数据同步到了下游。
- `state` 为该同步任务的状态：

    - `normal`：正常同步
    - `stopped`：停止同步（手动暂停）
    - `error`：停止同步（出错）
    - `removed`：已删除任务（只在指定 `--all` 选项时才会显示该状态的任务。未指定时，可通过 `query` 查询该状态的任务）
    - `finished`：任务已经同步到指定 `target-ts`，处于已完成状态（只在指定 `--all` 选项时才会显示该状态的任务。未指定时，可通过 `query` 查询该状态的任务）。

## 查询特定同步任务

使用 `changefeed query` 命令可以查询特定同步任务（对应某个同步任务的信息和状态），指定 `--simple` 或 `-s` 参数会简化输出，提供最基本的同步状态和 checkpoint 信息。不指定该参数会输出详细的任务配置、同步状态和同步表信息。

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

以上命令中：

- `state` 代表当前 changefeed 的同步状态，各个状态必须和 `changefeed list` 中的状态相同。
- `tso` 代表当前 changefeed 中已经成功写入下游的最大事务 TSO。
- `checkpoint` 代表当前 changefeed 中已经成功写入下游的最大事务 TSO 对应的时间。
- `error` 记录当前 changefeed 是否有错误发生。

```shell
cdc cli changefeed query --server=http://10.0.10.25:8300 --changefeed-id=simple-replication-task
```

```shell
{
  "info": {
    "sink-uri": "mysql://127.0.0.1:3306/?max-txn-row=20\u0026worker-count=4",
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

以上命令中：

- `info` 代表查询 changefeed 的同步配置。
- `status` 代表查询 changefeed 的同步状态信息。

    - `resolved-ts` 代表当前 changefeed 中已经成功从 TiKV 发送到 TiCDC 的最大事务 TS。
    - `checkpoint-ts` 代表当前 changefeed 中已经成功写入下游的最大事务 TS。
    - `admin-job-type` 代表一个 changefeed 的状态：
        - `0`：状态正常。
        - `1`：任务暂停，停止任务后所有同步 `processor` 会结束退出，同步任务的配置和同步状态都会保留，可以从 `checkpoint-ts` 恢复任务。
        - `2`：任务恢复，同步任务从 `checkpoint-ts` 继续同步。
        - `3`：任务已删除，接口请求后会结束所有同步 `processor`，并清理同步任务配置信息。同步状态保留，只提供查询，没有其他实际功能。
- `task-status` 代表查询 changefeed 所分配的各个同步子任务的状态信息。

## 停止同步任务

使用以下命令来停止同步任务：

```shell
cdc cli changefeed pause --server=http://10.0.10.25:8300 --changefeed-id simple-replication-task
```

以上命令中：

- `--changefeed-id=uuid` 为需要操作的 `changefeed` ID。

## 恢复同步任务

使用以下命令恢复同步任务：

```shell
cdc cli changefeed resume --server=http://10.0.10.25:8300 --changefeed-id simple-replication-task
```

- `--changefeed-id=uuid` 为需要操作的 `changefeed` ID。
- `--overwrite-checkpoint-ts`：从 v6.2 开始支持指定 changefeed 恢复的起始 TSO。TiCDC 集群将从这个 TSO 开始拉取数据。该项支持 `now` 或一个具体的 TSO（如 434873584621453313），指定的 TSO 应在 (GC safe point, CurrentTSO] 范围内。如未指定该参数，默认从当前的 `checkpoint-ts` 同步数据。
- `--no-confirm`：恢复同步任务时无需用户确认相关信息。默认为 false。

> **注意：**
>
> - 若 `--overwrite-checkpoint-ts` 指定的 TSO `t2` 大于 changefeed 的当前 checkpoint TSO `t1`（可通过 `cdc cli changefeed query` 命令获取），则会导致 `t1` 与 `t2` 之间的数据不会同步到下游，造成数据丢失。
> - 若 `--overwrite-checkpoint-ts` 指定的 TSO `t2` 小于 changefeed 的当前 checkpoint TSO `t1`，则会导致 TiCDC 集群从一个旧的时间点 `t2` 重新拉取数据，可能会造成数据重复（例如 TiCDC 下游为 MQ sink）。

## 删除同步任务

使用以下命令删除同步任务：

```shell
cdc cli changefeed remove --server=http://10.0.10.25:8300 --changefeed-id simple-replication-task
```

- `--changefeed-id=uuid` 为需要操作的 `changefeed` ID。

## 更新同步任务配置

TiCDC 支持非动态修改同步任务配置，修改 changefeed 配置需要按照 `暂停任务 -> 修改配置 -> 恢复任务` 的流程。

```shell
cdc cli changefeed pause -c test-cf --server=http://10.0.10.25:8300
cdc cli changefeed update -c test-cf --server=http://10.0.10.25:8300 --sink-uri="mysql://127.0.0.1:3306/?max-txn-row=20&worker-count=8" --config=changefeed.toml
cdc cli changefeed resume -c test-cf --server=http://10.0.10.25:8300
```

当前支持修改的配置包括：

- changefeed 的 `sink-uri`
- changefeed 配置文件及文件内所有配置
- changefeed 的 `target-ts`

## 管理同步子任务处理单元 (`processor`)

- 查询 `processor` 列表：

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

- 查询特定 `processor`，对应于某个节点处理的同步子任务信息和状态：

    ```shell
    cdc cli processor query --server=http://10.0.10.25:8300 --changefeed-id=simple-replication-task --capture-id=b293999a-4168-4988-a4f4-35d9589b226b
    ```

    ```shell
    {
      "status": {
        "tables": {
          "56": {    # 56 表示同步表 id，对应 TiDB 中表的 tidb_table_id
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

以上命令中：

- `status.tables` 中每一个作为 key 的数字代表同步表的 id，对应 TiDB 中表的 tidb_table_id。
- `resolved-ts` 代表当前 Processor 中已经排序数据的最大 TSO。
- `checkpoint-ts` 代表当前 Processor 已经成功写入下游的事务的最大 TSO。

## 同步启用了 TiDB 新的 Collation 框架的表

从 v4.0.15、v5.0.4、v5.1.1 和 v5.2.0 开始，TiCDC 支持同步启用了 TiDB [新的 Collation 框架](/character-set-and-collation.md#新框架下的排序规则支持)的表。

## 同步没有有效索引的表

从 v4.0.8 开始，TiCDC 支持通过修改任务配置来同步没有有效索引的表。若要开启该特性，需要在 `changefeed` 配置文件的根级别进行如下指定：

```toml
force-replicate = true
```

> **警告：**
>
> 在开启 `force-replicate` 之后，不保证数据一致性。对于没有有效索引的表，`INSERT` 和 `REPLACE` 等操作不具备可重入性，因此会有数据冗余的风险。TiCDC 在同步过程中只保证数据至少分发一次，因此开启该特性同步没有有效索引的表，一定会导致数据冗余出现。如果不能接受数据冗余，建议增加有效索引，譬如增加具有 `AUTO RANDOM` 属性的主键列。

## Unified Sorter 功能

> **注意：**
>
> 从 v6.0.0 开始，TiCDC 内部默认使用 DB Sorter 引擎来对数据进行排序，不再使用 Unified Sorter。建议用户不再主动配置 Sorter 项。

Unified Sorter 是 TiCDC 中的排序引擎功能，用于缓解以下场景造成的内存溢出问题：

- 如果 TiCDC 数据订阅任务的暂停中断时间长，其间积累了大量的增量更新数据需要同步。
- 从较早的时间点启动数据订阅任务，业务写入量大，积累了大量的更新数据需要同步。

对 v4.0.13 版本之后的 `cdc cli` 创建的 changefeed，默认开启 Unified Sorter。对 v4.0.13 版本前已经存在的 changefeed，则使用之前的配置。

要确定一个 changefeed 上是否开启了 Unified Sorter 功能，可执行以下示例命令查看（假设 PD 实例的 IP 地址为 `http://10.0.10.25:2379`）：

```shell
cdc cli --server="http://10.0.10.25:8300" changefeed query --changefeed-id=simple-replication-task | grep 'sort-engine'
```

以上命令的返回结果中，如果 `sort-engine` 的值为 "unified"，则说明 Unified Sorter 已在该 changefeed 上开启。

> **注意：**
>
> - 如果服务器使用机械硬盘或其他有延迟或吞吐有瓶颈的存储设备，Unified Sorter 性能会受到较大影响。
> - Unified Sorter 默认使用 `data_dir` 储存临时文件。建议保证硬盘的空闲容量大于等于 500 GiB。对于生产环境，建议保证每个节点上的磁盘可用空间大于（业务允许的最大）`checkpoint-ts` 延迟 * 业务高峰上游写入流量。此外，如果在 `changefeed` 创建后预期需要同步大量历史数据，请确保每个节点的空闲容量大于等于要追赶的同步数据。
