---
title: Overview of Optimizing SQL Performance
summary: Provides an overview of SQL performance tuning for TiDB application developers.
---

# Overview of Optimizing SQL Performance

This document introduces how to optimize the performance of SQL statements in TiDB. To get good performance, you can start with the following aspects:

* SQL performance tuning
* Schema design: Based on your application workload patterns, you might need to change the table schema to avoid transaction contention or hot spots.

## SQL performance tuning

To get good SQL statement performance, you can follow these guidelines:

* Scan as few rows as possible. It is recommended to scan only the data you need and avoid scanning excess data.
* Use the right index. Ensure that there is a corresponding index for the column in the `WHERE` clause in SQL. If not, the statement entails a full table scan and thus causes poor performance.
* Use the right join type. It is important to choose the right join type based on the relative size of the tables involved in the query. In general, TiDB's cost-based optimizer picks the best-performing join type. However, in a few cases, you might need to manually specify a better join type.
* Use the right storage engine. For hybrid OLTP and OLAP workloads, the TiFlash engine is recommended. For details, see [HTAP Query](/develop/dev-guide-hybrid-oltp-and-olap-queries.md).

## Schema design

After [tuning SQL performance](#sql-performance-tuning), if your application still cannot get good performance, you might need to check your schema design and data access patterns to avoid the following issues:

<CustomContent platform="tidb">

* Transaction contention. For how to diagnose and resolve transaction contention, see [Troubleshoot Lock Conflicts](/troubleshoot-lock-conflicts.md).
* Hot spots. For how to diagnose and resolve hot spots, see [Troubleshoot Hotspot Issues](/troubleshoot-hot-spot-issues.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

* Transaction contention. For how to diagnose and resolve transaction contention, see [Troubleshoot Lock Conflicts](https://docs.pingcap.com/tidb/stable/troubleshoot-lock-conflicts).
* Hot spots. For how to diagnose and resolve hot spots, see [Troubleshoot Hotspot Issues](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues).

</CustomContent>

### See also

<CustomContent platform="tidb">

* [SQL Performance Tuning](/sql-tuning-overview.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

* [SQL Performance Tuning](/tidb-cloud/tidb-cloud-sql-tuning-overview.md)

</CustomContent>
