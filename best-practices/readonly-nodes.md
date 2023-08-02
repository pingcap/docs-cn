---
title: 只读存储节点最佳实践
summary: 介绍如何通过使用只读存储节点，达到物理隔离部分流量的目的。
---

# 只读存储节点最佳实践

本文档介绍如何配置只读存储节点，以及如何将备份、分析、测试等流量导向这些节点，使这些对延迟要求较低的负载与线上重要服务在物理上达到隔离的效果。

## 操作步骤

### 1. 将部分 TiKV 节点指定为只读节点

通过给 TiKV 节点标记特殊 label（使用 `$` 作为 label key 的前缀）的方式，可以把部分节点指定为特殊只读节点。除非通过设置 Placement Rules 的方式显式指定这些节点存储某些数据，否则 PD 不会调度任何数据到这些节点上。

只读节点可通过执行 `tiup cluster edit-config` 命令进行配置：

```
tikv_servers:
  - host: ...
    ...
    labels:
      $mode: readonly
```

### 2. 将数据以 learner 形式存储在只读节点

1. 使用如下 `pd-ctl config placement-rules` 命令导出默认 Placement Rules：

    ```shell
    pd-ctl config placement-rules rule-bundle load --out="rules.json"
    ```

    如果之前没有配置过 Placement Rules，那么会导出如下内容：

    ```json
    [
      {
        "group_id": "pd",
        "group_index": 0,
        "group_override": false,
        "rules": [
          {
            "group_id": "pd",
            "id": "default",
            "start_key": "",
            "end_key": "",
            "role": "voter",
            "count": 3
          }
        ]
      }
    ]
    ```

2. 将所有数据在只读节点以 learner 方式存储一份。如下示例基于默认配置：

    ```json
    [
      {
        "group_id": "pd",
        "group_index": 0,
        "group_override": false,
        "rules": [
          {
            "group_id": "pd",
            "id": "default",
            "start_key": "",
            "end_key": "",
            "role": "voter",
            "count": 3
          },
          {
            "group_id": "pd",
            "id": "readonly",
            "start_key": "",
            "end_key": "",
            "role": "learner",
            "count": 1,
            "label_constraints": [
              {
                "key": "$mode",
                "op": "in",
                "values": [
                  "readonly"
                ]
              }
            ],
            "version": 1
          }
        ]
      }
    ]
    ```

3. 执行 `pd-ctl config placement-rules` 命令将上面的配置写入 PD：

    ```shell
    pd-ctl config placement-rules rule-bundle save --in="rules.json"
    ```

> **注意：**
>
> - 当对已存在大量数据的集群进行如上操作时，整个集群可能需要一段时间才能将数据完全复制到只读节点上。在这期间，只读节点可能无法进行服务。
>
> - 因为备份的特殊下推实现机制，每个 label 所对应的 learner 数量不能超过 1，否则会导致在备份时产生重复数据。

### 3. 使用 Follower Read 功能读取只读节点

#### 3.1 在 TiDB 中使用 Follower Read

你可以将系统变量 [`tidb_replica_read`](/system-variables.md#tidb_replica_read-从-v40-版本开始引入) 设置为 `learner` 来读取只读节点上的数据：

```sql
set tidb_replica_read=learner;
```

#### 3.2 在 TiSpark 中使用 Follower Read

你可以在 Spark 配置文件中设置 `spark.tispark.replica_read = learner` 来读取只读节点上的数据：

```
spark.tispark.replica_read learner
```

#### 3.3 在备份集群数据时只备份 Follower 节点

你可以在 br 命令行中添加 `--replica-read-label` 参数，来读取只读节点上的数据。注意，在 shell 中运行如下命令时需使用单引号包裹 label，以防止 `$` 被 shell 解析。

```shell
br backup full ... --replica-read-label '$mode:readonly'
```
