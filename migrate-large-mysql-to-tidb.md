---
title: Migrate MySQL of Large Datasets to TiDB
summary: Learn how to migrate MySQL of large datasets to TiDB.
---

# Migrate MySQL of Large Datasets to TiDB

When the data volume to be migrated is small, you can easily [use DM to migrate data](/migrate-small-mysql-to-tidb.md), both for full migration and incremental replication. However, because DM imports data at a slow speed (30~50 GiB/h), when the data volume is large, the migration might take a long time. "Large datasets" in this document usually mean data around one TiB or more.

This document describes how to migrate large datasets from MySQL to TiDB. The whole migration has two processes:

1. *Full migration*. Use Dumpling and TiDB Lightning to perform the full migration. TiDB Lightning's **local backend** mode can import data at a speed of up to 500 GiB/h.
2. *Incremental replication*. After the full migration is completed, you can replicate the incremental data using DM.

## Prerequisites

- [Install DM](/dm/deploy-a-dm-cluster-using-tiup.md).
- [Install Dumpling and TiDB Lightning](/migration-tools.md).
- [Grant the source database and target database privileges required for DM](/dm/dm-worker-intro.md).
- [Grant the target database privileges required for TiDB Lightning](/tidb-lightning/tidb-lightning-faq.md#what-are-the-privilege-requirements-for-the-target-database).
- [Grant the source database privileges required for Dumpling](/dumpling-overview.md#export-data-from-tidb-or-mysql).

## Resource requirements

**Operating system**: The example in this document uses fresh CentOS 7 instances. You can deploy a virtual machine either on your local host or in the cloud. Because TiDB Lightning consumes as much CPU resources as needed by default, it is recommended that you deploy it on a dedicated server. If this is not possible, you can deploy it on a single server together with other TiDB components (for example, `tikv-server`) and then configure `region-concurrency` to limit the CPU usage from TiDB Lightning. Usually, you can configure the size to 75% of the logical CPU.

**Memory and CPU**: Because TiDB Lightning consumes high resources, it is recommended to allocate more than 64 GiB of memory and more than 32 CPU cores. To get the best performance, make sure that the CPU core to memory (GiB) ratio is greater than 1:2.

**Disk space**:

- Dumpling requires a disk space that can store the whole data source (or to store all upstream tables to be exported). SSD is recommended. To calculate the required space, see [Downstream storage space requirements](/tidb-lightning/tidb-lightning-requirements.md#storage-space-of-the-target-database).
- During the import, TiDB Lightning needs temporary space to store the sorted key-value pairs. The disk space should be enough to hold the largest single table from the data source.
- If the full data volume is large, you can increase the binlog storage time in the upstream. This is to ensure that the binlogs are not lost during the incremental replication.

**Note**: It is difficult to calculate the exact data volume exported by Dumpling from MySQL, but you can estimate the data volume by using the following SQL statement to summarize the `data-length` field in the `information_schema.tables` table:

{{< copyable "" >}}

```sql
/* Calculate the size of all schemas, in MiB. Replace ${schema_name} with your schema name. */
SELECT table_schema,SUM(data_length)/1024/1024 AS data_length,SUM(index_length)/1024/1024 AS index_length,SUM(data_length+index_length)/1024/1024 AS SUM FROM information_schema.tables WHERE table_schema = "${schema_name}" GROUP BY table_schema;

/* Calculate the size of the largest table, in MiB. Replace ${schema_name} with your schema name. */
SELECT table_name,table_schema,SUM(data_length)/1024/1024 AS data_length,SUM(index_length)/1024/1024 AS index_length,SUM(data_length+index_length)/1024/1024 AS SUM from information_schema.tables WHERE table_schema = "${schema_name}" GROUP BY table_name,table_schema ORDER BY SUM DESC LIMIT 5;
```

### Disk space for the target TiKV cluster

The target TiKV cluster must have enough disk space to store the imported data. In addition to [the standard hardware requirements](/hardware-and-software-requirements.md), the storage space of the target TiKV cluster must be larger than **the size of the data source x [the number of replicas](/faq/manage-cluster-faq.md#is-the-number-of-replicas-in-each-region-configurable-if-yes-how-to-configure-it) x 2**. For example, if the cluster uses 3 replicas by default, the target TiKV cluster must have a storage space larger than 6 times the size of the data source. The formula has `x 2` because:

- Index might take extra space.
- RocksDB has a space amplification effect.

## Step 1. Export all data from MySQL

1. Export all data from MySQL by running the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup dumpling -h ${ip} -P 3306 -u root -t 16 -r 200000 -F 256MiB -B my_db1 -f 'my_db1.table[12]' -o 's3://my-bucket/sql-backup'
    ```

    Dumpling exports data in SQL files by default. You can specify a different file format by adding the `--filetype` option.

    The parameters used above are as follows. For more Dumpling parameters, refer to [Dumpling Overview](/dumpling-overview.md).

    |parameters             |Description|
    |-                      |-|
    |`-u` or `--user`       |MySQL user|
    |`-p` or `--password`   |MySQL user password|
    |`-P` or `--port`       |MySQL port|
    |`-h` or `--host`       |MySQL IP address|
    |`-t` or `--thread`     |The number of threads used for export|
    |`-o` or `--output`     |The directory that stores the exported file. Supports a local path or an [external storage URL](/br/backup-and-restore-storages.md#url-format)|
    |`-r` or `--row`        |The maximum number of rows in a single file|
    |`-F`                   |The maximum size of a single file, in MiB. Recommended value: 256 MiB.|
    |-`B` or `--database`   |Specifies a database to be exported|
    |`-f` or `--filter`     |Exports tables that match the pattern. Refer to [table-filter](/table-filter.md) for the syntax.|

    Make sure `${data-path}` has the space to store all exported upstream tables. To calculate the required space, see [Downstream storage space requirements](/tidb-lightning/tidb-lightning-requirements.md#storage-space-of-the-target-database). To prevent the export from being interrupted by a large table consuming all the spaces, it is strongly recommended to use the `-F` option to limit the size of a single file.

2. View the `metadata` file in the `${data-path}` directory. This is a Dumpling-generated metadata file. Record the binlog position information, which is required for the incremental replication in Step 3.

    ```
    SHOW MASTER STATUS:
    Log: mysql-bin.000004
    Pos: 109227
    GTID:
    ```

## Step 2. Import full data to TiDB

1. Create the `tidb-lightning.toml` configuration file:

    {{< copyable "" >}}

    ```toml
    [lightning]
    # log.
    level = "info"
    file = "tidb-lightning.log"

    [tikv-importer]
    # "local": Default backend. The local backend is recommended to import large volumes of data (1 TiB or more). During the import, the target TiDB cluster cannot provide any service.
    # "tidb": The "tidb" backend is recommended to import data less than 1 TiB. During the import, the target TiDB cluster can provide service normally. For more information on the backends, refer to https://docs.pingcap.com/tidb/stable/tidb-lightning-backends.
    backend = "local"
    # Sets the temporary storage directory for the sorted Key-Value files. The directory must be empty, and the storage space must be greater than the size of the dataset to be imported. For better import performance, it is recommended to use a directory different from `data-source-dir` and use flash storage, which can use I/O exclusively.
    sorted-kv-dir = "${sorted-kv-dir}"

    [mydumper]
    # The data source directory. The same directory where Dumpling exports data in "Step 1. Export all data from MySQL".
    data-source-dir = "${data-path}" # A local path or S3 path. For example, 's3://my-bucket/sql-backup'.

    [tidb]
    # The target TiDB cluster information.
    host = ${host}                # e.g.: 172.16.32.1
    port = ${port}                # e.g.: 4000
    user = "${user_name}"         # e.g.: "root"
    password = "${password}"      # e.g.: "rootroot"
    status-port = ${status-port}  # During the import, TiDB Lightning needs to obtain the table schema information from the TiDB status port. e.g.: 10080
    pd-addr = "${ip}:${port}"     # The address of the PD cluster, e.g.: 172.16.31.3:2379. TiDB Lightning obtains some information from PD. When backend = "local", you must specify status-port and pd-addr correctly. Otherwise, the import will be abnormal.
    ```

    For more information on TiDB Lightning configuration, refer to [TiDB Lightning Configuration](/tidb-lightning/tidb-lightning-configuration.md).

2. Start the import by running `tidb-lightning`. If you launch the program directly in the command line, the process might exit unexpectedly after receiving a SIGHUP signal. In this case, it is recommended to run the program using a `nohup` or `screen` tool. For example:

    If you import data from S3, pass the SecretKey and AccessKey that have access to the S3 storage path as environment variables to the TiDB Lightning node. You can also read the credentials from `~/.aws/credentials`.

    {{< copyable "shell-regular" >}}

    ```shell
    export AWS_ACCESS_KEY_ID=${access_key}
    export AWS_SECRET_ACCESS_KEY=${secret_key}
    nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out 2>&1 &
    ```

3. After the import starts, you can check the progress of the import by one of the following methods:

    - `grep` the keyword `progress` in the log. The progress is updated every 5 minutes by default.
    - Check progress in [the monitoring dashboard](/tidb-lightning/monitor-tidb-lightning.md).
    - Check progress in [the TiDB Lightning web interface](/tidb-lightning/tidb-lightning-web-interface.md).

4. After TiDB Lightning completes the import, it exits automatically. Check whether `tidb-lightning.log` contains `the whole procedure completed` in the last lines. If yes, the import is successful. If no, the import encounters an error. Address the error as instructed in the error message.

> **Note:**
>
> Whether the import is successful or not, the last line of the log shows `tidb lightning exit`. It means that TiDB Lightning exits normally, but does not necessarily mean that the import is successful.

If the import fails, refer to [TiDB Lightning FAQ](/tidb-lightning/tidb-lightning-faq.md) for troubleshooting.

## Step 3. Replicate incremental data to TiDB

### Add the data source

1. Create a `source1.yaml` file as follows:

    {{< copyable "" >}}

    ```yaml
    # Must be unique.
    source-id: "mysql-01"

    # Configures whether DM-worker uses the global transaction identifier (GTID) to pull binlogs. To enable this mode, the upstream MySQL must also enable GTID. If the upstream MySQL service is configured to switch master between different nodes automatically, GTID mode is required.
    enable-gtid: true

    from:
      host: "${host}"           # e.g.: 172.16.10.81
      user: "root"
      password: "${password}"   # Supported but not recommended to use a plaintext password. It is recommended to use `dmctl encrypt` to encrypt the plaintext password before using it.
      port: 3306
    ```

2. Load the data source configuration to the DM cluster using `tiup dmctl` by running the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup dmctl --master-addr ${advertise-addr} operate-source create source1.yaml
    ```

    The parameters used in the command above are described as follows:

    |Parameter              |Description    |
    |-                      |-              |
    |`--master-addr`        |The `{advertise-addr}` of any DM-master in the cluster where `dmctl` is to be connected, e.g.: 172.16.10.71:8261|
    |`operate-source create`|Loads the data source to the DM cluster.|

### Add a replication task

1. Edit the `task.yaml` file. Configure the incremental replication mode and the starting point of each data source:

    {{< copyable "shell-regular" >}}

    ```yaml
    name: task-test                      # Task name. Must be globally unique.
    task-mode: incremental               # Task mode. The "incremental" mode only performs incremental data replication.

    # Configures the target TiDB database.
    target-database:                     # The target database instance.
      host: "${host}"                    # e.g.: 127.0.0.1
      port: 4000
      user: "root"
      password: "${password}"            # It is recommended to use `dmctl encrypt` to encrypt the plaintext password before using it.

    # Use block and allow lists to specify the tables to be replicated.
    block-allow-list:                    # The collection of filtering rules that matches the tables in the source database instance. If the DM version is earlier than v2.0.0-beta.2, use black-white-list.
      bw-rule-1:                         # The block-allow-list configuration item ID.
        do-dbs: ["${db-name}"]           # Name of databases to be replicated.

    # Configures the data source.
    mysql-instances:
      - source-id: "mysql-01"            # Data source ID, i.e., source-id in source1.yaml
        block-allow-list: "bw-rule-1"    # You can use the block-allow-list configuration above.
        # syncer-config-name: "global"    # You can use the syncers incremental data configuration below.
        meta:                            # The position where the binlog replication starts when `task-mode` is `incremental` and the downstream database checkpoint does not exist. If the checkpoint exists, the checkpoint is used. If neither the `meta` configuration item nor the downstream database checkpoint exists, the migration starts from the latest binlog position of the upstream.
          # binlog-name: "mysql-bin.000004"  # The binlog position recorded in "Step 1. Export all data from MySQL". If the upstream database service is configured to switch master between different nodes automatically, GTID mode is required.
          # binlog-pos: 109227
          binlog-gtid: "09bec856-ba95-11ea-850a-58f2b4af5188:1-9"

    # (Optional) If you need to incrementally replicate data that has already been migrated in the full data migration, you need to enable the safe mode to avoid the incremental data replication error.
    # This scenario is common in the following case: the full migration data does not belong to the data source's consistency snapshot, and after that, DM starts to replicate incremental data from a position earlier than the full migration.
    # syncers:            # The running configurations of the sync processing unit.
    #   global:           # Configuration name.
    #     safe-mode: true # If this field is set to true, DM changes INSERT of the data source to REPLACE for the target database, and changes UPDATE of the data source to DELETE and REPLACE for the target database. This is to ensure that when the table schema contains a primary key or unique index, DML statements can be imported repeatedly. In the first minute of starting or resuming an incremental replication task, DM automatically enables the safe mode.
    ```

    The YAML above is the minimum configuration required for the migration task. For more configuration items, refer to [DM Advanced Task Configuration File](/dm/task-configuration-file-full.md).

    Before you start the migration task, to reduce the probability of errors, it is recommended to confirm that the configuration meets the requirements of DM by running the `check-task` command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup dmctl --master-addr ${advertise-addr} check-task task.yaml
    ```

2. Start the migration task by running the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup dmctl --master-addr ${advertise-addr} start-task task.yaml
    ```

    The parameters used in the command above are described as follows:

    |Parameter              |Description    |
    |-                      |-              |
    |`--master-addr`        |The {advertise-addr} of any DM-master in the cluster where `dmctl` is to be connected, e.g.: 172.16.10.71:8261|
    |`start-task`           |Starts the migration task.|

    If the task fails to start, check the prompt message and fix the configuration. After that, you can re-run the command above to start the task.

    If you encounter any problem, refer to [DM error handling](/dm/dm-error-handling.md) and [DM FAQ](/dm/dm-faq.md).

### Check the migration task status

To learn whether the DM cluster has an ongoing migration task and view the task status, run the `query-status` command using `tiup dmctl`:

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

For a detailed interpretation of the results, refer to [Query Status](/dm/dm-query-status.md).

### Monitor the task and view logs

To view the history status of the migration task and other internal metrics, take the following steps.

If you have deployed Prometheus, Alertmanager, and Grafana when you deployed DM using TiUP, you can access Grafana using the IP address and port specified during the deployment. You can then select DM dashboard to view DM-related monitoring metrics.

When DM is running, DM-worker, DM-master, and dmctl print the related information in logs. The log directories of these components are as follows:

- DM-master: specified by the DM-master process parameter `--log-file`. If you deploy DM using TiUP, the log directory is `/dm-deploy/dm-master-8261/log/` by default.
- DM-worker: specified by the DM-worker process parameter `--log-file`. If you deploy DM using TiUP, the log directory is `/dm-deploy/dm-worker-8262/log/` by default.

## What's next

- [Pause a Data Migration Task](/dm/dm-pause-task.md)
- [Resume a Data Migration Task](/dm/dm-resume-task.md)
- [Stop a Data Migration Task](/dm/dm-stop-task.md)
- [Export and Import Data Sources and Task Configuration of Clusters](/dm/dm-export-import-config.md)
- [Handle Failed DDL Statements](/dm/handle-failed-ddl-statements.md)
