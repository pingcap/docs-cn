---
title: TiDB 工具下载
---

# TiDB 工具下载

本页面汇总了 TiDB 工具官方维护版本的下载链接。

## TiUP

TiUP 安装过程十分简洁，无论是 Darwin 还是 Linux 操作系统，执行一行命令即可安装成功。详情请参考[安装 TiUP](/tiup/tiup-overview.md#安装-tiup)。

## TiDB Operator

TiDB Operator 运行在 Kubernetes 集群。在搭建好 Kubernetes 集群后，你可以选择在线或者离线部署 TiDB Operator。详情请参考[在 Kubernetes 上部署 TiDB Operator](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/deploy-tidb-operator)。

## TiDB Binlog

如需下载最新版本的 [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)，直接下载 TiDB 安装包即可，因为 TiDB Binlog 包含在 TiDB 安装包中。

| 安装包 | 操作系统 | 架构 | SHA256 校验和 |
|:---|:---|:---|:---|
| `https://download.pingcap.org/tidb-{version}-linux-amd64.tar.gz` (TiDB Binlog) | Linux | amd64 | `https://download.pingcap.org/tidb-{version}-linux-amd64.sha256` |

> **注意：**
>
> 下载链接中的 `{version}` 为 TiDB 的版本号。例如，`v5.4.3` 版本的下载链接为 `https://download.pingcap.org/tidb-v5.4.3-linux-amd64.tar.gz`。

## TiDB Lightning

使用下表中的链接下载 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)：

| 安装包 | 操作系统 | 架构 | SHA256 校验和 |
|:---|:---|:---|:---|
| `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.tar.gz` | Linux | amd64 | `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.sha256` |

> **注意：**
>
> 下载链接中的 `{version}` 为 TiDB Lightning 的版本号。例如，`v5.4.3` 版本的下载链接为 `https://download.pingcap.org/tidb-toolkit-v5.4.3-linux-amd64.tar.gz`。

## 备份和恢复 (BR) 工具

使用下表中的链接下载 [BR 工具](/br/backup-and-restore-tool.md)：

| 安装包 | 操作系统 | 架构 | SHA256 校验和 |
|:---|:---|:---|:---|
| `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.tar.gz` | Linux | amd64 | `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.sha256` |

> **注意：**
>
<<<<<<< HEAD
> 下载链接中的 `{version}` 为 BR 的版本号。例如，`v5.4.3` 版本的下载链接为 `https://download.pingcap.org/tidb-toolkit-v5.4.3-linux-amd64.tar.gz`。

## TiDB DM (Data Migration)

使用下表中的链接下载 [DM](/dm/dm-overview.md)：

| 安装包 | 操作系统 | 架构 | SHA256 校验和 |
|:---|:---|:---|:---|
| `https://download.pingcap.org/dm-{version}-linux-amd64.tar.gz` | Linux | amd64 | `https://download.pingcap.org/dm-{version}-linux-amd64.sha256` |

