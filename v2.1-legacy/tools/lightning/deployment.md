---
title: TiDB-Lightning 部署与执行
category: tools
---

# TiDB-Lightning 部署与执行

本文主要介绍 TiDB-Lightning 单独部署与混合部署的硬件需求，Ansible 部署与手动部署这两种部署方式，以及启动与执行。

## 注意事项

在使用 TiDB-Lightning 前，需注意以下事项：

- TiDB-Lightning 运行后，TiDB 集群将无法正常对外提供服务。
- 若 `tidb-lightning` 崩溃，集群会留在“导入模式”。若忘记转回“普通模式”，集群会产生大量未压缩的文件，继而消耗 CPU 并导致迟延 (stall)。此时，需要使用 `tidb-lightning-ctl` 手动将集群转回“普通模式”：

    ```sh
    bin/tidb-lightning-ctl -switch-mode=normal
    ```

## 硬件需求

`tidb-lightning` 和 `tikv-importer` 这两个组件皆为资源密集程序，建议各自单独部署。如果资源有限，可以将 `tidb-lightning` 和 `tikv-importer` 混合部署在同一台机器上。

### 单独部署的硬件配置

为了优化效能，使用单独部署建议的硬件配置如下：

- `tidb-lightning`

    - 32+ 逻辑核 CPU
    - 16 GB+ 内存
    - 1 TB+ SSD 硬盘，读取速度越快越好
    - 使用万兆网卡
    - 运行过程默认会打满 CPU，建议单独部署。条件不允许的情况下可以和其他组件 (比如 `tidb-server`) 部署在同一台机器上，然后通过配置 `region-concurrency` 限制 `tidb-lightning` 的 CPU 使用。

- `tikv-importer`

    - 32+ 逻辑核 CPU
    - 32 GB+ 内存
    - 1 TB+ SSD 硬盘，IOPS 越高越好
    - 使用万兆网卡
    - 运行过程中 CPU、I/O 和网络带宽都可能打满，建议单独部署。条件不允许的情况下可以和其他组件（比如 `tikv-server`）部署在同一台机器上，但可能会影响导入速度。

如果机器充裕的话，可以部署多套 `tidb-lightning` + `tikv-importer`，然后将源数据以表为粒度进行切分，并发导入。

### 混合部署的硬件配置

如果条件有限，可以将 `tidb-lightning` 和 `tikv-importer`（也可以是其他程序）混合部署在同一台机器上，但这样会影响导入速度。

使用混合部署建议的硬件配置如下：

- 32+ 逻辑核 CPU
- 32 GB+ 内存
- 1 TB+ SSD 硬盘，IOPS 越高越好
- 使用万兆网卡

> **注意：**
>
> `tidb-lightning` 是 CPU 密集型程序，如果和其它程序混合部署，需要通过 `region-concurrency` 限制 `tidb-lightning` 的 CPU 实际占用核数，否则会影响其他程序的正常运行。建议将混合部署机器上 75% 的 CPU 分配给 `tidb-lightning`。例如，机器为 32 核，则 `tidb-lightning` 的 `region-concurrency` 可设为 24。

## 部署 TiDB-Lightning

