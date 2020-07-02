---
title: 使用 Dumpling/TiDB Lightning 进行备份与恢复
category: how-to
---

# 使用 Dumpling/TiDB Lightning 进行备份与恢复

本文档介绍如何使用数据导出工具 [Dumpling](https://github.com/pingcap/dumpling)。该工具可以把存储在 TiDB 中的数据导出为 SQL 或者 CSV 格式，可以用于完成逻辑上的全量备份或者导出。

如果需要直接备份 SST 文件（键值对）或者对延迟不敏感的增量备份，请参阅 [BR](/br/backup-and-restore-tool.md)。如果需要实时的增量备份，请参阅 [TiCDC](/ticdc/ticdc-overview.md)。

Dumpling 的更多具体用法可以使用 --help 指令查看，或者查看[中文使用手册](https://github.com/pingcap/dumpling/blob/master/docs/cn/user-guide.md)。

使用 Dumpling 时，需要在已经启动的集群上执行导出命令。本文假设在 `127.0.0.1:4000` 有一个 TiDB 实例，并且这个 TiDB 实例中有无密码的 root 用户。

## Dumpling/TiDB Lightning 全量备份恢复最佳实践

为了快速地备份恢复数据 (特别是数据量巨大的库)，可以参考以下建议：

* 导出来的数据文件应当尽可能的小，可以通过设置参数 `-F` 来控制导出来的文件大小。如果后续使用 TiDB Lightning 对备份文件进行恢复，建议把 `dumpling` -F 参数的值设置为 `256m`。
* 如果导出的表中有数据表的行数非常多，可以通过设置参数 `-r` 来开启表内并发。

## 从 TiDB 备份数据

我们使用 `dumpling` 从 TiDB 备份数据，如下:

{{< copyable "shell-regular" >}}

```bash
./bin/dumpling -h 127.0.0.1 -P 4000 -u root -t 32 -F 256m -T test.t1 -T test.t2 -o ./var/test
```

上面，用 `-T test.t1 -T test.t2` 表明只导出 `test`.`t1`，`test`.`t2` 两张表。更多导出数据筛选方式可以参考[筛选导出的数据](/dumpling-overview.md#筛选导出的数据)。

`-t 32` 表明使用 32 个线程去导出数据。`-F 256m` 是将实际的表切分成一定大小的 chunk，这里的 chunk 大小为 256MB。

如果 `dumpling` 出现以下报错：

```
Could not read data from testSchema.testTable: GC life time is shorter than transaction duration, transaction starts at 2019-08-05 21:10:01.451 +0800 CST, GC safe point is 2019-08-05 21:14:53.801 +0800 CST
```

就再执行两步命令：

1. 执行 `dumpling` 命令前，查询 TiDB 集群的 [GC](/garbage-collection-overview.md) 值并使用 MySQL 客户端将其调整为合适的值：

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM mysql.tidb WHERE VARIABLE_NAME = 'tikv_gc_life_time';
    ```

    ```
    +-----------------------+------------------------------------------------------------------------------------------------+
    | VARIABLE_NAME         | VARIABLE_VALUE                                                                                 |
    +-----------------------+------------------------------------------------------------------------------------------------+
    | tikv_gc_life_time     | 10m0s                                                                                          |
    +-----------------------+------------------------------------------------------------------------------------------------+
    1 rows in set (0.02 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    update mysql.tidb set VARIABLE_VALUE = '720h' where VARIABLE_NAME = 'tikv_gc_life_time';
    ```

2. 执行 `dumpling` 命令后，将 TiDB 集群的 GC 值恢复到第 1 步中的初始值：

    {{< copyable "sql" >}}

    ```sql
    update mysql.tidb set VARIABLE_VALUE = '10m' where VARIABLE_NAME = 'tikv_gc_life_time';
    ```

## 向 TiDB 恢复数据

使用 TiDB Lightning 将之前导出的数据导入到 TiDB，完成恢复操作。具体的使用方法见 [TiDB Lightning 使用文档](/tidb-lightning/tidb-lightning-tidb-backend.md)
