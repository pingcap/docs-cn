---
title: DM-worker 配置文件介绍
category: reference
---

# DM-worker 配置文件介绍

## 基础配置

在一般场景中，用户只需要使用基础配置即可完成 DM-worker 的部署。

### 配置文件示例

```toml
# Worker Configuration.

# log configuration
log-file = "dm-worker.log"

# dm-worker listen address
worker-addr = ":8262"

# represents a MySQL/MariaDB instance or a replication group
source-id = "mysql-replica-01"

# directory that used to store relay log
relay-dir = "./relay_log"

[from]
host = "127.0.0.1"
user = "root"
password = "Up8156jArvIPymkVC+5LxkAT6rek"
port = 3306
```

### 配置项说明

#### Global 配置

`log-file`：日志文件，如果不配置日志会输出到标准输出中。

`worker-addr`：DM-worker 服务的地址，可以省略 IP 信息，例如：":8262"。

`source-id`：标识一个 MySQL/MariaDB 实例或者 replication group。

`relay-dir`：存储 relay log 的目录，默认值为 "./relay_log"。

#### 数据库链接配置（from 配置项）

`host`：上游数据库的 host。

`port`：上游数据库的端口。

`user`：连接数据库使用的用户名。

`password`：连接数据库使用的密码。注意：需要使用 dmctl 加密后的密码。

注：以上配置为部署 DM-worker 的基础配置，一般情况下使用基础配置即可，更多配置项参考 [DM-worker 完整配置说明](/dev/reference/tools/data-migration/configure/dm-worker-configuration-file-full.md)。

## 完整配置

完整配置项参考 [DM-worker 完整配置说明](/dev/reference/tools/data-migration/configure/dm-worker-configuration-file-full.md)。
