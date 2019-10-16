---
title: DM-worker 完整配置说明
category: reference
---

# DM-worker 完整配置说明

## DM-worker 完整配置文件示例

```toml
# Worker Configuration.

# log configuration
log-level = "info"
log-file = "dm-worker.log"

# dm-worker listen address
worker-addr = ":8262"

# server id of slave for binlog replication
# each instance (master and slave) in replication group should have different server id
server-id = 101

# represents a MySQL/MariaDB instance or a replication group
source-id = "mysql-replica-01"

# flavor: mysql/mariadb
flavor = "mysql"

# directory that used to store relay log
relay-dir = "./relay_log"

relay-binlog-name = ""
relay-binlog-gtid = ""

# enable gtid in relay log unit
enable-gtid = false

[from]
host = "127.0.0.1"
user = "root"
password = "Up8156jArvIPymkVC+5LxkAT6rek"
port = 3306

# relay log purge strategy
[purge]
interval = 3600
expires = 24
remain-space = 15

# task status checker
[checker]
check-enable = true
backoff-rollback = 5m
backoff-max = 5m
```

## 配置项说明

### Global 配置

`log-level`：日志等级，值可以为 "debug", "info", "warn", "error", "fatal"，默认值为 "info"。一般情况下不需要配置，如果需要排查问题，可以将等级设置为 "debug"。

`log-file`：日志文件，如果不配置日志会输出到标准输出中。

`worker-addr`：DM-worker 服务的地址，可以省略 IP 信息，例如：":8262"。

`server-id`：DM-worker 作为上游 MySQL/MariaDB slave 来获取 binlog 的 server id，该值在一个 replication group （包括 master 和 slave）中是唯一的。一般情况下不需要配置，DM 会随机生成一个 server id，如果生成的 server id 与其他 slave 服务的 server id 冲突，则可以通过该配置项设置。

`source-id`：标识一个 MySQL/MariaDB 实例或者 replication group。

`flavor`：上游数据库的类型，目前值可以为 "mysql" 或者 "mariadb"。一般情况下不需要配置，DM 会自动判断上游数据库的类型，如果判断的不正确，则可以通过该配置项设置。

`relay-dir`：存储 relay log 的目录，默认值为 "./relay_log"。

`relay-binlog-name`：拉取上游 binlog 的起始文件名，例如 "mysql-bin.000002"，该配置在 `enable-gtid` 为 false 的情况下生效。一般情况下不需要配置，DM-worker 默认从最新位置开始拉取。

`relay-binlog-gtid`：拉取上游 binlog 的起始 GTID，例如 "e9a1fc22-ec08-11e9-b2ac-0242ac110003:1-7849"，该配置在 `enable-gtid` 为 true 的情况下生效。一般情况下不需要配置，DM-worker 默认从最新位置开始拉取。

`enable-gtid`：是否使用 GTID 方式从上游拉取 binlog，默认值为 false。一般情况下不需要配置，如果上游数据库需要做主从切换，则将该配置项设置为 true。

### 数据库链接配置（from 配置项）

`host`：上游数据库的 host。

`port`：上游数据库的端口。

`user`：连接数据库使用的用户名。

`password`：连接数据库使用的密码。注意：需要使用 dmctl 加密后的密码。

### relay log 清理策略配置（purge 配置项）

一般情况下不需要配置，如果 relay log 数据量较大，磁盘空间不足，则可以通过该配置项设置，避免 relay log 写满磁盘。

`interval`：检查 relay log 的时间间隔，默认值为 0（单位：秒）。如果不设置则 DM 不会自动清理过期的 relay log。

`expires`：relay log 的过期时间，默认值为 0（单位：小时），超过过期时间的 relay log 会被 DM 删除。如果不设置则 DM 不会自动清理过期的 relay log。

`remain-space`：磁盘最小可用空间大小，默认值为 0（单位：GB），当可用空间小于该值时，DM 会删除的 relay log。

> **注意：**
>
> 仅在 `interval` 不为 0 且 `expires` 和 `remain-space` 两个配置项中至少有一个不为 0 的情况下 DM 的自动清理策略才会生效。