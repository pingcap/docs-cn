---
title: TiCDC Server 配置
summary: 了解 TiCDC 详细的命令行参数和配置文件定义。
---

# TiCDC Server 配置

本文介绍 TiCDC 的命令行参数和配置文件定义。

## `cdc server` 命令行参数说明

对于 `cdc server` 命令中可用选项解释如下：

- `addr`：TiCDC 的监听地址，提供服务的 HTTP API 查询地址和 Prometheus 查询地址，默认为 `127.0.0.1:8300`。
- `advertise-addr`：TiCDC 对外开放地址，供客户端访问。如果未设置该参数值，地址默认与 `addr` 相同。
- `pd`：TiCDC 监听的 PD 节点地址，用 `,` 来分隔多个 PD 节点地址。
- `config`：可选项，表示 TiCDC 使用的配置文件地址。TiCDC 从 v5.0.0 开始支持该选项，TiUP 从 v1.4.0 开始支持在部署 TiCDC 时使用该配置。配置文件的格式说明详见：[TiCDC Changefeed 配置参数](/ticdc/ticdc-changefeed-config.md)
- `data-dir`：指定 TiCDC 使用磁盘储存文件时的目录。目前 TiCDC 内部的排序引擎和 redo log 等特性会使用该目录储存临时文件，建议确保该目录所在设备的可用空间大于等于 500 GiB。如果你使用 TiUP，本选项可以通过配置 [`cdc_servers`](/tiup/tiup-cluster-topology-reference.md#cdc_servers) 中的 `data_dir` 来指定或默认使用 `global` 中 `data_dir` 路径。
- `gc-ttl`：TiCDC 在 PD 设置的服务级别 GC safepoint 的 TTL (Time To Live) 时长，和 TiCDC 同步任务所能够停滞的时长。单位为秒，默认值为 `86400`，即 24 小时。注意：TiCDC 同步任务的停滞会影响 TiCDC GC safepoint 的推进，即会影响上游 TiDB GC 的推进，详情可以参考 [TiCDC GC safepoint 的完整行为](/ticdc/ticdc-faq.md#ticdc-gc-safepoint-的完整行为是什么)。
- `log-file`：TiCDC 进程运行时日志的输出地址，未设置时默认为标准输出 (stdout)。
- `log-level`：TiCDC 进程运行时的日志级别，默认为 `"info"`。
- `ca`：TiCDC 创建 TLS 连接时使用的 CA 证书文件路径，PEM 格式，可选。
- `cert`：TiCDC 创建 TLS 连接时使用的证书文件路径，PEM 格式，可选。
- `cert-allowed-cn`：TiCDC 创建 TLS 连接时使用的通用名称文件路径，可选。
- `key`：TiCDC 创建 TLS 连接时使用的证书密钥文件路径，PEM 格式，可选。
- `tz`：TiCDC 服务使用的时区。TiCDC 在内部转换 `TIMESTAMP` 等时间数据类型和向下游同步数据时使用该时区，默认为进程运行本地时区。（注意如果同时指定 `tz` 参数和 `sink-uri` 中的 `time-zone` 参数，TiCDC 进程内部使用 `tz` 指定的时区，sink 向下游执行时使用 `time-zone` 指定的时区，请保持二者一致。）
- `cluster-id`：TiCDC 集群的 ID。可选，默认值为 `default`。`cluster-id` 是 TiCDC 集群的唯一标识，拥有相同 `cluster-id` 的 TiCDC 节点同属一个集群。长度最大为 128，需要符合正则表达式 `^[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*$`，且不能是以下值：`owner`，`capture`，`task`，`changefeed`，`job`，`meta`。

## `cdc server` 配置文件说明

对于 `cdc server` 命令中 `config` 参数指定的配置文件说明如下。你可以在 [`pkg/cmd/util/ticdc.toml`](https://github.com/pingcap/tiflow/blob/master/pkg/cmd/util/ticdc.toml) 找到默认值的配置文件。

### `newarch` <span class="version-mark">从 v8.5.4-release.1 版本开始引入</span>

- 控制是否开启 [TiCDC 新架构](/ticdc/ticdc-architecture.md)。
- 默认值：`false`，表示使用 [TiCDC 老架构](/ticdc/ticdc-classic-architecture.md)。
- 当设置为 `true` 时，表示开启 TiCDC 新架构。

<!-- 下面的字段的配置含义与命令行参数相同，但是命令行参数优先级更高 -->

### `addr`

- 示例值：`"127.0.0.1:8300"`

### `advertise-addr`

- 示例值：`""`

### `log-file`

- 示例值：`""`

### `log-level`

- 示例值：`"info"`

### `data-dir`

- 示例值：`""`

### `gc-ttl`

- 示例值：`86400` (24h)

### `tz`

- 示例值：`"System"`

### `cluster-id`

- 示例值：`"default"`

### `gc-tuner-memory-threshold`

- 控制 GOGC Tuner 自动调节的最大内存阈值。设置较小的阈值会提高 GC 频率；设置较大的阈值会降低 GC 频率并使 TiCDC 进程占用更多的内存资源；超过阈值后 GOGC Tuner 会停止工作。
- 默认值：`0`，表示禁用 GOGC Tuner
- 单位：Byte

### security

#### `ca-path`

- 示例值：`""`

#### `cert-path`

- 示例值：`""`

#### `key-path`

- 示例值：`""`

#### `mtls`

- 控制是否开启 TLS 客户端鉴权。
- 默认值：`false`

#### `client-user-required`

- 控制是否使用用户名和密码进行客户端鉴权。
- 默认值：`false`

#### `client-allowed-user`

- 指定可用于客户端鉴权的用户名，列表中不存在的用户的鉴权请求将被直接拒绝。
- 默认值：`null`

<!-- 示例值：`["username_1", "username_2"]` -->

### `capture-session-ttl`

- TiCDC 与 etcd 服务间的 session 时长。可选。
- 默认值：`10`
- 单位：秒

### `owner-flush-interval`

- TiCDC 集群中的 owner 模块尝试推进同步任务进度的周期，默认值为 `50000000` 纳秒（即 50 毫秒）。可选。
- 该参数有两种配置方式：只指定数字（例如，配置为 `40000000` 表示 40000000 纳秒，即 40 毫秒），或同时指定数字和单位（例如，直接配置为 `40ms`）。
- 默认值：`50000000`，即 50 毫秒

### `processor-flush-interval`

- TiCDC 集群中的 processor 模块尝试推进同步任务进度的周期，默认值为 `50000000` 纳秒（即 50 毫秒）。可选。
- 该参数配置方式与 `owner-flush-interval` 相同。
- 默认值：`50000000`，即 50 毫秒

### log

#### `error-output`

- 用于指定 zap log 模块内部的错误日志的输出位置。可选。
- 默认值：`"stderr"`

#### log.file

##### `max-size`

- 单个日志文件的最大文件大小。可选。
- 默认值：`300`
- 单位：MiB

##### `max-days`

- 日志文件最长保留天数。可选。
- 默认值：`0`，代表永不删除

##### `max-backups`

- 日志文件的保留个数。可选。
- 默认值：`0`，代表保留所有日志文件

### sorter

#### `cache-size-in-mb`

- Sorter 模块给默认启动的 8 个 pebble DB 共享的 pebble block cache 的大小。
- 默认值：`128`
- 单位：MiB

#### `sorter-dir`

- Sorter 文件相对于 `data-dir` 的目录。可选。
- 默认值：`"/tmp/sorter"`

### kv-client

#### `worker-concurrent`

- 单个 Region worker 中可使用的线程数量。可选。 
- 默认值：`8`

#### `worker-pool-size`

- TiCDC 中共享线程池中线程的数量，主要用于处理 KV 事件。可选。
- 默认值：`0`，表示默认为 CPU 核数的 2 倍

#### `region-retry-duration`

- Region 连接重试时间，默认值为 `60000000000` 纳秒（即 1 分钟）。可选。
- 该参数有两种配置方式：只指定数字（例如，配置为 `50000000` 表示 50000000 纳秒，即 50 毫秒），或同时指定数字和单位（例如，直接配置为 `50ms`）。
- 默认值：`60000000000`，即 1 分钟
