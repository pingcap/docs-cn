---
title: TiCDC 运维操作及任务管理
aliases: ['/docs-cn/dev/ticdc/manage-ticdc/','/docs-cn/dev/reference/tools/ticdc/manage/','/docs-cn/dev/reference/tools/ticdc/sink/','/docs-cn/dev/ticdc/sink-url/']
---

# TiCDC 运维操作及任务管理

本文档介绍如何通过 TiCDC 提供的命令行工具 `cdc cli` 管理 TiCDC 集群和同步任务，并介绍了如何使用 TiUP 来升级和修改 TiCDC 集群的配置。你也可以通过 HTTP 接口，即 TiCDC OpenAPI 来管理 TiCDC 集群和同步任务，详见 [TiCDC OpenAPI](/ticdc/ticdc-open-api.md)。

## 使用 TiUP 升级 TiCDC

本部分介绍如何使用 TiUP 来升级 TiCDC 集群。在以下例子中，假设需要将 TiCDC 组件和整个 TiDB 集群升级到 v5.3.0。

{{< copyable "shell-regular" >}}

```shell
tiup update --self && \
tiup update --all && \
tiup cluster upgrade <cluster-name> v5.3.0
```

### 升级的注意事项

* TiCDC v4.0.2 对 `changefeed` 的配置做了调整，请参阅[配置文件兼容注意事项](/ticdc/manage-ticdc.md#配置文件兼容性的注意事项)。
* 升级期间遇到的问题及其解决办法，请参阅[使用 TiUP 升级 TiDB](/upgrade-tidb-using-tiup.md#4-升级-faq)。

## 使用 TiUP 修改 TiCDC 配置

本节介绍如何使用 TiUP 的 [`tiup cluster edit-config`](/tiup/tiup-component-cluster-edit-config.md) 命令来修改 TiCDC 的配置。在以下例子中，假设需要把 TiCDC 的 `gc-ttl` 从默认值 `86400` 修改为 `3600`，即 1 小时。

首先执行以下命令。将 `<cluster-name>` 替换成实际的集群名。

{{< copyable "shell-regular" >}}

```shell
tiup cluster edit-config <cluster-name>
```

执行以上命令之后，进入到 vi 编辑器页面，修改 [`server-configs`](/tiup/tiup-cluster-topology-reference.md#server_configs) 下的 `cdc` 配置，如下所示：

```shell
 server_configs:
  tidb: {}
  tikv: {}
  pd: {}
  tiflash: {}
  tiflash-learner: {}
  pump: {}
  drainer: {}
  cdc:
    gc-ttl: 3600
```

修改完毕后执行 `tiup cluster reload -R cdc` 命令重新加载配置。

## 使用加密传输 (TLS) 功能

请参阅[为 TiDB 组件间通信开启加密传输](/enable-tls-between-components.md)。

## 使用 `cdc cli` 工具来管理集群状态和数据同步

本部分介绍如何使用 `cdc cli` 工具来管理集群状态和数据同步。`cdc cli` 是指通过 `cdc` binary 执行 `cli` 子命令。在以下接口描述中，通过 `cdc` binary 直接执行 `cli` 命令，PD 的监听 IP 地址为 `10.0.10.25`，端口为 `2379`。

> **注意：**
>
> PD 监听的 IP 和端口对应为 `pd-server` 启动时指定的 `advertise-client-urls` 参数。多个 `pd-server` 会包含多个该参数，用户可以指定其中任意一个或多个参数。例如 `--pd=http://10.0.10.25:2379` 或 `--pd=http://10.0.10.25:2379,http://10.0.10.26:2379,http://10.0.10.27:2379`。

如果你使用的 TiCDC 是用 TiUP 部署的，需要将以下命令中的 `cdc cli` 替换为 `tiup ctl cdc`。

### 管理 TiCDC 服务进程 (`capture`)

- 查询 `capture` 列表：

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli capture list --pd=http://10.0.10.25:2379
    ```

    ```
    [
      {
        "id": "806e3a1b-0e31-477f-9dd6-f3f2c570abdd",
        "is-owner": true,
        "address": "127.0.0.1:8300"
      },
      {
        "id": "ea2a4203-56fe-43a6-b442-7b295f458ebc",
        "is-owner": false,
        "address": "127.0.0.1:8301"
      }
    ]
    ```

    - `id`：服务进程的 ID。
    - `is-owner`：表示该服务进程是否为 owner 节点。
    - `address`：该服务进程对外提供接口的地址。

### 管理同步任务 (`changefeed`)

#### 同步任务状态流转

同步任务状态标识了同步任务的运行情况。在 TiCDC 运行过程中，同步任务可能会运行出错、手动暂停、恢复，或达到指定的 `TargetTs`，这些行为都可以导致同步任务状态发生变化。本节描述 TiCDC 同步任务的各状态以及状态之间的流转关系。

![TiCDC state transfer](/media/ticdc-state-transfer.png)

以上状态流转图中的状态说明如下：

- Normal：同步任务正常进行，checkpoint-ts 正常推进。
- Stopped：同步任务停止，由于用户手动暂停 (pause) changefeed。处于这个状态的 changefeed 会阻挡 GC 推进。
- Error：同步任务报错，由于某些可恢复的错误导致同步无法继续进行，处于这个状态的 changefeed 会不断尝试继续推进，直到状态转为 Normal。处于这个状态的 changefeed 会阻挡 GC 推进。
- Finished：同步任务完成，同步任务进度已经达到预设的 TargetTs。处于这个状态的 changefeed 不会阻挡 GC 推进。
- Failed：同步任务失败。由于发生了某些不可恢复的错误，导致同步无法继续进行，并且无法恢复。处于这个状态的 changefeed 不会阻挡 GC 推进。

以上状态流转图中的编号说明如下：

- ① 执行 `changefeed pause` 命令。
- ② 执行 `changefeed resume` 恢复同步任务。
- ③ `changefeed` 运行过程中发生可恢复的错误，自动进行恢复。
- ④ 执行 `changefeed resume` 恢复同步任务。
- ⑤ `changefeed` 运行过程中发生不可恢复的错误。
- ⑥ `changefeed` 已经进行到预设的 TargetTs，同步自动停止。
- ⑦ `changefeed` 停滞时间超过 `gc-ttl` 所指定的时长，不可被恢复。
- ⑧ `changefeed` 尝试自动恢复过程中发生不可恢复的错误。

#### 创建同步任务

使用以下命令来创建同步任务：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://10.0.10.25:2379 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task" --sort-engine="unified"
```

```shell
Create changefeed successfully!
ID: simple-replication-task
Info: {"sink-uri":"mysql://root:123456@127.0.0.1:3306/","opts":{},"create-time":"2020-03-12T22:04:08.103600025+08:00","start-ts":415241823337054209,"target-ts":0,"admin-job-type":0,"sort-engine":"unified","sort-dir":".","config":{"case-sensitive":true,"filter":{"rules":["*.*"],"ignore-txn-start-ts":null,"ddl-allow-list":null},"mounter":{"worker-num":16},"sink":{"dispatchers":null,"protocol":"default"},"scheduler":{"type":"table-number","polling-time":-1}},"state":"normal","history":null,"error":null}
```

- `--changefeed-id`：同步任务的 ID，格式需要符合正则表达式 `^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`。如果不指定该 ID，TiCDC 会自动生成一个 UUID（version 4 格式）作为 ID。
- `--sink-uri`：同步任务下游的地址，需要按照以下格式进行配置，目前 scheme 支持 `mysql`/`tidb`/`kafka`/`pulsar`。

    {{< copyable "" >}}

    ```
    [scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
    ```

    URI 中包含特殊字符时，需要以 URL 编码对特殊字符进行处理。

- `--start-ts`：指定 changefeed 的开始 TSO。TiCDC 集群将从这个 TSO 开始拉取数据。默认为当前时间。
- `--target-ts`：指定 changefeed 的目标 TSO。TiCDC 集群拉取数据直到这个 TSO 停止。默认为空，即 TiCDC 不会自动停止。
- `--sort-engine`：指定 changefeed 使用的排序引擎。因 TiDB 和 TiKV 使用分布式架构，TiCDC 需要对数据变更记录进行排序后才能输出。该项支持 `unified`（默认）/`memory`/`file`：

    - `unified`：优先使用内存排序，内存不足时则自动使用硬盘暂存数据。该选项默认开启。
    - `memory`：在内存中进行排序。 **不建议使用，同步大量数据时易引发 OOM。**
    - `file`：完全使用磁盘暂存数据。**已经弃用，不建议在任何情况使用。**

- `--config`：指定 changefeed 配置文件。
- `--sort-dir`: 用于指定排序器使用的临时文件目录。**自 TiDB v4.0.13, v5.0.3 和 v5.1.0 起已经无效，请不要使用**。

#### Sink URI 配置 `mysql`/`tidb`

配置样例如下所示：

{{< copyable "shell-regular" >}}

```shell
--sink-uri="mysql://root:123456@127.0.0.1:3306/?worker-count=16&max-txn-row=5000"
```

URI 中可配置的的参数如下：

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
| `time-zone`    | 连接下游 MySQL 实例时使用的时区名称，从 v4.0.8 开始生效。（可选。如果不指定该参数，使用 TiCDC 服务进程的时区；如果指定该参数但使用空值，则表示连接 MySQL 时不指定时区，使用下游默认时区） |

#### Sink URI 配置 `kafka`

配置样例如下所示：

{{< copyable "shell-regular" >}}

```shell
--sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1"
```

URI 中可配置的的参数如下：

| 参数               | 解析                                                         |
| :------------------ | :------------------------------------------------------------ |
| `127.0.0.1`          | 下游 Kafka 对外提供服务的 IP                                 |
| `9092`               | 下游 Kafka 的连接端口                                          |
| `topic-name`           | 变量，使用的 Kafka topic 名字                                      |
| `kafka-version`      | 下游 Kafka 版本号。可选，默认值 `2.4.0`，目前支持的最低版本为 `0.11.0.2`，最高版本为 `2.7.0`。该值需要与下游 Kafka 的实际版本保持一致。 |
| `kafka-client-id`    | 指定同步任务的 Kafka 客户端的 ID。可选，默认值为 `TiCDC_sarama_producer_同步任务的 ID`。 |
| `partition-num`     | 下游 Kafka partition 数量。可选，不能大于实际 partition 数量。如果不填，会自动获取 partition 数量。 |
| `max-message-bytes`  | 每次向 Kafka broker 发送消息的最大数据量（可选，默认值 `64MB`） |
| `replication-factor` | kafka 消息保存副本数（可选，默认值 `1`）                       |
| `protocol` | 输出到 kafka 消息协议，可选值有 `default`、`canal`、`avro`、`maxwell`（默认值为 `default`） |
| `max-batch-size` |  从 v4.0.9 引入。如果消息协议支持将多条变更记录输出到一条 kafka 消息，该参数指定一条 kafka 消息中变更记录的最多数量，目前仅对 Kafka 的 `protocol` 为 `default` 时有效（可选，默认值为 `16`）|
| `ca`       | 连接下游 Kafka 实例所需的 CA 证书文件路径（可选） |
| `cert`     | 连接下游 Kafka 实例所需的证书文件路径（可选） |
| `key`      | 连接下游 Kafka 实例所需的证书密钥文件路径（可选） |
| `sasl-user` | 连接下游 Kafka 实例所需的 SASL/PLAIN 或 SASL/SCRAM 验证的用户名（authcid）（可选） |
| `sasl-password` | 连接下游 Kafka 实例所需的 SASL/PLAIN 或 SASL/SCRAM 验证的密码（可选） |
| `sasl-mechanism` | 连接下游 Kafka 实例所需的 SASL/PLAIN 或 SASL/SCRAM 验证的名称（可选） |

> **注意：**
>
> 当 `protocol` 为 `default` 时，TiCDC 会尽量避免产生长度超过 `max-message-bytes` 的消息。但如果单条数据变更记录需要超过 `max-message-bytes` 个字节来表示，为了避免静默失败，TiCDC 会试图输出这条消息并在日志中输出 Warning。

#### TiCDC 集成 Kafka Connect (Confluent Platform)

> **警告：**
>
> 当前该功能为实验特性，不建议在生产环境中使用。

配置样例如下所示：

{{< copyable "shell-regular" >}}

```shell
--sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&protocol=avro&partition-num=6&max-message-bytes=67108864&replication-factor=1"
--opts registry="http://127.0.0.1:8081"
```

如要使用 Confluent 提供的 [data connectors](https://docs.confluent.io/current/connect/managing/connectors.html) 向关系型或非关系型数据库传输数据，应当选择 `avro` 协议，并在 `opts` 中提供 [Confluent Schema Registry](https://www.confluent.io/product/confluent-platform/data-compatibility/) 的 URL。请注意，`avro` 协议和 Confluent 集成目前均为**实验特性**。

集成具体步骤详见 [TiDB 集成 Confluent Platform 快速上手指南](/ticdc/integrate-confluent-using-ticdc.md)。

#### Sink URI 配置 `pulsar`

配置样例如下所示：

{{< copyable "shell-regular" >}}

```shell
--sink-uri="pulsar://127.0.0.1:6650/topic-name?connectionTimeout=2s"
```

URI 中可配置的的参数如下：

| 参数               | 解析                                                         |
| :------------------ | :------------------------------------------------------------ |
| `connectionTimeout` | 连接下游 Pulsar 的超时时间。可选参数，默认值为 30s。 |
| `operationTimeout` | 对下游 Pulsar 进行操作的超时时间（例如创建 topic）。可选参数，默认值为 30s。|
| `tlsTrustCertsFilePath` | 连接下游 Pulsar 实例所需的 CA 证书文件路径（可选） |
| `tlsAllowInsecureConnection` | 在开启 TLS 之后是否允许非加密连接（可选） |
| `tlsValidateHostname` | 是否校验下游 Pulsar 证书中的 host name（可选） |
| `maxConnectionsPerBroker` | 下游单个 Pulsar broker 最多允许的连接数（可选，默认值为 1） |
| `auth.tls` | 使用 TLS 模式认证下游 Pulsar（可选，示例 `auth=tls&auth.tlsCertFile=/path/to/cert&auth.tlsKeyFile=/path/to/key`）|
| `auth.token` | 使用 token 模式认证下游（可选，示例 `auth=token&auth.token=secret-token` 或者 `auth=token&auth.file=path/to/secret-token-file`）|
| `name` | TiCDC 中 Pulsar producer 名字（可选） |
| `maxPendingMessages` | Pending 消息队列的最大大小，例如，等待接收来自 Pulsar 的确认的消息（可选，默认值为 1000） |
| `disableBatching` | 禁止自动批量发送消息（可选） |
| `batchingMaxPublishDelay` | 设置发送消息的批处理时间（默认值为 10ms） |
| `compressionType` | 设置发送消息时使用的压缩算法（可选 `LZ4`，`ZLIB` 和 `ZSTD`，默认值为 `ZSTD`）|
| `hashingScheme` | 用于选择发送分区的哈希算法（可选 `JavaStringHash` 和 `Murmur3`，默认值为 `JavaStringHash`）|
| `properties.*` | 在 TiCDC 中 Pulsar producer 上添加用户定义的属性（可选，示例 `properties.location=Hangzhou`）|

更多关于 Pulsar 的参数解释，参见 [“pulsar-client-go ClientOptions 文档”](https://godoc.org/github.com/apache/pulsar-client-go/pulsar#ClientOptions) 和 [“pulsar-client-go ProducerOptions 文档”](https://godoc.org/github.com/apache/pulsar-client-go/pulsar#ProducerOptions) 。

#### 使用同步任务配置文件

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
    - `stopped`: 停止同步（手动暂停）
    - `error`: 停止同步（出错）
    - `removed`: 已删除任务（只在指定 `--all` 选项时才会显示该状态的任务。未指定时，可通过 `query` 查询该状态的任务）
    - `finished`: 任务已经同步到指定 `target-ts`，处于已完成状态（只在指定 `--all` 选项时才会显示该状态的任务。未指定时，可通过 `query` 查询该状态的任务）。

#### 查询特定同步任务

使用 `changefeed query` 命令可以查询特定同步任务（对应某个同步任务的信息和状态），指定 `--simple` 或 `-s` 参数会简化输出，提供最基本的同步状态和 checkpoint 信息。不指定该参数会输出详细的任务配置、同步状态和同步表信息。

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed query -s --pd=http://10.0.10.25:2379 --changefeed-id=simple-replication-task
```

```
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

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed query --pd=http://10.0.10.25:2379 --changefeed-id=simple-replication-task
```

```
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
      "case-sensitive": true,
      "enable-old-value": false,
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
        "protocol": "default"
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
        - `0`: 状态正常。
        - `1`: 任务暂停，停止任务后所有同步 `processor` 会结束退出，同步任务的配置和同步状态都会保留，可以从 `checkpoint-ts` 恢复任务。
        - `2`: 任务恢复，同步任务从 `checkpoint-ts` 继续同步。
        - `3`: 任务已删除，接口请求后会结束所有同步 `processor`，并清理同步任务配置信息。同步状态保留，只提供查询，没有其他实际功能。
- `task-status` 代表查询 changefeed 所分配的各个同步子任务的状态信息。

### 停止同步任务

使用以下命令来停止同步任务：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed pause --pd=http://10.0.10.25:2379 --changefeed-id simple-replication-task
```

以上命令中：

- `--changefeed-id=uuid` 为需要操作的 `changefeed` ID。

### 恢复同步任务

使用以下命令恢复同步任务：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed resume --pd=http://10.0.10.25:2379 --changefeed-id simple-replication-task
```

以上命令中：

- `--changefeed-id=uuid` 为需要操作的 `changefeed` ID。

### 删除同步任务

使用以下命令删除同步任务：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed remove --pd=http://10.0.10.25:2379 --changefeed-id simple-replication-task
```

- `--changefeed-id=uuid` 为需要操作的 `changefeed` ID。

### 更新同步任务配置

TiCDC 从 4.0.4 开始支持非动态修改同步任务配置，修改 changefeed 配置需要按照 `暂停任务 -> 修改配置 -> 恢复任务` 的流程。

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed pause -c test-cf --pd=http://10.0.10.25:2379
cdc cli changefeed update -c test-cf --pd=http://10.0.10.25:2379 --sink-uri="mysql://127.0.0.1:3306/?max-txn-row=20&worker-number=8" --config=changefeed.toml
cdc cli changefeed resume -c test-cf --pd=http://10.0.10.25:2379
```

当前支持修改的配置包括：

- changefeed 的 `sink-uri`
- changefeed 配置文件及文件内所有配置
- changefeed 是否使用文件排序和排序目录
- changefeed 的 `target-ts`

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
- `resolved-ts` 代表当前 processor 中已经排序数据的最大 TSO。
- `checkpoint-ts` 代表当前 processor 已经成功写入下游的事务的最大 TSO。

## 同步任务配置文件描述

本部分详细介绍了同步任务的配置。

```toml
# 指定配置文件中涉及的库名、表名是否为大小写敏感
# 该配置会同时影响 filter 和 sink 相关配置，默认为 true
case-sensitive = true

# 是否输出 old value，从 v4.0.5 开始支持，从 v5.0 开始默认为 true
enable-old-value = true

[filter]
# 忽略指定 start_ts 的事务
ignore-txn-start-ts = [1, 2]

# 过滤器规则
# 过滤规则语法：https://docs.pingcap.com/zh/tidb/stable/table-filter#表库过滤语法
rules = ['*.*', '!test.*']

[mounter]
# mounter 线程数，用于解码 TiKV 输出的数据
worker-num = 16

[sink]
# 对于 MQ 类的 Sink，可以通过 dispatchers 配置 event 分发器
# 支持 default、ts、rowid、table 四种分发器，分发规则如下：
# - default：有多个唯一索引（包括主键）时按照 table 模式分发；只有一个唯一索引（或主键）按照 rowid 模式分发；如果开启了 old value 特性，按照 table 分发
# - ts：以行变更的 commitTs 做 Hash 计算并进行 event 分发
# - rowid：以所选的 HandleKey 列名和列值做 Hash 计算并进行 event 分发
# - table：以表的 schema 名和 table 名做 Hash 计算并进行 event 分发
# matcher 的匹配语法和过滤器规则语法相同
dispatchers = [
    {matcher = ['test1.*', 'test2.*'], dispatcher = "ts"},
    {matcher = ['test3.*', 'test4.*'], dispatcher = "rowid"},
]
# 对于 MQ 类的 Sink，可以指定消息的协议格式
# 目前支持 default、canal、avro 和 maxwell 四种协议。default 为 TiCDC Open Protocol
protocol = "default"

```

### 配置文件兼容性的注意事项

* TiCDC v4.0.0 中移除了 `ignore-txn-commit-ts`，添加了 `ignore-txn-start-ts`，使用 start_ts 过滤事务。
* TiCDC v4.0.2 中移除了 `db-dbs`/`db-tables`/`ignore-dbs`/`ignore-tables`，添加了 `rules`，使用新版的数据库和数据表过滤规则，详细语法参考[表库过滤](/table-filter.md)。

## 输出行变更的历史值 <span class="version-mark">从 v4.0.5 版本开始引入</span>

> **警告：**
>
> 目前输出行变更历史值属于实验特性，尚未经过完备的测试，不建议在生产环境中使用该功能。

在默认配置下同步任务输出的 TiCDC Open Protocol 行变更数据只包含变更后的值，不包含变更前行的值，因此该输出数据不支持 TiDB 4.0 [新的 Collation 框架](/character-set-and-collation.md#新框架下的排序规则支持)，也不满足 TiCDC Open Protocol 的消费端使用行变更历史值的需求。

从 v4.0.5 开始，TiCDC 支持输出行变更数据的历史值。若要开启该特性，需要在 changefeed 的配置文件的根级别指定以下配置：

{{< copyable "" >}}

```toml
enable-old-value = true
```

开启该特性后，TiCDC Open Protocol 的输出格式参考 [TiCDC 开放数据协议 - Row Changed Event](/ticdc/ticdc-open-protocol.md#row-changed-event)，使用 MySQL sink 时也会自动支持的 TiDB 4.0 新 Collation 特性。

## 同步没有有效索引的表

从 v4.0.8 开始，TiCDC 支持通过修改任务配置来同步没有有效索引的表。若要开启该特性，需要在 `changefeed` 配置文件的根级别进行如下指定：

{{< copyable "" >}}

```toml
enable-old-value = true
force-replicate = true
```

> **警告：**
>
> 对于没有有效索引的表，`INSERT` 和 `REPLACE` 等操作不具备可重入性，因此会有数据冗余的风险。TiCDC 在同步过程中只保证数据至少分发一次，因此开启该特性同步没有有效索引的表，一定会导致数据冗余出现。如果不能接受数据冗余，建议增加有效索引，譬如增加具有 `AUTO RANDOM` 属性的主键列。

## Unified Sorter 功能

Unified Sorter 是 TiCDC 中的排序引擎功能，用于缓解以下场景造成的内存溢出问题：

+ 如果 TiCDC 数据订阅任务的暂停中断时间长，其间积累了大量的增量更新数据需要同步。
+ 从较早的时间点启动数据订阅任务，业务写入量大，积累了大量的更新数据需要同步。

对 v4.0.13 版本之后的 `cdc cli` 创建的 changefeed，默认开启 Unified Sorter。对 v4.0.13 版本前已经存在的 changefeed，则使用之前的配置。

要确定一个 changefeed 上是否开启了 Unified Sorter 功能，可执行以下示例命令查看（假设 PD 实例的 IP 地址为 `http://10.0.10.25:2379`）：

{{< copyable "shell-regular" >}}

```shell
cdc cli --pd="http://10.0.10.25:2379" changefeed query --changefeed-id=simple-replication-task | grep 'sort-engine'
```

以上命令的返回结果中，如果 `sort-engine` 的值为 "unified"，则说明 Unified Sorter 已在该 changefeed 上开启。

> **注意：**
>
> + 如果服务器使用机械硬盘或其他有延迟或吞吐有瓶颈的存储设备，请谨慎开启 Unified Sorter。
> + Unified Sorter 默认使用 `data_dir` 储存临时文件。建议保证硬盘的空闲容量大于等于 500 GiB。对于生产环境，建议保证每个节点上的磁盘可用空间大于（业务允许的最大）`checkpoint-ts` 延迟 * 业务高峰上游写入流量。此外，如果在 `changefeed` 创建后预期需要同步大量历史数据，请确保每个节点的空闲容量大于等于要追赶的同步数据。
> + Unified Sorter 默认开启，如果您的服务器不符合以上条件，并希望关闭 Unified Sorter，请手动将 changefeed 的 `sort-engine` 设为 `memory`。
> + 如需在已使用 `memory` 排序的 changefeed 上开启 Unified Sorter，参见[同步任务中断，尝试再次启动后 TiCDC 发生 OOM，如何处理](/ticdc/troubleshoot-ticdc.md#同步任务中断尝试再次启动后-ticdc-发生-oom应该如何处理)回答中提供的方法。

## 灾难场景的最终一致性复制

从 v5.3.0 版本开始，TiCDC 开始提供灾难场景下的最终一致性复制能力。具体解决的场景是，当生产集群（即 TiCDC 同步的上游集群）发生灾难、且短时间内无法恢复对外提供服务，TiCDC 需要具备保证从集群数据一致性的能力，并允许业务快速的将流量切换至从集群，避免数据库长时间不可用而对业务造成影响。

该功能支持 TiCDC 将 TiDB 集群的增量数据复制到备用关系型数据库 TiDB/Aurora/MySQL/MariaDB，在 TiCDC 正常同步没有延迟的情况下，上游发生灾难后，可以在 5 分钟内将下游集群恢复到上游的某个 snapshot 状态，并且允许丢失的数据小于 30 分钟。即 RTO <= 5min，RPO <= 30min。

### 使用前提

- 准备好具有高可用的 S3 存储或 NFS 系统，用于存储 TiCDC 的实时增量数据备份文件，在上游发生灾难情况下该文件存储可以访问。
- TiCDC 对需要具备灾难场景最终一致性的 changefeed 开启该功能，开启方式是在 changefeed 配置文件中增加以下配置：

```toml
[consistent]
# 一致性级别，选项有：
# - none： 默认值，非灾难场景，只有在任务指定 finished-ts 情况下保证最终一致性。
# - eventual： 使用 redo log，提供上游灾难情况下的最终一致性。
level = "eventual"

# 单个 redo log 文件大小，单位 MiB，默认值 64，建议该值不超过 128。
max-log-size = 64

# 刷新或上传 redo log 至 S3 的间隔，单位毫秒，默认 1000，建议范围 500-2000。
flush-interval = 1000

# 存储 redo log 的形式，包括 nfs（NFS 目录），S3（上传至S3）
storage = "s3://logbucket/test-changefeed?endpoint=http://$S3_ENDPOINT/"
```

### 灾难恢复

当上游发生灾难后，需要通过 `cdc redo` 命令在下游手动恢复。恢复流程如下：

1. 确保 TiCDC 进程已经退出，防止在数据恢复过程中上游恢复服务，TiCDC 重新开始同步数据。
2. 使用 cdc binary 进行数据恢复，具体命令如下：

```shell
cdc redo apply --tmp-dir="/tmp/cdc/redo/apply" \
    --storage="s3://logbucket/test-changefeed?endpoint=http://10.0.10.25:24927/" \
    --sink-uri="mysql://normal:123456@10.0.10.55:3306/"
```

以上命令中：

- `tmp-dir` ：指定用于下载 TiCDC 增量数据备份文件的临时目录。
- `storage` ：指定存储 TiCDC 增量数据备份文件的地址，为 S3 或者 NFS 目录。
- `sink-uri` ：恢复数据到的下游地址。scheme 仅支持 `mysql`。