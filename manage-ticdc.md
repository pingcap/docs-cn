---
title: 管理集群和同步任务
category: reference
aliases: ['/docs-cn/dev/reference/tools/ticdc/manage/']
---

# 管理集群和同步任务

目前 TiCDC 提供命令行工具 `cdc cli` 和 HTTP 接口两种方式来管理集群和同步任务。

## 使用 `cdc cli` 工具来管理集群状态和数据同步

以下内容介绍如何使用 `cdc cli` 工具来管理集群状态和数据同步。在以下接口描述中，假设 PD 的监听 IP 地址为 `127.0.0.1`，端口为 `2379`。

### 管理 TiCDC 服务进程 (`capture`)

- 查询 `capture` 列表：

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli capture list --pd=http://127.0.0.1:2379
    ```

    ```
    [
            {
                    "id": "6d92386a-73fc-43f3-89de-4e337a42b766",
                    "is-owner": true
            },
            {
                    "id": "b293999a-4168-4988-a4f4-35d9589b226b",
                    "is-owner": false
            }
    ]
    ```

### 管理同步任务 (`changefeed`)

#### 创建同步任务

使用以下命令来创建同步任务：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://127.0.0.1:2379 --sink-uri="mysql://root:123456@127.0.0.1:3306/"
create changefeed ID: 28c43ffc-2316-4f4f-a70b-d1a7c59ba79f info {"sink-uri":"mysql://root:123456@127.0.0.1:3306/","opts":{},"create-time":"2020-03-12T22:04:08.103600025+08:00","start-ts":415241823337054209,"target-ts":0,"admin-job-type":0,"config":{"filter-case-sensitive":false,"filter-rules":null,"ignore-txn-start-ts":null}}
```

其中 `--sink-uri` 需要按照以下格式进行配置，目前 scheme 支持 `mysql`/`tidb`/`kafka`。

{{< copyable "" >}}

```
[scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
```

- Sink URI 配置 `mysql`/`tidb`

    配置样例如下所示：

    {{< copyable "shell-regular" >}}

    ```shell
    --sink-uri="mysql://root:123456@127.0.0.1:3306/?worker-count=16&max-txn-row=5000"
    ```

    以上配置命令中的参数解析如下：

    | 参数         | 解析                                             |
    | :------------ | :------------------------------------------------ |
    | `root`        | 下游数据库的用户名                             |
    | `123456`       | 下游数据库密码                                     |
    | `127.0.0.1`    | 下游数据库的 IP                                |
    | `3306`         | 下游数据的连接端口                                 |
    | `worker-count` | 向下游执行 SQL 的并发度（可选，默认值为 `16`）       |
    | `max-txn-row`  | 向下游执行 SQL 的 batch 大小（可选，默认值为 `256`） |

- Sink URI 配置 `kafka`

    配置样例如下所示：

    {{< copyable "shell-regular" >}}

    ```shell
    --sink-uri="kafka://127.0.0.1:9092/cdc-test?kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1"
    ```

    以上配置命令中的参数解析如下：

    | 参数               | 解析                                                         |
    | :------------------ | :------------------------------------------------------------ |
    | `127.0.0.1`          | 下游 Kafka 对外提供服务的 IP                                 |
    | `9092`               | 下游 Kafka 的连接端口                                          |
    | `cdc-test`           | 使用的 Kafka topic 名字                                      |
    | `kafka-version`      | 下游 Kafka 版本号（可选，默认值 `2.4.0`）                      |
    | `partition-num`      | 下游 Kafka partition 数量（可选，不能大于实际 partition 数量。如果不填会自动获取 partition 数量。） |
    | `max-message-bytes`  | 每次向 Kafka broker 发送消息的最大数据量（可选，默认值 `64MB`） |
    | `replication-factor` | kafka 消息保存副本数（可选，默认值 `1`）                       |

#### 查询同步任务列表

使用以下命令来查询同步任务列表：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed list --pd=http://127.0.0.1:2379
```

```
[
        {
                "id": "28c43ffc-2316-4f4f-a70b-d1a7c59ba79f"
        }
]
```

#### 查询特定同步任务

使用以下命令来查询特定同步任务（对应某个同步任务的信息和状态）：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed query --pd=http://127.0.0.1:2379 --changefeed-id=28c43ffc-2316-4f4f-a70b-d1a7c59ba79f
```

