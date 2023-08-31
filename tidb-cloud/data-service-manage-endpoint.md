---
title: Manage an Endpoint
summary: Learn how to create, develop, test, deploy, and delete an endpoint in a Data App in the TiDB Cloud console.
---

# Manage an Endpoint

An endpoint in Data Service (beta) is a web API that you can customize to execute SQL statements. You can specify parameters for the SQL statements, such as the value used in the `WHERE` clause. When a client calls an endpoint and provides values for the parameters in a request URL, the endpoint executes the SQL statement with the provided parameters and returns the results as part of the HTTP response.

This document describes how to manage your endpoints in a Data App in the TiDB Cloud console.

## Before you begin

- Before you create an endpoint, make sure the following:

    - You have created a cluster and a Data App. For more information, see [Create a Data App](/tidb-cloud/data-service-manage-data-app.md#create-a-data-app).
    - The databases, tables, and columns that the endpoint will operate on already exist in the target cluster.

- Before you call an endpoint, make sure that you have created an API key in the Data App. For more information, see [Create an API key](/tidb-cloud/data-service-api-key.md#create-an-api-key).

## Create an endpoint

In Data Service, you can either generate an endpoint automatically or create an endpoint manually.

> **Tip:**
>
> You can also create an endpoint from a SQL file in Chat2Query (beta). For more information, see [Generate an endpoint from a SQL file](/tidb-cloud/explore-data-with-chat2query.md#generate-an-endpoint-from-a-sql-file).

### Generate an endpoint automatically

In TiDB Cloud Data Service, you can generate one or multiple endpoints automatically in one go as follows:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, locate your target Data App, click **+** to the right of the App name, and then click **Autogenerate Endpoint**. The dialog for endpoint generation is displayed.
3. In the dialog, do the following:

    1. Select the target cluster, database, and table for the endpoint to be generated.

        > **Note:**
        >
        > The **Table** drop-down list includes only user-defined tables with at least one column, excluding system tables and any tables without a column definition.

    2. Select at least one HTTP operation (such as `GET Retrieve`, `POST Create`, and `PUT Update`) for the endpoint to be generated.

        For each operation you selected, TiDB Cloud Data Service will generate a corresponding endpoint. If you have selected a batch operation (such as `POST Batch Create`), the generated endpoint lets you operate on multiple rows in a single request.

    3. (Optional) Configure a timeout and tag for the operations. All the generated endpoints will automatically inherit the configured properties, which can be modified later as needed.
    4. (Optional) The **Auto-Deploy Endpoint** option (disabled by default) controls whether to enable the direct deployment of the generated endpoints. When it is enabled, the draft review process is skipped, and the generated endpoints are deployed immediately without further manual review or approval.

4. Click **Generate**.

    The generated endpoint is displayed at the top of the endpoint list.

5. Check the generated endpoint name, SQL statements, properties, and parameters of the new endpoint.

    - Endpoint name: the generated endpoint name is the name of the selected table, and the request method (such as `GET`, `POST`, and `PUT`) is displayed before the name. For example, if the selected table name is `sample-table` and the selected operation is **POST Create**, the generated endpoint is displayed as `POST sample-table`.

        - If a batch operation is selected, TiDB Cloud Data Service appends `_batch` to the name of the generated endpoint. For example, if the selected table name is `sample-table` and the selected operation is **POST Batch Create**, the generated endpoint is displayed as `POST sample-table_batch`.
        - If there has been already an endpoint with the same request method and endpoint name, TiDB Cloud Data Service appends `_copy` to the name of the generated endpoint. For example, `sample-table_copy`.

    - SQL statements: TiDB Cloud Data Service automatically writes SQL statements for the generated endpoints according to the table column specifications and the selected endpoint operations. You can click the endpoint name to view its SQL statements in the middle section of the page.
    - Endpoint properties: TiDB Cloud Data Service automatically configures the endpoint path, request method, timeout, and tag according to your selection. You can find the properties in the right pane of the page.
    - Endpoint parameters: TiDB Cloud Data Service automatically configures parameters for the generated endpoints. You can find the parameters in the right pane of the page.

6. If you want to modify the details of the generated endpoint, such as its name, SQL statements, properties, or parameters, refer to the instructions provided in [Develop an endpoint](#deploy-an-endpoint).

### Create an endpoint manually

To create an endpoint manually, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, locate your target Data App, click **+** to the right of the App name, and then click **Create Endpoint**.
3. Update the default name if necessary. The newly created endpoint is added to the top of the endpoint list.
4. Configure the new endpoint according to the instructions in [Develop an endpoint](#develop-an-endpoint).

## Develop an endpoint

For each endpoint, you can write SQL statements to execute on a TiDB cluster, define parameters for the SQL statements, or manage the name and version.

> **Note:**
>
> If you have connected your Data App to GitHub with **Auto Sync & Deployment** enabled, you can also update the endpoint configurations using GitHub. Any changes you made in GitHub will be deployed in TiDB Cloud Data Service automatically. For more information, see [Deploy automatically with GitHub](/tidb-cloud/data-service-manage-github-connection.md).

### Configure properties

On the right pane of the endpoint details page, you can click the **Properties** tab to view and configure properties of the endpoint.

#### Basic properties

- **Path**: the path that users use to access the endpoint.

    - The combination of the request method and the path must be unique within a Data App.
    - Only letters, numbers, underscores (`_`), and slashes (`/`) are allowed in a path. A path must start with a slash (`/`) and end with a letter, number, or underscore (`_`). For example, `/my_endpoint/get_id`.
    - The length of the path must be less than 64 characters.

- **Endpoint URL**: (read-only) the URL is automatically generated based on the region where the corresponding cluster is located, the service URL of the Data App, and the path of the endpoint. For example, if the path of the endpoint is `/my_endpoint/get_id`, the endpoint URL is `https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/my_endpoint/get_id`.

- **Request Method**: the HTTP method of the endpoint. The following methods are supported:

    - `GET`: use this method to query or retrieve data, such as a `SELECT` statement.
    - `POST`: use this method to insert or create data, such as an `INSERT` statement.
    - `PUT`: use this method to update or modify data, such as an `UPDATE` statement.
    - `DELETE`: use this method to delete data, such as a `DELETE` statement.

- **Description** (Optional): the description of the endpoint.

#### Advanced properties

- **Timeout(ms)**: the timeout for the endpoint, in milliseconds.
- **Max Rows**: the maximum number of rows that the endpoint can operate or return.
- **Tag**: the tag used for identifying a group of endpoints.
- **Pagination**: this property is available only when the request method is `GET` and the last SQL statement of the endpoint is a `SELECT` operation. When **Pagination** is enabled, you can paginate the results by specifying `page` and `page_size` as query parameters when calling the endpoint, such as `https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/my_endpoint/get_id?page=<Page Number>&page_size=<Page Size>`. For more information, see [Call an endpoint](#call-an-endpoint).

    > **Note:**
    >
    > - If you do not include the `page` and `page_size` parameters in the request, the default behavior is to return the maximum number of rows specified in the **Max Rows** property on a single page.
    > - The `page_size` must be less than or equal to the **Max Rows** property. Otherwise, an error is returned.

- **Cache Response**: this property is available only when the request method is `GET`. When **Cache Response** is enabled, TiDB Cloud Data Service can cache the response returned by your `GET` requests within a specified time-to-live (TTL) period.
- **Time-to-live (s)**: this property is available only when **Cache Response** is enabled. You can use it to specify the time-to-live (TTL) period in seconds for cached response. During the TTL period, if you make the same `GET` requests again, Data Service returns the cached response directly instead of fetching data from the target database again, which improves your query performance.
- **Batch Operation**: this property is visible only when the request method is `POST`, `PUT`, or `DELETE`. When **Batch Operation** is enabled, you can operate on multiple rows in a single request. For example, you can insert multiple rows of data in a single `POST` request by adding an array of data objects in the `--data-raw` option of your curl command when calling the endpoint.

### Write SQL statements

On the SQL editor of the endpoint details page, you can write and run the SQL statements for an endpoint. You can also simply type `--` followed by your instructions to let AI generate SQL statements automatically.

1. Select a cluster.

    > **Note:**
    >
    > Only clusters that are linked to the Data App are displayed in the drop-down list. To manage the linked clusters, see [Manage linked clusters](/tidb-cloud/data-service-manage-data-app.md#manage-linked-data-sources).

    On the upper part of the SQL editor, select a cluster on which you want to execute SQL statements from the drop-down list. Then, you can view all databases of this cluster in the **Schema** tab on the right pane.

2. Write SQL statements.

    Before querying or modifying data, you need to first specify the database in the SQL statements. For example, `USE database_name;`.

    In the SQL editor, you can write statements such as table join queries, complex queries, and aggregate functions. You can also simply type `--` followed by your instructions to let AI generate SQL statements automatically.

    To define a parameter, you can insert it as a variable placeholder like `${ID}` in the SQL statement. For example, `SELECT * FROM table_name WHERE id = ${ID}`. Then, you can click the **Params** tab on the right pane to change the parameter definition and test values. For more information, see [Parameters](#configure-parameters).

    > **Note:**
    >
    > - The parameter name is case-sensitive.
    > - The parameter cannot be used as a table name or column name.

3. Run SQL statements.

    If you have inserted parameters in the SQL statements, make sure that you have set test values or default values for the parameters in the **Params** tab on the right pane. Otherwise, an error is returned.

    To run a SQL statement, select the line of the SQL with your cursor and click **Run** > **Run at cursor**.

    To run all SQL statements in the SQL editor, click **Run**. In this case, only the last SQL results are returned.

    After running the statements, you can see the query results immediately in the **Result** tab at the bottom of the page.

### Configure parameters

On the right pane of the endpoint details page, you can click the **Params** tab to view and manage the parameters used in the endpoint.

In the **Definition** section, you can view and manage the following properties for a parameter:

- The parameter name: the name can only include letters, digits, and underscores (`_`) and must start with a letter or an underscore (`_`). **DO NOT** use `page` and `page_size` as parameter names, which are reserved for pagination of request results.
- **Required**: specifies whether the parameter is required in the request. The default configuration is set to not required.
- **Type**: specifies the data type of the parameter. Supported values are `STRING`, `NUMBER`, `INTEGER`, and `BOOLEAN`. When using a `STRING` type parameter, you do not need to add quotation marks (`'` or `"`). For example, `foo` is valid for the `STRING` type and is processed as `"foo"`, whereas `"foo"` is processed as `"\"foo\""`.
- **Default Value**: specifies the default value of the parameter.

    - Make sure that the value can be converted to the type of parameter. Otherwise, the endpoint returns an error.
    - If you do not set a test value for a parameter, the default value is used when testing the endpoint.

In the **Test Values** section, you can view and set test parameters. These values are used as the parameter values when you test the endpoint. Make sure that the value can be converted to the type of parameter. Otherwise, the endpoint returns an error.

### Manage versions

On the right pane of the endpoint details page, you can click the **Deployments** tab to view and manage the deployed versions of the endpoint.

In the **Deployments** tab, you can deploy a draft version and undeploy the online version.

### Rename

To rename an endpoint, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its endpoints.
3. Locate the endpoint you want to rename, click **...** > **Rename**., and enter a new name for the endpoint.

## Test an endpoint

To test an endpoint, perform the following steps:

> **Tip:**
>
> If you have imported your Data App to Postman, you can also test endpoints of the Data App in Postman. For more information, see [Run Data App in Postman](/tidb-cloud/data-service-postman-integration.md).

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its endpoints.
3. Click the name of the endpoint you want to test to view its details.
4. (Optional) If the endpoint contains parameters, you need to set test values before testing.

    1. On the right pane of the endpoint details page, click the **Params** tab.
    2. Expand the **Test Values** section and set test values for the parameters.

        If you do not set a test value for a parameter, the default value is used.

5. Click **Test** in the upper-right corner.

    > **Tip:**
    >
    > Alternatively, you can also press <kbd>F5</kbd> to test the endpoint.

After testing the endpoint, you can see the response as JSON at the bottom of the page. For more information about the JSON response, refer to [Response of an endpoint](#response).

## Deploy an endpoint

> **Note:**
>
> If you have connected your Data App to GitHub with **Auto Sync & Deployment** enabled, any Data App changes you made in GitHub will be deployed in TiDB Cloud Data Service automatically. For more information, see [Deploy automatically with GitHub](/tidb-cloud/data-service-manage-github-connection.md).

To deploy an endpoint, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its endpoints.
3. Locate the endpoint you want to deploy, click the endpoint name to view its details, and then click **Deploy** in the upper-right corner.
4. If **Review Draft** is enabled for your Data App, a dialog is displayed for you to review the changes you made. You can choose whether to discard the changes based on the review.
5. Click **Deploy** to confirm the deployment. You will get the **Endpoint has been deployed** prompt if the endpoint is successfully deployed.

    On the right pane of the endpoint details page, you can click the **Deployments** tab to view the deployed history.

## Call an endpoint

To call an endpoint, you can send an HTTPS request to either an undeployed draft version or a deployed online version of the endpoint.

> **Tip:**
>
> If you have imported your Data App to Postman, you can also call endpoints of the Data App in Postman. For more information, see [Run Data App in Postman](/tidb-cloud/data-service-postman-integration.md).

### Prerequisites

Before calling an endpoint, you need to create an API key. For more information, refer to [Create an API key](/tidb-cloud/data-service-api-key.md#create-an-api-key).

### Request

TiDB Cloud Data Service generates code examples to help you call an endpoint. To get the code example, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its endpoints.
3. Locate the endpoint you want to call and click **...** > **Code Example**. The **Code Example** dialog box is displayed.

    > **Tip:**
    >
    > Alternatively, you can also click the endpoint name to view its details and click **...** > **Code Example** in the upper-right corner.

4. In the dialog box, select the environment and authentication method that you want to use to call the endpoint, and then copy the code example.

    > **Note:**
    >
    > - The code examples are generated based on the properties and parameters of the endpoint.
    > - Currently, TiDB Cloud Data Service only provides the curl code example.

    - Environment: choose **Test Environment** or **Online Environment** depending on your need. **Online Environment** is available only after you deploy the endpoint.
    - Authentication method: choose **Basic Authentication** or **Digest Authentication**.
        - **Basic Authentication** transmits your API key as based64 encoded text.
        - **Digest Authentication** transmits your API key in an encrypted form, which is more secure.

      Compared with **Basic Authentication**, the curl code of **Digest Authentication** includes an additional `--digest` option.

    Here is an example of a curl code snippet for a `POST` request that enables **Batch Operation** and uses **Digest Authentication**:

    <SimpleTab>
    <div label="Test Environment">

    To call a draft version of the endpoint, you need to add the `endpoint-type: draft` header:

    ```bash
    curl --digest --user '<Public Key>:<Private Key>' \
      --request POST 'https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/<Endpoint Path>' \
      --header 'content-type: application/json'\
      --header 'endpoint-type: draft'
      --data-raw '[{
        "age": "${age}",
        "career": "${career}"
    }]'
    ```

    </div>

    <div label="Online Environment">

    You must deploy your endpoint first before checking the code example in the online environment.

    To call the current online version of the endpoint, use the following command:

    ```bash
    curl --digest --user '<Public Key>:<Private Key>' \
      --request POST 'https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/<Endpoint Path>'
      --header 'content-type: application/json'\
      --data-raw '[{
        "age": "${age}",
        "career": "${career}"
    }]'
    ```

    </div>
    </SimpleTab>

    > **Note:**
    >
    > - By requesting the regional domain `<region>.data.tidbcloud.com`, you can directly access the endpoint in the region where the TiDB cluster is located.
    > - Alternatively, you can also request the global domain `data.tidbcloud.com` without specifying a region. In this way, TiDB Cloud Data Service will internally redirect the request to the target region, but this might result in additional latency. If you choose this way, make sure to add the `--location-trusted` option to your curl command when calling an endpoint.

5. Paste the code example in your application, edit the example according to your need, and then run it.

    - You need to replace the `<Public Key>` and `<Private Key>` placeholders with your API key. For more information, refer to [Manage an API key](/tidb-cloud/data-service-api-key.md).
    - If the request method of your endpoint is `GET` and **Pagination** is enabled for the endpoint, you can paginate the results by updating the values of `page=<Page Number>` and `page_size=<Page Size>` with your desired values. For example, to get the second page with 10 items per page, use `page=2` and `page_size=10`.
    - If the request method of your endpoint is `POST` or `PUT`, fill in the `--data-raw` option according to the rows of data that you want to operate on.

        - For endpoints with **Batch Operation** enabled, the `--data-raw` option accepts an array of data objects so you can operate on multiple rows of data using one endpoint.
        - For endpoints with **Batch Operation** not enabled, the `--data-raw` option only accepts one data object.

    - If the request method of your endpoint is `DELETE` and **Batch Operation** is enabled for the endpoint, you can use comma (`,`) to separate multiple rows to be deleted in your curl command, such as `/endpoint/<Endpoint Path>?id=${id1},${id2},${id3}`.
    - If the endpoint contains parameters, specify the parameter values when calling the endpoint.

### Response

After calling an endpoint, you can see the response in JSON format. For more information, see [Response and Status Codes of Data Service](/tidb-cloud/data-service-response-and-status-code.md).

## Undeploy an endpoint

> **Note:**
>
> If you have [connected your Data App to GitHub](/tidb-cloud/data-service-manage-github-connection.md) with **Auto Sync & Deployment** enabled, undeploying an endpoint of this Data App will also delete the configuration of this endpoint on GitHub.

To undeploy an endpoint, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its endpoints.
3. Locate the endpoint you want to undeploy, click **...** > **Undeploy**.
4. Click **Undeploy** to confirm the undeployment.

## Delete an endpoint

> **Note:**
>
> Before you delete an endpoint, make sure that the endpoint is not online. Otherwise, the endpoint cannot be deleted. To undeploy an endpoint, refer to [Undeploy an endpoint](#undeploy-an-endpoint).

To delete an endpoint, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its endpoints.
3. Click the name of the endpoint you want to delete, and then click **...** > **Delete** in the upper-right corner.
4. Click **Delete** to confirm the deletion.