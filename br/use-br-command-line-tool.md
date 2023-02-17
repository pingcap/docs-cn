---
title: br Command-line Manual
summary: Learn about the description, options, and usage of the br command-line tool.
---

# br Command-line Manual

This document describes the definition, components, and common options of `br` commands, and how to perform snapshot backup and restore, and log backup and point-in-time recovery (PITR) using `br` commands.

## `br` command-line description

A `br` command consists of sub-commands, options, and parameters. A sub-command is the characters without `-` or `--`. An option is the characters that start with `-` or `--`. A parameter is the characters that immediately follow behind and are passed to the sub-command or the option.

The following is a complete `br` command:

```shell
br backup full --pd "${PD_IP}:2379" \
--storage "s3://backup-data/snapshot-202209081330/"
```

Explanations for the preceding command are as follows:

* `backup`: the sub-command of `br`.
* `full`: the sub-command of `br backup`.
* `-s` (or `--storage`): the option that specifies the path where the backup files are stored. `"s3://backup-data/snapshot-202209081330/"` is the parameter of `-s`.
* `--pd`: the option that specifies the PD service address. `"${PD_IP}:2379"` is the parameter of `--pd`.

### Commands and sub-commands

A `br` command consists of multiple layers of sub-commands. Currently, br command-line tool has the following sub-commands:

* `br backup`: used to back up the data of the TiDB cluster.
* `br log`: used to start and manage log backup tasks.
* `br restore`: used to restore backup data of the TiDB cluster.

`br backup` and `br restore` include the following sub-commands:

* `full`: used to back up or restore all the cluster data.
* `db`: used to back up or restore a specified database of the cluster.
* `table`: used to back up or restore a single table in the specified database of the cluster.

### Common options

* `--pd`: specifies the PD service address. For example, `"${PD_IP}:2379"`.
* `-s` (or `--storage`): specifies the path where the backup files are stored. Amazon S3, Google Cloud Storage (GCS), Azure Blob Storage, and NFS are supported to store backup data. For more details, refer to [URI format of backup storages](/br/backup-and-restore-storages.md#uri-format).
* `--ca`: specifies the path to the trusted CA certificate in the PEM format.
* `--cert`: specifies the path to the SSL certificate in the PEM format.
* `--key`: specifies the path to the SSL certificate key in the PEM format.
* `--status-addr`: specifies the listening address through which `br` provides statistics to Prometheus.

## Commands of full backup

To back up cluster data, run the `br backup` command. You can add the `full` or `table` sub-command to specify the scope of your backup operation: the whole cluster (`full`) or a single table (`table`).

- [Back up TiDB cluster snapshots](/br/br-snapshot-manual.md#back-up-cluster-snapshots)
- [Back up a database](/br/br-snapshot-manual.md#back-up-a-database)
- [Back up a table](/br/br-snapshot-manual.md#back-up-a-table)
- [Back up multiple tables with table filter](/br/br-snapshot-manual.md#back-up-multiple-tables-with-table-filter)
- [Encrypt snapshots](/br/backup-and-restore-storages.md#server-side-encryption)

## Commands of log backup

To start log backup and manage log backup tasks, run the `br log` command.

- [Start a log backup task](/br/br-pitr-manual.md#start-a-backup-task)
- [Query the backup status](/br/br-pitr-manual.md#query-the-backup-status)
- [Pause and resume a log backup task](/br/br-pitr-manual.md#pause-and-resume-a-backup-task)
- [Stop and restart a log backup task](/br/br-pitr-manual.md#stop-and-restart-a-backup-task)
- [Clean up the backup data](/br/br-pitr-manual.md#clean-up-backup-data)
- [View the backup metadata](/br/br-pitr-manual.md#view-the-backup-metadata)

## Commands of restoring backup data

To restore cluster data, run the `br restore` command. You can add the `full`, `db`, or `table` sub-command to specify the scope of your restore: the whole cluster (`full`), a single database (`db`), or a single table (`table`).

- [Point-in-time recovery](/br/br-pitr-manual.md#restore-to-a-specified-point-in-time-pitr)
- [Restore cluster snapshots](/br/br-snapshot-manual.md#restore-cluster-snapshots)
- [Restore a database](/br/br-snapshot-manual.md#restore-a-database)
- [Restore a table](/br/br-snapshot-manual.md#restore-a-table)
- [Restore multiple tables with table filter](/br/br-snapshot-manual.md#restore-multiple-tables-with-table-filter)
- [Restore encrypted snapshots](/br/br-snapshot-manual.md#restore-encrypted-snapshots)
