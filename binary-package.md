---
title: TiDB Installation Packages
summary: Learn about TiDB installation packages and the specific components included.
---

# TiDB Installation Packages

Before [deploying TiUP offline](/production-deployment-using-tiup.md#deploy-tiup-offline), you need to download the binary packages of TiDB at the [official download page](https://en.pingcap.com/download/).

TiDB binary packages are available in amd64 and arm64 architectures. In either architecture, TiDB provides two binary packages: `TiDB-community-server` and `TiDB-community-toolkit`.

The `TiDB-community-server` package contains the following contents.

| Content | Change history |
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
| diag-{version}-linux-{arch}.tar.gz | New in v6.0.0 |
| influxdb-{version}-linux-{arch}.tar.gz |  |
| playground-{version}-linux-{arch}.tar.gz |  |

> **Note:**
>
> `{version}` depends on the version of the component or server you are installing. `{arch}` depends on the architecture of the system, which can be `amd64` or `arm64`.

The `TiDB-community-toolkit` package contains the following contents.

| Content | Change history |
|---|---|
| pd-recover-{version}-linux-{arch}.tar.gz |  |
| etcdctl | New in v6.0.0 |
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
| binlogctl | New in v6.0.0 |
| sync_diff_inspector |  |
| reparo |  |
| arbiter |  |
| server-{version}-linux-{arch}.tar.gz | New in v6.2.0 |
| grafana-{version}-linux-{arch}.tar.gz | New in v6.2.0 |
| alertmanager-{version}-linux-{arch}.tar.gz | New in v6.2.0 |
| prometheus-{version}-linux-{arch}.tar.gz | New in v6.2.0 |
| blackbox_exporter-{version}-linux-{arch}.tar.gz | New in v6.2.0  |
| node_exporter-{version}-linux-{arch}.tar.gz | New in v6.2.0  |

> **Note:**
>
> `{version}` depends on the version of the tool you are installing. `{arch}` depends on the architecture of the system, which can be `amd64` or `arm64`.

## See also

[Deploy TiUP offline](/production-deployment-using-tiup.md#deploy-tiup-offline)
