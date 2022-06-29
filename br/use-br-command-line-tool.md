---
title: Use BR Command-line for Backup and Restoration
summary: Learn how to use the BR command line to back up and restore cluster data.
---

# Use BR Command-line for Backup and Restoration

This document describes how to back up and restore TiDB cluster data using the BR command line.

Make sure you have read [BR Tool Overview](/br/backup-and-restore-overview.md), especially [Usage restrictions](/br/backup-and-restore-overview.md#usage-restrictions) and [Some tips](/br/backup-and-restore-overview.md#some-tips).

## BR command-line description

A `br` command consists of sub-commands, options, and parameters.

* Sub-command: the characters without `-` or `--`.
* Option: the characters that start with `-` or `--`.
* Parameter: the characters that immediately follow behind and are passed to the sub-command or the option.

This is a complete `br` command:

{{< copyable "shell-regular" >}}

```shell
`br backup full --pd "${PDIP}:2379" -s "s3://backup-data/2022-01-30/"`
```

Explanations for the above command are as follows:

* `backup`: the sub-command of `br`.
* `full`: the sub-command of `backup`.
* `-s` (or `--storage`): the option that specifies the path where the backup files are stored.
* `"s3://backup-data/2022-01-30/"`: the parameter of `-s`, indicating that backup data is stored to the `2022-01-30/` directory in the `backup-data` bucket of Amazon S3.
* `--pd`: the option that specifies the Placement Driver (PD) service address.
* `"${PDIP}:2379"`: the parameter of `--pd`.

### Sub-commands

A `br` command consists of multiple layers of sub-commands. Currently, BR has the following sub-commands:

* `br backup`: used to back up the data of the TiDB cluster.
* `br restore`: used to restore the data of the TiDB cluster.

Each of the above sub-commands might still include the following sub-commands to specify the scope of an operation:

* `full`: used to back up or restore all the cluster data.
* `db`: used to back up or restore the specified database of the cluster.
* `table`: used to back up or restore a single table in the specified database of the cluster.

### Common options

* `--pd`: used for connection, specifying the PD server address. For example, `"${PDIP}:2379"`.
* `-h` (or `--help`): used to get help on all sub-commands. For example, `br backup --help`.
* `-V` (or `--version`): used to check the version of BR.
* `--ca`: specifies the path to the trusted CA certificate in the PEM format.
* `--cert`: specifies the path to the SSL certificate in the PEM format.
* `--key`: specifies the path to the SSL certificate key in the PEM format.
* `--status-addr`: specifies the listening address through which BR provides statistics to Prometheus.

## Examples of using BR command-line to back up cluster data

To back up cluster data, run the `br backup` command. You can add the `full` or `table` sub-command to specify the scope of your backup operation: the whole cluster or a single table.

- [Back up TiDB cluster snapshots](/br/br-usage-backup.md#back-up-tidb-cluster-snapshots)
- [Back up a database](/br/br-usage-backup.md#back-up-a-database)
- [Back up a table](/br/br-usage-backup.md#back-up-a-table)
- [Back up multiple tables with table filter](/br/br-usage-backup.md#back-up-multiple-tables-with-table-filter)
- [Back Up data on Amazon S3 using BR](/br/backup-storage-S3.md)
- [Back up data on Google Cloud Storage using BR](/br/backup-storage-gcs.md)
- [Back up data on Azure Blob Storage using BR](/br/backup-storage-azblob.md)
- [Back up incremental data](/br/br-usage-backup.md#back-up-incremental-data)
- [Encrypt data during backup](/br/br-usage-backup.md#encrypt-backup-data-at-the-backup-end)

## Examples of using BR command-line to restore cluster data

To restore cluster data, run the `br restore` command. You can add the `full`, `db` or `table` sub-command to specify the scope of your restoration: the whole cluster, a database or a single table.

- [Restore TiDB cluster snapshots](/br/br-usage-restore.md#restore-tidb-cluster-snapshots)
- [Restore a database](/br/br-usage-restore.md#restore-a-database)
- [Restore a table](/br/br-usage-restore.md#restore-a-table)
- [Restore multiple tables with table filter](/br/br-usage-restore.md#restore-multiple-tables-with-table-filter)
- [Restore data on Amazon S3 using BR](/br/backup-storage-S3.md)
- [Restore data on Google Cloud Storage using BR](/br/backup-storage-gcs.md)
- [Restore data on Azure Blob Storage using BR](/br/backup-storage-azblob.md)
- [Restore incremental data](/br/br-usage-restore.md#restore-incremental-data)
- [Restore encrypted backup data](/br/br-usage-restore.md#restore-encrypted-backup-data)
