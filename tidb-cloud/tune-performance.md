---
title: Analyze and Tune Performance
summary: Learn how to analyze and tune performance of your TiDB Cloud cluster.
---

# Analyze and Tune Performance

TiDB Cloud provides [Statement Analysis](#statement-analysis) and [Key Visualizer](#key-visualizer) to analyze performance.

- Statement Analysis enables you to directly observe the SQL execution on the page, and easily locate performance problems without querying the system tables.

- Key Visualizer helps you observe TiDB's data access patterns and data hotspots.

## Statement Analysis

To use the statement analysis, perform the following steps:

1. Navigate to the **Diagnosis** tab of a cluster.

2. Click the **Statement** tab.

3. Select the time period to be analyzed in the time interval box. Then you can get the execution statistics of SQL statements of all databases in this period.

4. (Optional) If you only care about certain databases, you can select the corresponding schema(s) in the next box to filter the results.

The results are displayed in the form of a table, and you can sort the results by different columns.

![Statement Analysis](/media/tidb-cloud/statement-analysis.png)

For details, see [Statement Execution Details in TiDB Dashboard](https://docs.pingcap.com/tidb/stable/dashboard-statement-details).

## Key Visualizer

To view the key analytics, perform the following steps:

1. Navigate to the **Diagnosis** tab of a cluster.

2. Click the **Key Visualizer** tab.

![Key Visualizer](/media/tidb-cloud/key-visualizer.png)

On the **Key Visualizer** page, a large heat map shows changes on access traffic over time. The average values ​​along each axis of the heat map are shown below and on the right side. The left side is the table name, index name and other information.

For details, see [Key Visualizer](https://docs.pingcap.com/tidb/stable/dashboard-key-visualizer).
