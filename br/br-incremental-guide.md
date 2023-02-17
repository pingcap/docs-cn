---
title: TiDB Incremental Backup and Restore Guide
summary: Learns about how to perform incremental backup and restore in TiDB.
---

# TiDB Incremental Backup and Restore Guide

Incremental data of a TiDB cluster is differentiated data between the starting snapshot and the end snapshot of time period, and the DDLs generated during this period. Compared with full (snapshot) backup data, incremental data is smaller and therefore it is a supplementary to snapshot backup, which reduces the volume of backup data. To perform incremental backup, ensure that MVCC data generated within the specified period is not garbage collected by the [TiDB GC mechanism](/garbage-collection-overview.md). For example, to perform incremental backup hourly, you must set [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) to a value greater than 1 hour.

> **Warning:**
>
> Development for this feature has stopped. It is recommended that you use [log backup and PITR](/br/br-pitr-guide.md) as an alternative.

## Back up incremental data

To back up incremental data, run the `br backup` command with **the last backup timestamp** `--lastbackupts` specified. In this way, br command-line tool automatically backs up incremental data generated between `lastbackupts` and the current time. To get `--lastbackupts`, run the `validate` command. The following is an example:

```shell
LAST_BACKUP_TS=`tiup br validate decode --field="end-version" --storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"| tail -n1`
```

The following command backs up the incremental data between `(LAST_BACKUP_TS, current PD timestamp]` and the DDLs generated during this time period:

```shell
tiup br backup full --pd "${PD_IP}:2379" \
--storage "s3://backup-101/snapshot-202209081330/incr?access-key=${access-key}&secret-access-key=${secret-access-key}" \
--lastbackupts ${LAST_BACKUP_TS} \
--ratelimit 128
```

- `--lastbackupts`: The last backup timestamp.
- `--ratelimit`: The maximum speed **per TiKV** performing backup tasks (in MiB/s).
- `storage`: The storage path of backup data. You need to save the incremental backup data under a different path from the previous snapshot backup. In the preceding example, incremental backup data is saved in the `incr` directory under the full backup data. For details, see [Backup storage URI configuration](/br/backup-and-restore-storages.md#uri-format).

## Restore incremental data

When restoring incremental data, make sure that all the data backed up before `LAST_BACKUP_TS` has been restored to the target cluster. Also, because incremental restore updates data, you need to ensure that there are no other writes during the restore. Otherwise, conflicts might occur.

The following command restores the full backup data stored in the `backup-101/snapshot-202209081330` directory:

```shell
tiup br restore full --pd "${PD_IP}:2379" \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

The following command restores the incremental backup data stored in the `backup-101/snapshot-202209081330/incr` directory:

```shell
tiup br restore full --pd "${PD_IP}:2379" \
--storage "s3://backup-101/snapshot-202209081330/incr?access-key=${access-key}&secret-access-key=${secret-access-key}"
```
