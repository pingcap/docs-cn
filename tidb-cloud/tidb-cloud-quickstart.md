---
title: TiDB Cloud Quick Start
summary: Sign up quickly to try TiDB Cloud and create your TiDB cluster.
category: quick start
aliases: ['/tidbcloud/beta/tidb-cloud-quickstart']
---

# TiDB Cloud Quick Start

*Estimated completion time: 20 minutes*

This tutorial guides you through an easy way to get started with your TiDB Cloud. The content includes how to create a cluster, try playground, load your data, and connect to your cluster.

## Step 1. Create a TiDB cluster

TiDB Cloud [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier) is the best way to get started with TiDB Cloud. To create a free Serverless Tier cluster, take the following steps:

1. If you do not have a TiDB Cloud account, click [here](https://tidbcloud.com/free-trial) to sign up for an account.

    For Google or GitHub users, you can also sign up with your Google or GitHub account. Your email address and password will be managed by Google or GitHub and cannot be changed using the TiDB Cloud console.

2. [Log in](https://tidbcloud.com/) to your TiDB Cloud account.

    The plan selection page is displayed by default.

3. On the plan selection page, click **Get Started for Free** in the **Serverless Tier** plan.

4. On the **Create Cluster** page, **Serverless Tier** is selected by default. Update the default cluster name if necessary, and then select the region where you want to create your cluster.

5. Click **Create**.

    Your TiDB Cloud cluster will be created in several minutes.

6. During the creation process, perform security settings for your cluster:

    1. Click **Security Settings** in the upper-right corner of the cluster area.
    2. In the **Security Settings** dialog box, set a root password to connect to your cluster, and then click **Apply**. If you do not set a root password, you cannot connect to the cluster.

## Step 2. Try Playground

After your TiDB Cloud cluster is created, you can quickly start experimenting with TiDB using the pre-loaded sample data on TiDB Cloud.

On the **Clusters** page, click **Playground** to run queries instantly on TiDB Cloud.

## Step 3. Load sample data

After trying **Plaground**, you can load sample data to your TiDB Cloud cluster. We provide Capital Bikeshare sample data for you to easily import data and run sample queries.

1. Navigate to the **Clusters** page.

2. In the area of your newly created cluster, click **...** in the upper-right corner and select **Import Data**. The **Data Import** page is displayed.

    > **Tip:**
    >
    > Alternatively, you can also click the name of your newly created cluster on the **Clusters** page and click **Import Data** in the **Import** area.

3. Fill in the import parameters:

    - **Data Format**: select **SQL File**
    - **Location**: `AWS`
    - **Bucket URI**: `s3://tidbcloud-samples/data-ingestion/`
    - **Role ARN**: `arn:aws:iam::385595570414:role/import-sample-access`

    If the region of the bucket is different from your cluster, confirm the compliance of cross region. Click **Next**.

4. Add the table filter rules if needed. For the sample data, you can skip this step. Click **Next**.

5. On the **Preview** page, confirm the data to be imported and then click **Start Import**.

The data import process will take several minutes. When the data import progress shows **Finished**, you have successfully imported the sample data and the database schema to your database in TiDB Cloud.

## Step 4. Connect to your TiDB cluster

After loading data to the cluster, you can connect to your cluster from the command line or with a programming language.

1. Navigate to the **Clusters** page.

2. In the area of your newly created cluster, click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Follow the instructions in the dialog to connect to your TiDB cluster.

    1. Create traffic filter for your connection.

    2. Use a SQL client to connect to your cluster. Click the tab of your preferred connection method, and then connect to your cluster with the connection string.

    > **Tip:**
    >
    > TiDB Cloud is MySQL-compatible, so you can connect to your cluster using any MySQL client tool. We recommend using [mysql — The MySQL Command-Line Client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html) or [mysql — The MySQL Command-Line Client from MariaDB](https://mariadb.com/kb/en/mysql-command-line-client/).

4. After logging into your TiDB cluster, you can use the following SQL statement to validate the connection:

    {{< copyable "sql" >}}

    ```sql
    SELECT TiDB_version();
    ```

    If you see the release version information, you are ready to use your TiDB cluster.

## Step 4. Query data

After connecting to your TiDB cluster, you can run some queries in your Terminal.

1. Use the `bikeshare` database and tables:

    {{< copyable "sql" >}}

    ```sql
    USE bikeshare;
    SHOW tables;
    ```

2. Check the structure of the `trip` table:

    {{< copyable "sql" >}}

    ```sql
    DESCRIBE trips;
    ```

3. Check how many records exist in the `trips` table:

    {{< copyable "sql" >}}

    ```sql
    SELECT COUNT(*) FROM trips;
    ```

4. Check the entire trip history where the start station is "8th & D St NW":

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM trips WHERE start_station_name = '8th & D St NW';
    ```

5. Show the least ten popular bicycle stations for picking up:

    {{< copyable "sql" >}}

    ```sql
    SELECT start_station_name, COUNT(ride_id) as count from `trips`
    GROUP BY start_station_name
    ORDER BY count ASC
    LIMIT 10;
    ```

For more details on TiDB SQL usage, see [Explore SQL with TiDB](/basic-sql-operations.md).

For production use with the benefits of cross-zone high availability, horizontal scaling, and [HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing), refer to [Create a TiDB Cluster](/tidb-cloud/create-tidb-cluster.md) and create a Dedicated Tier cluster.
