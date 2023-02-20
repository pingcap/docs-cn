---
title: TiDB Dashboard Introduction
summary: Introduce TiDB Dashboard.
aliases: ['/docs/dev/dashboard/dashboard-intro/']
---

# TiDB Dashboard Introduction

TiDB Dashboard is a Web UI for monitoring, diagnosing, and managing the TiDB cluster, which is available since v4.0. It is built into the PD component and does not require an independent deployment.

> **Note:**
>
> TiDB v6.5.0 (and later) and TiDB Operator v1.4.0 (and later) support deploying TiDB Dashboard as an independent Pod on Kubernetes. For details, see [Deploy TiDB Dashboard independently in TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/dev/get-started#deploy-tidb-dashboard-independently).

![TiDB Dashboard interface](/media/dashboard/dashboard-intro.gif)

TiDB Dashboard is open-sourced on [GitHub](https://github.com/pingcap-incubator/tidb-dashboard).

This document introduces the main features of TiDB Dashboard. You can click links in the following sections to learn more details.

## Show the overall running status of the TiDB cluster

You can use TiDB Dashboard to learn the TiDB cluster's queries per second (QPS), execution time, the types of SQL statements that consume the most resources, and other overview information.

See [TiDB Dashboard Overview](/dashboard/dashboard-overview.md) for details.

## Show the running status of components and hosts

You can use TiDB Dashboard to view the running status of TiDB, TiKV, PD, TiFlash components in the entire cluster and the running status of the host on which these components are located.

See [TiDB Dashboard Cluster Information Page](/dashboard/dashboard-cluster-info.md) for details.

## Show distribution and trends of read and write traffic

The Key Visualizer feature of TiDB Dashboard visually shows the change of read and write traffic over time in the entire cluster in the form of heatmap. You can use this feature to timely discover changes of application modes or locate hotspot issues with uneven performance.

See [Key Visualizer Page](/dashboard/dashboard-key-visualizer.md) for details.

## Show a list of execution information of all SQL statements

The execution information of all SQL statements is listed on the SQL Statements page. You can use this page to learn the execution time and total executions at all stages, which helps you analyze and locate the SQL queries that consume the most resources and improve the overall cluster performance.

See [SQL Statements Page of TiDB Dashboard](/dashboard/dashboard-statement-list.md) for details.

## Learn the detailed execution information of slow queries

The Slow Queries page of TiDB Dashboard shows a list of all SQL statements that take a long time to execute, including the SQL texts and execution information. This page helps you locate the cause of slow queries or performance jitter.

See [Slow Queries Page](/dashboard/dashboard-slow-query.md) for details.

## Diagnose common cluster problems and generate reports

The diagnostic feature of TiDB Dashboard automatically determines whether some common risks (such as inconsistent configurations) or problems exist in the cluster, generates reports, and gives operation suggestions, or compares the status of each cluster metric in different time ranges for you to analyze possible problems.

See [TiDB Dashboard Cluster Diagnostics Page](/dashboard/dashboard-diagnostics-access.md) for details.

## Query logs of all components

On the Search Logs page of TiDB Dashboard, you can quickly search logs of all running instances in the cluster by keywords, time range, and other conditions, package these logs, and download them to your local machine.

See [Search Logs Page](/dashboard/dashboard-log-search.md) for details.

## Collect profiling data for each instance

This is an advanced debugging feature that lets you profile each instance online and analyze various internal operations an instance performed during the profiling data collection period and the proportion of the operation execution time in this period without third-party tools.

See [Profile Instances Page](/dashboard/dashboard-profiling.md) for details.
