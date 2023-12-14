---
title: Connect to TiDB with GORM
summary: Learn how to connect to TiDB using GORM. This tutorial gives Golang sample code snippets that work with TiDB using GORM.
---

# Connect to TiDB with GORM

TiDB is a MySQL-compatible database, and [GORM](https://gorm.io/index.html) is a popular open-source ORM framework for Golang. GORM adapts to TiDB features such as `AUTO_RANDOM` and [supports TiDB as a default database option](https://gorm.io/docs/connecting_to_the_database.html#TiDB).

In this tutorial, you can learn how to use TiDB and GORM to accomplish the following tasks:

- Set up your environment.
- Connect to your TiDB cluster using GORM.
- Build and run your application. Optionally, you can find [sample code snippets](#sample-code-snippets) for basic CRUD operations.

> **Note:**
>
> This tutorial works with TiDB Serverless, TiDB Dedicated, and TiDB Self-Hosted.

## Prerequisites

To complete this tutorial, you need:

- [Go](https://go.dev/) **1.20** or higher.
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

### Step 1: Clone the sample app repository

Run the following commands in your terminal window to clone the sample code repository:

```shell
git clone https://github.com/tidb-samples/tidb-golang-gorm-quickstart.git
cd tidb-golang-gorm-quickstart
```

### Step 2: Configure connection information

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

    > **Tip:**
    >
    > If your program is running in Windows Subsystem for Linux (WSL), switch to the corresponding Linux distribution.

4. Click **Generate Password** to create a random password.

    > **Tip:**
    > 
    > If you have created a password before, you can either use the original password or click **Reset Password** to generate a new one.

5. Run the following command to copy `.env.example` and rename it to `.env`:

    ```shell
    cp .env.example .env
    ```

6. Copy and paste the corresponding connection string into the `.env` file. The example result is as follows:

    ```dotenv
    TIDB_HOST='{host}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. xxxxxx.root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    USE_SSL='true'
    ```

    Be sure to replace the placeholders `{}` with the connection parameters obtained from the connection dialog.

    TiDB Serverless requires a secure connection. Therefore, you need to set the value of `USE_SSL` to `true`.

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

5. Copy and paste the corresponding connection string into the `.env` file. The example result is as follows:

    ```dotenv
    TIDB_HOST='{host}'  # e.g. tidb.xxxx.clusters.tidb-cloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    USE_SSL='false'
    ```

    Be sure to replace the placeholders `{}` with the connection parameters obtained from the connection dialog.

6. Save the `.env` file.

</div>
<div label="TiDB Self-Hosted">

1. Run the following command to copy `.env.example` and rename it to `.env`:

    ```shell
    cp .env.example .env
    ```

2. Copy and paste the corresponding connection string into the `.env` file. The example result is as follows:

    ```dotenv
    TIDB_HOST='{host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    USE_SSL='false'
    ```

    Be sure to replace the placeholders `{}` with the connection parameters, and set `USE_SSL` to `false`. If you are running TiDB locally, the default host address is `127.0.0.1`, and the password is empty.

3. Save the `.env` file.

</div>
</SimpleTab>

### Step 3: Run the code and check the result

1. Execute the following command to run the sample code:

    ```shell
    make
    ```

2. Check the [Expected-Output.txt](https://github.com/tidb-samples/tidb-golang-gorm-quickstart/blob/main/Expected-Output.txt) to see if the output matches.

## Sample code snippets

You can refer to the following sample code snippets to complete your own application development.

For complete sample code and how to run it, check out the [tidb-samples/tidb-golang-gorm-quickstart](https://github.com/tidb-samples/tidb-golang-gorm-quickstart) repository.

### Connect to TiDB

```golang
func createDB() *gorm.DB {
    dsn := fmt.Sprintf("%s:%s@tcp(%s:%s)/%s?charset=utf8mb4&tls=%s",
        ${tidb_user}, ${tidb_password}, ${tidb_host}, ${tidb_port}, ${tidb_db_name}, ${use_ssl})

    db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{
        Logger: logger.Default.LogMode(logger.Info),
    })
    if err != nil {
        panic(err)
    }

    return db
}
```

When using this function, you need to replace `${tidb_host}`, `${tidb_port}`, `${tidb_user}`, `${tidb_password}`, and `${tidb_db_name}` with the actual values of your TiDB cluster. TiDB Serverless requires a secure connection. Therefore, you need to set the value of `${use_ssl}` to `true`.

### Insert data

```golang
db.Create(&Player{ID: "id", Coins: 1, Goods: 1})
```

For more information, refer to [Insert data](/develop/dev-guide-insert-data.md).

### Query data

```golang
var queryPlayer Player
db.Find(&queryPlayer, "id = ?", "id")
```

For more information, refer to [Query data](/develop/dev-guide-get-data-from-single-table.md).

### Update data

```golang
db.Save(&Player{ID: "id", Coins: 100, Goods: 1})
```

For more information, refer to [Update data](/develop/dev-guide-update-data.md).

### Delete data

```golang
db.Delete(&Player{ID: "id"})
```

For more information, refer to [Delete data](/develop/dev-guide-delete-data.md).

## Next steps

- Learn more usage of GORM from [the documentation of GORM](https://gorm.io/docs/index.html) and the [TiDB section in the documentation of GORM](https://gorm.io/docs/connecting_to_the_database.html#TiDB).
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](/develop/dev-guide-overview.md), such as [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Single table reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

<CustomContent platform="tidb">

Ask questions on the [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc), or [create a support ticket](/support.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

Ask questions on the [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc), or [create a support ticket](https://support.pingcap.com/).

</CustomContent>
