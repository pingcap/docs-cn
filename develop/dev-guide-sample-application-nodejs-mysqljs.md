---
title: Connect to TiDB with mysql.js
summary: Learn how to connect to TiDB using mysql.js. This tutorial gives Node.js sample code snippets that work with TiDB using mysql.js.
---

# Connect to TiDB with mysql.js

TiDB is a MySQL-compatible database, and [mysql.js](https://github.com/mysqljs/mysql) driver is a pure Node.js JavaScript client implementing the MySQL protocol.

In this tutorial, you can learn how to use TiDB and mysql.js driver to accomplish the following tasks:

- Set up your environment.
- Connect to your TiDB cluster using mysql.js driver.
- Build and run your application. Optionally, you can find [sample code snippets](#sample-code-snippets) for basic CRUD operations.

> **Note:**
>
> This tutorial works with TiDB Serverless, TiDB Dedicated, and TiDB Self-Hosted.

## Prerequisites

To complete this tutorial, you need:

- [Node.js](https://nodejs.org/en) >= 16.x installed on your machine.
- [Git](https://git-scm.com/downloads) installed on your machine.
- A TiDB cluster running.

**If you don't have a TiDB cluster, you can create one as follows:**

<CustomContent platform="tidb">

- (Recommended) Follow [Creating a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Follow [Deploy a local test TiDB cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](/production-deployment-using-tiup.md) to create a local cluster.

</CustomContent>
<CustomContent platform="tidb-cloud">

- (Recommended) Follow [Creating a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Follow [Deploy a local test TiDB cluster](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) to create a local cluster.

</CustomContent>

## Run the sample app to connect to TiDB

This section demonstrates how to run the sample application code and connect to TiDB.

### Step 1: Clone the sample app repository

Run the following commands in your terminal window to clone the sample code repository:

```shell
git clone https://github.com/tidb-samples/tidb-nodejs-mysqljs-quickstart.git
cd tidb-nodejs-mysqljs-quickstart
```

### Step 2: Install dependencies

Run the following command to install the required packages (including `mysql` and `dotenv`) for the sample app:

```shell
npm install
```

<details>
<summary><b>Install dependencies to existing project</b></summary>

For your existing project, run the following command to install the packages:

```shell
npm install mysql dotenv --save
```

</details>

### Step 3: Configure connection information

Connect to your TiDB cluster depending on the TiDB deployment option you've selected.

<SimpleTab>
<div label="TiDB Serverless">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

    - **Endpoint Type** is set to `Public`.
    - **Connect With** is set to `General`.
    - **Operating System** matches the operating system where you run the application.

4. If you have not set a password yet, click **Create password** to generate a random password.

5. Run the following command to copy `.env.example` and rename it to `.env`:

    ```shell
    cp .env.example .env
    ```

6. Edit the `.env` file, set up the environment variables as follows, replace the corresponding placeholders `{}` with connection parameters on the connection dialog:

    ```dotenv
    TIDB_HOST={host}
    TIDB_PORT=4000
    TIDB_USER={user}
    TIDB_PASSWORD={password}
    TIDB_DATABASE=test
    TIDB_ENABLE_SSL=true
    ```

    > **Note**
    >
    > For TiDB Serverless, TLS connection **MUST** be enabled via `TIDB_ENABLE_SSL` when using public endpoint.

7. Save the `.env` file.

</div>
<div label="TiDB Dedicated">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Click **Allow Access from Anywhere** and then click **Download TiDB cluster CA** to download the CA certificate.

    For more details about how to obtain the connection string, refer to [TiDB Dedicated standard connection](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection).

4. Run the following command to copy `.env.example` and rename it to `.env`:

    ```shell
    cp .env.example .env
    ```

5. Edit the `.env` file, set up the environment variables as follows, replace the corresponding placeholders `{}` with connection parameters on the connection dialog:

    ```dotenv
    TIDB_HOST={host}
    TIDB_PORT=4000
    TIDB_USER={user}
    TIDB_PASSWORD={password}
    TIDB_DATABASE=test
    TIDB_ENABLE_SSL=true
    TIDB_CA_PATH={downloaded_ssl_ca_path}
    ```

    > **Note**
    >
    > It is recommended to enable TLS connection when using the public endpoint to connect to TiDB Dedicated.
    >
    > To enable TLS connection, modify `TIDB_ENABLE_SSL` to `true` and using `TIDB_CA_PATH` to specify the file path of CA certificate downloaded from the connection dialog.

6. Save the `.env` file.

</div>
<div label="TiDB Self-Hosted">

1. Run the following command to copy `.env.example` and rename it to `.env`:

    ```shell
    cp .env.example .env
    ```

2. Edit the `.env` file, replace the corresponding placeholders `{}` with connection parameters of your cluster. The example configuration is as follows:

    ```dotenv
    TIDB_HOST={host}
    TIDB_PORT=4000
    TIDB_USER=root
    TIDB_PASSWORD={password}
    TIDB_DATABASE=test
    ```

    If you are running TiDB locally, the default host address is `127.0.0.1`, and the password is empty.

3. Save the `.env` file.

</div>
</SimpleTab>

### Step 4: Run the code and check the result

Run the following command to execute the sample code:

```shell
npm start
```

If the connection is successful, the console will output the version of the TiDB cluster as follows:

```
🔌 Connected to TiDB cluster! (TiDB version: 8.0.11-TiDB-v7.4.0)
⏳ Loading sample game data...
✅ Loaded sample game data.

🆕 Created a new player with ID 12.
ℹ️ Got Player 12: Player { id: 12, coins: 100, goods: 100 }
🔢 Added 50 coins and 50 goods to player 12, updated 1 row.
🚮 Deleted 1 player data.
```

## Sample code snippets

You can refer to the following sample code snippets to complete your own application development.

For complete sample code and how to run it, check out the [tidb-samples/tidb-nodejs-mysqljs-quickstart](https://github.com/tidb-samples/tidb-nodejs-mysqljs-quickstart) repository.

### Connect with connection options

The following code establishes a connection to TiDB with options defined in the environment variables:

```javascript
// Step 1. Import the 'mysql' and 'dotenv' packages.
import { createConnection } from "mysql";
import dotenv from "dotenv";
import * as fs from "fs";

// Step 2. Load environment variables from .env file to process.env.
dotenv.config();

// Step 3. Create a connection to the TiDB cluster.
const options = {
    host: process.env.TIDB_HOST || '127.0.0.1',
    port: process.env.TIDB_PORT || 4000,
    user: process.env.TIDB_USER || 'root',
    password: process.env.TIDB_PASSWORD || '',
    database: process.env.TIDB_DATABASE || 'test',
    ssl: process.env.TIDB_ENABLE_SSL === 'true' ? {
        minVersion: 'TLSv1.2',
        ca: process.env.TIDB_CA_PATH ? fs.readFileSync(process.env.TIDB_CA_PATH) : undefined
    } : null,
}
const conn = createConnection(options);

// Step 4. Perform some SQL operations...

// Step 5. Close the connection.
conn.end();
```

> **Note**
>
> For TiDB Serverless, you **MUST** enable TLS connection via `TIDB_ENABLE_SSL` when using public endpoint. However, you **don't** have to specify an SSL CA certificate via `TIDB_CA_PATH`, because Node.js uses the built-in [Mozilla CA certificate](https://wiki.mozilla.org/CA/Included_Certificates) by default, which is trusted by TiDB Serverless.

### Insert data

The following query creates a single `Player` record and returns the ID of the newly created record:

```javascript
conn.query('INSERT INTO players (coins, goods) VALUES (?, ?);', [100, 100], (err, ok) => {
   if (err) {
       console.error(err);
   } else {
       console.log(ok.insertId);
   }
});
```

For more information, refer to [Insert data](/develop/dev-guide-insert-data.md).

### Query data

The following query returns a single `Player` record by ID `1`:

```javascript
conn.query('SELECT id, coins, goods FROM players WHERE id = ?;', [1], (err, rows) => {
   if (err) {
      console.error(err);
   } else {
      console.log(rows[0]);
   }
});
```

For more information, refer to [Query data](/develop/dev-guide-get-data-from-single-table.md).

### Update data

The following query adds `50` coins and `50` goods to the `Player` with ID `1`:

```javascript
conn.query(
   'UPDATE players SET coins = coins + ?, goods = goods + ? WHERE id = ?;',
   [50, 50, 1],
   (err, ok) => {
      if (err) {
         console.error(err);
      } else {
          console.log(ok.affectedRows);
      }
   }
);
```

For more information, refer to [Update data](/develop/dev-guide-update-data.md).

### Delete data

The following query deletes the `Player` record with ID `1`:

```javascript
conn.query('DELETE FROM players WHERE id = ?;', [1], (err, ok) => {
    if (err) {
        reject(err);
    } else {
        resolve(ok.affectedRows);
    }
});
```

For more information, refer to [Delete data](/develop/dev-guide-delete-data.md).

## Useful notes

- Using [connection pools](https://github.com/mysqljs/mysql#pooling-connections) to manage database connections can reduce the performance overhead caused by frequently establishing and destroying connections.
- To avoid SQL injection attacks, it is recommended to use [Escaping query values](https://github.com/mysqljs/mysql#escaping-query-values) before executing SQL.

    > **Note**
    >
    > The `mysqljs/mysql` package does not yet support prepared statements, it only escapes values on the client side (related issue: [mysqljs/mysql#274](https://github.com/mysqljs/mysql/issues/274)).
    >
    > If you want to use this feature to avoid SQL injection or improve efficiency of batch insert/update, it is recommended to use [mysql2](https://github.com/sidorares/node-mysql2) package instead.

- Using ORM frameworks to improve development efficiency in scenarios without a number of complex SQL statements, such as: [Sequelize](https://sequelize.org/), [TypeORM](https://typeorm.io/), and [Prisma](/develop/dev-guide-sample-application-nodejs-prisma.md).
- It is recommended to enable the `supportBigNumbers: true` option when dealing with big numbers (`BIGINT` and `DECIMAL` columns) in the database.

## Next steps

- Learn more usage of mysql.js driver from [the documentation of mysql.js](https://github.com/mysqljs/mysql#readme).
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](/develop/dev-guide-overview.md), such as: [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Query data](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

Ask questions on the [Discord](https://discord.gg/vYU9h56kAX), or [create a support ticket](https://support.pingcap.com/).
