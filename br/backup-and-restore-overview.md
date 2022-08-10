---
title: BR Overview
summary: Learn about the definition and functions of BR.
aliases: ['/docs/dev/br/backup-and-restore-tool/','/docs/dev/reference/tools/br/br/','/docs/dev/how-to/maintain/backup-and-restore/br/','/tidb/dev/backup-and-restore-tool']
---

# BR Overview

[BR](https://github.com/pingcap/tidb/tree/master/br) (Backup & Restore) is a command-line tool for **distributed backup and restoration** of the TiDB cluster data. In addition to regular backup and restoration, you can also use BR for large-scale data migration as long as compatibility is ensured.

This document describes BR's architecture, features, and usage tips.

## BR architecture

BR sends a backup or restoration command to each TiKV node. After receiving the command, TiKV performs the corresponding backup or restoration operation.

Each TiKV node has a path in which the backup files generated in the backup operation are stored and from which the stored backup files are read during the restoration.

![br-arch](/media/br-arch.png)

For detailed information about the BR design, see [BR Design Principles](/br/backup-and-restore-design.md).

## BR features

This section describes BR features and the performance impact.

### Back up TiDB cluster data

- **Back up cluster snapshots**: A snapshot of a TiDB cluster contains transactionally consistent data at a specific time. You can back up snapshot data of a TiDB cluster using BR. For details, see [Back up TiDB cluster snapshots](/br/br-usage-backup.md#back-up-tidb-cluster-snapshots).
- **Back up incremental data**: The incremental data of a TiDB cluster represents changes between the latest snapshot and the previous snapshot. Incremental data is smaller in size compared with full data, and can be used together with snapshot backup, which reduces the volume of backup data. For details, see [Back up incremental data](/br/br-usage-backup.md#back-up-incremental-data).
- **Back up a database or table**: On top of snapshot and incremental data backup, BR supports backing up a specific database or table and filtering out unnecessary data. For details, see [Back up a database or table](/br/br-usage-backup.md#back-up-a-database-or-a-table).
- **Encrypt backup data**: BR supports backup data encryption and Amazon S3 server-side encryption. You can select an encryption method as needed. For details, see [Encrypt backup data](/br/br-usage-backup.md#encrypt-backup-data).

#### Impact on performance

The impact of backup on a TiDB cluster is kept below 20%, and this value can be reduced to 10% or less with the proper configuration of the TiDB cluster. The backup speed of a TiKV node is scalable and ranges from 50 MB/s to 100 MB/s. For more information, see [Backup performance and impact](/br/br-usage-backup.md#backup-performance-and-impact).

#### Storage types of backup data

BR supports backing up data to Amazon S3, Google Cloud Storage, Azure Blob Storage, NFS, and other S3-compatible file storage services. For details, see [Back up data to external storages](/br/br-usage-backup.md#back-up-data-to-external-storage).

### Restore TiDB cluster data

- **Restore snapshot backup**: You can restore snapshot backup data to a new cluster. For details, see [Restore TiDB cluster snapshots](/br/br-usage-restore.md#restore-tidb-cluster-snapshots).
- **Restore incremental backup**: You can restore the incremental backup data to a cluster. For details, see [Restore incremental backup](/br/br-usage-restore.md#restore-incremental-data).
- **Restore a database or a table from backup**: You can restore part of a specific database or table. During the process, BR will filter out unnecessary data. For details, see [Restore a database or a table](/br/br-usage-restore.md#restore-a-database-or-a-table).

#### Impact on performance

Data restoration is performed at a scalable speed. Generally, the speed is 100 MB/s per TiKV node. BR only supports restoring data to a new cluster and uses the resources of the target cluster as much as possible. For more details, see [Restoration performance and impact](/br/br-usage-restore.md#restoration-performance-and-impact).

## Before you use BR

Before you use BR, pay attention to its usage restrictions, compatibility, and other considerations.

### Usage restrictions

This section describes usage restrictions of BR.

#### Unsupported scenarios

When BR restores data to the upstream cluster of TiCDC or TiDB Binlog, TiCDC or TiDB Binlog cannot replicate the restored data to the downstream cluster.

#### Compatibility

The compatibility issues of BR and a TiDB cluster are as follows:

- There is a cross-version compatibility issue:

    Before v5.4.0, BR cannot restore tables with `charset=GBK`. At the same time, no version of BR supports restoring `charset=GBK` tables to a TiDB cluster earlier than v5.4.0.

- The KV format might change when some features are enabled or disabled. If these features are not consistently enabled or disabled during backup and restoration, compatibility issues might occur.

These features are as follows:

| Feature | Issue | Solution |
|  ----  | ----  | ----- |
| Clustered index | [#565](https://github.com/pingcap/br/issues/565)       | Make sure that the value of the `tidb_enable_clustered_index` global variable during restoration is consistent with that during backup. Otherwise, data inconsistency might occur, such as `default not found` and inconsistent data index. |
| New collation  | [#352](https://github.com/pingcap/br/issues/352)       | Make sure that the value of the `new_collations_enabled_on_first_bootstrap` variable during restoration is consistent with that during backup. Otherwise, inconsistent data index might occur and checksum might fail to pass. |
| Global temporary tables | | Make sure that you are using BR v5.3.0 or a later version to back up and restore data. Otherwise, an error occurs in the definition of the backed global temporary tables. |

However, even after you have ensured that the preceding features are consistently enabled or disabled during backup and restoration, compatibility issues might still occur due to the inconsistent internal versions or inconsistent interfaces between BR and TiKV/TiDB/PD. To avoid such cases, BR provides a built-in version check.

#### Version check

Before performing backup and restoration, BR compares and checks the TiDB cluster version and the BR version. If there is a major-version mismatch (for example, BR v4.x and TiDB v5.x), BR prompts a reminder to exit. To forcibly skip the version check, you can set `--check-requirements=false`. Note that skipping the version check might introduce incompatibility.

The version compatibility mapping between BR and TiDB versions are as follows:

| Backup version (vertical) \ Restoration version (horizontal) | Use BR v5.4 to restore TiDB v5.4 | Use BR v6.0 to restore TiDB v6.0 | Use BR v6.1 to restore TiDB v6.1 | Use BR v6.2 to restore TiDB v6.2 |
|  ----  |  ----  | ---- | ---- | ---- |
| Use BR v5.4 to back up TiDB v5.4 | Compatible | Incompatible (Before restoration, modify the restoration cluster to use the same [new collation](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) as the backup cluster.) | Incompatible (Before restoration, modify the restoration cluster to use the same [new collation](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) as the backup cluster.) | Incompatible (Before restoration, modify the restoration cluster to use the same [new collation](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) as the backup cluster.) |
| Use BR v6.0 to back up TiDB v6.0 | Incompatible | Compatible | Compatible | Compatible |
| Use BR v6.1 to back up TiDB v6.1 | Incompatible | Compatible (A known issue [#36379](https://github.com/pingcap/tidb/issues/36379): if backup data contains an empty schema, BR might report an error.) | Compatible | Compatible |
| Use BR v6.2 to back up TiDB v6.2 | Incompatible | Compatible (A known issue [#36379](https://github.com/pingcap/tidb/issues/36379): if backup data contains an empty schema, BR might report an error.) | Compatible | Compatible |

#### Some tips

The following are some recommended operations for using BR:

- It is recommended that you perform the backup operation during off-peak hours to minimize the impact on applications.
- BR only supports restoring data to a new cluster and uses resources of the target cluster as much as possible. Therefore, it is not recommended that you restore data to a production cluster. Otherwise, services might be affected.
- It is recommended that you execute multiple backup or restoration operations one by one. Running backup or restoration operations in parallel reduces performance and also affects online applications. Worse still, lack of collaboration between multiple tasks might result in task failures and affect cluster performance.
- Amazon S3, Google Cloud Storage, and Azure Blob Storage are recommended to store backup data.
- Make sure that the BR and TiKV nodes, and the backup storage system have sufficient network bandwidth to ensure sound write/read performance. Insufficient storage capacity might be the bottleneck for a backup or restoration operation.

### See also

- [Back up Data to S3-Compatible Storage Using BR](https://docs.pingcap.com/tidb-in-kubernetes/stable/backup-to-aws-s3-using-br)
- [Restore Data from S3-Compatible Storage Using BR](https://docs.pingcap.com/tidb-in-kubernetes/stable/restore-from-aws-s3-using-br)
- [Back up Data to GCS Using BR](https://docs.pingcap.com/tidb-in-kubernetes/stable/backup-to-gcs-using-br)
- [Restore Data from GCS Using BR](https://docs.pingcap.com/tidb-in-kubernetes/stable/restore-from-gcs-using-br)
- [Back up Data to PV](https://docs.pingcap.com/tidb-in-kubernetes/stable/backup-to-pv-using-br)
- [Restore Data from PV](https://docs.pingcap.com/tidb-in-kubernetes/stable/restore-from-pv-using-br)
