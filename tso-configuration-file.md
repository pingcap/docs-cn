---
title: TSO 配置文件描述
summary: TSO 配置文件包含了多个配置项，如节点名称、数据路径、节点 URL 等。
---

# TSO 配置文件描述

<!-- markdownlint-disable MD001 -->

TSO 节点用于提供 PD 的 `tso` 微服务。本文档仅在 PD 开启微服务模式下适用。

> **Tip:**
>
> 如果你需要调整配置项的值，请参考[修改配置参数](/maintain-tidb-using-tiup.md#修改配置参数)进行操作。

### `name`

- TSO 节点名称。
- 默认值：`"TSO"`
- 如果你需要启动多个 TSO 节点，请确保不同的 TSO 节点使用不同的名字。

### `data-dir`

- TSO 节点上的数据存储路径。
- 默认值：`"default.${name}"`

### `listen-addr`

- TSO 节点监听的客户端 URL。
- 默认值：`"http://127.0.0.1:3379"`
- 部署集群时，`listen-addr` 必须指定当前主机的 IP 地址，例如 `"http://192.168.100.113:3379"`。如果运行在 Docker 中，则需要指定为 `"http://0.0.0.0:3379"`。

### `advertise-listen-addr`

- 用于外部访问 TSO 节点的 URL。
- 默认值：`"${listen-addr}"`
- 在某些情况下，例如 Docker 或者 NAT 网络环境，客户端并不能通过 TSO 节点自己监听的地址来访问 TSO 节点。此时，你可以设置 `advertise-listen-addr` 来让客户端访问。
- 例如，Docker 内部 IP 地址为 `172.17.0.1`，而宿主机的 IP 地址为 `192.168.100.113` 并且设置了端口映射 `-p 3379:3379`，那么可以设置 `advertise-listen-addr="http://192.168.100.113:3379"`，然后客户端就可以通过 `http://192.168.100.113:3379` 来找到这个服务。

### `backend-endpoints`

- TSO 节点监听其他 TSO 节点的 URL 列表。
- 默认值：`"http://127.0.0.1:2379"`

### `lease`

- TSO Primary Key 租约超时时间，超时系统重新选举 Primary。
- 默认值：3
- 单位：秒

### `tso-update-physical-interval`

- TSO 物理时钟更新周期。
- 在默认的一个 TSO 物理时钟更新周期内 (50ms)，TSO server 最多提供 262144 个 TSO。如果需要更多的 TSO，可以将这个参数调小。最小值为 `1ms`。
- 缩短这个参数会增加 TSO server 的 CPU 消耗。根据测试，相比 `50ms` 更新周期，更新周期为 `1ms` 时，TSO server 的 CPU 占用率 ([CPU usage](https://man7.org/linux/man-pages/man1/top.1.html)) 将增加约 10%。
- 默认值：50ms
- 最小值：1ms

## security

安全相关配置项。

### `cacert-path`

- CA 文件路径
- 默认值：""

### `cert-path`

- 包含 X.509 证书的 PEM 文件路径
- 默认值：""

### `key-path`

- 包含 X.509 key 的 PEM 文件路径
- 默认值：""

### `redact-info-log`

- 控制 TSO 节点日志脱敏的开关
- 该配置项值设为 true 时将对 TSO 节点的日志脱敏，遮蔽日志中的用户信息。
- 默认值：false

## log

日志相关的配置项。

### `level`

- 指定日志的输出级别。
- 可选值："debug"，"info"，"warn"，"error"，"fatal"
- 默认值："info"

### `format`

- 日志格式。
- 可选值："text"，"json"
- 默认值："text"

### `disable-timestamp`

- 是否禁用日志中自动生成的时间戳。
- 默认值：false

## log.file

日志文件相关的配置项。

### `max-size`

- 单个日志文件最大大小，超过该值系统自动切分成多个文件。
- 默认值：300
- 单位：MiB
- 最小值为 1

### `max-days`

- 日志保留的最长天数。
- 如果未设置本参数或把本参数设置为默认值 `0`，TSO 节点不清理日志文件。
- 默认：0

### `max-backups`

- 日志文件保留的最大个数。
- 如果未设置本参数或把本参数设置为默认值 `0`，TSO 节点会保留所有的日志文件。
- 默认：0

## metric

监控相关的配置项。

### `interval`

- 向 Prometheus 推送监控指标数据的间隔时间。
- 默认：15s
