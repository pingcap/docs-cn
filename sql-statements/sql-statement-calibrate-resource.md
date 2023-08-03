---
title: CALIBRATE RESOURCE
summary: An overview of the usage of CALIBRATE RESOURCE for the TiDB database.
---

# `CALIBRATE RESOURCE`

The `CALIBRATE RESOURCE` statement is used to estimate and output the ['Request Unit (RU)`](/tidb-resource-control#what-is-request-unit-ru) capacity of the current cluster.

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This feature is not available on [TiDB Serverless clusters](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless).

</CustomContent>

## Synopsis

```ebnf+diagram
CalibrateResourceStmt ::= 'CALIBRATE' 'RESOURCE' WorkloadOption

WorkloadOption ::=
( 'WORKLOAD' ('TPCC' | 'OLTP_READ_WRITE' | 'OLTP_READ_ONLY' | 'OLTP_WRITE_ONLY') )
| ( 'START_TIME' 'TIMESTAMP' ('DURATION' stringLit | 'END_TIME' 'TIMESTAMP')?)?

```

## Privileges

To execute this command, make sure that the following requirements are met:

- You have enabled [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660).
- The user has `SUPER` or `RESOURCE_GROUP_ADMIN` privilege.
- The user has the `SELECT` privilege for all tables in the `METRICS_SCHEMA` schema.

## Methods for estimating capacity

TiDB provides two methods for estimation:

### Estimate capacity based on actual workload

If your application is already running in a production environment, or you can run actual business tests, it is recommended to use the actual workload over a period of time to estimate the total capacity. To improve the accuracy of the estimation, observe the following constraints:

- Use the `START_TIME` parameter to specify the time point at which the estimation starts, in the format of `2006-01-02 15:04:05`. The default estimation end time is the current time.
- After specifying the `START_TIME` parameter, you can use the `END_TIME` parameter to specify the estimation end time, or use the `DURATION` parameter to specify the estimation time window from `START_TIME`.
- The time window ranges from 10 minutes to 24 hours.
- In the specified time window, if the CPU utilization of TiDB and TiKV is too low, you cannot estimate the capacity.

> **Note:**
>
> TiKV does not monitor CPU usage metrics on macOS. It does not support capacity estimation based on the actual workload on macOS.

### Estimate capacity based on hardware deployment

This method mainly estimates capacity based on the current cluster configuration, combined with the empirical values observed for different workloads. Because different types of workloads require different ratios of hardware, the output capacity of the same configuration of hardware might be different. The `WORKLOAD` parameter here accepts the following different workload types. The default value is `TPCC`.

- `TPCC`: applies to workloads with heavy data write. It is estimated based on a workload model similar to `TPC-C`.
- `OLTP_WRITE_ONLY`: applies to workloads with heavy data write. It is estimated based on a workload model similar to `sysbench oltp_write_only`.
- `OLTP_READ_WRITE`: applies to workloads with even data read and write. It is estimated based on a workload model similar to `sysbench oltp_read_write`.
- `OLTP_READ_ONLY`: applies to workloads with heavy data read. It is estimated based on a workload model similar to `sysbench oltp_read_only`.

> **Note:**
>
> The RU capacity of a cluster varies with the topology of the cluster and the hardware and software configuration of each component. The actual RU that each cluster can provide is also related to the actual workload. The estimated value based on hardware deployment is for reference only and might differ from the actual maximum value. It is recommended to [estimate capacity based on actual workload](#estimate-capacity-based-on-actual-workload).

## Examples

Specify the start time `START_TIME` and the time window `DURATION` to view the RU capacity according to the actual workload.

```sql
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' DURATION '20m';
+-------+
| QUOTA |
+-------+
| 27969 |
+-------+
1 row in set (0.01 sec)
```

Specify the start time `START_TIME` and the end time `END_TIME` to view the RU capacity according to the actual workload.

```sql
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' END_TIME '2023-04-18 08:20:00';
+-------+
| QUOTA |
+-------+
| 27969 |
+-------+
1 row in set (0.01 sec)
```

When the time window range `DURATION` does not fall between 10 minutes and 24 hours, an error occurs.

```sql
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' DURATION '25h';
ERROR 1105 (HY000): the duration of calibration is too long, which could lead to inaccurate output. Please make the duration between 10m0s and 24h0m0s
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' DURATION '9m';
ERROR 1105 (HY000): the duration of calibration is too short, which could lead to inaccurate output. Please make the duration between 10m0s and 24h0m0s
```

The monitoring metrics for the [capacity estimation based on the actual workload](#estimate-capacity-based-on-actual-workload) feature include `tikv_cpu_quota`, `tidb_server_maxprocs`, `resource_manager_resource_unit`, and `process_cpu_usage`. If the CPU quota monitoring data is empty, there will be an error with the corresponding monitoring metric name, as shown in the following example:

```sql
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' DURATION '60m';
Error 1105 (HY000): There is no CPU quota metrics, metrics 'tikv_cpu_quota' is empty
```

If the workload in the time window is too low, or the `resource_manager_resource_unit` and `process_cpu_usage` monitoring data is missing, the following error will be reported. In addition, because TiKV does not monitor CPU utilization on macOS, it does not support capacity estimation based on the actual workload, and will also report this error.

```sql
CALIBRATE RESOURCE START_TIME '2023-04-18 08:00:00' DURATION '60m';
ERROR 1105 (HY000): The workload in selected time window is too low, with which TiDB is unable to reach a capacity estimation; please select another time window with higher workload, or calibrate resource by hardware instead
```

Specify `WORKLOAD` to view the RU capacity. The default value is `TPCC`.

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
