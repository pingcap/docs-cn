---
title: TiCDC
category: reference
aliases: ['/docs-cn/dev/reference/tools/ticdc/overview/', '/docs-cn/dev/reference/tools/ticdc/manage/','/docs-cn/dev/reference/tools/ticdc/sink/','/docs-cn/dev/ticdc/sink-url/']
---

# TiCDC

> **注意：**
>
> TiCDC 目前为实验特性，不建议在生产环境中使用。

[TiCDC](https://github.com/pingcap/ticdc) 是一款通过拉取 TiKV 变更日志实现的 TiDB 增量数据同步工具，具有将数据还原到与上游任意 TSO 一致状态的能力，同时提供[开放数据协议](/ticdc/ticdc-open-protocol.md) (TiCDC Open Protocol)，支持其他系统订阅数据变更。

## 架构

TiCDC 运行时是一种无状态节点，通过 PD 内部的 etcd 实现高可用。TiCDC 集群支持创建多个同步任务，向多个不同的下游进行数据同步。

TiCDC 的系统架构如下图所示：

![TiCDC architecture](/media/cdc-architecture.png)

## 系统概念介绍

- TiKV CDC 组件：只输出 key-value (KV) change log。
    - 集成在 TiKV 中。
    - 内部逻辑拼装 KV change log。
    - 提供输出 KV change log 的接口，发送数据包括实时 change log 和增量扫的 change log。

- `capture`：TiCDC 运行进程，多个 `capture` 组成一个 TiCDC 集群，负责 KV change log 的同步。
    - 由 `cdc server` 启动。
    - 每个 `capture` 负责拉取一部分 KV change log。
    - 对拉取的一个或多个 KV change log 进行排序。
    - 向下游还原事务或按照 TiCDC Open Protocol 进行输出。

- `processor`: 运行在 `capture` 内部的同步任务处理单元，负责同步单个表。

- `changefeed`: 运行在 TiCDC 集群上的同步任务
    - 通过 `cdc cli changefeed` 创建并管理。
    - 指定了需要同步表（同步子任务），同步子任务运行在 `processor` 中。
    - 指定了输出的下游地址。

## 部署

### 使用 TiUP 部署

#### 使用 TiUP 部署包含 TiCDC 组件的 TiDB 集群

详细操作参考[使用 TiUP 部署 TiCDC](/production-deployment-using-tiup.md#第-3-步编辑初始化配置文件)。

#### 使用 TiUP 在原有 TiDB 集群上新增 TiCDC 组件

1. 首先确认当前 TiDB 的版本支持 TiCDC，否则需要先升级 TiDB 集群至 4.0.0 rc.1 或更新版本。

2. 参考 [扩容 TiDB/TiKV/PD/TiCDC 节点](/scale-tidb-using-tiup.md#扩容-ticdc-节点) 章节对 TiCDC 进行部署。

### 在原有 TiDB 集群上使用 binary 部署 TiCDC 组件

假设 PD 集群有一个可以提供服务的 PD 节点（client URL 为 `10.0.10.25:2379`）。若要部署三个 TiCDC 节点，可以按照以下命令启动集群。只需要指定相同的 PD 地址，新启动的节点就可以自动加入 TiCDC 集群。

{{< copyable "shell-regular" >}}

```shell
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_1.log --addr=0.0.0.0:8301 --advertise-addr=127.0.0.1:8301
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_2.log --addr=0.0.0.0:8302 --advertise-addr=127.0.0.1:8302
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_3.log --addr=0.0.0.0:8303 --advertise-addr=127.0.0.1:8303
```

对于 `cdc server` 命令中可用选项解释如下：

- `gc-ttl`: TiCDC 在 PD 设置的服务级别 GC safepoint 的 TTL (Time To Live) 时长，单位为秒，默认值为 `86400`，即 24 小时。
- `pd`: PD client 的 URL。
- `addr`: TiCDC 的监听地址，提供服务的 HTTP API 查询地址和 Prometheus 查询地址。
- `advertise-addr`: TiCDC 对外访问地址。
- `tz`: TiCDC 服务使用的时区。TiCDC 在内部转换 timestamp 等时间数据类型和向下游同步数据时使用该时区，默认为进程运行本地时区。
- `log-file`: TiCDC 进程运行日志的地址，默认为 `cdc.log`。
- `log-level`: TiCDC 进程运行时默认的日志级别，默认为 `info`。

## 管理同步任务 (`changefeed`)

这节内容介绍如何使用 `cdc cli` 工具来管理集群状态和数据同步。在以下接口描述中，假设 PD 的监听 IP 地址为 `127.0.0.1`，端口为 `2379`。

### 创建同步任务

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

### 查询同步任务列表

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

### 查询特定同步任务

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


## 管理 TiCDC 服务进程 (`capture`)

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

## 管理同步子任务处理单元 (`processor`)

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

## 使用 HTTP 接口管理集群状态

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

## TiCDC 常见问题

在使用 TiCDC 过程中经常遇到的问题以及相对应的解决方案请参考 [TiCDC 常见问题](/ticdc/troubleshoot-ticdc.md)。

## TiCDC 开放数据协议

TiCDC Open Protocol 是一种行级别的数据变更通知协议，为监控、缓存、全文索引、分析引擎、异构数据库的主从复制等提供数据源。TiCDC 遵循 TiCDC Open Protocol，向 MQ (Message Queue) 等第三方数据媒介复制 TiDB 的数据变更。详细信息参考 [TiCDC 开放数据协议](/ticdc/ticdc-open-protocol.md)。

### sink 支持

目前 TiCDC sink 模块支持同步数据到以下下游：

- MySQL 协议兼容的数据库，提供最终一致性支持。
- 以 TiCDC Open Protocol 输出到 Kafka，可实现行级别有序、最终一致性或严格事务一致性三种一致性保证。

## 同步限制

将数据同步到 TiDB 或 MySQL，需要满足以下条件才能保证正确性：

- 表必须要有主键或者唯一索引。
- 如果表只存在唯一索引，至少有一个唯一索引的每一列在表结构中明确定义 `NOT NULL`。

### 暂不支持的场景

目前 TiCDC（4.0 发布版本）与部分 TiDB 特性存在冲突，在后续的 TiCDC 版本上会逐渐修复。当前版本需要做相应的兼容性处理。暂不支持的场景如下：

- 暂不支持同步分区表。
- 暂不支持单独使用 RawKV 的 TiKV 集群。
- 暂不支持 TiDB 4.0 [新的 Collation 框架](/character-set-and-collation.md#新框架下的-collation-支持)。如果开启该功能，需保证下游集群为 TiDB 并使用与上游相同的 collation，否则会出现 collation 导致的无法定位数据的问题。
- 暂不支持 TiDB 4.0 中[创建 SEQUENCE 的 DDL 操作](/sql-statements/sql-statement-create-sequence.md) 和 [SEQUENCE 函数](/sql-statements/sql-statement-create-sequence.md#sequence-函数)。在上游 TiDB 使用 SEQUENCE 时，TiCDC 将会忽略掉上游执行的 SEQUENCE DDL 操作/函数，但是使用 SEQUENCE 函数的 DML 操作可以正确地同步。
- 暂不支持 [TiKV Hibernate Region](https://github.com/tikv/tikv/blob/master/docs/reference/configuration/raftstore-config.md#hibernate-region)。TiCDC 会使 Region 无法进入静默状态。

TiCDC 本身也有部分功能尚未完善，将在后续的 TiCDC 版本逐渐修复：

- TiCDC 集群扩容后，不支持将已有的同步表调度到新的 TiCDC 节点中。
- 暂不支持库表同步黑白名单。
