---
title: Clinic 数据采集说明 - Operator 环境
summary: 详细说明 Clinic 在 Operator 集群中能够采集哪些诊断数据
---

# Clinic 数据采集说明 - Operator 环境

## 数据用途
仅用集群问题分析和诊断。

## 数据存储和安全
数据存储于 PingCAP 设立在 AWS S3 中国区（北京）的服务器，数据诊断分析服务器位于 PingCAP 内网，在中国境内。
数据访问权限做了严格的访问控制，只有经授权的 PingCAP 技术人员能够访问。
数据将在对应的技术支持 Case 关闭后90天内永久删除或匿名化处理。

## TiDB 集群数据采集范围

### Cluster 基础信息
|  诊断数据类型 | 输出文文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 集群基础信息，包括集群 ID | `cluster.json` | 每次收集默认采集 |
|  集群详细信息 | `tidbcluster.json` |每次收集默认采集 |

### TiDB 诊断数据
|诊断数据类型 | 输出文文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 实时配置 | `config.json` |`--include=config` |

### TiKV 诊断数据
|诊断数据类型 | 输出文文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 实时配置 | `config.json` | `--include=config` |

### PD 诊断数据
|诊断数据类型 | 输出文文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 实时配置 | `config.json` |`--include=config` |
| `tiup ctl pd -u http://${pd IP}:${PORT} store`  的输出结果 | `store.json`|`--include=config`|
| `tiup ctl pd -u http://${pd IP}:${PORT} config placement-rules show` 的输出结果 |`placement-rule.json`|`--include=config` |

### TiFlash 诊断数据
|诊断数据类型 | 输出文文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 实时配置 | `config.json` |`--include=config` |

### Ticdc 诊断数据
|诊断数据类型 | 输出文文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 实时配置 | `config.json` |`--include=config` |

### Prometheus 监控数据
|诊断数据类型 | 输出文文件 | Clinic 采集参数 |
| :------ | :------ |:-------- |
| 所有的 Metrics 数据| `{metric_name}.json` | `--include=monitor` |
|  Alert 配置 |`alerts.json`| `--include=monitor` |