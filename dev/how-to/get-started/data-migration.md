---
title: TiDB Data Migration 教程
category: how-to
---

# TiDB Data Migration 教程

TiDB Data Migration (DM) 是一体化的数据同步任务管理平台，支持将大量、复杂的生产环境中的数据从 MySQL 或 MariaDB 迁移到 TiDB。

DM 功能如下：

- 数据迁移
    - 支持导出与导入源数据库的初始全量数据，并在数据迁移过程中读取、应用来自源数据库存储的 binlog，从而保持数据的同步。
    - 通过合并上游的多个 MySQL 或 MariaDB 实例或集群的表，DM 能迁移生产环境中的分库分表。
- 将 TiDB 作为 MySQL 或 MariaDB 的从库时，DM 能持续提高数据库水平扩展的能力，或在无需 ETL 作业的情况下，在 TiDB 上进行数据实时分析。

本教程主要介绍如何使用 DM 迁移上游多个 MySQL 实例的一个分片表。包括两种场景：

- 合并若干个互不冲突的表或分片，即这些表或分片的表结构并不会造成唯一键的冲突；
- 合并唯一键存在冲突的表。

本教程假设目前使用的是一台新的、纯净版 CentOS 7 实例，你能（使用 VMware、VirtualBox 及其他工具）在本地虚拟化或在供应商提供的平台上部署一台小型的云虚拟主机。因为需要运行多个服务，建议内存最好在 1 GB 以上。

> **警告：**
>
> 本教程中 TiDB 的部署方法并**不适用**于生产或开发环境。

## Data Migration 架构

![TiDB Data Migration 架构](/media/dm-architecture.png)

TiDB Data Migration 平台由 3 部分组成：DM-master、DM-worker 和 dmctl。

* DM-master 负责管理和调度数据同步任务的操作。
* DM-worker 负责执行特定的数据同步任务。
* dmctl 是一个命令行工具，用于控制 DM 集群。

`.yaml` 文件中定义了各个数据同步任务，dmctl 读取这些数据，并将这些数据提交至 DM-master。DM-master 再将关于给定任务的相应职责告知每个 DM-worker 实例。

详情参见 [Data Migration 简介](/reference/tools/data-migration/overview.md)。

## 安装

本部分介绍如何部署 3 个 MySQL Server 实例及 `pd-server`、`tikv-server` 和 `tidb-server` 实例各 1 个，以及如何启动 1 个 DM-master 和 3 个 DM-worker 实例。

1. 安装 MySQL 5.7，下载或提取 TiDB 安装包：

    ```bash
    sudo yum install -y http://repo.mysql.com/yum/mysql-5.7-community/el/7/x86_64/mysql57-community-release-el7-10.noarch.rpm
    sudo yum install -y mysql-community-server
    curl http://download.pingcap.org/tidb-v3.0-linux-amd64.tar.gz | tar xzf -
    curl http://download.pingcap.org/dm-latest-linux-amd64.tar.gz | tar xzf -
    curl -L https://github.com/pingcap/docs/raw/master/dev/how-to/get-started/dm-cnf/dm-cnf.tgz | tar xvzf -
    ```

2. 创建目录和符号链接：

    ```bash
    mkdir -p bin data logs
    ln -sf -t bin/ "$HOME"/*/bin/*
    [[ :$PATH: = *:$HOME/bin:* ]] || echo 'export PATH=$PATH:$HOME/bin' >> ~/.bash_profile && . ~/.bash_profile
    ```

3. 安装 3 个 MySQL Server 实例的配置：

    ```bash
    tee -a "$HOME/.my.cnf" <<EoCNF
    [server]
    socket=mysql.sock
    pid-file=mysql.pid
    log-error=mysql.err
    log-bin
    auto-increment-increment=5
    [server1]
    datadir=$HOME/data/mysql1
    server-id=1
    port=3307
    auto-increment-offset=1
    [server2]
    datadir=$HOME/data/mysql2
    server-id=2
    port=3308
    auto-increment-offset=2
    [server3]
    datadir=$HOME/data/mysql3
    server-id=3
    port=3309
    auto-increment-offset=3
    EoCNF
    ```

