---
title: TiDB 工具下载
category: reference
aliases: ['/docs-cn/stable/reference/tools/download/']
---

# TiDB 工具下载

本页面汇总了 TiDB 周边工具官方维护版本的下载链接。

## TiDB Binlog

如需下载最新版本的 [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)，直接下载 TiDB 安装包即可，因为 TiDB Binlog 包含在 TiDB 安装包中。

以下表格中也提供了 Kafka 版本的 TiDB Binlog 下载链接。

| 安装包 | 操作系统 | 架构 | SHA256 校验和 |
|:---|:---|:---|:---|
| `https://download.pingcap.org/tidb-{version}-linux-amd64.tar.gz` (TiDB Binlog) | Linux | amd64 | `https://download.pingcap.org/tidb-{version}-linux-amd64.sha256` |
| `https://download.pingcap.org/tidb-binlog-kafka-linux-amd64.tar.gz`（Kafka 版本的 TiDB Binlog）| Linux | amd64 | `https://download.pingcap.org/tidb-binlog-kafka-linux-amd64.sha256` |

> **注意：**
>
> 下载链接中的 `{version}` 为 TiDB 的版本号。例如，`v3.0.5` 版本的下载链接为 `https://download.pingcap.org/tidb-v3.0.5-linux-amd64.tar.gz`。

## TiDB Lightning

使用下表中的链接下载 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)：

| 安装包 | 操作系统 | 架构 | SHA256 校验和 |
|:---|:---|:---|:---|
| `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.tar.gz` | Linux | amd64 | `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.sha256` |

> **注意：**
>
> 下载链接中的 `{version}` 为 TiDB Lightning 的版本号。例如，`v3.0.5` 版本的下载链接为 `https://download.pingcap.org/tidb-toolkit-v3.0.5-linux-amd64.tar.gz`。

## 快速备份和恢复（BR）

使用下表中的链接下载 [快速备份和恢复（BR）](/br/backup-and-restore-tool.md)：

| 安装包 | 操作系统 | 架构 | SHA256 校验和 |
|:---|:---|:---|:---|
| `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.tar.gz` | Linux | amd64 | `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.sha256` |

> **注意：**
>
> 下载链接中的 `{version}` 为 BR 的版本号。例如，`v3.1.0-beta` 版本的下载链接为 `https://download.pingcap.org/tidb-toolkit-v3.1.0-beta-linux-amd64.tar.gz`。

## TiDB DM (Data Migration)

使用下表中的链接下载 [DM](https://docs.pingcap.com/zh/tidb-data-migration/v1.0/overview)：

| 安装包 | 操作系统 | 架构 | SHA256 校验和 |
|:---|:---|:---|:---|
| `https://download.pingcap.org/dm-{version}-linux-amd64.tar.gz` | Linux | amd64 | `https://download.pingcap.org/dm-{version}-linux-amd64.sha256` |

> **注意：**
>
> 下载链接中的 `{version}` 为 DM 的版本号。例如，`v1.0.1` 版本的下载链接为 `https://download.pingcap.org/dm-v1.0.1-linux-amd64.tar.gz`。可以通过 [DM Release](https://github.com/pingcap/dm/releases) 查看当前已发布版本。

## Syncer，Loader 和 Mydumper

如需下载最新版本的 [Syncer](/syncer-overview.md)，[Loader](/loader-overview.md) 或 [Mydumper](/mydumper-overview.md)，直接下载 tidb-enterprise-tools 安装包即可，因为这些工具均包含在此安装包中。

| 安装包 | 操作系统 | 架构 | SHA256 校验和 |
|:---|:---|:---|:---|
| [tidb-enterprise-tools-nightly-linux-amd64.tar.gz](https://download.pingcap.org/tidb-enterprise-tools-nightly-linux-amd64.tar.gz) | Linux | amd64 | [tidb-enterprise-tools-nightly-linux-amd64.sha256](https://download.pingcap.org/tidb-enterprise-tools-nightly-linux-amd64.sha256) |

tidb-enterprise-tools 安装包包含以下工具：

- Syncer
- Loader
- Mydumper
- ddl_checker
- [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md)
