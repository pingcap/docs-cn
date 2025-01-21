---
title: TiDB Data Migration 上游数据库配置文件介绍
summary: TiDB Data Migration (DM) 上游数据库配置文件包括示例与配置项说明。示例配置文件包括上游数据库的配置项，如是否开启 GTID、是否开启 relay log、拉取上游 binlog 的起始文件名等。配置项说明包括全局配置、relay log 清理策略配置、任务状态检查配置和 Binlog event filter。配置项包括标识一个 MySQL 实例、是否使用 GTID 方式、是否开启 relay log、存储 relay log 的目录等。从 DM v2.0.2 开始，Binlog event filter 也可以在上游数据库配置文件中进行配置。
---

# TiDB Data Migration 上游数据库配置文件介绍

本文介绍 TiDB Data Migration (DM) 上游数据库的配置文件，包括配置文件示例与配置项说明。

## 配置文件示例

上游数据库的示例配置文件如下所示：

```yaml
source-id: "mysql-replica-01"

# 是否开启 GTID
enable-gtid: false

# 是否开启 relay log
enable-relay: false
relay-binlog-name: ""     # 拉取上游 binlog 的起始文件名
relay-binlog-gtid: ""     # 拉取上游 binlog 的起始 GTID
# relay-dir: "relay-dir"  # 存储 relay log 的目录，默认值为 "relay-dir"。从 v6.1 版本起该配置标记为弃用，被 worker 配置中的同名参数取代

from:
  host: "127.0.0.1"
  port: 3306
  user: "root"
  password: "ZqMLjZ2j5khNelDEfDoUhkD5aV5fIJOe0fiog9w=" # 推荐使用 dmctl 对上游数据库的用户密码加密之后的密码
  security:                       # 上游数据库 TLS 相关配置
    ssl-ca: "/path/to/ca.pem"
    ssl-cert: "/path/to/cert.pem"
    ssl-key: "/path/to/key.pem"

# purge:
#   interval: 3600
#   expires: 0
#   remain-space: 15

# checker:
#   check-enable: true
#   backoff-rollback: 5m0s
#   backoff-max: 5m0s       # backoff 的最大值，不能小于 1s

# 从 DM v2.0.2 开始，Binlog event filter 也可以在上游数据库配置文件中进行配置
# case-sensitive: false
# filters:
# - schema-pattern: dmctl
#   table-pattern: t_1
#   events: []
#   sql-pattern:
#   - alter table .* add column `aaa` int
#   action: Ignore
```

> **注意：**
>
> 在 DM v2.0.1 版本中，请勿同时配置 `enable-gtid` 与 `enable-relay` 为 `true`，否则可能引发增量数据丢失问题。

## 配置项说明

### Global 配置

| 配置项        | 说明                                    |
| :------------ | :--------------------------------------- |
| `source-id` | 标识一个 MySQL 实例。|
| `enable-gtid` | 是否使用 GTID 方式从上游拉取 binlog，默认值为 false。一般情况下不需要手动配置，如果上游数据库启用了 GTID 支持，且需要做主从切换，则将该配置项设置为 true。 |
| `enable-relay` | 是否开启 relay log，默认值为 false。从 v5.4 开始，该参数生效。此外，你可以使用 `start-relay` 命令[动态开启 relay log](/dm/relay-log.md#开启关闭-relay-log)。 |
| `relay-binlog-name` | 拉取上游 binlog 的起始文件名，例如 "mysql-bin.000002"，该配置在 `enable-gtid` 为 false 的情况下生效。如果不配置该项，DM-worker 将从正在同步的最早的 binlog 文件开始拉取，一般情况下不需要手动配置。 |
| `relay-binlog-gtid` | 拉取上游 binlog 的起始 GTID，例如 "e9a1fc22-ec08-11e9-b2ac-0242ac110003:1-7849"，该配置在 `enable-gtid` 为 true 的情况下生效。如果不配置该项，DM-worker 将从正在同步的最早 binlog GTID 开始拉取 binlog，一般情况下不需要手动配置。 |
| `relay-dir` | 存储 relay log 的目录，默认值为 "./relay_log"。|
| `host` | 上游数据库的 host。|
| `port` | 上游数据库的端口。|
| `user` | 上游数据库使用的用户名。|
| `password` | 上游数据库的用户密码。注意：推荐使用 dmctl 加密后的密码。|
| `security` | 上游数据库 TLS 相关配置。配置的证书文件路径需能被所有节点访问。若配置为本地路径，则集群所有节点需要将证书文件拷贝一份放在各节点机器相同的路径位置上。|

### relay log 清理策略配置（purge 配置项）

一般情况下不需要手动配置，如果 relay log 数据量较大，磁盘空间不足，则可以通过设置该配置项来避免 relay log 写满磁盘。

| 配置项        | 说明                                    |
| :------------ | :--------------------------------------- |
| `interval` | 定期检查 relay log 是否过期的间隔时间，默认值：3600，单位：秒。 |
| `expires` | relay log 的过期时间，默认值为 0，单位：小时。未由 relay 处理单元进行写入、或已有数据迁移任务当前或未来不需要读取的 relay log 在超过过期时间后会被 DM 删除。如果不设置则 DM 不会自动清理过期的 relay log。 |
| `remain-space` | 设置最小的可用磁盘空间。当磁盘可用空间小于这个值时，DM-worker 会尝试删除 relay log，默认值：15，单位：GB。 |

> **注意：**
>
> 仅在 `interval` 不为 0 且 `expires` 和 `remain-space` 两个配置项中至少有一个不为 0 的情况下 DM 的自动清理策略才会生效。

### 任务状态检查配置（checker 配置项）

DM 会定期检查当前任务状态以及错误信息，判断恢复任务能否消除错误，并自动尝试恢复任务进行重试。DM 会使用指数回退策略调整检查间隔。这些行为可以通过如下配置进行调整：

| 配置项        | 说明                                    |
| :------------ | :--------------------------------------- |
| `check-enable` | 启用自动重试功能。 |
| `backoff-rollback` | 如果指数回退策略的间隔大于该值，且任务处于正常状态，尝试减小间隔。 |
| `backoff-max` | 指数回退策略的间隔的最大值，该值必须大于 1 秒。 |

### Binlog event filter

从 DM v2.0.2 开始，Binlog event filter 也可以在上游数据库配置文件中进行配置。

| 配置项        | 说明                                    |
| :------------ | :--------------------------------------- |
| `case-sensitive` | Binlog event filter 标识符是否大小写敏感。默认值：false。|
| `filters` | 配置 Binlog event filter，含义见 [Binlog event filter 参数解释](/dm/dm-binlog-event-filter.md#参数解释)。 |