4. 初始化并启动这些 MySQL 实例：

    ```bash
    for i in 1 2 3
    do
        echo  "mysql$i"
        mysqld --defaults-group-suffix="$i" --initialize-insecure
        mysqld --defaults-group-suffix="$i" &
    done
    ```

5. （可选）执行 `jobs` 和/或 `pgrep -a mysqld` 以确保 MySQL Server 实例都在运行状态。

    ```
    $ jobs
    [1]   Running                 mysqld --defaults-group-suffix="$i" &
    [2]-  Running                 mysqld --defaults-group-suffix="$i" &
    [3]+  Running                 mysqld --defaults-group-suffix="$i" &
    $ pgrep -a mysqld
    17672 mysqld --defaults-group-suffix=1
    17727 mysqld --defaults-group-suffix=2
    17782 mysqld --defaults-group-suffix=3
    ```

## 无重叠分片

本示例场景由 3 个分片组成，这些分片表结构相同，但自增主键并不重叠。

在 `.my.cnf` 文件中设置 `auto-increment-increment=5` 和 `auto-increment-offset` 可以实现这种情况。将 `auto-increment-increment` 设置为 5，则这些实例的自增 ID 以 5 为单位递增；每个实例的 `auto-increment-offset` 都设置得不同，则这些实例的偏移为 0 到开始计数的值。例如，若一个实例的 `auto-increment-increment` 为 5，`auto-increment-offset` 为 2，则会生成自增 ID 序列 {2,7,12,17,22,…}。

1. 对于这 3 个 MySQL Server 实例，每个实例都分别创建数据库和表：

    ```bash
    for i in 1 2 3
    do
        mysql -h 127.0.0.1 -P "$((3306+i))" -u root <<EoSQL
            create database dmtest1;
            create table dmtest1.t1 (id bigint unsigned not null auto_increment primary key, c char(32), port int);
    EoSQL
    done
    ```

2. 在每个 MySQL 实例中插入几百行数据：

    ```bash
    for i in 1 2 3; do
        mysql -h 127.0.0.1 -P "$((3306+i))" -u root dmtest1 <<EoSQL
            insert into t1 values (),(),(),(),(),(),(),();
            insert into t1 (id) select null from t1;
            insert into t1 (id) select null from t1;
            insert into t1 (id) select null from t1;
            insert into t1 (id) select null from t1;
            insert into t1 (id) select null from t1;
            update t1 set c=md5(id), port=@@port;
    EoSQL
    done
    ```

3. 查询上一步写入的所有行并排序，以确认写入数据是正确的：

    ```bash
    for i in 1 2 3; do
        mysql -N -h 127.0.0.1 -P "$((3306+i))" -u root -e 'select * from dmtest1.t1'
    done | sort -n
    ```

注意返回的列表左侧是一列递增的、无重叠的 ID，右侧的端口编号显示这些数据插入到哪些实例以及从哪些实例中查询：

```
...
1841    e8dfff4676a47048d6f0c4ef899593dd        3307
1842    57c0531e13f40b91b3b0f1a30b529a1d        3308
1843    4888241374e8c62ddd9b4c3cfd091f96        3309
1846    f45a1078feb35de77d26b3f7a52ef502        3307
1847    82cadb0649a3af4968404c9f6031b233        3308
1848    7385db9a3f11415bc0e9e2625fae3734        3309
1851    ff1418e8cc993fe8abcfe3ce2003e5c5        3307
1852    eb1e78328c46506b46a4ac4a1e378b91        3308
1853    7503cfacd12053d309b6bed5c89de212        3309
1856    3c947bc2f7ff007b86a9428b74654de5        3307
1857    a3545bd79d31f9a72d3a78690adf73fc        3308
1858    d7fd118e6f226a71b5f1ffe10efd0a78        3309
```

### 启动 DM-master 和 DM-worker

本小节介绍如何使用 DM 将来自不同的 MySQL 实例的数据合并到 TiDB 的一张表里。

配置文件包 `dm-cnf.tgz` 包含：

- TiDB 集群组件和 DM 组件的配置
- 本教程后文介绍的 2 个 DM 任务的配置

