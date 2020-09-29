---
title: Slow Queries Page of TiDB Dashboard
summary: Learn the Slow Queries page of TiDB Dashboard.
aliases: ['/docs/dev/dashboard/dashboard-slow-query/']
---

# Slow Queries Page of TiDB Dashboard

On the Slow Queries page of TiDB Dashboard, you can search and view all slow queries in the cluster.

By default, SQL queries with an execution time of more than 300 milliseconds are considered as slow queries. These queries are recorded in the [slow query logs](/identify-slow-queries.md) and can be searched via TiDB Dashboard. You can adjust the threshold of slow queries through the [`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold) session variable or the [`slow-threshold`](/tidb-configuration-file.md#slow-threshold) TiDB parameter.

> **Note:**
>
> If the slow query log is disabled, this feature will be unavailable. The slow query log is enabled by default, and you can enable or disable the slow query log through the [`enable-slow-log`](/tidb-configuration-file.md#enable-slow-log) TiDB configuration item.

## Access the page

You can use one of the following two methods to access the slow query page:

* After logging into TiDB Dashboard, click **Slow Queries** on the left navigation menu:

![Access slow query page](/media/dashboard/dashboard-slow-queries-access.png)

* Visit <http://127.0.0.1:2379/dashboard/#/slow_query> in your browser. Replace `127.0.0.1:2379` with the actual PD address and port.

All data displayed on the slow query page comes from TiDB slow query system tables and slow query logs. See [slow query logs](/identify-slow-queries.md) for details.

### Change Filters

You can filter slow queries based on the time range, the related database, SQL keywords, SQL types, the number of slow queries to be displayed. In the image below, 100 slow queries over the recent 30 minutes are displayed by default.

![Modify list filters](/media/dashboard/dashboard-slow-queries-list1.png)

### Display More Columns

Click **Columns** on the page and you can choose to see more columns. You can move your mouse to the **(i)** icon at the right side of a column name to view the description of this column:

![Show more columns](/media/dashboard/dashboard-slow-queries-list2.png)

### Sort by Column

By default, the list is sorted by **Finish Time** in the descending order. Click column headings to sort by the column or switch the sorting order:

![Modify sorting basis](/media/dashboard/dashboard-slow-queries-list3.png)

## View execution details

Click any item in the list to display detailed execution information of the slow query, including:

- Query: The text of the SQL statement (see area 1 in the image below);
- Plan: The execution plan of the slow query. See [Understand the Query Execution Plan](/explain-overview.md) to learn how to read the execution plan (see area 2 in the image below);
- Other sorted SQL execution information (see area 3 in the image below).

![View execution details](/media/dashboard/dashboard-slow-queries-detail1.png)

Click the **Expand** link to show the detailed information of an item. Click the **Copy** link to copy the detailed information to the clipboard.

Click the corresponding tab titles to switch information of different sorted SQL executions.

![Show different sorted execution information](/media/dashboard/dashboard-slow-queries-detail2.png)
