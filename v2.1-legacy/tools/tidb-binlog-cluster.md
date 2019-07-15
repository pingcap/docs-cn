---
title: TiDB-Binlog Cluster 版本用户文档
category: tools
---

# TiDB-Binlog Cluster 版本用户文档

本文档介绍 cluster 版本 TiDB-Binlog 的架构以及部署方案。

TiDB-Binlog 是一个用于收集 TiDB 的 Binlog，并提供实时备份和同步功能的商业工具。

TiDB-Binlog 支持以下功能场景：

* **数据同步**：同步 TiDB 集群数据到其他数据库
* **实时备份和恢复**：备份 TiDB 集群数据，同时可以用于 TiDB 集群故障时恢复

## TiDB-Binlog 架构

TiDB-Binlog 的整体架构：

![TiDB-Binlog 架构](../media/tidb_binlog_cluster_architecture.png)

TiDB-Binlog 集群主要分为 Pump 和 Drainer 两个组件：

### Pump

Pump 用于实时记录 TiDB 产生的 Binlog，并将 Binlog 按照事务的提交时间进行排序，再提供给 Drainer 进行消费。

### Drainer

Drainer 从各个 Pump 中收集 Binlog 进行归并，再将 Binlog 转化成 SQL 或者指定格式的数据，最终同步到下游。

## 主要特性

* 多个 Pump 形成一个集群，可以水平扩容；
* TiDB 通过内置的 Pump Client 将 Binlog 分发到各个 Pump；
* Pump 负责存储 Binlog，并将 Binlog 按顺序提供给 Drainer；
* Drainer 负责读取各个 Pump 的 Binlog，归并排序后发送到下游。

## 服务器要求

Pump 和 Drainer 都支持部署和运行在 Intel x86-64 架构的 64 位通用硬件服务器平台上。对于开发，测试以及生产环境的服务器硬件配置有以下要求和建议：

| 服务     | 部署数量       | CPU   | 磁盘          | 内存   |
| -------- | -------- | --------| --------------- | ------ |
| Pump | 3 | 8核+   | SSD, 200 GB+ | 16G |
| Drainer | 1 | 8核+ | SAS, 100 GB+ （如果输出为本地文件，则使用 SSD，并增加磁盘大小） | 16G |

## 注意

* 需要使用 TiDB v2.0.8-binlog、v2.1.0-rc.5 及以上版本，否则不兼容该版本的 TiDB-Binlog。
* 在运行 TiDB 时，需要保证至少一个 Pump 正常运行。
* 通过给 TiDB 增加启动参数 enable-binlog 来开启 binlog 服务。尽量保证同一集群的所有 TiDB 都开启了 binlog 服务，否则在同步数据时可能会导致上下游数据不一致。如果要临时运行一个不开启 binlog 服务的 TiDB 实例，需要在 TiDB 的配置文件中设置 `run_ddl= false`。
* Drainer 不支持对 ignore schemas（在过滤列表中的 schemas）的 table 进行 rename DDL 操作。
* 在已有的 TiDB 集群中启动 Drainer，一般需要全量备份并且获取 savepoint，然后导入全量备份，最后启动 Drainer 从 savepoint 开始同步增量数据。
* Drainer 支持将 Binlog 同步到 MySQL、TiDB、Kafka 或者本地文件。如果需要将 Binlog 同步到其他类型的目的地中，可以设置 Drainer 将 Binlog 同步到 Kafka，再读取 Kafka 中的数据进行自定义处理，参考 [binlog slave client 用户文档](../tools/binlog-slave-client.md)。
* 如果 TiDB-Binlog 用于增量恢复，可以设置下游为 `pb`，Drainer 会将 binlog 转化为指定的 proto buffer 格式的数据，再写入到本地文件中。这样就可以使用 [Reparo](../tools/reparo.md) 恢复增量数据。
* Pump/Drainer 的状态需要区分已暂停（paused）和下线（offline），Ctrl + C 或者 kill 进程，Pump 和 Drainer 的状态都将变为 paused。暂停状态的 Pump 不需要将已保存的 Binlog 数据全部发送到 Drainer；如果需要较长时间退出 Pump（或不再使用该 Pump），需要使用 binlogctl 工具来下线 Pump。Drainer 同理。
* 如果下游为 MySQL/TiDB，数据同步后可以使用 [sync-diff-inspector](../tools/sync-diff-inspector.md) 进行数据校验。

