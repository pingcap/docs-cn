---
title: CALIBRATE RESOURCE
summary: TiDB 数据库中 CALIBRATE RESOURCE 的使用概况。
---

# `CALIBRATE RESOURCE`

`CALIBRATE RESOURCE` 语句用于预估并输出当前集群的 [`Request Unit (RU)`](/tidb-resource-control.md#什么是-request-unit-ru) 的容量。TiDB 提供两种预估方式：

- 方法一：根据实际负载查看指定时间窗口内的容量，为提高预估准确性，存在以下约束：
    - 时间窗口范围为 10 分钟至 24 小时
    - 在指定的时间窗口内，TiDB 与 TiKV 的 CPU 利用率过低时不能进行容量估算

- 方法二：指定 `WORKLOAD` 查看 RU 容量，默认为 `TPCC`。目前支持以下选项：
    - OLTP_READ_WRITE
    - OLTP_READ_ONLY
    - OLTP_WRITE_ONLY
    - TPCC

> **注意：**
>
> 集群 RU 的容量会随集群的拓扑结构和各个组件软硬件配置的变化而变化，每个集群实际能消耗的 RU 还与实际的负载相关。方法二的预估值仅供参考，可能会与实际的最大值存在偏差。建议使用方法一根据实际负载进行预估。

## 语法图

```ebnf+diagram
CalibrateResourceStmt ::= 'CALIBRATE' 'RESOURCE' CalibrateOption

CalibrateOption ::=
('START_TIME' 'TIMESTAMP' ('DURATION' stringLit | 'END_TIME' 'TIMESTAMP')?)
| ('WORKLOAD' ('TPCC' | 'OLTP_READ_WRITE' | 'OLTP_READ_ONLY' | 'OLTP_WRITE_ONLY'))?

```

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

当时间窗口范围内的负载过低，会导致报错提醒。

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