---
title: 2023-09-26 TiDB Cloud Console Maintenance Notification
summary: Learn about the details of the TiDB Cloud Console maintenance on Sep 26, 2023, such as the maintenance window, reason, and impact.
---

# [2023-09-26] TiDB Cloud Console Maintenance Notification

This notification describes the details that you need to know about the [TiDB Cloud console](https://tidbcloud.com/) maintenance on September 26, 2023.

## Maintenance window

- Date: 2023-09-26
- Start time: 8:00 (UTC+0)
- End time: 8:30 (UTC+0)
- Duration: Approximately 30 minutes

> **Note:**
>
> Currently, the overall maintenance schedule for the TiDB Cloud Console does not support user modifications to the maintenance timing.

## Reason for maintenance

We're upgrading the management infrastucture of the TiDB Cloud Serverless to enhance performance and efficiency, delivering a better experience for all users. This is part of our ongoing commitment to providing high-quality services.

## Impact

During the maintenance window, you might experience intermittent disruptions in functionalities related to creating and updating within the TiDB Cloud console UI and API. However, your TiDB cluster will maintain its regular operations for data read and write, ensuring no adverse effects on your online business.

### Affected features of TiDB Cloud console UI

- Cluster level
    - Cluster management
        - Create clusters
        - Delete clusters
        - Scale clusters
        - View clusters
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

- All [API requests](https://docs.pingcap.com/tidbcloud/api/v1beta) will be responded with 500.
- [Data Service API](https://docs.pingcap.com/tidbcloud/data-service-overview) will not be affected.

## Completion and resumption

Once the maintenance is successfully completed, the affected functionalities will be reinstated, offering you an even better experience.

## Get support

If you have any questions or need assistance, contact our [support team](/tidb-cloud/tidb-cloud-support.md). We are here to address your concerns and provide any necessary guidance.