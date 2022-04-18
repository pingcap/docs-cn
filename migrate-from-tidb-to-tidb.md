---
title: 从 TiDB 集群迁移至另一 TiDB 集群
summary: 了解如何将数据从一个 TiDB 集群迁移至另一 TiDB 集群。
aliases: ['zh/tidb/dev/incremental-replication-between-clusters']
---

# 从 TiDB 集群迁移数据至另一 TiDB 集群

本文档介绍如何将数据从一个 TiDB 集群迁移至另一 TiDB。在如下场景中，你可以将数据从一个 TiDB 集群迁移至另一个 TiDB 集群：

- 拆库：原 TiDB 集群体量过大，或者为了避免原有的 TiDB 集群所承载的数个业务之间互相影响，将原 TiDB 集群中的部分表迁到另一个 TiDB 集群。
- 迁库：是对数据库的物理位置进行迁移，比如更换数据中心。
- 升级：在对数据正确性要求严苛的场景下，可以将数据迁移到一个更高版本的 TiDB 集群，确保数据安全。

本文将模拟整个迁移过程，具体包括以下四个步骤：

1. 搭建环境
2. 迁移全量数据
3. 迁移增量数据
4. 平滑切换业务

## 第 1 步：搭建环境

1. 部署集群。

    使用 tiup playground 快速部署 5.4.0 上下游测试集群。更多部署信息，请参考 [tiup 官方文档](//tiup/tiup-cluster.md)。

    {{< copyable "shell-regular" >}}

    ```shell
    # 创建上游集群
    tiup --tag upstream playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    # 创建下游集群
    tiup --tag downstream playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
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
    # 配置访问 minio 的 access-key access-screct-id
    export HOST_IP='172.16.6.122' # 替换为实际上游集群 ip
    export MINIO_ROOT_USER='minio'
    export MINIO_ROOT_PASSWORD='miniostorage'
    # 创建数据目录,  其中 backup 为 bucket 的名称
    mkdir -p data/backup
    # 启动 minio, 暴露端口在 6060
    ./minio server ./data --address :6060 &
    ```

    上述的命令行启动了一个单节点的 minio server 模拟 s3 服务，其相关参数为：

     - Endpoint: "http://${HOST_IP}:6060/"
     - Access-key: minio
     - Secret-access-key: miniostorage
     - Bucket: backup

    相应的访问链接为：

    {{< copyable "shell-regular" >}}

    ```shell
    s3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true
    ```

## 第 2 步：迁移全量数据

搭建好测试环境后，开始迁移数据。如果之前没有迁移过数据，则需要先进行全量迁移，再根据需要迁移增量数据。

全量迁移可以使用 [BR](https://github.com/pingcap/br) 工具的备份和恢复功能。BR 全称为 Backup & Restore，是 TiDB 分布式备份恢复的命令行工具，用于对 TiDB 集群进行数据备份和恢复，也可以在保证兼容性前提下用来做大规模的数据迁移。BR 工具有多种[使用方式](/br/backup-and-restore-tool.md#使用方式)，本文中使用 SQL 语句 [BACKUP](/sql-statements/sql-statement-backup.md#backup) 和 [RESTORE](/sql-statements/sql-statement-restore.md#restore) 进行备份恢复。

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
    +-------------------------+：
    | @@global.tidb_gc_enable |
    +-------------------------+
    |                       0 |
    +-------------------------+
    1 row in set (0.00 sec)
    ```

    > **注意：**
    >
    > 在生产集群中，关闭 GC 机制和备份操作会一定程度上降低集群的读性能，建议在业务低峰期进行备份，并设置合适的 RATE_LIMIT 限制备份操作对线上业务的影响。

2. 备份数据。

    在上游集群中执行 BACKUP 语句备份数据：

    {{< copyable "sql" >}}

    ```sql
    MySQL [(none)]> BACKUP DATABASE * TO 's3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true' RATE_LIMIT = 120 MB/SECOND;
    +---------------+----------+--------------------+---------------------+---------------------+
    | Destination   | Size     | BackupTS           | Queue Time          | Execution Time      |
    +---------------+----------+--------------------+---------------------+---------------------+
    | s3://backup   | 10315858 | 431434047157698561 | 2022-02-25 19:57:59 | 2022-02-25 19:57:59 |
    +---------------+----------+--------------------+---------------------+---------------------+
    1 row in set (2.11 sec)
    ```

    备份语句提交成功后，TiDB 会返回关于备份数据的元信息，这里需要重点关注 BackupTS，它意味着该时间点之前数据会被备份，后边的教程中，本文将使用 BackupTS 作为**数据校验截止时间**和 **TiCDC 增量扫描的开始时间**。

3. 恢复数据。

    在下游集群中执行 RESTORE 语句恢复数据：

    {{< copyable "sql" >}}

    ```sql
    mysql> RESTORE DATABASE * FROM 's3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true';
    +--------------+-----------+--------------------+---------------------+---------------------+
    | Destination  | Size      | BackupTS           | Queue Time          | Execution Time      |
    +--------------+-----------+--------------------+---------------------+---------------------+
    | s3://backup  | 10315858  | 431434141450371074 | 2022-02-25 20:03:59 | 2022-02-25 20:03:59 |
    +--------------+-----------+--------------------+---------------------+---------------------+
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
    ######################### Datasource config #########################
    [data-sources]
    [data-sources.upstream]
            host = "172.16.6.122" # 需要替换为实际上游集群 ip
            port = 4000
            user = "root"
            password = ""
            snapshot = "431434047157698561" # 配置为实际的备份时间点（参见「备份」小节的 BackupTS）
    [data-sources.downstream]
            host = "172.16.6.125" # 需要替换为实际下游集群 ip
            port = 4000
            user = "root"
            password = ""

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

    在上游集群中，执行以下命令创建从上游到下游集群的同步链路：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cdc cli changefeed create --pd=http://172.16.6.122:2379 --sink-uri="mysql://root:@172.16.6.125:4000" --changefeed-id="upstream-to-downstream" --start-ts="431434047157698561"
    ```

    以上命令中：
     - --pd：实际的上游集群的地址
     - --sink-uri：同步任务下游的地址
     - --changefeed-id：同步任务的 ID，格式需要符合正则表达式 ^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$
     - --start-ts：TiCDC 同步的起点，需要设置为实际的备份时间点（也就是第二章「备份」小节提到的 BackupTS）

    更多关于 changefeed 的配置，请参考[同步任务配置文件描述](/ticdc/manage-ticdc.md#同步任务配置文件描述)。

3. 重新开启 GC。

    TiCDC 可以保证 GC 只回收已经同步的历史数据。因此，创建完从上游到下游集群的 changefeed 之后，就可以执行如下命令恢复集群的垃圾回收功能。详情请参考 [TiCDC GC safepoint 的完整行为](/ticdc/troubleshoot-ticdc.md#ticdc-gc-safepoint-的完整行为是什么)。

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

## 第 4 步：平滑切换业务

通过 TiCDC 创建上下游的同步链路后，原集群的写入数据会以非常低的延迟同步到新集群，此时可以逐步将读流量迁移到新集群了。观察一段时间，如果新集群表现稳定，就可以将写流量接入新集群，主要分为三个步骤：

1. 停止上游集群的写业务。确认上游数据已全部同步到下游后，停止上游到下游集群的 changefeed。

    {{< copyable "shell-regular" >}}

    ```shell
    # 停止旧集群到新集群的 changefeed
    tiup cdc cli changefeed pause -c "upstream-to-downstream" --pd=http://172.16.6.122:2379

    # 查看 changefeed 状态
    tiup cdc cli changefeed list
    [
      {
        "id": "upstream-to-downstream",
        "summary": {
        "state": "stopped",  # 需要确认这里的状态为 stopped
        "tso": 431747241184329729,
        "checkpoint": "2022-03-11 15:50:20.387", # 确认这里的时间晚于停写的时间
        "error": null
        }
      }
    ]
    ```

2. 创建下游到上游集群的 changefeed。由于此时上下游数据是一致的，且没有新数据写入，因此可以不指定 start-ts，默认为当前时间：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cdc cli changefeed create --pd=http://172.16.6.125:2379 --sink-uri="mysql://root:@172.16.6.122:4000" --changefeed-id="downstream -to-upstream"
    ```

3. 将写业务迁移到下游集群，观察一段时间后，等新集群表现稳定，便可以弃用原集群。