本节介绍 TiDB-Lightning 的两种部署方式：[使用 Ansible 部署](#使用-ansible-部署-tidb-lightning)和[手动部署](#手动部署-tidb-lightning)。

### 使用 Ansible 部署 TiDB-Lightning

TiDB-Lightning 可随 TiDB 集群一起用 [Ansible 部署](../../op-guide/ansible-deployment.md)。

1. 编辑 `inventory.ini`，分别配置一个 IP 来部署 `tidb-lightning` 和 `tikv-importer`。

    ```ini
    ...

    [importer_server]
    192.168.20.9

    [lightning_server]
    192.168.20.10

    ...
    ```

2. 修改 `group_vars/*.yml` 的变量配置这两个工具。

    - `group_vars/all.yml`

        ```yaml
        ...
        # tikv-importer 的监听端口。需对 tidb-lightning 服务器开放。
        tikv_importer_port: 20170
        ...
        ```

    - `group_vars/lightning_server.yml`

        ```yaml
        ---
        dummy:

        # 提供监控告警的端口。需对监控服务器 (monitoring_server) 开放。
        tidb_lightning_pprof_port: 10089

        # 获取 mydumper SQL dump 的路径。
        data_source_dir: "{{ deploy_dir }}/mydumper"
        ```

    - `group_vars/importer_server.yml`

        ```yaml
        ---
        dummy:

        # 储存引擎文件的路径。需存放在空间足够大的分区。
        import_dir: "{{ deploy_dir }}/data.import"
        ```

3. 开始部署。

    ```sh
    ansible-playbook bootstrap.yml
    ansible-playbook deploy.yml
    ```

4. 将数据源写入 `data_source_dir` 指定的路径。

5. 登录 `tikv-importer` 的服务器，并执行以下命令来启动 Importer。

    ```sh
    scripts/start_importer.sh
    ```

6. 登录 `tidb-lightning` 的服务器，并执行以下命令来启动 Lightning，开始导入过程。

    ```sh
    scripts/start_lightning.sh
    ```

7. 完成后，在 `tikv-importer` 的服务器执行 `scripts/stop_importer.sh` 来关闭 Importer。

### 手动部署 TiDB-Lightning

#### 第 1 步：部署 TiDB 集群

在开始数据导入之前，需先部署一套要进行导入的 TiDB 集群 (版本要求 2.0.9 以上)，建议使用最新版。部署方法可参考 [TiDB 快速入门指南](../../QUICKSTART.md)。

#### 第 2 步：下载 TiDB-Lightning 安装包

通过以下链接获取 TiDB-Lightning 安装包（需选择与集群相同的版本）：

- **v2.1**: https://download.pingcap.org/tidb-lightning-release-2.1-linux-amd64.tar.gz
- **v2.0**: https://download.pingcap.org/tidb-lightning-release-2.0-linux-amd64.tar.gz

#### 第 3 步：启动 `tikv-importer`

1. 从安装包上传 `bin/tikv-importer`。

2. 配置 `tikv-importer.toml`。

    ```toml
    # TiKV Importer 配置文件模版

    # 日志文件。
    log-file = "tikv-importer.log"
    # 日志等级：trace、debug、info、warn、error、off。
    log-level = "info"

    [server]
    # tikv-importer 监听的地址，tidb-lightning 需要连到这个地址进行数据写入。
    addr = "0.0.0.0:20170"
    # gRPC 服务器的线程池大小。
    grpc-concurrency = 16

    [metric]
    # 给 Prometheus 客户端的推送任务名称。
    job = "tikv-importer"
    # 给 Prometheus 客户端的推送间隔。
    interval = "15s"
    # Prometheus Pushgateway 地址。
    address = ""

    [rocksdb]
    # 最大的背景任务并发数。
    max-background-jobs = 32

    [rocksdb.defaultcf]
    # 数据在刷新到硬盘前能存于内存的容量上限。
    write-buffer-size = "1GB"
    # 存于内存的写入缓冲最大数量。
    max-write-buffer-number = 8

    # 各个压缩层级使用的算法。
    # 第 0 层的算法用于压缩 KV 数据。
    # 第 6 层的算法用于压缩 SST 文件。
    # 第 1 至 5 层的算法目前忽略。
    compression-per-level = ["lz4", "no", "no", "no", "no", "no", "zstd"]

    [import]
    # 存储引擎文档 (engine file) 的文件夹路径。
    import-dir = "/tmp/tikv/import"
    # 处理 gRPC 请求的线程数量。
    num-threads = 16
    # 导入任务并发数。
    num-import-jobs = 24
    # 预处理 Region 最长时间。
    #max-prepare-duration = "5m"
    # 把要导入的数据切分为这个大小的 Region。
    #region-split-size = "96MB"
    # 流管道窗口大小，管道满时会阻塞流。
    #stream-channel-window = 128
    # 引擎文档同时打开的最大数量。
    max-open-engines = 8
    ```

3. 运行 `tikv-importer`。

    ```sh
    nohup ./tikv-importer -C tikv-importer.toml > nohup.out &
    ```

#### 第 4 步：启动 `tidb-lightning`

1. 从安装包上传 `bin/tidb-lightning` 及 `bin/tidb-lightning-ctl`。

2. 将 mydumper SQL dump 数据源写入到同样的机器。

3. 配置 `tidb-lightning.toml`。

    ```toml
    # TiDB-Lightning 配置文件模版

    [lightning]
    # 用于调试和 Prometheus 监控的 HTTP 端口。输入 0 关闭。
    pprof-port = 10089

    # 开始导入前先检查集群版本是否支持。
    #check-requirements = true

    # 控制同时处理的表的数量。这个值会影响 tikv-importer 的内存使用量。
    # 不能超过 tikv-importer 中 max-open-engines 的值。
    table-concurrency = 8
    # 转换数据的并发数，默认为逻辑 CPU 数量，不需要配置。
    # 混合部署的情况下可以配置为逻辑 CPU 的 75% 大小。
    #region-concurrency =

    # 日志
    level = "info"
    file = "tidb-lightning.log"
    max-size = 128 # MB
    max-days = 28
    max-backups = 14

    [checkpoint]
    # 启用断点续传。
    # 导入时，Lightning 会记录当前进度。
    # 若 Lightning 或其他组件异常退出，在重启时可以避免重复再导入已完成的数据。
    enable = true
    # 存储断点的数据库名称。
    schema = "tidb_lightning_checkpoint"
    # 存储断点的数据库连接参数 (DSN)，格式为“用户:密码@tcp(地址:端口)/”。
    # 默认会重用 [tidb] 设置目标数据库来存储断点。
    # 为避免加重目标集群的压力，建议另外使用一个兼容 MySQL 协议的数据库服务器。
    # dsn = "root@tcp(127.0.0.1:4000)/"
    # 导入成功后是否保留断点。默认为删除。
    # 保留断点可用于调试，但有可能泄漏数据源的元数据。
    # keep-after-success = false

    [tikv-importer]
    # tikv-importer 的监听地址，需改成 tikv-importer 服务器的实际地址。
    addr = "172.16.31.10:20170"

    [mydumper]
    # 文件读取区块大小。
    read-block-size = 4096 # 字节 (默认 = 4 KB)
    # 每个文档在转换时会切分为多个 Chunk 并发处理，此为每个 Chunk 的大小。
    region-min-size = 268435456 # 字节 (默认 = 256 MB)
    # mydumper 源数据目录。
    data-source-dir = "/data/my_database"
    # 如果 no-schema 设置为 true，tidb-lightning 将直接去 tidb-server 获取表结构信息，
    # 而不是根据 data-source-dir 的 schema 文件来创建库/表，
    # 适用于手动创建表或者 TiDB 本来就有表结构的情况。
    no-schema = false

    [tidb]
    # 目标集群的信息。tidb-server 的监听地址，填一个即可。
    host = "172.16.31.1"
    port = 4000
    user = "root"
    password = ""
    # 表架构信息在从 TiDB 的“状态端口”获取。
    status-port = 10080
    # pd-server 的监听地址，填一个即可。
    pd-addr = "172.16.31.4:2379"
    # tidb-lightning 引用了 TiDB 库，而它自己会产生一些日志。此设置控制 TiDB 库的日志等级。
    log-level = "error"
    # 设置 TiDB 会话变量，提升 CHECKSUM 和 ANALYZE 的速度。
    distsql-scan-concurrency = 16

    # 导完数据以后可以自动进行校验和 (CHECKSUM)、压缩 (Compact) 和分析 (ANALYZE) 的操作。
    # 生产环境建议都设为 true
    # 执行顺序是: CHECKSUM -> Compact -> ANALYZE。
    [post-restore]
    # 如果设置为 true，会对每个表逐个做 `ADMIN CHECKSUM TABLE <table>` 操作。
    checksum = true
    # 如果设置为 true，会对所有数据做一次全量 Compact。
    compact = true
    # 如果设置为 true，会对每个表逐个做 `ANALYZE TABLE <table>` 操作。
    analyze = true
    ```

4. 运行 `tidb-lightning`。如果直接在命令行中用 `nohup` 启动程序，可能会因为 SIGHUP 信号而退出，建议把 `nohup` 放到脚本里面，如：

    ```sh
    #!/bin/bash
    nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```