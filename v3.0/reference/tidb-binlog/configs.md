---
title: TiDB Binlog 配置说明
category: reference
aliases: ['/docs-cn/tools/binlog/overview/','/docs-cn/tools/tidb-binlog-cluster/','/docs-cn/v3.0/reference/tidb-binlog-overview/','/docs-cn/v3.0/reference/tools/tidb-binlog/overview/']
---

# TiDB Binlog 配置说明

## Pump

### addr

HTTP API 监听的地址，格式为 `host:port`。

默认：`"127.0.0.1:8250"`

### advertise-addr

对外可访问的 HTTP API 地址，这个地址会被注册到 PD，格式为 `host:port`。

默认：设定成与 `addr` 相同的配置

### socket

HTTP API 监听的 Unix socket 地址。

默认：`""`

### pd-urls

一个逗号分隔的 PD URL 列表，如果指定多个地址，PD 客户端在连接一个地址时出错会自动尝试连接下一个地址。

默认：`"http://127.0.0.1:2379"`

### data-dir

本地存放 Binlog 及其索引的目录。

默认：`"data.pump"`

### heartbeat-interval

心跳间隔，即每隔几秒向 PD 汇报一下最新的状态。

默认：`2`

### gen-binlog-interval

每隔几秒写一条 fake binlog。

默认：`3`

### gc

指定最多在本地存储几天的 Binlog，在有效范围之前的会被自动删除。

默认：`7

### log-file

日志文件路径，如果为空日志就不会保存。

默认：`""`

### log-level

Log 等级。

默认：`"info"`

### node-id

Pump 节点 ID，用于在集群中识别这个进程。

默认：`主机名:端口号`，例如 `node-1:8250`

### security

#### ssl-ca

包含可信 SSL CA 列表的文件路径，例如 `/path/to/ca.pem`。

默认：`""`

#### ssl-cert

包含 PEM 格式编码的 X509 证书文件路径，例如 `/path/to/pump.pem`。

默认：`""`

#### ssl-key

包含 PEM 格式编码的 X509 Key 文件路径，例如 `/path/to/pump-key.pem`。

默认：`""`

### storage

#### sync-log

是否在每次**批量**写入 Binlog 后使用 `fsync` 以确保数据安全。

默认：`true`

#### kv_chan_cap

在 Pump 接收写入请求时会先将请求放入一个缓冲区，这一项指定的就是缓冲区能放多少个请求。

默认：`1048576`（即 2 的 20 次方）

#### slow_write_threshold

单个 Binlog 写入耗时超过几秒就认为是慢写入，输出一条包含文本 `"take a long time to write binlog"` 的日志。

默认：`1`

#### stop-write-at-available-space

可用存储空间低于指定值时不再接收 Binlog 写入请求，可以用形如 `900 MB`，`5 GB`，`12 GiB` 的格式指定大小。
如果集群中 Pump 节点多于一个，那么在一个 Pump 因为空间不足而拒绝写入时，TiDB 端会自动写入到其他 Pump 实例。

默认：`10 GiB`

#### kv

目前 Pump 的存储实现是基于 [GoLevelDB](https://github.com/syndtr/goleveldb)，storage 下还有一个 kv 子分组可以用于调整 GoLevelDB 的配置，支持的配置项包括：

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

配置具体含义可在 [GoLevelDB 文档](https://godoc.org/github.com/syndtr/goleveldb/leveldb/opt#Options)中查看，这里不再重复。

## Drainer

### addr

HTTP API 监听的地址，格式为 `host:port`。

默认：`"127.0.0.1:8249"`

### advertise-addr

对外可访问的 HTTP API 地址，这个地址会被注册到 PD，格式为 `host:port`。

默认：设定成与 `addr` 相同的配置

### log-file

日志文件路径，如果为空日志就不会保存。

默认：`""`

### log-level

Log 等级。

默认：`"info"`

### node-id

Drainer 节点 ID，用于在集群中识别这个进程。

默认：`主机名:端口号`，例如 `node-1:8249`

### data-dir

用于存放 Drainer 运行中需要保存的文件的目录。

默认：`"data.drainer"`

### detect-interval

每隔多少秒从 PD 更新一次 Pumps 信息，以获知节点加入、离开之类的事件。

默认：`5`

### pd-urls

一个逗号分隔的 PD URL 列表，如果指定多个地址，PD 客户端在连接一个地址时出错会自动尝试连接下一个地址。

默认：`"http://127.0.0.1:2379"`

### initial-commit-ts

指定从哪个 commit timestamp 之后开始同步。
这个配置仅对初次开始同步的 Drainer 实例有效，如果下游已经有 Checkpoint 存在，
则会以 Checkpoint 里记录的时间为准。

默认：`-1`，Drainer 会从 PD 得到一个最新的 timestamp 作为初始时间。

### synced-check-time

通过 HTTP API 访问 /status 路径可以查询 Drainer 同步的状态，`synced-check-time`
指定距离上次成功同步的时间超过多少分钟可以认为是 `synced` 即同步完成。

默认：`5`

### compressor

Pump 与 Drainer 间的数据传输用何种压缩算法，目前仅支持一种算法，即 `gzip`。

默认：`""`，表示不压缩。

### security

#### ssl-ca

包含可信 SSL CA 列表的文件路径，例如 `/path/to/ca.pem`。

默认：`""`

#### ssl-cert

包含 PEM 格式编码的 X509 证书文件路径，例如 `/path/to/drainer.pem`。

默认：`""`

#### ssl-key

包含 PEM 格式编码的 X509 Key 文件路径，例如 `/path/to/drainer-key.pem`。

默认：`""`

### syncer

syncer 分组包含一些与同步下游相关的配置项。

#### db-type

下游类型，目前支持的选项有：

* mysql
* tidb
* kafka
* file

默认：`"mysql"`

#### sql-mode

当下游为 mysql/tidb 类型时，可以指定 SQL mode， 如果超过一个，则用逗号隔开。

默认：`""`

#### ignore-txn-commit-ts

同步时忽略指定 commit timestamp 的 Binlog。

默认：`[]`

#### ignore-schemas

同步时忽略指定数据库的变更，如果超过一个，则用逗号隔开。
如果一个 Binlog 中的变更全部被过滤掉，则忽略整个 Binlog。

默认：`"INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql"`

#### ignore-table

同步时忽略指定表格的变更。在 `toml` 中可以用以下方式指定多个表格：

```toml
[[syncer.ignore-table]]
db-name = "test"
tbl-name = "log"

