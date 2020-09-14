---
title: Mydumper 使用文档
summary: 使用 Mydumper 从 TiDB 导出数据。
aliases: ['/docs-cn/dev/mydumper-overview/','/docs-cn/dev/reference/tools/mydumper/']
---

# Mydumper 使用文档

## Mydumper 简介

> **警告：**
>
> PingCAP 之前维护的 Mydumper 工具 fork 自 [mydumper project](https://github.com/maxbube/mydumper)，针对 TiDB 的特性进行了优化。Mydumper 目前已经不再开发新功能，其绝大部分功能已经被 [Dumpling](/dumpling-overview.md) 取代。Dumpling 工具使用 Go 语言编写，支持更多针对 TiDB 特性的优化。强烈建议切换到 Dumpling。

### 相比于普通的 Mydumper，此工具有哪些改进之处？

+ 对于 TiDB 可以设置 [tidb_snapshot](/read-historical-data.md#操作流程) 的值指定备份数据的时间点，从而保证备份的一致性，而不是通过 `FLUSH TABLES WITH READ LOCK` 来保证备份一致性。

+ 使用 TiDB 的隐藏列 `_tidb_rowid` 优化了单表内数据的并发导出性能。

## 基本用法

### 新添参数

- `-z` 或 `--tidb-snapshot`：设置 `tidb_snapshot` 用于备份。默认值为当前 TSO（`SHOW MASTER STATUS` 输出的 `Position` 字段）。此参数可设为 TSO 或有效的 `datetime` 时间，例如：`-z "2016-10-08 16:45:26"`。

### 需要的权限

- SELECT
- RELOAD
- LOCK TABLES
- REPLICATION CLIENT

### 使用举例

执行如下命令从 TiDB 备份数据，需要根据实际情况添加命令行参数：

{{< copyable "shell-regular" >}}

```bash
./bin/mydumper -h 127.0.0.1 -u root -P 4000
```

## 表内并发 Dump

### 原理

Mydumper 首先计算 `min(_tidb_rowid)` 和 `max(_tidb_rowid)`，然后按照 `-r` 设定的值对表划分 chunks，将 chunks 分配到不同线程并发导出。

### 并发 Dump 相关参数

- `-t` 或 `--threads`：并发线程数，默认值为 `4`。
- `-r` 或 `--rows`：每个 chunks 包含的最大行数。设置该值后，Mydumper 将会忽略 `--chunk-filesize` 值。

### 示例

以下是一条完整的 Mydumper 命令：

{{< copyable "shell-regular" >}}

```bash
./bin/mydumper -h 127.0.0.1 -u root -P 4000 -r 10000 -t 4
```

### 支持 `_tidb_rowid` 索引的 TiDB 版本

由于表内并发使用 TiDB 的隐藏列 `_tidb_rowid`，数据库需要支持 `_tidb_rowid` 索引才能发挥并发导出的优势。

以下 TiDB 版本支持 `_tidb_rowid` 索引：

- v2.1.3 及以上
- v3.0 及以上，包括 v3.1 及未来版本

### 性能评估

在 Dump 操作前需要进行性能评估。由于并发 Scan 操作对 TiDB、TiKV 集群都会产生一定压力，所以需要评估与测试 Dump 操作对数据库集群和业务的影响。

## FAQ

### 使用的 `--tidb-snapshot` 导出时报错，怎么处理？

需要执行命令时增加一个参数 --skip-tz-utc，如果不设置的话 Mydumper 会预先设置 UTC 时区，然后在设置 tidb-snapshot 的时候会做时区转化，就会有问题

### 如何判断使用的 Mydumper 是否为 PingCAP 优化的版本？

执行如下命令：

{{< copyable "shell-regular" >}}

```bash
./bin/mydumper -V
```

如果输出结果中包含 `githash`（如下列示例输出中的 `d3e6fec8b069daee772d0dbaa47579f67a5947e7`），则使用的 Mydumper 为 PingCAP 优化的版本。

```
mydumper 0.9.5 (d3e6fec8b069daee772d0dbaa47579f67a5947e7), built against MySQL 5.7.24
```

### 使用 Loader 恢复 Mydumper 备份出来的数据时报错 "invalid mydumper files for there are no `-schema-create.sql` files found"，应该如何解决？

检查使用 Mydumper 备份数据时是否使用了 `-T` 或者 `--tables-list` 配置，如果使用了这些配置，Mydumper 就不会生成包含建库 SQL 的文件。

**解决方法**：在 Mydumper 备份数据目录下创建文件 `{schema-name}-schema-create.sql`，在文件中写入 "CREATE DATABASE `{schema-name}`"，再运行 Loader 即可。

### 为什么使用 Mydumper 导出来的 TIMESTAMP 类型的数据和数据库中的数据不一致？

检查一下运行 Mydumper 的服务器的时区与数据库的时区是否一致，Mydumper 会根据运行所在服务器的时区对 TIMESTAMP 类型的数据进行转化，可以给 Mydumper 加上 `--skip-tz-utc` 参数禁止这种转化。

### 如何配置 Mydumper 的参数 `-F, --chunk-filesize`？

Mydumper 在备份时会根据这个参数的值把每个表的数据划分成多个 chunk，每个 chunk 保存到一个文件中，大小约为 `chunk-filesize`。根据这个参数把数据切分到多个文件中，这样就可以利用 Loader/TiDB Lightning 的并行处理逻辑提高导入速度。如果后续使用 Loader 对备份文件进行恢复，建议把该参数的值设置为 `64`（单位 MB）；如果使用 TiDB Lightning 恢复，则建议设置为 `256`（单位 MB）。

### 如何配置 Mydumper 的参数 `-s --statement-size`？

Mydumper 使用该参数控制 `Insert Statement` 的大小，默认值为 `10000000`（约 1 MB）。使用该参数来尽量避免在恢复数据时报以下错误：

```log
packet for query is too large. Try adjusting the 'max_allowed_packet' variable
```

默认值在绝大部分情况下都可以满足需求，但是**如果表为宽表，单行数据的大小可能超过 statement-size 的限制，Mydumper 会报如下的 Warning**：

```log
Row bigger than statement_size for xxx
```

此时恢复数据时仍然会报 `packet for query is too large` 的错误日志，这个时候需要修改以下两个配置（以设置为 `128M` 为例）：

* 在 TiDB Server 执行 `set @@global.max_allowed_packet=134217728`（`134217728` = `128M`）。
* 根据实际情况为 Loader 的配置文件或者 DM task 配置文件中的 db 配置增加类似 `max-allowed-packet=128M` 的语句，然后重启进程或者任务。

### 如何设置 Mydumper 的参数 `-l, --long-query-guard`？

把该参数设置为预估备份需要消耗的时间，如果 Mydumper 运行时间超过该参数的值，就会报错退出。推荐初次备份设置为 `7200`（单位：秒），之后可根据具体备份时间进行调整。

### 如何设置 Mydumper 的参数 `--tidb-force-priority`？

仅当备份 TiDB 的数据时才可以设置该参数，值可以为 `LOW_PRIORITY`，`DELAYED` 或者 `HIGH_PRIORITY`。如果不希望数据备份对线上业务造成影响，推荐将该参数设置为 `LOW_PRIORITY`；如果备份的优先级更高，则可以设置为 `HIGH_PRIORITY`。

### Mydumper 备份 TiDB 数据报错 "GC life time is shorter than transaction duration" 应该怎么解决？

Mydumper 备份 TiDB 数据时为了保证数据的一致性使用了 TiDB 的 snapshot 特性，如果备份过程中 snapshot 对应的历史数据被 TiDB GC 处理了，则会报该错误。解决步骤如下：

1. 在备份前，使用 MySQL 客户端查询 TiDB 集群的 `tikv_gc_life_time` 的值，并将其调整为一个合适的值：

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

2. 备份完成后，将 `tikv_gc_life_time` 调整为原来的值：

    {{< copyable "sql" >}}

    ```sql
    update mysql.tidb set VARIABLE_VALUE = '10m0s' where VARIABLE_NAME = 'tikv_gc_life_time';
    ```

### Mydumper 的参数 `--tidb-rowid` 是否需要配置？

如果设置该参数为 true，则导出的数据中会包含 TiDB 的隐藏列的数据。将数据恢复到 TiDB 的时候使用隐藏列会有数据不一致的风险，目前不推荐使用该参数。

### Mydumper 报错 "Segmentation fault" 怎么解决？

该 bug 已修复。如果仍然报错，可尝试升级到最新版本。

### Mydumper 报错 "Error dumping table ({schema}.{table}) data: line ...... (total length ...)" 怎么解决？

Mydumper 解析 SQL 时报错，可尝试使用最新版本。如果仍然报错，可以提 issue 到 [mydumper/issues](https://github.com/pingcap/mydumper/issues)。

### Mydumper 报错 "Failed to set tidb_snapshot: parsing time \"20190901-10:15:00 +0800\" as \"20190901-10:15:00 +0700 MST\": cannot parse \"\" as \"MST\"" 如何解决？

检查 TiDB 的版本是否低于 v2.1.11。如果是的话，需要升级 TiDB 到 v2.1.11 或以上版本。

### 未来是否计划让 PingCAP 对 Mydumper 的改动合并到上游？

是的，PingCAP 团队计划将对 Mydumper 的改动合并到上游。参见 [PR #155](https://github.com/maxbube/mydumper/pull/155)。
