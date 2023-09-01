---
title: Connect to TiDB with mysql2 in AWS Lambda Function
summary: This article describes how to build a CRUD application using TiDB and mysql2 in AWS Lambda Function and provides a simple example code snippet.
---

# Connect to TiDB with mysql2 in AWS Lambda Function

TiDB is a MySQL-compatible database, [AWS Lambda Function](https://aws.amazon.com/lambda/) is a compute service, and [mysql2](https://github.com/sidorares/node-mysql2) is a popular open-source driver for Node.js.

In this tutorial, you can learn how to use TiDB and mysql2 in AWS Lambda Function to accomplish the following tasks:

- Set up your environment.
- Connect to your TiDB cluster using mysql2.
- Build and run your application. Optionally, you can find [sample code snippets](#sample-code-snippets) for basic CRUD operations.
- Deploy your AWS Lambda Function.

> **Note**
>
> This tutorial works with TiDB Serverless and TiDB Self-Hosted.

## Prerequisites

To complete this tutorial, you need:

- [Node.js **18**](https://nodejs.org/en/download/) or later.
- [Git](https://git-scm.com/downloads).
- A TiDB cluster.
- An [AWS user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html) with administrator permissions.
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

<CustomContent platform="tidb">

**If you don't have a TiDB cluster, you can create one as follows:**

- (Recommended) Follow [Creating a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Follow [Deploy a local test TiDB cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](/production-deployment-using-tiup.md) to create a local cluster.

</CustomContent>
<CustomContent platform="tidb-cloud">

**If you don't have a TiDB cluster, you can create one as follows:**

- (Recommended) Follow [Creating a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Follow [Deploy a local test TiDB cluster](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) to create a local cluster.

</CustomContent>

If you don't have an AWS account or a user, you can create them by following the steps in the [Getting Started with Lambda](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html) guide.

## Run the sample app to connect to TiDB

This section demonstrates how to run the sample application code and connect to TiDB.

> **Note**
>
> For complete code snippets and running instructions, refer to the [tidb-samples/tidb-aws-lambda-quickstart](https://github.com/tidb-samples/tidb-aws-lambda-quickstart) GitHub repository.

### Step 1: Clone the sample app repository

Run the following commands in your terminal window to clone the sample code repository:

```bash
git clone git@github.com:tidb-samples/tidb-aws-lambda-quickstart.git
cd tidb-aws-lambda-quickstart
```

### Step 2: Install dependencies

Run the following command to install the required packages (including `mysql2`) for the sample app:

```bash
npm install
```

### Step 3: Configure connection information

Connect to your TiDB cluster depending on the TiDB deployment option you've selected.

<SimpleTab>

<div label="TiDB Serverless">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

    - **Endpoint Type** is set to `Public`
    - **Connect With** is set to `General`
    - **Operating System** matches your environment.

    > **Note**
    >
    > In Node.js applications, you don't have to provide an SSL CA certificate, because Node.js uses the built-in [Mozilla CA certificate](https://wiki.mozilla.org/CA/Included_Certificates) by default when establishing the TLS (SSL) connection.

4. Click **Create password** to create a random password.

    > **Tip**
    >
    > If you have generated a password before, you can either use the original password or click **Reset password** to generate a new one.

5. Copy and paste the corresponding connection string into `env.json`. The following is an example:

    ```json
    {
      "Parameters": {
        "TIDB_HOST": "{gateway-region}.aws.tidbcloud.com",
        "TIDB_PORT": "4000",
        "TIDB_USER": "{prefix}.root",
        "TIDB_PASSWORD": "{password}"
      }
    }
    ```

    Replace the placeholders in `{}` with the values obtained in the connection dialog.

</div>

<div label="TiDB Self-Hosted">

Copy and paste the corresponding connection string into `env.json`. The following is an example:

```json
{
  "Parameters": {
    "TIDB_HOST": "{tidb_server_host}",
    "TIDB_PORT": "4000",
    "TIDB_USER": "root",
    "TIDB_PASSWORD": "{password}"
  }
}
```

Replace the placeholders in `{}` with the values obtained in the **Connect** window.

</div>

</SimpleTab>

### Step 4: Run the code and check the result

1. (Prerequisite) Install the [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html).

2. Build the bundle:

    ```bash
    npm run build
    ```

3. Invoke the sample Lambda function:

    ```bash
    sam local invoke --env-vars env.json -e events/event.json "tidbHelloWorldFunction"
    ```

4. Check the output in the terminal. If the output is similar to the following, the connection is successful:

    ```bash
    {"statusCode":200,"body":"{\"results\":[{\"Hello World\":\"Hello World\"}]}"}
    ```

After you confirm that the connection is successful, you can follow the [next section](#deploy-the-aws-lambda-function) to deploy the AWS Lambda Function.

## Deploy the AWS Lambda Function

You can deploy the AWS Lambda Function using either the [SAM CLI](#sam-cli-deployment-recommended) or the [AWS Lambda console](#web-console-deployment).

### SAM CLI deployment (Recommended)

1. ([Prerequisite](#prerequisites)) Install the [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html).

2. Build the bundle:

    ```bash
    npm run build
    ```

3. Update the environment variables in [`template.yml`](https://github.com/tidb-samples/tidb-aws-lambda-quickstart/blob/main/template.yml):

    ```yaml
    Environment:
      Variables:
        TIDB_HOST: {tidb_server_host}
        TIDB_PORT: 4000
        TIDB_USER: {prefix}.root
        TIDB_PASSWORD: {password}
    ```

4. Set AWS environment variables (refer to [Short-term credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-authentication-short-term.html)):

    ```bash
    export AWS_ACCESS_KEY_ID={your_access_key_id}
    export AWS_SECRET_ACCESS_KEY={your_secret_access_key}
    export AWS_SESSION_TOKEN={your_session_token}
    ```

5. Deploy the AWS Lambda Function:

    ```bash
    sam deploy --guided

    # Example:

    # Configuring SAM deploy
    # ======================

    #        Looking for config file [samconfig.toml] :  Not found

    #        Setting default arguments for 'sam deploy'
    #        =========================================
    #        Stack Name [sam-app]: tidb-aws-lambda-quickstart
    #        AWS Region [us-east-1]: 
    #        #Shows you resources changes to be deployed and require a 'Y' to initiate deploy
    #        Confirm changes before deploy [y/N]: 
    #        #SAM needs permission to be able to create roles to connect to the resources in your template
    #        Allow SAM CLI IAM role creation [Y/n]: 
    #        #Preserves the state of previously provisioned resources when an operation fails
    #        Disable rollback [y/N]: 
    #        tidbHelloWorldFunction may not have authorization defined, Is this okay? [y/N]: y
    #        tidbHelloWorldFunction may not have authorization defined, Is this okay? [y/N]: y
    #        tidbHelloWorldFunction may not have authorization defined, Is this okay? [y/N]: y
    #        tidbHelloWorldFunction may not have authorization defined, Is this okay? [y/N]: y
    #        Save arguments to configuration file [Y/n]: 
    #        SAM configuration file [samconfig.toml]: 
    #        SAM configuration environment [default]: 

    #        Looking for resources needed for deployment:
    #        Creating the required resources...
    #        Successfully created!
    ```

### Web console deployment

1. Build the bundle:

    ```bash
    npm run build

    # Bundle for AWS Lambda
    # =====================
    # dist/index.zip
    ```

2. Visit the [AWS Lambda console](https://console.aws.amazon.com/lambda/home#/functions).

3. Follow the steps in [Creating a Lambda function](https://docs.aws.amazon.com/lambda/latest/dg/lambda-nodejs.html) to create a Node.js Lambda function.

4. Follow the steps in [Lambda deployment packages](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-package.html#gettingstarted-package-zip) and upload the `dist/index.zip` file.

5. [Copy and configure the corresponding connection string](https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html) in Lambda Function.

    1. In the [Functions](https://console.aws.amazon.com/lambda/home#/functions) page of the Lambda console, select the **Configuration** tab, and then choose **Environment variables**.
    2. Choose **Edit**.
    3. To add your database access credentials, do the following:
        - Choose **Add environment variable**, then for **Key** enter `TIDB_HOST` and for **Value** enter the host name.
        - Choose **Add environment variable**, then for **Key** enter `TIDB_PORT` and for **Value** enter the port (4000 is default).
        - Choose **Add environment variable**, then for **Key** enter `TIDB_USER` and for **Value** enter the user name.
        - Choose **Add environment variable**, then for **Key** enter `TIDB_PASSWORD` and for **Value** enter the password you chose when you created your database.
        - Choose **Save**.

## Sample code snippets

You can refer to the following sample code snippets to complete your own application development.

For complete sample code and how to run it, check out the [tidb-samples/tidb-aws-lambda-quickstart](https://github.com/tidb-samples/tidb-aws-lambda-quickstart) repository.

### Connect to TiDB

The following code establish a connection to TiDB with options defined in the environment variables:

```typescript
// lib/tidb.ts
import mysql from 'mysql2';

let pool: mysql.Pool | null = null;

function connect() {
  return mysql.createPool({
    host: process.env.TIDB_HOST, // TiDB host, for example: {gateway-region}.aws.tidbcloud.com
    port: process.env.TIDB_PORT ? Number(process.env.TIDB_PORT) : 4000, // TiDB port, default: 4000
    user: process.env.TIDB_USER, // TiDB user, for example: {prefix}.root
    password: process.env.TIDB_PASSWORD, // TiDB password
    database: process.env.TIDB_DATABASE || 'test', // TiDB database name, default: test
    ssl: {
      minVersion: 'TLSv1.2',
      rejectUnauthorized: true,
    },
    connectionLimit: 1, // Setting connectionLimit to "1" in a serverless function environment optimizes resource usage, reduces costs, ensures connection stability, and enables seamless scalability.
    maxIdle: 1, // max idle connections, the default value is the same as `connectionLimit`
    enableKeepAlive: true,
  });
}

export function getPool(): mysql.Pool {
  if (!pool) {
    pool = connect();
  }
  return pool;
}
```

### Insert data

The following query creates a single `Player` record and returns a `ResultSetHeader` object:

```typescript
const [rsh] = await pool.query('INSERT INTO players (coins, goods) VALUES (?, ?);', [100, 100]);
console.log(rsh.insertId);
```

For more information, refer to [Insert data](/develop/dev-guide-insert-data.md).

### Query data

The following query returns a single `Player` record by ID `1`:

```typescript
const [rows] = await pool.query('SELECT id, coins, goods FROM players WHERE id = ?;', [1]);
console.log(rows[0]);
```

For more information, refer to [Query data](/develop/dev-guide-get-data-from-single-table.md).

### Update data

The following query adds `50` coins and `50` goods to the `Player` with ID `1`:

```typescript
const [rsh] = await pool.query(
    'UPDATE players SET coins = coins + ?, goods = goods + ? WHERE id = ?;',
    [50, 50, 1]
);
console.log(rsh.affectedRows);
```

For more information, refer to [Update data](/develop/dev-guide-update-data.md).

### Delete data

The following query deletes the `Player` record with ID `1`:

```typescript
const [rsh] = await pool.query('DELETE FROM players WHERE id = ?;', [1]);
console.log(rsh.affectedRows);
```

For more information, refer to [Delete data](/develop/dev-guide-delete-data.md).

## Useful notes

- Using [connection pools](https://github.com/sidorares/node-mysql2#using-connection-pools) to manage database connections can reduce the performance overhead caused by frequently establishing and destroying connections.
- To avoid SQL injection, it is recommended to use [prepared statements](https://github.com/sidorares/node-mysql2#using-prepared-statements).
- In scenarios where there are not many complex SQL statements involved, using ORM frameworks like [Sequelize](https://sequelize.org/), [TypeORM](https://typeorm.io/), or [Prisma](https://www.prisma.io/) can greatly improve development efficiency. 
- For building a RESTful API for your application, it is recommended to [use AWS Lambda with API Gateway](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html).
- For designing high-performance applications using TiDB Serverless and AWS Lambda, refer to [this blog](https://aws.amazon.com/blogs/apn/designing-high-performance-applications-using-serverless-tidb-cloud-and-aws-lambda/).

## Next steps

- For more details on how to use TiDB in AWS Lambda Function, see our [TiDB-Lambda-integration/aws-lambda-bookstore Demo](https://github.com/pingcap/TiDB-Lambda-integration/blob/main/aws-lambda-bookstore/README.md). You can also use AWS API Gateway to build a RESTful API for your application.
- Learn more usage of `mysql2` from [the documentation of `mysql2`](https://github.com/sidorares/node-mysql2/tree/master/documentation/en).
- Learn more usage of AWS Lambda from [the AWS developer guide of `Lambda`](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html).
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](/develop/dev-guide-overview.md), such as [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Single table reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

Ask questions on the [Discord](https://discord.gg/vYU9h56kAX), or [create a support ticket](https://support.pingcap.com/).
