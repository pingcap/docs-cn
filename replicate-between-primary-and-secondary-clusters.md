---
title: Replicate data between primary and secondary clusters
summary: Learn how to replicate data from a primary cluster to a secondary cluster.
aliases: ['/docs/dev/incremental-replication-between-clusters/', '/tidb/dev/replicate-betwwen-primary-and-secondary-clusters/']
---

# Replicate Data Between Primary and Secondary Clusters

This document describes how to configure a TiDB primary (upstream) cluster and a TiDB or MySQL secondary (downstream) cluster, and replicate incremental data from the primary cluster to the secondary cluster. The process includes the following steps:

1. Configure a TiDB primary cluster and a TiDB or MySQL secondary cluster.
2. Replicate incremental data from the primary cluster to the secondary cluster.
3. Recover data consistently by using Redo log when the primary cluster is down.

To replicate incremental data from a running TiDB cluster to its secondary cluster, you can use Backup & Restore [BR](/br/backup-and-restore-overview.md) and [TiCDC](/ticdc/ticdc-overview.md).

## Step 1. Set up the environment

1. Deploy TiDB clusters.

    Deploy two TiDB clusters, one upstream and the other downstream by using TiUP Playground. For production environments, deploy the clusters by referring to [Deploy and Maintain an Online TiDB Cluster Using TiUP](/tiup/tiup-cluster.md).

    In this document, we deploy the two clusters on two machines:

    - Node A: 172.16.6.123, for deploying the upstream TiDB cluster

    - Node B: 172.16.6.124, for deploying the downstream TiDB cluster

    ```shell
    # Create an upstream cluster on Node A
    tiup --tag upstream playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    # Create a downstream cluster on Node B
    tiup --tag downstream playground --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 0
    # View cluster status
    tiup status
    ```

