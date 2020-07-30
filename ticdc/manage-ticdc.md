---
title: TiCDC 运维操作及任务管理
aliases: ['/docs-cn/dev/reference/tools/ticdc/manage/','/docs-cn/dev/reference/tools/ticdc/sink/','/docs-cn/dev/ticdc/sink-url/']
---

# TiCDC 运维操作及任务管理

本文档介绍如何部署 TiCDC 集群，以及如何通过 TiCDC 提供的命令行工具 `cdc cli` 和 HTTP 接口两种方式来管理 TiCDC 集群和同步任务。

## TiCDC 部署

### 软件和硬件环境推荐配置

在生产环境中，TiCDC 的软件和硬件配置推荐如下：

| Linux 操作系统平台       | 版本         |
| :----------------------- | :----------: |
| Red Hat Enterprise Linux | 7.3 及以上   |
| CentOS                   | 7.3 及以上   |

| **CPU** | **内存** | **硬盘类型** | **网络** | **实例数量(最低要求)** |
| --- | --- | --- | --- | --- |
| 16 核+ | 64 GB+ | SSD | 万兆网卡（2 块最佳） | 2 |

更多信息参见 [TiDB 软件和硬件环境建议配置](/hardware-and-software-requirements.md)

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
- `ca`: TiCDC 使用的 CA 证书文件路径，PEM 格式，可选。
- `cert`: TiCDC 使用的证书文件路径，PEM 格式，可选。
- `key`: TiCDC 使用的证书密钥文件路径，PEM 格式，可选。

## 使用加密传输 (TLS) 功能

请参阅[为 TiDB 组件间通信开启加密传输](/enable-tls-between-components.md)。

## 使用 `cdc cli` 工具来管理集群状态和数据同步

以下内容介绍如何使用 `cdc cli` 工具来管理集群状态和数据同步。在以下接口描述中，假设 PD 的监听 IP 地址为 `10.0.10.25`，端口为 `2379`。

### 管理 TiCDC 服务进程 (`capture`)

- 查询 `capture` 列表：

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli capture list --pd=http://10.0.10.25:2379
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
cdc cli changefeed create --pd=http://10.0.10.25:2379 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task"
Create changefeed successfully!
ID: simple-replication-task
Info: {"sink-uri":"mysql://root:123456@127.0.0.1:3306/","opts":{},"create-time":"2020-03-12T22:04:08.103600025+08:00","start-ts":415241823337054209,"target-ts":0,"admin-job-type":0,"sort-engine":"memory","sort-dir":".","config":{"case-sensitive":true,"filter":{"rules":["*.*"],"ignore-txn-start-ts":null,"ddl-allow-list":null},"mounter":{"worker-num":16},"sink":{"dispatchers":null,"protocol":"default"},"cyclic-replication":{"enable":false,"replica-id":0,"filter-replica-ids":null,"id-buckets":0,"sync-ddl":false},"scheduler":{"type":"table-number","polling-time":-1}},"state":"normal","history":null,"error":null}
```

- `--changefeed-id`: 同步任务的 ID，格式需要符合正则表达式 `^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`。如果不指定该 ID，TiCDC 会自动生成一个 UUID（version 4 格式）作为 ID。
- `--sink-uri`: 同步任务下游的地址，需要按照以下格式进行配置，目前 scheme 支持 `mysql`/`tidb`/`kafka`。

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
    | `ssl-ca`       | 连接下游 MySQL 实例所需的 CA 证书文件路径（可选） |
    | `ssl-cert`     | 连接下游 MySQL 实例所需的证书文件路径（可选） |
    | `ssl-key`      | 连接下游 MySQL 实例所需的证书密钥文件路径（可选） |

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
    | `kafka-client-id`    | 指定同步任务的 Kafka 客户端的 ID（可选，默认值为 `TiCDC_sarama_producer_同步任务的 ID`） |
    | `partition-num`      | 下游 Kafka partition 数量（可选，不能大于实际 partition 数量。如果不填会自动获取 partition 数量。） |
    | `max-message-bytes`  | 每次向 Kafka broker 发送消息的最大数据量（可选，默认值 `64MB`） |
    | `replication-factor` | kafka 消息保存副本数（可选，默认值 `1`）                       |
    | `protocol` | 输出到 kafka 消息协议，可选值有 `default`, `canal`（默认值为 `default`）    |
    | `ca`       | 连接下游 Kafka 实例所需的 CA 证书文件路径（可选） |
    | `cert`     | 连接下游 Kafka 实例所需的证书文件路径（可选） |
    | `key`      | 连接下游 Kafka 实例所需的证书密钥文件路径（可选） |

如需设置更多同步任务的配置，比如指定同步单个数据表，请参阅[同步任务配置文件描述](#同步任务配置文件描述)。

使用配置文件创建同步任务的方法如下：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://10.0.10.25:2379 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --config changefeed.toml
```

