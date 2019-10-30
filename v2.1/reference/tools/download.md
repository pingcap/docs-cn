---
title: TiDB 工具下载
category: reference
---

# TiDB 工具下载

本页面汇总了 TiDB 周边工具官方维护版本的下载链接。

## TiDB Binlog 和 TiDB Lightning

如需下载 2.1 版本的 [TiDB Binlog](/v2.1/reference/tools/tidb-binlog/overview.md) 或 [TiDB Lightning](/v2.1/reference/tools/tidb-lightning/overview.md)，直接下载 TiDB 安装包即可，因为 TiDB Binlog 和 TiDB Lightning 均包含在 TiDB 安装包中。

以下表格中也提供了 Kafka 版本的 TiDB Binlog 下载链接。

| 安装包 | 操作系统 | 架构 | SHA256 校验和 |
|:---|:---|:---|:---|
| [tidb-v2.1.0-linux-amd64.tar.gz](http://download.pingcap.org/tidb-v2.1.0-linux-amd64.tar.gz) (TiDB Binlog, TiDB Lightning) | Linux | amd64 |[tidb-v2.1.0-linux-amd64.sha256](http://download.pingcap.org/tidb-v2.1.0-linux-amd64.sha256)|
| [tidb-binlog-kafka-linux-amd64.tar.gz](http://download.pingcap.org/tidb-binlog-kafka-linux-amd64.tar.gz)（Kafka 版本的 TiDB Binlog）| Linux | amd64 |[tidb-binlog-kafka-linux-amd64.sha256](http://download.pingcap.org/tidb-binlog-kafka-linux-amd64.sha256)|

## TiDB DM (Data Migration)

如需下载 1.0 GA 版本的 [DM](https://github.com/pingcap/dm)，点击下表中的下载链接即可。

| 安装包 | 操作系统 | 架构 | SHA256 校验和 |
|:---|:---|:---|:---|
| [dm-v1.0.1-linux-amd64.tar.gz](http://download.pingcap.org/dm-v1.0.1-linux-amd64.tar.gz) | Linux | amd64 | [dm-v1.0.1-linux-amd64.sha256](http://download.pingcap.org/dm-v1.0.1-linux-amd64.sha256) |

如需下载最新版本的 [DM](https://github.com/pingcap/dm)，点击下表中的下载链接即可。你也可以参考 [DM Release](https://github.com/pingcap/dm/releases) 页面。

| 安装包 | 操作系统 | 架构 | SHA256 校验和 |
|:---|:---|:---|:---|
| [dm-latest-linux-amd64.tar.gz](http://download.pingcap.org/dm-latest-linux-amd64.tar.gz) | Linux | amd64 | [dm-latest-linux-amd64.sha256](http://download.pingcap.org/dm-latest-linux-amd64.sha256) |

## Syncer，Loader 和 Mydumper

如需下载最新版本的 [Syncer](/v2.1/reference/tools/syncer.md)，[Loader](/v2.1/reference/tools/loader.md) 或 [Mydumper](/v2.1/reference/tools/mydumper.md)，直接下载 tidb-enterprise-tools 安装包即可，因为这些工具均包含在此安装包中。

| 安装包 | 操作系统 | 架构 | SHA256 校验和 |
|:---|:---|:---|:---|
| [tidb-enterprise-tools-latest-linux-amd64.tar.gz](http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.tar.gz) | Linux | amd64 | [tidb-enterprise-tools-latest-linux-amd64.sha256](http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.sha256) |

tidb-enterprise-tools 安装包包含以下工具：

- Syncer
- Loader
- Mydumper
- [binlogctl](/v2.1/reference/tools/tidb-binlog/overview.md#binlogctl-工具)
- ddl_checker
- [sync_diff_inspector](/v2.1/reference/tools/sync-diff-inspector/overview.md)
