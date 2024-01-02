---
title: 2023-11-14 TiDB Cloud Dedicated Scale Feature Maintenance Notification
summary: Learn about the details of TiDB Cloud Dedicated Scale Feature Maintenance on November 14, 2023, such as the maintenance window and impact.
---

# [2023-11-14] TiDB Cloud Dedicated Scale Feature Maintenance Notification

This notification describes the details that you need to know about the maintenance for [Scale feature](https://docs.pingcap.com/tidbcloud/scale-tidb-cluster#scale-your-tidb-cluster) of TiDB Cloud Dedicated on November 14, 2023.

## Maintenance window

- Start time: 2023-11-14 16:00 (UTC+0)
- End time: 2023-11-21 16:00 (UTC+0)
- Duration: 7 days

> **Note:**
>
> Updated on 2023-11-16: The end time of the maintenance window has been extended from 2023-11-16 to 2023-11-21.

## Impact

During the maintenance window, [change vCPU and RAM](https://docs.pingcap.com/tidbcloud/scale-tidb-cluster#change-vcpu-and-ram) is disabled and you can not change vCPU and RAM for your Dedicated Clusters. However, you can still change the node number or storage in the Modify Cluster page. Your TiDB cluster will maintain its regular operations for data read and write, ensuring no adverse effects on your online business.

### Affected features of TiDB Cloud console UI

- Cluster level
    - Cluster management
        - Modify clusters
            - Change the vCPU and RAM of TiDB, TiKV, or TiFlash nodes.
 
### Affected features of TiDB Cloud API

- Cluster management
    - [UpdateCluster](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)

## Completion and resumption

Once the maintenance is successfully completed, the affected functionalities will be reinstated, offering you an even better experience.

## Get support

If you have any questions or need assistance, contact our [support team](/tidb-cloud/tidb-cloud-support.md). We are here to address your concerns and provide any necessary guidance.
