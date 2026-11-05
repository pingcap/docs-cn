---
title: 从 TiDB 集群迁移数据至兼容 MySQL 的数据库
summary: 了解如何将数据从 TiDB 集群迁移至与 MySQL 兼容的数据库。
---

# 从 TiDB 集群迁移数据至兼容 MySQL 的数据库

本文档介绍如何将数据从 TiDB 集群迁移至兼容 MySQL 的数据库，如 Aurora、MySQL、MariaDB 等。本文将模拟整个迁移过程，具体包括以下四个步骤：

1. 搭建环境
2. 迁移全量数据
3. 迁移增量数据
4. 平滑切换业务

## 第 1 步：搭建环境

1. 部署上游 TiDB 集群。

    使用 TiUP Playground 部署上游 TiDB 集群。更多信息，请参见[本地快速部署 TiDB 集群](/tiup/tiup-playground.md)。

    [TiCDC](/ticdc/ticdc-overview.md) 会将上游 TiDB 集群中的增量数据变更复制到下游兼容 MySQL 的数据库。下面的示例将 TiCDC 的 `gc-ttl` 设置为 `172800` 秒（48 小时）。这个值需要覆盖全量导出、全量导入以及增量复制追平所需的时间。更多信息，请参见[第 2 步中的 GC 注意事项](#第-2-步迁移全量数据)。

    ```shell
    # 创建 TiCDC 配置文件
    cat > ticdc.toml <<'EOF'
    gc-ttl = 172800
    EOF
    # 创建上游集群
    tiup playground --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1 --ticdc.config ticdc.toml
    # 查看集群状态
    tiup status
    ```

2. 部署下游 MySQL 实例。

    - 在实验环境中，可以使用 Docker 快速部署 MySQL 实例，执行如下命令：

        ```shell
        docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -p 3306:3306 -d mysql
        ```

    - 在生产环境中，可以参考 [Installing MySQL](https://dev.mysql.com/doc/refman/8.0/en/installing.html) 来部署 MySQL 实例。

3. 模拟业务负载。

    在测试实验环境下，可以使用 go-tpc 向上游 TiDB 集群写入数据，以让 TiDB 产生事件变更数据。执行如下命令，将首先在上游 TiDB 创建名为 tpcc 的数据库，然后使用 TiUP bench 写入数据到刚创建的 tpcc 数据库中。

    ```shell
    tiup bench tpcc -H 127.0.0.1 -P 4000 -D tpcc --warehouses 4 prepare
    tiup bench tpcc -H 127.0.0.1 -P 4000 -D tpcc --warehouses 4 run --time 300s
    ```

    关于 go-tpc 的更多详细内容，可以参考[如何对 TiDB 进行 TPC-C 测试](/benchmark/benchmark-tidb-using-tpcc.md)。

## 第 2 步：迁移全量数据

搭建好测试环境后，可以使用 [Dumpling](/dumpling-overview.md) 工具导出上游集群的全量数据。

> **注意：**
>
> 在生产集群中，关闭 GC 机制和备份操作会一定程度上降低集群的读性能，建议在业务低峰期进行备份，并设置合适的 `RATE_LIMIT` 限制备份操作对线上业务的影响。

1. 关闭 GC (Garbage Collection)。

    为了保证增量迁移过程中新写入的数据不丢失，在开始全量导出之前，需要关闭上游集群的垃圾回收 (GC) 机制，以确保系统不再清理历史数据。对于 TiDB v4.0.0 及之后的版本，Dumpling 可能会[自动调整 GC 的 safe point 从而阻塞 GC](/dumpling-overview.md#手动设置-tidb-gc-时间)。然而，手动关闭 GC 仍然是必要的，因为在 Dumpling 退出后，GC 可能会被触发，从而导致增量变更迁移失败。

    执行如下命令关闭 GC：

    ```sql
    MySQL [test]> SET GLOBAL tidb_gc_enable=FALSE;
    ```

    ```
    Query OK, 0 rows affected (0.01 sec)
    ```

    查询 `tidb_gc_enable` 的取值，判断 GC 是否已关闭：

    ```sql
    MySQL [test]> SELECT @@global.tidb_gc_enable;
    ```

    ```
    +-------------------------+
    | @@global.tidb_gc_enable |
    +-------------------------+
    |                       0 |
    +-------------------------+
    1 row in set (0.00 sec)
    ```

    > **注意：**
    >
    > TiCDC 中 `gc-ttl` 的默认值为 24 小时。如果后续[增量同步任务](#第-3-步迁移增量数据)的复制延迟超过 `gc-ttl`，任务可能会因 `ErrGCTTLExceeded` 而失败。对于耗时较长的迁移，请按照[第 1 步](#第-1-步搭建环境)中的示例，在启动 TiCDC 之前配置更大的值。更多信息，请参见[TiCDC 的 `gc-ttl` 是什么](/ticdc/ticdc-faq.md#ticdc-的-gc-ttl-是什么)。

2. 备份数据。

    1. 使用 Dumpling 导出 SQL 格式的数据：

        ```shell
        tiup dumpling -u root -P 4000 -h 127.0.0.1 --filetype sql -t 8 -o ./dumpling_output -r 200000 -F256MiB
        ```

    2. 导出完毕后，执行如下命令查看导出数据的元信息，metadata 文件中的 `Pos` 就是导出快照的 TSO，将其记录为 BackupTS：

        ```shell
        cat dumpling_output/metadata
        ```

        ```
        Started dump at: 2022-06-28 17:49:54
        SHOW MASTER STATUS:
                Log: tidb-binlog
                Pos: 434217889191428107
                GTID:

        Finished dump at: 2022-06-28 17:49:57
        ```

3. 恢复数据。

    使用开源工具 MyLoader 导入数据到下游 MySQL。MyLoader 的安装和详细用例参见 [MyDumpler/MyLoader](https://github.com/mydumper/mydumper)。注意需要使用 MyLoader v0.10 或更早版本，否则会导致 MyLoader 无法处理 Dumpling 导出的 metadata 文件。

    执行以下指令，将 Dumpling 导出的上游全量数据导入到下游 MySQL 实例：

    ```shell
    myloader -h 127.0.0.1 -P 3306 -u root -p my-secret-pw -d ./dumpling_output/
    ```

4. （可选）校验数据。

    通过 [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) 工具，可以验证上下游数据在某个时间点的一致性。

    ```shell
    sync_diff_inspector -C ./config.yaml
    ```

    关于 sync-diff-inspector 的配置方法，请参考[配置文件说明](/sync-diff-inspector/sync-diff-inspector-overview.md#配置文件说明)。在本文中，相应的配置如下：

    ```toml
    # Diff Configuration.
    ######################### Datasource config #########################
    [data-sources]
    [data-sources.upstream]
            host = "127.0.0.1" # 需要替换为实际上游集群 ip
            port = 4000
            user = "root"
            password = ""
            snapshot = "434217889191428107" # 配置为实际的备份时间点（参见「备份」小节的 BackupTS）
    [data-sources.downstream]
            host = "127.0.0.1" # 需要替换为实际下游集群 ip
            port = 3306
            user = "root"
            password = "my-secret-pw"

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

    > **注意：**
    >
    > 创建 changefeed 前，请先确认每个需要同步的表至少具有一个[有效索引](/ticdc/ticdc-overview.md#有效索引)：主键，或者所有列都显式定义为 `NOT NULL` 且不存在虚拟生成列的唯一索引。默认情况下，TiCDC 不会同步没有有效索引的表中的数据变更。后续再添加有效索引，只会让之后的数据变更开始同步，不会补回此前已跳过的变更。更多信息，请参见 [DDL 白名单](/ticdc/ticdc-ddl.md#ddl-白名单)。
    >
    > 对于没有有效索引的表，建议优先补充有效索引。或者，你也可以在 changefeed 配置文件开头（所有 `[xxx]` 配置段之前）添加 [`force-replicate = true`](/ticdc/ticdc-changefeed-config.md#force-replicate)，并在创建 changefeed 时通过 `--config` 指定该配置文件。但该选项不能保证数据一致性，并且可能导致数据重复。

    在上游集群中，执行以下命令创建从上游到下游集群的同步链路：

    ```shell
    tiup cdc:v<CLUSTER_VERSION> cli changefeed create --server=http://127.0.0.1:8300 --sink-uri="mysql://root:***@127.0.0.1:3306" --changefeed-id="upstream-to-downstream" --start-ts="434217889191428107"
    ```

    请将 `***` 替换为你在[第 1 步：搭建环境](#第-1-步搭建环境)中为下游 MySQL root 账户配置的密码。对于 Docker 示例，请使用 `my-secret-pw`。

    以上命令中：

    - `--server`：TiCDC 集群任意一节点地址
    - `--sink-uri`：同步任务下游的地址
    - `--changefeed-id`：同步任务的 ID，格式需要符合正则表达式 `^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`
    - `--start-ts`：TiCDC 同步的起点，需要设置为实际的备份时间点，也就是[第 2 步：迁移全量数据](/migrate-from-tidb-to-mysql.md#第-2-步迁移全量数据)中 “备份数据” 提到的 BackupTS

    更多关于 changefeed 的配置，请参考 [TiCDC Changefeed 配置参数](/ticdc/ticdc-changefeed-config.md)。

3. 重新开启 GC。

    TiCDC 可以保证 GC 只回收已经同步的历史数据。因此，创建完从上游到下游集群的 changefeed 之后，就可以执行如下命令恢复集群的垃圾回收功能。详情请参考 [TiCDC GC safepoint 的完整行为](/ticdc/ticdc-faq.md#ticdc-gc-safepoint-的完整行为是什么)。

    执行如下命令打开 GC：

    ```sql
    MySQL [test]> SET GLOBAL tidb_gc_enable=TRUE;
    ```

    ```
    Query OK, 0 rows affected (0.01 sec)
    ```

    查询 `tidb_gc_enable` 的取值，判断 GC 是否已开启：

    ```sql
    MySQL [test]> SELECT @@global.tidb_gc_enable;
    ```

    ```
    +-------------------------+
    | @@global.tidb_gc_enable |
    +-------------------------+
    |                       1 |
    +-------------------------+
    1 row in set (0.00 sec)
    ```

## 第 4 步：平滑切换业务

创建 changefeed 后，TiCDC 会以较低延迟将纳入同步范围的上游表中的数据变更复制到下游集群。此时可以逐步将读流量迁移到新集群。观察一段时间，如果新集群表现稳定，就可以将写流量接入新集群，步骤如下：

1. 停止上游集群的写业务。确认上游数据已全部同步到下游后，停止上游到下游集群的 changefeed。

    ```shell
    # 停止旧集群到新集群的 changefeed
    tiup cdc cli changefeed pause -c "upstream-to-downstream" --pd=http://172.16.6.122:2379

    # 查看 changefeed 状态
    tiup cdc cli changefeed list
    ```

    ```
    [
      {
        "id": "upstream-to-downstream",
        "summary": {
        "state": "stopped",  # 需要确认这里的状态为 stopped
        "tso": 434218657561968641,
        "checkpoint": "2022-06-28 18:38:45.685", # 确认这里的时间晚于停写的时间
        "error": null
        }
      }
    ]
    ```

2. 将写业务迁移到下游集群，观察一段时间后，等新集群表现稳定，便可以弃用原集群。
