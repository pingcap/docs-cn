---
title: Deploy and Use BR
summary: Learn how to deploy and use BR.
---

# Deploy and Use BR

This document describes the recommended deployment of Backup & Restore (BR) and how to use BR to back up and restore data.

## Deploy BR

Recommended practices when deploying BR:

- In production environments, deploy BR on a node with at least 8 cores CPU and 16 GB memory. Select an appropriate OS version by following [Linux OS version requirements](/hardware-and-software-requirements.md#linux-os-version-requirements).
- Save backup data to Amazon S3, GCS or Azure Blob Storage.
- Allocate sufficient resources for backup and restoration；

    - BR, TiKV nodes, and the backup storage system should provide network bandwidth that is greater than the backup speed. If the target cluster is particularly large, the threshold of backup and restoration speed is limited by the bandwidth of the backup network.
    - The backup storage system should also provide sufficient write/read performance (IOPS). Otherwise, the IOPS might become a performance bottleneck during backup or restoration.
    - TiKV nodes need to have at least two additional CPU cores and high performance disks for backups. Otherwise, the backup might have an impact on the services running on the cluster.

> **Note**:
>
> - If no Network File System (NFS) is mounted to a BR or TiKV node, or if you use external storage that supports Amazon S3, GCS, or Azure Blob Storage protocols, the data backed up by BR is generated at each TiKV node. Because BR only backs up the leader replica, you need to estimate the space reserved on each node based on the leader size. Because TiDB uses the leader count for load balancing by default, leaders can greatly differ in size. This might result in the issue that the backup data is unevenly distributed on each node.
> - **Note that this is not the recommended way to deploy BR**, because the backup data are scattered in the local file system of each node. Collecting the backup data might result in data redundancy and operation and maintenance problems. Meanwhile, if you restore data directly before collecting the backup data, you will encounter the `SST file not found` error.

## Use BR

Currently, the following methods are supported to run the BR tool:

### Use SQL statements

TiDB supports both [`BACKUP`](/sql-statements/sql-statement-backup.md) and [`RESTORE`](/sql-statements/sql-statement-restore.md) SQL statements. You can monitor the progress of these operations using the statement [`SHOW BACKUPS|RESTORES`](/sql-statements/sql-statement-show-backups.md).

### Use the command-line tool

For details, see [Use BR Command-line for Backup and Restoration](/br/use-br-command-line-tool.md).

### Use BR in the Kubernetes environment

In a Kubernetes environment, you can use TiDB Operator to back up TiDB cluster data to Amazon S3, GCS or persistent volumes, and restore data from the backup data in such systems. For details, see [Back Up and Restore Data Using TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/stable/backup-restore-overview).