1. 启动单个 `tidb-server` 实例、每个 MySQL Server 实例 （总共 3 个实例）的 DM-worker 进程和一个 DM-master 进程：

    ```bash
    tidb-server --log-file=logs/tidb-server.log &
    for i in 1 2 3; do dm-worker --config=dm-cnf/dm-worker$i.toml & done
    dm-master --config=dm-cnf/dm-master.toml &
    ```

2. 执行 `jobs` 和/或 `ps -a`，确保这些进程都正在运行：

    ```
    $ jobs
    [1]   Running                 mysqld --defaults-group-suffix="$i" &
    [2]   Running                 mysqld --defaults-group-suffix="$i" &
    [3]   Running                 mysqld --defaults-group-suffix="$i" &
    [4]   Running                 tidb-server --log-file=logs/tidb-server.log &
    [5]   Running                 dm-worker --config=dm-cnf/dm-worker$i.toml &
    [6]   Running                 dm-worker --config=dm-cnf/dm-worker$i.toml &
    [7]-  Running                 dm-worker --config=dm-cnf/dm-worker$i.toml &
    [8]+  Running                 dm-master --config=dm-cnf/dm-master.toml &
    $ ps -a
       PID TTY          TIME CMD
     17317 pts/0    00:00:00 screen
     17672 pts/1    00:00:04 mysqld
     17727 pts/1    00:00:04 mysqld
     17782 pts/1    00:00:04 mysqld
     18586 pts/1    00:00:02 tidb-server
     18587 pts/1    00:00:00 dm-worker
     18588 pts/1    00:00:00 dm-worker
     18589 pts/1    00:00:00 dm-worker
     18590 pts/1    00:00:00 dm-master
     18892 pts/1    00:00:00 ps
    ```

每个上游的 MySQL Server 实例对应一个单独的 DM-worker 实例，每个 DM-worker 实例都有各自的配置文件。这些文件内容包括：

- 连接到上游 MySQL Server 的细节信息
- relay log（上游服务器的 binlog）的存储路径
- mydumper 的输出

各个 DM-worker 通过不同的端口监听（由 `worker-addr` 定义）。

以下为 `dm-worker1.toml` 的示例：

```toml
# DM-worker 配置

server-id = 1
source-id = "mysql1"
flavor = "mysql"
worker-addr = ":8262"
log-file = "logs/worker1.log"
relay-dir = "data/relay1"
meta-dir = "data/meta1"
dir = "data/dump1"

[from]
host = "127.0.0.1"
user = "root"
password = ""
port = 3307
```

- 如果从 MySQL Server、Percona Server、Percona XtraDB Cluster、Amazon Aurora 或 RDS 迁移数据，则 `flavor` 配置项应设为 "mysql"（默认值，支持 5.5 < MySQL 版本 < 8.0）。
- 如果从 MariaDB Server 或 MariaDB (Galera) Cluster 迁移数据，则设置 `flavor = "mariadb"`（仅支持 10.1.2 以上 MariaDB 版本）。

YAML 文件定义 task。以下为一个 `dmtask1.yaml` 文件示例：

```yaml
name: dmtask1
task-mode: all
is-sharding: true
enable-heartbeat: true
ignore-checking-items: ["auto_increment_ID"]

target-database:
  host: "127.0.0.1"
  port: 4000
  user: "root"
  password: ""

mysql-instances:
  - source-id: "mysql1"
    server-id: 1
    black-white-list: "dmtest1"
    loader-config-name: "loader1"
  - source-id: "mysql2"
    server-id: 2
    black-white-list: "dmtest1"
    loader-config-name: "loader2"
  - source-id: "mysql3"
    server-id: 3
    black-white-list: "dmtest1"
    loader-config-name: "loader3"

black-white-list:
  dmtest1:
    do-dbs: ["dmtest1"]

loaders:
  loader1:
    dir: "data/dump1"
  loader2:
    dir: "data/dump2"
  loader3:
    dir: "data/dump3"
```

以上文件包含一些全局配置项和几组定义各种行为的配置项。

* `task-mode: all`：DM 导入上游实例的全量备份，并使用上游 MySQL Server 的 binlog 进行增量同步。
  
    * 此外，可将 `task-mode` 设置为 `full` 或 `incremental` 以分别进行全量备份或增量同步。

* `is-sharding: true`：多个 DM-worker 实例在一个 task 上工作，这些实例将上游的若干分片合并到一个下游的表中。

