---
title: DM-worker 配置文件介绍
category: reference
---

# DM-worker 配置文件介绍

## DM-worker 基础配置文件示例

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

# enable gtid in relay log unit
enable-gtid = false

# charset of DSN of source mysql/mariadb instance
# charset= ""

[from]
host = "127.0.0.1"
user = "root"
password = "Up8156jArvIPymkVC+5LxkAT6rek"
port = 3306

# relay log purge strategy
# [purge]
# interval = 3600
# expires = 24
# remain-space = 15

# task status checker
# [checker]
# check-enable = true
# backoff-rollback = 5m
# backoff-max = 5m
```

## 配置项说明

### Global 配置

`log-level`：日志等级，值可以为 "debug", "info", "warn", "error", "fatal"，默认值为 "info"。

`log-file`：日志文件，如果不配置日志会输出到标准输出中。

`worker-addr`：DM-worker 服务的地址，可以省略 IP 信息，例如：":8262"。

`server-id`：DM-worker 作为上游 MySQL/MariaDB slave 来获取 binlog 的 server id，该值在一个 replication group （包括 master 和 slave）中是唯一的。

`source-id`：标识一个 MySQL/MariaDB 实例或者 replication group。

`flavor`：上游数据库的类型，目前值可以为 "mysql" 或者 "mariadb"。

`relay-dir`：存储 relay log 的目录，默认值为 "./relay_log"。

`enable-gtid`：是否使用 GTID 方式从上游拉取 binlog，默认值为 false。

`charset`：连接上游拉 binlog 时使用的 charset。

### 数据库链接配置

`host`：上游数据库的 host。

`port`：上游数据库的端口。

`user`：连接数据库使用的用户名。

`password`：连接数据库使用的密码。注意：需要使用 dmctl 加密后的密码。