2. Initialize data.

    By default, test databases are created in the newly deployed clusters. Therefore, you can use [sysbench](https://github.com/akopytov/sysbench#linux) to generate test data and simulate data in real scenarios.

    ```shell
    sysbench oltp_write_only --config-file=./tidb-config --tables=10 --table-size=10000 prepare
    ```

    In this document, we use sysbench to run the `oltp_write_only` script. This script generates 10 tables in the upstream database, each with 10,000 rows. The tidb-config is as follows:

    ```shell
    mysql-host=172.16.6.122 # Replace it with the IP address of your upstream cluster
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

    In full data backup, both the upstream and downstream clusters need to access backup files. It is recommended that you use [External storage](/br/backup-and-restore-storages.md) to store backup files. In this example, Minio is used to simulate an S3-compatible storage service.

    ```shell
    wget https://dl.min.io/server/minio/release/linux-amd64/minio
    chmod +x minio
    # Configure access-key access-screct-id to access minio
    export HOST_IP='172.16.6.123' # Replace it with the IP address of your upstream cluster
    export MINIO_ROOT_USER='minio'
    export MINIO_ROOT_PASSWORD='miniostorage'
    # Create the redo and backup directories. `backup` and `redo` are bucket names.
    mkdir -p data/redo
    mkdir -p data/backup
    # Start minio at port 6060
    nohup ./minio server ./data --address :6060 &
    ```

    The preceding command starts a minio server on one node to simulate S3 services. Parameters in the command are configured as follows:

    - Endpoint: `http://${HOST_IP}:6060/`
    - Access-key: `minio`
    - Secret-access-key: `miniostorage`
    - Bucket: `redo`

    The link is as follows:

    ```shell
    s3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true
    ```

## Step 2. Migrate full data

After setting up the environment, you can use the backup and restore functions of [BR](https://github.com/pingcap/tidb/tree/master/br)) to migrate full data. BR can be started in [three ways](/br/br-use-overview.md#deploy-and-use-br). In this document, we use the SQL statements, `BACKUP` and `RESTORE`.

> **Note:**
>
> - In production clusters, performing a backup with GC disabled might affect cluster performance. It is recommended that you back up data in off-peak hours, and set RATE_LIMIT to a proper value to avoid performance degradation.
>
> - If the versions of the upstream and downstream clusters are different, you should check [BR compatibility](/br/backup-and-restore-overview.md#some-tips). In this document, we assume that the upstream and downstream clusters are the same version.

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
    +-------------------------+
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
    +----------------------+----------+--------------------+---------------------+---------------------+
    | Destination          | Size     | BackupTS           | Queue Time          | Execution Time      |
    +----------------------+----------+--------------------+---------------------+---------------------+
    | local:///tmp/backup/ | 10315858 | 431434047157698561 | 2022-02-25 19:57:59 | 2022-02-25 19:57:59 |
    +----------------------+----------+--------------------+---------------------+---------------------+
    1 row in set (2.11 sec)
    ```

    After the `BACKUP` command is executed, TiDB returns metadata about the backup data. Pay attention to `BackupTS`, because data generated before it is backed up. In this document, we use `BackupTS` as **the end of data check** and **the start of incremental migration scanning by TiCDC**.

3. Restore data.

    Run the `RESTORE` command in the downstream cluster to restore data:

    ```sql
    mysql> RESTORE DATABASE * FROM 's3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://${HOST_IP}:6060&force-path-style=true';
    ```

    ```
    +----------------------+----------+--------------------+---------------------+---------------------+
    | Destination          | Size     | BackupTS           | Queue Time          | Execution Time      |
    +----------------------+----------+--------------------+---------------------+---------------------+
    | local:///tmp/backup/ | 10315858 | 431434141450371074 | 2022-02-25 20:03:59 | 2022-02-25 20:03:59 |
    +----------------------+----------+--------------------+---------------------+---------------------+
    1 row in set (41.85 sec)
    ```

4. (Optional) Validate data.

    Use [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) to check data consistency between upstream and downstream at a certain time. The preceding `BACKUP` output shows that the upstream cluster finishes backup at 431434047157698561. The preceding `RESTORE` output shows that the downstream finishes restoration at 431434141450371074.

    ```shell
    sync_diff_inspector -C ./config.yaml
    ```

    For details about how to configure the sync-diff-inspector, see [Configuration file description](/sync-diff-inspector/sync-diff-inspector-overview.md#configuration-file-description). In this document, the configuration is as follows:

    ```shell
    # Diff Configuration.
    ######################### Global config #########################
    check-thread-count = 4
    export-fix-sql = true
    check-struct-only = false

    ######################### Datasource config #########################
    [data-sources]
    [data-sources.upstream]
            host = "172.16.6.123" # Replace it with the IP address of your upstream cluster
            port = 4000
            user = "root"
            password = ""
            snapshot = "431434047157698561" # Set snapshot to the actual backup time
    [data-sources.downstream]
            host = "172.16.6.124" # Replace the value with the IP address of your downstream cluster
            port = 4000
            user = "root"
            password = ""
            snapshot = "431434141450371074" # Set snapshot to the actual restore time

    ######################### Task config #########################
    [task]
            output-dir = "./output"
            source-instances = ["upstream"]
            target-instance = "downstream"
            target-check-tables = ["*.*"]
    ```

## Step 3. Migrate incremental data

1. Deploy TiCDC.

    After finishing full data migration, deploy and configure a TiCDC to replicate incremental data. In production environments, deploy TiCDC as instructed in [Deploy TiCDC](/ticdc/deploy-ticdc.md). In this document, a TiCDC node has been started upon the creation of the test clusters. Therefore, we skip the step of deploying TiCDC and proceed with changefeed configuration.

2. Create a changefeed.

    Create a changefeed configuration file `changefeed.toml`.

    ```shell
    [consistent]
    # Consistency level, eventual means enabling consistent replication
    level = "eventual"
    # Use S3 to store redo logs. Other options are local and nfs.
    storage = "s3://redo?access-key=minio&secret-access-key=miniostorage&endpoint=http://172.16.6.125:6060&force-path-style=true"
    ```

    In the upstream cluster, run the following command to create a changefeed from the upstream to the downstream clusters:

    ```shell
    tiup cdc cli changefeed create --server=http://172.16.6.122:8300 --sink-uri="mysql://root:@172.16.6.125:4000" --changefeed-id="primary-to-secondary" --start-ts="431434047157698561"
    ```

    In this command, the parameters are as follows:

    - `--server`: IP address of any node in the TiCDC cluster
    - `--sink-uri`: URI of the downstream cluster
    - `--start-ts`: start timestamp of the changefeed, must be the backup time (or BackupTS mentioned in [Step 2. Migrate full data](#step-2-migrate-full-data))

    For more information about the changefeed configurations, see [TiCDC Changefeed Configurations](/ticdc/ticdc-changefeed-config.md).

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

## Step 4. Simulate a disaster in the upstream cluster

Create a disastrous event in the upstream cluster while it is running. For example, you can terminate the tiup playground process by pressing Ctrl+C.

## Step 5. Use redo log to ensure data consistency

Normally, TiCDC concurrently writes transactions to downstream to increase throughout. When a changefeed is interrupted unexpectedly, the downstream may not have the latest data as it is in the upstream. To address inconsistency, run the following command to ensure that the downstream data is consistent with the upstream data.

```shell
tiup cdc redo apply --storage "s3://redo?access-key=minio&secret-access-key=miniostorage&endpoint=http://172.16.6.123:6060&force-path-style=true" --tmp-dir /tmp/redo --sink-uri "mysql://root:@172.16.6.124:4000"
```

- `--storage`: Location and credential of the redo log in S3
- `--tmp-dir`: Cache directory of the redo log downloaded from S3
- `--sink-uri`: URI of the downstream cluster

## Step 6. Recover the primary cluster and its services

After the previous step, the downstream (secondary) cluster has data that is consistent with the upstream (primary) cluster at a specific time. You need to set up new primary and secondary clusters to ensure data reliability.

1. Deploy a new TiDB cluster on Node A as the new primary cluster.

    ```shell
    tiup --tag upstream playground v5.4.0 --host 0.0.0.0 --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    ```

2. Use BR to back up and restore data fully from the secondary cluster to the primary cluster.

    ```shell
    # Back up full data of the secondary cluster
    tiup br --pd http://172.16.6.124:2379 backup full --storage ./backup
    # Restore full data of the secondary cluster
    tiup br --pd http://172.16.6.123:2379 restore full --storage ./backup
    ```

3. Create a new changefeed to back up data from the primary cluster to the secondary cluster.

    ```shell
    # Create a changefeed
    tiup cdc cli changefeed create --server=http://172.16.6.122:8300 --sink-uri="mysql://root:@172.16.6.125:4000" --changefeed-id="primary-to-secondary"
    ```
