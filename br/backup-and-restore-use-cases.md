---
title: TiDB Backup and Restore Use Cases
summary: Learn the use cases of backing up and restoring data using br command-line tool.
aliases: ['/docs/dev/br/backup-and-restore-use-cases/','/docs/dev/reference/tools/br/use-cases/','/tidb/dev/backup-and-restore-use-cases-for-maintain/']
---

# TiDB Backup and Restore Use Cases

[TiDB Snapshot Backup and Restore Guide](/br/br-snapshot-guide.md) and [TiDB Log Backup and PITR Guide](/br/br-pitr-guide.md) introduce the backup and restore solutions provided by TiDB, namely, snapshot (full) backup and restore, log backup and point-in-time recovery (PITR). This document helps you to quickly get started with the backup and restore solutions of TiDB in specific use cases.

Assume that you have deployed a TiDB production cluster on AWS and the business team requests the following requirements:

- Back up the data changes in a timely manner. When the database encounters a disaster, you can quickly recover the application with minimal data loss (only a few minutes of data loss is tolerable).
- Perform business audits every month at no specific time. When an audit request is received, you must provide a database to query the data at a certain time point of the past month as requested.

With PITR, you can satisfy the preceding requirements.

## Deploy the TiDB cluster and BR

To use PITR, you need to deploy a TiDB cluster >= v6.2.0 and update BR to the same version as the TiDB cluster. This document uses v6.6.0 as an example.

The following table shows the recommended hardware resources for using PITR in a TiDB cluster.

| Component | CPU | Memory | Disk | AWS instance  | Number of instances |
| --- | --- | --- | --- | --- | --- |
| TiDB | 8 core+ | 16 GB+ | SAS | c5.2xlarge | 2 |
| PD | 8 core+ | 16 GB+ | SSD | c5.2xlarge | 3 |
| TiKV | 8 core+ | 32 GB+ | SSD | m5.2xlarge | 3 |
| BR | 8 core+ | 16 GB+ | SAS | c5.2xlarge | 1 |
| Monitor | 8 core+ | 16 GB+ | SAS | c5.2xlarge | 1 |

> **Note:**
>
> - When BR runs backup and restore tasks, it needs to access PD and TiKV. Make sure that BR can connect to all PD and TiKV nodes.
> - BR and PD servers must use the same time zone.

Deploy or upgrade a TiDB cluster using TiUP:

- To deploy a new TiDB cluster, refer to [Deploy a TiDB cluster](/production-deployment-using-tiup.md).
- If the TiDB cluster is earlier than v6.2.0, upgrade it by referring to [Upgrade a TiDB cluster](/upgrade-tidb-using-tiup.md).

Install or upgrade BR using TiUP:

- Install:

    ```shell
    tiup install br:v6.6.0
    ```

- Upgrade:

    ```shell
    tiup update br:v6.6.0
    ```

## Configure backup storage (Amazon S3)

Before you start a backup task, prepare the backup storage, including the following aspects:

1. Prepare the S3 bucket and directory that stores the backup data.
2. Configure the permissions to access the S3 bucket.
3. Plan the subdirectory that stores each backup data.

The detailed steps are as follows:

1. Create a directory in S3 to store the backup data. The directory in this example is `s3://tidb-pitr-bucket/backup-data`.

    1. Create a bucket. You can choose an existing S3 to store the backup data. If there is none, refer to [AWS documentation: Creating a bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html) and create an S3 bucket. In this example, the bucket name is `tidb-pitr-bucket`.
    2. Create a directory for your backup data. In the bucket (`tidb-pitr-bucket`), create a directory named `backup-data`. For detailed steps, refer to [AWS documentation: Organizing objects in the Amazon S3 console using folders](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html).

