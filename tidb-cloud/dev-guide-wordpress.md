---
title: Connect to TiDB Serverless with WordPress
summary: Learn how to use TiDB Serverless to run WordPress. This tutorial gives step-by-step guidance to run WordPress + TiDB Serverless in a few minutes.
---

# Connect to TiDB Serverless with WordPress

TiDB is a MySQL-compatible database, TiDB Serverless is a fully managed TiDB offering, and [WordPress](https://github.com/WordPress) is a free, open-source content management system (CMS) that lets users create and manage websites. WordPress is written in PHP and uses a MySQL database.

In this tutorial, you can learn how to use TiDB Serverless to run WordPress for free.

> **Note:**
>
> In addition to TiDB Serverless, this tutorial works with TiDB Dedicated and TiDB Self-Hosted clusters as well. However, it is highly recommended to run WordPress with TiDB Serverless for cost efficiency.

## Prerequisites

To complete this tutorial, you need:

- A TiDB Serverless cluster. Follow [creating a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster if you don't have one.

## Run WordPress with TiDB Serverless

This section demonstrates how to run WordPress with TiDB Serverless.

### Step 1: Clone the WordPress sample repository

Run the following commands in your terminal window to clone the sample code repository:

```shell
git clone https://github.com/Icemap/wordpress-tidb-docker.git
cd wordpress-tidb-docker
```

### Step 2: Install dependencies

1. The sample repository requires [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) to start WordPress. If you have them installed, you can skip this step. It is highly recommended to run your WordPress in a Linux environment (such as Ubuntu). Run the following command to install them:

    ```shell
    sudo sh install.sh
    ```

2. The sample repository includes the [TiDB Compatibility Plugin](https://github.com/pingcap/wordpress-tidb-plugin) as a submodule. Run the following command to update the submodule:

    ```shell
    git submodule update --init --recursive
    ```

### Step 3: Configure connection information

Configure the WordPress database connection to TiDB Serverless.

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

    - **Endpoint Type** is set to `Public`.
    - **Connect With** is set to `WordPress`.
    - **Operating System** is set to `Debian/Ubuntu/Arch`.

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
    TIDB_HOST='{HOST}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    TIDB_PORT='4000'
    TIDB_USER='{USERNAME}'  # e.g. xxxxxx.root
    TIDB_PASSWORD='{PASSWORD}'
    TIDB_DB_NAME='test'
    ```

    Be sure to replace the placeholders `{}` with the connection parameters obtained from the connection dialog. By default, your TiDB Serverless comes with a `test` database. If you have already created another database in your TiDB Serverless cluster, you can replace `test` with your database name.

7. Save the `.env` file.

### Step 4: Start WordPress with TiDB Serverless

1. Execute the following command to run WordPress as a Docker container:

    ```shell
    docker compose up -d
    ```

2. Set up your WordPress site by visiting [localhost](http://localhost/) if you start the container on your local machine or `http://<your_instance_ip>` if the WordPress is running on a remote machine.

## Need help?

Ask questions on the [Discord](https://discord.gg/vYU9h56kAX), or [create a support ticket](/tidb-cloud/tidb-cloud-support.md).
