---
title: Migrate from one TiDB cluster to another TiDB cluster
summary: Learn how to migrate data from one TiDB cluster to another TiDB cluster.
---

# Migrate from One TiDB Cluster to Another TiDB Cluster

This document describes how to migrate data from one TiDB cluster to another TiDB cluster. This function applies to the following scenarios:

- Split databases: You can split databases when a TiDB cluster is excessively large, or you want to avoid impact between services of a cluster.
- Relocate databases: Physically relocate databases, such as changing the data center.
- Migrate data to a TiDB cluster of a newer version: Migrate data to a TiDB cluster of a newer version to satisfy data security and accuracy requirements.

This document exemplifies the whole migration process and contains the following steps:

1. Set up the environment.

2. Migrate full data.

3. Migrate incremental data.

4. Migrate services to the new TiDB cluster.

## Step 1. Set up the environment

1. Deploy TiDB clusters.

    Deploy two TiDB clusters, one upstream and the other downstream by using TiUP Playground. For more information, refer to [Deploy and Maintain an Online TiDB Cluster Using TiUP](/tiup/tiup-cluster.md).

    ```shell
    # Create an upstream cluster
    tiup --tag upstream playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    # Create a downstream cluster
    tiup --tag downstream playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    # View cluster status
    tiup status
    ```

