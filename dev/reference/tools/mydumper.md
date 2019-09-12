---
title: Mydumper 使用文档
summary: 使用 Mydumper 从 TiDB 导出数据。
category: reference
---

# Mydumper 使用文档

## Mydumper 简介

[Mydumper](https://github.com/pingcap/mydumper) 是一个 fork 项目，针对 TiDB 的特性进行了优化，推荐使用此工具对 TiDB 进行逻辑备份。

Mydumper 包含在 tidb-enterprise-tools 安装包中，可[在此下载](/dev/reference/tools/download.md)。

### 相比于普通的 Mydumper，此工具有哪些改进之处？

+ 对于 TiDB 可以设置 [tidb_snapshot](/dev/how-to/get-started/read-historical-data.md#操作流程) 的值指定备份数据的时间点，从而保证备份的一致性，而不是通过 `FLUSH TABLES WITH READ LOCK` 来保证备份一致性。

+ 优化了 TiDB PK not handle 场景（表没有 Primary Key 或者 Primary Key 非整数）下的数据导出性能。

## Mydumper 使用

### 新添参数

  ```bash
    -z, --tidb-snapshot: 设置 tidb_snapshot 用于备份
                         默认值：当前 TSO（SHOW MASTER STATUS 输出的 Position)
                         此参数可设为 TSO 或有效的 datetime 时间，例如：-z "2016-10-08 16:45:26"
  ```

### 需要的权限

- SELECT
- RELOAD
- LOCK TABLES
- REPLICATION CLIENT

### 使用举例

命令行参数：

  ```bash
  ./bin/mydumper -h 127.0.0.1 -u root -P 4000
  ```

## FAQ

### 如何判断使用的 Mydumper 是否为 PingCAP 优化的版本？

运行命令

  ```bash
  ./bin/mydumper --help
  ```

包含如下配置项的为 PingCAP 优化的版本：

  ```bash
  -z, --tidb-snapshot         Snapshot to use for TiDB
  ```

### 使用 Loader 恢复 Mydumper 备份出来的数据时报错 "invalid mydumper files for there are no `-schema-create.sql` files found"，应该如何解决？

检查使用 Mydumper 备份数据时是否使用了 `-T` 或者 `--tables-list` 配置，如果使用了这些配置 Mydumper 就不会生成包含建库 SQL 的文件。解决方法：在 Mydumper 备份数据目录下创建文件 `{schema-name}-schema-create.sql`，在文件中写入 "CREATE DATABASE `{schema-name}`"，再运行 Loader 即可。

### 为什么使用 Mydumper 导出来的时间类型的数据和数据库中的数据不一致？

检查一下运行 Mydumper 的服务器的时区与数据库的时区是否一致，Mydumper 会根据运行所在服务器的时区对时间类型数据进行转化，可以给 Mydumper 加上 `--skip-tz-utc` 参数忽略这种转化。

### 如何配置 Mydumper 的参数 `-F, --chunk-filesize`?

Mydumper 在备份时会根据这个参数的值把每个表的数据划分成多个 `chunk`，每个 `chunk` 保存到一个文件中，大小约为 `chunk-filesize`。根据这个参数把数据切分到多个文件中，这样就可以利用 Loader/TiDB-Lightning 的并行处理逻辑提高导入速度。 如果后续使用 Loader 对备份文件进行恢复，建议把该参数的值设置为 64（单位 MB）；如果使用 TiDB-Lightning 恢复，则建议设置为 256（单位 MB）。

### 如何配置 Mydumper 的参数 `-s --statement-size`?

Mydumper 使用该参数控制 `Insert Statement` 的大小，默认值为 1M 左右。使用该参数来尽量避免在恢复数据时报以下错误：

  ```log
  packet for query is too large. Try adjusting the 'max_allowed_packet' variable
  ```

默认值在绝大部分情况下都可以满足需求，但是如果表为宽表，单行数据的大小可能超过 statement-size 的限制，Mydumper 会报如下的 WARN：

  ```log
  Row bigger than statement_size for xxx
  ```

这种情况下恢复数据时仍然会报 `packet for query is too large` 的错误日志，这个时候需要修改以下两个配置（以设置为 128M 为例）：
     * 在 TiDB Server 执行 `set @@global.max_allowed_packet=134217728` （`134217728 = 128M`）
     * 根据实际情况为 Loader 的配置文件或者 DM task 配置文件中的 db 配置增加类似 `max-allowed-packet=128M`，然后重启进程或者任务

### Mydumper 备份 TiDB 数据报错 "GC life time is shorter than transaction duration" 应该怎么解决？

Mydumper 备份 TiDB 数据时为了保证数据的一致性使用了 TiDB 的 snapshot 特性，如果备份过程中 snapshot 对应的历史数据被 TiDB GC 处理了，则会报该错误。建议在备份前通过如下命令调整 TiDB 的 GC 参数：

  ```bash
  mysql> update mysql.tidb set VARIABLE_VALUE = '720h' where VARIABLE_NAME = 'tikv_gc_life_time';
  ```

备份完成后再将 `tikv_gc_life_time` 的值调整为原来的值。

### Mydumper 的参数 `--tidb-rowid` 是否需要配置？

如果设置该参数为 true 则导出的数据中会包含 TiDB 的隐藏列的数据，在恢复到 TiDB 的时候使用隐藏列会有数据不一致的风险，不推荐使用该参数。

### Mydumper 报错 "Segmentation fault" 怎么解决？

是 Mydumper 的 bug 导致的，已经修复，可以尝试使用最新版本。

### Mydumper 报错 "Error dumping table ({schema}.{table}) data: line ...... (total length ...)" 怎么解决？

Mydumper 解析 SQL 时报错，可以尝试使用最新版本。如果仍然报错，可以提 issue 到 [mydumper/issues](https://github.com/pingcap/mydumper/issues)。

### Mydumper 报错 "Failed to set tidb_snapshot: parsing time \"20190901-10:15:00 +0800\" as 20190901-10:15:00 +0700 MST\": cannot parse \"\" as \"MST\"" 如何解决？

检查 TiDB 的版本是否低于 v2.1.11，如果是的话需要升级 TiDB 到 v2.1.11 或以上版本。

### PingCAP 的 Mydumper 的源码是否可获取？

PingCAP 的 Mydumper 源码 [位于 GitHub](https://github.com/pingcap/mydumper)。

### 未来是否计划让 PingCAP 对 Mydumper 的改动合并到上游？

是的，PingCAP 团队计划将对 Mydumper 的改动合并到上游。参见 [PR #155](https://github.com/maxbube/mydumper/pull/155)。
