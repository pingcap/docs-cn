---
title: Slow Queries Page of TiDB Dashboard
summary: Learn the Slow Queries page of TiDB Dashboard.
aliases: ['/docs/dev/dashboard/dashboard-slow-query/']
---

# Slow Queries Page of TiDB Dashboard

On the Slow Queries page of TiDB Dashboard, you can search and view all slow queries in the cluster.

By default, SQL queries with an execution time of more than 300 milliseconds are considered as slow queries. These queries are recorded in the [slow query logs](/identify-slow-queries.md) and can be searched via TiDB Dashboard. You can adjust the threshold of slow queries through the [`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold) session variable or the [`instance.tidb_slow_log_threshold`](/tidb-configuration-file.md#tidb_slow_log_threshold) TiDB parameter.

> **Note:**
>
> If the slow query log is disabled, this feature will be unavailable. The slow query log is enabled by default, and you can enable or disable it through the system variable [`tidb_enable_slow_log`](/system-variables.md#tidb_enable_slow_log).

## Access the page

You can use one of the following two methods to access the slow query page:

* After logging in to TiDB Dashboard, click **Slow Queries** in the left navigation menu.

* Visit <http://127.0.0.1:2379/dashboard/#/slow_query> in your browser. Replace `127.0.0.1:2379` with the actual PD address and port.

All data displayed on the slow query page comes from TiDB slow query system tables and slow query logs. See [slow query logs](/identify-slow-queries.md) for details.

### Change filters

You can filter slow queries based on the time range, the related database, SQL keywords, SQL types, the number of slow queries to be displayed. In the image below, 100 slow queries over the recent 30 minutes are displayed by default.

![Modify list filters](/media/dashboard/dashboard-slow-queries-list1-v620.png)

### Display more columns

Click **Columns** on the page and you can choose to see more columns. You can move your mouse to the **(i)** icon at the right side of a column name to view the description of this column:

![Show more columns](/media/dashboard/dashboard-slow-queries-list2-v620.png)

### Export slow queries locally

Click ☰ (**More**) in the upper-right corner of the page to display the **Export** option. After you click **Export**, TiDB Dashboard exports slow queries in the current list as a CSV file.

![Export slow queries locally](/media/dashboard/dashboard-slow-queries-export-v651.png)

### Sort by column

By default, the list is sorted by **Finish Time** in the descending order. Click column headings to sort by the column or switch the sorting order:

![Modify sorting basis](/media/dashboard/dashboard-slow-queries-list3-v620.png)

## View execution details

Click any item in the list to display detailed execution information of the slow query, including:

- Query: The text of the SQL statement (area 1 in the following figure)
- Plan: The execution plan of the slow query (area 2 in the following figure)
- Other sorted SQL execution information (area 3 in the following figure)

![View execution details](/media/dashboard/dashboard-slow-queries-detail1-v620.png)

### SQL

Click the **Expand** button to view the detailed information of an item. Click the **Copy** button to copy the detailed information to the clipboard.

### Execution plans

On TiDB Dashboard, you can view execution plans in two ways: Graph and text. Visual execution plans allow you to learn each operator of a statement and detailed information more intuitively. See [Understand the Query Execution Plan](/explain-overview.md) to learn how to read a execution plan.

#### Visual execution plans

The following figure shows a visual execution plan.

![Visual execution plan](/media/dashboard/dashboard-visual-plan-2.png)

- The graph shows the execution from left to right, and from top to bottom.
- Upper nodes are parent operators and lower nodes are child operators.
- The color of the title bar indicates the component where the operator is executed: yellow stands for TiDB, blue stands for TiKV, and pink stands for TiFlash.
- The title bar shows the operator name and the text shown below is the basic information of the operator. 

Click the node area, and the detailed operator information is displayed on the right sidebar.

![Visual execution plan - sidebar](/media/dashboard/dashboard-visual-plan-popup.png)

### SQL execution details

Click the corresponding tab titles to switch information of SQL executions.

![Show different execution information](/media/dashboard/dashboard-slow-queries-detail2-v620.png)
