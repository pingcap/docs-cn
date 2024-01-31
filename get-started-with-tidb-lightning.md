---
title: Quick Start for TiDB Lightning
aliases: ['/docs/dev/get-started-with-tidb-lightning/','/docs/dev/how-to/get-started/tidb-lightning/']
---

# Quick Start for TiDB Lightning

This document provides a quick guide on getting started with TiDB Lightning by importing MySQL data into a TiDB cluster.

> **Warning:**
>
> The deployment method in this tutorial is only recommended for test and trial. **Do not apply it in the production or development environment.**

## Step 1: Prepare full backup data

First, you can use [dumpling](/dumpling-overview.md) to export data from MySQL.

1. Run `tiup --version` to check if TiUP is already installed. If TiUP is installed, skip this step. If TiUP is not installed, run the following command:

    ```
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. Using TiUP to install Dumpling:

    ```shell
    tiup install dumpling
    ```

3. To export data from MySQL, you can refer to the detailed steps provided in [Use Dumpling to Export Data](/dumpling-overview.md#export-to-sql-files)：

    ```sh
    tiup dumpling -h 127.0.0.1 -P 3306 -u root -t 16 -F 256MB -B test -f 'test.t[12]' -o /data/my_database/
    ```

    In the above command:

    - `-t 16`: Export data using 16 threads.
    - `-F 256MB`: Split each table into multiple files, with each file approximately 256 MB in size.
    - `-B test`: Export from the `test` database.
    - `-f 'test.t[12]'`: Export only the two tables `test.t1` and `test.t2`.

    The full backup data exported will be saved in the `/data/my_database` directory.

## Step 2: Deploy the TiDB cluster

Before starting the data import, you need to deploy a TiDB cluster for the import. If you already have a TiDB cluster, you can skip this step.

For the steps on deploying a TiDB cluster, refer to the [Quick Start Guide for the TiDB Database Platform](/quick-start-with-tidb.md).

## Step 3: Install TiDB Lightning

Run the following command to install the latest version of TiDB Lightning:

```shell
tiup install tidb-lightning
```

## Step 4: Start TiDB Lightning

> **Note:**
>
> The import method in this section is only suitable for testing and functional experience. For production environments, refer to [Migrate Large Datasets from MySQL to TiDB](/migrate-large-mysql-to-tidb.md)

1. Create the configuration file `tidb-lightning.toml` and fill in the following settings based on your cluster information:

    ```toml
    [lightning]
    # Logging
    level = "info"
    file = "tidb-lightning.log"

    [tikv-importer]
    # Configure the import mode
    backend = "local"
    # Sets the directory for temporarily storing the sorted key-value pairs. The target directory must be empty.
    sorted-kv-dir = "/mnt/ssd/sorted-kv-dir"

    [mydumper]
    # Local source data directory
    data-source-dir = "/data/my_datasource/"

    # Configures the wildcard rule. By default, all tables in the mysql, sys, INFORMATION_SCHEMA, PERFORMANCE_SCHEMA, METRICS_SCHEMA, and INSPECTION_SCHEMA system databases are filtered.
    # If this item is not configured, the "cannot find schema" error occurs when system tables are imported.
    filter = ['*.*', '!mysql.*', '!sys.*', '!INFORMATION_SCHEMA.*', '!PERFORMANCE_SCHEMA.*', '!METRICS_SCHEMA.*', '!INSPECTION_SCHEMA.*']
    [tidb]
    # Information of the target cluster
    host = "172.16.31.2"
    port = 4000
    user = "root"
    password = "rootroot"
    # Table schema information is fetched from TiDB via this status-port.
    status-port = 10080
    # The PD address of the cluster. Starting from v7.6.0, TiDB supports setting multiple PD addresses.
    pd-addr = "172.16.31.3:2379,56.78.90.12:3456"
    ```

2. Run `tidb-lightning`. To avoid the program exiting due to the `SIGHUP` signal when starting the program directly in the command line using `nohup`, it is recommended to put the `nohup` command in a script. For example:

    ```shell
    #!/bin/bash
    nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```

## Step 5: Check data integrity

After the import is completed, TiDB Lightning exits automatically. If the import is successful, you can find `tidb lightning exit` in the last line of the log file.

If any error occurs, refer to [TiDB Lightning FAQs](/tidb-lightning/tidb-lightning-faq.md).

## Summary

This tutorial briefly introduces what TiDB Lightning is and how to quickly deploy a TiDB Lightning cluster to import full backup data to the TiDB cluster.

For detailed features and usage about TiDB Lightning, refer to [TiDB Lightning Overview](/tidb-lightning/tidb-lightning-overview.md).
