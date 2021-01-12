---
title: 使用 Dumpling/TiDB Lightning 进行备份与恢复
aliases: ['/docs-cn/dev/backup-and-restore-using-dumpling-lightning/','/docs-cn/dev/export-or-backup-using-dumpling/','/zh/tidb/dev/export-or-backup-using-dumpling','/docs-cn/dev/backup-and-restore-using-mydumper-lightning/','/docs-cn/dev/how-to/maintain/backup-and-restore/mydumper-lightning/','/docs-cn/dev/how-to/maintain/backup-and-restore/','/zh/tidb/dev/backup-and-restore-using-mydumper-lightning/']
---

# 使用 Dumpling/TiDB Lightning 进行备份与恢复

> **注意：**
>
> PingCAP 之前维护的 Mydumper 工具 fork 自 [mydumper project](https://github.com/maxbube/mydumper)，针对 TiDB 的特性进行了优化。Mydumper 目前已经不再开发新功能，其绝大部分功能已经被 [Dumpling](/dumpling-overview.md) 取代。Dumpling 工具使用 Go 语言编写，支持更多针对 TiDB 特性的优化。请切换到 Dumpling。
>
> 如果你需要阅读使用 Mydumper/TiDB Lightning 进行备份与恢复的文档，可参阅[使用 Mydumper/TiDB Lightning 进行备份与恢复](https://docs.pingcap.com/zh/tidb/v4.0/backup-and-restore-using-mydumper-lightning)。

本文档将详细介绍如何使用 Dumpling/TiDB Lightning 对 TiDB 进行全量备份与恢复。增量备份和同步可使用 [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)。

这里假定 TiDB 服务器信息如下：

|服务器名称|服务器地址|端口|用户名|密码|
|----|-------|----|----|--------|
|TiDB|127.0.0.1|4000|root|*|

在这个备份恢复过程中，会用到下面的工具：

- [Dumpling](/dumpling-overview.md)：从 TiDB 导出数据
- [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)：导入数据到 TiDB

## Dumpling/TiDB Lightning 全量备份恢复最佳实践

为了快速地备份恢复数据（特别是数据量巨大的库），可以参考以下建议：

* 导出来的数据文件应当尽可能的小，可以通过设置选项 `-F` 来控制导出来的文件大小。如果后续使用 TiDB Lightning 对备份文件进行恢复，建议把 `dumpling` -F 选项的值设置为 `256m`。
* 如果导出的表中有些表的行数非常多，可以通过设置选项 `-r` 来开启表内并发。

## 从 TiDB 备份数据

使用 `dumpling` 从 TiDB 备份数据的命令如下:

{{< copyable "shell-regular" >}}

```bash
./bin/dumpling -h 127.0.0.1 -P 4000 -u root -t 32 -F 256m -T test.t1 -T test.t2 -o ./var/test
```

上述命令中，用 `-T test.t1 -T test.t2` 表明只导出 `test`.`t1`，`test`.`t2` 两张表。更多导出数据筛选方式可以参考[筛选导出的数据](/dumpling-overview.md#筛选导出的数据)。

`-t 32` 表明使用 32 个线程来导出数据。`-F 256m` 是将实际的表切分成一定大小的 chunk，这里的 chunk 大小为 256MB。

从 v4.0.0 版本开始，Dumpling 可以自动延长 GC 时间（Dumpling 需要访问 TiDB 集群的 PD 地址），而 v4.0.0 之前的版本，需要手动调整 GC 时间，否则 `dumpling` 备份时可能出现以下报错：

```log
Could not read data from testSchema.testTable: GC life time is shorter than transaction duration, transaction starts at 2019-08-05 21:10:01.451 +0800 CST, GC safe point is 2019-08-05 21:14:53.801 +0800 CST
```

手动调整 GC 时间的步骤如下：

1. 执行 `dumpling` 命令前，查询 TiDB 集群的 [GC](/garbage-collection-overview.md) 值并在 MySQL 客户端执行下列语句将其调整为合适的值：

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM mysql.tidb WHERE VARIABLE_NAME = 'tikv_gc_life_time';
    ```

    ```sql
    +-----------------------+------------------------------------------------------------------------------------------------+
    | VARIABLE_NAME         | VARIABLE_VALUE                                                                                 |
    +-----------------------+------------------------------------------------------------------------------------------------+
    | tikv_gc_life_time     | 10m0s                                                                                          |
    +-----------------------+------------------------------------------------------------------------------------------------+
    1 rows in set (0.02 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    UPDATE mysql.tidb SET VARIABLE_VALUE = '720h' WHERE VARIABLE_NAME = 'tikv_gc_life_time';
    ```

2. 执行 `dumpling` 命令后，将 TiDB 集群的 GC 值恢复到第 1 步中的初始值：

    {{< copyable "sql" >}}

    ```sql
    UPDATE mysql.tidb SET VARIABLE_VALUE = '10m' WHERE VARIABLE_NAME = 'tikv_gc_life_time';
    ```

## 向 TiDB 恢复数据

使用 TiDB Lightning 将之前导出的数据导入到 TiDB，完成恢复操作。具体的使用方法见 [TiDB Lightning 使用文档](/tidb-lightning/tidb-lightning-backends.md)
