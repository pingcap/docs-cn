---
title: Use BR to Back up and Restore Data
summary: Learn how to back up and restore data of the TiDB cluster using BR.
category: how-to
---

# Use BR to Back up and Restore Data

Backup & Restore (BR) is a command-line tool for distributed backup and restoration of the TiDB cluster data. Compared with [`mydumper`/`loader`](/v3.1/how-to/maintain/backup-and-restore/mydumper-loader.md), BR is more suitable for scenarios of huge data volume. This document describes the BR command line, detailed use examples, best practices, restrictions, and introduces the implementation principles of BR.

## Command-line description

A `br` command consists of sub-commands, options, and parameters.

* Sub-command: the characters without `-` or `--`.
* Option: the characters that start with `-` or `--`.
* Parameter: the characters that immediately follow behind and are passed to the sub-command or the option.

This is a complete `br` command:

{{< copyable "shell-regular" >}}

```shell
br backup full --pd "${PDIP}:2379" -s "local:///tmp/backup"
```

Explanations for the above command are as follows:

* `backup`: the sub-command of `br`.
* `full`: the sub-command of `backup`.
* `-s` (or `--storage`): the option that specifies the path where the backup files are stored.
* `"local:///tmp/backup"`: the parameter of `-s`. `/tmp/backup` is the path in the local disk where the backup files are stored.
* `--pd`: the option that specifies the Placement Driver (PD) service address.
* `"${PDIP}:2379"`: the parameter of `--pd`.

### Sub-commands

A `br` command consists of multiple layers of sub-commands. Currently, BR has the following three sub-commands:

* `br backup`: used to back up the data of the TiDB cluster.
* `br restore`: used to restore the data of the TiDB cluster.
* `br version`: used to check the version of BR.

Each of the above three sub-commands might still include the following three sub-commands to specify the scope of an operation:

* `full`: used to back up or restore all the cluster data.
* `db`: used to restore the specified database of the cluster.
* `table`: used to back up or restore a single table in the specified database of the cluster.

### Common options

* `--pd`: used for connection, specifying the PD server address. For example, `"${PDIP}:2379"`.
* `-h` (or `--help`): used to get help on all sub-commands. For example, `br backup --help`.
* `--ca`: specifies the path to the trusted CA certificate in the PEM format.
* `--cert`: specifies the path to the SSL certificate in the PEM format.
* `--key`: specifies the path to the SSL certificate key in the PEM format.
* `--status-addr`: specifies the listening address through which BR provides statistics to Prometheus.

## Back up cluster data

To back up the cluster data, use the `br backup` command. You can add the `full` or `table` sub-command to specify the scope of your backup operation: the whole cluster or a single table.

