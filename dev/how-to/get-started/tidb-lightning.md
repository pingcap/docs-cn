---
title: TiDB Lightning 教程
category: how-to
---

# TiDB Lightning 教程

TiDB Lightning 是一个将全量数据高速导入到 TiDB 集群的工具，有以下两个主要的使用场景：一是大量新数据的快速导入；二是全量数据的备份恢复。目前，支持 Mydumper 或 CSV 输出格式的数据源。您可以在以下两种场景下使用 Lightning：

- **迅速**导入**大量新**数据。
- 备份恢复所有数据。

TiDB Lightning 主要包含两个部分:

- **`tidb-lightning`**（“前端”）：主要完成适配工作，通过读取数据源，在下游 TiDB 集群建表、将数据转换成键/值对 (KV 对) 发送到 `tikv-importer`、检查数据完整性等。
- **`tikv-importer`**（“后端”）：主要完成将数据导入 TiKV 集群的工作，把 `tidb-lightning` 写入的 KV 对缓存、排序、切分并导入到 TiKV 集群。

![TiDB Lightning 其整体架构](/media/tidb-lightning-architecture.png)

本教程假设目前使用的是若干新的、纯净版 CentOS 7 实例，你能（使用 VMware、VirtualBox 及其他工具）在本地虚拟化或在供应商提供的平台上部署一台小型的云虚拟主机。因为 TiDB Lightning 对计算机资源消耗较高，建议内存在 4 GB 以上。

> **警告：**
>
> 本教程中的部署方法只适用于测试及功能体验，并不适用于生产或开发环境。

## 准备全量备份数据

我们使用 [`mydumper`](/dev/reference/tools/mydumper.md) 从 MySQL 导出数据，如下：

{{< copyable "shell-regular" >}}

```sh
./bin/mydumper -h 127.0.0.1 -P 3306 -u root -t 16 -F 256 -B test -T t1,t2 --skip-tz-utc -o /data/my_database/
```

其中：

- `-B test`：从 `test` 数据库导出。
- `-T t1,t2`：只导出 `t1` 和 `t2` 这两个表。
- `-t 16`：使用 16 个线程导出数据。
- `-F 256`：将每张表切分成多个文件，每个文件大小约为 256 MB。
- `--skip-tz-utc`：添加这个参数则会忽略掉 TiDB 与导数据的机器之间时区设置不一致的情况，禁止自动转换。

这样全量备份数据就导出到了 `/data/my_database` 目录中。

## TiDB Lightning 的部署

### 第 1 步：部署 TiDB 集群

在开始数据导入之前，需先部署一套要进行导入的 TiDB 集群 (版本要求 2.0.9 以上)，本教程使用 TiDB v3.0.4 版本。部署方法可参考 [TiDB 快速入门指南](/dev/overview.md#部署方式)。

### 第 2 步：下载 TiDB Lightning 安装包

通过以下链接获取 TiDB Lightning 安装包（选择与 TiDB 集群相同的版本）：

- **v3.0.4**: [https://download.pingcap.org/tidb-v3.0.4-linux-amd64.tar.gz](https://download.pingcap.org/tidb-v3.0.4-linux-amd64.tar.gz)

### 第 3 步：启动 `tikv-importer`

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

    {{< copyable "shell-regular" >}}

    ```sh
    nohup ./tikv-importer -C tikv-importer.toml > nohup.out &
    ```

### 第 4 步：启动 `tidb-lightning`

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

    {{< copyable "shell-regular" >}}

    ```sh
    #!/bin/bash
    nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```

### 第 5 步：检查数据

检查 checksum 是否一致，如果一致则数据成功导入。

## 总结

本教程对 TiDB Lightning 进行了简单的介绍，并快速部署一套简单的 TiDB Lightning 集群将全量备份数据进行导入到 TiDB 集群中。

对于 TiDB Lightning 的详细功能使用参见 [TiDB Lightning overwiew](/dev/reference/tools/tidb-lightning/overview.md)。