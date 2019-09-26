---
title: 使用 DM binary 部署 DM 集群
category: how-to
---

# 使用 DM binary 部署 DM 集群

本文将介绍如何使用 DM binary 快速部署 DM 集群。

## 准备工作

下载官方 binary，链接地址：[DM 下载](/dev/reference/tools/download.md#tidb-dm-data-migration)。

下载的文件中包括子目录 bin 和 conf。bin 目录下包含 dm-master、dm-worker、dmctl 以及 Mydumper 的二进制文件。conf 目录下有相关的示例配置文件。

## 使用样例

假设在两台服务器上部署 MySQL，在一台服务器上部署 TiDB（mocktikv 模式），另外在三台服务器上部署两个 DM-worker 实例和一个 DM-master 实例。各个节点的信息如下：

| 实例        | 服务器地址   |
| :---------- | :----------- |
| MySQL1     | 192.168.0.1 |
| MySQL2     | 192.168.0.2 |
| TiDB       | 192.168.0.3 |
| DM-master  | 192.168.0.4 |
| DM-worker1 | 192.168.0.5 |
| DM-worker2 | 192.168.0.6 |

MySQL1 和 MySQL2 中需要开启 binlog。DM-worker1 负责同步 MySQL1 的数据，DM-worker2 负责同步 MySQL2 的数据。下面以此为例，说明如何部署 DM。

### DM-worker 的部署

DM-worker 需要连接上游 MySQL，且为了安全，强制用户配置加密后的密码。首先使用 dmctl 对 MySQL 的密码进行加密，以密码为 "123456" 为例：

{{< copyable "shell-regular" >}}

```bash
./bin/dmctl --encrypt "123456"
```

```
fCxfQ9XKCezSzuCD0Wf5dUD+LsKegSg=
```

记录该加密后的值，用于下面部署 DM-worker 时的配置。

DM-worker 提供命令行参数和配置文件两种配置方式。

查看 DM-worker 的命令行参数说明：

{{< copyable "shell-regular" >}}

```bash
./bin/dm-worker --help
```

```
Usage of worker:
  -L string
        日志等级，值可以为 "debug"，"info"，"warn"，"error" 或者 "fatal"（默认值："info"）
  -V    输出版本信息
  -checker-backoff-max duration
        任务检查模块中，检查出错误后等待自动恢复的最长时间间隔（默认值："5m0s"，一般情况下不需要修改。如果对该参数的作用没有深入的了解，不建议修改该参数）
  -checker-backoff-rollback duration
        任务检查模块中，定时调整恢复等待时间的间隔（默认值："5m0s"，一般情况下不需要修改，如果对该参数的作用没有深入的了解，不建议修改该参数）
  -checker-check-enable
        是否开启任务状态检查。开启后 DM 会尝试自动恢复因错误而暂停的数据同步任务（默认值：true）
  -config string
        配置文件的路径
  -log-file string
        日志文件的路径
  -print-sample-config
        打印示例配置
  -purge-expires int
        relay log 的过期时间。DM-worker 会尝试自动删除最后修改时间超过了过期时间的 relay log（单位：小时）
  -purge-interval int
        定期检查 relay log 是否过期的间隔时间（默认值：3600）（单位：秒）
  -purge-remain-space int
        设置最小的可用磁盘空间。当磁盘可用空间小于这个值时，DM-worker 会尝试删除 relay log（默认值：15）（单位：GB）
  -relay-dir string
        存储 relay log 的路径（默认值："./relay_log"）
  -worker-addr string
        DM-worker 的地址
```

DM-worker 的配置文件：

```toml
# Worker Configuration.

# 日志配置
log-level = "info"
log-file = "dm-worker.log"

# dm-worker 的地址
worker-addr = ":8262"

# 作为 MySQL slave 的 server ID，用于获取 MySQL 的 binlog
# 在一个 replication group 中，每个实例（master 和 slave）都应该有唯一的 server ID
server-id = 101

# 用于标识一个 replication group 或者 MySQL/MariaDB 实例
source-id = "mysql-replica-01"

# 上游实例类型，值可为 "mysql" 或者 "mariadb"
flavor = "mysql"

# 存储 relay log 的路径
relay-dir = "./relay_log"

# 存储 dm-worker 元信息的路径
meta-dir = "dm_worker_meta"

# relay log 处理单元是否开启 gtid
enable-gtid = false

# 连接 MySQL/Mariadb 的 DSN 中的 charset 配置
# charset= ""

# MySQL 的连接地址
[from]
host = "192.168.0.1"
user = "root"
password = "fCxfQ9XKCezSzuCD0Wf5dUD+LsKegSg="
port = 3306

# relay log 的删除规则
# [purge]
# interval = 3600
# expires = 24
# remain-space = 15

# 任务状态检查相关配置
# [checker]
# check-enable = true
# backoff-rollback = 5m
# backoff-max = 5m
```

推荐统一使用配置文件，把以上配置内容写入到 `conf/dm-worker1.toml` 中，在终端中使用下面的命令运行 DM-worker：

{{< copyable "shell-regular" >}}

```bash
bin/dm-worker -config conf/dm-worker1.toml
```

对于 DM-worker2，修改配置文件中的 `source-id` 为 `mysql-replica-02`，并将 `from` 配置部分修改为 MySQL2 的地址即可。

### DM-master 的部署

DM-master 提供命令行参数和配置文件两种配置方式。

DM-master 的命令行参数说明：

```bash
./bin/dm-master --help
```

```
Usage of dm-master:
  -L string
        日志等级，值可以为 "debug"，"info"，"warn"，"error" 或者 "fatal"（默认值为 "info"）
  -V    输出版本信息
  -config string
        配置文件的路径
  -log-file string
        日志文件的路径
  -master-addr string
        DM-master 的地址
  -print-sample-config
        打印出 dm-master 的示例配置
```

DM-master 的配置文件：

```toml
# Master Configuration.

# rpc 相关配置
rpc-rate-limit = 10.0
rpc-rate-burst = 40

# 日志配置
log-level = "info"
log-file = "dm-master.log"

# dm-master 监听地址
master-addr = ":8261"

# replication group <-> DM-Worker 的配置
[[deploy]]
# 对应 DM-worker1 配置文件中的 source-id
source-id = "mysql-replica-01"
# DM-worker1 的服务地址
dm-worker = "192.168.0.5:8262"

[[deploy]]
# 对应 DM-worker2 配置文件中的 source-id
source-id = "mysql-replica-02"
# DM-worker2 的服务地址
dm-worker = "192.168.0.6:8262"
```

推荐统一使用配置文件，把以上配置内容写入到 `conf/dm-master.toml` 中，在终端中使用下面的命令运行 DM-master：

{{< copyable "shell-regular" >}}

```bash
bin/dm-master -config conf/dm-master.toml
```

这样，DM 集群就部署成功了。下面创建简单的数据同步任务来使用 DM 集群。

### 创建数据同步任务

假设在 MySQL1 和 MySQL2 实例中有若干个分表，这些分表的结构相同，所在库的名称都以 "sharding" 开头，表名称都以 "t" 开头，并且主键或唯一键不存在冲突。现在需要把这些分表同步到 TiDB 中的 `db_target.t_target` 表中。

首先创建任务的配置文件：

{{< copyable "" >}}

```yaml
---
name: test
task-mode: all
is-sharding: true
meta-schema: "dm_meta"
remove-meta: false
enable-heartbeat: true
timezone: "Asia/Shanghai"

target-database:
  host: "192.168.0.3"
  port: 4000
  user: "root"
  password: "" # 如果密码不为空，也需要配置 dmctl 加密后的密码

mysql-instances:
  - source-id: "mysql-replica-01"
    black-white-list:  "instance"
    route-rules: ["sharding-route-rules-table", "sharding-route-rules-schema"]
    mydumper-config-name: "global"
    loader-config-name: "global"
    syncer-config-name: "global"

  - source-id: "mysql-replica-02"
    black-white-list:  "instance"
    route-rules: ["sharding-route-rules-table", "sharding-route-rules-schema"]
    mydumper-config-name: "global"
    loader-config-name: "global"
    syncer-config-name: "global"

black-white-list:
  instance:
    do-dbs: ["~^sharding[\\d]+"]
    do-tables:
    -  db-name: "~^sharding[\\d]+"
       tbl-name: "~^t[\\d]+"

routes:
  sharding-route-rules-table:
    schema-pattern: sharding*
    table-pattern: t*
    target-schema: db_target
    target-table: t_target

  sharding-route-rules-schema:
    schema-pattern: sharding*
    target-schema: db_target

mydumpers:
  global:
    mydumper-path: "./bin/mydumper"
    threads: 4
    chunk-filesize: 64
    skip-tz-utc: true
    extra-args: "--regex '^sharding.*'"

loaders:
  global:
    pool-size: 16
    dir: "./dumped_data"

syncers:
  global:
    worker-count: 16
    batch: 100

```

将以上配置内容写入到 `conf/task.yaml` 文件中，并使用 dmctl 创建任务：

{{< copyable "shell-regular" >}}

```bash
bin/dmctl -master-addr 192.168.0.4:8261
```

```
Welcome to dmctl
Release Version: v1.0.0-69-g5134ad1
Git Commit Hash: 5134ad19fbf6c57da0c7af548f5ca2a890bddbe4
Git Branch: master
UTC Build Time: 2019-04-29 09:36:42
Go Version: go version go1.12 linux/amd64
»
```

{{< copyable "" >}}

```bash
» start-task conf/task.yaml
```

```
{
    "result": true,
    "msg": "",
    "workers": [
        {
            "result": true,
            "worker": "192.168.0.5:8262",
            "msg": ""
        },
        {
            "result": true,
            "worker": "192.168.0.6:8262",
            "msg": ""
        }
    ]
}
```

这样就成功创建了一个将 MySQL1 和 MySQL2 实例中的分表数据同步到 TiDB 的任务。
