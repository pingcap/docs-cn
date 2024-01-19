---
title: TiDB 离线包
summary: 了解 TiDB 离线包及其包含的内容。
---

# TiDB 离线包

在[使用 TiUP 离线部署 TiDB](/production-deployment-using-tiup.md#离线部署) 前，你需要在[官方下载页面](https://pingcap.com/zh/product#SelectProduct)选择对应版本的 TiDB server 离线镜像包（包含 TiUP 离线组件包）。

TiDB 提供了 amd64 和 arm64 两种架构的离线包。对于每种架构，TiDB 提供了两个二进制离线包：`TiDB-community-server` 软件包和 `TiDB-community-toolkit` 软件包。

`TiDB-community-server` 软件包中包含以下内容：

| 内容 | 变更说明 |
|---|---|
| tidb-{version}-linux-{arch}.tar.gz |  |
| tikv-{version}-linux-{arch}.tar.gz |  |
| tiflash-{version}-linux-{arch}.tar.gz |  |
| pd-{version}-linux-{arch}.tar.gz |  |
| ctl-{version}-linux-{arch}.tar.gz |  |
| grafana-{version}-linux-{arch}.tar.gz |  |
| alertmanager-{version}-linux-{arch}.tar.gz |  |
| blackbox_exporter-{version}-linux-{arch}.tar.gz |  |
| prometheus-{version}-linux-{arch}.tar.gz |  |
| node_exporter-{version}-linux-{arch}.tar.gz |  |
| tiup-linux-{arch}.tar.gz |  |
| tiup-{version}-linux-{arch}.tar.gz |  |
| local_install.sh |  |
| cluster-{version}-linux-{arch}.tar.gz |  |
| insight-{version}-linux-{arch}.tar.gz |  |
| diag-{version}-linux-{arch}.tar.gz | 从 v6.0.0 起新增 |
| influxdb-{version}-linux-{arch}.tar.gz |  |
| playground-{version}-linux-{arch}.tar.gz |  |
| tiproxy-{version}-linux-{arch}.tar.gz | 从 v7.6.0 起新增 |

> **注意：**
>
> 以上离线包名称中，`{version}` 取决于离线包中内容的版本号，`{arch}` 取决于离线包对应的架构（amd64 或 arm64）。

`TiDB-community-toolkit` 软件包中包含以下内容：

| 内容 | 变更说明 |
|---|---|
| pd-recover-{version}-linux-{arch}.tar.gz |  |
| etcdctl | 从 v6.0.0 起新增 |
| tiup-linux-{arch}.tar.gz |  |
| tiup-{version}-linux-{arch}.tar.gz |  |
| tidb-lightning-{version}-linux-{arch}.tar.gz |  |
| tidb-lightning-ctl |  |
| dumpling-{version}-linux-{arch}.tar.gz |  |
| cdc-{version}-linux-{arch}.tar.gz |  |
| dm-{version}-linux-{arch}.tar.gz |  |
| dm-worker-{version}-linux-{arch}.tar.gz |  |
| dm-master-{version}-linux-{arch}.tar.gz |  |
| dmctl-{version}-linux-{arch}.tar.gz |  |
| br-{version}-linux-{arch}.tar.gz |  |
| package-{version}-linux-{arch}.tar.gz |  |
| bench-{version}-linux-{arch}.tar.gz |  |
| errdoc-{version}-linux-{arch}.tar.gz |  |
| dba-{version}-linux-{arch}.tar.gz |  |
| PCC-{version}-linux-{arch}.tar.gz |  |
| pump-{version}-linux-{arch}.tar.gz |  |
| drainer-{version}-linux-{arch}.tar.gz |  |
| binlogctl | 从 v6.0.0 起新增 |
| sync_diff_inspector |  |
| reparo |  |
| arbiter |  |
| server-{version}-linux-{arch}.tar.gz | 从 v6.2.0 起新增 |
| grafana-{version}-linux-{arch}.tar.gz | 从 v6.2.0 起新增 |
| alertmanager-{version}-linux-{arch}.tar.gz | 从 v6.2.0 起新增 |
| prometheus-{version}-linux-{arch}.tar.gz | 从 v6.2.0 起新增  |
| blackbox_exporter-{version}-linux-{arch}.tar.gz | 从 v6.2.0 起新增 |
| node_exporter-{version}-linux-{arch}.tar.gz | 从 v6.2.0 起新增 |

> **注意：**
>
> 以上离线包名称中，`{version}` 取决于离线包中工具的版本号，`{arch}` 取决于离线包对应的架构（amd64 或 arm64）。

## 延伸阅读

[离线部署 TiDB 集群](/production-deployment-using-tiup.md#离线部署)
