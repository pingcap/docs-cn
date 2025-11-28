---
title: TiDB 工具下载
---

# TiDB 工具下载

本文介绍如何下载 TiDB 工具包以及 [TiUniManager](/tiunimanager/tiunimanager-overview.md)。关于 TiDB 工具包的内容，请查看 [TiDB 离线包](/binary-package.md)。

## TiDB 工具包下载

TiDB 工具包中包含了一些常用的 TiDB 工具，例如数据导出工具 Dumpling、数据导入工具 TiDB Lightning、备份恢复工具 BR。

> **建议：**
>
> 如果你的部署环境能访问互联网，无需单独下载 TiDB 工具包，可以直接通过使用 [TiUP 命令一键部署](/tiup/tiup-component-management.md)所需的 TiDB 工具。

### 环境要求

- 操作系统：Linux
- 架构：amd64

### 下载步骤

1. 访问[软件下载中心](https://pingkai.cn/download#tidb-community)页面。
2. 选择你所需的 TiDB 版本和架构，选择 **TiDB 工具集 TiDB-community-toolkit**，确认隐私政策，然后点击**立即下载**。

> **注意：**
>
> - 如需在 Kubernetes 上部署运维 TiDB，无需下载 TiDB-community-toolkit 软件包，请参考[离线安装 TiDB Operator](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/deploy-tidb-operator#离线安装-tidb-operator)。
> - 如需使用 [PD Control](/pd-control.md) 工具 `pd-ctl`，请下载 **TiDB-community-server 软件包**。

### TiDB 工具包说明

在 TiDB 工具包中，你可以依据要使用的工具，选择安装对应的离线包。

| 工具  | 离线包名称  |
|:------|:----------|
| [TiUP](/tiup/tiup-overview.md)  | `tiup-linux-amd64.tar.gz` <br/>`tiup-{tiup-version}-linux-amd64.tar.gz` <br/>`dm-{tiup-version}-linux-amd64.tar.gz` <br/> `server-{version}-linux-amd64.tar.gz` |
| [Dumpling](/dumpling-overview.md)  | `dumpling-{version}-linux-amd64.tar.gz`  |
| [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)  | `tidb-lightning-ctl` <br/>`tidb-lightning-{version}-linux-amd64.tar.gz`  |
| [TiDB DM (Data Migration)](/dm/dm-overview.md)  | `dm-worker-{version}-linux-amd64.tar.gz` <br/>`dm-master-{version}-linux-amd64.tar.gz` <br/>`dmctl-{version}-linux-amd64.tar.gz`  |
| [TiCDC](/ticdc/ticdc-overview.md)  | `cdc-{version}-linux-amd64.tar.gz`  |
| [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)  | `pump-{version}-linux-amd64.tar.gz` <br/>`drainer-{version}-linux-amd64.tar.gz` <br/>`binlogctl` <br/>`reparo`  |
| [Backup & Restore (BR)](/br/backup-and-restore-overview.md)  | `br-{version}-linux-amd64.tar.gz`  |
| [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md)  | `sync_diff_inspector`  |
| [TiSpark](/tispark-overview.md)  | `tispark-{tispark-version}-any-any.tar.gz` <br/>`spark-{spark-version}-any-any.tar.gz`  |
| [PD Recover](/pd-recover.md)  | `pd-recover-{version}-linux-amd64.tar.gz` |

## TiUniManager 下载

[TiUniManager](/tiunimanager/tiunimanager-overview.md) 是为 TiDB 打造的管控平台软件和数据库运维管理平台。使用下表中的链接下载 TiUniManager：

| 安装包 | 操作系统 | 架构 | SHA256 校验和 |
|:---|:---|:---|:---|
| `https://download.pingcap.org/em-enterprise-server-{version}-linux-amd64.tar.gz` | Linux | amd64 | `https://download.pingcap.org/em-enterprise-server-{version}-linux-amd64.sha256` |

> **注意：**
>
> - 下载链接中的 `{version}` 为 TiUniManager 的版本号。例如，`v1.0.2` 版本的下载链接为 `https://download.pingcap.org/em-enterprise-server-v1.0.2-linux-amd64.tar.gz`。
> - TiUniManager 从 v1.0.2 起开放源代码，因此下载链接中 `{version}` 支持的最低版本为 `v1.0.2`。你不能将 `{version}` 替换为 `v1.0.0` 或 `v1.0.1`。
