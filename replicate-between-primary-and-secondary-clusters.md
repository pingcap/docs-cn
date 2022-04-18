---
title: 搭建双集群主从复制
summary: 了解如何配置一个 TiDB 集群以及该集群的 TiDB 或 MySQL 从集群，并将增量数据实时从主集群同步到从集群，
---

# 搭建双集群主从复制

本文档介绍如何配置一个 TiDB 集群以及该集群的 TiDB 或 MySQL 从集群，并将增量数据实时从主集群同步到从集群，主要包含以下内容：

* 配置一个 TiDB 集群以及该集群的 TiDB 或 MySQL 从集群。
* 将增量数据实时从主集群同步到从集群。
* 在主集群发生灾难利用 Redo log 恢复一致性数据。

如果你需要配置一个运行中的 TiDB 集群和其从集群，以进行实时增量数据同步，可使用 [Backup & Restore (BR)](/BR/backup-and-restore-tool.md) 和 [TiCDC](/ticdc/ticdc-overview.md)。

## 第 1 步：搭建环境

1. 部署集群。

    使用 tiup playground 快速部署 TiDB 上下游测试集群。生产环境可以参考 [tiup 官方文档](/tiup/tiup-cluster.md)根据业务需求来部署集群。

    为了方便展示和理解，我们简化部署结构，需要以下准备两台机器，分别来部署上游主集群，下游从集群。假设 IP 地址分别为:

    - NodeA: `172.16.6.123`，部署上游 TiDB

    - NodeB: `172.16.6.124`，部署下游 TiDB

    {{< copyable "shell-regular" >}}

    ```shell

    # 在 NodeA 上创建上游集群
    tiup --tag upstream playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    # 在 NodeB 上创建下游集群
    tiup --tag downstream playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 0
    # 查看集群状态
    tiup status
    ```