* `ignore-checking-items: ["auto_increment_ID"]`：关闭 DM 对上游实例中潜在的自增 ID 冲突的检测。DM 能检测出上游表结构相同、并包含自增列的分片间潜在的列值冲突。通过配置 `auto-increment-increment` 和 `auto-increment-offset` 可使每个 MySQL Server 的 ID 都不重叠，从而避免不同表之间冲突的产生。因此，可以让 DM 关闭对自增 ID 冲突的检测。

* `black-white-list`：将一个任务限制在数据库 `dmtest` 中。

* `loaders`：定义由各个 DM-worker 实例执行的每个 mydumper 实例的输出地址。

`dmctl` 是控制 DM 集群的命令行工具，用于启动任务、查询任务状态。执行 `dmctl -master-addr :8261` 获取如下交互提示，从而启动该工具：

```
$ dmctl -master-addr :8261
Welcome to dmctl
Release Version: v1.0.0-alpha-69-g5134ad1
Git Commit Hash: 5134ad19fbf6c57da0c7af548f5ca2a890bddbe4
Git Branch: master
UTC Build Time: 2019-04-29 09:36:42
Go Version: go version go1.12 linux/amd64

»
```

执行 `start-task dm-cnf/dmtask1.yaml` 启动 `dmtask1`：

```
» start-task dm-cnf/dmtask1.yaml
{
    "result": true,
    "msg": "",
    "workers": [
        {
            "result": true,
            "worker": "127.0.0.1:8262",
            "msg": ""
        },
        {
            "result": true,
            "worker": "127.0.0.1:8263",
            "msg": ""
        },
        {
            "result": true,
            "worker": "127.0.0.1:8264",
            "msg": ""
        }
    ]
}
```

启动该任务意味着启动任务配置文件中定义的行为，包括执行 mydumper 和 loader 实例，加载初次 dump 的数据后，将 DM-worker 作为同步任务的 slave 连接到上游的 MySQL Server。

所有的行数据都被迁移到 TiDB Server：

```bash
mysql -h 127.0.0.1 -P 4000 -u root -e 'select * from t1' dmtest1 | tail
```

输出结果：

```
...
1843    4888241374e8c62ddd9b4c3cfd091f96        3309
1846    f45a1078feb35de77d26b3f7a52ef502        3307
1847    82cadb0649a3af4968404c9f6031b233        3308
1848    7385db9a3f11415bc0e9e2625fae3734        3309
1851    ff1418e8cc993fe8abcfe3ce2003e5c5        3307
1852    eb1e78328c46506b46a4ac4a1e378b91        3308
1853    7503cfacd12053d309b6bed5c89de212        3309
1856    3c947bc2f7ff007b86a9428b74654de5        3307
1857    a3545bd79d31f9a72d3a78690adf73fc        3308
1858    d7fd118e6f226a71b5f1ffe10efd0a78        3309
```

现在 DM 正作为每个 MySQL Server 的 slave，读取 MySQL Server 的 binlog，将更新的数据实时同步到下游的 TiDB Server：

```bash
for i in 1 2 3
do
     mysql -h 127.0.0.1 -P "$((3306+i))" -u root -e 'select host, command, state from information_schema.processlist where command="Binlog Dump"'
done
```

输出结果：

```
+-----------------+-------------+---------------------------------------------------------------+
| host            | command     | state                                                         |
+-----------------+-------------+---------------------------------------------------------------+
| localhost:42168 | Binlog Dump | Master has sent all binlog to slave; waiting for more updates |
+-----------------+-------------+---------------------------------------------------------------+
+-----------------+-------------+---------------------------------------------------------------+
| host            | command     | state                                                         |
+-----------------+-------------+---------------------------------------------------------------+
| localhost:42922 | Binlog Dump | Master has sent all binlog to slave; waiting for more updates |
+-----------------+-------------+---------------------------------------------------------------+
+-----------------+-------------+---------------------------------------------------------------+
| host            | command     | state                                                         |
+-----------------+-------------+---------------------------------------------------------------+
| localhost:56798 | Binlog Dump | Master has sent all binlog to slave; waiting for more updates |
+-----------------+-------------+---------------------------------------------------------------+
```

