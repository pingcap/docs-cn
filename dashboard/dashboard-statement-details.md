---
title: Statement Execution Details of TiDB Dashboard
summary: View the execution details of a single SQL statement in TiDB Dashboard.
aliases: ['/docs/dev/dashboard/dashboard-statement-details/']
---

# Statement Execution Details of TiDB Dashboard

Click any item in the list to enter the detail page of the SQL statement to view more detailed information. This information includes the following parts:

- The overview of SQL statements, which includes the SQL template, the SQL template ID, the current time range of displayed SQL executions, the number of execution plans, the database in which the SQL statement is executed, and the fast plan binding feature (area 1 in the following figure).
- The execution plan list: If a SQL statement has multiple execution plans, this list is displayed. Besides text information of execution plans, TiDB v6.2.0 introduces visual execution plans, through which you can learn each operator of a statement and detailed information more intuitively. You can select different execution plans, and the details of the selected plans are displayed below the list (area 2 in the following figure).
- Execution detail of plans, which displays the detailed information of the selected execution plans. See [Execution plan in details](#execution-details-of-plans) (area 3 in the following figure).

![Details](/media/dashboard/dashboard-statement-detail-v660.png)

## Fast plan binding

Starting from v6.6.0, TiDB introduces the fast plan binding feature. You can quickly bind a SQL statement to a specific execution plan in TiDB Dashboard.

### Usage

#### Bind an execution plan

1. Click **Plan Binding**. The **Plan Binding** dialog box is displayed.

    ![Fast plan binding - not bound - entry](/media/dashboard/dashboard-quick-binding-entry-notbound.png)

2. Select a plan that you want to bind and click **Bind**.

    ![Fast plan binding - popup](/media/dashboard/dashboard-quick-binding-popup-notbound.png)

3. After the binding is completed, you can see the **Bound** label.

    ![Fast plan binding - popup - binding completed](/media/dashboard/dashboard-quick-binding-popup-bound.png)

#### Drop an existing binding

1. On the page of a SQL statement that has an existing binding, click **Plan Binding**. The **Plan Binding** dialog box is displayed.

    ![Fast plan binding - bound - entry](/media/dashboard/dashboard-quick-binding-entry-bound.png)

2. Click **Drop**.

    ![Fast plan binding - popup - bound](/media/dashboard/dashboard-quick-binding-popup-bound.png)

3. After the binding is dropped, you can see the **Not bound** label.

    ![Fast plan binding - popup](/media/dashboard/dashboard-quick-binding-popup-notbound.png)

### Limitation

Currently, the fast plan binding feature does not support the following types of SQL statements:

- Statements that are not `SELECT`, `DELETE`, `UPDATE`, `INSERT`, or `REPLACE`
- Queries with subqueries
- Queries that access TiFlash
- Queries that join three or more tables

To use this feature, you must have the SUPER privilege. If you encounter permission issues while using it, refer to [TiDB Dashboard User Management](/dashboard/dashboard-user.md) to add the necessary privileges.

## Execution details of plans

The execution detail of plans includes the following information:

- SQL sample: The text of a certain SQL statement that is actually executed corresponding to the plan. Any SQL statement that has been executed within the time range might be used as a SQL sample.
- Execution plan: Complete information about execution plans, displayed in graph and text. For details of the execution plan, see [Understand the Query Execution Plan](/explain-overview.md). If multiple execution plans are selected, only (any) one of them is displayed.
- For basic information, execution time, Coprocessor read, transaction, and slow query of the SQL statement, you can click the corresponding tab titles to switch among different information.

![Execution details of plans](/media/dashboard/dashboard-statement-plans-detail.png)

### Basic Tab

The basic information of a SQL execution includes the table names, index name, execution count, and total latency. The **Description** column provides detailed description of each field.

![Basic information](/media/dashboard/dashboard-statement-plans-basic.png)

### Time Tab

Click the **Time** tab, and you can see how long each stage of the execution plan lasts.

> **Note:**
>
> Because some operations might be performed in parallel within a single SQL statement, the cumulative duration of each stage might exceed the actual execution time of the SQL statement.

![Execution time](/media/dashboard/dashboard-statement-plans-time.png)

### Coprocessor Read Tab

Click the **Coprocessor Read** tab, and you can see information related to Coprocessor read.

![Coprocessor read](/media/dashboard/dashboard-statement-plans-cop-read.png)

### Transaction Tab

Click the **Transaction** tab, and you can see information related to execution plans and transactions, such as the average number of written keys or the maximum number of written keys.

![Transaction](/media/dashboard/dashboard-statement-plans-transaction.png)

### Slow Query Tab

If an execution plan is executed too slowly, you can see its associated slow query records under the **Slow Query** tab.

![Slow Query](/media/dashboard/dashboard-statement-plans-slow-queries.png)

The information displayed in this area has the same structure with the slow query page. See [TiDB Dashboard Slow Query Page](/dashboard/dashboard-slow-query.md) for details.
