---
title: mydumper 使用文档 
summary: 使用 mydumper 从 TiDB 导出数据。
category: tools
---

# mydumper 使用文档

## mydumper 简介

`mydumper` 是 [mydumper](https://github.com/maxbube/mydumper) 的 fork 项目，并添加了一些针对 TiDB 的功能。推荐使用此工具对 TiDB 进行逻辑备份。

[下载 Binary](http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.tar.gz)。

## 相比于普通的 mydumper，此工具有哪些改进之处?

+ 使用 `tidb_snapshot` 而非 `FLUSH TABLES WITH READ LOCK` 提供备份一致性 

+ `INSERT` 语句中包含隐藏的 `_tidb_rowid` 列

+ 允许 `tidb_snapshot` 为 [configurable](../op-guide/history-read.md#how-tidb-reads-data-from-history-versions) （即备份之前的数据）

### 新添参数

```
  -z, --tidb-snapshot: Set the tidb_snapshot to be used for the backup.
                       Default: NOW()-INTERVAL 1 SECOND.
                       Accepts either a TSO or valid datetime.  For example: -z "2016-10-08 16:45:26"
```

### 使用举例

命令行参数：

```
./bin/mydumper -h 127.0.0.1 -u root -P 4000
```

## FAQ

### PingCAP 的 mydumper 的源码是否可获取？

PingCAP 的 mydumper 源码 [位于 GitHub](https://github.com/pingcap/mydumper)。

### 是否计划未来让 PingCAP 的 mydumper 对上游的 mydumper 生效？

是的，PingCAP 团队计划让此 mydumper 对上游的 mydumper 生效。参见 [PR #155](https://github.com/maxbube/mydumper/pull/155).