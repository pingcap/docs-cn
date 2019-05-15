---
title: mydumper 使用文档 
summary: 使用 mydumper 从 TiDB 导出数据。
category: reference
aliases: ['/docs-cn/tools/mydumper/']
---

# mydumper 使用文档

## mydumper 简介

`mydumper` 是 [mydumper](https://github.com/maxbube/mydumper) 的 fork 项目，并添加了一些针对 TiDB 的功能。推荐使用此工具对 TiDB 进行逻辑备份。

mydumper 包含在 tidb-enterprise-tools 安装包中，可[在此下载](/dev/reference/tool/download.md)。

## 相比于普通的 mydumper，此工具有哪些改进之处？

+ 使用 `tidb_snapshot` 而非 `FLUSH TABLES WITH READ LOCK` 提供备份一致性
+ [允许设置](/dev/how-to/get-started/read-historical-data.md#操作流程) `tidb_snapshot` 的值（即可备份不同时间点的数据）  

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

### PingCAP 的 mydumper 的源码是否可获取？

PingCAP 的 mydumper 源码 [位于 GitHub](https://github.com/pingcap/mydumper)。

### 未来是否计划让 PingCAP 对 mydumper 的改动合并到上游？

是的，PingCAP 团队计划将对 mydumper 的改动合并到上游。参见 [PR #155](https://github.com/maxbube/mydumper/pull/155)。
