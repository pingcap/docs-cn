---
title: Top SQL
summary: This document describes how to use Top SQL to locate SQL queries that contribute to a high load.
---

# Top SQL

> **Warning:**
>
> Currently, Top SQL is an experimental feature. It is not recommended that you use it for production environments.

This document describes how to use Top SQL to locate SQL queries that contribute to a high load of a TiDB or TiKV node in a specified time range. For example, you can use Top SQL to locate an analytic query that consumes 99% of the load for a low-load database.

For a specified TiDB or TiKV node, Top SQL provides the following features:

* Show the top 5 types of SQL queries that contribute the most to the load in a specified time range.
* Show information such as CPU usage, requests per second, average latency, and query plan of a particular query, which can be used for potential performance optimization to improve your business.

## Enable Top SQL

The Top SQL feature is disabled by default. You can enable the feature for the entire cluster using either of the following methods:

- Method 1: Log in to TiDB Dashboard, click **Top SQL** in the left pane, click the gear button in the upper-right corner of the page, and then enable the Top SQL feature.
- Method 2: Set the value of the TiDB system variable [`tidb_enable_top_sql`](/system-variables.md#tidb_enable_top_sql-new-in-v540) to `ON`.

> **Note:**
>
> Enabling Top SQL has a slight impact on the performance of your cluster.

## Use Top SQL

Once Top SQL is enabled, you can log into TiDB Dashboard, and then click **Top SQL** in the left pane to use it.

![Top SQL](/media/dashboard/top-sql-overview.png)

Usage tips：

* You can select the target node and time range in the drop-down lists at the top of the page, or you can select the time range in the chart.
* If the data in the chart is out of date, you can click **Refresh**, or select auto-refresh and specify the auto-refresh interval in the **Refresh** drop-down list.
* The chart shows the top 5 types of queries that contribute the most to the load of the selected node in the selected time range.
* You can select a query type in the list to view the execution plan of that query type on this node and the execution details such as the Call/sec, Scan Rows/sec, Scan Indexes/sec, and Latency/call.

![Top SQL Details](/media/dashboard/top-sql-details.png)