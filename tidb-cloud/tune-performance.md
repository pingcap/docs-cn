---
title: Analyze and Tune Performance
summary: Learn how to analyze and tune performance of your TiDB Cloud cluster.
---

# Analyze and Tune Performance

TiDB Cloud provides [Statement Analysis](#statement-analysis), [Slow Query](#slow-query), and [Key Visualizer](#key-visualizer) to analyze performance.

- Statement Analysis enables you to directly observe the SQL execution on the page, and easily locate performance problems without querying the system tables.

- Slow Query lets you search and view all slow queries in your TiDB cluster, and explore the bottlenecks of each slow query by viewing its execution plan, SQL execution information, and other details.

- Key Visualizer helps you observe TiDB's data access patterns and data hotspots.

> **Note:**
>
> Currently, these three features are unavailable for [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta).
  
## Statement Analysis

To use the statement analysis, perform the following steps:

1. Navigate to the **SQL Diagnosis** tab of a cluster.

2. Click the **SQL Statement** tab.

3. Select the time period to be analyzed in the time interval box. Then you can get the execution statistics of SQL statements of all databases in this period.

4. (Optional) If you only care about certain databases, you can select the corresponding schema(s) in the next box to filter the results.

The results are displayed in the form of a table, and you can sort the results by different columns.

![Statement Analysis](/media/tidb-cloud/statement-analysis.png)

For more information, see [Statement Execution Details in TiDB Dashboard](https://docs.pingcap.com/tidb/stable/dashboard-statement-details).

## Slow Query

By default, SQL queries that take more than 300 milliseconds are considered as slow queries. 

To view slow queries in a cluster, perform the following steps:

1. Navigate to the **SQL Diagnosis** tab of a cluster.

2. Click the **Slow Query** tab.

3. Click any slow query in the list to display its detailed execution information.

4. (Optional) You can filter slow queries based on the target time range, the related databases, and SQL keywords. You can also limit the number of slow queries to be displayed.

The results are displayed in the form of a table, and you can sort the results by different columns.

![Slow Queries](/media/tidb-cloud/slow-queries.png)

For more information, see [Slow Queries in TiDB Dashboard](https://docs.pingcap.com/tidb/stable/dashboard-slow-query).

## Key Visualizer

To view the key analytics, perform the following steps:

1. Navigate to the **SQL Diagnosis** tab of a cluster.

2. Click the **Key Visualizer** tab.

![Key Visualizer](/media/tidb-cloud/key-visualizer.png)

On the **Key Visualizer** page, a large heat map shows changes on access traffic over time. The average values ​​along each axis of the heat map are shown below and on the right side. The left side is the table name, index name and other information.

For more information, see [Key Visualizer](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer).
