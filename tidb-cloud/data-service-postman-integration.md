---
title: Run Data App in Postman
summary: Learn how to run your Data App in Postman.
---

# Run Data App in Postman

[Postman](https://www.postman.com/) is an API platform that simplifies the API lifecycle and enhances collaboration for faster and better API development.

In TiDB Cloud [Data Service](https://tidbcloud.com/console/data-service), you can easily import your Data App to Postman and leverage Postman's extensive tools to enhance your API development experience.

This document describes how to import your Data App to Postman and how to run your Data App in Postman.

## Before you begin

Before importing a Data App to Postman, make sure that you have the following:

- A [Postman](https://www.postman.com/) account
- A [Postman desktop app](https://www.postman.com/downloads) (optional). Alternatively, you can use the Postman web version without downloading the app.
- A [Data App](/tidb-cloud/data-service-manage-data-app.md) with at least one well-defined [endpoint](/tidb-cloud/data-service-manage-endpoint.md). Only endpoints that meet the following requirements can be imported to Postman:

    - The target cluster is selected.
    - The endpoint path and request method are configured.
    - The SQL statements are written.

- An [API key](/tidb-cloud/data-service-api-key.md#create-an-api-key) for the Data App.

## Step 1. Import your Data App to Postman

To import your Data App to Postman, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. In the upper-right corner of the page, click **Run in Postman**. A dialog with import instructions is displayed.

    > **Note:**
    >
    > - If a Data App lacks a well-defined endpoint (the target cluster, path, request method, and SQL statements are configured), **Run in Postman** remains disabled for the Data App.
    > - For a Chat2Query Data App, **Run in Postman** is not available.

4. Follow the steps provided in the dialog for the Data App import:

    1. Depending on your preference, choose either **Run in Postman for Web** or **Run in Postman Desktop** to open your Postman workspaces, and then select your target workspace.

        - If you have not logged into Postman, follow the on-screen instructions to log into Postman first.
        - If you clicked **Run in Postman Desktop**, follow the on-screen instructions to launch the Postman desktop app.

    2. On the page of your target workspace in Postman, click **Import** in the left navigation menu.
    3. Copy the Data App URL from the TiDB Cloud dialog, and then paste the URL to Postman for the import.

5. After you paste the URL, Postman imports the Data App automatically as a new [collection](https://learning.postman.com/docs/collections/collections-overview). The name of the collection is in the `TiDB Data Service - <Your App Name>` format.

    In the collection, the deployed endpoints are grouped under the **Deployed** folder and the un-deployed endpoints are grouped under the **Draft** folder.

## Step 2. Configure your Data App API key in Postman

Before running the imported Data App in Postman, you need to configure the API key for the Data App in Postman as follows:

1. In the left navigation menu of Postman, click `TiDB Data Service - <Your App Name>` to open a tab for it on the right side.
2. Under the `TiDB Data Service - <Your App Name>` tab, click the **Variables** tab.
3. In the variable table, enter the public key and private key for your Data App in the **Current value** column.
4. In the upper-right corner of the `TiDB Data Service - <Your App Name>` tab, click **Save**.

## Step 3. Run Data App in Postman

To run your Data App in Postman, take the following steps:

1. In the left navigation pane of Postman, expand the **Deployed** or **Draft** folder, and then click your endpoint name to open a tab for it on the right side.
2. Under the `<Your Endpoint Name>` tab, you can call your endpoint as follows:

    - For an endpoint without parameters, you can click **Send** to call it directly.
    - For an endpoint with parameters, you need to fill in the parameter values first, and then click **Send**.

        - For a `GET` or `DELETE` request, fill in the parameter values in the **Query Params** table.
        - For a `POST` or `PUT` request, click the **Body** tab, and then fill in the parameter values as a JSON object. If **Batch Operation** is enabled for the endpoint in TiDB Cloud Data Service, fill in the parameter values as an array of JSON objects.

3. Check the response in the lower pane.

4. If you want to call the endpoint again with different parameter values, you can edit the parameter values accordingly, and then click **Send** again.

To learn more about the Postman usage, see [Postman documentation](https://learning.postman.com/docs).

## Deal with new changes in Data App

After a Data App is imported to Postman, TiDB Cloud Data Service will not automatically synchronize new changes of the Data App to Postman.

If you want any new changes to reflect in Postman, you have to [follow the import process](#step-1-import-your-data-app-to-postman) once again. Because the collection name is unique in a Postman workspace, you can either use the latest Data App to replace the previously imported one or import the latest Data App as a new collection.

Also, after re-importing the Data App, you will have to [configure the API key for the newly imported App](#step-2-configure-your-data-app-api-key-in-postman) in Postman again.