> **注意：**
>
> 下载链接中的 `{version}` 为 DM 的版本号。例如，`v5.4.3` 版本的下载链接为 `https://download.pingcap.org/dm-v5.4.3-linux-amd64.tar.gz`。可以通过 [DM Release](https://github.com/pingcap/tiflow/releases) 查看当前已发布版本。

## Dumpling

使用下表中的链接下载 [Dumpling](/dumpling-overview.md):

| 安装包 | 操作系统 | 架构 | SHA256 校验和 |
|:---|:---|:---|:---|
| `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.tar.gz` | Linux | amd64 | `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.sha256` |
=======
> - 点击**立即下载**后，默认下载当前 TiDB 的最新发布版本。如需下载其它版本，请在 [TiDB 社区版](https://pingcap.com/zh/product-community/)页面底部查看其它版本下载信息。
> - 如需在 Kubernetes 上部署运维 TiDB，无需下载 TiDB-community-toolkit 软件包，请参考[离线安装 TiDB Operator](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/deploy-tidb-operator#离线安装-tidb-operator)。
> - 如需使用 [PD Control](/pd-control.md) 工具 `pd-ctl`，请下载 **TiDB-community-server 软件包**。

### TiDB 工具包说明

在 TiDB 工具包中，你可以依据要使用的工具，选择安装对应的离线包。

| 工具  | 离线包名称  |
|:------|:----------|
| [TiUP](/tiup/tiup-overview.md)  | `tiup-linux-{arch}.tar.gz` <br/>`tiup-{tiup-version}-linux-{arch}.tar.gz` <br/>`dm-{tiup-version}-linux-{arch}.tar.gz` <br/> `server-{version}-linux-{arch}.tar.gz` |
| [Dumpling](/dumpling-overview.md)  | `dumpling-{version}-linux-{arch}.tar.gz`  |
| [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)  | `tidb-lightning-ctl` <br/>`tidb-lightning-{version}-linux-{arch}.tar.gz`  |
| [TiDB DM (Data Migration)](/dm/dm-overview.md)  | `dm-worker-{version}-linux-{arch}.tar.gz` <br/>`dm-master-{version}-linux-{arch}.tar.gz` <br/>`dmctl-{version}-linux-{arch}.tar.gz`  |
| [TiCDC](/ticdc/ticdc-overview.md)  | `cdc-{version}-linux-{arch}.tar.gz`  |
| [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)  | `pump-{version}-linux-{arch}.tar.gz` <br/>`drainer-{version}-linux-{arch}.tar.gz` <br/>`binlogctl` <br/>`reparo`  |
| [Backup & Restore (BR)](/br/backup-and-restore-overview.md)  | `br-{version}-linux-{arch}.tar.gz`  |
| [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md)  | `sync_diff_inspector`  |
| [TiSpark](/tispark-overview.md)  | `tispark-{tispark-version}-any-any.tar.gz` <br/>`spark-{spark-version}-any-any.tar.gz`  |
| [PD Recover](/pd-recover.md)  | `pd-recover-{version}-linux-{arch}.tar.gz` |
>>>>>>> 2c36b1690 (Keep the download description consistent with the product-community (#12065))

> **注意：**
>
> - 下载链接中的 `{version}` 为 Dumpling 的版本号。例如，`v5.4.3` 版本的下载链接为 `https://download.pingcap.org/tidb-toolkit-v5.4.3-linux-amd64.tar.gz`。可以通过 [TiDB Release](https://github.com/pingcap/tidb/releases) 查看当前已发布版本。
> - Dumpling 已支持 arm64 linux，将下载链接中的 amd64 替换为 arm64，即表示 arm64 版 Dumpling。

## sync-diff-inspector

使用下表中的链接下载 [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md):

| 安装包 | 操作系统 | 架构 | SHA256 校验和 |
|:---|:---|:---|:---|
| [tidb-enterprise-tools-nightly-linux-amd64.tar.gz](https://download.pingcap.org/tidb-enterprise-tools-nightly-linux-amd64.tar.gz) | Linux | amd64 | [tidb-enterprise-tools-nightly-linux-amd64.sha256](https://download.pingcap.org/tidb-enterprise-tools-nightly-linux-amd64.sha256) |

## TiCDC

[TiCDC](/ticdc/ticdc-overview.md) 的下载方式见 [TiCDC 安装部署文档](/ticdc/deploy-ticdc.md)。

## TiUniManager 下载

[TiUniManager](https://docs.pingcap.com/zh/tidb/stable/tiunimanager-overview) 是为 TiDB 打造的管控平台软件和数据库运维管理平台。使用下表中的链接下载 TiUniManager：

| 安装包 | 操作系统 | 架构 | SHA256 校验和 |
|:---|:---|:---|:---|
| `https://download.pingcap.org/em-enterprise-server-{version}-linux-amd64.tar.gz` | Linux | amd64 | `https://download.pingcap.org/em-enterprise-server-{version}-linux-amd64.sha256` |

> **注意：**
>
> - 下载链接中的 `{version}` 为 TiUniManager 的版本号。例如，`v1.0.2` 版本的下载链接为 `https://download.pingcap.org/em-enterprise-server-v1.0.2-linux-amd64.tar.gz`。
> - TiUniManager 从 v1.0.2 起开放源代码，因此下载链接中 `{version}` 支持的最低版本为 `v1.0.2`。你不能将 `{version}` 替换为 `v1.0.0` 或 `v1.0.1`。