向上游 MySQL Server 插入几行数据，更新 MySQL 中的这些行，并再次查询这些行：

```bash
for i in 1 2 3; do
    mysql -N -h 127.0.0.1 -P "$((3306+i))" -u root -e 'insert into t1 (id) select null from t1' dmtest1
done
mysql -h 127.0.0.1 -P 4000 -u root -e 'select * from t1' dmtest1 | tail
```

输出结果：

```
6313    NULL    NULL
6316    NULL    NULL
6317    NULL    NULL
6318    NULL    NULL
6321    NULL    NULL
6322    NULL    NULL
6323    NULL    NULL
6326    NULL    NULL
6327    NULL    NULL
6328    NULL    NULL
```

更新这些行，则可见更新的数据已同步到 TiDB 中：

```bash
for i in 1 2 3; do
    mysql -N -h 127.0.0.1 -P "$((3306+i))" -u root -e 'update t1 set c=md5(id), port=@@port' dmtest1
done | sort -n
mysql -h 127.0.0.1 -P 4000 -u root -e 'select * from t1' dmtest1 | tail
```

输出结果：

```
6313    2118d8a1b7004ed5baf5347a4f99f502        3309
6316    6107d91fc9a0b04bc044aa7d8c1443bd        3307
6317    0e9b734aa25ca8096cb7b56dc0dd8929        3308
6318    b0eb9a95e8b085e4025eae2f0d76a6a6        3309
6321    7cb36e23529e4de4c41460940cc85e6e        3307
6322    fe1f9c70bdf347497e1a01b6c486bdb9        3308
6323    14eac0d254a6ccaf9b67584c7830a5c0        3309
6326    17b65afe58c49edc1bdd812c554ee3bb        3307
6327    c54bc2ded4480856dc9f39bdcf35a3e7        3308
6328    b294504229c668e750dfcc4ea9617f0a        3309
```

只要 DM-master 和 DM-worker 运行 `dmtest1` 任务，下游的 TiDB Server 将持续和上游的 MySQL Server 实例保持同步的状态。

## 重叠分片

本示例场景由 3 个分片组成，这些分片的自增主键存在冲突。

1. 创建一个新的数据库和 MySQL 各实例中的一些表：

    ```bash
    for i in 1 2 3
    do
        mysql -h 127.0.0.1 -P "$((3306+i))" -u root <<EoSQL
            create database dmtest2;
            create table dmtest2.t1 (id bigint unsigned not null auto_increment primary key, c char(32), port int);
    EoSQL
    done
    ```

2. 向每个 MySQL 实例插入几百行数据。通过设置 `auto_increment_increment=1` and `auto_increment_offset=1` 确保这 3 个 MySQL Server 都分配相同的自增 ID：

    ```bash
    for i in 1 2 3; do
        mysql -h 127.0.0.1 -P "$((3306+i))" -u root dmtest2 <<EoSQL
            set auto_increment_increment=1, auto_increment_offset=1;
            insert into t1 values (),(),(),(),(),(),(),();
            insert into t1 (id) select null from t1;
            insert into t1 (id) select null from t1;
            insert into t1 (id) select null from t1;
            insert into t1 (id) select null from t1;
            insert into t1 (id) select null from t1;
            update t1 set c=md5(id), port=@@port;
    EoSQL
    done
    ```

3. 在 MySQL 实例中查询这些行，确保插入的数据无误：

    ```bash
    for i in 1 2 3; do
        mysql -N -h 127.0.0.1 -P "$((3306+i))" -u root -e 'select * from t1' dmtest2
    done | sort -n
    ```

4. 在返回的结果中，可以发现同一个自增 ID（最左侧一栏）在上游不同的实例（由最右侧一栏的端口号区分）中多次出现：

    ```
    ...
    370     d709f38ef758b5066ef31b18039b8ce5        3307
    370     d709f38ef758b5066ef31b18039b8ce5        3308
    370     d709f38ef758b5066ef31b18039b8ce5        3309
    371     41f1f19176d383480afa65d325c06ed0        3307
    371     41f1f19176d383480afa65d325c06ed0        3308
    371     41f1f19176d383480afa65d325c06ed0        3309
    372     24b16fede9a67c9251d3e7c7161c83ac        3307
    372     24b16fede9a67c9251d3e7c7161c83ac        3308
    372     24b16fede9a67c9251d3e7c7161c83ac        3309
    ```

