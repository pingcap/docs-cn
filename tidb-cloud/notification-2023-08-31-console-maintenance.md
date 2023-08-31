---
title: 2023-08-31 TiDB Cloud Console Maintenance Notification
summary: Learn about the details of the TiDB Cloud Console maintenance on August 31, 2023, such as the maintenance window, reason, and impact.
---

# [2023-08-31] TiDB Cloud Console Maintenance Notification

This notification describes the details that you need to know about the [TiDB Cloud console](https://tidbcloud.com/) maintenance on August 31, 2023.

## Maintenance window

- Date: 2023-08-31
- Start time: 8:00 (UTC+0)
- End time: 10:00 (UTC+0)
- Duration: Approximately 2 hours

> **Note:**
>
> Currently, users cannot modify the maintenance timing for the TiDB Cloud console, so you need to plan accordingly in advance.

## Reason for maintenance

We are upgrading the meta database services of the TiDB Cloud console to enhance performance and efficiency. This improvement aims to provide a better experience for all users as part of our ongoing commitment to delivering high-quality services.

## Impact

During the maintenance window, you might experience intermittent disruptions in functionalities related to creating and updating within the TiDB Cloud console UI and API. However, your TiDB cluster will maintain its regular operations for data read and write, ensuring no adverse effects on your online business.

### Affected features of TiDB Cloud console UI

- Cluster level
    - Cluster management
        - Create clusters
        - Delete clusters
        - Scale clusters
        - Pause or Resume clusters
        - Change cluster password
        - Change cluster traffic filter
    - Import
        - Create an import job
    - Data Migration
        - Create a migration job
    - Changefeed
        - Create a changefeed job
    - Backup
        - Create a manual backup job
        - Auto backup job
    - Restore
        - Create a restore Job
    - Database audit log
        - Test connectivity
        - Add or delete access record
        - Enable or disable Database audit logging
        - Restart database audit logging
- Project level
    - Network access
        - Create a private endpoint
        - Delete a private endpoint
        - Add VPC Peering
        - Delete VPC Peering
    - Maintenance
        - Change maintenance window
        - Defer task
    - Recycle Bin
        - Delete clusters
        - Delete backups
        - Restore clusters

### Affected features of TiDB Cloud API

- Cluster management
    - [CreateCluster](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/CreateCluster)
    - [DeleteCluster](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/DeleteCluster)
    - [UpdateCluster](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)
    - [CreateAwsCmek](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/CreateAwsCmek)
- Backup
    - [CreateBackup](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Backup/operation/CreateBackup)
    - [DeleteBackup](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Backup/operation/DeleteBackup)
- Restore
    - [CreateRestoreTask](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Restore/operation/CreateRestoreTask)
- Import
    - [CreateImportTask](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Import/operation/CreateImportTask)
    - [UpdateImportTask](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Import/operation/UpdateImportTask)

## Completion and resumption

Once the maintenance is successfully completed, the affected functionalities will be reinstated, offering you an even better experience.

## Get support

If you have any questions or need assistance, contact our [support team](/tidb-cloud/tidb-cloud-support.md). We are here to address your concerns and provide any necessary guidance.