If the backup time might exceed the [`tikv_gc_life_time`](/v3.1/reference/garbage-collection/configuration.md#tikv_gc_life_time) configuration which is `10m0s` by default, increase the value of this configuration.

For example, set `tikv_gc_life_time` to `720h`:

{{< copyable "sql" >}}

```sql
mysql -h${TiDBIP} -P4000 -u${TIDB_USER} ${password_str} -Nse \
    "update mysql.tidb set variable_value='720h' where variable_name='tikv_gc_life_time'";
```

### Back up all the cluster data

To back up all the cluster data, execute the `br backup full` command. To get help on this command, execute `br backup full -h` or `br backup full --help`.

**Usage example:**

Back up all the cluster data to the `/tmp/backup` path of each TiKV node and write the `backupmeta` file to this path.

{{< copyable "shell-regular" >}}

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --ratelimit 120 \
    --concurrency 4 \
    --log-file backupfull.log
```

Explanations for some options in the above command are as follows:

* `--ratelimit`: specifies the maximum speed at which a backup operation is performed (MiB/s) on each TiKV node.
* `--concurrency`: sets an upper limit on the number of concurrent operations on each TiKV node.
* `--log-file`: specifies writing the BR log to the `backupfull.log` file.

A progress bar is displayed in the terminal during the backup. When the progress bar advances to 100%, the backup is complete. Then the BR also checks the backup data to ensure data safety. The progress bar is displayed as follows:

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --ratelimit 120 \
    --concurrency 4 \
    --log-file backupfull.log
Full Backup <---------/................................................> 17.12%.
```

### Back up data of a single table

To back up the data of a single table in the cluster, execute the `br backup table` command. To get help on this command, execute `br backup table -h` or `br backup table --help`.

**Usage example:**

Back up the data of the `test.usertable` table to the `/tmp/backup` path on each TiKV node and write the `backupmeta` file to this path.

{{< copyable "shell-regular" >}}

```shell
br backup table \
    --pd "${PDIP}:2379" \
    --db test \
    --table usertable \
    --storage "local:///tmp/backup" \
    --ratelimit 120 \
    --concurrency 4 \
    --log-file backuptable.log
```

The `table` sub-command has two options:

* `--db`: specifies the database name
* `--table`: specifies the table name.

For descriptions of other options, see [Back up all cluster data](#back-up-all-cluster-data).

A progress bar is displayed in the terminal during the backup operation. When the progress bar advances to 100%, the backup is complete. Then the BR also checks the backup data to ensure data safety.

## Restore cluster data

To restore the cluster data, use the `br restore` command. You can add the `full`, `db` or `table` sub-command to specify the scope of your restoration: the whole cluster, a database or a single table.

> **Note:**
>
> If the backed up cluster does not have a network storage, before the restoration, copy the backup SST files to the path specified by `--storage` on each TiKV node.

### Restore all the backup data

To restore all the backup data to the cluster, execute the `br restore full` command. To get help on this command, execute `br restore full -h` or `br restore full --help`.

**Usage example:**

Restore all the backup data in the `/tmp/backup` path to the cluster.

{{< copyable "shell-regular" >}}

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --concurrency 128 \
    --log-file restorefull.log
```

Explanations for some options in the above command are as follows:

* `--concurrency`: specifies how many sub-tasks can be performed concurrently in a restoration operation.
* `--log-file`: specifies writing the BR log to the `restorefull.log` file.

A progress bar is displayed in the terminal during the restoration. When the progress bar advances to 100%, the restoration is complete. Then the BR also checks the backup data to ensure data safety.

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --log-file restorefull.log
Full Restore <---------/...............................................> 17.12%.
```

### Restore a database

To restore a database to the cluster, execute the `br restore db` command. To get help on this command, execute `br restore db -h` or `br restore db --help`.

**Usage example:**

Restore a database backed up in the `/tmp/backup` path to the cluster.

{{< copyable "shell-regular" >}}

```shell
br restore db \
    --pd "${PDIP}:2379" \
    --db "test" \
    --storage "local:///tmp/backup" \
    --log-file restorefull.log
```

In the above command, `--db` specifies the name of the database to be restored. For descriptions of other options, see [Restore all backup data](#restore-all-backup-data).

### Restore a table

To restore a single table to the cluster, execute the `br restore table` command. To get help on this command, execute `br restore table -h` or `br restore table --help`.

**Usage example:**

Restore a table backed up in the `/tmp/backup` path to the cluster.

{{< copyable "shell-regular" >}}

```shell
br restore table \
    --pd "${PDIP}:2379" \
    --db "test" \
    --table "usertable" \
    --storage "local:///tmp/backup" \
    --log-file restorefull.log
```

In the above command, `--table` specifies the name of the table to be restored. For descriptions of other options, see [Restore all backup data](#restore-all-backup-data) and [Restore a database](#restore-a-database).

## Best practices

- It is recommended that you mount a shared storage (for example, NFS) on the backup path specified by `-s`, to make it easier to collect and manage backup files.
- It is recommended that you use a storage hardware with high throughput, because the throughput of a storage hardware limits the backup and restoration speed.
- It is recommended that you perform the backup operation during off-peak hours to minimize the impact on applications.
- To speed up the restoration, use pd-ctl to remove the schedulers related to scheduling before the restoration and add back these removed schedulers after the restoration.

    Remove schedulers:

    {{< copyable "shell-regular" >}}

    ```shell
    ./pd-ctl -u ${PDIP}:2379 scheduler remove balance-hot-region-scheduler
    ./pd-ctl -u ${PDIP}:2379 scheduler remove balance-leader-scheduler
    ./pd-ctl -u ${PDIP}:2379 scheduler remove balance-region-scheduler
    ```

    Add schedulers:

    {{< copyable "shell-regular" >}}

    ```shell
    ./pd-ctl -u ${PDIP}:2379 scheduler add balance-hot-region-scheduler
    ./pd-ctl -u ${PDIP}:2379 scheduler add balance-leader-scheduler
    ./pd-ctl -u ${PDIP}:2379 scheduler add balance-region-scheduler
    ```

## Usage restrictions

- BR only supports TiDB v3.1 and later versions.
- TiDB cannot perform backup operation when executing DDL operations.
- Currently, TiDB does not support backing up and restoring partitioned tables.
- Currently, you can perform restoration only on new clusters.

## Examples

This section shows how to back up and restore the data of an existing cluster. You can estimate the performance of backup and restoration based on machine performance, configuration and data volume.

### Data volume and machine configuration

Suppose that the backup and restoration operations are performed on 10 tables in the TiKV cluster, each table with 5 million rows of data. The total data volume is 35 GB.

```sql
MySQL [sbtest]> show tables;
+------------------+
| Tables_in_sbtest |
+------------------+
| sbtest1          |
| sbtest10         |
| sbtest2          |
| sbtest3          |
| sbtest4          |
| sbtest5          |
| sbtest6          |
| sbtest7          |
| sbtest8          |
| sbtest9          |
+------------------+

MySQL [sbtest]> select count(*) from sbtest1;
+----------+
| count(*) |
+----------+
|  5000000 |
+----------+
1 row in set (1.04 sec)
```

The table structure is as follows:

```sql
CREATE TABLE `sbtest1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `k` int(11) NOT NULL DEFAULT '0',
  `c` char(120) NOT NULL DEFAULT '',
  `pad` char(60) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `k_1` (`k`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=5138499
```

Suppose that 4 TiKV nodes is used, each with the following configuration:

| CPU      | Memory | Disk | Number of replicas |
| :-------- | :------ | :---- | :------------------ |
| 16 cores | 32 GB  | SSD  | 3                  |

### Backup

Before the backup operation, check the following two items:

- You have set `tikv_gc_life_time` set to a larger value so that the backup operation will not be interrupted because of data loss.
- No DDL statement is being executed on the TiDB cluster.

Then execute the following command to back up all the cluster data:

{{< copyable "shell-regular" >}}

```shell
bin/br backup full -s local:///tmp/backup --pd "${PDIP}:2379" --log-file backup.log
```

```
[INFO] [client.go:288] ["Backup Ranges"] [take=2m25.801322134s]
[INFO] [schema.go:114] ["backup checksum finished"] [take=4.842154366s]
```

### Restoration

Before the restoration, make sure that the TiKV cluster to be restored is a new cluster.

Then execute the following command to restore all the cluster data:

{{< copyable "shell-regular" >}}

```shell
bin/br restore full -s local:///tmp/backup --pd "${PDIP}:2379" --log-file restore.log
```

```
[INFO] [client.go:345] [RestoreAll] [take=2m8.907369337s]
[INFO] [client.go:435] ["Restore Checksum"] [take=6.385818026s]
```

## Implementation principles

BR sends the backup and restoration commands to each TiKV node. After receiving these commands, TiKV performs the corresponding backup and restoration operations. Each TiKV node has a path in which the backup files generated in the backup operation are stored and from which the stored backup files are read during the restoration.

### Backup principle

When BR performs a backup operation, it first obtains the following information from PD:

- The current TS (timestamp) as the time of the backup snapshot
- The TiKV node information of the current cluster

According to these information, BR starts a TiDB instance internally to obtain the database or table information corresponding to the TS, and filters out the system databases (`information_schema`, `performance_schema`, `mysql`) at the same time.

According to the backup sub-command, BR adopts the following two types of backup logic:

- Full backup: BR traverses all the tables and constructs the KV range to be backed up according to each table.
- Single table backup: BR constructs the KV range to be backed up according a single table.

Finally, BR collects the KV range to be backed up and sends the complete backup request to the TiKV node of the cluster.

The structure of the request:

```
backup.BackupRequest{
    ClusterId:    clusterID,   // The cluster ID.
    StartKey:     startKey,    // The starting key of the backup (backed up).
    EndKey:       endKey,      // The ending key of the backup (not backed up).
    StartVersion: backupTS,    // The backup snapshot time.
    ...
    Path:         path,        // The path where backup files are stored.
    RateLimit:    rateLimit,   // Backup speed (MB/s).
    Concurrency:  concurrency, // The number of threads for the backup operation (4 by default).
}
```

After receiving the backup request, the TiKV node traverses all Region leaders on the node to find the Regions that overlap with the KV ranges in this request. The TiKV node backs up some or all of the data within the range, and generates the corresponding SST file (named in the format of `storeID_regionID_regionEpoch_tableID`) in the backup path.

After finishing backing up the data of the corresponding Region, the TiKV node returns the metadata to BR. BR collects the metadata and stores it in the `backupMeta` file which is used for restoration.

If checksum is enabled when you execute the backup command, BR calculates the checksum of each backed up table for data check.

### Restoration principle

During the data restoration process, BR performs the following tasks in order:

1. It parses the `backupMeta` file in the backup path, and then starts a TiDB instance internally to create the corresponding databases and tables based on the parsed information.

2. It aggregates the parsed SST files according to the tables and `GroupBy`.

3. It pre-splits Regions according to the key range of the SST file so that every Region corresponds to at least one SST file.

4. It traverses each table to be restored and the SST file corresponding to each tables.

5. It finds the Region corresponding to the SST file and sends a request to the corresponding TiKV node for downloading the file. Then it sends a request for loading the file after the file is successfully downloaded.

After TiKV receives the request to load the SST file, TiKV uses the Raft mechanism to ensure the strong consistency of the SST data. After the downloaded SST file is loaded successfully, the file is deleted asynchronously.

After the restoration operation is completed, BR performs a checksum calculation on the restored data to compare the stored data with the backed up data.

![br-arch](/media/br-arch.png)