```
{
        "info": {
                "sink-uri": "mysql://root:123456@127.0.0.1:3306/",
                "opts": {},
                "create-time": "2020-03-12T22:04:08.103600025+08:00",
                "start-ts": 415241823337054209,
                "target-ts": 0,
                "admin-job-type": 0,
                "config": {
                        "filter-case-sensitive": false,
                        "filter-rules": null,
                        "ignore-txn-start-ts": null
                }
        },
        "status": {
                "resolved-ts": 415241860902289409,
                "checkpoint-ts": 415241860640145409,
                "admin-job-type": 0
        }
}
```

以上命令中：

- `resolved-ts` 代表当前 changfeed 中最大的已经成功从 TiKV 发送到 TiCDC 的事务 TS；
- `checkpoint-ts` 代表当前 changefeed 中最大的已经成功写入下游的事务 TS；
- `admin-job-type` 代表一个 changefeed 的状态：
    - `0`: 状态正常，也是初始状态。
    - `1`: 任务暂停。停止任务后所有同步 `processor` 会结束退出，同步任务的配置和同步状态都会保留，可以从 `checkpoint-ts` 恢复任务。
    - `2`: 任务恢复，同步任务从 `checkpoint-ts` 继续同步。
    - `3`: 任务已删除，接口请求后会结束所有同步 `processor`，并清理同步任务配置信息。同步状态保留，只提供查询，没有其他实际功能。

### 停止同步任务

使用以下命令来停止同步任务：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed pause --pd=http://127.0.0.1:2379 --changefeed-id 28c43ffc-2316-4f4f-a70b-d1a7c59ba79f
```

以上命令中：

- `--changefeed=uuid` 为需要操作的 `changefeed` ID。

### 恢复同步任务

使用以下命令恢复同步任务：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed resume --pd=http://127.0.0.1:2379 --changefeed-id 28c43ffc-2316-4f4f-a70b-d1a7c59ba79f
```

以上命令中：

- `--changefeed=uuid` 为需要操作的 `changefeed` ID。

### 删除同步任务

使用以下命令删除同步任务：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed remove --pd=http://127.0.0.1:2379 --changefeed-id 28c43ffc-2316-4f4f-a70b-d1a7c59ba79f
```

- `--changefeed=uuid` 为需要操作的 `changefeed` ID。

### 管理同步子任务处理单元 (`processor`)

- 查询 `processor` 列表：

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli processor list --pd=http://127.0.0.1:2379
    ```

    ```
    [
            {
                    "id": "9f84ff74-abf9-407f-a6e2-56aa35b33888",
                    "capture-id": "b293999a-4168-4988-a4f4-35d9589b226b",
                    "changefeed-id": "28c43ffc-2316-4f4f-a70b-d1a7c59ba79f"
            }
    ]
    ```

- 查询特定 `processor`，对应于某个节点处理的同步子任务信息和状态：

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli processor query --pd=http://127.0.0.1:2379 --changefeed-id=28c43ffc-2316-4f4f-a70b-d1a7c59ba79f
    ```

    ```
    {
            "status": {
                    "table-infos": [
                            {
                                    "id": 45,
                                    "start-ts": 415241823337054209
                            }
                    ],
                    "table-p-lock": null,
                    "table-c-lock": null,
                    "admin-job-type": 0
            },
            "position": {
                    "checkpoint-ts": 415241893447467009,
                    "resolved-ts": 415241893971492865
            }
    }
    ```

## 使用 HTTP 接口管理集群状态和数据同步

目前 HTTP 接口提供一些基础的查询和运维功能。在以下接口描述中，假设 TiCDC server 的监听 IP 地址为 `127.0.0.1`，端口为 `8300`（在启动 TiCDC server 时通过 `--addr=ip:port` 指定绑定的 IP 和端口）。

### 获取 TiCDC server 状态信息的接口

使用以下命令获取 CDC server 状态信息的接口：

{{< copyable "shell-regular" >}}

```shell
curl http://127.0.0.1:8300/status
```

```
{
 "version": "0.0.1",
 "git_hash": "863f8ea889b144244ff53593a45c47ad22d37396",
 "id": "6d92386a-73fc-43f3-89de-4e337a42b766", # capture id
 "pid": 12102    # cdc server pid
}
```

### 驱逐 owner 节点

{{< copyable "shell-regular" >}}

```shell
curl -X POST http://127.0.0.1:8300/capture/owner/resign
```

以上命令仅对 owner 节点请求有效。

```
{
 "status": true,
 "message": ""
}
```

{{< copyable "shell-regular" >}}

```shell
curl -X POST http://127.0.0.1:8301/capture/owner/resign
```

以上命令对非 owner 节点请求返回错误。

```
election: not leader
```
