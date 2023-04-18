---
title: CALIBRATE RESOURCE
summary: TiDB 数据库中 CALIBRATE RESOURCE 的使用概况。
---

# `CALIBRATE RESOURCE`

`CALIBRATE RESOURCE` 语句用于预估并输出当前集群的 [`Request Unit (RU)`](/tidb-resource-control.md#什么是-request-unit-ru) 的容量。提供两种预估方式：

- 方法一：对于当前集群的实际负载，支持在指定时间窗口范围内查看，时间窗口最小为 10 分钟，最大为 24 小时。
- 方法二：支持指定 WORKLOAD 查看 RU 容量，默认为 TPCC，目前支持以下选项：
    - OLTP_READ_WRITE
    - OLTP_READ_ONLY
    - OLTP_WRITE_ONLY
    - TPCC

> **注意：**
>
> 集群 RU 的容量会随集群的拓扑结构和各个组件软硬件配置的变化而变化，每个集群实际能消耗的 RU 还与实际的负载相关。方法二的预估值仅供参考，可能会与实际的最大值存在偏差，建议采用方法一通过实际负载来进行预估。

## 语法图

```ebnf+diagram
CalibrateResourceStmt ::= 'CALIBRATE' 'RESOURCE' CalibrateOption

CalibrateOption ::=
('WORKLOAD' ('TPCC' | 'OLTP_READ_WRITE' | 'OLTP_READ_ONLY' | 'OLTP_WRITE_ONLY'))
| ('START_TIME' 'TIMESTAMP' ('DURATION' stringLit | 'END_TIME' 'TIMESTAMP')?)?

```

## 示例

```sql
CALIBRATE RESOURCE;
+-------+
| QUOTA |
+-------+
| 190470 |
+-------+
1 row in set (0.01 sec)

```

```sql
CALIBRATE RESOURCE WORKLOAD OLTP_READ_WRITE;
+-------+
| QUOTA |
+-------+
| 70702 |
+-------+
1 row in set (0.01 sec)
```