---
title: TiDB Lightning 部署与执行
category: reference
aliases: ['/docs-cn/tools/lightning/deployment/']
---

# TiDB Lightning 部署与执行

本文主要介绍 TiDB Lightning 单独部署与混合部署的硬件需求，Ansible 部署与手动部署这两种部署方式，以及启动与执行。

## 注意事项

在使用 TiDB Lightning 前，需注意以下事项：

- TiDB Lightning 运行后，TiDB 集群将无法正常对外提供服务。
- 若 `tidb-lightning` 崩溃，集群会留在“导入模式”。若忘记转回“普通模式”，集群会产生大量未压缩的文件，继而消耗 CPU 并导致迟延 (stall)。此时，需要使用 `tidb-lightning-ctl` 手动将集群转回“普通模式”：

    ```sh
    bin/tidb-lightning-ctl -switch-mode=normal
    ```

- TiDB Lightning 需要下游 TiDB 的权限：

    | 权限 | 作用域 |
    |----:|:------|
    | SELECT | Tables |
    | INSERT | Tables |
    | UPDATE | Tables |
    | DELETE | Tables |
    | CREATE | Databases, tables |
    | DROP | Databases, tables |
    | ALTER | Tables |
  
  如果 TiDB Lightning 配置项 `checksum = true`，则 TiDB Lightning 需要有下游 TiDB admin 用户权限。

## 硬件需求

`tidb-lightning` 和 `tikv-importer` 这两个组件皆为资源密集程序，建议各自单独部署。

为了优化效能，建议硬件配置如下：

- `tidb-lightning`

    - 32+ 逻辑核 CPU
    - 足够储存整个数据源的 SSD 硬盘，读取速度越快越好
    - 使用万兆网卡，带宽需 300 MB/s 以上
    - 运行过程默认会打满 CPU，建议单独部署。条件不允许的情况下可以和其他组件 (比如 `tidb-server`) 部署在同一台机器上，然后通过配置 `region-concurrency` 限制 `tidb-lightning` 的 CPU 使用。

- `tikv-importer`

    - 32+ 逻辑核 CPU
    - 40 GB+ 内存
    - 1 TB+ SSD 硬盘，IOPS 越高越好（要求 ≥8000）
        * 硬盘必须大于最大的 N 个表的大小总和，其中 N = max(index-concurrency, table-concurrency)。
    - 使用万兆网卡，带宽需 300 MB/s 以上
    - 运行过程中 CPU、I/O 和网络带宽都可能打满，建议单独部署。

如果机器充裕的话，可以部署多套 `tidb-lightning` + `tikv-importer`，然后将源数据以表为粒度进行切分，并发导入。

> **注意：**
>
> - `tidb-lightning` 是 CPU 密集型程序，如果和其它程序混合部署，需要通过 `region-concurrency` 限制 `tidb-lightning` 的 CPU 实际占用核数，否则会影响其他程序的正常运行。建议将混合部署机器上 75% 的 CPU 分配给 `tidb-lightning`。例如，机器为 32 核，则 `tidb-lightning` 的 `region-concurrency` 可设为 24。
>
> - `tikv-importer` 将中间数据存储缓存到内存上以加速导入过程。占用内存大小可以通过 **(`max-open-engines` × `write-buffer-size` × 2) + (`num-import-jobs` × `region-split-size` × 2)** 计算得来。如果磁盘写入速度慢，缓存可能会带来更大的内存占用。

