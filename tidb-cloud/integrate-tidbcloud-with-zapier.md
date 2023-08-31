---
title: Integrate TiDB Cloud with Zapier
summary: Learn how to connect TiDB Cloud to 5000+ Apps with Zapier.
---

# Integrate TiDB Cloud with Zapier

[Zapier](https://zapier.com) is a no-code automation tool that lets you easily create workflows that involve thousands of apps and services.

Using the [TiDB Cloud app](https://zapier.com/apps/tidb-cloud/integrations) on Zapier enables you to:

- Use TiDB, a MySQL-compatible HTAP database. No need to build locally.
- Make it easier to manage your TiDB Cloud.
- Connect TiDB Cloud to 5000+ apps and automate your workflows.

This guide gives a high-level introduction to the TiDB Cloud app on Zapier and an example of how to use it.

## Quick start with template

[Zap Templates](https://platform.zapier.com/partners/zap-templates) are ready made integrations or Zaps with the apps and core fields pre-selected, for publicly available Zapier integrations.

In this section, we will use the **Add new Github global events to TiDB rows** template as an example to create a workflow. In this workflow, every time a new global event (any [GitHub event](https://docs.github.com/en/developers/webhooks-and-events/events/github-event-types) happens from or to you, on any repo) is created from your GitHub account, Zapier adds a new row to your TiDB Cloud cluster.

### Prerequisites

Before you start, you need:

- A [Zapier account](https://zapier.com/app/login).
- A [GitHub account](https://github.com/login).
- A [TiDB Cloud account](https://tidbcloud.com/signup) and a TiDB Serverless cluster on TiDB Cloud. For more details, see [TiDB Cloud Quick Start](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart#step-1-create-a-tidb-cluster).

### Step 1: Get the template

Go to [TiDB Cloud App on Zapier](https://zapier.com/apps/tidb-cloud/integrations). Choose the **Add new Github global events to TiDB rows** template and click **Try it**. Then you will enter the editor page.

### Step 2: Set up the trigger

In the editor page, you can see the trigger and action. Click the trigger to set it up.

1. Choose app & event

    The template has set the app and the event by default, so you don't need to do anything here. Click **Continue**.

2. Choose account

    Choose a GitHub account that you want to connect with TiDB Cloud. You can either connect a new account or select an existing account. After you set up, click **Continue**.

3. Set up trigger

    The template has set the trigger by default. Click **Continue**.

4. Test trigger

    Click **Test trigger**. If the trigger is successfully set up, you can see the data of a new global event from the GitHub account. Click **Continue**.

### Step 3: Set up the `Find Table in TiDB Cloud` action

1. Choose app & event

    Keep the default value `Find Table` set by the template. Click **Continue**.

2. Choose account

    1. Click the **Sign in** button, and you will be redirected to a new login page.
    2. On the login page, fill in your public key and private key. To get the TiDB Cloud API key, follow the instructions in [TiDB Cloud API documentation](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management).
    3. Click **Continue**.

    ![Account](/media/tidb-cloud/zapier/zapier-tidbcloud-account.png)

3. Set up action

    In this step, you need to specify a table in your TiDB Cloud cluster to store the event data. If you do not already have a table, you can create one through this step.

    1. From the drop-down list, choose the project name and cluster name. The connection information of your cluster will be displayed automatically.

        ![Set up project name and cluster name](/media/tidb-cloud/zapier/zapier-set-up-tidbcloud-project-and-cluster.png)

    2. Enter your password.

    3. From the drop-down list, choose the database.

        ![Set up database name](/media/tidb-cloud/zapier/zapier-set-up-tidbcloud-databse.png)

        Zapier queries the databases from TiDB Cloud using the password you entered. If no database is found in your cluster, re-enter your password and refresh the page.

    4. In **The table you want to search** box, fill in `github_global_event`. If the table does not exist, the template uses the following DDL to create the table. Click **Continue**.

        ![The create table DDL](/media/tidb-cloud/zapier/zapier-tidbcloud-create-table-ddl.png)

4. Test action

    Click **Test action**, and Zapier will create the table. You can also skip the test, and the table will be created when this workflow is running for the first time.

### Step 4: Set up the `Create Row in TiDB Cloud` action

1. Choose app & event

    Keep the default value set by the template. Click **Continue**.

2. Choose account

    Select the account you have chosen when you set up the `Find Table in TiDB Cloud` action. Click **Continue**.

    ![Choose account](/media/tidb-cloud/zapier/zapier-tidbcloud-choose-account.png)

3. Set up action

    1. Fill in the **Project Name**, **Cluster Name**, **TiDB Password**, and **Database Name** as in the previous step.

    2. In the **Table Name**, choose the **github_global_event** table from the drop-down list. The columns of the table are displayed.

        ![Table columns](/media/tidb-cloud/zapier/zapier-set-up-tidbcloud-columns.png)

    3. In the **Columns** box, choose the corresponding data from the trigger. Fill in all the columns, and click **Continue**.

        ![Fill in Columns](/media/tidb-cloud/zapier/zapier-fill-in-tidbcloud-triggers-data.png)

4. Test action

    Click **Test action** to create a new row in the table. If you check your TiDB Cloud cluster, you can find the data is written successfully.

   ```sql
   mysql> SELECT * FROM test.github_global_event;
   +-------------+-------------+------------+-----------------+----------------------------------------------+--------+---------------------+
   | id          | type        | actor      | repo_name       | repo_url                                     | public | created_at          |
   +-------------+-------------+------------+-----------------+----------------------------------------------+--------+---------------------+
   | 25324462424 | CreateEvent | shiyuhang0 | shiyuhang0/docs | https://api.github.com/repos/shiyuhang0/docs | True   | 2022-11-18 08:03:14 |
   +-------------+-------------+------------+-----------------+----------------------------------------------+--------+---------------------+
   1 row in set (0.17 sec)
   ```

### Step 5: Publish your zap

Click **Publish** to publish your zap. You can see the zap is running in the [home page](https://zapier.com/app/zaps).

![Publish the zap](/media/tidb-cloud/zapier/zapier-tidbcloud-publish.png)

Now, this zap will automatically record all the global events from your GitHub account into TiDB Cloud.

## Triggers & Actions

[Triggers and actions](https://zapier.com/how-it-works) are the key concepts in Zapier. By combining different triggers and actions, you can create various automation workflows.

This section introduces the triggers and actions provided by TiDB Cloud App on Zapier.

### Triggers

The following table lists the triggers supported by TiDB Cloud App.

| Trigger                | Description                                                                 |
| ---------------------- |-----------------------------------------------------------------------------|
| New Cluster            | Triggers when a new cluster is created.                                     |
| New Table              | Triggers when a new table is created.                                       |
| New Row                | Triggers when new rows are created. Only fetches the recent 10000 new rows. |
| New Row (Custom Query) | Triggers when new rows are returned from a custom query that you provide.   |

### Actions

The following table lists the actions supported by TiDB Cloud App. Note that some actions need extra resources, and you need to prepare the corresponding resources before using the action.

| Action | Description | Resource |
|---|---|---|
| Find Cluster | Finds an existing TiDB Serverless or TiDB Dedicated cluster. | None |
| Create Cluster | Creates a new cluster. Only supports creating a TiDB Serverless cluster. | None |
| Find Database | Finds an existing database. | A TiDB Serverless cluster |
| Create Database | Creates a new database. | A TiDB Serverless cluster |
| Find Table | Finds an existing Table. | A TiDB Serverless cluster and a database |
| Create Table | Creates a new table. | A TiDB Serverless cluster and a database |
| Create Row | Creates a new row. | A TiDB Serverless cluster, a database, and a table |
| Update Row | Updates an existing row. | A TiDB Serverless cluster, a database, and a table |
| Find Row | Finds a row in a table via a lookup column. | A TiDB Serverless cluster, a database, and a table |
| Find Row (Custom Query) | Finds a row in a table via a custom query the you provide. | A TiDB Serverless cluster, a database, and a table |

## TiDB Cloud App templates

TiDB Cloud provides some templates for you to use in Zapier directly. You can find all the templates in the [TiDB Cloud App](https://zapier.com/apps/tidb-cloud/integrations) page.

Here are some examples:

- [Duplicate new TiDB Cloud rows in Google Sheets](https://zapier.com/apps/google-sheets/integrations/tidb-cloud/1134881/duplicate-new-tidb-cloud-rows-in-google-sheets).
- [Send emails via Gmail from new custom TiDB queries](https://zapier.com/apps/gmail/integrations/tidb-cloud/1134903/send-emails-via-gmail-from-new-custom-tidb-queries).
- [Add rows to TiDB Cloud from newly caught webhooks](https://zapier.com/apps/tidb-cloud/integrations/webhook/1134955/add-rows-to-tidb-cloud-from-newly-caught-webhooks).
- [Store new Salesforce contacts on TiDB rows](https://zapier.com/apps/salesforce/integrations/tidb-cloud/1134923/store-new-salesforce-contacts-on-tidb-rows).
- [Create TiDB rows for new Gmail emails with resumes and send direct Slack notifications](https://zapier.com/apps/gmail/integrations/slack/1135456/create-tidb-rows-for-new-gmail-emails-with-resumes-and-send-direct-slack-notifications)

## FAQ

### How can I set up the TiDB Cloud account in Zapier?

Zapier requires your **TiDB Cloud API key** to connect with your TiDB Cloud account. Zapier does not need your login account for TiDB Cloud.

To get your TiDB Cloud API key, follow the [TiDB Cloud API documentation](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management).

### How do TiDB Cloud triggers perform de-duplication?

Zapier triggers can work with a polling API call to check for new data periodically (the interval depends on your Zapier plan).

TiDB Cloud triggers provide a polling API call that returns a lot of results. However, most of the results have been seen by Zapier before, that is, most of the results are duplication.

Since we don’t want to trigger an action multiple times when an item in your API exists in multiple distinct polls, TiDB Cloud triggers deduplicate the data with the `id` field.

`New Cluster` and `New Table` triggers simply use the `cluster_id` or `table_id` as the `id` field to do the deduplication. You do not need to do anything for the two triggers.

**New Row Trigger**

The `New Row` trigger limits 10,000 results in every fetch. Therefore, if some new rows are not included in the 10,000 results, they cannot trigger Zapier.

One way to avoid this is to specify the `Order By` configuration in the trigger. For example, once you sort the rows by their creation time, the new rows will always be included in the 10,000 results.

The `New Row` trigger also uses a flexible strategy to generate the `id` field to do the deduplication. The trigger generates the `id` field in the following order:

1. If the result contains an `id` column, use the `id` column.
2. If you specify a `Dedupe Key` in the trigger configuration, use the `Dedupe Key`.
3. If the table has a primary key, use the primary key. If there are multiple primary keys, use the first column.
4. If the table has a unique key, use the unique key.
5. Use the first column of the table.

**New Row (Custom Query) Trigger**

The `New Row (Custom Query)` trigger limits 1,000,000 results in every fetch. 1,000,000 is a large number, and it is only set so as to protect the whole system. It is recommended that your query includes `ORDER BY` and `LIMIT`.

To perform deduplication, your query results must have a unique id field. Otherwise, you will get the `You must return the results with id field` error.

Make sure that your custom query executes in less than 30 seconds. Otherwise, you will get the timeout error.

### How do I use the `find or create` action?

`Find or create` action enables you to create a resource if it does not exist. Here is an example:

1. Choose `Find Table` action

2. In the`set up action` step, tick the `Create TiDB Cloud Table if it doesn’t exist yet?` box to enable `find and create`.

   ![Find and create](/media/tidb-cloud/zapier/zapier-tidbcloud-find-and-create.png)

This workflow creates a table if it does not exist yet. Note that the table will be created directly if you test your action.