如果要把这些行原封不动地迁移到下游 TiDB 实例中的一张表中，将产生主键自增值冲突，导致重复的 key error 报错。可以使用 DM 的 "column mappings" 功能中的 "partition id" 表达式转化自增值，以避免自增值冲突。

以下是 `dmtask2.yaml`：

```yaml
name: dmtask2
task-mode: all
is-sharding: true
enable-heartbeat: true

target-database:
  host: "127.0.0.1"
  port: 4000
  user: "root"
  password: ""

# column-mappings 部分是关于如何用 DM 整合来自上游 3 个实例的数据。
column-mappings:
  mysql1:
    schema-pattern: "dmtest2"
    table-pattern: "t1"
    expression: "partition id"
    arguments: ["1", "", ""]
    source-column: "id"
    target-column: "id"
  mysql2:
    schema-pattern: "dmtest2"
    table-pattern: "t1"
    expression: "partition id"
    arguments: ["2", "", ""]
    source-column: "id"
    target-column: "id"
  mysql3:
    schema-pattern: "dmtest2"
    table-pattern: "t1"
    expression: "partition id"
    arguments: ["3", "", ""]
    source-column: "id"
    target-column: "id"

mysql-instances:
  - source-id: "mysql1"
    server-id: 1
    black-white-list: "dmtest2"
    column-mapping-rules: ["mysql1"]
    loader-config-name: "loader1"
  - source-id: "mysql2"
    server-id: 2
    black-white-list: "dmtest2"
    column-mapping-rules: ["mysql2"]
    loader-config-name: "loader2"
  - source-id: "mysql3"
    server-id: 3
    black-white-list: "dmtest2"
    column-mapping-rules: ["mysql3"]
    loader-config-name: "loader3"

black-white-list:
  dmtest2:
    do-dbs: ["dmtest2"]

loaders:
  loader1:
    dir: "data/dump1"
  loader2:
    dir: "data/dump2"
  loader3:
    dir: "data/dump3"
```

* `ignore-checking-items: ["auto_increment_ID"]` 将不再使用，因为上游的自增 ID 存在冲突。

* `column-mappings` 部分指引 DM 如何进行 shard merge 操作。
  
    * 只有一个上游表结构和表，因此 `schema-pattern` 和 `table-pattern` 事实上是字符串。

        * 如果要将多个表结构和/或表合并到下游的一个表中，可以使用通配符。
  
    * `partition id` 表达式有一个对应的 `arguments` 部分，该部分控制将上游 ID 转换成下游 TiDB 集群中使用的 ID 的算法。
  
    * `source_column` 和 `target_column` 的含义不言自明，需要注意的是，这二者能将上游插入的数据合并到下游结构不同的表中，例如，需要保留原始值时，可以这样操作。
  
    * `mysql-instances` 中的每一项都有不同的列映射，因为不同的 `partition id` 算法需要不同的参数。

启动 `dmtask2`：

```bash
dmctl -master-addr :8261 <<<"start-task dm-cnf/dmtask2.yaml"
```

输出结果：

```
Welcome to dmctl
Release Version: v1.0.0-alpha-76-g9fa6918
Git Commit Hash: 9fa6918c4b698e742a9893fa22235ee6ffcfa3b1
Git Branch: master
UTC Build Time: 2019-05-14 06:17:31
Go Version: go version go1.12 linux/amd64

{
    "result": true,
    "msg": "",
    "workers": [
        {
            "result": true,
            "worker": "127.0.0.1:8262",
            "msg": ""
        },
        {
            "result": true,
            "worker": "127.0.0.1:8263",
            "msg": ""
        },
        {
            "result": true,
            "worker": "127.0.0.1:8264",
            "msg": ""
        }
    ]
}
```

数据导入到下游 TiDB 实例后：

```bash
mysql -h 127.0.0.1 -P 4000 -u root -e 'select * from t1' dmtest2 | tail
```

输出结果：

