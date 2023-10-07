---
title: CALIBRATE RESOURCE
summary: TiDB 数据库中 CALIBRATE RESOURCE 的使用概况。
---

# `CALIBRATE RESOURCE`

`CALIBRATE RESOURCE` 语句用于预估并输出当前集群的 [`Request Unit (RU)`](/tidb-resource-control.md#什么是-request-unit-ru) 的容量。

## 语法图

```ebnf+diagram
CalibrateResourceStmt ::= 'CALIBRATE' 'RESOURCE' CalibrateOption

CalibrateOption ::=
('START_TIME' 'TIMESTAMP' ('DURATION' stringLit | 'END_TIME' 'TIMESTAMP')?)
| ('WORKLOAD' ('TPCC' | 'OLTP_READ_WRITE' | 'OLTP_READ_ONLY' | 'OLTP_WRITE_ONLY'))?

```

## 预估方式

TiDB 提供两种预估方式：

### 根据实际负载估算容量

如果应用已经在线上运行，或者你能够运行实际业务测试，建议利用一段时间的实际负载来预估总容量。为了提高预估准确性，需要遵守以下约束条件：

- 使用 `START_TIME` 参数指定预估开始的时间点，格式为 `2006-01-02 15:04:05`，默认预估结束时间为当前时间。
- 指定完成 `START_TIME` 参数后，可以使用 `END_TIME` 参数指定预估结束时间，或者使用 `DURATION` 参数指定距离 `START_TIME` 的预估时间窗口。
- 时间窗口范围为 10 分钟至 24 小时。
- 在预估的时间窗口内，TiDB 与 TiKV 的 CPU 利用率不能过低，否则无法进行容量估算。

> **注意：**
>
> 由于 TiKV 未在 macOS 上监控 CPU 使用率，所以不支持在 macOS 上使用根据实际负载估算容量功能。

### 基于硬件部署估算容量

这种方式主要根据当前的集群配置，结合对不同负载观测的经验值进行预估。由于不同类型的负载对硬件的配比要求不同，相同配置的硬件所输出的容量也会有所不同。这里的 `WORKLOAD` 参数提供了以下不同的负载类型供选择，默认为 `TPCC`：

- `TPCC`：数据写入较重的负载，根据类似 `TPC-C` 的负载模型预测。
- `OLTP_WRITE_ONLY`：数据写入较重的负载，根据类似 `sysbench oltp_write_only` 的负载模型预测。
- `OLTP_READ_WRITE`：数据读写平衡的负载，根据类似 `sysbench oltp_read_write` 的负载模型预测。
- `OLTP_READ_ONLY`：数据读取较重的负载，根据类似 `sysbench oltp_read_only` 的负载模型预测。
- `TPCH_10`：AP 类型查询，根据 TPCH-10G 的 22 条查询进行负载预测。

> **注意：**
>
> 集群 RU 的容量会随集群的拓扑结构和各个组件软硬件配置的变化而变化，每个集群实际能消耗的 RU 还与实际的负载相关。基于硬件部署估算容量的预估值仅供参考，可能会与实际的最大值存在偏差。建议[根据实际负载估算容量](#根据实际负载估算容量)。

## 权限

执行此命令依赖如下配置和权限：

- [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-从-v660-版本开始引入) 需要处于开启状态
- 需要拥有 `SUPER` 或者 `RESOURCE_GROUP_ADMIN` 权限
- 需要拥有 `METRICS_SCHEMA` 库下所有表的 `SELECT` 权限

## 示例

指定初始时间 `START_TIME` 和时间窗口 `DURATION` 大小，根据实际负载查看 RU 容量。

```sql
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' DURATION '20m';
+-------+
| QUOTA |
+-------+
| 27969 |
+-------+
1 row in set (0.01 sec)
```

指定初始时间 `START_TIME` 和结束时间 `END_TIME`，根据实际负载查看 RU 容量。

```sql
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' END_TIME '2023-04-18 08:20:00';
+-------+
| QUOTA |
+-------+
| 27969 |
+-------+
1 row in set (0.01 sec)
```

当时间窗口范围 `DURATION` 不满足 10 分钟至 24 小时的条件，会导致报错提醒。

```sql
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' DURATION '25h';
ERROR 1105 (HY000): the duration of calibration is too long, which could lead to inaccurate output. Please make the duration between 10m0s and 24h0m0s
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' DURATION '9m';
ERROR 1105 (HY000): the duration of calibration is too short, which could lead to inaccurate output. Please make the duration between 10m0s and 24h0m0s
```

[根据实际负载估算容量](#根据实际负载估算容量)功能的监控指标包括 `tikv_cpu_quota`、`tidb_server_maxprocs`、`resource_manager_resource_unit`、`process_cpu_usage`、`tiflash_cpu_quota`、`tiflash_resource_manager_resource_unit`、`tiflash_process_cpu_usage`。如果 CPU quota 监控数据为空，会有对应监控项名称的报错，如下面例子所示。

```sql
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' DURATION '60m';
Error 1105 (HY000): There is no CPU quota metrics, metrics 'tikv_cpu_quota' is empty
```

当时间窗口范围内的负载过低或者 `resource_manager_resource_unit` 及 `process_cpu_usage` 监控数据缺失，会导致报错。此外，由于 TiKV 未在 macOS 上监控 CPU 使用率，也会导致报错。

```sql
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' DURATION '60m';
ERROR 1105 (HY000): The workload in selected time window is too low, with which TiDB is unable to reach a capacity estimation; please select another time window with higher workload, or calibrate resource by hardware instead
```

指定 `WORKLOAD` 查看 RU 容量，默认为 `TPCC`。

```sql
CALIBRATE RESOURCE;
+-------+
| QUOTA |
+-------+
| 190470 |
+-------+
1 row in set (0.01 sec)

CALIBRATE RESOURCE WORKLOAD OLTP_WRITE_ONLY;
+-------+
| QUOTA |
+-------+
| 27444 |
+-------+
1 row in set (0.01 sec)
```
