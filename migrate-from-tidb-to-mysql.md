---
title: Migrate Data from TiDB to MySQL-compatible Databases
summary: Learn how to migrate data from TiDB to MySQL-compatible databases.
---

# Migrate Data from TiDB to MySQL-compatible Databases

This document describes how to migrate data from TiDB clusters to MySQL-compatible databases, such as Aurora, MySQL, and MariaDB. The whole process contains four steps:

1. Set up the environment.
2. Migrate full data.
3. Migrate incremental data.
4. Migrate services to the MySQL-compatible cluster.

## Step 1. Set up the environment

1. Deploy a TiDB cluster upstream.

    Deploy a TiDB cluster by using TiUP Playground. For more information, refer to [Deploy and Maintain an Online TiDB Cluster Using TiUP](/tiup/tiup-cluster.md).

    ```shell
    # Create a TiDB cluster
    tiup playground --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    # View cluster status
    tiup status
    ```

2. Deploy a MySQL instance downstream.

    - In a lab environment, you can use Docker to quickly deploy a MySQL instance by running the following command:

        ```shell
        docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -p 3306:3306 -d mysql
        ```

    - In a production environment, you can deploy a MySQL instance by following instructions in [Installing MySQL](https://dev.mysql.com/doc/refman/8.0/en/installing.html).

3. Simulate service workload.

    In the lab environment, you can use `go-tpc` to write data to the TiDB cluster upstream. This is to generate event changes in the TiDB cluster. Run the following command to create a database named `tpcc` in the TiDB cluster, and then use TiUP bench to write data to this database.

    ```shell
    tiup bench tpcc -H 127.0.0.1 -P 4000 -D tpcc --warehouses 4 prepare
    tiup bench tpcc -H 127.0.0.1 -P 4000 -D tpcc --warehouses 4 run --time 300s
    ```

    For more details about `go-tpc`, refer to [How to Run TPC-C Test on TiDB](/benchmark/benchmark-tidb-using-tpcc.md).

## Step 2. Migrate full data

After setting up the environment, you can use [Dumpling](/dumpling-overview.md) to export the full data from the upstream TiDB cluster.

> **Note:**
>
> In production clusters, performing a backup with GC disabled might affect cluster performance. It is recommended that you complete this step in off-peak hours.

1. Disable Garbage Collection (GC).

    To ensure that newly written data is not deleted during incremental migration, you should disable GC for the upstream cluster before exporting full data. In this way, history data is not deleted.

    Run the following command to disable GC:

    ```sql
    MySQL [test]> SET GLOBAL tidb_gc_enable=FALSE;
    ```

    ```
    Query OK, 0 rows affected (0.01 sec)
    ```

    To verify that the change takes effect, query the value of `tidb_gc_enable`:

    ```sql
    MySQL [test]> SELECT @@global.tidb_gc_enable;
    ```

    ```
    +-------------------------+：
    | @@global.tidb_gc_enable |
    +-------------------------+
    |                       0 |
    +-------------------------+
    1 row in set (0.00 sec)
    ```

2. Back up data.

    1. Export data in SQL format using Dumpling:

        ```shell
        tiup dumpling -u root -P 4000 -h 127.0.0.1 --filetype sql -t 8 -o ./dumpling_output -r 200000 -F256MiB
        ```

    2. After finishing exporting data, run the following command to check the metadata. `Pos` in the metadata is the TSO of the export snapshot and can be recorded as the BackupTS.

        ```shell
        cat dumpling_output/metadata
        ```

        ```
        Started dump at: 2022-06-28 17:49:54
        SHOW MASTER STATUS:
                Log: tidb-binlog
                Pos: 434217889191428107
                GTID:
        Finished dump at: 2022-06-28 17:49:57
        ```

3. Restore data.

    Use MyLoader (an open-source tool) to import data to the downstream MySQL instance. For details about how to install and use MyLoader, see [MyDumpler/MyLoader](https://github.com/mydumper/mydumper). Run the following command to import full data exported by Dumpling to MySQL:

    ```shell
    myloader -h 127.0.0.1 -P 3306 -d ./dumpling_output/
    ```

4. (Optional) Validate data.

    You can use [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) to check data consistency between upstream and downstream at a certain time.

    ```shell
    sync_diff_inspector -C ./config.yaml
    ```

    For details about how to configure the sync-diff-inspector, see [Configuration file description](/sync-diff-inspector/sync-diff-inspector-overview.md#configuration-file-description). In this document, the configuration is as follows:

    ```toml
    # Diff Configuration.
    ######################### Datasource config #########################
    [data-sources]
    [data-sources.upstream]
            host = "127.0.0.1" # Replace the value with the IP address of your upstream cluster
            port = 4000
            user = "root"
            password = ""
            snapshot = "434217889191428107" # Set snapshot to the actual backup time (BackupTS in the "Back up data" section in [Step 2. Migrate full data](#step-2-migrate-full-data))
    [data-sources.downstream]
            host = "127.0.0.1" # Replace the value with the IP address of your downstream cluster
            port = 3306
            user = "root"
            password = ""
    ######################### Task config #########################
    [task]
            output-dir = "./output"
            source-instances = ["upstream"]
            target-instance = "downstream"
            target-check-tables = ["*.*"]
    ```

## Step 3. Migrate incremental data

1. Deploy TiCDC.

    After finishing full data migration, deploy and configure a TiCDC cluster to replicate incremental data. In production environments, deploy TiCDC as instructed in [Deploy TiCDC](/ticdc/deploy-ticdc.md). In this document, a TiCDC node has been started upon the creation of the test cluster. Therefore, you can skip the step of deploying TiCDC and proceed with the next step to create a changefeed.

2. Create a changefeed.

    In the upstream cluster, run the following command to create a changefeed from the upstream to the downstream clusters:

    ```shell
    tiup ctl:v<CLUSTER_VERSION> cdc changefeed create --server=http://127.0.0.1:8300 --sink-uri="mysql://root:@127.0.0.1:3306" --changefeed-id="upstream-to-downstream" --start-ts="434217889191428107"
    ```

    In this command, the parameters are as follows:

    - `--server`: IP address of any node in the TiCDC cluster
    - `--sink-uri`: URI of the downstream cluster
    - `--changefeed-id`: changefeed ID, must be in the format of a regular expression, `^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`
    - `--start-ts`: start timestamp of the changefeed, must be the backup time (or BackupTS in the "Back up data" section in [Step 2. Migrate full data](#step-2-migrate-full-data))

    For more information about the changefeed configurations, see [Task configuration file](/ticdc/ticdc-changefeed-config.md).

3. Enable GC.

    In incremental migration using TiCDC, GC only removes history data that is replicated. Therefore, after creating a changefeed, you need to run the following command to enable GC. For details, see [What is the complete behavior of TiCDC garbage collection (GC) safepoint](/ticdc/ticdc-faq.md#what-is-the-complete-behavior-of-ticdc-garbage-collection-gc-safepoint).

   To enable GC, run the following command:

    ```sql
    MySQL [test]> SET GLOBAL tidb_gc_enable=TRUE;
    ```

    ```
    Query OK, 0 rows affected (0.01 sec)
    ```

    To verify that the change takes effect, query the value of `tidb_gc_enable`:

    ```sql
    MySQL [test]> SELECT @@global.tidb_gc_enable;
    ```

    ```
    +-------------------------+
    | @@global.tidb_gc_enable |
    +-------------------------+
    |                       1 |
    +-------------------------+
    1 row in set (0.00 sec)
    ```

## Step 4. Migrate services

After creating a changefeed, data written to the upstream cluster is replicated to the downstream cluster with low latency. You can migrate read traffic to the downstream cluster gradually. Observe the read traffic for a period. If the downstream cluster is stable, you can migrate write traffic to the downstream cluster as well in the following steps:

1. Stop write services in the upstream cluster. Make sure that all upstream data are replicated to downstream before stopping the changefeed.

    ```shell
    # Stop the changefeed from the upstream cluster to the downstream cluster
    tiup cdc cli changefeed pause -c "upstream-to-downstream" --pd=http://172.16.6.122:2379
    # View the changefeed status
    tiup cdc cli changefeed list
    ```

    ```
    [
      {
        "id": "upstream-to-downstream",
        "summary": {
        "state": "stopped",  # Ensure that the status is stopped
        "tso": 434218657561968641,
        "checkpoint": "2022-06-28 18:38:45.685", # This time should be later than the time of stopping writing
        "error": null
        }
      }
    ]
    ```

2. After migrating writing services to the downstream cluster, observe for a period. If the downstream cluster is stable, you can discard the upstream cluster.
