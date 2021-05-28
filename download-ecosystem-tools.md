---
title: TiDB 工具下载
aliases: ['/docs-cn/stable/download-ecosystem-tools/','/docs-cn/v4.0/download-ecosystem-tools/','/docs-cn/stable/reference/tools/download/']
---

# TiDB 工具下载

本页面汇总了 TiDB 周边工具官方维护版本的下载链接。

## TiDB Binlog

如需下载最新版本的 [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)，直接下载 TiDB 安装包即可，因为 TiDB Binlog 包含在 TiDB 安装包中。

| 安装包 | 操作系统 | 架构 | SHA256 校验和 |
|:---|:---|:---|:---|
| `https://download.pingcap.org/tidb-{version}-linux-amd64.tar.gz` (TiDB Binlog) | Linux | amd64 | `https://download.pingcap.org/tidb-{version}-linux-amd64.sha256` |

> **注意：**
>
> 下载链接中的 `{version}` 为 TiDB 的版本号。例如，`v4.0.13` 版本的下载链接为 `https://download.pingcap.org/tidb-v4.0.13-linux-amd64.tar.gz`。

## TiDB Lightning

使用下表中的链接下载 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)：

| 安装包 | 操作系统 | 架构 | SHA256 校验和 |
|:---|:---|:---|:---|
| `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.tar.gz` | Linux | amd64 | `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.sha256` |

> **注意：**
>
> 下载链接中的 `{version}` 为 TiDB Lightning 的版本号。例如，`v4.0.13` 版本的下载链接为 `https://download.pingcap.org/tidb-toolkit-v4.0.13-linux-amd64.tar.gz`。

## 备份和恢复 (BR) 工具

使用下表中的链接下载 [BR 工具](/br/backup-and-restore-tool.md)：

| 安装包 | 操作系统 | 架构 | SHA256 校验和 |
|:---|:---|:---|:---|
| `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.tar.gz` | Linux | amd64 | `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.sha256` |

> **注意：**
>
> 下载链接中的 `{version}` 为 BR 的版本号。例如，`v4.0.13` 版本的下载链接为 `https://download.pingcap.org/tidb-toolkit-v4.0.13-linux-amd64.tar.gz`。

## TiDB DM (Data Migration)

使用下表中的链接下载 [DM](https://docs.pingcap.com/zh/tidb-data-migration/stable/overview)：

| 安装包 | 操作系统 | 架构 | SHA256 校验和 |
|:---|:---|:---|:---|
| `https://download.pingcap.org/dm-{version}-linux-amd64.tar.gz` | Linux | amd64 | `https://download.pingcap.org/dm-{version}-linux-amd64.sha256` |

> **注意：**
>
> 下载链接中的 `{version}` 为 DM 的版本号。例如，`v2.0.3` 版本的下载链接为 `https://download.pingcap.org/dm-v2.0.3-linux-amd64.tar.gz`。可以通过 [DM Release](https://github.com/pingcap/dm/releases) 查看当前已发布版本。

## Dumpling

使用下表中的链接下载 [Dumpling](/dumpling-overview.md):

| 安装包 | 操作系统 | 架构 | SHA256 校验和 |
|:---|:---|:---|:---|
| `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.tar.gz` | Linux | amd64 | `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.sha256` |

> **注意：**
>
> 下载链接中的 `{version}` 为 Dumpling 的版本号。例如，`v4.0.13` 版本的下载链接为 `https://download.pingcap.org/tidb-toolkit-v4.0.13-linux-amd64.tar.gz`。可以通过 [Dumpling Release](https://github.com/pingcap/dumpling/releases) 查看当前已发布版本。
> Dumpling 已支持 arm64 linux，将下载链接中的 amd64 替换为 arm64，即表示 arm64 版 Dumpling。

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
