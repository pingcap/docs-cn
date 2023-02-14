---
title: PingCAP Clinic Diagnostic Data
summary: Learn what diagnostic data can be collected by PingCAP Clinic Diagnostic Service from the TiDB and DM clusters deployed using TiUP.
---

# PingCAP Clinic Diagnostic Data

This document provides the types of diagnostic data that can be collected by PingCAP Clinic Diagnostic Service (PingCAP Clinic) from the TiDB and DM clusters deployed using TiUP. Also, the document lists the parameters for data collection corresponding to each data type. When running a command to [collect data using Diag client (Diag)](/clinic/clinic-user-guide-for-tiup.md), you can add the required parameters to the command according to the types of the data to be collected.

The diagnostic data collected by PingCAP Clinic is **only** used for troubleshooting cluster problems.

A diagnostic service deployed in the cloud, Clinic Server provides two independent services depending on the data storage location:

- [Clinic Server for international users](https://clinic.pingcap.com): If you upload the collected data to Clinic Server for international users, the data will be stored in the Amazon S3 service deployed by PingCAP in AWS US regions. PingCAP uses strict data access policies and only authorized technical support can access the data.
- [Clinic Server for users in the Chinese mainland](https://clinic.pingcap.com.cn): If you upload the collected data to Clinic Server for users in the Chinese mainland, the data will be stored in the Amazon S3 service deployed by PingCAP in China (Beijing) regions. PingCAP uses strict data access policies and only authorized technical support can access the data.

## TiDB clusters

This section lists the types of diagnostic data that can be collected by Diag from the TiDB clusters deployed using TiUP.

### TiDB cluster information

| Data type | Exported file | Parameter for data collection by PingCAP Clinic |
| :------ | :------ |:-------- |
| Basic information of the cluster, including the cluster ID | `cluster.json` | The data is collected per run by default. |
| Detailed information of the cluster | `meta.yaml` | The data is collected per run by default. |

### TiDB diagnostic data

| Data type | Exported file | Parameter for data collection by PingCAP Clinic |
| :------ | :------ |:-------- |
| Log | `tidb.log` | `--include=log` |
| Error log | `tidb_stderr.log` | `--include=log` |
| Slow log | `tidb_slow_query.log` | `--include=log` |
| Configuration file | `tidb.toml` | `--include=config` |
| Real-time configuration | `config.json` | `--include=config` |

### TiKV diagnostic data

| Data type | Exported file | Parameter for data collection by PingCAP Clinic |
| :------ | :------ |:-------- |
| Log | `tikv.log` | `--include=log` |
| Error log | `tikv_stderr.log` | `--include=log` |
| Configuration file | `tikv.toml` | `--include=config` |
| Real-time configuration | `config.json` | `--include=config` |

### PD diagnostic data

| Data type | Exported file | Parameter for data collection by PingCAP Clinic |
| :------ | :------ |:-------- |
| Log | `pd.log` | `--include=log` |
| Error log | `pd_stderr.log` | `--include=log` |
| Configuration file | `pd.toml` | `--include=config` |
| Real-time configuration | `config.json` | `--include=config` |
| Outputs of the command `tiup ctl:v<CLUSTER_VERSION> pd -u http://${pd IP}:${PORT} store` | `store.json` | `--include=config` |
| Outputs of the command `tiup ctl:v<CLUSTER_VERSION> pd -u http://${pd IP}:${PORT} config placement-rules show` | `placement-rule.json` | `--include=config` |

### TiFlash diagnostic data

| Data type | Exported file | Parameter for data collection by PingCAP Clinic |
| :------ | :------ |:-------- |
| Log | `tiflash.log` | `--include=log` |
| Error log | `tiflash_stderr.log` | `--include=log` |
| Configuration file |  `tiflash-learner.toml`, `tiflash-preprocessed.toml`, `tiflash.toml` | `--include=config` |
| Real-time configuration | `config.json` | `--include=config` |

### TiCDC diagnostic data

| Data type | Exported file | Parameter for data collection by PingCAP Clinic |
| :------ | :------ |:-------- |
| Log | `ticdc.log` | `--include=log`|
| Error log | `ticdc_stderr.log` | `--include=log` |
| Configuration file | `ticdc.toml` | `--include=config` |
| Debug data | `info.txt`, `status.txt`, `changefeeds.txt`, `captures.txt`, `processors.txt` | `--include=debug` (Diag does not collect this data type by default) |

### Prometheus monitoring data

| Data type | Exported file | Parameter for data collection by PingCAP Clinic |
| :------ | :------ |:-------- |
| All metrics data | `{metric_name}.json` | `--include=monitor` |
| All alerts data | `alerts.json` | `--include=monitor` |

### TiDB system variables

| Data type | Exported file | Parameter for data collection by PingCAP Clinic |
| :------ | :------ |:-------- |
| TiDB system variables | `mysql.tidb.csv` | `--include=db_vars` (Diag does not collect this data type by default; if you need to collect this data type, database credential is required) |
| | `global_variables.csv` | `--include=db_vars` (Diag does not collect this data type by default) |

### System information of the cluster node

| Data type | Exported file | Parameter for data collection by PingCAP Clinic |
| :------ | :------ |:-------- |
| Kernel log | `dmesg.log` | `--include=system` |
| Basic information of the system and hardware | `insight.json` | `--include=system` |
| Contents in the `/etc/security/limits.conf` | `limits.conf` | `--include=system` |
| List of kernel parameters | `sysctl.conf` | `--include=system` |
| Socket system information, which is the output of the `ss` command | `ss.txt` | `--include=system` |

## DM clusters

This section lists the types of diagnostic data that can be collected by Diag from the DM clusters deployed using TiUP.

### DM cluster information

| Data type | Exported file | Parameter for data collection by PingCAP Clinic |
| :------ | :------ |:-------- |
| Basic information of the cluster, including the cluster ID  | `cluster.json`| The data is collected per run by default. |
| Detailed information of the cluster | `meta.yaml` | The data is collected per run by default. |

### dm-master diagnostic data

| Data type | Exported file | Parameter for data collection by PingCAP Clinic |
| :------ | :------ |:-------- |
| Log | `m-master.log` | `--include=log` |
| Error log | `dm-master_stderr.log` | `--include=log` |
| Configuration file | `dm-master.toml` | `--include=config` |

### dm-worker diagnostic data

| Data type | Exported file | Parameter for data collection by PingCAP Clinic |
| :------ | :------ |:-------- |
| Log| `dm-worker.log` | `--include=log`|
| Error log | `dm-worker_stderr.log` | `--include=log` |
| Configuration file | `dm-work.toml` | `--include=config` |

### Prometheus monitoring data

| Data type | Exported file | Parameter for data collection by PingCAP Clinic |
| :------ | :------ |:-------- |
| All metrics data | `{metric_name}.json` | `--include=monitor` |
| All alerts data | `alerts.json` | `--include=monitor` |

### System information of the cluster node

| Data type | Exported file | Parameter for data collection by PingCAP Clinic |
| :------ | :------ |:-------- |
| Kernel log | `dmesg.log` | `--include=system` |
| Basic information of the system and hardware | `insight.json` | `--include=system` |
| Contents in the `/etc/security/limits.conf` system | `limits.conf` | `--include=system` |
| List of kernel parameters | `sysctl.conf` | `--include=system` |
| Socket system information, which is the output of the `ss` command | `ss.txt` | `--include=system` |
