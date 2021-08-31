---
title: SQL Statements Page of TiDB Dashboard
summary: View the execution status of all SQL statements in the TiDB cluster.
aliases: ['/docs/dev/dashboard/dashboard-statement-list/']
---

# SQL Statements Page of TiDB Dashboard

The SQL statements page shows the execution status of all SQL statements in the cluster. This page is often used to analyze the SQL statement whose total or single execution time is long.

On this page, SQL queries with a consistent structure (even if the query parameters are inconsistent) are classified as the same SQL statement. For example, both `SELECT * FROM employee WHERE id IN (1, 2, 3)` and `select * from EMPLOYEE where ID in (4, 5)` are classified as the same `select * from employee where id in (...)` SQL statement.

## Access the page

You can use one of the following two methods to access the SQL statement summary page:

- After logging into TiDB Dashboard, click **SQL Statements** on the left navigation menu:

  ![Access SQL statement summary page](/media/dashboard/dashboard-statement-access.png)

- Visit <http://127.0.0.1:2379/dashboard/#/statement> in your browser. Replace `127.0.0.1:2379` with the actual PD instance address and port.

All the data shown on the SQL statement summary page are from the TiDB statement summary tables. For more details about the tables, see [TiDB Statement Summary Tables](/statement-summary-tables.md).

> **Note:**
>
> In the **Mean Latency** column of the SQL statement summary page, the blue bar indicates the average execution time. If there is a yellow line on the blue bar for an SQL statement, the left and right sides of the yellow line respectively represent the minimum and maximum execution time of the SQL statement during the recent data collection cycle. 

### Change Filters

On the top of the SQL statement summary page, you can modify the time range of SQL executions to be displayed. You can also filter the list by database in which SQL statements are executed, or by SQL types. The following image shows all SQL executions over the recent data collection cycle (recent 30 minutes by default).

![Modify filters](/media/dashboard/dashboard-statement-filter-options.png)

### Display More Columns

Click **Columns** on the page and you can choose to see more columns. You can move your mouse to the **(i)** icon at the right side of a column name to view the description of this column:

![Choose columns](/media/dashboard/dashboard-statement-columns-selector.png)

### Sort by Column

By default, the list is sorted by **Total Latency** from high to low. Click on different column headings to modify the sorting basis or switch the sorting order:

![Modify list sorting](/media/dashboard/dashboard-statement-change-order.png)

### Change Settings

On the list page, click the **Settings** button on the top right to change the settings of the SQL statements feature:

![Settings entry](/media/dashboard/dashboard-statement-setting-entry.png)

After clicking the **Settings** button, you can see the following setting dialog box:

![Settings](/media/dashboard/dashboard-statement-settings.png)

On the setting page, you can disable or enable the SQL statements feature. When the SQL statements feature is enabled, you can modify the following settings:

- Collect interval: The length of period for each SQL statement analysis, which is 30 minutes by default. The SQL statements feature summarizes and counts all SQL statements within a period of time. If the period is too long, the granularity of the summary is coarse, which is not good for locating problems; if the period is too short, the granularity of the statistics is fine, which is good for locating problems, but this will result in more records and more memory usage within the same data retention duration. Therefore, you need to adjust this value based on the actual situation, and properly lower this value when locating problems.
- Data retain duration: The retention duration of summary information, which is 1 day by default. Data retained longer than this duration will be deleted from system tables.

See [Configurations of Statement Summary Tables](/statement-summary-tables.md#parameter-configuration) for details.

> **Note:**
>
> + Because the statement system table is only stored in memory, after the SQL Statements feature is disabled, the data in the system table will be cleared.
>
> + The values of `Collect interval` and `retain duration` affect the memory usage, so it is recommended to adjust these values according to the actual situation. The value of `retain duration` should not be set too large.
