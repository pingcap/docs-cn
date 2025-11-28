---
title: TiDB 离线包
summary: 了解 TiDB 离线包及其包含的内容。
---

# TiDB 离线包

在[使用 TiUP 离线部署 TiDB](/production-deployment-using-tiup.md#离线部署) 前，你需要在[软件下载中心](https://pingkai.cn/download#tidb-community)选择对应版本的 TiDB server 离线镜像包（包含 TiUP 离线组件包）。

TiDB 提供两个二进制离线包：`TiDB-community-server` 软件包和 `TiDB-community-toolkit` 软件包。

`TiDB-community-server` 软件包中包含以下内容：

| 内容 | 变更说明 |
|---|---|
| tidb-{version}-linux-amd64.tar.gz |  |
| tikv-{version}-linux-amd64.tar.gz |  |
| tiflash-{version}-linux-amd64.tar.gz |  |
| pd-{version}-linux-amd64.tar.gz |  |
| ctl-{version}-linux-amd64.tar.gz |  |
| grafana-{version}-linux-amd64.tar.gz |  |
| alertmanager-{version}-linux-amd64.tar.gz |  |
| blackbox_exporter-{version}-linux-amd64.tar.gz |  |
| prometheus-{version}-linux-amd64.tar.gz |  |
| node_exporter-{version}-linux-amd64.tar.gz |  |
| tiup-linux-amd64.tar.gz |  |
| tiup-{version}-linux-amd64.tar.gz |  |
| local_install.sh |  |
| cluster-{version}-linux-amd64.tar.gz |  |
| insight-{version}-linux-amd64.tar.gz |  |
| diag-{version}-linux-amd64.tar.gz | 从 v6.0.0 起新增 |
| influxdb-{version}-linux-amd64.tar.gz |  |
| playground-{version}-linux-amd64.tar.gz |  |

`TiDB-community-toolkit` 软件包中包含以下内容：

| 内容 | 变更说明 |
|---|---|
| tikv-importer-{version}-linux-amd64.tar.gz |  |
| pd-recover-{version}-linux-amd64.tar.gz |  |
| etcdctl | 从 v6.0.0 起新增 |
| tiup-linux-amd64.tar.gz |  |
| tiup-{version}-linux-amd64.tar.gz |  |
| tidb-lightning-{version}-linux-amd64.tar.gz |  |
| tidb-lightning-ctl |  |
| dumpling-{version}-linux-amd64.tar.gz |  |
| cdc-{version}-linux-amd64.tar.gz |  |
| dm-{version}-linux-amd64.tar.gz |  |
| dm-worker-{version}-linux-amd64.tar.gz |  |
| dm-master-{version}-linux-amd64.tar.gz |  |
| dmctl-{version}-linux-amd64.tar.gz |  |
| br-{version}-linux-amd64.tar.gz |  |
| spark-{version}-any-any.tar.gz |  |
| tispark-{version}-any-any.tar.gz |  |
| package-{version}-linux-amd64.tar.gz |  |
| bench-{version}-linux-amd64.tar.gz |  |
| errdoc-{version}-linux-amd64.tar.gz |  |
| dba-{version}-linux-amd64.tar.gz |  |
| PCC-{version}-linux-amd64.tar.gz |  |
| pump-{version}-linux-amd64.tar.gz |  |
| drainer-{version}-linux-amd64.tar.gz |  |
| binlogctl | 从 v6.0.0 起新增 |
| sync_diff_inspector |  |
| reparo |  |
| arbiter |  |
| mydumper | 从 v6.0.0 起新增 |
| server-{version}-linux-amd64.tar.gz | 从 v6.1.1 起新增 |
| grafana-{version}-linux-amd64.tar.gz | 从 v6.1.1 起新增 |
| alertmanager-{version}-linux-amd64.tar.gz | 从 v6.1.1 起新增 |
| prometheus-{version}-linux-amd64.tar.gz | 从 v6.1.1 起新增 |
| blackbox_exporter-{version}-linux-amd64.tar.gz | 从 v6.1.1 起新增 |
| node_exporter-{version}-linux-amd64.tar.gz | 从 v6.1.1 起新增 |

## 延伸阅读

[离线部署 TiDB 集群](/production-deployment-using-tiup.md#离线部署)
