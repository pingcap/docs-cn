---
title: DM-worker 完整配置说明
category: reference
---

# DM-worker 完整配置说明

## 配置文件示例

```toml
# Worker Configuration.

# log configuration
log-level = "info"
log-file = "dm-worker.log"

# DM-worker listening address
worker-addr = ":8262"

# Represents a MySQL/MariaDB instance or a replication group
source-id = "mysql-replica-01"

# Server id of slave for binlog replication
# Each instance (master and slave) in the replication group should have a different server id
server-id = 101

# flavor: mysql/mariadb
flavor = "mysql"

# directory that used to store relay log
relay-dir = "./relay_log"

# enable gtid in relay log unit
enable-gtid = false

relay-binlog-name = ""
relay-binlog-gtid = ""

[from]
host = "127.0.0.1"
user = "root"
password = "Up8156jArvIPymkVC+5LxkAT6rek"
port = 3306

# Relay log purge strategy
[purge]
interval = 3600
expires = 24
remain-space = 15

# Task status checker
[checker]
check-enable = true
backoff-rollback = "5m"
backoff-max = "5m"
```

## 配置项说明

### Global 配置

| 配置项        | 说明                                    |
| :------------ | :--------------------------------------- |
| `log-level` | 日志等级，值可以为 "debug"、"info"、"warn"、"error"、"fatal"，默认值为 "info"。一般情况下不需要手动配置，如果需要排查问题，可以将等级设置为 "debug"。 |
| `log-file` | 日志文件，如果不配置日志会输出到标准输出中。 |
| `worker-addr` | DM-worker 服务的地址，可以省略 IP 信息，例如：":8262"。 |
| `source-id` | 标识一个 MySQL/MariaDB 实例或者 replication group。 |
| `server-id` | DM-worker 作为上游 MySQL/MariaDB slave 来获取 binlog 的 server id，该值在一个 replication group （包括 master 和 slave）中必须是唯一的。v1.0.2 及以上版本的 DM 会自动生成，不需要手动配置该项。 |
| `flavor` | 上游数据库的类型，目前值可以为 "mysql" 或者 "mariadb"。v1.0.2 及以上版本的 DM 会自动判断上游版本，不需要手动配置该项。 |
| `relay-dir` | 存储 relay log 的目录，默认值为 "./relay_log"。 |
| `enable-gtid` | 是否使用 GTID 方式从上游拉取 binlog，默认值为 false。一般情况下不需要手动配置，如果上游数据库启用了 GTID 支持，且需要做主从切换，则将该配置项设置为 true。 |
| `relay-binlog-name` | 拉取上游 binlog 的起始文件名，例如 "mysql-bin.000002"，该配置在 `enable-gtid` 为 false 的情况下生效。如果不配置该项，v1.0.2 之前版本的 DM-worker 将从上游 MySQL 或 MariaDB 现有最早时间点的 binlog 文件开始拉取 binlog，拉取到数据同步任务需要的最新 binlog 可能需要很长时间；v1.0.2 及之后版本的 DM-worker 将从最新时间点的 binlog 文件开始拉取 binlog，一般情况下不需要手动配置。 |
| `relay-binlog-gtid` | 拉取上游 binlog 的起始 GTID，例如 "e9a1fc22-ec08-11e9-b2ac-0242ac110003:1-7849"，该配置在 `enable-gtid` 为 true 的情况下生效。如果不配置该项，v1.0.2 之前版本的 DM-worker 将从上游 MySQL 或 MariaDB 现有最早时间点的 binlog GTID 开始拉取 binlog，拉取到数据同步任务需要的最新 binlog 可能需要很长时间；v1.0.2 及之后版本的 DM-worker 将从最新时间点的 binlog GTID 开始拉取 binlog，一般情况下不需要手动配置。 |

### 数据库链接配置（from 配置项）

| 配置项        | 说明                                    |
| :------------ | :--------------------------------------- |
| `host` | 上游数据库的 host。 |
| `port` | 上游数据库的端口。 |
| `user` | 连接数据库使用的用户名。 |
| `password` | 连接数据库使用的密码。注意：需要使用 dmctl 加密后的密码。 |

### relay log 清理策略配置（purge 配置项）

一般情况下不需要手动配置，如果 relay log 数据量较大，磁盘空间不足，则可以通过该配置项设置，避免 relay log 写满磁盘。

| 配置项        | 说明                                    |
| ------------ | --------------------------------------- |
| `interval` | 定期检查 relay log 是否过期的间隔时间，默认值：3600，单位：秒。 |
| `expires` | relay log 的过期时间，默认值为 0，单位：小时。超过过期时间的 relay log 会被 DM 删除。如果不设置则 DM 不会自动清理过期的 relay log。 |
| `remain-space` | 设置最小的可用磁盘空间。当磁盘可用空间小于这个值时，DM-worker 会尝试删除 relay log，默认值：15，单位：GB。 |

> **注意：**
>
> 仅在 `interval` 不为 0 且 `expires` 和 `remain-space` 两个配置项中至少有一个不为 0 的情况下 DM 的自动清理策略才会生效。

### 任务检查模块配置（checker 配置项）

| 配置项        | 说明                                    |
| ------------ | --------------------------------------- |
| `check-enable` | 是否开启任务状态检查。开启后 DM 会尝试自动恢复因错误而暂停的数据同步任务，默认值：true。 |
| `backoff-rollback` | 任务检查模块中，定时调整恢复等待时间的间隔，默认值："5m0s"。 |
| `backoff-max` | 任务检查模块中，检查出错误后等待自动恢复的最长时间间隔，默认值："5m0s"。 |

> **注意：**
>
> 用户只需要通过配置 `check-enable` 开启或者关闭任务状态检查功能。对于 `backoff-rollback` 和 `backoff-max` 一般情况下不需要修改，如果对该参数的作用没有深入的了解，不建议修改这两项参数。
