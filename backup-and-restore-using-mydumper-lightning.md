---
title: 使用 Mydumper/TiDB Lightning 进行备份与恢复
aliases: ['/docs-cn/stable/backup-and-restore-using-mydumper-lightning/','/docs-cn/v4.0/backup-and-restore-using-mydumper-lightning/','/docs-cn/stable/how-to/maintain/backup-and-restore/mydumper-lightning/','/docs-cn/v4.0/how-to/maintain/backup-and-restore/mydumper-lightning/']
---

# 使用 Mydumper/TiDB Lightning 进行备份与恢复

本文档将详细介绍如何使用 Mydumper/TiDB Lightning 对 TiDB 进行全量备份与恢复。增量备份与恢复可使用 [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)。

这里假定 TiDB 服务器信息如下：

|服务器名称|服务器地址|端口|用户名|密码|
|----|-------|----|----|--------|
|TiDB|127.0.0.1|4000|root|*|

在这个备份恢复过程中，会用到下面的工具：

- [Mydumper](/mydumper-overview.md) 从 TiDB 导出数据
- [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 导入数据到 TiDB

## 使用 Mydumper/TiDB Lightning 全量备份恢复数据

`mydumper` 是一个强大的数据备份工具，具体可以参考 [`maxbube/mydumper`](https://github.com/maxbube/mydumper)。

可使用 [Mydumper](/mydumper-overview.md) 从 TiDB 导出数据进行备份，然后用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 将其导入到 TiDB 里面进行恢复。

> **注意：**
>
> PingCAP 研发团队对 `mydumper` 进行了针对 TiDB 的适配性改造，建议使用 PingCAP 官方提供的 [Mydumper](/mydumper-overview.md)。由于使用 `mysqldump` 进行数据备份和恢复都要耗费许多时间，这里也并不推荐。

### Mydumper/TiDB Lightning 全量备份恢复最佳实践

为了快速地备份恢复数据 (特别是数据量巨大的库)，可以参考以下建议：

* 导出来的数据文件应当尽可能的小，可以通过设置参数 `-F` 来控制导出来的文件大小。如果后续使用  TiDB Lightning 对备份文件进行恢复，建议把 `mydumper` -F 参数的值设置为 `256`（单位 MB）；如果使用 `loader` 恢复，则建议设置为 `64`（单位 MB）。

## 从 TiDB 备份数据

我们使用 `mydumper` 从 TiDB 备份数据，如下:

{{< copyable "shell-regular" >}}

```bash
./bin/mydumper -h 127.0.0.1 -P 4000 -u root -t 32 -F 256 -B test -T t1,t2 --skip-tz-utc -o ./var/test
```

上面，我们使用 `-B test` 表明是对 `test` 这个 database 操作，然后用 `-T t1,t2` 表明只导出 `t1`，`t2` 两张表。

`-t 32` 表明使用 32 个线程去导出数据。`-F 256` 是将实际的表切分成一定大小的 chunk，这里的 chunk 大小为 256MB。

添加 `--skip-tz-utc` 参数后，会忽略掉 TiDB 与导数据的机器之间时区设置不一致的情况，禁止自动转换。

如果 `mydumper` 出现以下报错：

```
** (mydumper:27528): CRITICAL **: 13:25:09.081: Could not read data from testSchema.testTable: GC life time is shorter than transaction duration, transaction starts at 2019-08-05 21:10:01.451 +0800 CST, GC safe point is 2019-08-05 21:14:53.801 +0800 CST
```

就再执行两步命令：

1. 执行 `mydumper` 命令前，查询 TiDB 集群的 [GC](/garbage-collection-overview.md) 值并使用 MySQL 客户端将其调整为合适的值：

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
    UPDATE mysql.tidb SET VARIABLE_VALUE = '720h' WHERE VARIABLE_NAME = 'tikv_gc_life_time';
    ```

2. 执行 `mydumper` 命令后，将 TiDB 集群的 GC 值恢复到第 1 步中的初始值：

    {{< copyable "sql" >}}

    ```sql
    UPDATE mysql.tidb SET VARIABLE_VALUE = '10m' WHERE VARIABLE_NAME = 'tikv_gc_life_time';
    ```

## 向 TiDB 恢复数据

使用 TiDB Lightning 将之前导出的数据导入到 TiDB，完成恢复操作。具体的使用方法见 [TiDB Lightning 使用文档](/tidb-lightning/tidb-lightning-backends.md)