2. Initialize data.

    By default, test databases are created in the newly deployed clusters. Therefore, you can use [sysbench](https://github.com/akopytov/sysbench#linux) to generate test data and simulate data in real scenarios.

    ```shell
    sysbench oltp_write_only --config-file=./tidb-config --tables=10 --table-size=10000 prepare
    ```

    In this document, we use sysbench to run the `oltp_write_only` script. This script generates 10 tables in the test database, each with 10,000 rows. The tidb-config is as follows:

    ```shell
    mysql-host=172.16.6.122 # Replace the value with the IP address of your upstream cluster
    mysql-port=4000
    mysql-user=root
    mysql-password=
    db-driver=mysql         # Set database driver to MySQL
    mysql-db=test           # Set the database as a test database
    report-interval=10      # Set data collection period to 10s
    threads=10              # Set the number of worker threads to 10
    time=0                  # Set the time required for executing the script. O indicates time unlimited
    rate=100                # Set average TPS to 100
    ```

3. Simulate service workload.

    In real scenarios, service data is continuously written to the upstream cluster. In this document, we use sysbench to simulate this workload. Specifically, run the following command to enable 10 workers to continuously write data to three tables, sbtest1, sbtest2, and sbtest3, with a total TPS not exceeding 100.

    ```shell
    sysbench oltp_write_only --config-file=./tidb-config --tables=3 run
    ```

4. Prepare external storage.

    In full data backup, both the upstream and downstream clusters need to access backup files. It is recommended that you use [External storage](/br/backup-and-restore-storages.md) to store backup files. In this document, Minio is used to simulate an S3-compatible storage service.

    ```shell
    wget https://dl.min.io/server/minio/release/linux-amd64/minio
    chmod +x minio
    # Configure access-key access-screct-id to access minio
    export HOST_IP='172.16.6.122' # Replace the value with the IP address of your upstream cluster
    export MINIO_ROOT_USER='minio'
    export MINIO_ROOT_PASSWORD='miniostorage'
    # Create the database directory. backup is the bucket name.
    mkdir -p data/backup
    # Start minio at port 6060
    ./minio server ./data --address :6060 &
    ```

    The preceding command starts a minio server on one node to simulate S3 services. Parameters in the command are configured as follows:

    - Endpoint: `http://${HOST_IP}:6060/`
    - Access-key: `minio`
    - Secret-access-key: `miniostorage`
    - Bucket: `backup`

    The access link is as follows:

    ```shell
    s3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true
    ```

## Step 2. Migrate full data

After setting up the environment, you can use the backup and restore functions of [BR](https://github.com/pingcap/tidb/tree/master/br) to migrate full data. BR can be started in [three ways](/br/br-use-overview.md#deploy-and-use-br). In this document, we use the SQL statements, `BACKUP` and `RESTORE`.

> **Note:**
>
> - `BACKUP` and `RESTORE` SQL statements are experimental. It is not recommended that you use them in the production environment. They might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.
> - In production clusters, performing a backup with GC disabled might affect cluster performance. It is recommended that you back up data in off-peak hours, and set `RATE_LIMIT` to a proper value to avoid performance degradation.
> - If the versions of the upstream and downstream clusters are different, you should check [BR compatibility](/br/backup-and-restore-overview.md#before-you-use). In this document, we assume that the upstream and downstream clusters are the same version.

1. Disable GC.

    To ensure that newly written data is not deleted during incremental migration, you should disable GC for the upstream cluster before backup. In this way, history data is not deleted.

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
    +-------------------------+:
    | @@global.tidb_gc_enable |
    +-------------------------+
    |                       0 |
    +-------------------------+
    1 row in set (0.00 sec)
    ```

2. Back up data.

    Run the `BACKUP` statement in the upstream cluster to back up data:

    ```sql
    MySQL [(none)]> BACKUP DATABASE * TO 's3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true' RATE_LIMIT = 120 MB/SECOND;
    ```

    ```
    +---------------+----------+--------------------+---------------------+---------------------+
    | Destination   | Size     | BackupTS           | Queue Time          | Execution Time      |
    +---------------+----------+--------------------+---------------------+---------------------+
    | s3://backup   | 10315858 | 431434047157698561 | 2022-02-25 19:57:59 | 2022-02-25 19:57:59 |
    +---------------+----------+--------------------+---------------------+---------------------+
    1 row in set (2.11 sec)
    ```

    After the `BACKUP` command is executed, TiDB returns metadata about the backup data. Pay attention to `BackupTS`, because data generated before it is backed up. In this document, we use `BackupTS` as **the end of data check** and **the start of incremental migration scanning by TiCDC**.

3. Restore data.

    Run the `RESTORE` command in the downstream cluster to restore data:

    ```sql
    mysql> RESTORE DATABASE * FROM 's3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true';
    ```

    ```
    +--------------+-----------+--------------------+---------------------+---------------------+
    | Destination  | Size      | BackupTS           | Queue Time          | Execution Time      |
    +--------------+-----------+--------------------+---------------------+---------------------+
    | s3://backup  | 10315858  | 431434141450371074 | 2022-02-25 20:03:59 | 2022-02-25 20:03:59 |
    +--------------+-----------+--------------------+---------------------+---------------------+
    1 row in set (41.85 sec)
    ```

4. (Optional) Validate data.

    You can use [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) to check data consistency between upstream and downstream at a certain time. The preceding `BACKUP` output shows that the upstream cluster finishes backup at 431434047157698561. The preceding `RESTORE` output shows that the downstream finishes restoration at 431434141450371074.

    ```shell
    sync_diff_inspector -C ./config.yaml
    ```

    For details about how to configure the sync-diff-inspector, see [Configuration file description](/sync-diff-inspector/sync-diff-inspector-overview.md#configuration-file-description). In this document, the configuration is as follows:

    ```shell
    # Diff Configuration.
    ######################### Datasource config #########################
    [data-sources]
    [data-sources.upstream]
        host = "172.16.6.122" # Replace the value with the IP address of your upstream cluster
        port = 4000
        user = "root"
        password = ""
        snapshot = "431434047157698561" # Set snapshot to the actual backup time (BackupTS in the "Back up data" section in [Step 2. Migrate full data](#step-2-migrate-full-data))
    [data-sources.downstream]
        host = "172.16.6.125" # Replace the value with the IP address of your downstream cluster
        port = 4000
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

    After finishing full data migration, deploy and configure a TiCDC to replicate incremental data. In production environments, deploy TiCDC as instructed in [Deploy TiCDC](/ticdc/deploy-ticdc.md). In this document, a TiCDC node has been started upon the creation of the test clusters. Therefore, you can skip the step of deploying TiCDC and proceed with changefeed configuration.

2. Create a changefeed.

    In the upstream cluster, run the following command to create a changefeed from the upstream to the downstream clusters:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cdc cli changefeed create --server=http://172.16.6.122:8300 --sink-uri="mysql://root:@172.16.6.125:4000" --changefeed-id="upstream-to-downstream" --start-ts="431434047157698561"
    ```

    In this command, the parameters are as follows:

    - `--server`: IP address of any node in the TiCDC cluster
    - `--sink-uri`: URI of the downstream cluster
    - `--changefeed-id`: changefeed ID, must be in the format of a regular expression, ^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$
    - `--start-ts`: start timestamp of the changefeed, must be the backup time (or BackupTS in the "Back up data" section in [Step 2. Migrate full data](#step-2-migrate-full-data))

    For more information about the changefeed configurations, see [Task configuration file](/ticdc/ticdc-changefeed-config.md).

3. Enable GC.

    In incremental migration using TiCDC, GC only removes history data that is replicated. Therefore, after creating a changefeed, you need to run the following command to enable GC. For details, see [What is the complete behavior of TiCDC garbage collection (GC) safepoint?](/ticdc/ticdc-faq.md#what-is-the-complete-behavior-of-ticdc-garbage-collection-gc-safepoint).

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

## Step 4. Migrate services to the new TiDB cluster

After creating a changefeed, data written to the upstream cluster is replicated to the downstream cluster with low latency. You can migrate read traffic to the downstream cluster gradually. Observe for a period. If the downstream cluster is stable, you can migrate write traffic to the downstream cluster by performing the following steps:

1. Stop write services in the upstream cluster. Make sure that all upstream data are replicated to downstream before stopping the changefeed.

    ```shell
    # Stop the changefeed from the upstream cluster to the downstream cluster
    tiup cdc cli changefeed pause -c "upstream-to-downstream" --server=http://172.16.6.122:8300

    # View the changefeed status
    tiup cdc cli changefeed list
    ```

    ```
    [
      {
        "id": "upstream-to-downstream",
        "summary": {
        "state": "stopped",  # Ensure that the status is stopped
        "tso": 431747241184329729,
        "checkpoint": "2022-03-11 15:50:20.387", # This time must be later than the time of stopping writing
        "error": null
        }
      }
    ]
    ```

2. Create a changefeed from downstream to upstream. You can leave `start-ts` unspecified so as to use the default setting, because the upstream and downstream data are consistent and there is no new data written to the cluster.

    ```shell
    tiup cdc cli changefeed create --server=http://172.16.6.125:8300 --sink-uri="mysql://root:@172.16.6.122:4000" --changefeed-id="downstream -to-upstream"
    ```

3. After migrating writing services to the downstream cluster, observe for a period. If the downstream cluster is stable, you can discard the upstream cluster.
