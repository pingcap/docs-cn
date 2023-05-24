---
title: TiDB Dashboard Top SQL page
summary: Learn how to use Top SQL to find SQL statements with high CPU overhead.
---

# TiDB Dashboard Top SQL Page

With Top SQL, you can monitor and visually explore the CPU overhead of each SQL statement in your database in real-time, which helps you optimize and resolve database performance issues. Top SQL continuously collects and stores CPU load data summarized by SQL statements at any seconds from all TiDB and TiKV instances. The collected data can be stored for up to 30 days. Top SQL presents you with visual charts and tables to quickly pinpoint which SQL statements are contributing the high CPU load of a TiDB or TiKV instance over a certain period of time.

Top SQL provides the following features:

* Visualize the top 5 types of SQL statements with the highest CPU overhead through charts and tables.
* Display detailed execution information such as queries per second, average latency, and query plan.
* Collect all SQL statements that are executed, including those that are still running.
* Allow viewing data of a specific TiDB and TiKV instance.

## Recommended scenarios

Top SQL is suitable for analyzing performance issues. The following are some typical Top SQL scenarios:

* You discovered that an individual TiKV instance in the cluster has a very high CPU usage through the Grafana charts. You want to know which SQL statements cause the CPU hotspots so that you can optimize them and better leverage all of your distributed resources.
* You discovered that the cluster has a very high CPU usage overall and queries are slow. You want to quickly figure out which SQL statements are currently consuming the most CPU resources so that you can optimize them.
* The CPU usage of the cluster has drastically changed and you want to know the major cause.
* Analyze the most resource-intensive SQL statements in the cluster and optimize them to reduce hardware costs.

Top SQL cannot be used to pinpoint non-performance issues, such as incorrect data or abnormal crashes.

The Top SQL feature is still in an early stage and is being continuously enhanced. Here are some scenarios that are **not supported** at the moment:

* Analyzing the overhead of SQL statements outside of Top 5 (for example, when multiple business workloads are mixed).
* Analyzing the overhead of Top N SQL statements by various dimensions such as users and databases.
* Analyzing database performance issues that are not caused by high CPU load, such as transaction lock conflicts.

## Access the page

You can access the Top SQL page using either of the following methods:

* After logging in to TiDB Dashboard, click **Top SQL** in the left navigation menu.

  ![Top SQL](/media/dashboard/top-sql-access.png)

* Visit <http://127.0.0.1:2379/dashboard/#/topsql> in your browser. Replace `127.0.0.1:2379` with the actual PD instance address and port.

## Enable Top SQL

> **Note:**
>
> To use Top SQL, your cluster should be deployed or upgraded with a recent version of TiUP (v1.9.0 or above) or TiDB Operator (v1.3.0 or above). If your cluster was upgraded using an earlier version of TiUP or TiDB Operator, see [FAQ](/dashboard/dashboard-faq.md#a-required-component-ngmonitoring-is-not-started-error-is-shown) for instructions.

Top SQL is not enabled by default as it has a slight impact on cluster performance (within 3% on average) when enabled. You can enable Top SQL by the following steps:

1. Visit the [Top SQL page](#access-the-page).
2. Click **Open Settings**. On the right side of the **Settings** area, switch on **Enable Feature**.
3. Click **Save**.

After enabling the feature, wait up to 1 minute for Top SQL to load the data. Then you can see the CPU load details.

In addition to the UI, you can also enable the Top SQL feature by setting the TiDB system variable [`tidb_enable_top_sql`](/system-variables.md#tidb_enable_top_sql-new-in-v540):

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_enable_top_sql = 1;
```

## Use Top SQL

The following are the common steps to use Top SQL.

1. Visit the [Top SQL page](#access-the-page).

2. Select a particular TiDB or TiKV instance that you want to observe the load.

   ![Select Instance](/media/dashboard/top-sql-usage-select-instance.png)

   If you are unsure of which TiDB or TiKV instance to observe, you can select an arbitrary instance. Also, when the cluster CPU load is extremely unbalanced, you can first use Grafana charts to determine the specific instance you want to observe.

3. Observe the charts and tables presented by Top SQL.

   ![Chart and Table](/media/dashboard/top-sql-usage-chart.png)

   The size of the bars in the bar chart represents the size of CPU resources consumed by the SQL statement at that moment. Different colors distinguish different types of SQL statements. In most cases, you only need to focus on the SQL statements that have a higher CPU resource overhead in the corresponding time range in the chart.

4. Click a SQL statement in the table to show more information. You can see detailed execution metrics of different plans of that statement, such as Call/sec (average queries per second) and Scan Indexes/sec (average number of index rows scanned per second).

   ![Details](/media/dashboard/top-sql-details.png)

5. Based on these initial clues, you can further explore the [SQL Statement](/dashboard/dashboard-statement-list.md) or [Slow Queries](/dashboard/dashboard-slow-query.md) page to find the root cause of high CPU consumption or large data scans of the SQL statement.

Additionally, you can configure Top SQL as follows:

* You can adjust the time range in the time picker or select a time range in the chart to get a more precise and detailed look at the problem. A smaller time range can provide more detailed data, with precision of up to 1 second.

  ![Change time range](/media/dashboard/top-sql-usage-change-timerange.png)

* If the chart is out of date, you can click the **Refresh** button or select Auto Refresh options from the **Refresh** drop-down list.

  ![Refresh](/media/dashboard/top-sql-usage-refresh.png)

## Disable Top SQL

You can disable this feature by following these steps:

1. Visit [Top SQL page](#access-the-page).
2. Click the gear icon in the upper right corner to open the settings screen and switch off **Enable Feature**.
3. Click **Save**.
4. In the popped-up dialog box, click **Disable**.

In addition to the UI, you can also disable the Top SQL feature by setting the TiDB system variable [`tidb_enable_top_sql`](/system-variables.md#tidb_enable_top_sql-new-in-v540):

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_enable_top_sql = 0;
```

## Frequently asked questions

**1. Top SQL cannot be enabled and the UI displays "required component NgMonitoring is not started"**.

See [TiDB Dashboard FAQ](/dashboard/dashboard-faq.md#a-required-component-ngmonitoring-is-not-started-error-is-shown).

**2. Will performance be affected after enabling Top SQL?**

This feature has a slight impact on cluster performance. According to our benchmark, the average performance impact is usually less than 3% when the feature is enabled.

**3. What is the status of this feature?**

It is now a generally available (GA) feature and can be used in production environments.

**4. What is the meaning of "Other Statements"?**

"Other Statement" counts the total CPU overhead of all non-Top 5 statements. With this information, you can learn the CPU overhead contributed by the Top 5 statements compared with the overall.

**5. What is the relationship between the CPU overhead displayed by Top SQL and the actual CPU usage of the process?**

Their correlation is strong but they are not exactly the same thing. For example, the cost of writing multiple replicas is not counted in the TiKV CPU overhead displayed by Top SQL. In general, SQL statements with higher CPU usage result in higher CPU overhead displayed in Top SQL.

**6. What is the meaning of the Y-axis of the Top SQL chart?**

It represents the size of CPU resources consumed. The more resources consumed by a SQL statement, the higher the value is. In most cases, you do not need to care about the meaning or unit of the specific value.

**7. Does Top SQL collect running (unfinished) SQL statements?**

Yes. The bars displayed in the Top SQL chart at each moment indicate the CPU overhead of all running SQL statements at that moment.
