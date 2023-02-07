---
title: TiDB Log Backup and PITR Guide
summary: Learns about how to perform log backup and PITR in TiDB.
aliases: ['/tidb/dev/pitr-usage']
---

# TiDB Log Backup and PITR Guide

A full backup (snapshot backup) contains the full cluster data at a certain point, while TiDB log backup can back up data written by applications to a specified storage in a timely manner. If you want to choose the restore point as required, that is, to perform point-in-time recovery (PITR), you can [start log backup](#start-log-backup) and [run full backup regularly](#run-full-backup-regularly).

Before you back up or restore data using the br command-line tool (hereinafter referred to as `br`), you need to [install `br`](/br/br-use-overview.md#deploy-and-use-br) first.

## Back up TiDB cluster

### Start log backup

> **Note:**
>
> - The following examples assume that Amazon S3 access keys and secret keys are used to authorize permissions. If IAM roles are used to authorize permissions, you need to set `--send-credentials-to-tikv` to `false`.
> - If other storage systems or authorization methods are used to authorize permissions, adjust the parameter settings according to [Backup Storages](/br/backup-and-restore-storages.md).

To start a log backup, run `br log start`. A cluster can only run one log backup task each time.

```shell
tiup br log start --task-name=pitr --pd "${PD_IP}:2379" \
--storage 's3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}"'
```

After the log backup task starts, it runs in the background of the TiDB cluster until you stop it manually. During this process, the TiDB change logs are regularly backed up to the specified storage in small batches. To query the status of the log backup task, run the following command:

```shell
tiup br log status --task-name=pitr --pd "${PD_IP}:2379"
```

Expected output:

```
● Total 1 Tasks.
> #1 <
    name: pitr
    status: ● NORMAL
    start: 2022-05-13 11:09:40.7 +0800
      end: 2035-01-01 00:00:00 +0800
    storage: s3://backup-101/log-backup
    speed(est.): 0.00 ops/s
checkpoint[global]: 2022-05-13 11:31:47.2 +0800; gap=4m53s
```

### Run full backup regularly

The snapshot backup can be used as a method of full backup. You can run `br backup full` to back up the cluster snapshot to the backup storage according to a fixed schedule (for example, every 2 days).

```shell
tiup br backup full --pd "${PD_IP}:2379" \
--storage 's3://backup-101/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}"'
```

## Run PITR

To restore the cluster to any point in time within the backup retention period, you can use `br restore point`. When you run this command, you need to specify the **time point you want to restore**, **the latest snapshot backup data before the time point**, and the **log backup data**. BR will automatically determine and read data needed for the restore, and then restore these data to the specified cluster in order.

```shell
br restore point --pd "${PD_IP}:2379" \
--storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}"' \
--full-backup-storage='s3://backup-101/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}"' \
--restored-ts '2022-05-15 18:00:00+0800'
```

During data restore, you can view the progress through the progress bar in the terminal. The restore is divided into two phases, full restore and log restore (restore meta files and restore KV files). After each phase is completed, `br` outputs information such as restore time and data size.

```shell
Full Restore <--------------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
*** ["Full Restore success summary"] ****** [total-take=xxx.xxxs] [restore-data-size(after-compressed)=xxx.xxx] [Size=xxxx] [BackupTS={TS}] [total-kv=xxx] [total-kv-size=xxx] [average-speed=xxx]
Restore Meta Files <--------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
Restore KV Files <----------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
*** ["restore log success summary"] [total-take=xxx.xx] [restore-from={TS}] [restore-to={TS}] [total-kv-count=xxx] [total-size=xxx]
```

## Clean up outdated data

As described in the [Usage Overview of TiDB Backup and Restore](/br/br-use-overview.md):

To perform PITR, you need to restore the full backup before the restore point, and the log backup between the full backup point and the restore point. Therefore, for log backups that exceed the backup retention period, you can use `br log truncate` to delete the backup before the specified time point. **It is recommended to only delete the log backup before the full snapshot**.

The following steps describe how to clean up backup data that exceeds the backup retention period:

1. Get the **last full backup** outside the backup retention period.
2. Use the `validate` command to get the time point corresponding to the backup. Assume that the backup data before 2022/09/01 needs to be cleaned, you should look for the last full backup before this time point and ensure that it will not be cleaned.

    ```shell
    FULL_BACKUP_TS=`tiup br validate decode --field="end-version" --storage "s3://backup-101/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}"| tail -n1`
    ```

3. Delete log backup data earlier than the snapshot backup `FULL_BACKUP_TS`:

    ```shell
    tiup br log truncate --until=${FULL_BACKUP_TS} --storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}"'
    ```

4. Delete snapshot data earlier than the snapshot backup `FULL_BACKUP_TS`:

    ```shell
    rm -rf s3://backup-101/snapshot-${date}
    ```

## Performance and impact of PITR

### Capabilities

- On each TiKV node, PITR can restore snapshot data at a speed of 280 GB/h and log data 30 GB/h.
- BR deletes outdated log backup data at a speed of 600 GB/h.

> **Note:**
>
> The preceding specifications are based on test results from the following two testing scenarios. The actual data might be different.
>
> - Snapshot data restore speed = Snapshot data size / (duration * the number of TiKV nodes)
> - Log data restore speed = Restored log data size / (duration * the number of TiKV nodes)

Testing scenario 1 (on [TiDB Cloud](https://tidbcloud.com)):

- The number of TiKV nodes (8 core, 16 GB memory): 21
- The number of Regions: 183,000
- New log data created in the cluster: 10 GB/h
- Write (INSERT/UPDATE/DELETE) QPS: 10,000

Testing scenario 2 (on-premises):

- The number of TiKV nodes (8 core, 64 GB memory): 6
- The number of Regions: 50,000
- New log data created in the cluster: 10 GB/h
- Write (INSERT/UPDATE/DELETE) QPS: 10,000

## See also

* [TiDB Backup and Restore Use Cases](/br/backup-and-restore-use-cases.md)
* [br Command-line Manual](/br/use-br-command-line-tool.md)
* [Log Backup and PITR Architecture](/br/br-log-architecture.md)