```
1729382256910270827     00411460f7c92d2124a67ea0f4cb5f85        3309
1729382256910270828     bac9162b47c56fc8a4d2a519803d51b3        3309
1729382256910270829     9be40cee5b0eee1462c82c6964087ff9        3309
1729382256910270830     5ef698cd9fe650923ea331c15af3b160        3309
1729382256910270831     05049e90fa4f5039a8cadc6acbb4b2cc        3309
1729382256910270832     cf004fdc76fa1a4f25f62e0eb5261ca3        3309
1729382256910270833     0c74b7f78409a4022a2c4c5a5ca3ee19        3309
1729382256910270834     d709f38ef758b5066ef31b18039b8ce5        3309
1729382256910270835     41f1f19176d383480afa65d325c06ed0        3309
1729382256910270836     24b16fede9a67c9251d3e7c7161c83ac        3309
```

DM 使用一种算法将上游 MySQL 实例分配的 ID 进行位移，以生成下游 TiDB 实例的唯一 ID。在测试中，partition ID 仅由 "instance ID" 组成，因为上游 MySQL Server 中 schema 和表名是相同的。我们将 partition ID 表达式参数中的 "schema ID" 和 "table ID" 留空：

```bash
grep arguments dm-cnf/dmtask2.yaml
```

输出结果：

```
    arguments: ["1", "", ""]
    arguments: ["2", "", ""]
    arguments: ["3", "", ""]
```

上游 MySQL Server 分配的最后一个自增 ID 是 372。数据迁移到 TiDB server 后，转换后的自增 ID 最大值来自 instance 3（对应从右向左第一列的 3309 端口）。中间一列最后一行的值与 MySQL 实例中自增 ID 372 所在行的值相同。这个算法为来自上游的自增 ID 分配 64 位整数的 44 位，这意味着 partition ID 列映射方案的默认实现无法处理大于 2^44（大约 17.5 万亿）的值。1 位为符号的保留位，4 位为 instance ID，7 位为 schema ID，8 位为 table ID（44 + 1 + 4 + 7 + 8 = 64 位）。

在此，可为本示例复现算法，以自增 ID 372、instance ID 为 3 为例：

```bash
id=372 instance_id=3 schema_id=0 table_id=0
echo $(( instance_id << (64-1-4) | schema_id << (64-1-4-7) | table_id << 44 | id ))
```

输出结果：

```
1729382256910270836
```

因为只有 44 位对应原始的自增值，所以可以舍弃其他位，从而将转换后的值转换回原来的值：

```bash
echo $(( 1729382256910270836 & (1<<45)-1 ))
```

输出结果：

```
372
```

可使用 SQL 查询中的表达式查看转换后的 ID 和原来的 ID：

```bash
mysql -h 127.0.0.1 -P 4000 -u root -e 'select id, id&(1<<45)-1 as orig_id, c, port from t1 order by orig_id' dmtest2 | tail
```

输出结果：

```
576460752303423857      369     0c74b7f78409a4022a2c4c5a5ca3ee19        3307
576460752303423858      370     d709f38ef758b5066ef31b18039b8ce5        3307
1152921504606847346     370     d709f38ef758b5066ef31b18039b8ce5        3308
1729382256910270834     370     d709f38ef758b5066ef31b18039b8ce5        3309
576460752303423859      371     41f1f19176d383480afa65d325c06ed0        3307
1729382256910270835     371     41f1f19176d383480afa65d325c06ed0        3309
1152921504606847347     371     41f1f19176d383480afa65d325c06ed0        3308
576460752303423860      372     24b16fede9a67c9251d3e7c7161c83ac        3307
1729382256910270836     372     24b16fede9a67c9251d3e7c7161c83ac        3309
1152921504606847348     372     24b16fede9a67c9251d3e7c7161c83ac        3308
```

## 结论

本教程完成了 2 个练习：

- 上游 3 个 MySQL Server 实例的分片迁移，每个实例的自增 ID 都互不重叠。
- 上游 3 个 MySQL Server 实例的分片迁移，这些实例的自增 ID 存在冲突。

本教程介绍了分片迁移中，DM 如何在集群中导入初始数据，以及 DM 读取 binlog，从而使下游 TiDB 集群与上游实例保持同步。

关于 DM 的更多详情，请参考 [Data Migration 简介](/reference/tools/data-migration/overview.md)，或加入 [TiDB Community Slack](https://pingcap.com/tidbslack/) channel 参与讨论。