2. 初始化数据。

    测试集群中默认创建了 test 数据库，因此可以使用 sysbench 工具生成测试数据，用以模拟真实集群中的历史数据。

    {{< copyable "shell-regular" >}}

    ```shell
    sysbench oltp_write_only --config-file=./tidb-config --tables=10 --table-size=10000 prepare
    ```

    这里通过 [sysbench](https://github.com/akopytov/sysbench#linux) 运行 oltp_write_only 脚本，其将在测试数据库中生成 10 张表 ，每张表包含 1w 行初始数据。tidb-config 的配置如下：

    {{< copyable "shell-regular" >}}

    ```shell
    mysql-host=172.16.6.122 # 这里需要替换为实际上游集群 ip
    mysql-port=4000
    mysql-user=root
    mysql-password=
    db-driver=mysql         # 设置数据库驱动为 mysql
    mysql-db=test           # 设置测试数据库为 test
    report-interval=10      # 设置定期统计的时间间隔为 10 秒
    threads=10              # 设置 worker 线程数量为 10
    time=0                  # 设置脚本总执行时间，0 表示不限制
    rate=100                # 设置平均事务速率 tps = 100
    ```

3. 模拟业务负载。

    实际生产集群的数据迁移过程中，通常原集群还会写入新的业务数据，本文中可以通过 sysbench 工具模拟持续的写入负载，下面的命令会使用 10 个 worker 在数据库中的 sbtest1、sbtest2 和 sbtest3 三张表中持续写入数据，其总 tps 限制为 100。

    {{< copyable "shell-regular" >}}

    ```shell
    sysbench oltp_write_only --config-file=./tidb-config --tables=3 run
    ```

4. 准备外部存储。

    在全量数据备份中，上下游集群均需访问备份文件，因此推荐使用[外部存储](/br/backup-and-restore-storages.md)存储备份文件，本文中通过 Minio 模拟兼容 S3 的存储服务：

    {{< copyable "shell-regular" >}}

    ```shell
    wget https://dl.min.io/server/minio/release/linux-amd64/minio
    chmod +x minio
    # 配置访问 minio 的 access-key access-secret-id
    export `HOST_IP`='172.16.6.123' # 替换为实际部署 minio 的机器 ip
    export** **MINIO_ROOT_USER**='**minio'
    export MINIO_ROOT_PASSWORD='miniostorage'
    # 创建 redo 和 backup 数据目录,  其中 redo, backup 为 bucket 名字
    mkdir -p data/redo
    mkdir -p data/backup
    # 启动 minio, 暴露端口在 6060
    nohup ./minio server ./data --address :6060 &
    ```

    上述命令行启动了一个单节点的 minio server 模拟 S3 服务，其相关参数为：

    * Endpoint : `http://${HOST_IP}:6060/`
    * Access-key : `minio`
    * Secret-access-key: `miniostorage`
    * Bucket: `redo`

    其访问链接为如下:

    {{< copyable "shell-regular" >}}

    ```shell
    s3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true
    ```

## 第 2 步：迁移全量数据

搭建好测试环境后，可以使用 [BR](https://github.com/pingcap/br) 工具的备份和恢复功能迁移全量数据。BR 工具有多种[使用方式](/br/backup-and-restore-tool.md#使用方式)，本文中使用 SQL 语句 [`BACKUP`](/sql-statements/sql-statement-backup.md) 和 [`RESTORE`](/sql-statements/sql-statement-restore.md) 进行备份恢复。

> **注意：**
>
> 上下游集群版本不一致时，应检查 BR 工具的[兼容性](/br/backup-and-restore-tool.md#兼容性)。本文假设上下游集群版本相同。

1. 关闭 GC。

    为了保证增量迁移过程中新写入的数据不丢失，在开始备份之前，需要关闭上游集群的垃圾回收 (GC) 机制，以确保系统不再清理历史数据。

    {{< copyable "sql" >}}

    ```sql
    MySQL [test]> SET GLOBAL tidb_gc_enable=FALSE;
    Query OK, 0 rows affected (0.01 sec)
    MySQL [test]> SELECT @@global.tidb_gc_enable;
    +-------------------------+
    | @@global.tidb_gc_enable |
    +-------------------------+
    |                       0 |
    +-------------------------+
    1 row in set (0.00 sec)

    > **注意：**
    >
    > 在生产集群中，关闭 GC 机制和备份操作会一定程度上降低集群的读性能，建议在业务低峰期进行备份，并设置合适的 RATE_LIMIT 限制备份操作对线上业务的影响。

2. 备份数据。

    在上游集群中执行 BACKUP 语句备份数据：

    {{< copyable "sql" >}}

    ```sql
    MySQL [(none)]> BACKUP DATABASE * TO '`s3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true`' RATE_LIMIT = 120 MB/SECOND;
    +----------------------+----------+--------------------+---------------------+---------------------+
    | Destination          | Size     | BackupTS           | Queue Time          | Execution Time      |
    +----------------------+----------+--------------------+---------------------+---------------------+
    | local:///tmp/backup/ | 10315858 | 431434047157698561 | 2022-02-25 19:57:59 | 2022-02-25 19:57:59 |

    +----------------------+----------+--------------------+---------------------+---------------------+

    1 row in set (2.11 sec)
    ```

    备份语句提交成功后，TiDB 会返回关于备份数据的元信息，这里需要重点关注 BackupTS，它意味着该时间点之前数据会被备份，后边的教程中，本文将使用 BackupTS 作为**数据校验截止时间**和 **TiCDC 增量扫描的开始时间**。

3. 恢复数据。

    在下游集群中执行 RESTORE 语句恢复数据：

    {{< copyable "sql" >}}

    ```sql
    mysql> RESTORE DATABASE * FROM '`s3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true`';
    +----------------------+----------+--------------------+---------------------+---------------------+
    | Destination          | Size     | BackupTS           | Queue Time          | Execution Time      |
    +----------------------+----------+--------------------+---------------------+---------------------+
    | local:///tmp/backup/ | 10315858 | 431434141450371074 | 2022-02-25 20:03:59 | 2022-02-25 20:03:59 |
    +----------------------+----------+--------------------+---------------------+---------------------+
    1 row in set (41.85 sec)
    ```

4. （可选）校验数据。

    通过 [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) 工具，可以验证上下游数据在某个时间点的一致性。从上述备份和恢复命令的输出可以看到，上游集群备份的时间点为 431434047157698561，下游集群完成数据恢复的时间点为 431434141450371074。

    {{< copyable "shell-regular" >}}

    ```shell
    sync_diff_inspector -C ./config.yaml
    ```

    关于 sync-diff-inspector 的配置方法，请参考[配置文件说明](/sync-diff-inspector/sync-diff-inspector-overview.md#配置文件说明)，在本文中，相应的配置为：

    {{< copyable "shell-regular" >}}

    ```shell
    # Diff Configuration.
    ######################### Global config #########################
    check-thread-count = 4
    export-fix-sql = true
    check-struct-only = false

    {{< copyable "shell-regular" >}}

    ```shell
    ######################### Datasource config #########################
    [data-sources]
    [data-sources.upstream]
        host = "172.16.6.123" # 替换为实际上游集群 ip
        port = 4000
        user = "root"
        password = ""
        snapshot = "431434047157698561" # 配置为实际的备份时间点
    [data-sources.downstream]
        host = "172.16.6.124" # 替换为实际下游集群 ip
        port = 4000
        user = "root"
        password = ""
        snapshot = "431434141450371074" # 配置为实际的恢复时间点

    ######################### Task config #########################
    [task]
        output-dir = "./output"
        source-instances = ["upstream"]
        target-instance = "downstream"
        target-check-tables = ["*.*"]
    ```

## 第 3 步：迁移增量数据

1. 部署 TiCDC。

    完成全量数据迁移后，就可以部署并配置 TiCDC 集群同步增量数据，实际生产集群中请参考 [TiCDC 部署](/ticdc/deploy-ticdc.md)。本文在创建测试集群时，已经启动了一个 TiCDC 节点，因此可以直接进行 changefeed 的配置。

2. 创建同步任务。

    创建 Changefeed 配置文件并保存为 changefeed.toml。

    {{< copyable "toml" >}}

    ```toml
    [consistent]
    # 一致性级别，配置成 eventual 表示开启一致性复制
    level = "eventual"
    # 使用 s3 来存储 redo log, 其他可选为 local, nfs
    storage = "s3://redo?access-key=minio&secret-access-key=miniostorage&endpoint=http://172.16.6.125:6060&force-path-style=true"
    ```

    在上游集群中，执行以下命令创建从上游到下游集群的同步链路：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cdc  cli changefeed --sink-url "mysql://root:@172.16.6.124:4000" --config ./changefeed.toml
    ```

    以上命令中：

   * --pd: 实际的上游集群的地址
   * --sink-uri：同步任务下游的地址
   * --start-ts: TiCDC 同步的起点，需要设置为实际的备份时间点（也就是第二章「备份」小节提到的 BackupTS）

    更多关于 changefeed 的配置，请参考[同步任务配置文件描述](/ticdc/manage-ticdc.md#同步任务配置文件描述)。

3. 重新开启 GC。

    TiCDC 可以保证未同步的历史数据不会被回收。因此，创建完从上游到下游集群的 changefeed 之后，就可以执行如下命令恢复集群的垃圾回收功能。详情请参考 [TiCDC GC safepoint 的完整行为](/ticdc/troubleshoot-ticdc.md#ticdc-gc-safepoint-的完整行为是什么)。

    {{< copyable "sql" >}}

    ```sql
    MySQL [test]> SET GLOBAL tidb_gc_enable=TRUE;
    Query OK, 0 rows affected (0.01 sec)
    MySQL [test]> SELECT @@global.tidb_gc_enable;
    +-------------------------+
    | @@global.tidb_gc_enable |
    +-------------------------+
    |                       1 |
    +-------------------------+
    1 row in set (0.00 sec)
    ```

## 第 4 步：模拟主集群故障

模拟在业务过程中上游 TiDB 发生灾难性故障无法再启动起来，这里可以直接使用 Ctrl + C 终止 tiup playground 进程。

## 第 5 步：使用 redo log 确保数据一致性

在正常同步过程中，为了提高 TiCDC 的吞吐能力，TiCDC 会将事务并行写入下游。因此，当 TiCDC 同步链路意外中断时，下游可能不会恰好停在与上游一致的状态。我们这里需要使用 TiCDC 的命令行工具来向下游重放 redo log，使下游达到最终一致性状态。

{{< copyable "shell-regular" >}}

```shell
tiup cdc redo apply --storage "s3://redo?access-key=minio&secret-access-key=miniostorage&endpoint=http://172.16.6.123:6060&force-path-style=true" --tmp-dir /tmp/redo --sink-uri "mysql://root:@172.16.6.124:4000"
```

- `--storage`：指定 redo log 所在的 s3 位置以及 credential
- `--tmp-dir`：为从 s3 下载 redo log 的缓存目录
- `--sink-uri`：指定下游集群的地址

## 第 6 步：恢复主集群及业务

现在从集群有了某一时刻全部的一致性数据，你需要重新搭建主从集群来保证数据可靠性。

1. 在 NodeA 重新搭建一个新的 TiDB 集群作为新的主集群。

    {{< copyable "shell-regular" >}}

    ```shell
    tiup --tag upstream playground v5.4.0 --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    ```

2. 使用 BR 将从集群数据全量备份恢复到主集群。

    {{< copyable "shell-regular" >}}

    ```shell
    # 全量备份从集群的数据
    tiup br --pd http://172.16.6.124:2379 backup full --storage ./backup
    # 全量恢复从集群的数据
    tiup br --pd http://172.16.6.123:2379 restore full --storage ./backup
    ```

3. 创建一个 TiCDC 同步任务，备份主集群数据到从集群。

    {{< copyable "shell-regular" >}}

    ```shell
    # 创建 changefeed
    tiup cdc cli changefeed --sink-url "mysql://root:@172.16.6.124:4000" --config ./changefeed.toml
    ```
