---
title: Integrate TiDB Cloud with n8n
summary: Learn the use of TiDB Cloud node in n8n.
---

# Integrate TiDB Cloud with n8n

[n8n](https://n8n.io/) is an extendable workflow automation tool. With a [fair-code](https://faircode.io/) distribution model, n8n will always have visible source code, be available to self-host, and allow you to add your custom functions, logic, and apps.

This document introduces how to build an auto-workflow: create a TiDB Serverless cluster, gather Hacker News RSS, store it to TiDB and send a briefing email.

## Prerequisites: Get TiDB Cloud API key

1. Access your TiDB Cloud dashboard.
2. Click <MDSvgIcon name="icon-top-organization" />, and then click **Organization Settings** in the lower-left corner.
3. Click the **API Keys** tab.
4. Click the **Create API Key** button to create a new API key.
5. Save the created API key for later use in n8n.

For more information, see [TiDB Cloud API Overview](/tidb-cloud/api-overview.md).

## Step 1: Install n8n

There are two ways to install your self-hosting n8n. Choose whichever works for you.

<SimpleTab>
<div label="npm">

1. Install [node.js](https://nodejs.org/en/download/) on your workspace.
2. Download and start n8n by `npx`.

    ```shell
    npx n8n
    ```

</div>
<div label="Docker">

1. Install [Docker](https://www.docker.com/products/docker-desktop) on your workspace.
2. Download and start n8n by `docker`.

    ```shell
    docker run -it --rm --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n
    ```

</div>
</SimpleTab>

After starting n8n, you can visit [localhost:5678](http://localhost:5678) to try out n8n.

## Step 2: Install TiDB Cloud node in n8n

TiDB Cloud node is named `n8n-nodes-tidb-cloud` in the npm repository. You need to install this node manually to control TiDB Cloud with n8n.

1. In the [localhost:5678](http://localhost:5678) page, create an owner account for self-hosting n8n.
2. Go to **Settings** > **Community nodes**.
3. Click **Install a community node**.
4. In the **npm Package Name** field, enter `n8n-nodes-tidb-cloud`.
5. Click **Install**.

Then you can search the **TiDB Cloud** node in **Workflow** > search bar and use the TiDB Cloud node by dragging it to a workspace.

## Step 3: Build your workflow

In this step, you will create a new workflow to insert some data to TiDB when you click **Execute** button.

This example usage workflow would use the following nodes:

- [Schedule Trigger](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.scheduletrigger/)
- [RSS Read](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.rssfeedread/)
- [Code](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.code/)
- [Gmail](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.gmail/)
- [TiDB Cloud node](https://www.npmjs.com/package/n8n-nodes-tidb-cloud)

The final workflow should look like the following image.

![img](/media/tidb-cloud/integration-n8n-workflow-rss.jpg)

### (Optional) Create a TiDB Serverless cluster

If you don't have a TiDB Serverless cluster, you can use this node to create one. Otherwise, feel free to skip this operation.

1. Navigate to **Workflows** panel, and click **Add workflow**.
2. In new workflow workspace, click **+** in the top right corner and choose **All** field.
3. Search `TiDB Cloud` and drag it to the workspace.
4. Enter credentials, which is the TiDB Cloud API key, for the TiDB Cloud node.
5. In the **Project** list, select your project.
6. In the **Operation** list, select `Create Serverless Cluster`.
7. In the **Cluster Name** box, enter a cluster name.
8. In the **Region** list, select a region.
9. In the **Password** box, enter a password used to log in to your TiDB clusters.
10. Click **Execute Node** to run the node.

> **Note:**
>
> It takes several seconds to create a new TiDB Serverless cluster.

### Create a workflow

#### Use a manual trigger as the workflow's starter

1. If you don't have a workflow yet, navigate to the **Workflows** panel, and click **Start from scratch**. Otherwise, skip this step.
2. Click **+** in the top right corner and search `schedule trigger`.
3. Drag the manual trigger node to your workspace, and double-click the node. The **Parameters** dialog is displayed.
4. Configure the rule as follows:

    - **Trigger Interval**: `Days`
    - **Days Between Triggers**: `1`
    - **Trigger at Hour**: `8am`
    - **Trigger at Minute**: `0`

This trigger will execute your workflow every morning at 8 AM.

#### Create a table used to insert data

1. Click **+** to the right of the manual trigger node.
2. Search `TiDB Cloud` and add it to the workspace.
3. In the **Parameters** dialog, enter the credential for the TiDB Cloud node. The credential is your TiDB Cloud API key.
4. In the **Project** list, select your project.
5. In the **Operation** list, select `Execute SQL`.
6. Select the cluster. If you have not seen your new cluster in the list, you need to wait a few minutes until the cluster creation is completed.
7. In the **User** list, select a user. TiDB Cloud always creates a default user, so you don't have to manually create one.
8. In the **Database** box, enter `test`.
9. Enter your database password.
10. In the **SQL** box, enter the following SQL:

    ```sql
    CREATE TABLE IF NOT EXISTS hacker_news_briefing (creator VARCHAR (200), title TEXT,  link VARCHAR(200), pubdate VARCHAR(200), comments VARCHAR(200), content TEXT, guid VARCHAR (200), isodate VARCHAR(200));
    ```

11. Click **Execute node** to create the table.

#### Get the Hacker News RSS

1. Click **+** to the right of the TiDB Cloud node.
2. Search `RSS Read` and add it to the workspace.
3. In the **URL** box, enter `https://hnrss.org/frontpage`.

#### Insert data to TiDB

1. Click **+** to the right of the RSS Read node.
2. Search `TiDB Cloud` and add it to the workspace.
3. Select the credentials that you entered in the previous TiDB Cloud node.
4. In the **Project** list, select your project.
5. In the **Operation** list, select `Insert`.
6. In **Cluster**, **User**, **Database** and **Password** boxes, enter the corresponding values.
7. In the **Table** box, enter the `hacker_news_briefing` table.
8. In the **Columns** box, enter `creator, title, link, pubdate, comments, content, guid, isodate`.

#### Build message

1. Click **+** to the right of the RSS Feed Read node.
2. Search `code` and add it to the workspace.
3. Select the `Run Once for All Items` mode.
4. In the **JavaScript** box, copy and paste the following code.

    ```javascript
    let message = "";

    // Loop the input items
    for (item of items) {
      message += `
          <h3>${item.json.title}</h3>
          <br>
          ${item.json.content}
          <br>
          `
    }

    let response =
        `
          <!DOCTYPE html>
          <html>
          <head>
          <title>Hacker News Briefing</title>
        </head>
        <body>
            ${message}
        </body>
        </html>
        `
    // Return our message
    return [{json: {response}}];
    ```

#### Send message by Gmail

1. Click **+** to the right of the code node.
2. Search `gmail` and add it to the workspace.
3. Enter the credential for the Gmail node. For detailed instructions, refer to [n8n documentation](https://docs.n8n.io/integrations/builtin/credentials/google/oauth-single-service/).
4. In the **Resource** list, select `Message`.
5. In the **Operation** list, select `Send`.
6. In the **To** box, enter your email.
7. In the **Subject** box, enter `Hacker News Briefing`.
8. In the **Email Type** box, select `HTML`.
9. In the **Message** box, click `Expression` and enter `{{ $json["response"] }}`.

    > **Note:**
    >
    > You must hover over the **Message** box and select the **Expression** pattern.

## Step 4: Run your workflow

After building up the workflow, you can click **Execute Workflow** to test run it.

If the workflow runs as expected, you'll get Hacker News briefing emails. These news contents will be logged to your TiDB Serverless cluster, so you don't have to worry about losing them.

Now you can activate this workflow in the **Workflows** panel. This workflow will help you get the front-page articles on Hacker News every day.

## TiDB Cloud node core

### Supported operations

TiDB Cloud node acts as a [regular node](https://docs.n8n.io/workflows/nodes/#regular-nodes) and only supports the following five operations:

- **Create Serverless Cluster**: creates a TiDB Serverless cluster.
- **Execute SQL**: executes an SQL statement in TiDB.
- **Delete**: deletes rows in TiDB.
- **Insert**: inserts rows in TiDB.
- **Update**: updates rows in TiDB.

### Fields

To use different operations, you need to fill in the different required fields. The following shows the respective field descriptions for the corresponding operation.

<SimpleTab>
<div label="Create Serverless Cluster">

- **Credential for TiDB Cloud API**: only supports TiDB Cloud API key. For how to create an API key, refer to [Get TiDB Cloud API Key](#prerequisites-get-tidb-cloud-api-key).
- **Project**: the TiDB Cloud project name.
- **Operation**: the operation of this node. For all supported operations, refer to [Supported operations](#supported-operations).
- **Cluster**: the TiDB Cloud cluster name. Enter the name for your new cluster.
- **Region**: the region name. Choose a region where your cluster will be deployed. Usually, choose the region closest to your application deployment.
- **Password**: the root password. Set a password for your new cluster.

</div>
<div label="Execute SQL">

- **Credential for TiDB Cloud API**: only supports TiDB Cloud API key. For how to create an API key, refer to [Get TiDB Cloud API Key](#prerequisites-get-tidb-cloud-api-key).
- **Project**: the TiDB Cloud project name.
- **Operation**: the operation of this node. For all supported operations, refer to [Supported operations](#supported-operations).
- **Cluster**: the TiDB Cloud cluster name. You should choose one existing cluster.
- **Password**: the password of the TiDB Cloud cluster.
- **User**: the username of the TiDB Cloud cluster.
- **Database**: the database name.
- **SQL**: the SQL statement to be executed.

</div>
<div label="Delete">

- **Credential for TiDB Cloud API**: only supports TiDB Cloud API key. For how to create an API key, refer to [Get TiDB Cloud API Key](#prerequisites-get-tidb-cloud-api-key).
- **Project**: the TiDB Cloud project name.
- **Operation**: the operation of this node. For all supported operations, refer to [Support Operation](#supported-operations).
- **Cluster**: the TiDB Cloud cluster name. You should choose one existing cluster.
- **Password**: the password of the TiDB Cloud cluster.
- **User**: the username of the TiDB Cloud cluster.
- **Database**: the database name.
- **Table**: the table name. You can use the `From list` mode to choose one or use the `Name` mode to type the table name manually.
- **Delete Key**: the name of the item's property that decides which rows in the database are deleted. An item is the data sent from one node to another. A node performs its action on each item of the incoming data. For more information about items in n8n, see [n8n documentation](https://docs.n8n.io/workflows/items/).

</div>
<div label="Insert">

- **Credential for TiDB Cloud API**: only supports TiDB Cloud API key. For how to create an API key, refer to [Get TiDB Cloud API Key](#prerequisites-get-tidb-cloud-api-key).
- **Project**: the TiDB Cloud project name.
- **Operation**: the operation of this node. For all supported operations, refer to [Support Operation](#supported-operations).
- **Cluster**: the TiDB Cloud cluster name. You should choose one existing cluster.
- **Password**: the password of the TiDB Cloud cluster.
- **User**: the username of the TiDB Cloud cluster.
- **Database**: the database name.
- **Table**: the table name. You can use the `From list` mode to choose one or use the `Name` mode to type the table name manually.
- **Columns**: The comma-separated list of the input item's properties, which are used as columns for the new rows. An item is the data sent from one node to another. A node performs its action on each item of the incoming data. For more information about items in n8n, see [n8n documentation](https://docs.n8n.io/workflows/items/).

</div>
<div label="Update">

- **Credential for TiDB Cloud API**: only supports TiDB Cloud API key. For how to create an API key, refer to [Get TiDB Cloud API Key](#prerequisites-get-tidb-cloud-api-key).
- **Project**: the TiDB Cloud project name.
- **Operation**: the operation of this node. For all supported operations, refer to [Support Operation](#supported-operations).
- **Cluster**: the TiDB Cloud cluster name. You should choose one existing cluster.
- **Password**: the password of the TiDB Cloud cluster.
- **User**: the username of the TiDB Cloud cluster.
- **Database**: the database name.
- **Table**: the table name. You can use the `From list` mode to choose one or use the `Name` mode to type the table name manually.
- **Update Key**: the name of the item's property that decides which rows in the database are updated. An item is the data sent from one node to another. A node performs its action on each item of the incoming data. For more information about items in n8n, see [n8n documentation](https://docs.n8n.io/workflows/items/).
- **Columns**: The comma-separated list of the input item's properties, which are used as columns for the rows to be updated.

</div>
</SimpleTab>

### Limitations

- Normally only one SQL statement is allowed in the **Execute SQL** operation. If you want to execute more than one statement in a single operation, you need to manually enable [`tidb_multi_statement_mode`](https://docs.pingcap.com/tidbcloud/system-variables#tidb_multi_statement_mode-new-in-v4011).
- For the **Delete** and **Update** operations, you need to specify one field as a key. For example, the `Delete Key` is set to `id`, which is equivalent to executing `DELETE FROM table WHERE id = ${item.id}`. Currently, the **Delete** and **Update** operations only support specifying one key.
- For the **Insert** and **Update** operations, you need to specify the comma-separated list in the **Columns** field, and the field name must be the same as the input item's property.
