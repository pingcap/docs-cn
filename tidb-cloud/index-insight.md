---
title: Index Insight (Beta)
summary: Learn how to use the Index Insight feature in TiDB Cloud and obtain index recommendations for slow queries.
---

# Index Insight (Beta)

The Index Insight (beta) feature in TiDB Cloud provides powerful capabilities to optimize query performance by offering index recommendations for slow queries that are not using indexes effectively. This document walks you through the steps to enable and utilize the Index Insight feature effectively.

> **Note:**
>
> Index Insight is currently in beta and only available for [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters.

## Introduction

The Index Insight feature provides you with the following benefits:

- Enhanced query performance: Index Insight identifies slow queries and suggests appropriate indexes for them, thereby speeding up query execution, reducing response time, and improving user experience.
- Cost efficiency: By using Index Insight to optimize query performance, the need for extra computing resources is reduced, enabling you to use existing infrastructure more effectively. This can potentially lead to operational cost savings.
- Simplified optimization process: Index Insight simplifies the identification and implementation of index improvements, eliminating the need for manual analysis and guesswork. As a result, you can save time and effort with accurate index recommendations.
- Improved application efficiency: By using Index Insight to optimize database performance, applications running on TiDB Cloud can handle larger workloads and serve more users concurrently, which makes scaling operations of applications more efficient.

## Usage

This section introduces how to enable the Index Insight feature and obtain recommended indexes for slow queries.

### Before you begin

Before enabling the Index Insight feature, make sure that you have created a TiDB Dedicated cluster. If you do not have one, follow the steps in [Create a TiDB Dedicated cluster](/tidb-cloud/create-tidb-cluster.md) to create one.

### Step 1: Enable Index Insight

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the cluster overview page of your TiDB Dedicated cluster, and then click **Diagnosis** in the left navigation pane.

2. Click the **Index Insight BETA** tab. The **Index Insight overview** page is displayed.

3. To use the Index Insight feature, you need to create a dedicated SQL user, which is used to trigger the feature and receive index recommendations. The following SQL statements create a new SQL user with required privileges, including read privilege for `information_schema` and `mysql`, and `PROCESS` and `REFERENCES` privileges for all databases. Replace `'index_insight_user'` and `'random_password'` with your values.

    ```sql
    CREATE user 'index_insight_user'@'%' IDENTIFIED by 'random_password';
    GRANT SELECT ON information_schema.* TO 'index_insight_user'@'%';
    GRANT SELECT ON mysql.* TO 'index_insight_user'@'%';
    GRANT PROCESS, REFERENCES ON *.* TO 'index_insight_user'@'%';
    FLUSH PRIVILEGES;
    ```

    > **Note:**
    >
    > To connect to your TiDB Dedicated cluster, see [Connect to a TiDB Dedicated cluster](/tidb-cloud/connect-to-tidb-cluster.md).

4. Enter the username and password of the SQL user created in the preceding step. Then, click **Activate** to initiate the activation process.

### Step 2: Manually trigger Index Insight

To obtain index recommendations for slow queries, you can manually trigger the Index Insight feature by clicking **Check Up** in the upper-right corner of the **Index Insight overview** page.

Then, the feature begins scanning slow queries from the past three hours. After the scan finishes, it provides a list of index recommendations based on its analysis.

### Step 3: View index recommendations

To view the details of a specific index recommendation, click the insight from the list. The **Index Insight Details** page is displayed.

On this page, you can find the index recommendations, related slow queries, execution plans, and relevant metrics. This information helps you better understand the performance issues and evaluate the potential impact of implementing the index recommendations.

### Step 4: Implement index recommendations

Before implementing the index recommendations, you need to first review and evaluate the recommendations from the **Index Insight Details** page.

To implement the index recommendations, follow these steps:

1. Evaluate the impact of the proposed index on existing queries and workload.
2. Consider the storage requirements and potential trade-offs associated with the index implementation.
3. Use appropriate database management tools to create the index recommendations on the relevant tables.
4. Monitor the performance after implementing the indexes to assess the improvements.

## Best practices

This section introduces some best practices for using the Index Insight feature.

### Regularly trigger Index Insight

To maintain optimized indexes, it is recommended to trigger the Index Insight feature periodically, such as every day, or whenever substantial changes occur in your queries or database schema.

### Analyze impact before implementing indexes

Before implementing the index recommendations, analyze the potential impact on query execution plans, disk space, and any trade-offs involved. Prioritize implementing indexes that provide the most significant performance improvements.

### Monitor performance

Regularly monitor query performance after implementing the index recommendations. This helps you confirm the improvements and make further adjustments if necessary.

## FAQ

This section lists some frequently asked questions about the Index Insight feature.

### How to deactivate Index Insight?

To deactivate the Index Insight feature, perform the following steps:

1. In the upper-right corner of the **Index Insight overview** page, click **Settings**. The **Index Insight settings** page is displayed.
2. Click **Deactivate**. A confirmation dialog box is displayed.
3. Click **OK** to confirm the deactivation.

    After you deactivate the Index Insight feature, all index recommendations are removed from the **Index Insight overview** page. However, the SQL user created for the feature is not deleted. You can delete the SQL user manually.

### How to delete the SQL user after deactivating Index Insight?

After you deactivate the Index Insight feature, you can execute the `DROP USER` statement to delete the SQL user created for the feature. The following is an example. Replace `'username'` with your value.

```sql
DROP USER 'username';
```

### Why does the `invalid user or password` message show up during activation or check-up?

The `invalid user or password` message typically prompts when the system cannot authenticate the credentials you provided. This issue might occur due to various reasons, such as incorrect username or password, or an expired or locked user account.

To resolve this issue, perform the following steps:

1. Verify your credentials: Make sure that the username and password you provided are correct. Pay attention to case sensitivity.
2. Check account status: Make sure that your user account is in active status and not expired or locked. You can confirm this by contacting the system administrator or the relevant support channel.
3. Create a new SQL user: If this issue is not resolved by the preceding steps, you can create a new SQL user using the following statements. Replace `'index_insight_user'` and `'random_password'` with your values.

    ```sql
    CREATE user 'index_insight_user'@'%' IDENTIFIED by 'random_password';
    GRANT SELECT ON information_schema.* TO 'index_insight_user'@'%';
    GRANT SELECT ON mysql.* TO 'index_insight_user'@'%';
    GRANT PROCESS, REFERENCES ON *.* TO 'index_insight_user'@'%';
    FLUSH PRIVILEGES;
    ```

If you are still facing the issue after following the preceding steps, it is recommended to contact [PingCAP support team](/tidb-cloud/tidb-cloud-support.md).

### Why does the `no sufficient privileges` message show up during activation or check-up?

The `no sufficient privileges` message typically prompts when the SQL user you provided lacks the required privileges to request index recommendations from Index Insight.

To resolve this issue, perform the following steps:

1. Check the user privileges: Confirm if your user account has been granted the required privileges, including read privilege for `information_schema` and `mysql`, and `PROCESS` and `REFERENCES` privileges for all databases.

2. Create a new SQL user: If this issue is not resolved by the preceding steps, you can create a new SQL user using the following statements. Replace `'index_insight_user'` and `'random_password'` with your values.

    ```sql
    CREATE user 'index_insight_user'@'%' IDENTIFIED by 'random_password';
    GRANT SELECT ON information_schema.* TO 'index_insight_user'@'%';
    GRANT SELECT ON mysql.* TO 'index_insight_user'@'%';
    GRANT PROCESS, REFERENCES ON *.* TO 'index_insight_user'@'%';
    FLUSH PRIVILEGES;
    ```

If you are still facing the issue after following the preceding steps, it is recommended to contact [PingCAP support team](/tidb-cloud/tidb-cloud-support.md).

### Why does the `operations may be too frequent` message show up during using Index Insight?

The `operations may be too frequent` message typically prompts when you have exceeded the rate or usage limit set by Index Insight.

To resolve this issue, perform the following steps:

1. Slow down operations: If you receive this message, you need to decrease your operation frequency on Index Insight.
2. Contact support: If the issue persists, contact [PingCAP support team](/tidb-cloud/tidb-cloud-support.md) and provide details of the error message, your actions, and any other relevant information.

### Why does the `internal error` message show up during using Index Insight?

The `internal error` message typically prompts when the system encounters an unexpected error or issue. This error message is general and does not provide details about the underlying cause.

To resolve this issue, perform the following steps:

1. Retry the operation: Refresh the page or try the operation again. The error might be temporary and can be resolved by a simple retry.
2. Contact support: If the issue persists, contact [PingCAP support team](/tidb-cloud/tidb-cloud-support.md) and provide details of the error message, your actions, and any other relevant information.
