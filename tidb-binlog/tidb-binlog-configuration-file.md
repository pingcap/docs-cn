---
title: TiDB Binlog 配置说明
---

# TiDB Binlog 配置说明

本文档介绍 TiDB Binlog 的各项配置说明。

## Pump

本节介绍 Pump 的配置项。可以在 [Pump Configuration](https://github.com/pingcap/tidb-binlog/blob/master/cmd/pump/pump.toml) 中查看完整的 Pump 配置文件示例。

### addr

* HTTP API 的监听地址，格式为 `host:port`。
* 默认：`"127.0.0.1:8250"`

### advertise-addr

* 对外可访问的 HTTP API 地址。这个地址会被注册到 PD，格式为 `host:port`。
* 默认：与 `addr` 的配置相同。

### socket

* HTTP API 监听的 Unix socket 地址。
* 默认：`""`

### pd-urls

* 由逗号分隔的 PD URL 列表。如果指定了多个地址，PD 客户端在连接一个地址时出错时会自动尝试连接另一个地址。
* 默认：`"http://127.0.0.1:2379"`

### data-dir

* 本地存放 binlog 及其索引的目录。
* 默认：`"data.pump"`

### heartbeat-interval

* 心跳间隔，即每隔指定秒数向 PD 汇报最新的状态。
* 默认：`2`

### gen-binlog-interval

* 指定写入 fake binlog 的间隔秒数。
* 默认：`3`

### gc

* 指定 binlog 可在本地存储的天数（整型）。超过指定天数的 binlog 会被自动删除。
* 默认：`7`

### log-file

* 保存日志文件的路径。如果为空，日志不会被保存。
* 默认：`""`

### log-level

* Log 等级。
* 默认：`"info"`

### node-id

* Pump 节点的 ID，用于在集群中识别这个进程。
* 默认：`主机名:端口号`，例如 `node-1:8250`。

### security

以下是与安全相关的配置项。

#### ssl-ca

* 包含可信 SSL 证书或 CA 证书列表的文件路径，例如 `/path/to/ca.pem`。
* 默认：`""`

#### ssl-cert

* 包含 PEM 格式编码的 X509 证书文件路径，例如 `/path/to/pump.pem`。
* 默认：`""`

#### ssl-key

* 包含 PEM 格式编码的 X509 Key 文件路径，例如 `/path/to/pump-key.pem`。
* 默认：`""`

### storage

以下是与存储相关的配置项。

#### sync-log

* 指定是否在每次**批量**写入 binlog 后使用 `fsync` 以确保数据安全。
* 默认：`true`

#### kv_chan_cap

* 在 Pump 接收写入请求时会先将请求放入一个缓冲区，该项指定缓冲区能存放的请求数量。
* 默认：`1048576`（即 2 的 20 次方）

#### slow_write_threshold

* 写入单个 binlog 的耗时超过该项设定的秒数就被认为是慢写入，并输出一条包含 `"take a long time to write binlog"` 的日志。
* 默认：`1`

#### stop-write-at-available-space

* 可用存储空间低于指定值时不再接收 binlog 写入请求。可以用例如 `900 MB`、`5 GB`、`12 GiB` 的格式指定空间大小。如果集群中 Pump 节点多于一个，那么在某个 Pump 节点因为空间不足而拒绝写入时，TiDB 端会自动写入到其他 Pump 节点。
* 默认：`10 GiB`

#### kv

目前 Pump 的存储是基于 [GoLevelDB](https://github.com/syndtr/goleveldb) 实现的。`storage` 下还有一个 kv 子分组可以用于调整 GoLevelDB 的配置，支持的配置项包括：

* block-cache-capacity
* block-restart-interval
* block-size
* compaction-L0-trigger
* compaction-table-size
* compaction-total-size
* compaction-total-size-multiplier
* write-buffer
* write-L0-pause-trigger
* write-L0-slowdown-trigger

配置具体含义可在 [GoLevelDB 文档](https://godoc.org/github.com/syndtr/goleveldb/leveldb/opt#Options)中查看。

## Drainer

本节介绍 Drainer 的配置项。可以在 [Drainer Configuration](https://github.com/pingcap/tidb-binlog/blob/master/cmd/drainer/drainer.toml) 中查看完整的配置文件示例。

### addr

* HTTP API 的监听的地址，格式为 `host:port`。
* 默认：`"127.0.0.1:8249"`

### advertise-addr

* 对外可访问的 HTTP API 地址，这个地址会被注册到 PD，格式为 `host:port`。
* 默认：设定成与 `addr` 相同的配置

### log-file

* 日志的文件保存路径。如果为空，日志不会被保存。
* 默认：`""`

### log-level

* Log 等级。
* 默认：`"info"`

### node-id

* Drainer 节点 ID，用于在集群中识别这个进程。
* 默认：`主机名:端口号`，例如 `node-1:8249`。

### data-dir

* 用于存放 Drainer 运行中需要保存的文件的目录。
* 默认：`"data.drainer"`

### detect-interval

* 每隔指定秒数从 PD 更新一次 Pumps 信息，以获取节点加入或离开等事件。
* 默认：`5`

### pd-urls

* 由逗号分隔的 PD URL 列表。如果指定了多个地址，PD 客户端在连接一个地址出错时会自动尝试连接另一个地址。
* 默认：`"http://127.0.0.1:2379"`

### initial-commit-ts

* 指定从哪个事务提交时间点（事务的 commit ts） 之后开始同步。这个配置仅适用于初次开始同步的 Drainer 节点。如果下游已经有 checkpoint 存在，则会根据 checkpoint 里记录的时间进行同步。
* commit ts 是 TiDB 事务的提交时间点，是从 PD 获取的全局唯一递增的时间戳作为当前事务的唯一 ID，典型 initial-commit-ts 配置可以通过以下方式获得
    - BR 备份元信息 backupmeta 中记录的 backup TS
    - Dumpling 备份元信息 metadata 中记录的 Pos
    - PD control 中 tso 命令返回的结果
* 默认：`-1`。Drainer 会从 PD 得到一个最新的 timestamp 作为初始时间。即从当前的时间点开始同步。

### synced-check-time

* 通过 HTTP API 访问 `/status` 路径可以查询 Drainer 同步的状态。`synced-check-time` 指定距离上次成功同步的时间超过多少分钟可以认为是 `synced`，即同步完成。
* 默认：`5`

### compressor

* 指定 Pump 与 Drainer 间的数据传输所用的压缩算法。目前仅支持一种算法，即 `gzip`。
* 默认：`""`，表示不压缩。

### security

以下是与 Drainer 安全相关的配置。

#### ssl-ca

* 包含可信 SSL 证书或 CA 证书列表的文件路径，例如 `/path/to/ca.pem`。
* 默认：`""`

#### ssl-cert

* 包含 PEM 格式编码的 X509 证书文件路径，例如 `/path/to/drainer.pem`。
* 默认：`""`

#### ssl-key

* 包含 PEM 格式编码的 X509 Key 文件路径，例如 `/path/to/drainer-key.pem`。
* 默认：`""`

### syncer

syncer 分组包含一些与同步下游相关的配置项。

#### db-type

下游类型，目前支持的选项有：

* `mysql`
* `tidb`
* `kafka`
* `file`

默认：`mysql`

#### sql-mode

* 当下游为 `mysql`/`tidb` 类型时，可以指定 SQL mode，如果超过一个 mode，则用逗号隔开。
* 默认：`""`

#### ignore-txn-commit-ts

* 同步时，该项所指定的 commit timestamp 的 binlog 会被忽略，例如 `[416815754209656834, 421349811963822081]`。
* 默认：`[]`

#### ignore-schemas

* 同步时忽略指定数据库的变更。如果超过一个需忽略的数据库，则用逗号隔开。如果一个 binlog 中的变更全部被过滤掉，则忽略整个 binlog。
* 默认：`"INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql"`

#### ignore-table

同步时忽略指定表格的变更。在 `toml` 中可以用以下方式指定多个需忽略的表格：

{{< copyable "" >}}

```toml
[[syncer.ignore-table]]
db-name = "test"
tbl-name = "log"

[[syncer.ignore-table]]
db-name = "test"
tbl-name = "audit"
```

如果一个 binlog 中的变更全部被过滤掉，则忽略整个 binlog。

默认：`[]`

#### replicate-do-db

* 指定要同步的数据库，例如 `[db1, db2]`。
* 默认：`[]`

#### replicate-do-table

指定要同步的表格，示例如下：

{{< copyable "" >}}

```toml
[[syncer.replicate-do-table]]
db-name ="test"
tbl-name = "log"

[[syncer.replicate-do-table]]
db-name ="test"
tbl-name = "~^a.*"
```

默认：`[]`

#### txn-batch

* 当下游为 `mysql`/`tidb` 类型时，会将 DML 分批执行。这个配置可以用于设置每个事务中包含多少个 DML。
* 默认：`20`

#### worker-count

* 当下游为 `mysql`/`tidb` 类型时，会并发执行 DML，`worker-count` 可以指定并发数。
* 默认：`16`

#### disable-dispatch

* 关掉并发，强制将 `worker-count` 置为 `1`。
* 默认：`false`

#### safe-mode

如果打开 Safe mode，Drainer 会对同步的变更作以下修改，使其变成可重入的操作：

* `Insert` 变为 `Replace Into`
* `Update` 变为 `Delete` 和 `Replace Into`

默认：`false`

### syncer.to

不同类型的下游配置都在 `syncer.to` 分组。以下按配置类型进行介绍。

#### mysql/tidb

用于连接下游数据库的配置项：

* `host`：如果没有设置，会尝试检查环境变量 `MYSQL_HOST`，默认值为 `"localhost"`。
* `port`：如果没有设置，会尝试检查环境变量 `MYSQL_PORT`，默认值为 `3306`。
* `user`：如果没有设置，会尝试检查环境变量 `MYSQL_USER`，默认值为 `"root"`。
* `password`：如果没有设置，会尝试检查环境变量 `MYSQL_PSWD`，默认值为 `""`。

#### file

* `dir`：指定用于保存 binlog 的目录。如果不指定该项，则使用 `data-dir`。

#### kafka

当下游为 `kafka` 时，有效的配置包括：

* `zookeeper-addrs`
* `kafka-addrs`
* `kafka-version`
* `kafka-max-messages`
* `topic-name`

### syncer.to.checkpoint

以下是 `syncer.to.checkpoint` 相关的配置项。

### type

* 指定用哪种方式保存同步进度。
* 目前支持的选项：`mysql` 和 `tidb`

* 默认：与下游类型相同。例如 `file` 类型的下游进度保存在本地文件系统，`mysql` 类型的下游进度保存在下游数据库。当明确指定要使用 `mysql` 或 `tidb` 保存同步进度时，需要指定以下配置项：

    * `schema`：默认为 `"tidb_binlog"`。

        > **注意：**
        >
        > 在同个 TiDB 集群中部署多个 Drainer 时，需要为每个 Drainer 节点指定不同的 checkpoint schema，否则两个实例的同步进度会互相覆盖。

    * `host`
    * `user`
    * `password`
    * `port`
