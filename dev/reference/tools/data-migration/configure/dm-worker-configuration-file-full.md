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