其中 `changefeed.toml` 为同步任务的配置文件。

#### 查询同步任务列表

使用以下命令来查询同步任务列表：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed list --pd=http://10.0.10.25:2379
```

```
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
    - `normal`: 正常同步
    - `stopped`: 停止同步（手动暂停或出错）
    - `removed`: 已删除任务

#### 查询特定同步任务

使用以下命令来查询特定同步任务（对应某个同步任务的信息和状态）：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed query --pd=http://10.0.10.25:2379 --changefeed-id=simple-replication-task
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

- `resolved-ts` 代表当前 changefeed 中最大的已经成功从 TiKV 发送到 TiCDC 的事务 TS；
- `checkpoint-ts` 代表当前 changefeed 中最大的已经成功写入下游的事务 TS；
- `admin-job-type` 代表一个 changefeed 的状态：
    - `0`: 状态正常。
    - `1`: 任务暂停，停止任务后所有同步 `processor` 会结束退出，同步任务的配置和同步状态都会保留，可以从 `checkpoint-ts` 恢复任务。
    - `2`: 任务恢复，同步任务从 `checkpoint-ts` 继续同步。
    - `3`: 任务已删除，接口请求后会结束所有同步 `processor`，并清理同步任务配置信息。同步状态保留，只提供查询，没有其他实际功能。

### 停止同步任务

使用以下命令来停止同步任务：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed pause --pd=http://10.0.10.25:2379 --changefeed-id simple-replication-task
```

以上命令中：

- `--changefeed=uuid` 为需要操作的 `changefeed` ID。

### 恢复同步任务

使用以下命令恢复同步任务：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed resume --pd=http://10.0.10.25:2379 --changefeed-id simple-replication-task
```

以上命令中：

- `--changefeed=uuid` 为需要操作的 `changefeed` ID。

### 删除同步任务

使用以下命令删除同步任务：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed remove --pd=http://10.0.10.25:2379 --changefeed-id simple-replication-task
```

- `--changefeed=uuid` 为需要操作的 `changefeed` ID。

### 管理同步子任务处理单元 (`processor`)

- 查询 `processor` 列表：

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli processor list --pd=http://10.0.10.25:2379
    ```

    ```
    [
            {
                    "id": "9f84ff74-abf9-407f-a6e2-56aa35b33888",
                    "capture-id": "b293999a-4168-4988-a4f4-35d9589b226b",
                    "changefeed-id": "simple-replication-task"
            }
    ]
    ```

