---
title: Migrate from MySQL-Compatible Databases
summary: Learn how to migrate data from MySQL-compatible databases to TiDB Cloud using the Dumpling and TiDB Lightning tools.
---

# Migrate Data from MySQL-Compatible Databases

TiDB is highly compatible with MySQL. You can migrate data from any MySQL-compatible databases to TiDB smoothly, whether the data is from a self-hosted MySQL instance or RDS service provided by the public cloud.

This document describes how to use [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) to export data from MySQL-compatible databases and use [TiDB Lightning](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview) TiDB-backend to import the data to TiDB Cloud. 

> **Note:**
>
> If your upstream database is Amazon Aurora MySQL, instead of referring to this document, follow instructions in [Migrate from Amazon Aurora MySQL to TiDB Cloud in Bulk](/tidb-cloud/migrate-from-aurora-bulk-import.md).

## Prerequisites

TiDB currently only supports the following CI collations. Before migrating data from MySQL-compatible databases into TiDB, ensure that the supported collations can meet your requirements.

- utf8_general_ci
- utf8mb4_general_ci

## Step 1. Install TiUP

TiUP is a package manager in the TiDB ecosystem, which can help you run any TiDB cluster component with only a single line of command. In this document, TiUP is used to help you install and run Dumpling and TiDB Lightning.

1. Download and install TiUP:

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. Declare the global environment variable:

    > **Note:**
    >
    > After the installation, TiUP displays the absolute path of the corresponding `profile` file. In the following command, you need to modify `.bash_profile` to the path of your `profile` file.

    {{< copyable "shell-regular" >}}

    ```shell
    source .bash_profile
    ```

## Step 2. Export data from MySQL-compatible databases

You can use several ways to dump data from MySQL, such as using `mysqldump` or `mydumper`. It is recommended to use [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) for higher performance and compatibility with TiDB, which is also one of the open source tools created by PingCAP.

1. Install Dumpling:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup install dumpling
    ```

2. Export your MySQL database using Dumpling.

    - To export your data to Amazon S3 cloud storage, see [Export data to Amazon S3 cloud storage](https://docs.pingcap.com/tidb/stable/dumpling-overview#export-data-to-amazon-s3-cloud-storage). 
    - To export your data to local data files, use the following command:

        {{< copyable "shell-regular" >}}

        ```shell
        tiup dumpling -h <mysql-host> -P 3306 -u <user> -F 64MiB -t 8 -o /path/to/export/dir
        ```

        If you want to export only some specified databases, use `-B` to specify a comma-separated list of database names.

        The minimum permissions required are as follows:

        - `SELECT`
        - `RELOAD`
        - `LOCK TABLES`
        - `REPLICATION CLIENT`

## Step 3. Import data to TiDB Cloud

Depending on the location and size of your source data, the importing methods are different.  

- If your source data is located in Amazon S3 cloud storage, take the following steps:

    1. Configure Amazon S3 access to allow TiDB cloud to access the source data in your Amazon S3 bucket. For more information, see [configure Amazon S3 access](/tidb-cloud/migrate-from-amazon-s3-or-gcs.md#step-2-configure-amazon-s3-access). 
    2. From the TiDB Cloud console, navigate to the TiDB Clusters page, and then click the name of your target cluster to go to its own overview page. In the cluster information pane on the left, click **Import**, and then fill in the importing related information on the **Data Import Task** page.

- If your source data is in local files, do one of the following:

    - If the data is larger than 1 TB, it is recommended that you use Amazon S3 or GCS as a staging area to import or migrate data into TiDB Cloud. For more information, see [Import or migrate from Amazon S3 or GCS to TiDB Cloud](/tidb-cloud/migrate-from-amazon-s3-or-gcs.md). 
    - If the data is less than 1 TB, you can use TiDB Lightning TiDB-backend according to the following steps in this document. 

The following steps show how to import data to TiDB Cloud using TiDB Lightning TiDB-backend.

1. Install TiDB Lightning:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup install tidb-lightning
    ```

2. Create a TiDB Lightning configuration file and configure the importing information. 

    1. Create the TiDB Lightning configuration file. 

        {{< copyable "shell-regular" >}}

        ```shell
        vim tidb-lighting.toml
        ```

    2. Configure the importing information.       

        {{< copyable "" >}}

        ```toml
        [lightning] 
        # The address and port to check TiDB Lightning metrics.
        status-addr = '127.0.0.1:8289'

        [tidb]
        # The target cluster information. Fill in one address of tidb-server. 
        # For example: 172.16.128.1
        host = "${host}" 
        # The port number of the target cluster. For example: 4000
        port = ${port number}
        # The target database username. For example: root
        user = "${user_name}" 
        # The target database password. 
        password = "${password}" 

        [tikv-importer]
        # The TiDB backend to be used for data importing. 
        backend = "tidb"

        [mydumper]
        # The data source directory, supporting local path and s3.
        # For example: `/data` for local path or `s3://bucket-name/data-path` for s3
        data-source-dir = "${data_path}"  

        # When Dumpling is used to export data, the corresponding table schemas are exported too by default. 
        # If you want TiDB Lightning to automatically create table schemas in TiDB Cloud according to the exported schemas, set no-schema to false. 
        no-schema = false
        ```

       If you want to configure TLS in the target TiDB cluster or do more configurations, see [TiDB Lightning Configuration](https://docs.pingcap.com/tidb/stable/tidb-lightning-configuration).

3. Import data into TiDB using TiDB Lightning:

    {{< copyable "shell-regular" >}}

    ```shell
    nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```

    After the importing task is started, you can view the importing progress in either of the following ways:

    - To get the progress using command lines, `grep` the keyword `progress` in logs, which is updated every 5 minutes by default.
    - To get more monitoring metrics using the TiDB monitoring framework, see [TiDB Lightning Monitoring](https://docs.pingcap.com/tidb/stable/monitor-tidb-lightning).