---
title: Clinic 数据采集说明 - Operator 环境
summary: 详细说明 Clinic 诊断服务会在使用 TiDB Operator 部署的集群中采集哪些诊断数据。
---

# Clinic 数据采集说明 - Operator 环境

通过 Clinic 诊断服务对使用 TiDB Operator 部署的集群采集的数据会**仅**用于集群问题诊断与分析。

采集的数据会存储于 PingCAP 设立在 AWS S3 中国区（北京）的服务器，数据诊断分析服务器位于 PingCAP 内网（中国境内）。PingCAP 对于数据访问权限进行了严格的访问控制，只有经授权的内部技术人员能够访问该数据。

在对应的技术支持 Case 关闭后，PingCAP 会在 90 天内对相关数据进行永久删除或匿名化处理。

### Cluster 基础信息

|  诊断数据类型 | 输出文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 集群基础信息，包括集群 ID | `cluster.json` | 每次收集默认采集 |
| 集群详细信息 | `tidbcluster.json` | 每次收集默认采集 |

### TiDB 诊断数据

|诊断数据类型 | 输出文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 实时配置 | `config.json` | `--include=config` |

### TiKV 诊断数据

|诊断数据类型 | 输出文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 实时配置 | `config.json` | `--include=config` |

### PD 诊断数据

|诊断数据类型 | 输出文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 实时配置 | `config.json` |`--include=config` |
| `tiup ctl pd -u http://${pd IP}:${PORT} store` 的输出结果 | `store.json` | `--include=config` |
| `tiup ctl pd -u http://${pd IP}:${PORT} config placement-rules show` 的输出结果 | `placement-rule.json` | `--include=config` |

### TiFlash 诊断数据

|诊断数据类型 | 输出文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 实时配置 | `config.json` |`--include=config` |

### TiCDC 诊断数据

|诊断数据类型 | 输出文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 实时配置 | `config.json` |`--include=config` |

### Prometheus 监控数据

|诊断数据类型 | 输出文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 所有的 Metrics 数据 | `{metric_name}.json` | `--include=monitor` |
| Alert 配置 | `alerts.json` | `--include=monitor` |
