---
title: CALIBRATE RESOURCE
summary: TiDB 数据库中 CALIBRATE RESOURCE 的使用概况。
---

# `CALIBRATE RESOURCE`

`CALIBRATE RESOURCE` 语句用于预估并输出当前集群的 [`Request Unit (RU)`](/tidb-resource-control.md#什么是-request-unit-ru) 的容量。

## 语法图

```ebnf+diagram
CalibrateResourceStmt ::= 'CALIBRATE' 'RESOURCE' WorkloadOption

WorkloadOption ::=
    ( 'WORKLOAD' ('TPCC' | 'OLTP_READ_WRITE' | 'OLTP_READ_ONLY' | 'OLTP_WRITE_ONLY') )?
``` 

## 示例

WORKLOAD 为可选项，默认为 TPCC，目前支持：OLTP_READ_WRITE、OLTP_READ_ONLY、OLTP_WRITE_ONLY。

```sql
CALIBRATE RESOURCE;
+-------+
| QUOTA |
+-------+
| 190470 |
+-------+
1 row in set (0.01 sec)

MySQL [(none)]> CALIBRATE RESOURCE WORKLOAD OLTP_READ_WRITE;
+-------+
| QUOTA |
+-------+
| 70702 |
+-------+
1 row in set (0.01 sec)
```

> **注意：**
>
> 集群 RU 的容量会随集群的拓扑结构和各个组件软硬件配置的变化而变化，每个集群实际能消耗的 RU 还与实际的负载相关。此预估值仅供参考，可能会与实际的最大值存在偏差。
