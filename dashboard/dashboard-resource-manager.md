---
title: TiDB Dashboard Resource Manager Page
summary: Introduce how to use the Resource Manager page in TiDB Dashboard to view the information about resource control, so you can estimate cluster capacity before resource planning and allocate resources more effectively.
---

# TiDB Dashboard Resource Manager Page

To implement resource isolation using the [Resource Control](/tidb-resource-control.md) feature, cluster administrators can create resource groups and set quotas for each group. Before resource planning, you need to know the overall capacity of the cluster. This document helps you view the information about resource control, so you can estimate the cluster capacity before resource planning and allocate resources more effectively.

## Access the page

You can use one of the following two methods to access the Resource Manager page:

* After logging in to TiDB Dashboard, click **Resource Manager** in the left navigation menu.

* Visit <http://127.0.0.1:2379/dashboard/#/resource_manager> in your browser. Replace `127.0.0.1:2379` with the actual PD instance address and port.

## Resource Manager page

The following figure shows the Resource Manager details page:

![TiDB Dashboard: Resource Manager](/media/dashboard/dashboard-resource-manager-info.png)

The Resource Manager page contains the following three sections:

- Configuration: This section displays the data obtained from the `RESOURCE_GROUPS` table of TiDB. It contains the information about all resource groups. For more information, see [`RESOURCE_GROUPS`](/information-schema/information-schema-resource-groups.md).

- Estimate Capacity: Before resource planning, you need to know the overall capacity of the cluster. You can use one of the following methods:

    - [Estimate capacity based on actual workload](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-actual-workload)
    - [Estimate capacity based on hardware deployment](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-hardware-deployment)

- Metrics: By observing the metrics on the panels, you can understand the current overall resource consumption status of the cluster.

## Estimate Capacity

Before resource planning, you need to know the overall capacity of the cluster. TiDB provides two methods to estimate the capacity of [Request Unit (RU)](/tidb-resource-control.md#what-is-request-unit-ru#what-is-request-unit-ru) in the current cluster:

- [Estimate capacity based on hardware deployment](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-hardware-deployment)
    
    TiDB accepts the following workload types:
    
    - `tpcc`: applies to workloads with heavy data write. It is estimated based on a workload model similar to `TPC-C`.
    - `oltp_write_only`: applies to workloads with heavy data write. It is estimated based on a workload model similar to `sysbench oltp_write_only`.
    - `oltp_read_write`: applies to workloads with even data read and write. It is estimated based on a workload model similar to `sysbench oltp_read_write`.
    - `oltp_read_only`: applies to workloads with heavy data read. It is estimated based on a workload model similar to `sysbench oltp_read_only`.

  ![Calibrate by Hardware](/media/dashboard/dashboard-resource-manager-calibrate-by-hardware.png)

    The **Total RU of user resource groups** represents the total amount of RU for all user resource groups, excluding the `default` resource group. If this value is less than the estimated capacity, the system triggers an alert. By default, the system allocates unlimited usage to the predefined `default` resource group. When all users belong to the `default` resource group, resources are allocated in the same way as when resource control is disabled.

- [Estimate capacity based on actual workload](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-actual-workload)

    ![Calibrate by Workload](/media/dashboard/dashboard-resource-manager-calibrate-by-workload.png)

    You can select a time range for estimation within the range of 10 minutes to 24 hours. The time zone used is the same as that of the front-end user.

    - When the time window range does not fall between 10 minutes and 24 hours, the following error is displayed `ERROR 1105 (HY000): the duration of calibration is too short, which could lead to inaccurate output. Please make the duration between 10m0s and 24h0m0s`.

    - The monitoring metrics for the [capacity estimation based on the actual workload](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-actual-workload) feature include `tikv_cpu_quota`, `tidb_server_maxprocs`, `resource_manager_resource_unit`, and `process_cpu_usage`. If the CPU quota monitoring data is empty, there will be an error with the corresponding monitoring metric name, for example, `Error 1105 (HY000): There is no CPU quota metrics, metrics 'tikv_cpu_quota' is empty`.

    - If the workload in the time window is too low, or the `resource_manager_resource_unit` and `process_cpu_usage` monitoring data is missing, an error will be reported `Error 1105 (HY000): The workload in selected time window is too low, with which TiDB is unable to reach a capacity estimation; please select another time window with higher workload, or calibrate resource by hardware instead`. In addition, because TiKV does not monitor CPU utilization on macOS, it does not support capacity estimation based on the actual workload, and will also report this error.

  You can select an appropriate time range using **CPU Usage** in the [Metrics](#metrics) section.

## Metrics

By observing the metrics on the panels, you can understand the current overall resource consumption status of the cluster. The monitoring metrics and their meanings are as follows:

- Total RU Consumed: The total consumption of Request Units counted in real time.
- RU Consumed by Resource Groups: The number of Request Units consumed by resource groups in real time.
- TiDB
    - CPU Quota: The maximum CPU usage of TiDB.
    - CPU Usage: The total CPU usage of all TiDB instances.
- TiKV
    - CPU Quota: The maximum CPU usage of TiKV.
    - CPU Usage: The total CPU usage of all TiKV instances.
    - IO MBps: The total I/O throughput of all TiKV instances.