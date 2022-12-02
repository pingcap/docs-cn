---
title: Usage Overview of TiDB Backup and Restore
summary: Learn about how to deploy the backup and restore tool, and how to use it to back up and restore a TiDB cluster.
aliases: ['/tidb/dev/br-deployment/']
---

# Usage Overview of TiDB Backup and Restore

This document describes best practices of using TiDB backup and restore features, including how to choose a backup method, how to manage backup data, and how to install and deploy the backup and restore tool.

## Recommended practices

Before using TiDB backup and restore features, it is recommended that you understand the recommended backup and restore solutions.

### How to back up data?

**TiDB provides two types of backup. Which one should I use?** Full backup contains the full data of a cluster at a certain point in time. Log backup contains the data changes written to TiDB. It is recommended to use both types of backup at the same time:

- **[Start log backup](/br/br-pitr-guide.md#start-log-backup)**: Run the `br log start` command to start the log backup task. After that, the task keeps running on all TiKV nodes and backs up TiDB data changes to the specified storage in small batches regularly.
- **Perform [snapshot (full) backup](/br/br-snapshot-guide.md#back-up-cluster-snapshots) regularly**: Run the `br backup full` command to back up the snapshot of the cluster to the specified storage. For example, back up the cluster snapshot at 0:00 AM every day.

### How to manage backup data?

BR provides only basic backup and restore features, and does not support backup management. Therefore, you need to decide how to manage backup data on your own, which might involve the following questions?

* Which backup storage system should I choose?
* In which directory should I place the backup data during a backup task?
* In what way should I organize the directory of the full backup data and log backup data?
* How to handle the historical backup data in the storage system?

The following sections will answer these questions one by one.

**Choose a backup storage system**

It is recommended that you store backup data to Amazon S3, Google Cloud Storage (GCS), or Azure Blob Storage. Using these systems, you do not need to worry about the backup capacity and bandwidth allocation.

If the TiDB cluster is deployed in a self-built data center, the following practices are recommended:

* Build [MinIO](https://docs.min.io/docs/minio-quickstart-guide.html) as the backup storage system, and use the S3 protocol to back up data to MinIO.
* Mount Network File System (NFS, such as NAS) disks to br command-line tool and all TiKV instances, and use the POSIX file system interface to write backup data to the corresponding NFS directory.

> **Note:**
>
> If you do not choose NFS or a storage system that supports Amazon S3, GCS, or Azure Blob Storage protocols, the data backed up is generated at each TiKV node. **Note that this is not the recommended way to use BR**, because collecting the backup data might result in data redundancy and operation and maintenance problems.

**Organize the backup data directory**

* Store the snapshot backup and log backup in the same directory for unified management, for example, `backup-${cluster-id}`.
* Store each snapshot backup in a directory with the backup date included, for example, `backup-${cluster-id}/fullbackup-202209081330`.
* Store the log backup in a fixed directory, for example, `backup-${cluster-id}/logbackup`. The log backup program creates subdirectories under the `logbackup` directory every day to distinguish the data backed up each day.

**Handle historical backup data**

Assume that you need to set the life cycle for each backup data, for example, 7 days. Such a life cycle is called **backup retention period**, which will also be mentioned in backup tutorials.

* To perform PITR, you need to restore the full backup before the restore point, and the log backup between the full backup and the restore point. Therefore, **It is recommended to only delete the log backup before the full snapshot**. For log backups that exceed the backup retention period, you can use `br log truncate` command to delete the backup before the specified time point.
* For backup data that exceeds the retention period, you can delete or archive the backup directory.

### How to restore data?

- To restore only full backup data, you can use `br restore` to perform a full restore of the specified backup.
- If you have started log backup and regularly performed a full backup, you can run the `br restore point` command to restore data to any time point within the backup retention period.

## Deploy and use BR

To deploy BR, ensure that the following requirements are met:

- BR, TiKV nodes, and the backup storage system provide network bandwidth that is greater than the backup speed. If the target cluster is particularly large, the threshold of backup and restore speed is limited by the bandwidth of the backup network.
- The backup storage system provides sufficient read and write performance (IOPS). Otherwise, they might become a performance bottleneck during backup or restore.
- TiKV nodes have at least two additional CPU cores and high performance disks for backups. Otherwise, the backup might have an impact on the services running on the cluster.
- BR runs on a node with more than 8 cores and 16 GiB memory.

You can use backup and restore features in several ways, such as via the command-line tool, by running SQL commands, and using TiDB Operator. The following sections describe these three methods in detail.

### Use br command-line tool (recommended)

TiDB supports backup and restore using br command-line tool.

* You can run the `tiup install br` command to [install br command-line tool using TiUP online](/migration-tools.md#install-tools-using-tiup).
* For details about how to use `br` commands to back up and restore data, refer to the following documents:

    * [TiDB Snapshot Backup and Restore Guide](/br/br-snapshot-guide.md)
    * [TiDB Log Backup and PITR Guide](/br/br-pitr-guide.md)
    * [TiDB Backup and Restore Use Cases](/br/backup-and-restore-use-cases.md)

### Use SQL statements

TiDB supports full backup and restore using SQL statements:

- [`BACKUP`](/sql-statements/sql-statement-backup.md): backs up full snapshot data.
- [`RESTORE`](/sql-statements/sql-statement-restore.md): restores snapshot backup data.
- [`SHOW BACKUPS|RESTORES`](/sql-statements/sql-statement-show-backups.md): views the backup and restore progress.

### Use TiDB Operator on Kubernetes

On Kubernetes, you can use TiDB Operator to back up TiDB cluster data to Amazon S3, GCS, or Azure Blob Storage, and restore data from the backup data in such systems. For details, see [Back Up and Restore Data Using TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/stable/backup-restore-overview).

## See also

- [TiDB Backup and Restore Overview](/br/backup-and-restore-overview.md)
- [TiDB Backup and Restore Architecture](/br/backup-and-restore-design.md)
