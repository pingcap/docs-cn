---
title: Mydumper 使用文档
summary: 使用 Mydumper 从 TiDB 导出数据。
category: reference
---

# Mydumper 使用文档

## Mydumper 简介

[Mydumper](https://github.com/pingcap/mydumper) 是一个 fork 项目，针对 TiDB 的特性进行了优化，推荐使用此工具对 TiDB 进行逻辑备份。

Mydumper 包含在 tidb-enterprise-tools 安装包中，可[在此下载](/dev/reference/tools/download.md)。

## 相比于普通的 Mydumper，此工具有哪些改进之处？

+ 对于 TiDB 可以设置 [tidb_snapshot](/dev/how-to/get-started/read-historical-data.md#操作流程) 的值指定备份数据的时间点，从而保证备份的一致性，而不是通过 `FLUSH TABLES WITH READ LOCK` 来保证备份一致性。

+ 
  

### 新添参数

```bash
  -z, --tidb-snapshot: 设置 tidb_snapshot 用于备份
                       默认值：当前 TSO（SHOW MASTER STATUS 输出的 UniqueID）
                       此参数可设为 TSO 时间或有效的 datetime 时间。例如：-z "2016-10-08 16:45:26"
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

### 使用 Loader 恢复 Mydumper 备份出来的数据时报错 "invalid mydumper files for there are no `-schema-create.sql` files found", 这个是什么原因，如何解决？

检查使用 Mydumper 备份数据时是否使用了 `-T` 或者 `--tables-list` 配置，如果使用了这些配置 Mydumper 就不会生成保存建库 SQL 的文件。解决方法：在 Mydumper 备份数据目录下创建文件 `{schema-name}-schema-create.sql`， 在文件中写入 "CREATE DATABASE `{schema-name}`"，再运行 Loader 即可。

### 为什么使用 Mydumper 导出来的时间类型的数据和数据库中的数据不一致？

检查一下运行 Mydumper 的服务器的时区与数据库的时区是否一致，Mydumper 会根据运行所在服务器的时区对时间类型数据进行转化，可以给 Mydumper 加上 `--skip-tz-utc` 参数忽略这种转化。

### 如何配置 Mydumper 的参数 `-F, --chunk-filesize`?

Mydumper 在备份时会根据这个参数的值把每个表的数据划分成多个 `chunk`，每个 `chunk` 保存到一个文件中，大小约为 `chunk-filesize`。TiDB-Lightning/Loader 在恢复数据时会按照文件粒度进行并行处理，推荐把该参数的值设置为 64（单位 MB）。

### Mydumper 的参数 `--tidb-rowid` 是否需要配置？

设置该参数为 true 则导出的数据中会包含 TiDB 的隐藏列的数据。

### PingCAP 的 Mydumper 的源码是否可获取？

PingCAP 的 Mydumper 源码 [位于 GitHub](https://github.com/pingcap/mydumper)。

### 未来是否计划让 PingCAP 对 Mydumper 的改动合并到上游？

是的，PingCAP 团队计划将对 Mydumper 的改动合并到上游。参见 [PR #155](https://github.com/maxbube/mydumper/pull/155)。