## TiDB-Binlog 部署

### 使用 TiDB-Ansible 部署 TiDB-Binlog

#### 第 1 步：下载 TiDB-Ansible

1. 以 TiDB 用户登录中控机并进入 `/home/tidb` 目录。以下为 TiDB-Ansible 分支与 TiDB 版本的对应关系，版本选择可咨询官方 info@pingcap.com。

    | TiDB-Ansible 分支 | TiDB 版本 | 备注 |
    | ---------------- | --------- | --- |
    | release-2.0-new-binlog | 2.0 版本 | 最新 2.0 稳定版本，可用于生产环境。 |
    | release-2.1 | 2.1 版本 | 最新 2.1 稳定版本，可用于生产环境（建议）。 |
    | master | master 版本 | 包含最新特性，每日更新。 |

2. 使用以下命令从 GitHub [TiDB-Ansible 项目](https://github.com/pingcap/tidb-ansible)上下载 TiDB-Ansible 相应分支，默认的文件夹名称为 `tidb-ansible`。

    - 下载 2.0 版本：

        ```bash
        $ git clone -b release-2.0-new-binlog https://github.com/pingcap/tidb-ansible.git
        ```

    - 下载 2.1 版本：

        ```bash
        $ git clone -b release-2.1 https://github.com/pingcap/tidb-ansible.git
        ```

    - 下载 master 版本：

        ```bash
        $ git clone https://github.com/pingcap/tidb-ansible.git
        ```

#### 第 2 步：部署 Pump

1. 修改 tidb-ansible/inventory.ini 文件

    1. 设置 `enable_binlog = True`，表示 TiDB 集群开启 binlog。

        ```ini
        ## binlog trigger
        enable_binlog = True
        ```

    2. 为 `pump_servers` 主机组添加部署机器 IP。

        ```ini
        ## Binlog Part
        [pump_servers]
        172.16.10.72
        172.16.10.73
        172.16.10.74
        ```

        默认 Pump 保留 5 天数据，如需修改可修改 `tidb-ansible/conf/pump.yml` 文件中 `gc` 变量值，并取消注释，如修改为 7。

        ```yaml
        global:
          # an integer value to control the expiry date of the binlog data, which indicates for how long (in days) the binlog data would be stored
          # must be bigger than 0
          gc: 7
        ```

        请确保部署目录有足够空间存储 binlog，详见：[部署目录调整](../op-guide/ansible-deployment.md#部署目录调整)，也可为 Pump 设置单独的部署目录。

        ```ini
        ## Binlog Part
        [pump_servers]
        pump1 ansible_host=172.16.10.72 deploy_dir=/data1/pump
        pump2 ansible_host=172.16.10.73 deploy_dir=/data1/pump
        pump3 ansible_host=172.16.10.74 deploy_dir=/data1/pump
        ```

2. 部署并启动含 Pump 组件的 TiDB 集群

    参照上文配置完 `inventory.ini` 文件后，从以下两种方式中选择一种进行部署。

    **方式一**：在已有的 TiDB 集群上增加 Pump 组件，需按以下步骤逐步进行。

    1. 部署 pump_servers 和 node_exporters

        ```
        ansible-playbook deploy.yml -l ${pump1_ip}, ${pump2_ip}, [${alias1_name}, ${alias2_name}]
        ```

    2. 启动 pump_servers

        ```
        ansible-playbook start.yml --tags=pump
        ```

    3. 更新并重启 tidb_servers

        ```
        ansible-playbook rolling_update.yml --tags=tidb
        ```

    4. 更新监控信息

        ```
        ansible-playbook rolling_update_monitor.yml --tags=prometheus
        ```

    **方式二**：从零开始部署含 Pump 组件的 TiDB 集群

    使用 Ansible 部署 TiDB 集群，方法参考 [TiDB Ansible 部署方案](../op-guide/ansible-deployment.md)。

3. 查看 Pump 服务状态

    使用 binlogctl 查看 Pump 服务状态，pd-urls 参数请替换为集群 PD 地址，结果 State 为 online 表示 Pump 启动成功。

    ```bash
    $ cd /home/tidb/tidb-ansible
    $ resources/bin/binlogctl -pd-urls=http://172.16.10.72:2379 -cmd pumps

    INFO[0000] pump: {NodeID: ip-172-16-10-72:8250, Addr: 172.16.10.72:8250, State: online, MaxCommitTS: 403051525690884099, UpdateTime: 2018-12-25 14:23:37 +0800 CST}
    INFO[0000] pump: {NodeID: ip-172-16-10-73:8250, Addr: 172.16.10.73:8250, State: online, MaxCommitTS: 403051525703991299, UpdateTime: 2018-12-25 14:23:36 +0800 CST}
    INFO[0000] pump: {NodeID: ip-172-16-10-74:8250, Addr: 172.16.10.74:8250, State: online, MaxCommitTS: 403051525717360643, UpdateTime: 2018-12-25 14:23:35 +0800 CST}
    ```

#### 第 3 步：部署 Drainer

1. 获取 initial_commit_ts

    使用 binlogctl 工具生成 Drainer 初次启动所需的 tso 信息，命令：

    ```bash
    $ cd /home/tidb/tidb-ansible
    $ resources/bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd generate_meta
    INFO[0000] [pd] create pd client with endpoints [http://192.168.199.118:32379]
    INFO[0000] [pd] leader switches to: http://192.168.199.118:32379, previous:
    INFO[0000] [pd] init cluster id 6569368151110378289
    2018/06/21 11:24:47 meta.go:117: [info] meta: &{CommitTS:400962745252184065}
    ```

    该命令会输出 `meta: &{CommitTS:400962745252184065}`，CommitTS 的值作为 Drainer 初次启动使用的 `initial-commit-ts` 参数的值。

2. 全量数据的备份与恢复

    推荐使用 mydumper 备份 TiDB 的全量数据，再使用 loader 将备份数据导入到下游。具体使用方法参考：[备份与恢复](https://github.com/pingcap/docs-cn/blob/master/op-guide/backup-restore.md)。

3. 修改 `tidb-ansible/inventory.ini` 文件

    为 `drainer_servers` 主机组添加部署机器 IP，initial_commit_ts 请设置为获取的 initial_commit_ts，仅用于 Drainer 第一次启动。

    - 以下游为 MySQL 为例，别名为 `drainer_mysql`。

        ```ini
        [drainer_servers]
        drainer_mysql ansible_host=172.16.10.71 initial_commit_ts="402899541671542785"
        ```

    - 以下游为 pb 为例，别名为 `drainer_pb`。

        ```ini
        [drainer_servers]
        drainer_pb ansible_host=172.16.10.71 initial_commit_ts="402899541671542785"
        ```

4. 修改配置文件

    - 以下游为 MySQL 为例

        ```bash
        $ cd /home/tidb/tidb-ansible/conf
        $ cp drainer.toml drainer_mysql_drainer.toml
        $ vi drainer_mysql_drainer.toml
        ```

        > **注意：**
        >
        > 配置文件名命名规则为 `别名_drainer.toml`，否则部署时无法找到自定义配置文件。

        db-type 设置为 "mysql"， 配置下游 MySQL 信息。

        ```toml
        # downstream storage, equal to --dest-db-type
        # Valid values are "mysql", "pb", "kafka", "flash".
        db-type = "mysql"

        # the downstream MySQL protocol database
        [syncer.to]
        host = "172.16.10.72"
        user = "root"
        password = "123456"
        port = 3306
        # Time and size limits for flash batch write
        # time-limit = "30s"
        # size-limit = "100000"
        ```

    - 以下游为 proto buffer（pb）格式的本地文件为例

        ```bash
        $ cd /home/tidb/tidb-ansible/conf
        $ cp drainer.toml drainer_pb_drainer.toml
        $ vi drainer_pb_drainer.toml
        ```

        db-type 设置为 "pb"。

        ```toml
        # downstream storage, equal to --dest-db-type
        # Valid values are "mysql", "pb", "kafka", "flash".
        db-type = "pb"

        # Uncomment this if you want to use `pb` or `sql` as `db-type`.
        # `Compress` compresses the output file, like the `pb` and `sql` file. Now it supports the `gzip` algorithm only.
        # The value can be `gzip`. Leave it empty to disable compression.
        [syncer.to]
        compression = ""
        # default data directory: "{{ deploy_dir }}/data.drainer"
        dir = "data.drainer"
        ```

5. 部署 Drainer

    ```bash
    $ ansible-playbook deploy_drainer.yml
    ```

6. 启动 Drainer

    ```bash
    $ ansible-playbook start_drainer.yml
    ```

### 使用 Binary 部署 TiDB-Binlog

#### 下载官方 Binary

```bash
wget https://download.pingcap.org/tidb-{version}-linux-amd64.tar.gz
wget https://download.pingcap.org/tidb-{version}-linux-amd64.sha256

# 检查文件完整性，返回 ok 则正确
sha256sum -c tidb-{version}-linux-amd64.sha256
```

对于 v2.1.0 GA 及以上版本，Pump 和 Drainer 已经包含在 TiDB 的下载包中，其他版本需要单独下载 Pump 和 Drainer:

```bash
wget https://download.pingcap.org/tidb-binlog-{version}-linux-amd64.tar.gz
wget https://download.pingcap.org/tidb-binlog-{version}-linux-amd64.sha256

# 检查文件完整性，返回 ok 则正确
sha256sum -c tidb-binlog-{version}-linux-amd64.sha256
```

#### 使用样例

假设有三个 PD，一个 TiDB，另外有两台机器用于部署 Pump，一台机器用于部署 Drainer。各个节点信息如下：

```
TiDB="192.168.0.10"
PD1="192.168.0.16"
PD2="192.168.0.15"
PD3="192.168.0.14"
Pump="192.168.0.11"
Pump="192.168.0.12"
Drainer="192.168.0.13"
```

下面以此为例，说明 Pump/Drainer 的使用。

1. 使用 binary 部署 Pump

    - Pump 命令行参数说明（以在 “192.168.0.11” 上部署为例）

        ```bash
        Usage of Pump:
        -L string
            日志输出信息等级设置：debug，info，warn，error，fatal (默认 "info")
        -V
            打印版本信息
        -addr string
            Pump 提供服务的 RPC 地址(-addr="192.168.0.11:8250")
        -advertise-addr string
            Pump 对外提供服务的 RPC 地址(-advertise-addr="192.168.0.11:8250")
        -config string
            配置文件路径，如果你指定了配置文件，Pump 会首先读取配置文件的配置；
            如果对应的配置在命令行参数里面也存在，Pump 就会使用命令行参数的配置来覆盖配置文件里的配置。
        -data-dir string
            Pump 数据存储位置路径
        -enable-tolerant
            开启 tolerant 后，如果 binlog 写入失败，Pump 不会报错（默认开启）
        -gc int
            Pump 只保留多少天以内的数据 (默认 7)
        -heartbeat-interval int
            Pump 向 PD 发送心跳间隔 (单位 秒)
        -log-file string
            log 文件路径
        -log-rotate string
            log 文件切换频率，hour/day
        -metrics-addr string
            Prometheus Pushgateway 地址，不设置则禁止上报监控信息
        -metrics-interval int
            监控信息上报频率 (默认 15，单位 秒)
        -pd-urls string
            PD 集群节点的地址 (-pd-urls="http://192.168.0.16:2379,http://192.168.0.15:2379,http://192.168.0.14:2379")
        ```

    - Pump 配置文件（以在 “192.168.0.11” 上部署为例）

        ```toml
        # Pump Configuration

        # Pump 绑定的地址
        addr = "192.168.0.11:8250"

        # Pump 对外提供服务的地址
        advertise-addr = "192.168.0.11:8250"

        # Pump 只保留多少天以内的数据 (默认 7)
        gc = 7

        # Pump 数据存储位置路径
        data-dir = "data.pump"

        # Pump 向 PD 发送心跳的间隔 (单位 秒)
        heartbeat-interval = 2

        # PD 集群节点的地址
        pd-urls = "http://192.168.0.16:2379,http://192.168.0.15:2379,http://192.168.0.14:2379"

        # [storage]
        # 设置为 true（默认值）来保证可靠性，确保 binlog 数据刷新到磁盘
        # sync-log = true
        ```

    - 启动示例

        ```bash
        ./bin/pump -config pump.toml
        ```

        如果命令行参数与配置文件中的参数重合，则使用命令行设置的参数的值。

2. 使用 binary 部署 Drainer

    - Drainer 命令行参数说明（以在 “192.168.0.13” 上部署为例）

        ```bash
        Usage of Drainer
        -L string
            日志输出信息等级设置：debug，info，warn，error，fatal (默认 "info")
        -V
            打印版本信息
        -addr string
            Drainer 提供服务的地址(-addr="192.168.0.13:8249")
        -c int
            同步下游的并发数，该值设置越高同步的吞吐性能越好 (default 1)
        -config string
            配置文件路径，Drainer 会首先读取配置文件的配置；
            如果对应的配置在命令行参数里面也存在，Drainer 就会使用命令行参数的配置来覆盖配置文件里面的配置
        -data-dir string
            Drainer 数据存储位置路径 (默认 "data.drainer")
        -dest-db-type string
            Drainer 下游服务类型 (默认为 mysql，支持 kafka、pb、flash)
        -detect-interval int
            向 PD 查询在线 Pump 的时间间隔 (默认 10，单位 秒)
        -disable-detect
            是否禁用冲突监测
        -disable-dispatch
            是否禁用拆分单个 binlog 的 SQL 的功能，如果设置为 true，则每个 binlog
            按顺序依次还原成单个事务进行同步（下游服务类型为 MySQL，该项设置为 False）
        -ignore-schemas string
            db 过滤列表 (默认 "INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql,test")，
            不支持对 ignore schemas 的 table 进行 rename DDL 操作
        -initial-commit-ts (默认为 0)
            如果 Drainer 没有相关的断点信息，可以通过该项来设置相关的断点信息
        -log-file string
            log 文件路径
        -log-rotate string
            log 文件切换频率，hour/day
        -metrics-addr string
            Prometheus Pushgateway 地址，不设置则禁止上报监控信息
        -metrics-interval int
            监控信息上报频率（默认 15，单位：秒）
        -pd-urls string
            PD 集群节点的地址 (-pd-urls="http://192.168.0.16:2379,http://192.168.0.15:2379,http://192.168.0.14:2379")
        -safe-mode
            是否开启安全模式（将 update 语句拆分为 delete + replace 语句）
        -txn-batch int
            输出到下游数据库一个事务的 SQL 数量（默认 1）
        ```

    - Drainer 配置文件（以在 “192.168.0.13” 上部署为例）

        ```toml
        # Drainer Configuration.

        # Drainer 提供服务的地址("192.168.0.13:8249")
        addr = "192.168.0.13:8249"

        # 向 PD 查询在线 Pump 的时间间隔 (默认 10，单位 秒)
        detect-interval = 10

        # Drainer 数据存储位置路径 (默认 "data.drainer")
        data-dir = "data.drainer"

        # PD 集群节点的地址
        pd-urls = "http://192.168.0.16:2379,http://192.168.0.15:2379,http://192.168.0.14:2379"

        # log 文件路径
        log-file = "drainer.log"

        # Drainer 从 Pump 获取 binlog 时对数据进行压缩，值可以为 "gzip"，如果不配置则不进行压缩
        # compressor = "gzip"

        # Syncer Configuration
        [syncer]
        # 如果设置了该项，会使用该 sql-mode 解析 DDL 语句
        # sql-mode = "STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION"

        # 输出到下游数据库一个事务的 SQL 语句数量 (默认 20)
        txn-batch = 20

        # 同步下游的并发数，该值设置越高同步的吞吐性能越好 (默认 16)
        worker-count = 16

        # 是否禁用拆分单个 binlog 的 SQL 的功能，如果设置为 true，则按照每个 binlog
        # 顺序依次还原成单个事务进行同步（下游服务类型为 MySQL, 该项设置为 False）
        disable-dispatch = false

        # Drainer 下游服务类型（默认为 mysql）
        # 参数有效值为 "mysql"，"pb"，"kafka"，"flash"
        db-type = "mysql"

        # db 过滤列表 (默认 "INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql,test")，
        # 不支持对 ignore schemas 的 table 进行 rename DDL 操作
        ignore-schemas = "INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql"

        # replicate-do-db 配置的优先级高于 replicate-do-table。如果配置了相同的库名，支持使用正则表达式进行配置。
        # 以 '~' 开始声明使用正则表达式

        # replicate-do-db = ["~^b.*","s1"]

        # [[syncer.replicate-do-table]]
        # db-name ="test"
        # tbl-name = "log"

        # [[syncer.replicate-do-table]]
        # db-name ="test"
        # tbl-name = "~^a.*"

        # 忽略同步某些表
        # [[syncer.ignore-table]]
        # db-name = "test"
        # tbl-name = "log"

        # db-type 设置为 mysql 时，下游数据库服务器参数
        [syncer.to]
        host = "192.168.0.13"
        user = "root"
        password = ""
        port = 3306

        # db-type 设置为 pb 时，存放 binlog 文件的目录
        # [syncer.to]
        # dir = "data.drainer"

        # db-type 设置为 kafka 时，Kafka 相关配置
        # [syncer.to]
        # zookeeper-addrs = "127.0.0.1:2181"
        # kafka-addrs = "127.0.0.1:9092"
        # kafka-version = "0.8.2.0"

        # 保存 binlog 数据的 Kafka 集群的 topic 名称，默认值为 <cluster-id>_obinlog
        # 如果运行多个 Drainer 同步数据到同一个 Kafka 集群，每个 Drainer 的 topic-name 需要设置不同的名称
        # topic-name = ""
        ```

    - 启动示例

        > **注意：**
        >
        > 如果下游为 MySQL/TiDB，为了保证数据的完整性，在 Drainer 初次启动前需要获取 initial-commit-ts 的值，并进行全量数据的备份与恢复。详细信息参见[部署 Drainer](#第-3-步部署-drainer)。

        初次启动时使用参数 `initial-commit-ts`， 命令如下：

        ```bash
        ./bin/drainer -config drainer.toml -initial-commit-ts {initial-commit-ts}
        ```

        如果命令行参数与配置文件中的参数重合，则使用命令行设置的参数的值。

## TiDB-Binlog 运维

### Pump/Drainer 状态

Pump/Drainer 中状态的定义：

* online：正常运行中；
* pausing：暂停中，当使用 kill 或者 Ctrl+C 退出进程时，都将处于该状态；
* paused：已暂停，处于该状态时 Pump 不接受写 binlog 的请求，也不继续为 Drainer 提供 binlog，Drainer 不再往下游同步数据。当 Pump/Drainer 安全退出了所有的线程后，将自己的状态切换为 paused，再退出进程；
* closing：下线中，使用 binlogctl 控制 Pump/Drainer 下线，在进程退出前都处于该状态。下线时 Pump 不再接受写 binlog 的请求，等待所有的 binlog 数据被 Drainer 消费完；
* offline：已下线，当 Pump 已经将已保存的所有 binlog 数据全部发送给 Drainer 后，该 Pump 将状态切换为 offline；Drainer 只需要等待各个线程退出后即可切换状态为 offline。

> **注意：**
>
> * 当暂停 Pump/Drainer 时，数据同步会中断；
> * Pump 在下线时需要确认自己的数据被所有的非 offline 状态的 Drainer 消费了，所以在下线 Pump 时需要确保所有的 Drainer 都是处于 online 状态，否则 Pump 无法正常下线；
> * Pump 保存的 binlog 数据只有在被所有非 offline 状态的 Drainer 消费的情况下才会被 GC 处理；
> * 不要轻易下线 Drainer，只有在永久不需要使用该 Drainer 的情况下才需要下线 Drainer。

关于 Pump/Drainer 暂停、下线、状态查询、状态修改等具体的操作方法，参考如下 binlogctl 工具的使用方法介绍。

### binlogctl 工具

[binlogctl](https://github.com/pingcap/tidb-tools/tree/master/tidb-binlog/binlogctl) 是一个 TiDB-Binlog 配套的运维工具，具有如下功能：

* 获取当前 ts
* 查看 Pump/Drainer 状态
* 修改 Pump/Drainer 状态
* 暂停/下线 Pump/Drainer

使用 binlogctl 的场景：

* 第一次运行 Drainer，需要获取当前的 ts
* Pump/Drainer 异常退出，状态没有更新，对业务造成影响，可以直接使用该工具修改状态
* 同步出现故障/检查运行情况，需要查看 Pump/Drainer 的状态
* 维护集群，需要暂停/下线 Pump/Drainer

binlogctl 下载链接：

```bash
wget https://download.pingcap.org/binlogctl-new-linux-amd64.tar.gz
wget https://download.pingcap.org/binlogctl-new-linux-amd64.sha256

# 检查文件完整性，返回 ok 则正确
sha256sum -c tidb-binlog-new-linux-amd64.sha256
```

binlogctl 使用说明：

命令行参数：

```bash
Usage of binlogctl:
-V
输出 binlogctl 的版本信息
-cmd string
    命令模式，包括 "generate_meta", "pumps", "drainers", "update-pump" ,"update-drainer", "pause-pump", "pause-drainer", "offline-pump", "offline-drainer"
-data-dir string
    保存 Drainer 的 checkpoint 的文件的路径 (默认 "binlog_position")
-node-id string
    Pump/Drainer 的 ID
-pd-urls string
    PD 的地址，如果有多个，则用"," 连接 (默认 "http://127.0.0.1:2379")
-ssl-ca string
    SSL CAs 文件的路径
-ssl-cert string
        PEM 格式的 X509 认证文件的路径
-ssl-key string
        PEM 格式的 X509 key 文件的路径
-time-zone string
    如果设置时区，在 "generate_meta" 模式下会打印出获取到的 tso 对应的时间。例如"Asia/Shanghai" 为 CST 时区，"Local" 为本地时区
```

命令示例：

- 查询所有的 Pump/Drainer 的状态：

    设置 `cmd` 为 `pumps` 或者 `drainers` 来查看所有 Pump 或者 Drainer 的状态。例如：

    ```bash
    bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd pumps

    INFO[0000] pump: {NodeID: ip-172-16-30-67:8250, Addr: 172.16.30.192:8250, State: online, MaxCommitTS: 405197570529820673, UpdateTime: 2018-12-25 14:23:37 +0800 CST}
    ```

- 修改 Pump/Drainer 的状态

    设置 `cmd` 为 `update-pump` 或者 `update-drainer` 来更新 Pump 或者 Drainer 的状态。Pump 和 Drainer 的状态可以为：online，pausing，paused，closing 以及 offline。例如：

    ```bash
    bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd update-pump -node-id ip-127-0-0-1:8250 -state paused
    ```

    这条命令会修改 Pump/Drainer 保存在 pd 中的状态。

- 暂停/下线 Pump/Drainer

    分别设置 `cmd` 为 `pause-pump`、`pause-drainer`、`offline-pump`、`offline-drainer` 来暂停 Pump、暂停 Drainer、下线 Pump、下线 Drainer。例如：

    ```bash
    bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd pause-pump -node-id ip-127-0-0-1:8250
    ```

    binlogctl 会发送 HTTP 请求给 Pump/Drainer，Pump/Drainer 收到命令后会退出进程，并且将自己的状态设置为 paused/offline。

- 生成 Drainer 启动需要的 meta 文件

    ```bash
    bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd generate_meta

    INFO[0000] [pd] create pd client with endpoints [http://192.168.199.118:32379]
    INFO[0000] [pd] leader switches to: http://192.168.199.118:32379, previous:
    INFO[0000] [pd] init cluster id 6569368151110378289
    2018/06/21 11:24:47 meta.go:117: [info] meta: &{CommitTS:400962745252184065}
    ```

    该命令会生成一个文件 `{data-dir}/savepoint`， 该文件中保存了 Drainer 初次启动需要的 tso 信息。

## TiDB-Binlog 监控

使用 Ansible 部署成功后，可以进入 Grafana Web 界面（默认地址: <http://grafana_ip:3000>，默认账号：admin，密码：admin）查看 Pump 和 Drainer 的运行状态。

监控指标说明：[TiDB-Binlog 监控指标说明](../tools/tidb-binlog-monitor.md)

## 版本升级方法

新版本的 TiDB（v2.0.8-binlog、v2.1.0-rc.5 及以上版本）不兼容 [Kafka 版本](../tools/tidb-binlog-kafka.md)以及 [Local 版本](../tools/tidb-binlog.md)的 TiDB-Binlog，集群升级到新版本后只能使用 Cluster 版本的 TiDB-Binlog。如果在升级前已经使用了 Kafka／Local 版本的 TiDB-Binlog，必须将其升级到 Cluster 版本。

 TiDB-Binlog 版本与 TiDB 版本的对应关系如下：

| TiDB-Binlog 版本 | TiDB 版本 | 说明 |
|---|---|---|
| Local | TiDB 1.0 及更低版本 ||
| Kafka | TiDB 1.0 ~ TiDB 2.1 RC5 | TiDB 1.0 支持 local 版本和 Kafka 版本的 TiDB-Binlog。 |
| Cluster | TiDB v2.0.8-binlog，TiDB 2.1 RC5 及更高版本 | TiDB v2.0.8-binlog 是一个支持 Cluster 版本 TiDB-Binlog 的 2.0 特殊版本。 |

升级流程：

* 如果能接受重新导全量数据，则可以直接废弃老版本，按本文档部署。

* 如果想从原来的 checkpoint 继续同步，则使用以下升级流程：
    1. 部署新版本 Pump；
    2. 暂停 TiDB 集群业务；
    3. 更新 TiDB 以及配置，写 Binlog 到新的 Pump Cluster；
    4. TiDB 集群重新接入业务；
    5. 确认老版本的 Drainer 已经将老版本的 Pump 的数据完全同步到下游；

        查询 Drainer 的 `status` 接口，示例命令如下：

        ```bash
        $ curl 'http://172.16.10.49:8249/status'
        {"PumpPos":{"172.16.10.49:8250":{"offset":32686}},"Synced": true ,"DepositWindow":{"Upper":398907800202772481,"Lower":398907799455662081}}
        ```

        如果返回的 `Synced` 为 true，则可以认为 Binlog 数据已经全部同步到了下游。
    6. 启动新版本 Drainer；
    7. 下线无用的老版本的 Pump、Drainer 以及依赖的 Kafka 和 Zookeeper。
