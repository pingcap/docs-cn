---
title: SQL Diagnostics
summary: Understand SQL diagnostics in TiDB.
aliases: ['/docs/dev/system-tables/system-table-sql-diagnostics/','/docs/dev/reference/system-databases/sql-diagnosis/','/docs/dev/system-tables/system-table-sql-diagnosis/','/tidb/dev/system-table-sql-diagnostics/','/tidb/dev/check-cluster-status-using-sql-statements','/docs/dev/check-cluster-status-using-sql-statements/','/docs/dev/reference/performance/check-cluster-status-using-sql-statements/']
---

# SQL Diagnostics

SQL diagnostics is a feature introduced in TiDB v4.0. You can use this feature to locate problems in TiDB with higher efficiency. Before TiDB v4.0, you need to use different tools to obtain different information.

The SQL diagnostic system has the following advantages:

+ It integrates information from all components of the system as a whole.
+ It provides a consistent interface to the upper layer through system tables.
+ It provides monitoring summaries and automatic diagnostics.
+ You will find it easier to query cluster information.

## Overview

The SQL diagnostic system consists of three major parts:

+ **Cluster information table**: The SQL diagnostics system introduces cluster information tables that provide a unified way to get the discrete information of each instance. This system fully integrates the cluster topology, hardware information, software information, kernel parameters, monitoring, system information, slow queries, statements, and logs of the entire cluster into the table. So you can query these information using SQL statements.

+ **Cluster monitoring table**: The SQL diagnostic system introduces cluster monitoring tables. All of these tables are in `metrics_schema`, and you can query monitoring information using SQL statements. Compared to the visualized monitoring before v4.0, you can use this SQL-based method to perform correlated queries on all the monitoring information of the entire cluster, and compare the results of different time periods to quickly identify performance bottlenecks. Because the TiDB cluster has many monitoring metrics, the SQL diagnostic system also provides monitoring summary tables, so you can find abnormal monitoring items more easily.

**Automatic diagnostics**: Although you can manually execute SQL statements to query cluster information tables, cluster monitoring tables, and summary tables to locate issues, the automatic diagnostics allows you to quickly locate common issues. The SQL diagnostic system performs automatic diagnostics based on the existing cluster information tables and monitoring tables, and provides relevant diagnostic result tables and diagnostic summary tables.

## Cluster information tables

The cluster information tables bring together the information of all instances and instances in a cluster. With these tables, you can query all cluster information using only one SQL statement. The following is a list of cluster information tables:

+ From the cluster topology table [`information_schema.cluster_info`](/information-schema/information-schema-cluster-info.md), you can get the current topology information of the cluster, the version of each instance, the Git Hash corresponding to the version, the starting time of each instance, and the running time of each instance.
+ From the cluster configuration table [`information_schema.cluster_config`](/information-schema/information-schema-cluster-config.md), you can get the configuration of all instances in the cluster. For versions earlier than 4.0, you need to access the HTTP API of each instance one by one to get these configuration information.
+ On the cluster hardware table [`information_schema.cluster_hardware`](/information-schema/information-schema-cluster-hardware.md), you can quickly query the cluster hardware information.
+ On the cluster load table [`information_schema.cluster_load`](/information-schema/information-schema-cluster-load.md), you can query the load information of different instances and hardware types of the cluster.
+ On the kernel parameter table [`information_schema.cluster_systeminfo`](/information-schema/information-schema-cluster-systeminfo.md), you can query the kernel configuration information of different instances in the cluster. Currently, TiDB supports querying the sysctl information.
+ On the cluster log table [`information_schema.cluster_log`](/information-schema/information-schema-cluster-log.md), you can query cluster logs. By pushing down query conditions to each instance, the impact of the query on cluster performance is less than that of the `grep` command.

On the system tables earlier than TiDB v4.0, you can only view the current instance. TiDB v4.0 introduces the corresponding cluster tables and you can have a global view of the entire cluster on a single TiDB instance. These tables are currently in `information_schema`, and the query method is the same as other `information_schema` system tables.

## Cluster monitoring tables

To dynamically observe and compare cluster conditions in different time periods, the SQL diagnostic system introduces cluster monitoring system tables. All monitoring tables are in `metrics_schema`, and you can query the monitoring information using SQL statements. Using this method, you can perform correlated queries on all monitoring information of the entire cluster and compare the results of different time periods to quickly identify performance bottlenecks.

+ [`information_schema.metrics_tables`](/information-schema/information-schema-metrics-tables.md): Because many system tables exist now, you can query meta-information of these monitoring tables on the `information_schema.metrics_tables` table.

Because the TiDB cluster has many monitoring metrics, TiDB provides the following monitoring summary tables in v4.0:

+ The monitoring summary table [`information_schema.metrics_summary`](/information-schema/information-schema-metrics-summary.md) summarizes all monitoring data to for you to check each monitoring metric with higher efficiency.
+ [`information_schema.metrics_summary_by_label`](/information-schema/information-schema-metrics-summary.md) also summarizes all monitoring data. Particularly, this table aggregates statistics using different labels of each monitoring metric.

## Automatic diagnostics

On the cluster information tables and cluster monitoring tables above, you need to manually execute SQL statements to troubleshoot the cluster. TiDB v4.0 supports the automatic diagnostics. You can use diagnostic-related system tables based on the existing basic information tables, so that the diagnostics is automatically executed. The following are the system tables related to the automatic diagnostics:

+ The diagnostic result table [`information_schema.inspection_result`](/information-schema/information-schema-inspection-result.md) displays the diagnostic result of the system. The diagnostics is passively triggered. Executing `select * from inspection_result` triggers all diagnostic rules to diagnose the system, and the faults or risks in the system are displayed in the results.
+ The diagnostic summary table [`information_schema.inspection_summary`](/information-schema/information-schema-inspection-summary.md) summarizes the monitoring information of a specific link or module. You can troubleshoot and locate problems based on the context of the entire module or link.
