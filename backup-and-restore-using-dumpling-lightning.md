---
title: Back up and Restore Data Using Dumpling and TiDB Lightning
summary: Learn how to use Dumpling and TiDB Lightning to back up and restore full data of TiDB.
---

# Back up and Restore Data Using Dumpling and TiDB Lightning

This document introduces how to use Dumpling and TiDB Lightning to back up and restore full data of TiDB.

If you need to back up a small amount of data (for example, less than 50 GiB) and do not require high backup speed, you can use [Dumpling](/dumpling-overview.md) to export data from the TiDB database and then use [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) to restore the data into another TiDB database. 

If you need to back up larger databases, the recommended method is to use [BR](/br/backup-and-restore-overview.md). Note that Dumpling can be used to export large databases, but BR is a better tool for that.

## Requirements

- Install Dumpling:

    ```shell
    tiup install dumpling
    ```

- Install TiDB Lightning:

    ```shell
    tiup install tidb-lightning
    ```

- [Grant the source database privileges required for Dumpling](/dumpling-overview.md#export-data-from-tidb-or-mysql)
- [Grant the target database privileges required for TiDB Lightning](/tidb-lightning/tidb-lightning-requirements.md#privileges-of-the-target-database)

## Resource requirements

**Operating system**: The example in this document uses fresh CentOS 7 instances. You can deploy a virtual machine either on your local host or in the cloud. Because TiDB Lightning consumes as much CPU resources as needed by default, it is recommended that you deploy it on a dedicated server. If this is not possible, you can deploy it on a single server together with other TiDB components (for example, `tikv-server`) and then configure `region-concurrency` to limit the CPU usage from TiDB Lightning. Usually, you can configure the size to 75% of the logical CPU.

**Memory and CPU**: Because TiDB Lightning consumes high resources, it is recommended to allocate more than 64 GiB of memory and more than 32 CPU cores. To get the best performance, make sure that the CPU core to memory (GiB) ratio is greater than 1:2.

**Disk space**:

It is recommended to use Amazon S3, Google Cloud Storage (GCS), or Azure Blob Storage as the external storage. With such a cloud storage, you can store backup files quickly without being limited by the disk space.

If you need to save data of one backup task to the local disk, note the following limitations:

- Dumpling requires a disk space that can store the whole data source (or to store all upstream tables to be exported). To calculate the required space, see [Downstream storage space requirements](/tidb-lightning/tidb-lightning-requirements.md#storage-space-of-the-target-database).
- During the import, TiDB Lightning needs temporary space to store the sorted key-value pairs. The disk space should be enough to hold the largest single table from the data source.

**Note**: It is difficult to calculate the exact data volume exported by Dumpling from MySQL, but you can estimate the data volume by using the following SQL statement to summarize the `DATA_LENGTH` field in the `information_schema.tables` table:

```sql
-- Calculate the size of all schemas
SELECT
  TABLE_SCHEMA,
  FORMAT_BYTES(SUM(DATA_LENGTH)) AS 'Data Size',
  FORMAT_BYTES(SUM(INDEX_LENGTH)) 'Index Size'
FROM
  information_schema.tables
GROUP BY
  TABLE_SCHEMA;

-- Calculate the 5 largest tables
SELECT 
  TABLE_NAME,
  TABLE_SCHEMA,
  FORMAT_BYTES(SUM(data_length)) AS 'Data Size',
  FORMAT_BYTES(SUM(index_length)) AS 'Index Size',
  FORMAT_BYTES(SUM(data_length+index_length)) AS 'Total Size'
FROM
  information_schema.tables
GROUP BY
  TABLE_NAME,
  TABLE_SCHEMA
ORDER BY
  SUM(DATA_LENGTH+INDEX_LENGTH) DESC
LIMIT
  5;
```

### Disk space for the target TiKV cluster

The target TiKV cluster must have enough disk space to store the imported data. In addition to [the standard hardware requirements](/hardware-and-software-requirements.md), the storage space of the target TiKV cluster must be larger than **the size of the data source x [the number of replicas](/faq/manage-cluster-faq.md#is-the-number-of-replicas-in-each-region-configurable-if-yes-how-to-configure-it) x 2**. For example, if the cluster uses 3 replicas by default, the target TiKV cluster must have a storage space larger than 6 times the size of the data source. The formula has x 2 because:

- Index might take extra space.
- RocksDB has a space amplification effect.

## Use Dumpling to back up full data

1. Run the following command to export full data from TiDB to `s3://my-bucket/sql-backup` in Amazon S3:

    ```shell
    tiup dumpling -h ${ip} -P 3306 -u root -t 16 -r 200000 -F 256MiB -B my_db1 -f 'my_db1.table[12]' -o 's3://my-bucket/sql-backup'
    ```

    Dumpling exports data in SQL files by default. You can specify a different file format by adding the `--filetype` option.

    For more configurations of Dumpling, see [Option list of Dumpling](/dumpling-overview.md#option-list-of-dumpling).

2. After the export is completed, you can view the backup files in the directory `s3://my-bucket/sql-backup`.

## Use TiDB Lightning to restore full data

1. Edit the `tidb-lightning.toml` file to import full data backed up using Dumpling from `s3://my-bucket/sql-backup` to the target TiDB cluster:

    ```toml
    [lightning]
    # log
    level = "info"
    file = "tidb-lightning.log"

    [tikv-importer]
    # "local": Default backend. The local backend is recommended to import large volumes of data (1 TiB or more). During the import, the target TiDB cluster cannot provide any service.
    # "tidb": The "tidb" backend is recommended to import data less than 1 TiB. During the import, the target TiDB cluster can provide service normally. For more information on the backends, refer to https://docs.pingcap.com/tidb/stable/tidb-lightning-backends.
    backend = "local"
    # Sets the temporary storage directory for the sorted Key-Value files. The directory must be empty, and the storage space must be greater than the size of the dataset to be imported. For better import performance, it is recommended to use a directory different from `data-source-dir` and use flash storage, which can use I/O exclusively.
    sorted-kv-dir = "${sorted-kv-dir}"

    [mydumper]
    # The data source directory. The same directory where Dumpling exports data in "Use Dumpling to back up full data".
    data-source-dir = "${data-path}" #  A local path or S3 path. For example, 's3://my-bucket/sql-backup'

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

2. Start the import by running `tidb-lightning`. If you launch the program directly in the command line, the process might exit unexpectedly after receiving a `SIGHUP` signal. In this case, it is recommended to run the program using a `nohup` or `screen` tool. For example:

    If you import data from S3, pass the SecretKey and AccessKey that have access to the S3 storage path as environment variables to the TiDB Lightning node. You can also read the credentials from `~/.aws/credentials`.

    ```shell
    export AWS_ACCESS_KEY_ID=${access_key}
    export AWS_SECRET_ACCESS_KEY=${secret_key}
    nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out 2>&1 &
    ```

3. After the import starts, you can `grep` the keyword `progress` in the log to check the progress of the import. The progress is updated every 5 minutes by default.

4. After TiDB Lightning completes the import, it exits automatically. Check whether `tidb-lightning.log` contains `the whole procedure completed` in the last lines. If yes, the import is successful. If no, the import encounters an error. Address the error as instructed in the error message.

> **Note:**
>
> Whether the import is successful or not, the last line of the log shows `tidb lightning exit`. It means that TiDB Lightning exits normally, but does not necessarily mean that the import is successful.

If the import fails, refer to [TiDB Lightning FAQ](/tidb-lightning/tidb-lightning-faq.md) for troubleshooting.
