---
title: Connect to TiDB with Prisma
summary: Learn how to connect to TiDB using Prisma. This tutorial gives Node.js sample code snippets that work with TiDB using Prisma.
---

# Connect to TiDB with Prisma

TiDB is a MySQL-compatible database, and [Prisma](https://github.com/prisma/prisma) is a popular open-source ORM framework for Node.js.

In this tutorial, you can learn how to use TiDB and Prisma to accomplish the following tasks:

- Set up your environment.
- Connect to your TiDB cluster using Prisma.
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
git clone https://github.com/tidb-samples/tidb-nodejs-prisma-quickstart.git
cd tidb-nodejs-prisma-quickstart
```

### Step 2: Install dependencies

Run the following command to install the required packages (including `prisma`) for the sample app:

```shell
npm install
```

<details>
<summary><b>Install dependencies to existing project</b></summary>

For your existing project, run the following command to install the packages:

```shell
npm install prisma typescript ts-node @types/node --save-dev
```

</details>

### Step 3: Provide connection Parameters

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

6. Edit the `.env` file, set up the environment variable `DATABASE_URL` as follows, replace the corresponding placeholders `{}` with connection parameters on the connection dialog:

    ```dotenv
    DATABASE_URL=mysql://{user}:{password}@{host}:4000/test?sslaccept=strict
    ```

    > **Note**
    >
    > For TiDB Serverless, you **MUST** enable TLS connection by setting `sslaccept=strict` when using public endpoint.

7. Save the `.env` file.
8. In the `prisma/schema.prisma`, set up `mysql` as the connection provider and `env("DATABASE_URL")` as the connection URL:

    ```prisma
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

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

5. Edit the `.env` file, set up the environment variable `DATABASE_URL` as follows, replace the corresponding placeholders `{}` with connection parameters on the connection dialog:

    ```dotenv
    DATABASE_URL=mysql://{user}:{password}@{host}:4000/test?sslaccept=strict&sslcert={downloaded_ssl_ca_path}
    ```

    > **Note**
    >
    > For TiDB Serverless, It is **RECOMMENDED** to enable TLS connection by setting `sslaccept=strict` when using public endpoint. When you set up `sslaccept=strict` to enable TLS connection, you **MUST** specify the file path of the CA certificate downloaded from connection dialog via `sslcert=/path/to/ca.pem`.

6. Save the `.env` file.
7. In the `prisma/schema.prisma`, set up `mysql` as the connection provider and `env("DATABASE_URL")` as the connection URL:

    ```prisma
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

</div>
<div label="TiDB Self-Hosted">

1. Run the following command to copy `.env.example` and rename it to `.env`:

    ```shell
    cp .env.example .env
    ```

2. Edit the `.env` file, set up the environment variable `DATABASE_URL` as follows, replace the corresponding placeholders `{}` with connection parameters of your TiDB cluster:

    ```dotenv
    DATABASE_URL=mysql://{user}:{password}@{host}:4000/test
    ```

   If you are running TiDB locally, the default host address is `127.0.0.1`, and the password is empty.

3. Save the `.env` file.

4. In the `prisma/schema.prisma`, set up `mysql` as the connection provider and `env("DATABASE_URL")` as the connection URL:

    ```prisma
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

</div>
</SimpleTab>

### Step 4. Initialize the database schema

Run following command to invoke [Prisma Migrate](https://www.prisma.io/docs/concepts/components/prisma-migrate) to initialize the database with the data models defined in `prisma/prisma.schema`.

```shell
npx prisma migrate dev
```

**Data models defined in `prisma.schema`:**

```prisma
// Define a Player model, which represents the `players` table.
model Player {
  id        Int      @id @default(autoincrement())
  name      String   @unique(map: "uk_player_on_name") @db.VarChar(50)
  coins     Decimal  @default(0)
  goods     Int      @default(0)
  createdAt DateTime @default(now()) @map("created_at")
  profile   Profile?

  @@map("players")
}

// Define a Profile model, which represents the `profiles` table.
model Profile {
  playerId  Int    @id @map("player_id")
  biography String @db.Text

  // Define a 1:1 relation between the `Player` and `Profile` models with foreign key.
  player    Player @relation(fields: [playerId], references: [id], onDelete: Cascade, map: "fk_profile_on_player_id")

  @@map("profiles")
}
```

To learn how to define data models in Prisma, please check the [Data model](https://www.prisma.io/docs/concepts/components/prisma-schema/data-model) documentation.

**Expected execution output:**

```
Your database is now in sync with your schema.

✔ Generated Prisma Client (5.1.1 | library) to ./node_modules/@prisma/client in 54ms
```

This command will also generate [Prisma Client](https://www.prisma.io/docs/concepts/components/prisma-client) for TiDB database accessing based on the `prisma/prisma.schema`.

### Step 5: Run the code

Run the following command to execute the sample code:

```shell
npm start
```

**Main logic in the sample code:**

```typescript
// Step 1. Import the auto-generated `@prisma/client` package.
import {Player, PrismaClient} from '@prisma/client';

async function main(): Promise<void> {
  // Step 2. Create a new `PrismaClient` instance.
  const prisma = new PrismaClient();
  try {

    // Step 3. Perform some CRUD operations with Prisma Client ...

  } finally {
    // Step 4. Disconnect Prisma Client.
    await prisma.$disconnect();
  }
}

void main();
```

**Expected execution output:**

If the connection is successful, the terminal will output the version of the TiDB cluster as follows:

```
🔌 Connected to TiDB cluster! (TiDB version: 5.7.25-TiDB-v6.6.0-serverless)
🆕 Created a new player with ID 1.
ℹ️ Got Player 1: Player { id: 1, coins: 100, goods: 100 }
🔢 Added 50 coins and 50 goods to player 1, now player 1 has 150 coins and 150 goods.
🚮 Player 1 has been deleted.
```

## Sample code snippets

You can refer to the following sample code snippets to complete your own application development.

For complete sample code and how to run it, check out the [tidb-samples/tidb-nodejs-prisma-quickstart](https://github.com/tidb-samples/tidb-nodejs-prisma-quickstart) repository.

### Insert data

The following query creates a single `Player` record, and returns the created `Player` object, which contains the `id` field generated by TiDB:

```javascript
const player: Player = await prisma.player.create({
   data: {
      name: 'Alice',
      coins: 100,
      goods: 200,
      createdAt: new Date(),
   }
});
```

For more information, refer to [Insert data](/develop/dev-guide-insert-data.md).

### Query data

The following query returns a single `Player` object with ID `101` or `null` if no record is found:

```javascript
const player: Player | null = prisma.player.findUnique({
   where: {
      id: 101,
   }
});
```

For more information, refer to [Query data](/develop/dev-guide-get-data-from-single-table.md).

### Update data

The following query adds `50` coins and `50` goods to the `Player` with ID `101`:

```javascript
await prisma.player.update({
   where: {
      id: 101,
   },
   data: {
      coins: {
         increment: 50,
      },
      goods: {
         increment: 50,
      },
   }
});
```

For more information, refer to [Update data](/develop/dev-guide-update-data.md).

### Delete data

The following query deletes the `Player` with ID `101`:

```javascript
await prisma.player.delete({
   where: {
      id: 101,
   }
});
```

For more information, refer to [Delete data](/develop/dev-guide-delete-data.md).

## Useful notes

### Foreign key constraints vs Prisma relation mode

To check [referential integrity](https://en.wikipedia.org/wiki/Referential_integrity?useskin=vector), you can use foreign key constraints or Prisma relation mode:

- [Foreign key](https://docs.pingcap.com/tidb/stable/foreign-key) is an experimental feature supported starting from TiDB v6.6.0, which allows cross-table referencing of related data, and foreign key constraints to maintain data consistency.

    > **Warning:**
    >
    > **Foreign keys are suitable for small and medium-volumes data scenarios.** Using foreign keys in large data volumes might lead to serious performance issues and could have unpredictable effects on the system. If you plan to use foreign keys, conduct thorough validation first and use them with caution.

- [Prisma relation mode](https://www.prisma.io/docs/concepts/components/prisma-schema/relations/relation-mode) is the emulation of referential integrity in Prisma Client side. However, it should be noted that there are performance implications, as it requires additional database queries to maintain referential integrity.

## Next steps

- Learn more usage of the ORM framework Prisma driver from [the documentation of Prisma](https://www.prisma.io/docs).
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](/develop/dev-guide-overview.md), such as: [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Query data](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

<CustomContent platform="tidb">

Ask questions on the [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc), or [create a support ticket](/support.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

Ask questions on the [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc), or [create a support ticket](https://support.pingcap.com/).

</CustomContent>
