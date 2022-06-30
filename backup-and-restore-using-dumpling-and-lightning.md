---
title: 使用 Dumpling 和 TiDB Lightning 备份与恢复
summary: 了解如何使用 Dumpling 和 TiDB Lightning 备份与恢复集群数据。
---

# 使用 Dumpling 和 TiDB Lightning 备份与恢复

本文档介绍如何使用 Dumpling 和 TiDB Lightning 进行全量备份与恢复。

在备份恢复过程中，我们会使用 [Dumpling](/dumpling-overview.md) 从 TiDB 导出数据进行备份，然后使用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 导入数据至 TiDB 实现恢复。

## 前提条件

- [安装 Dumpling 和 TiDB Lightning。](/migration-tools.md)
- [获取 Dumpling 所需上游数据库权限。](/dumpling-overview.md#从-tidbmysql-导出数据)
- [获取 TiDB Lightning 所需下游数据库权限。](/tidb-lightning/tidb-lightning-requirements.md#下游数据库权限要求)

## 资源要求

**操作系统**：本文档示例使用的是若干新的、纯净版 CentOS 7 实例，你可以在本地虚拟化一台主机，或在供应商提供的平台上部署一台小型的云虚拟主机。TiDB Lightning 运行过程中，默认会占满 CPU，建议单独部署在一台主机上。如果条件不允许，你可以将 TiDB Lightning 和其他组件（比如 `tikv-server`）部署在同一台机器上，然后设置 `region-concurrency` 配置项的值为逻辑 CPU 数的 75%，以限制 TiDB Lightning 对 CPU 资源的使用。

**内存和 CPU**：因为 TiDB Lightning 对计算机资源消耗较高，建议分配 64 GB 以上的内存以及 32 核以上的 CPU，而且确保 CPU 核数和内存（GB）比为 1:2 以上，以获取最佳性能。

**磁盘空间**：

- Dumpling 需要能够储存整个数据源的存储空间，即可以容纳要导出的所有上游表的空间。计算方式参考[下游数据库所需空间](/tidb-lightning/tidb-lightning-requirements.md#下游数据库所需空间)。
- TiDB Lightning 导入期间，需要临时空间来存储排序键值对，磁盘空间需要至少能存储数据源的最大单表。
- 若全量数据量较大，可适当加长上游 binlog 保存时间，以避免增量同步时缺必要 binlog 导致重做。

**说明**：目前无法精确计算 Dumpling 从 TiDB 导出的数据大小，但你可以用下面 SQL 语句统计信息表的 `data_length` 字段估算数据量：

{{< copyable "" >}}

```sql
/* 统计所有 schema 大小，单位 MiB，注意修改 ${schema_name} */
SELECT table_schema,SUM(data_length)/1024/1024 AS data_length,SUM(index_length)/1024/1024 AS index_length,SUM(data_length+index_length)/1024/1024 AS SUM FROM information_schema.tables WHERE table_schema = "${schema_name}" GROUP BY table_schema;

/* 统计最大单表，单位 MiB，注意修改 ${schema_name} */
SELECT table_name,table_schema,SUM(data_length)/1024/1024 AS data_length,SUM(index_length)/1024/1024 AS index_length,SUM(data_length+index_length)/1024/1024 AS SUM from information_schema.tables WHERE table_schema = "${schema_name}" GROUP BY table_name,table_schema ORDER BY SUM DESC LIMIT 5;
```

### 目标 TiKV 集群的磁盘空间要求

目标 TiKV 集群必须有足够空间接收新导入的数据。除了[标准硬件配置](/hardware-and-software-requirements.md)以外，目标 TiKV 集群的总存储空间必须大于**数据源大小 × [副本数量](/faq/manage-cluster-faq.md#每个-region-的-replica-数量可配置吗调整的方法是) × 2**。例如，集群默认使用 3 副本，那么总存储空间需为数据源大小的 6 倍以上。公式中的 2 倍可能难以理解，其依据是以下因素的估算空间占用：

* 索引会占据额外的空间。
* RocksDB 的空间放大效应。

## 使用 Dumpling 备份全量数据

1. 运行以下命令，从 TiDB 导出全量数据：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup dumpling -h ${ip} -P 3306 -u root -t 16 -r 200000 -F 256MiB -B my_db1 -f 'my_db1.table[12]' -o 's3://my-bucket/sql-backup?region=us-west-2'
    ```

    Dumpling 默认导出数据格式为 SQL 文件，你也可以通过设置 `--filetype` 指定导出文件的类型。

    以上命令行中用到的参数描述如下。要了解更多 Dumpling 参数，请参考 [Dumpling 使用文档](/dumpling-overview.md)。

    | 参数               | 说明 |
    | -                  | - |
    | `-u` 或 `--user`       | MySQL 数据库的用户 |
    | `-p` 或 `--password`   | MySQL 数据库的用户密码 |
    | `-P` 或 `--port`       | MySQL 数据库的端口 |
    | `-h` 或 `--host`       | MySQL 数据库的 IP 地址 |
    | `-t` 或 `--thread`     | 导出的线程数。增加线程数会增加 Dumpling 并发度提高导出速度，但也会加大数据库内存消耗，因此不宜设置过大，一般不超过 64 |
    | `-o` 或 `--output`     | 存储导出文件的目录，支持本地文件路径或[外部存储 URL 格式](/br/backup-and-restore-storages.md) |
    | `-r` 或 `--row`        | 用于指定单个文件的最大行数，指定该参数后 Dumpling 会开启表内并发加速导出，同时减少内存使用 |
    | `-F`                   | 指定单个文件的最大大小，单位为 MiB。强烈建议使用 `-F` 参数以避免单表过大导致备份过程中断 |
    | `-B` 或 `--database`   | 导出指定数据库 |
    | `-f` 或 `--filter`     | 导出能匹配模式的表，语法可参考 [table-filter](/table-filter.md)|

    请确保 `${data-path}` 的空间可以容纳要导出的所有上游表，计算方式参考[下游数据库所需空间](/tidb-lightning/tidb-lightning-requirements.md#下游数据库所需空间)。强烈建议使用 `-F` 参数以避免单表过大导致备份过程中断。

2. 导出完成后，可以在数据存储目录查看导出的备份文件。

## 使用 TiDB Lightning 恢复全量数据

1. 编写配置文件 `tidb-lightning.toml`：

    {{< copyable "" >}}

    ```toml
    [lightning]
    # 日志
    level = "info"
    file = "tidb-lightning.log"

    [tikv-importer]
    # "local"：默认使用该模式，适用于 TB 级以上大数据量，但导入期间下游 TiDB 无法对外提供服务。
    # "tidb"：TB 级以下数据量也可以采用`tidb`后端模式，下游 TiDB 可正常提供服务。 关于后端模式更多信息请参阅：https://docs.pingcap.com/tidb/stable/tidb-lightning-backends
    backend = "local"
    # 设置排序的键值对的临时存放地址，目标路径必须是一个空目录，目录空间须大于待导入数据集的大小。建议设为与 `data-source-dir` 不同的磁盘目录并使用闪存介质，独占 IO 会获得更好的导入性能
    sorted-kv-dir = "${sorted-kv-dir}"

    [mydumper]
    # 源数据目录，即上一章节中 Dumpling 保存数据的路径。
    data-source-dir = "${data-path}" # 本地或 S3 路径，例如：'s3://my-bucket/sql-backup?region=us-west-2'

    [tidb]
    # 目标集群的信息
    host = ${host}                # 例如：172.16.32.1
    port = ${port}                # 例如：4000
    user = "${user_name}"         # 例如："root"
    password = "${password}"      # 例如："rootroot"
    status-port = ${status-port}  # 导入过程 Lightning 需要在从 TiDB 的“状态端口”获取表结构信息，例如：10080
    pd-addr = "${ip}:${port}"     # 集群 PD 的地址，Lightning 通过 PD 获取部分信息，例如 172.16.31.3:2379。当 backend = "local" 时 status-port 和 pd-addr 必须正确填写，否则导入将出现异常。
    ```

    关于更多 TiDB Lightning 的配置，请参考 [TiDB Lightning 配置参数](/tidb-lightning/tidb-lightning-configuration.md)。

2. 运行 `tidb-lightning`。如果直接在命令行中启动程序，可能会因为 `SIGHUP` 信号而退出，建议配合 `nohup` 或 `screen` 等工具，如：

    若从 S3 导入，则需将有权限访问该 Amazon S3 后端存储的账号的 SecretKey 和 AccessKey 作为环境变量传入 Lightning 节点。同时还支持从 `~/.aws/credentials` 读取凭证文件。

    {{< copyable "shell-regular" >}}

    ```shell
    export AWS_ACCESS_KEY_ID=${access_key}
    export AWS_SECRET_ACCESS_KEY=${secret_key}
    nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out 2>&1 &
    ```

3. 导入开始后，可以采用以下任意方式查看进度：

   - 通过 `grep` 日志关键字 `progress` 查看进度，默认 5 分钟更新一次。
   - 通过监控面板查看进度，请参考 [TiDB Lightning 监控](/tidb-lightning/monitor-tidb-lightning.md)。
   - 通过 Web 页面查看进度，请参考 [Web 界面](/tidb-lightning/tidb-lightning-web-interface.md)。

4. 导入完毕后，TiDB Lightning 会自动退出。查看日志的最后 5 行中会有 `the whole procedure completed`，此时，数据导入成功，恢复完成。

> **注意：**
>
> 无论导入成功与否，最后一行都会显示 `tidb lightning exit`。它只是表示 TiDB Lightning 正常退出，不代表恢复任务完成。

如果恢复过程中遇到问题，请参见 [TiDB Lightning 常见问题](/tidb-lightning/tidb-lightning-faq.md)。