2. Configure permissions for BR and TiKV to access the S3 directory. It is recommended to grant permissions using the IAM method, which is the most secure way to access the S3 bucket. For detailed steps, refer to [AWS documentation: Controlling access to a bucket with user policies](https://docs.aws.amazon.com/AmazonS3/latest/userguide/walkthrough1.html). The required permissions are as follows:

    - TiKV and BR in the backup cluster need `s3:ListBucket`, `s3:PutObject`, and `s3:AbortMultipartUpload` permissions of the `s3://tidb-pitr-bucket/backup-data` directory.
    - TiKV and BR in the restore cluster need `s3:ListBucket` and `s3:GetObject` permissions of the `s3://tidb-pitr-bucket/backup-data` directory.

3. Plan the directory structure that stores the backup data, including the snapshot (full) backup and the log backup.

    - All snapshot backup data are stored in the `s3://tidb-pitr-bucket/backup-data/snapshot-${date}` directory. `${date}` is the start time of the snapshot backup. For example, a snapshot backup starting at 2022/05/12 00:01:30 is stored in `s3://tidb-pitr-bucket/backup-data/snapshot-20220512000130`.
    - Log backup data are stored in the `s3://tidb-pitr-bucket/backup-data/log-backup/` directory.

## Determine the backup policy

To meet the requirements of minimum data loss, quick recovery, and business audits within a month, you can set the backup policy as follows:

- Run the log backup to continuously back up the data change in the database.
- Run a snapshot backup at 00:00 AM every two days.
- Retain the snapshot backup data and log backup data within 30 days and clean up backup data older than 30 days.

## Run log backup

After the log backup task is started, the log backup process runs in the TiKV cluster to continuously send the data change in the database to the S3 storage. To start a log backup task, run the following command:

```shell
tiup br log start --task-name=pitr --pd="${PD_IP}:2379" \
--storage='s3://tidb-pitr-bucket/backup-data/log-backup'
```

When the log backup task is running, you can query the backup status:

```shell
tiup br log status --task-name=pitr --pd="${PD_IP}:2379"

● Total 1 Tasks.
> #1 <
    name: pitr
    status: ● NORMAL
    start: 2022-05-13 11:09:40.7 +0800
      end: 2035-01-01 00:00:00 +0800
    storage: s3://tidb-pitr-bucket/backup-data/log-backup
    speed(est.): 0.00 ops/s
checkpoint[global]: 2022-05-13 11:31:47.2 +0800; gap=4m53s
```

## Run snapshot backup

You can run snapshot backup tasks on a regular basis using an automatic tool such as crontab. For example, run a snapshot backup at 00:00 every two days.

The following are two snapshot backup examples:

- Run a snapshot backup at 2022/05/14 00:00:00

    ```shell
    tiup br backup full --pd="${PD_IP}:2379" \
    --storage='s3://tidb-pitr-bucket/backup-data/snapshot-20220514000000' \
    --backupts='2022/05/14 00:00:00'
    ```

- Run a snapshot backup at 2022/05/16 00:00:00

    ```shell
    tiup br backup full --pd="${PD_IP}:2379" \
    --storage='s3://tidb-pitr-bucket/backup-data/snapshot-20220516000000' \
    --backupts='2022/05/16 00:00:00'
    ```

## Run PITR

Assume that you need to query the data at 2022/05/15 18:00:00. You can use PITR to restore a cluster to that time point by restoring a snapshot backup taken at 2022/05/14 and the log backup data between the snapshot and 2022/05/15 18:00:00.

The command is as follows:

```shell
tiup br restore point --pd="${PD_IP}:2379" \
--storage='s3://tidb-pitr-bucket/backup-data/log-backup' \
--full-backup-storage='s3://tidb-pitr-bucket/backup-data/snapshot-20220514000000' \
--restored-ts '2022-05-15 18:00:00+0800'

Full Restore <--------------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
[2022/05/29 18:15:39.132 +08:00] [INFO] [collector.go:69] ["Full Restore success summary"] [total-ranges=12] [ranges-succeed=xxx] [ranges-failed=0] [split-region=xxx.xxxµs] [restore-ranges=xxx] [total-take=xxx.xxxs] [restore-data-size(after-compressed)=xxx.xxx] [Size=xxxx] [BackupTS={TS}] [total-kv=xxx] [total-kv-size=xxx] [average-speed=xxx]
Restore Meta Files <--------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
Restore KV Files <----------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
[2022/05/29 18:15:39.325 +08:00] [INFO] [collector.go:69] ["restore log success summary"] [total-take=xxx.xx] [restore-from={TS}] [restore-to={TS}] [total-kv-count=xxx] [total-size=xxx]
```

## Clean up outdated data

You can clean up outdated data every two days using an automatic tool such as crontab.

For example, you can run the following commands to clean up outdated data:

- Delete snapshot data earlier than 2022/05/14 00:00:00

  ```shell
  rm s3://tidb-pitr-bucket/backup-data/snapshot-20220514000000
  ```

- Delete log backup data earlier than 2022/05/14 00:00:00

  ```shell
  tiup br log truncate --until='2022-05-14 00:00:00 +0800' --storage='s3://tidb-pitr-bucket/backup-data/log-backup'
  ```

## See also

- [Backup Storages](/br/backup-and-restore-storages.md)
- [Snapshot Backup and Restore Command Manual](/br/br-snapshot-manual.md)
- [Log Backup and PITR Command Manual](/br/br-pitr-manual.md)
