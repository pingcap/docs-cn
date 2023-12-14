---
title: Connect to TiDB with Sequelize
summary: Learn how to connect to TiDB using Sequelize. This tutorial gives Node.js sample code snippets that work with TiDB using Sequelize.
---

# Connect to TiDB with Sequelize

TiDB is a MySQL-compatible database, and [Sequelize](https://sequelize.org/) is a popular ORM framework for Node.js.

In this tutorial, you can learn how to use TiDB and Sequelize to accomplish the following tasks:

- Set up your environment.
- Connect to your TiDB cluster using Sequelize.
- Build and run your application. Optionally, you can find [sample code snippets](#sample-code-snippets) for basic CRUD operations.

> **Note**
>
> This tutorial works with TiDB Serverless, TiDB Dedicated, and TiDB Self-Hosted.

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
> For complete code snippets and running instructions, refer to the [tidb-samples/tidb-nodejs-sequelize-quickstart](https://github.com/tidb-samples/tidb-nodejs-sequelize-quickstart) GitHub repository.

### Step 1: Clone the sample app repository

Run the following commands in your terminal window to clone the sample code repository:

```bash
git clone git@github.com:tidb-samples/tidb-nodejs-sequelize-quickstart.git
cd tidb-nodejs-sequelize-quickstart
```

### Step 2: Install dependencies

Run the following command to install the required packages (including `sequelize`) for the sample app:

```bash
npm install
```

### Step 3: Configure connection information

Connect to your TiDB cluster depending on the TiDB deployment option you've selected.

<SimpleTab>

<div label="TiDB Serverless">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

    - **Endpoint Type** is set to `Public`
    - **Branch** is set to `main`
    - **Connect With** is set to `General`
    - **Operating System** matches your environment.

    > **Note**
    >
    > In Node.js applications, you don't have to provide an SSL CA certificate, because Node.js uses the built-in [Mozilla CA certificate](https://wiki.mozilla.org/CA/Included_Certificates) by default when establishing the TLS (SSL) connection.

4. Click **Generate Password** to create a random password.

    > **Tip**
    >
    > If you have generated a password before, you can either use the original password or click **Reset Password** to generate a new one.

5. Run the following command to copy `.env.example` and rename it to `.env`:

    ```shell
    cp .env.example .env
    ```

6. Edit the `.env` file, set up the environment variables as follows, replace the corresponding placeholders `{}` with connection parameters on the connection dialog:

    ```dotenv
    TIDB_HOST='{host}'
    TIDB_PORT='4000'
    TIDB_USER='{user}'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    TIDB_ENABLE_SSL='true'
    ```

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

    ```shell
    TIDB_HOST='{host}'
    TIDB_PORT='4000'
    TIDB_USER='{user}'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    TIDB_ENABLE_SSL='true'
    TIDB_CA_PATH='{path/to/ca}'
    ```

6. Save the `.env` file.

</div>

<div label="TiDB Self-Hosted">

1. Run the following command to copy `.env.example` and rename it to `.env`:

    ```shell
    cp .env.example .env
    ```

2. Edit the `.env` file, set up the environment variables as follows, replace the corresponding placeholders `{}` with connection parameters on the connection dialog:

    ```shell
    TIDB_HOST='{host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    If you are running TiDB locally, the default host address is `127.0.0.1`, and the password is empty.

3. Save the `.env` file.

</div>

</SimpleTab>

### Step 4: Run the sample app

Run the following command to execute the sample code:

```shell
npm start
```

<details>
<summary>**Expected output(partial):**</summary>

```shell
INFO (app/10117): Getting sequelize instance...
Executing (default): SELECT 1+1 AS result
Executing (default): DROP TABLE IF EXISTS `players`;
Executing (default): CREATE TABLE IF NOT EXISTS `players` (`id` INTEGER NOT NULL auto_increment  COMMENT 'The unique ID of the player.', `coins` INTEGER NOT NULL COMMENT 'The number of coins that the player had.', `goods` INTEGER NOT NULL COMMENT 'The number of goods that the player had.', `createdAt` DATETIME NOT NULL, `updatedAt` DATETIME NOT NULL, PRIMARY KEY (`id`)) ENGINE=InnoDB;
Executing (default): SHOW INDEX FROM `players`
Executing (default): INSERT INTO `players` (`id`,`coins`,`goods`,`createdAt`,`updatedAt`) VALUES (1,100,100,'2023-08-31 09:10:11','2023-08-31 09:10:11'),(2,200,200,'2023-08-31 09:10:11','2023-08-31 09:10:11'),(3,300,300,'2023-08-31 09:10:11','2023-08-31 09:10:11'),(4,400,400,'2023-08-31 09:10:11','2023-08-31 09:10:11'),(5,500,500,'2023-08-31 09:10:11','2023-08-31 09:10:11');
Executing (default): SELECT `id`, `coins`, `goods`, `createdAt`, `updatedAt` FROM `players` AS `players` WHERE `players`.`coins` > 300;
Executing (default): UPDATE `players` SET `coins`=?,`goods`=?,`updatedAt`=? WHERE `id` = ?
Executing (default): DELETE FROM `players` WHERE `id` = 6
```

</details>

## Sample code snippets

You can refer to the following sample code snippets to complete your own application development.

For complete sample code and how to run it, check out the [tidb-samples/tidb-nodejs-sequelize-quickstart](https://github.com/tidb-samples/tidb-nodejs-sequelize-quickstart) repository.

### Connect to TiDB

The following code establish a connection to TiDB with options defined in the environment variables:

```typescript
// src/lib/tidb.ts
import { Sequelize } from 'sequelize';

export function initSequelize() {
  return new Sequelize({
    dialect: 'mysql',
    host: process.env.TIDB_HOST || 'localhost',     // TiDB host, for example: {gateway-region}.aws.tidbcloud.com
    port: Number(process.env.TIDB_PORT) || 4000,    // TiDB port, default: 4000
    username: process.env.TIDB_USER || 'root',      // TiDB user, for example: {prefix}.root
    password: process.env.TIDB_PASSWORD || 'root',  // TiDB password
    database: process.env.TIDB_DB_NAME || 'test',   // TiDB database name, default: test
    dialectOptions: {
      ssl:
        process.env?.TIDB_ENABLE_SSL === 'true'     // (Optional) Enable SSL
          ? {
              minVersion: 'TLSv1.2',
              rejectUnauthorized: true,
              ca: process.env.TIDB_CA_PATH          // (Optional) Path to the custom CA certificate
                ? readFileSync(process.env.TIDB_CA_PATH)
                : undefined,
            }
          : null,
    },
}

export async function getSequelize() {
  if (!sequelize) {
    sequelize = initSequelize();
    try {
      await sequelize.authenticate();
      logger.info('Connection has been established successfully.');
    } catch (error) {
      logger.error('Unable to connect to the database:');
      logger.error(error);
      throw error;
    }
  }
  return sequelize;
}
```

### Insert data

The following query creates a single `Players` record and returns a `Players` object:

```typescript
logger.info('Creating a new player...');
const newPlayer = await playersModel.create({
  id: 6,
  coins: 600,
  goods: 600,
});
logger.info('Created a new player.');
logger.info(newPlayer.toJSON());
```

For more information, refer to [Insert data](/develop/dev-guide-insert-data.md).

### Query data

The following query returns a single `Players` record those coins are greater than `300`:

```typescript
logger.info('Reading all players with coins > 300...');
const allPlayersWithCoinsGreaterThan300 = await playersModel.findAll({
  where: {
    coins: {
      [Op.gt]: 300,
    },
  },
});
logger.info('Read all players with coins > 300.');
logger.info(allPlayersWithCoinsGreaterThan300.map((p) => p.toJSON()));
```

For more information, refer to [Query data](/develop/dev-guide-get-data-from-single-table.md).

### Update data

The following query set `700` coins and `700` goods to the `Players` with ID `6` that was created in the [Insert data](#insert-data) section:

```typescript
logger.info('Updating the new player...');
await newPlayer.update({ coins: 700, goods: 700 });
logger.info('Updated the new player.');
logger.info(newPlayer.toJSON());
```

For more information, refer to [Update data](/develop/dev-guide-update-data.md).

### Delete data

The following query deletes the `Player` record with ID `6` that was created in the [Insert data](#insert-data) section:

```typescript
logger.info('Deleting the new player...');
await newPlayer.destroy();
const deletedNewPlayer = await playersModel.findByPk(6);
logger.info('Deleted the new player.');
logger.info(deletedNewPlayer?.toJSON());
```

For more information, refer to [Delete data](/develop/dev-guide-delete-data.md).

## Next steps

- Learn more usage of the ORM framework Sequelize driver from [the documentation of Sequelize](https://sequelize.org/).
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](/develop/dev-guide-overview.md), such as [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Single table reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

<CustomContent platform="tidb">

Ask questions on the [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc), or [create a support ticket](/support.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

Ask questions on the [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc), or [create a support ticket](https://support.pingcap.com/).

</CustomContent>