此外，目标 TiKV 集群必须有足够空间接收新导入的数据。除了[标准硬件配置](/how-to/deploy/hardware-recommendations.md)以外，目标 TiKV 集群的总存储空间必须大于 **数据源大小 × [副本数量](/faq/tidb.md#3-2-6-每个-region-的-replica-数量可配置吗-调整的方法是) × 2**。例如集群默认使用 3 副本，那么总存储空间需为数据源大小的 6 倍以上。

## 导出数据

我们使用 [`mydumper`](/reference/tools/mydumper.md) 从 MySQL 导出数据，如下：

```sh
./bin/mydumper -h 127.0.0.1 -P 3306 -u root -t 16 -F 256 -B test -T t1,t2 --skip-tz-utc -o /data/my_database/
```

其中：

- `-B test`：从 `test` 数据库导出。
- `-T t1,t2`：只导出 `t1` 和 `t2` 这两个表。
- `-t 16`：使用 16 个线程导出数据。
- `-F 256`：将每张表切分成多个文件，每个文件大小约为 256 MB。
- `--skip-tz-utc`：添加这个参数则会忽略掉 TiDB 与导数据的机器之间时区设置不一致的情况，禁止自动转换。

如果数据源是 CSV 文件，请参考 [CSV 支持](/reference/tools/tidb-lightning/csv.md)获取配置信息。

## 部署 TiDB Lightning

本节介绍 TiDB Lightning 的两种部署方式：[使用 Ansible 部署](#使用-ansible-部署-tidb-lightning)和[手动部署](#手动部署-tidb-lightning)。

### 使用 Ansible 部署 TiDB Lightning

TiDB Lightning 可随 TiDB 集群一起用 [Ansible 部署](/how-to/deploy/orchestrated/ansible.md)。

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
        tikv_importer_port: 8287
        ...
        ```

    - `group_vars/lightning_server.yml`

        ```yaml
        ---
        dummy:

        # 提供监控告警的端口。需对监控服务器 (monitoring_server) 开放。
        tidb_lightning_pprof_port: 8289

        # 获取数据源（Mydumper SQL dump 或 CSV）的路径。
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

### 手动部署 TiDB Lightning

#### 第 1 步：部署 TiDB 集群

在开始数据导入之前，需先部署一套要进行导入的 TiDB 集群 (版本要求 2.0.9 以上)，建议使用最新版。部署方法可参考 [TiDB 快速入门指南](/overview.md#部署方式)。

#### 第 2 步：下载 TiDB Lightning 安装包

通过以下链接获取 TiDB Lightning 安装包（需选择与集群相同的版本）：

- **v2.1.9**: `https://download.pingcap.org/tidb-v2.1.9-linux-amd64.tar.gz`
- **v2.0.9**: `https://download.pingcap.org/tidb-lightning-v2.0.9-linux-amd64.tar.gz`
- 最新 unstable 版本：`https://download.pingcap.org/tidb-lightning-test-xx-latest-linux-amd64.tar.gz`

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
    addr = "0.0.0.0:8287"
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
    compression-per-level = ["lz4", "no", "no", "no", "no", "no", "lz4"]

    [rocksdb.writecf]
    # (同上)
    compression-per-level = ["lz4", "no", "no", "no", "no", "no", "lz4"]

    [import]
    # 存储引擎文档 (engine file) 的文件夹路径。
    import-dir = "/mnt/ssd/data.import/"
    # 处理 gRPC 请求的线程数量。
    num-threads = 16
    # 导入任务并发数。
    num-import-jobs = 24
    # 预处理 Region 最长时间。
    # max-prepare-duration = "5m"
    # 把要导入的数据切分为这个大小的 Region。
    # region-split-size = "512MB"
    # 流管道窗口大小，管道满时会阻塞流。
    # stream-channel-window = 128
    # 引擎文档同时打开的最大数量。
    max-open-engines = 8
    # Importer 上传至 TiKV 的最大速度 (bytes per second)。
    # upload-speed-limit = "512MB"
    # 目标 store 可用空间的最小比率：store_available_space / store_capacity.
    # 如果目标存储空间的可用比率低于下值，Importer 将会暂停上传 SST 来为 PD 提供足够时间进行 regions 负载均衡。
    min-available-ratio = 0.05
    ```

3. 运行 `tikv-importer`。

    ```sh
    nohup ./tikv-importer -C tikv-importer.toml > nohup.out &
    ```

#### 第 4 步：启动 `tidb-lightning`

1. 从安装包上传 `bin/tidb-lightning` 及 `bin/tidb-lightning-ctl`。

2. 将数据源写入到同样的机器。

3. 配置 `tidb-lightning.toml`。对于没有出现在下述模版中的配置，TiDB Lightning 给出配置错误的提醒并退出。

    ```toml
    # TiDB Lightning 配置文件模版

    [lightning]
    # 用于调试和 Prometheus 监控的 HTTP 端口。输入 0 关闭。
    pprof-port = 8289

    # 开始导入前先检查集群版本是否支持。
    # check-requirements = true

    # 控制同时处理的最大引擎数量。
    # 每张表被分割为一个用于储存索引的“索引引擎”和若干存储行数据的“数据引擎”。
    # 这两项设置控制同时处理每种引擎的最大数量。设置会影响 tikv-importer 的内存和
    # 磁盘用量。两项数值之和不能超过 tikv-importer 的 max-open-engines 的设定。
    index-concurrency = 2
    table-concurrency = 6

    # 转换数据的并发数，默认为逻辑 CPU 数量，不需要配置。
    # 混合部署的情况下可以配置为逻辑 CPU 的 75% 大小。
    # region-concurrency =

    # 最大的 I/O 并发数。I/O 并发量太高时，会因硬盘内部缓存频繁被刷新而增加 I/O 等待时间，
    # 导致缓存未命中和降低读取速度。因应不同的存储介质，此参数可能需要调整以达到最佳效率。
    io-concurrency = 5

    # 日志
    level = "info"
    file = "tidb-lightning.log"
    max-size = 128 # MB
    max-days = 28 # 默认不删除旧日志
    max-backups = 14

    # Server 模式
    # 是否启用 Server 模式
    # server-mode = false
    # Server 模式下的监听地址
    # status-addr = ":8289"

    [checkpoint]
    # 启用断点续传。
    # 导入时，Lightning 会记录当前进度。
    # 若 Lightning 或其他组件异常退出，在重启时可以避免重复再导入已完成的数据。
    enable = true
    # 存储断点的数据库名称。
    schema = "tidb_lightning_checkpoint"
    # 存储断点的方式
    #  - file：存放在本地文件系统（要求 v2.1.1 或以上）
    #  - mysql：存放在兼容 MySQL 的数据库服务器
    driver = "file"
    # 断点的存放位置
    # 若 driver = "file"，此参数为断点信息存放的文件路径。
    # 如果不设置改参数则默认为“/tmp/CHECKPOINT_SCHEMA.pb”。
    # 若 driver = "mysql"，此参数为数据库连接参数 (DSN)，格式为“用户:密码@tcp(地址:端口)/”。
    # 默认会重用 [tidb] 设置目标数据库来存储断点。
    # 为避免加重目标集群的压力，建议另外使用一个兼容 MySQL 的数据库服务器。
    # dsn = "/tmp/tidb_lightning_checkpoint.pb"
    # 导入成功后是否保留断点。默认为删除。
    # 保留断点可用于调试，但有可能泄漏数据源的元数据。
    # keep-after-success = false

    [tikv-importer]
    # tikv-importer 的监听地址，需改成 tikv-importer 服务器的实际地址。
    addr = "172.16.31.10:8287"

    [mydumper]
    # 文件读取区块大小。
    read-block-size = 65536 # 字节 (默认 = 64 KB)

    #（源数据文件）单个导入区块大小的最小值。
    # Lightning 根据该大小将一张大表分割为多个数据引擎文件。
    batch-size = 107_374_182_400 # 字节 (默认 100 GiB)
    # 引擎文件要按序导入。因为是并行处理，多个数据引擎几乎同时被导入，
    # 这样形成的处理队列会造成资源浪费。因此，Lightning 稍微增大了前几个
    # 区块的大小，从而合理分配资源。该参数也决定了向上扩展（scale up）因
    # 数，代表在完全并发下“导入”和“写入”过程的持续时间比。这个值也可以通过
    # 计算 1 GB 大小单张表的（导入时长/写入时长）得到。精确的时间可以在日志
    # 里看到。如果“导入”更快，区块大小差异就会更小；比值为 0 则说明区块大小
    # 是一致的。取值范围是（0 <= batch-import-ratio < 1）。
    batch-import-ratio = 0.75

    # Mydumper 源数据目录。
    data-source-dir = "/data/my_database"
    # 如果 no-schema 设置为 true，tidb-lightning 将直接去 tidb-server 获取表结构信息，
    # 而不是根据 data-source-dir 的 schema 文件来创建库/表，
    # 适用于手动创建表或者 TiDB 本来就有表结构的情况。
    no-schema = false
    # 指定包含 CREATE TABLE 语句的表结构文件的字符集。只支持下列选项：
    #  - utf8mb4：表结构文件必须使用 UTF-8 编码，否则 Lightning 会报错
    #  - gb18030：表结构文件必须使用 GB-18030 编码，否则 Lightning 会报错
    #  - auto：（默认）自动判断文件编码是 UTF-8 还是 GB-18030，两者皆非则会报错
    #  - binary：不尝试转换编码
    # 注意，此参数不影响 Lightning 读取数据文件。
    character-set = "auto"
    # 是否区分大小写
    # case-sensitive = false

    # 配置如何解析 CSV 文件。
    [mydumper.csv]
    # 字段分隔符，应为单个 ASCII 字符。
    separator = ','
    # 引用定界符，可为单个 ASCII 字符或空字符串。
    delimiter = '"'
    # CSV 文件是否包含表头。
    # 如果为 true，第一行导入时会被跳过。
    header = true
    # CSV 是否包含 NULL。
    # 如果 `not-null` 为 true，CSV 所有列都不能解析为 NULL。
    not-null = false
    # 如果 `not-null` 为 false（即 CSV 可以包含 NULL），
    # 为以下值的字段将会被解析为 NULL。
    null = '\N'
    # 是否解析字段内反斜线转义符。
    backslash-escape = true
    # 如果有行以分隔符结尾，删除尾部分隔符。
    trim-last-separator = false

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
    # MySQL SQL Mode 配置
    # sql-mode = ""

    # 设置 TiDB 会话变量，提升 CHECKSUM 和 ANALYZE 的速度。各参数定义可参阅
    # https://pingcap.com/docs-cn/sql/statistics/#%E6%8E%A7%E5%88%B6-analyze-%E5%B9%B6%E5%8F%91%E5%BA%A6
    build-stats-concurrency = 20
    distsql-scan-concurrency = 100
    index-serial-scan-concurrency = 20
    checksum-table-concurrency = 16

    # 导完数据以后可以自动进行校验和 (CHECKSUM)、压缩 (Compact) 和分析 (ANALYZE) 的操作。
    # 生产环境建议都设为 true
    # 执行顺序是: CHECKSUM -> ANALYZE。
    [post-restore]
    # 如果设置为 true，会对每个表逐个做 `ADMIN CHECKSUM TABLE <table>` 操作。
    checksum = true
    # 如果设置为 true，会在导入每张表后做一次 level-1 Compact。
    # 如果不填写，则默认为 false。
    level-1-compact = false
    # 如果设置为 true，会在导入过程结束时对整个 TiKV 集群执行一次全量 Compact。
    # 如果不填写，则默认为 false。
    compact = false
    # 如果设置为 true，会对每个表逐个做 `ANALYZE TABLE <table>` 操作。
    analyze = true

    # 设置背景周期性动作。
    # 支持的单位：h（时）、m（分）、s（秒）。
    [cron]
    # Lightning 自动刷新导入模式周期。需要比 TiKV 对应的设定值短。
    switch-mode = "5m"
    # 每经过这段时间，在日志打印当前进度。
    log-progress = "5m"

    # 表库过滤设置。详情见《TiDB Lightning 表库过滤》。
    #[black-white-list]
    # ...

    ```

4. 运行 `tidb-lightning`。如果直接在命令行中用 `nohup` 启动程序，可能会因为 SIGHUP 信号而退出，建议把 `nohup` 放到脚本里面，如：

    ```sh
    #!/bin/bash
    nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```
