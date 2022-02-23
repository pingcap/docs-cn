---
title: Clinic 数据采集说明
summary: 详细说明 Clinic 诊断服务会在使用 TiUP 部署的集群中采集哪些诊断数据。
---

# Clinic 数据采集说明

本文提供了 Clinic 诊断服务在使用 TiUP 部署的集群中的数据采集范围，并列出了各个采集项对应的采集参数。当执行 Clinic Diag 诊断工具（以下简称为 Diag）数据采集命令时，你可以依据所需采集的数据范围，在命令中配置所需的采集参数。

通过 Clinic 诊断服务对使用 TiUP 部署的集群采集的数据**仅**用于集群问题诊断与分析。

Clinic Server 位于 PingCAP 内网（中国境内）。如果你将采集的数据上传到了 Clinic Server 供 PingCAP 技术人员远程定位集群问题，这些数据将存储于 PingCAP 设立在 AWS S3 中国区（北京）的服务器。PingCAP 对于数据访问权限进行了严格的访问控制，只有经授权的内部技术人员能够访问该数据。

在对应的技术支持 Case 关闭后，PingCAP 会在 90 天内对相关数据进行永久删除或匿名化处理。

## TiDB 集群数据采集范围

本节列出了 Diag 在使用 TiUP 部署的 TiDB 集群中采集的详细的诊断数据。

### Cluster 基础信息

| 诊断数据类型 | 输出文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 集群基础信息，包括集群 ID | `cluster.json` | 每次收集默认采集 |
| 集群详细信息 | `meta.yaml` | 每次收集默认采集 |

### TiDB 诊断数据

| 诊断数据类型 | 输出文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 日志 | `tidb.log` | `--include=log` |
| Error 日志 | `tidb_stderr.log` | `--include=log` |
| 慢日志| `tidb_slow_query.log` | `--include=log` |
| 配置文件 | `tidb.toml` | `--include=config` |
| 实时配置| `config.json` | `--include=config` |

### TiKV 诊断数据

| 诊断数据类型 | 输出文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 日志 | `tikv.log` | `--include=log` |
| Error 日志 | `tikv_stderr.log` | `--include=log` |
| 配置文件 | `tikv.toml` | `--include=config` |
| 实时配置 | `config.json` | `--include=config` |

### PD 诊断数据

| 诊断数据类型 | 输出文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 日志 | `pd.log` | `--include=log` |
| Error 日志 | `pd_stderr.log` | `--include=log` |
| 配置文件 | `pd.toml` | `--include=config` |
| 实时配置 | `config.json` | `--include=config` |
| `tiup ctl pd -u http://${pd IP}:${PORT} store` 的输出结果 | `store.json` | `--include=config` |
| `tiup ctl pd -u http://${pd IP}:${PORT} config placement-rules show` 的输出结果 | `placement-rule.json` | `--include=config` |

### TiFlash 诊断数据

| 诊断数据类型 | 输出文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 日志 | `tiflash.log` | `--include=log` |
| Error 日志 | `tiflash_stderr.log` | `--include=log` |
| 配置文件 |  `tiflash-learner.toml`，`tiflash-preprocessed.toml`，`tiflash.toml` | `--include=config` |
| 实时配置 | `config.json` | `--include=config` |

### TiCDC 诊断数据

| 诊断数据类型 | 输出文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 日志 | `ticdc.log` | `--include=log`|
| Error 日志 | `ticdc_stderr.log` | `--include=log` |
| 配置文件 | `ticdc.toml` | `--include=config` |

### Prometheus 监控数据

| 诊断数据类型 | 输出文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 所有的 Metrics 数据 | `{metric_name}.json` | `--include=monitor` |
| Alert 配置 | `alerts.json` | `--include=monitor` |

### TiDB 系统变量

| 诊断数据类型 | 输出文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 获取 TiDB 系统变量（默认不采集，采集需要额外提供数据库帐号） | `mysql.tidb.csv` | `--include=db_vars` |
| | `global_variables.csv` | `--include=db_vars` |

### 集群系统信息

| 诊断数据类型 | 输出文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 内核日志 | `dmesg.log` | `--include=system` |
| 基础的系统和硬件信息 | `insight.json` | `--include=system` |
| 系统 `/etc/security/limits.conf` 中的内容 | `limits.conf` | `--include=system` |
| 内核参数列表 | `sysctl.conf` | `--include=system` |
| socket 统计信息，ss 命令结果| `ss.txt` | `--include=system` |

## DM 集群数据采集范围

本节列出了 Diag 在使用 TiUP 部署的 DM 集群中采集的详细的诊断数据。

### Cluster 基础信息

| 诊断数据类型 | 输出文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 集群基础信息，包括集群 ID | `cluster.json`| 每次收集默认采集 |
| 集群详细信息 | `meta.yaml` | 每次收集默认采集 |

### dm-master 诊断数据

| 诊断数据类型 | 输出文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 日志 | `m-master.log` | `--include=log` |
| Error 日志 | `dm-master_stderr.log` | `--include=log` |
| 配置文件 | `dm-master.toml` | `--include=config` |

### dm-worker 诊断数据

| 诊断数据类型 | 输出文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 日志| `dm-worker.log` | `--include=log`|
| Error 日志 | `dm-worker_stderr.log` | `--include=log` |
| 配置文件 | `dm-work.toml` | `--include=config` |

### Prometheus 监控数据

| 诊断数据类型 | 输出文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 所有的 Metrics 数据 | `{metric_name}.json` | `--include=monitor` |
| Alert 配置 | `alerts.json` | `--include=monitor` |

### 集群系统信息

| 诊断数据类型 | 输出文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 内核日志 | `dmesg.log` | `--include=system` |
| 基础的系统和硬件信息 | `insight.json` | `--include=system` |
| 系统 `/etc/security/limits.conf` 中的内容 | `limits.conf` | `--include=system` |
| 内核参数列表 | `sysctl.conf` | `--include=system` |
| socket 统计信息，ss 命令结果 | `ss.txt` | `--include=system` |