---
title: Connect to TiDB with mysql2 in Next.js
summary: This article describes how to build a CRUD application using TiDB and mysql2 in Next.js and provides a simple example code snippet.
---

# Connect to TiDB with mysql2 in Next.js

TiDB is a MySQL-compatible database, and [mysql2](https://github.com/sidorares/node-mysql2) is a popular open-source driver for Node.js.

In this tutorial, you can learn how to use TiDB and mysql2 in Next.js to accomplish the following tasks:

- Set up your environment.
- Connect to your TiDB cluster using mysql2.
- Build and run your application. Optionally, you can find [sample code snippets](#sample-code-snippets) for basic CRUD operations.

> **Note**
>
> This tutorial works with TiDB Serverless and TiDB Self-Hosted.

## Prerequisites

To complete this tutorial, you need:

- [Node.js **18**](https://nodejs.org/en/download/) or later.
- [Git](https://git-scm.com/downloads).
- A TiDB cluster. 

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

## Run the sample app to connect to TiDB

This section demonstrates how to run the sample application code and connect to TiDB.

> **Note**
>
> For complete code snippets and running instructions, refer to the [tidb-nextjs-vercel-quickstart](https://github.com/tidb-samples/tidb-nextjs-vercel-quickstart) GitHub repository.

### Step 1: Clone the sample app repository

Run the following commands in your terminal window to clone the sample code repository:

```bash
git clone git@github.com:tidb-samples/tidb-nextjs-vercel-quickstart.git
cd tidb-nextjs-vercel-quickstart
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

1. Navigate to the [**Clusters** page](https://tidbcloud.com/console/clusters), and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

    - **Endpoint Type** is set to `Public`
    - **Connect With** is set to `General`
    - **Operating System** matches your environment.

    > **Note**
    >
    > In Node.js applications, you do not have to provide an SSL CA certificate, because Node.js uses the built-in [Mozilla CA certificate](https://wiki.mozilla.org/CA/Included_Certificates) by default when establishing the TLS (SSL) connection.

4. Click **Create password** to create a random password.

    > **Tip**
    >
    > If you have created a password before, you can either use the original password or click **Reset password** to generate a new one.

5. Run the following command to copy `.env.example` and rename it to `.env`:

    ```bash
    # Linux
    cp .env.example .env
    ```

    ```powershell
    # Windows
    Copy-Item ".env.example" -Destination ".env"
    ```

6. Copy and paste the corresponding connection string into the `.env` file. The example result is as follows:

    ```bash
    TIDB_HOST='{gateway-region}.aws.tidbcloud.com'
    TIDB_PORT='4000'
    TIDB_USER='{prefix}.root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    Replace the placeholders in `{}` with the values obtained in the connection dialog.

7. Save the `.env` file.

</div>

<div label="TiDB Self-Hosted">

1. Run the following command to copy `.env.example` and rename it to `.env`:

    ```bash
    # Linux
    cp .env.example .env
    ```

    ```powershell
    # Windows
    Copy-Item ".env.example" -Destination ".env"
    ```

2. Copy and paste the corresponding connection string into the `.env` file. The example result is as follows:

    ```bash
    TIDB_HOST='{tidb_server_host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    Replace the placeholders in `{}` with the values obtained in the **Connect** window. If you are running TiDB locally, the default host address is `127.0.0.1`, and the password is empty.

3. Save the `.env` file.

</div>

</SimpleTab>

### Step 4: Run the code and check the result

1. Start the application:

   ```bash
   npm run dev
   ```

2. Open your browser and visit `http://localhost:3000`. (Check your terminal for the actual port number, and the default is `3000`.)

3. Click **RUN SQL** to execute the sample code.

4. Check the output in the terminal. If the output is similar to the following, the connection is successful:

   ```json
   {
     "results": [
       {
         "Hello World": "Hello World"
       }
     ]
   }
   ```

## Sample code snippets

You can refer to the following sample code snippets to complete your own application development.

For complete sample code and how to run it, check out the [tidb-nextjs-vercel-quickstart](https://github.com/tidb-samples/tidb-nextjs-vercel-quickstart) repository.

### Connect to TiDB

The following code establish a connection to TiDB with options defined in the environment variables:

```javascript
// src/lib/tidb.js
import mysql from 'mysql2';

let pool = null;

export function connect() {
  return mysql.createPool({
    host: process.env.TIDB_HOST, // TiDB host, for example: {gateway-region}.aws.tidbcloud.com
    port: process.env.TIDB_PORT || 4000, // TiDB port, default: 4000
    user: process.env.TIDB_USER, // TiDB user, for example: {prefix}.root
    password: process.env.TIDB_PASSWORD, // The password of TiDB user.
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

export function getPool() {
  if (!pool) {
    pool = createPool();
  }
  return pool;
}
```

### Insert data

The following query creates a single `Player` record and returns a `ResultSetHeader` object:

```javascript
const [rsh] = await pool.query('INSERT INTO players (coins, goods) VALUES (?, ?);', [100, 100]);
console.log(rsh.insertId);
```

For more information, refer to [Insert data](/develop/dev-guide-insert-data.md).

### Query data

The following query returns a single `Player` record by ID `1`:

```javascript
const [rows] = await pool.query('SELECT id, coins, goods FROM players WHERE id = ?;', [1]);
console.log(rows[0]);
```

For more information, refer to [Query data](/develop/dev-guide-get-data-from-single-table.md).

### Update data

The following query adds `50` coins and `50` goods to the `Player` with ID `1`:

```javascript
const [rsh] = await pool.query(
    'UPDATE players SET coins = coins + ?, goods = goods + ? WHERE id = ?;',
    [50, 50, 1]
);
console.log(rsh.affectedRows);
```

For more information, refer to [Update data](/develop/dev-guide-update-data.md).

### Delete data

The following query deletes the `Player` record with ID `1`:

```javascript
const [rsh] = await pool.query('DELETE FROM players WHERE id = ?;', [1]);
console.log(rsh.affectedRows);
```

For more information, refer to [Delete data](/develop/dev-guide-delete-data.md).

## Useful notes

- Using [connection pools](https://github.com/sidorares/node-mysql2#using-connection-pools) to manage database connections can reduce the performance overhead caused by frequently establishing and destroying connections.
- To avoid SQL injection, it is recommended to use [prepared statements](https://github.com/sidorares/node-mysql2#using-prepared-statements).
- In scenarios where there are not many complex SQL statements involved, using ORM frameworks like [Sequelize](https://sequelize.org/), [TypeORM](https://typeorm.io/), or [Prisma](https://www.prisma.io/) can greatly improve development efficiency.

## Next steps

- For more details on how to build a complex application with ORM and Next.js, see [our Bookshop Demo](https://github.com/pingcap/tidb-prisma-vercel-demo).
- Learn more usage of node-mysql2 driver from [the documentation of node-mysql2](https://github.com/sidorares/node-mysql2/tree/master/documentation/en).
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](/develop/dev-guide-overview.md), such as [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Single table reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

Ask questions on the [Discord](https://discord.gg/vYU9h56kAX), or [create a support ticket](https://support.pingcap.com/).
