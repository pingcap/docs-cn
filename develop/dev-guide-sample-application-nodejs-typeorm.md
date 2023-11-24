---
title: Connect to TiDB with TypeORM
summary: Learn how to connect to TiDB using TypeORM. This tutorial gives Node.js sample code snippets that work with TiDB using TypeORM.
---

# Connect to TiDB with TypeORM

TiDB is a MySQL-compatible database, and [TypeORM](https://github.com/TypeORM/TypeORM) is a popular open-source ORM framework for Node.js.

In this tutorial, you can learn how to use TiDB and TypeORM to accomplish the following tasks:

- Set up your environment.
- Connect to your TiDB cluster using TypeORM.
- Build and run your application. Optionally, you can find [sample code snippets](#sample-code-snippets) for basic CRUD operations.

> **Note**
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
git clone https://github.com/tidb-samples/tidb-nodejs-typeorm-quickstart.git
cd tidb-nodejs-typeorm-quickstart
```

### Step 2: Install dependencies

Run the following command to install the required packages (including `typeorm` and `mysql2`) for the sample app:

```shell
npm install
```

<details>
<summary><b>Install dependencies to an existing project</b></summary>

For your existing project, run the following command to install the packages:

- `typeorm`: the ORM framework for Node.js.
- `mysql2`: the MySQL driver for Node.js. You can also use the `mysql` driver.
- `dotenv`: loads environment variables from the `.env` file.
- `typescript`: compiles TypeScript code to JavaScript.
- `ts-node`: runs TypeScript code directly without compiling.
- `@types/node`: provides TypeScript type definitions for Node.js.

```shell
npm install typeorm mysql2 dotenv --save
npm install @types/node ts-node typescript --save-dev
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
    > For TiDB Serverless, you **MUST** enable TLS connection via `TIDB_ENABLE_SSL` when using public endpoint.

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
    > For TiDB Dedicated, it is **RECOMMENDED** to enable TLS connection via `TIDB_ENABLE_SSL` when using public endpoint. When you set up `TIDB_ENABLE_SSL=true`, you **MUST** specify the path of the CA certificate downloaded from connection dialog via `TIDB_CA_PATH=/path/to/ca.pem`.

6. Save the `.env` file.

</div>
<div label="TiDB Self-Hosted">

1. Run the following command to copy `.env.example` and rename it to `.env`:

    ```shell
    cp .env.example .env
    ```

2. Edit the `.env` file, set up the environment variables as follows, replace the corresponding placeholders `{}` with connection parameters of your TiDB cluster:

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

### Step 4: Initialize the database schema

Run the following command to invoke TypeORM CLI to initialize the database with the SQL statements written in the migration files in the `src/migrations` folder:

```shell
npm run migration:run
```

<details>
<summary><b>Expected execution output</b></summary>

The following SQL statements create a `players` table and a `profiles` table, and the two tables are associated through foreign keys.

```sql
query: SELECT VERSION() AS `version`
query: SELECT * FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA` = 'test' AND `TABLE_NAME` = 'migrations'
query: CREATE TABLE `migrations` (`id` int NOT NULL AUTO_INCREMENT, `timestamp` bigint NOT NULL, `name` varchar(255) NOT NULL, PRIMARY KEY (`id`)) ENGINE=InnoDB
query: SELECT * FROM `test`.`migrations` `migrations` ORDER BY `id` DESC
0 migrations are already loaded in the database.
1 migrations were found in the source code.
1 migrations are new migrations must be executed.
query: START TRANSACTION
query: CREATE TABLE `profiles` (`player_id` int NOT NULL, `biography` text NOT NULL, PRIMARY KEY (`player_id`)) ENGINE=InnoDB
query: CREATE TABLE `players` (`id` int NOT NULL AUTO_INCREMENT, `name` varchar(50) NOT NULL, `coins` decimal NOT NULL, `goods` int NOT NULL, `created_at` datetime NOT NULL, `profilePlayerId` int NULL, UNIQUE INDEX `uk_players_on_name` (`name`), UNIQUE INDEX `REL_b9666644b90ccc5065993425ef` (`profilePlayerId`), PRIMARY KEY (`id`)) ENGINE=InnoDB
query: ALTER TABLE `players` ADD CONSTRAINT `fk_profiles_on_player_id` FOREIGN KEY (`profilePlayerId`) REFERENCES `profiles`(`player_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
query: INSERT INTO `test`.`migrations`(`timestamp`, `name`) VALUES (?, ?) -- PARAMETERS: [1693814724825,"Init1693814724825"]
Migration Init1693814724825 has been  executed successfully.
query: COMMIT
```

</details>

Migration files are generated from the entities defined in the `src/entities` folder. To learn how to define entities in TypeORM, refer to [TypeORM: Entities](https://typeorm.io/entities).

### Step 5: Run the code and check the result

Run the following command to execute the sample code:

```shell
npm start
```

**Expected execution output:**

If the connection is successful, the terminal will output the version of the TiDB cluster as follows:

```
🔌 Connected to TiDB cluster! (TiDB version: 8.0.11-TiDB-v7.4.0)
🆕 Created a new player with ID 2.
ℹ️ Got Player 2: Player { id: 2, coins: 100, goods: 100 }
🔢 Added 50 coins and 50 goods to player 2, now player 2 has 100 coins and 150 goods.
🚮 Deleted 1 player data.
```

## Sample code snippets

You can refer to the following sample code snippets to complete your own application development.

For complete sample code and how to run it, check out the [tidb-samples/tidb-nodejs-typeorm-quickstart](https://github.com/tidb-samples/tidb-nodejs-typeorm-quickstart) repository.

### Connect with connection options

The following code establishes a connection to TiDB with options defined in the environment variables:

```typescript
// src/dataSource.ts

// Load environment variables from .env file to process.env.
require('dotenv').config();

export const AppDataSource = new DataSource({
  type: "mysql",
  host: process.env.TIDB_HOST || '127.0.0.1',
  port: process.env.TIDB_PORT ? Number(process.env.TIDB_PORT) : 4000,
  username: process.env.TIDB_USER || 'root',
  password: process.env.TIDB_PASSWORD || '',
  database: process.env.TIDB_DATABASE || 'test',
  ssl: process.env.TIDB_ENABLE_SSL === 'true' ? {
    minVersion: 'TLSv1.2',
    ca: process.env.TIDB_CA_PATH ? fs.readFileSync(process.env.TIDB_CA_PATH) : undefined
  } : null,
  synchronize: process.env.NODE_ENV === 'development',
  logging: false,
  entities: [Player, Profile],
  migrations: [__dirname + "/migrations/**/*{.ts,.js}"],
});
```

> **Note**
>
> For TiDB Serverless, you MUST enable TLS connection when using public endpoint. In this sample code, please set up the environment variable `TIDB_ENABLE_SSL` in the `.env` file to `true`.
>
> However, you **don't** have to specify an SSL CA certificate via `TIDB_CA_PATH`, because Node.js uses the built-in [Mozilla CA certificate](https://wiki.mozilla.org/CA/Included_Certificates) by default, which is trusted by TiDB Serverless.

### Insert data

The following query creates a single `Player` record, and returns the created `Player` object, which contains the `id` field generated by TiDB:

```typescript
const player = new Player('Alice', 100, 100);
await this.dataSource.manager.save(player);
```

For more information, refer to [Insert data](/develop/dev-guide-insert-data.md).

### Query data

The following query returns a single `Player` object with ID 101 or `null` if no record is found:

```typescript
const player: Player | null = await this.dataSource.manager.findOneBy(Player, {
  id: id
});
```

For more information, refer to [Query data](/develop/dev-guide-get-data-from-single-table.md).

### Update data

The following query adds `50` goods to the `Player` with ID `101`:

```typescript
const player = await this.dataSource.manager.findOneBy(Player, {
  id: 101
});
player.goods += 50;
await this.dataSource.manager.save(player);
```

For more information, refer to [Update data](/develop/dev-guide-update-data.md).

### Delete data

The following query deletes the `Player` with ID `101`:

```typescript
await this.dataSource.manager.delete(Player, {
  id: 101
});
```

For more information, refer to [Delete data](/develop/dev-guide-delete-data.md).

### Execute raw SQL queries

The following query executes a raw SQL statement (`SELECT VERSION() AS tidb_version;`) and returns the version of the TiDB cluster:

```typescript
const rows = await dataSource.query('SELECT VERSION() AS tidb_version;');
console.log(rows[0]['tidb_version']);
```

For more information, refer to [TypeORM: DataSource API](https://typeorm.io/data-source-api).

## Useful notes

### Foreign key constraints

Using [foreign key constraints](https://docs.pingcap.com/tidb/stable/foreign-key) (experimental) ensures the [referential integrity](https://en.wikipedia.org/wiki/Referential_integrity) of data by adding checks on the database side. However, this might lead to serious performance issues in scenarios with large data volumes.

You can control whether foreign key constraints are created when constructing relationships between entities by using the `createForeignKeyConstraints` option (default value is `true`).

```typescript
@Entity()
export class ActionLog {
    @PrimaryColumn()
    id: number

    @ManyToOne((type) => Person, {
        createForeignKeyConstraints: false,
    })
    person: Person
}
```

For more information, refer to the [TypeORM FAQ](https://typeorm.io/relations-faq#avoid-foreign-key-constraint-creation) and [Foreign key constraints](https://docs.pingcap.com/tidbcloud/foreign-key#foreign-key-constraints).

## Next steps

- Learn more usage of TypeORM from the [documentation of TypeORM](https://typeorm.io/).
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](/develop/dev-guide-overview.md), such as: [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Query data](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

<CustomContent platform="tidb">

Ask questions on the [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc), or [create a support ticket](/support.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

Ask questions on the [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc), or [create a support ticket](https://support.pingcap.com/).

</CustomContent>