- 查询特定 `processor`，对应于某个节点处理的同步子任务信息和状态：

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli processor query --pd=http://10.0.10.25:2379 --changefeed-id=simple-replication-task --capture-id=b293999a-4168-4988-a4f4-35d9589b226b
    ```

    ```
    {
      "status": {
        "tables": {
          "56": {    # 56 表示同步表 id，对应 TiDB 中表的 tidb_table_id
            "start-ts": 417474117955485702,
            "mark-table-id": 0  # mark-table-id 是用于环形复制时标记表的 id，对应于 TiDB 中标记表的 tidb_table_id
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

- `status.tables` 中每一个作为 key 的数字代表同步表的 id，对应 TiDB 中表的 tidb_table_id；
- `mark-table-id` 是用于环形复制时标记表的 id，对应于 TiDB 中标记表的 tidb_table_id；
- `resolved-ts` 代表当前 processor 中已经排序数据的最大 TSO；
- `checkpoint-ts` 代表当前 processor 已经成功写入下游的事务的最大 TSO；

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

### 手动调度表到其他节点

{{< copyable "shell-regular" >}}

```shell
curl -X POST curl 127.0.0.1:8300/capture/owner/move_table -X POST -d 'cf-id=cf060953-036c-4f31-899f-5afa0ad0c2f9&target-cp-id=6f19a6d9-0f8c-4dc9-b299-3ba7c0f216f5&table-id=49'
```

参数说明

| 参数名        | 说明 |
| :----------- | :--- |
| `cf-id`        | 进行调度的 Changefeed ID |
| `target-cp-id` | 目标 Capture ID |
| `table-id`     | 需要调度的 Table ID |

以上命令仅对 owner 节点请求有效。对非 owner 节点将会返回错误。

```
{
 "status": true,
 "message": ""
}
```

## 同步任务配置文件描述

以下内容详细介绍了同步任务的配置。

```toml
# 指定配置文件中涉及的库名、表名是否为大小写敏感
# 该配置会同时影响 filter 和 sink 相关配置，默认为 true
case-sensitive = true

[filter]
# 忽略指定 start_ts 的事务
ignore-txn-start-ts = [1, 2]

# 过滤器规则
# 过滤规则语法：https://docs.pingcap.com/zh/tidb/stable/table-filter#%E8%A1%A8%E5%BA%93%E8%BF%87%E6%BB%A4%E8%AF%AD%E6%B3%95
rules = ['*.*', '!test.*']

[mounter]
# mounter 线程数，用于解码 TiKV 输出的数据
worker-num = 16

[sink]
# 对于 MQ 类的 Sink，可以通过 dispatchers 配置 event 分发器
# 支持 default、ts、rowid、table 四种分发器
# matcher 匹配语法和过滤器相同
dispatchers = [
    {matcher = ['test1.*', 'test2.*'], dispatcher = "ts"},
    {matcher = ['test3.*', 'test4.*'], dispatcher = "rowid"},
]
# 对于 MQ 类的 Sink，可以指定消息的协议格式
# 目前支持 default 和 canal 两种协议。default 为 TiCDC Open Protocol
protocol = "default"

[cyclic-replication]
# 是否开启环形同步
enable = false
# 当前 TiCDC 的复制 ID
replica-id = 1
# 需要过滤掉的同步 ID
filter-replica-ids = [2,3]
# 是否同步 DDL
sync-ddl = true
```

### 配置文件兼容性的注意事项

* TiCDC v4.0.0 中移除了 `ignore-txn-commit-ts`，添加了 `ignore-txn-start-ts`，使用 start_ts 过滤事务。
* TiCDC v4.0.2 中移除了 `db-dbs`/`db-tables`/`ignore-dbs`/`ignore-tables`，添加了 `rules`，使用新版的数据库和数据表过滤规则，详细语法参考[表库过滤](/table-filter.md)。

## 环形同步

> **警告：**
>
> 目前环形同步属于实验特性，尚未经过完备的测试，不建议在生产环境中使用该功能。

环形同步功能支持在多个独立的 TiDB 集群间同步数据。比如有三个 TiDB 集群 A、B 和 C，它们都有一个数据表 `test.user_data`，并且各自对它有数据写入。环形同步功能可以将 A、B 和 C 对 `test.user_data` 的写入同步其它集群上，使三个集群上的 `test.user_data` 达到最终一致。

### 环形同步使用示例

在三个集群 A、B 和 C 上开启环形复制，其中 A 到 B 的同步使用两个 TiCDC。A 作为三个集群的 DDL 入口。

![TiCDC cyclic replication](/media/cdc-cyclic-replication.png)

使用环形同步功能时，需要设置同步任务的创建参数：

+ `--cyclic-replica-id`：用于指定为上游集群的写入指定来源 ID，需要确保每个集群 ID 的唯一性。
+ `--cyclic-filter-replica-ids`：用于指定需要过滤的写入来源 ID，通常为下游集群的 ID。
+ `--cyclic-sync-ddl`：用于指定是否同步 DDL 到下游，只能在一个集群的 CDC 上开启 DDL 同步。

环形同步任务创建步骤如下：

1. 在 TiDB 集群 A，B 和 C 上[启动 TiCDC 组件](#ticdc-部署)。

    {{< copyable "shell-regular" >}}

    ```shell
    # 在 TiDB 集群 A 上启动 TiCDC 组件。
    cdc server \
        --pd="http://${PD_A_HOST}:${PD_A_PORT}" \
        --log-file=ticdc_1.log \
        --addr=0.0.0.0:8301 \
        --advertise-addr=127.0.0.1:8301

    # 在 TiDB 集群 B 上启动 TiCDC 组件。
    cdc server \
        --pd="http://${PD_B_HOST}:${PD_B_PORT}" \
        --log-file=ticdc_2.log \
        --addr=0.0.0.0:8301 \
        --advertise-addr=127.0.0.1:8301

    # 在 TiDB 集群 C 上启动 TiCDC 组件。
    cdc server \
        --pd="http://${PD_C_HOST}:${PD_C_PORT}" \
        --log-file=ticdc_3.log \
        --addr=0.0.0.0:8301 \
        --advertise-addr=127.0.0.1:8301
    ```

2. 在 TiDB 集群 A，B 和 C 上创建环形同步需要使用的标记数据表 (`mark table`)。

    {{< copyable "shell-regular" >}}

    ```shell
    # 在 TiDB 集群 A 上创建标记数据表。
    cdc cli changefeed cyclic create-marktables \
        --cyclic-upstream-dsn="root@tcp(${TIDB_A_HOST}:${TIDB_A_PORT})/" \
        --pd="http://${PD_A_HOST}:${PD_A_PORT}"

    # 在 TiDB 集群 B 上创建标记数据表。
    cdc cli changefeed cyclic create-marktables \
        --cyclic-upstream-dsn="root@tcp(${TIDB_B_HOST}:${TIDB_B_PORT})/" \
        --pd="http://${PD_B_HOST}:${PD_B_PORT}"

    # 在 TiDB 集群 C 上创建标记数据表。
    cdc cli changefeed cyclic create-marktables \
        --cyclic-upstream-dsn="root@tcp(${TIDB_C_HOST}:${TIDB_C_PORT})/" \
        --pd="http://${PD_C_HOST}:${PD_C_PORT}"
    ```

3. 在 TiDB 集群 A，B 和 C 上创建环形同步任务。

    {{< copyable "shell-regular" >}}

    ```shell
    # 在 TiDB 集群 A 上创建环形同步任务。
    cdc cli changefeed create \
        --sink-uri="mysql://root@${TiDB_B_HOST}/" \
        --pd="http://${PD_A_HOST}:${PD_A_PORT}" \
        --cyclic-replica-id 1 \
        --cyclic-filter-replica-ids 2 \
        --cyclic-sync-ddl true

    # 在 TiDB 集群 B 上创建环形同步任务。
    cdc cli changefeed create \
        --sink-uri="mysql://root@${TiDB_C_HOST}/" \
        --pd="http://${PD_B_HOST}:${PD_B_PORT}" \
        --cyclic-replica-id 2 \
        --cyclic-filter-replica-ids 3 \
        --cyclic-sync-ddl true

    # 在 TiDB 集群 C 上创建环形同步任务。
    cdc cli changefeed create \
        --sink-uri="mysql://root@${TiDB_A_HOST}/" \
        --pd="http://${PD_C_HOST}:${PD_C_PORT}" \
        --cyclic-replica-id 3 \
        --cyclic-filter-replica-ids 1 \
        --cyclic-sync-ddl false
    ```

### 环形同步使用说明

1. 在创建环形同步任务前，必须使用 `cdc cli changefeed cyclic create-marktables` 创建环形同步功能使用到的标记表。
2. 开启环形同步的数据表名字需要符合正则表达式 `^[a-zA-Z0-9_]+$`。
3. 在创建环形同步任务前，开启环形复制的数据表必须已创建完毕。
4. 开启环形复制后，不能创建一个会被环形同步任务同步的表。
5. 如果想在线 DDL，需要确保以下两点：
    1. 多个集群的 TiCDC 构成一个单向 DDL 同步链，不能成环，例如示例中只有 C 集群的 TiCDC 关闭了 `sync-ddl`。
    2. DDL 必须在单向 DDL 同步链的开始集群上执行，例如示例中的 A 集群。
