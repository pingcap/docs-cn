---
title: TiDB 工具下载
summary: 本文介绍如何下载 TiDB 工具包。TiDB 工具包包含常用工具如 Dumpling、TiDB Lightning、BR 等。如果部署环境能访问互联网，可直接通过 TiUP 命令一键部署所需的 TiDB 工具。操作系统需为 Linux，架构为 amd64 或 arm64。下载步骤包括访问 TiDB 社区版页面，找到 TiDB-community-toolkit 软件包并点击立即下载。注意，点击立即下载后默认下载当前 TiDB 的最新发布版本。根据要使用的工具选择安装对应的离线包。
---

# TiDB 工具下载

本文介绍如何下载 TiDB 工具包。关于 TiDB 工具包的内容，请查看 [TiDB 离线包](/binary-package.md)。

## TiDB 工具包下载

TiDB 工具包中包含了一些常用的 TiDB 工具，例如数据导出工具 Dumpling、数据导入工具 TiDB Lightning、备份恢复工具 BR。

> **建议：**
>
> 如果你的部署环境能访问互联网，无需单独下载 TiDB 工具包，可以直接通过使用 [TiUP 命令一键部署](/tiup/tiup-component-management.md)所需的 TiDB 工具。

### 环境要求

- 操作系统：Linux
- 架构：amd64 或 arm64

### 下载步骤

1. 访问 [TiDB 社区版](https://pingcap.com/zh/product-community/)页面。
2. 找到 **TiDB-community-toolkit 软件包**，点击**立即下载**。

> **注意：**
>
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
| [Backup & Restore (BR)](/br/backup-and-restore-overview.md)  | `br-{version}-linux-{arch}.tar.gz`  |
| [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md)  | `sync_diff_inspector`  |
| [PD Recover](/pd-recover.md)  | `pd-recover-{version}-linux-{arch}.tar.gz` |

> **注意：**
>
> 以上离线包名称中，`{version}` 取决于离线包中工具的版本号，`{arch}` 取决于离线包对应的架构（amd64 或 arm64）。
