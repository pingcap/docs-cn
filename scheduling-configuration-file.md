---
title: Scheduling 配置文件描述
summary: Scheduling 配置文件包含了多个配置项，如节点名称、数据路径、节点 URL 等。
---

# Scheduling 配置文件描述

<!-- markdownlint-disable MD001 -->

Scheduling 节点用于提供 PD 的 `scheduling` 微服务。本文档仅在 PD 开启微服务模式下适用。

> **Tip:**
>
> 如果你需要调整配置项的值，请参考[修改配置参数](/maintain-tidb-using-tiup.md#修改配置参数)进行操作。

### `name`

- Scheduling 节点名称。
- 默认值：`"Scheduling"`
- 如果你需要启动多个 Scheduling 节点，请确保不同的 Scheduling 节点使用不同的名字。

### `data-dir`

- Scheduling 节点上的数据存储路径。
- 默认值：`"default.${name}"`

### `listen-addr`

- Scheduling 节点监听的客户端 URL。
- 默认值：`"http://127.0.0.1:3379"`
- 部署集群时，`listen-addr` 必须指定当前主机的 IP 地址，例如 `"http://192.168.100.113:3379"`。如果运行在 Docker 中，则需要指定为 `"http://0.0.0.0:3379"`。

### `advertise-listen-addr`

- 用于外部访问 Scheduling 节点的 URL。
- 默认值：`"${listen-addr}"`
- 在某些情况下，例如 Docker 或者 NAT 网络环境，客户端并不能通过 Scheduling 节点自己监听的地址来访问 Scheduling 节点。此时，你可以设置 `advertise-listen-addr` 来让客户端访问。
- 例如，Docker 内部 IP 地址为 `172.17.0.1`，而宿主机的 IP 地址为 `192.168.100.113` 并且设置了端口映射 `-p 2379:2379`，那么可以设置 `advertise-listen-addr="http://192.168.100.113:2379"`，然后客户端就可以通过 `http://192.168.100.113:2379` 来找到这个服务。

### `backend-endpoints`

- Scheduling 节点监听其他 Scheduling 节点的 URL 列表。
- 默认值：`"http://127.0.0.1:2379"`

### `lease`

- Scheduling Primary Key 租约超时时间，超时系统重新选举 Primary。
- 默认值：3
- 单位：秒

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

- 控制 Scheduling 节点日志脱敏的开关
- 该配置项值设为 true 时将对 Scheduling 日志脱敏，遮蔽日志中的用户信息。
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
- 如果未设置本参数或把本参数设置为默认值 `0`，Scheduling 不清理日志文件。
- 默认：0

### `max-backups`

- 日志文件保留的最大个数。
- 如果未设置本参数或把本参数设置为默认值 `0`，Scheduling 会保留所有的日志文件。
- 默认：0

## metric

监控相关的配置项。

### `interval`

- 向 Prometheus 推送监控指标数据的间隔时间。
- 默认：15s
