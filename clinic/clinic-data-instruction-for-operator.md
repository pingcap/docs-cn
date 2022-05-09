---
title: Operator 环境 Clinic 数据采集说明
summary: 详细说明 PingCAP Clinic 诊断服务在使用 Operator 部署的 TiDB 集群中能够采集哪些诊断数据。
---

# Clinic 数据采集说明 - Operator 环境

本文提供了 PingCAP Clinic 诊断服务（以下简称为 PingCAP Clinic）在使用 TiDB Operator 部署的 TiDB 集群中能够采集的诊断数据类型，并列出了各个采集项对应的采集参数。当[执行 Clinic Diag 诊断客户端（以下简称为 Diag）数据采集命令](/clinic/clinic-user-guide-for-operator.md)时，你可以依据需要采集的数据类型，在命令中添加所需的采集参数。

PingCAP Clinic 对使用 TiDB Operator 部署的 TiDB 集群采集的数据**仅**用于集群问题诊断与分析。

Clinic Server 是部署在云端的云服务，位于 PingCAP 内网（中国境内）。如果你把采集的数据上传到了 Clinic Server 供 PingCAP 技术人员远程定位集群问题，这些数据将存储于 PingCAP 设立在 AWS S3 中国区（北京）的服务器。PingCAP 对数据访问权限进行了严格的访问控制，只有经授权的内部技术人员可以访问该数据。

## TiDB 集群信息

|  诊断数据类型 | 输出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 集群基础信息，包括集群 ID | `cluster.json` | 每次收集默认采集 |
| 集群详细信息 | `tidbcluster.json` | 每次收集默认采集 |

## TiDB 诊断数据

|诊断数据类型 | 输出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 性能数据| `cpu_profile.proto`，`mem_heap.proto`，`goroutine.txt`，`mutex.txt` | `collectors:perf`（默认不采集）|
| 实时配置 | `config.json` | `collectors:config` |

## TiKV 诊断数据

|诊断数据类型 | 输出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 实时配置 | `config.json` | `collectors:config` |
| 性能数据| `cpu_profile.proto` | `collectors:perf` （默认不采集）|

## PD 诊断数据

|诊断数据类型 | 输出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 实时配置 | `config.json` |`collectors:config` |
| `tiup ctl pd -u http://${pd IP}:${PORT} store` 的输出结果 | `store.json` | `collectors:config` |
| `tiup ctl pd -u http://${pd IP}:${PORT} config placement-rules show` 的输出结果 | `placement-rule.json` | `collectors:config` |
| 性能数据| `cpu_profile.proto`，`mem_heap.proto`，`goroutine.txt`，`mutex.txt` | `collectors:perf`（默认不采集）|

## TiFlash 诊断数据

|诊断数据类型 | 输出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 实时配置 | `config.json` |`collectors:config` |
| 性能数据| `cpu_profile.proto` | `collectors:perf`（默认不采集） |

## TiCDC 诊断数据

|诊断数据类型 | 输出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 实时配置 | `config.json` |`collectors:config` |
| Debug 数据| `info.txt`，`status.txt`，`changefeeds.txt`，`captures.txt`，`processors.txt` | `collectors:debug`（默认不采集） |

## Prometheus 监控数据

|诊断数据类型 | 输出文件 | PingCAP Clinic 采集参数 |
| :------ | :------ |:-------- |
| 所有的 Metrics 数据 | `{metric_name}.json` | `collectors:monitor` |
| Alert 配置 | `alerts.json` | `collectors:monitor` |
