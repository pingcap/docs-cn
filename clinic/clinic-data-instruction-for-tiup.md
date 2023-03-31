---
title: PingCAP Clinic 数据采集说明
summary: 详细说明 PingCAP Clinic 诊断服务在使用 TiUP 部署的 TiDB 集群和 DM 集群中能够采集哪些诊断数据。
---

# PingCAP Clinic 数据采集说明

本文提供了 PingCAP Clinic 诊断服务（以下简称为 PingCAP Clinic）在使用 TiUP 部署的 TiDB 集群和 DM 集群中能够采集的诊断数据类型，并列出了各个采集项对应的采集参数。当[执行 Clinic Diag 诊断客户端（以下简称为 Diag）数据采集命令](/clinic/clinic-user-guide-for-tiup.md)时，你可以依据需要采集的数据类型，在命令中添加所需的采集参数。

通过 PingCAP Clinic 在使用 TiUP 部署的集群中采集的数据**仅**用于诊断和分析集群问题。

Clinic Server 是部署在云端的云服务，根据数据存储的位置不同，分为以下两个独立的服务：

- [Clinic Server 中国区](https://clinic.pingcap.com.cn)：如果你把采集的数据上传到了 Clinic Server 中国区，这些数据将存储于 PingCAP 设立在 AWS 中国区（北京）的 S3 服务。PingCAP 对数据访问权限进行了严格的访问控制，只有经授权的内部技术人员可以访问该数据。
- [Clinic Server 美国区](https://clinic.pingcap.com)：如果你把采集的数据上传到了 Clinic Server 美国区，这些数据将存储于 PingCAP 设立在 AWS 美国区的 S3 服务。PingCAP 对数据访问权限进行了严格的访问控制，只有经授权的内部技术人员可以访问该数据。

## TiDB 集群

本节列出了 [Diag](https://github.com/pingcap/diag) 在使用 TiUP 部署的 TiDB 集群中能够采集的诊断数据类型。

### TiDB 集群信息

| 诊断数据类型 | 输出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 集群基础信息，包括集群 ID | `cluster.json` | 每次收集默认采集 |
| 集群详细信息 | `meta.yaml` | 每次收集默认采集 |

### TiDB 诊断数据

| 诊断数据类型 | 输出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 日志 | `tidb.log` | `--include=log` |
| Error 日志 | `tidb_stderr.log` | `--include=log` |
| 慢日志| `tidb_slow_query.log` | `--include=log` |
| 配置文件 | `tidb.toml` | `--include=config` |
| 实时配置| `config.json` | `--include=config` |

### TiKV 诊断数据

| 诊断数据类型 | 输出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 日志 | `tikv.log` | `--include=log` |
| Error 日志 | `tikv_stderr.log` | `--include=log` |
| 配置文件 | `tikv.toml` | `--include=config` |
| 实时配置 | `config.json` | `--include=config` |

### PD 诊断数据

| 诊断数据类型 | 输出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 日志 | `pd.log` | `--include=log` |
| Error 日志 | `pd_stderr.log` | `--include=log` |
| 配置文件 | `pd.toml` | `--include=config` |
| 实时配置 | `config.json` | `--include=config` |
| `tiup ctl:v<CLUSTER_VERSION> pd -u http://${pd IP}:${PORT} store` 的输出结果 | `store.json` | `--include=config` |
| `tiup ctl:v<CLUSTER_VERSION> pd -u http://${pd IP}:${PORT} config placement-rules show` 的输出结果 | `placement-rule.json` | `--include=config` |

### TiFlash 诊断数据

| 诊断数据类型 | 输出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 日志 | `tiflash.log` | `--include=log` |
| Error 日志 | `tiflash_stderr.log` | `--include=log` |
| 配置文件 |  `tiflash-learner.toml`，`tiflash-preprocessed.toml`，`tiflash.toml` | `--include=config` |
| 实时配置 | `config.json` | `--include=config` |

### TiCDC 诊断数据

| 诊断数据类型 | 输出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 日志 | `ticdc.log` | `--include=log`|
| Error 日志 | `ticdc_stderr.log` | `--include=log` |
| 配置文件 | `ticdc.toml` | `--include=config` |
| Debug 数据 | `info.txt`，`status.txt`，`changefeeds.txt`，`captures.txt`，`processors.txt` | `--include=debug`（默认不采集）|

### Prometheus 监控数据

| 诊断数据类型 | 输出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 所有的 Metrics 数据 | `{metric_name}.json` | `--include=monitor` |
| Alert 列表 | `alerts.json` | `--include=monitor` |

### TiDB 系统变量

| 诊断数据类型 | 输出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 获取 TiDB 系统变量（默认不采集，采集需要额外提供数据库账号） | `mysql.tidb.csv` | `--include=db_vars`（默认不采集） |
| | `global_variables.csv` | `--include=db_vars`（默认不采集）|

### 集群节点的系统信息

| 诊断数据类型 | 输出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 内核日志 | `dmesg.log` | `--include=system` |
| 系统和硬件的基础信息 | `insight.json` | `--include=system` |
| 系统 `/etc/security/limits.conf` 中的内容 | `limits.conf` | `--include=system` |
| 内核参数列表 | `sysctl.conf` | `--include=system` |
| socket 统计信息（即 ss 的命令结果） | `ss.txt` | `--include=system` |

## DM 集群

本节列出了 Diag 在使用 TiUP 部署的 DM 集群中能够采集的诊断数据类型。

### DM 集群信息

| 诊断数据类型 | 输出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 集群基础信息，包括集群 ID | `cluster.json`| 每次收集默认采集 |
| 集群详细信息 | `meta.yaml` | 每次收集默认采集 |

### dm-master 诊断数据

| 诊断数据类型 | 输出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 日志 | `m-master.log` | `--include=log` |
| Error 日志 | `dm-master_stderr.log` | `--include=log` |
| 配置文件 | `dm-master.toml` | `--include=config` |

### dm-worker 诊断数据

| 诊断数据类型 | 输出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 日志| `dm-worker.log` | `--include=log`|
| Error 日志 | `dm-worker_stderr.log` | `--include=log` |
| 配置文件 | `dm-work.toml` | `--include=config` |

### Prometheus 监控数据

| 诊断数据类型 | 输出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 所有的 Metrics 数据 | `{metric_name}.json` | `--include=monitor` |
| Alert 列表 | `alerts.json` | `--include=monitor` |

### 集群节点的系统信息

| 诊断数据类型 | 输出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 内核日志 | `dmesg.log` | `--include=system` |
| 系统和硬件基础信息 | `insight.json` | `--include=system` |
| 系统 `/etc/security/limits.conf` 中的内容 | `limits.conf` | `--include=system` |
| 内核参数列表 | `sysctl.conf` | `--include=system` |
| socket 统计信息（即 ss 的命令结果） | `ss.txt` | `--include=system` |