[[syncer.ignore-table]]
db-name = "test"
tbl-name = "audit"
```

如果一个 Binlog 中的变更全部被过滤掉，则忽略整个 Binlog。

默认：`[]`

#### replicate-do-db

指定要同步的数据库，例如 `[db1, db2]`。

默认：`[]`

#### replicate-do-table

指定要同步的表格，例如：

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

当下游为 mysql/tidb 类型时，会将 DML 分批执行，
这个配置可以用于设置每个事务中包含多少个 DML。

默认：`20`

#### worker-count

当下游为 mysql/tidb 类型时，会并发执行 DML，`worker-count` 可以指定并发数。

默认：`16`

#### disable-dispatch

关掉并发，强制将 `worker-count` 置为 `1`。

默认：`false`

#### safe-mode

如果打开 safe mode，Drainer 会对同步的变更作如下修改，使其变成可重入的操作：

* Insert -> Replace Into
* Update -> Delete, Replace Into

默认：`false`

### syncer.to

不同类型下游的配置都在这个分组，以下按类型分开介绍。

#### mysql/tidb

用于连接下游数据库的几个配置项：

* `host`：如果没有设置，会尝试检查环境变量`MYSQL_HOST`，默认值`"localhost"`
* `port`：如果没有设置，会尝试检查环境变量`MYSQL_PORT`，默认值`3306`
* `user`：如果没有设置，会尝试检查环境变量`MYSQL_USER`，默认值`"root"`
* `password`：如果没有设置，会尝试检查环境变量`MYSQL_PSWD`，默认值`""`

#### file

* `dir`：指定用于保存 Binlog 的目录，如果不指定，则使用 `data-dir`。

#### kafka

当下游为 Kafka 时，有效的配置包括：

* `zookeeper-addrs`
* `kafka-addrs`
* `kafka-version`
* `kafka-max-messages`
* `topic-name`

### syncer.to.checkpoint

### type

用哪种方式保存同步进度，目前支持的选项有 `mysql` 和 `tidb`。

默认：与下游类型相同，例如`file`类型的下游进度保存在本地文件系统，`mysql`类型的下游进度保存在下游数据库。

当明确指定要使用 `mysql` 或 `tidb` 保存同步进度时，需要指定以下配置项：

* `schema`：默认为 `"tidb_binlog"`。 **注意**： 在同个集群部署多个 Drainer 时，需要为每个 Drainer 实例指定不同的 Checkpoint schema，否则两个实例的同步进度会互相覆盖。
* `host`
* `user`
* `password`
* `port`
