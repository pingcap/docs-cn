---
title: Overview Page
summary: Learn the overview page of TiDB Dashboard.
aliases: ['/docs/dev/dashboard/dashboard-overview/']
---

# Overview Page

This page shows the overview of the entire TiDB cluster, including the following information:

- Queries per second (QPS) of the entire cluster.
- The query latency of the entire cluster.
- The SQL statements that have accumulated the longest execution time over the recent period.
- The slow queries whose execution time over the recent period exceeds the threshold.
- The node count and status of each instance.
- Monitor and alert messages.

## Access the page

After logging in to TiDB Dashboard, the overview page is entered by default, or you can click **Overview** in the left navigation menu to enter this page:

![Enter overview page](/media/dashboard/dashboard-overview-access-v650.png)

## QPS

This area shows the number of successful and failed queries per second for the entire cluster over the recent hour:

![QPS](/media/dashboard/dashboard-overview-qps.png)

> **Note:**
>
> This feature is available only in the cluster where the Prometheus monitoring component is deployed. If Prometheus is not deployed, an error will be displayed.

## Latency

This area shows the latency of 99.9%, 99%, and 90% of queries in the entire cluster over the recent one hour:

![Latency](/media/dashboard/dashboard-overview-latency.png)

> **Note:**
>
> This feature is available only on the cluster where the Prometheus monitoring component is deployed. If Prometheus is not deployed, an error will be displayed.

## Top SQL statements

This area shows the ten types of SQL statements that have accumulated the longest execution time in the entire cluster over the recent period. SQL statements with different query parameters but of the same structure are classified into the same SQL type and displayed in the same row:

![Top SQL](/media/dashboard/dashboard-overview-top-statements.png)

The information shown in this area is consistent with the more detailed [SQL Statements Page](/dashboard/dashboard-statement-list.md). You can click the **Top SQL Statements** heading to view the complete list. For details of the columns in this table, see [SQL Statements Page](/dashboard/dashboard-statement-list.md).

> **Note:**
>
> This feature is available only on the cluster where SQL Statements feature is enabled.

## Recent slow queries

By default, this area shows the latest 10 slow queries in the entire cluster over the recent 30 minutes:

![Recent slow queries](/media/dashboard/dashboard-overview-slow-query.png)

By default, the SQL query that is executed longer than 300 milliseconds is counted as a slow query and displayed on the table. You can change this threshold by modifying the [tidb_slow_log_threshold](/system-variables.md#tidb_slow_log_threshold) variable or the [instance.tidb_slow_log_threshold](/tidb-configuration-file.md#tidb_slow_log_threshold) TiDB parameter.

The content displayed in this area is consistent with the more detailed [Slow Queries Page](/dashboard/dashboard-slow-query.md). You can click the **Recent Slow Queries** title to view the complete list. For details of the columns in this table, see this [Slow Queries Page](/dashboard/dashboard-slow-query.md).

> **Note:**
>
> This feature is available only in the cluster with slow query logs enabled. By default, slow query logs are enabled in the cluster deployed using TiUP.

## Instances

This area summarizes the total number of instances and abnormal instances of TiDB, TiKV, PD, and TiFlash in the entire cluster:

![Instances](/media/dashboard/dashboard-overview-instances.png)

The statuses in the preceding image are described as follows:

- Up: The instance is running properly (including the offline storage instance).
- Down: The instance is running abnormally, such as network disconnection and process crash.

Click the **Instance** title to enter the [Cluster Info Page](/dashboard/dashboard-cluster-info.md) that shows the detailed running status of each instance.

## Monitor and alert

This area provides links for you to view detailed monitor and alert:

![Monitor and alert](/media/dashboard/dashboard-overview-monitor.png)

- **View Metrics**: Click this link to jump to the Grafana dashboard where you can view detailed monitoring information of the cluster. For details of each monitoring metric in the Grafana dashboard, see [monitoring metrics](/grafana-overview-dashboard.md).
- **View Alerts**: Click this link to jump to the AlertManager page where you can view detailed alert information of the cluster. If alerts exist in the cluster, the number of alerts is directly shown in the link text.
- **Run Diagnostics**: Click this link to jump to the more detailed [cluster diagnostics page](/dashboard/dashboard-diagnostics-access.md).

> **Note:**
>
> The **View Metrics** link is available only in the cluster where the Grafana node is deployed. The **View Alerts** link is available only in the cluster where the AlertManager node is deployed.
