---
title: Overview of TiDB Backup & Restore Architecture
summary: TiDB supports backup and restore for cluster data using Backup & Restore (BR) and TiDB Operator. Tasks can be created to back up data from TiKV nodes and restore data to TiKV nodes. The architecture includes full data backup and restore, data change log backup, and point-in-time recovery (PITR). For details, refer to specific documents for each feature.
---

# Overview of TiDB Backup & Restore Architecture

As described in [TiDB Backup & Restore Overview](/br/backup-and-restore-overview.md), TiDB supports backing up and restoring multiple types of cluster data. You can use Backup & Restore (BR) and TiDB Operator to access these features, and create tasks to back up data from TiKV nodes or restore data to TiKV nodes.

For details about the architecture of each backup and restore feature, see the following documents:

- Full data backup and restore

    - [Back up snapshot data](/br/br-snapshot-architecture.md#process-of-backup)
    - [Restore snapshot backup data](/br/br-snapshot-architecture.md#process-of-restore)

- Data change log backup

    - [Log backup: backup of KV data change](/br/br-log-architecture.md#process-of-log-backup)

- Point-in-time recovery (PITR)

    - [PITR](/br/br-log-architecture.md#process-of-pitr)
